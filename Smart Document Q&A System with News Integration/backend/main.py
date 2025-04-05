from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

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
        # Process the document and generate a unique document ID
        result = process_document(file)

        # Check if document processing was successful
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])

        return {
            "document_id": result["document_id"],  # Return the unique document ID
            "message": result["message"],
            "content": result["content"],  # Return extracted text for Q&A use
        }
    except Exception as e:
        print(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# ✅ Request Model for Q&A
class QnARequest(BaseModel):
    question: str
    document_id: str  # Pass the document ID
    document_text: str  # Pass the document content

@app.post("/qna/")
async def ask_qna(request: QnARequest):
    """
    Handles Q&A on legal documents using the document ID and content.
    """
    try:
        print("Received QnA request:", request.dict())  # Debugging log

        # Pass the document ID and content to the Q&A function
        response = query_document(request.question, request.document_id, request.document_text)

        if "error" in response:
            return {"response": response["error"]}

        return {
            "response": response["answer"],
            "source": response.get("source", ""),
            "document_id": response.get("document_id", ""),
        }
    except Exception as e:
        print(f"Error during Q&A: {e}")
        raise HTTPException(status_code=500, detail=f"Error during Q&A: {str(e)}")

@app.get("/news/")
def get_legal_news(keywords: Optional[List[str]] = Query(None)):
    """Fetches the latest Indian legal news summaries."""
    try:
        print(f"Fetching legal news with keywords: {keywords}")
        # Filter out empty keywords
        filtered_keywords = [k for k in (keywords or []) if k and k.strip()]
        news = get_indian_legal_news(keywords=filtered_keywords)
        return {"news": news or []}
    except Exception as e:
        print(f"Error fetching legal news: {e}")
        return {"news": []}

# ✅ Request Model for Fact-Checking
class FactCheckRequest(BaseModel):
    claim: str

@app.post("/fact-check/")
async def fact_check(request: FactCheckRequest):
    """
    Fact-checks a legal claim using trusted sources.
    """
    try:
        print("Received Fact-Check request:", request.dict())  # Debugging log

        # Call the fact_check_legal_claim function from fact_check.py
        response = fact_check_legal_claim(request.claim)

        # Check if the response contains an error
        if "error" in response:
            return {"response": response["error"]}

        # Return the full response from fact_check_legal_claim
        return response
    except Exception as e:
        print(f"Error during fact-checking: {e}")
        raise HTTPException(status_code=500, detail=f"Error during fact-checking: {str(e)}")
