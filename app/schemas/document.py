from pydantic import BaseModel


class DocumentExtractResponse(BaseModel):
    filename: str
    pages: int
    characters: int
    text: str