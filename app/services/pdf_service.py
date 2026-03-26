from fastapi import UploadFile


class PdfService:
    @staticmethod
    async def read_bytes(file: UploadFile) -> bytes:
        return await file.read()