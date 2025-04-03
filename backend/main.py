from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import mimetypes
import pytesseract
from PIL import Image
import pypdf
import docx

# Import necessary modules
from qna import process_document, query_document  # Q&A functionalities
from news import get_indian_legal_news  # Legal news summarization
from fact_check import fact_check_legal_claim  # Fact-checking functionality

app = FastAPI()

# ✅ Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Ensure Upload Directory Exists
UPLOAD_DIR = "uploaded_docs/"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def extract_text_from_file(file_path: str, file_type: str) -> str:
    """
    Extract text from various file types.
    Args:
        file_path (str): Path to the uploaded file.
        file_type (str): MIME type of the file.
    Returns:
        str: Extracted text.
    """
    try:
        if file_type in ["application/pdf"]:
            # Extract text from PDF
            with open(file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif file_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
            # Extract text from DOCX
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
        elif file_type in ["text/plain"]:
            # Extract text from TXT
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        elif file_type in ["image/png", "image/jpeg", "image/jpg"]:
            # Extract text from images using OCR
            image = Image.open(file_path)
            return pytesseract.image_to_string(image)
        else:
            raise ValueError("Unsupported file type.")
    except Exception as e:
        print(f"Error extracting text from file: {e}")
        raise HTTPException(status_code=400, detail="Failed to extract text from the uploaded file.")

@app.get("/")
def home():
    """API Home Endpoint."""
    return {"message": "Smart Document Q&A System is running with Gemini AI"}

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    """
    Uploads a file, extracts text, and processes embeddings in memory.
    """
    try:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Detect file type
        file_type, _ = mimetypes.guess_type(file_path)
        if not file_type:
            raise HTTPException(status_code=400, detail="Could not determine file type.")

        # Extract text based on file type
        extracted_text = extract_text_from_file(file_path, file_type)

        # Process the document (if needed for embeddings)
        result = process_document(file)

        # Cleanup uploaded file
        os.remove(file_path)

        return {
            "document_id": result.get("document_id", "unknown"),
            "message": "File processed successfully.",
            "content": extracted_text,  # Return extracted text for Q&A use
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# ✅ Request Model for Q&A
class QnARequest(BaseModel):
    question: str
    document_text: str  # Directly pass the document content

@app.post("/qna/")
async def ask_qna(request: QnARequest):
    """
    Handles Q&A on legal documents without storing embeddings in DB.
    """
    try:
        response = query_document(request.question, request.document_text)

        if "error" in response:
            return {"response": response["error"]}

        return {"response": response["answer"], "source": response.get("source", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during Q&A: {str(e)}")

@app.get("/news/")
def get_legal_news():
    """
    Fetches the latest Indian legal news summaries.
    """
    try:
        news = get_indian_legal_news()
        return {"news": news}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching legal news: {str(e)}")

# ✅ Request Model for Fact-Checking
class FactCheckRequest(BaseModel):
    claim: str

@app.post("/fact-check/")
async def fact_check(request: FactCheckRequest):
    """
    Fact-checks a legal claim using trusted sources.
    """
    try:
        response = fact_check_legal_claim(request.claim)

        if "error" in response:
            return {"response": response["error"]}

        return {
            "claim": request.claim,
            "verified_sources": response["verified_sources"],
            "confidence_score": response.get("confidence_score", 0),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during fact-checking: {str(e)}")