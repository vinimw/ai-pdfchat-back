from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    document_id: str
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)