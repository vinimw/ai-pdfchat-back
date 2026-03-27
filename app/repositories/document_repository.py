from typing import Optional

from sqlalchemy.orm import Session

from app.models.document import DocumentModel


class DocumentRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(
        self,
        document_id: str,
        collection_name: str,
        filename: str,
        stored_filename: str,
        file_path: str,
        pages: int,
        characters: int,
    ) -> DocumentModel:
        document = DocumentModel(
            document_id=document_id,
            collection_name=collection_name,
            filename=filename,
            stored_filename=stored_filename,
            file_path=file_path,
            pages=pages,
            characters=characters,
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document

    def list_all(self) -> list[DocumentModel]:
        return self.db.query(DocumentModel).order_by(DocumentModel.created_at.desc()).all()

    def get_by_id(self, document_id: str) -> Optional[DocumentModel]:
        return (
            self.db.query(DocumentModel)
            .filter(DocumentModel.document_id == document_id)
            .first()
        )

    def delete(self, document: DocumentModel) -> None:
        self.db.delete(document)
        self.db.commit()