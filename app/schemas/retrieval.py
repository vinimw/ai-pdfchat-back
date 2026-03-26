from pydantic import BaseModel

class RetrievedChunk(BaseModel):
    chunk_index: int
    text: str
    score: float
    start_char: int
    end_char: int