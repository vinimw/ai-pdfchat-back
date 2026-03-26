from pydantic import BaseModel


class DocumentChunk(BaseModel):
    index: int
    text: str
    start_char: int
    end_char: int