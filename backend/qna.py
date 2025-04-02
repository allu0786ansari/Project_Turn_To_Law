import os
import shutil
import faiss
import numpy as np
import pickle
import google.generativeai as genai
from fastapi import UploadFile
import pypdf
import docx
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import RecursiveCharacterTextSplitter
from db import get_db_connection
from config import GOOGLE_API_KEY

# Configure Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-pro")

# Embedding Model (Consistent with other modules)
embedding_model = SentenceTransformer("sentence-transformers/msmarco-distilbert-base-v4")

# FAISS Index (Persisted)
embedding_dim = 768  # Adjusted based on selected model
faiss_index_path = "models/faiss_index.bin"

if os.path.exists(faiss_index_path):
    faiss_index = faiss.read_index(faiss_index_path)
else:
    faiss_index = faiss.IndexFlatL2(embedding_dim)

UPLOAD_DIR = "uploaded_docs/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_file(uploaded_file: UploadFile) -> str:
    """Save uploaded file to the server."""
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(uploaded_file.file, buffer)
    return file_path

def extract_text(file_path: str) -> str:
    """Extract text from PDF or DOCX."""
    ext = file_path.split(".")[-1].lower()
    if ext == "pdf":
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    elif ext == "docx":
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX.")

def store_document_in_db(filename: str, content: str):
    """Store extracted text in MySQL."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO documents (filename, content) VALUES (%s, %s) ON DUPLICATE KEY UPDATE content=%s",
                   (filename, content, content))
    db.commit()
    cursor.close()
    db.close()

def store_embeddings_in_db(doc_id: int, embeddings: np.ndarray):
    """Store document embeddings in MySQL."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("INSERT INTO document_embeddings (doc_id, embedding) VALUES (%s, %s)",
                   (doc_id, pickle.dumps(embeddings)))
    db.commit()
    cursor.close()
    db.close()

def split_document(text: str, chunk_size: int = 1024, chunk_overlap: int = 100):
    """Splits large legal documents into manageable chunks."""
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

def process_document(uploaded_file: UploadFile) -> str:
    """Process and store document with embeddings."""
    file_path = save_file(uploaded_file)
    extracted_text = extract_text(file_path)
    
    # Store document in MySQL
    store_document_in_db(uploaded_file.filename, extracted_text)

    # Generate and store embeddings
    chunks = [extracted_text[i:i+512] for i in range(0, len(extracted_text), 512)]
    chunk_embeddings = embedding_model.encode(chunks)

    global faiss_index
    faiss_index.add(np.array(chunk_embeddings, dtype=np.float32))
    faiss.write_index(faiss_index, faiss_index_path)  # Persist FAISS index

    return f"Document '{uploaded_file.filename}' processed successfully."

def search_relevant_text(file_name: str, query: str) -> str:
    """Find the most relevant text chunk from the document using FAISS."""
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("SELECT content FROM documents WHERE filename = %s", (file_name,))
    result = cursor.fetchone()
    cursor.close()
    db.close()

    if not result or not result[0]:
        return ""

    document_text = result[0]
    chunks = [document_text[i:i+512] for i in range(0, len(document_text), 512)]
    chunk_embeddings = embedding_model.encode(chunks)
    
    query_embedding = embedding_model.encode([query])[0]
    distances, indices = faiss_index.search(np.array([query_embedding], dtype=np.float32), k=1)

    return chunks[indices[0][0]] if indices[0][0] < len(chunks) else ""

def query_document(file_name: str, question: str) -> dict:
    """Ask a question about a document using Gemini AI."""
    relevant_text = search_relevant_text(file_name, question)
    
    if not relevant_text:
        return {"error": "Document not found or no relevant information available."}

    prompt = f"""
    You are a legal assistant. Answer based on the document below.

    Document Context:
    {relevant_text}

    Question: {question}
    """

    try:
        response = gemini_model.generate_content(prompt)
        return {
            "question": question,
            "answer": response.text,
            "source": file_name
        }
    except Exception as e:
        return {"error": f"AI processing failed: {e}"}
