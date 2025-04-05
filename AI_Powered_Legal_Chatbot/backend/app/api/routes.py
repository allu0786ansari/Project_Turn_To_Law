from fastapi import APIRouter
from pydantic import BaseModel
from app.services.qa_service import get_response

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
def handle_query(request: QueryRequest):
    response = get_response(request.question)
    return {"answer": response}