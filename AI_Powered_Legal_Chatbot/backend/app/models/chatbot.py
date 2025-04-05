from pydantic import BaseModel

class ChatbotQuery(BaseModel):
    question: str

class ChatbotResponse(BaseModel):
    answer: str