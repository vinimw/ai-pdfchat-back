from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.repositories.document_repository import DocumentRepository

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def setup_function():
    Base.metadata.create_all(bind=engine)


def teardown_function():
    Base.metadata.drop_all(bind=engine)


def test_create_and_get_document() -> None:
    db = TestingSessionLocal()
    repository = DocumentRepository(db)

    repository.create(
        document_id="doc-1",
        collection_name="document_doc-1",
        filename="sample.pdf",
        pages=1,
        characters=100,
    )

    document = repository.get_by_id("doc-1")

    assert document is not None
    assert document.filename == "sample.pdf"
    db.close()


def test_list_all_documents() -> None:
    db = TestingSessionLocal()
    repository = DocumentRepository(db)

    repository.create(
        document_id="doc-1",
        collection_name="document_doc-1",
        filename="sample.pdf",
        pages=1,
        characters=100,
    )

    documents = repository.list_all()

    assert len(documents) == 1
    assert documents[0].document_id == "doc-1"
    db.close()