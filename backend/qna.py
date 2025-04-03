import os
import shutil
import faiss
import numpy as np
import uuid
from fastapi import UploadFile
import pypdf
import docx
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai
from config import GOOGLE_API_KEY

# Configure Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-pro")

# Embedding Model
embedding_model = SentenceTransformer("sentence-transformers/msmarco-distilbert-base-v4")
embedding_dim = embedding_model.get_sentence_embedding_dimension()

# FAISS Index (In-Memory)
faiss_index = faiss.IndexFlatL2(embedding_dim)

UPLOAD_DIR = "uploaded_docs/"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_file(uploaded_file: UploadFile, doc_id: str) -> str:
    """Save uploaded file to the server with a unique document ID prefix."""
    filename = f"{doc_id}_{uploaded_file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return file_path


def extract_text(file_path: str) -> str:
    """Extract text from PDF or DOCX."""
    ext = file_path.split(".")[-1].lower()
    extracted_text = ""

    try:
        if (ext == "pdf"):
            with open(file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                extracted_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif ext == "docx":
            doc = docx.Document(file_path)
            extracted_text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        else:
            raise ValueError("Unsupported file format. Please upload a PDF or DOCX.")
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

    return extracted_text.strip()


def split_document(text: str, chunk_size: int = 1024, chunk_overlap: int = 100):
    """Splits large legal documents into manageable chunks using LangChain."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)


def process_document(uploaded_file: UploadFile) -> dict:
    """Process document and store embeddings only in runtime (not in DB)."""
    doc_id = str(uuid.uuid4())[:8]  # Generate unique document ID
    file_path = save_file(uploaded_file, doc_id)
    extracted_text = extract_text(file_path)

    if not extracted_text:
        # Cleanup uploaded file if no text is extracted
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
        return {"error": "Document contains no extractable text."}

    # Generate embeddings dynamically
    chunks = split_document(extracted_text)
    if not chunks:
        try:
            os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")
        return {"error": "Document chunking failed; no valid text chunks found."}

    chunk_embeddings = embedding_model.encode(chunks)

    global faiss_index
    faiss_index.reset()  # Clear the FAISS index before adding new embeddings
    faiss_index.add(np.array(chunk_embeddings, dtype=np.float32))  # In-memory FAISS index

    # Cleanup uploaded file after processing
    try:
        os.remove(file_path)
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")

    return {
        "document_id": doc_id,
        "message": f"Document '{uploaded_file.filename}' processed successfully.",
        "content": extracted_text  # Return content for runtime use
    }


def search_relevant_text(query: str, document_text: str) -> str:
    """Find the most relevant text chunk dynamically (no DB)."""
    chunks = split_document(document_text)
    if not chunks:
        return ""

    chunk_embeddings = embedding_model.encode(chunks)
    query_embedding = embedding_model.encode([query])[0]

    if faiss_index.ntotal == 0:
        return ""

    distances, indices = faiss_index.search(np.array([query_embedding], dtype=np.float32), k=1)

    # Ensure the index is valid
    if indices[0][0] < len(chunks):
        return chunks[indices[0][0]]
    return ""


def query_document(question: str, document_text: str) -> dict:
    """Ask a question about a document using Gemini AI (no DB storage)."""
    relevant_text = search_relevant_text(question, document_text)

    if not relevant_text:
        return {"error": "No relevant information found in the document."}

    prompt = f"""
    You are a legal assistant. Answer based on the document below.

    Document Context:
    {relevant_text}

    Question: {question}
    """

    try:
        response = gemini_model.generate_content(prompt)
        if response and hasattr(response, "text"):
            return {
                "question": question,
                "answer": response.text,
                "source": relevant_text  # Include the relevant text as the source
            }
        else:
            return {"error": "No response generated by the AI."}
    except Exception as e:
        print(f"Error during AI processing: {e}")
        return {"error": f"AI processing failed: {e}"}
