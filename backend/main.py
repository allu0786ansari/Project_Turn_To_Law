from fastapi import FastAPI, UploadFile, Form, File
from qna import process_document, query_document
from news import get_indian_legal_news
from db import initialize_db
from fact_check import fact_check_legal_claim
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
import os

app = FastAPI()

# ✅ Allow CORS for frontend at http://localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this if deployed elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads/"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure upload directory exists

@app.get("/")
def home():
    return {"message": "Smart Document Q&A System is running with Gemini AI"}

@app.post("/upload/")
async def upload_document(file: UploadFile = File(...)):
    """Upload a legal document and store it."""
    try:
        doc_id = str(uuid4())[:8]  # ✅ Generate unique document ID
        file_path = os.path.join(UPLOAD_DIR, f"{doc_id}_{file.filename}")

        with open(file_path, "wb") as f:
            f.write(await file.read())

        # If you have a processing function, call it
        # process_document(file_path)  # Uncomment if needed

        return {"document_id": doc_id, "filename": file.filename}  # ✅ Send document_id
    except Exception as e:
        return {"error": str(e)}

@app.post("/ask/")
async def ask_question(file_name: str = Form(...), question: str = Form(...)):
    """Ask a question about an uploaded document."""
    return query_document(file_name, question)

@app.get("/news/")
def get_legal_news():
    return get_indian_legal_news()

@app.post("/fact-check/")
async def fact_check(claim: str = Form(...)):
    """Fact-check a legal claim using trusted sources."""
    return fact_check_legal_claim(claim)

initialize_db()
