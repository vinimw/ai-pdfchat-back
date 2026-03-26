from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    document_id: str = Field(min_length=1)
    collection_name: str = Field(min_length=3)
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)