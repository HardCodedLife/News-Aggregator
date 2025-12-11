from pydantic import BaseModel
from typing import List, Optional

# --- Ingestion Schemas ---
class NewsIngest(BaseModel):
    title: str
    content: str
    url: str

# --- Chat Schemas ---
class ChatRequest(BaseModel):
    question: str

class Source(BaseModel):
    title: str
    url: str
    score: float # Confidence score (0 to 1)

class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]
