from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

class FileStorageService:
    STORAGE_DIR = Path("storage/documents")

    @classmethod
    def ensure_storage_dir(cls) -> None:
        cls.STORAGE_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    async def save_upload(cls, file: UploadFile) -> tuple[str, str]:
        cls.ensure_storage_dir()

        extension = Path(file.filename or "document.pdf").suffix or ".pdf"
        stored_filename = f"{uuid4()}{extension}"
        stored_path = cls.STORAGE_DIR / stored_filename

        content = await file.read()
        stored_path.write_bytes(content)

        return stored_filename, str(stored_path)