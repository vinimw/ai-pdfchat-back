from fastapi import FastAPI
from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.query import router as query_router
from app.api.routes.upload import router as upload_router
from app.db.database import Base, engine
from app.api.routes.documents import router as documents_router
from app.services.document_service import DocumentService
from app.services.vector_store_service import VectorStoreService

from app.models.document import DocumentModel

DocumentService.ensure_storage_dir()
VectorStoreService.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI PDF Chat API",
    version="0.1.0",
)

app.include_router(health_router, prefix="/api")
app.include_router(upload_router, prefix="/api")
app.include_router(query_router, prefix="/api")
app.include_router(chat_router, prefix="/api")
app.include_router(documents_router, prefix="/api")
