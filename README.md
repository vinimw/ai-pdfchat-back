# AI PDF Chat

AI PDF Chat is a backend-first document question-answering system built to ingest PDF files, extract text, split content into chunks, index those chunks in a vector database, and answer user questions grounded in the original document.

The project follows a Retrieval-Augmented Generation (RAG) architecture:

1. Upload a PDF
2. Extract readable text
3. Split the text into chunks
4. Generate embeddings for each chunk
5. Store vectors in Chroma
6. Persist document metadata in SQLite
7. Ask questions about the document
8. Retrieve the most relevant chunks
9. Build a prompt with the retrieved context
10. Send the prompt to a local LLM through Ollama
11. Return a grounded answer plus sources

---

## Why this project exists

This project was created to study and demonstrate how a practical AI product is built beyond simply calling an LLM.

It shows how to combine:

* file ingestion
* PDF parsing
* chunking
* embedding generation
* vector search
* local LLM orchestration
* relational persistence
* downloadable file storage
* source-aware answers

It is designed as a portfolio-quality project for learning AI engineering in a product-oriented way.

---

## Core idea

The LLM does **not** read the raw PDF every time a user asks a question.

Instead, the backend prepares the information first:

* it parses and structures the document
* it stores semantic representations of the text
* it retrieves the most relevant passages for a question
* only then it calls the LLM with focused context

This makes the answer more grounded, more efficient, and easier to audit.

---

## Architecture overview

### Main layers

#### API layer

Responsible for receiving HTTP requests and returning responses.

* FastAPI routes
* request validation
* response formatting
* error handling

#### Service layer

Responsible for business logic and orchestration.

* PDF extraction
* chunking
* embeddings
* vector storage
* retrieval
* prompt building
* LLM calls
* file storage
* document lifecycle

#### Persistence layer

Responsible for storing structured data.

* SQLite for document metadata
* local file storage for original PDFs
* Chroma for vector storage

---

## High-level request flows

### 1. Upload flow

When a PDF is uploaded, the backend performs the following steps:

1. Validate that the uploaded file is a PDF
2. Read the file bytes
3. Save the original file to local storage
4. Extract the text from the PDF
5. Split the text into chunks
6. Generate embeddings for each chunk
7. Store the chunk embeddings in Chroma
8. Save document metadata in SQLite
9. Return the processed document information

### 2. Chat flow

When a user asks a question about a document, the backend performs the following steps:

1. Receive `document_id`, `collection_name`, and the question
2. Generate an embedding for the question
3. Search the document collection in Chroma
4. Retrieve the top relevant chunks
5. Build a prompt using those chunks as context
6. Send the prompt to the LLM through Ollama
7. Receive the generated answer
8. Return the answer with the source chunks

---

## Explaining important concepts

### Prompt built with retrieved chunks

When the system says it “builds a prompt with the retrieved chunks,” it means the backend does not send the raw PDF to the LLM.

Instead, it first finds the most relevant text pieces for the user’s question.

Example:

User question:

> What is the cancellation policy?

Retrieved chunks:

* chunk 12: "Cancellation requires 30 days written notice..."
* chunk 13: "Early termination may incur additional fees..."

The backend then creates a prompt like this:

```text
You are a document assistant.

Answer the user's question using ONLY the context below.
If the answer is not clearly present in the context, say:
"I could not find enough information in the provided document."

Context:
[Chunk 12]
Cancellation requires 30 days written notice...

[Chunk 13]
Early termination may incur additional fees...

Question:
What is the cancellation policy?

Answer:
```

This is important because:

* it narrows the model’s focus
* it reduces hallucinations
* it keeps answers grounded in the actual document
* it improves reliability and explainability

### The file is no longer just transient

If a file is transient, it exists only during request processing.

That means:

* the user uploads it
* the backend reads it in memory
* the backend processes it
* the file disappears afterward

In this project, the PDF is stored on disk. That means the document persists after the upload request ends.

This matters because it allows:

* reprocessing later without asking for a new upload
* downloading the original file
* auditability
* easier debugging
* better product behavior

### Collection name in Chroma

Each uploaded document gets its own collection name, such as:

```text
document_<document_id>
```

That collection is the logical container inside Chroma where the embeddings for that document are stored.

Why this matters:

* it isolates one document from another
* retrieval can target the exact document
* it avoids mixing embeddings across unrelated files
* it makes delete and cleanup simpler

In practice:

* `document_id` identifies the document in SQLite and the application flow
* `collection_name` identifies the vector store collection in Chroma

---

## Project structure

```text
backend/
  app/
    api/
      routes/
        chat.py
        documents.py
        health.py
        query.py
        upload.py
    core/
      exceptions.py
    db/
      database.py
      dependencies.py
    models/
      document.py
    repositories/
      document_repository.py
    schemas/
      chat.py
      chunk.py
      document.py
      query.py
      retrieval.py
    services/
      chat_service.py
      chunk_service.py
      document_service.py
      embedding_service.py
      llm_service.py
      pdf_service.py
      retrieval_service.py
      vector_store_service.py
    tests/
      fixtures/
      test_*.py
  chroma_db/
  storage/
    documents/
  documents.db
  main.py
  pytest.ini
  requirements.txt
```

---

## Responsibilities by file

### Routes

#### `upload.py`

Receives PDF uploads and triggers document processing.

#### `documents.py`

Lists documents, gets a document by ID, downloads the stored file, and deletes a document.

#### `query.py`

Retrieves relevant chunks without generating a natural-language answer.

#### `chat.py`

Runs retrieval plus LLM generation and returns an answer with sources.

#### `health.py`

Basic API healthcheck.

---

### Services

#### `pdf_service.py`

Extracts readable text from PDF bytes.

#### `chunk_service.py`

Splits long text into smaller overlapping chunks.

#### `embedding_service.py`

Generates embeddings for chunks and user queries.

#### `vector_store_service.py`

Stores and retrieves embeddings in Chroma.

#### `retrieval_service.py`

Coordinates embedding generation and vector search.

#### `llm_service.py`

Calls Ollama to generate answers from a prompt.

#### `chat_service.py`

Combines retrieval and generation into one answer pipeline.

#### `document_service.py`

Coordinates the entire document lifecycle during upload, storage, indexing, and deletion.

---

### Repository

#### `document_repository.py`

Provides database operations for document metadata.

---

## Data storage model

### SQLite

Stores metadata such as:

* `document_id`
* `collection_name`
* `filename`
* `stored_filename`
* `file_path`
* `pages`
* `characters`
* `created_at`

### Local file storage

Stores the original PDF file in:

```text
storage/documents/
```

### Chroma

Stores vectorized chunks and their metadata in:

```text
chroma_db/
```

---

## API endpoints

### Healthcheck

#### `GET /api/health`

Returns API health status.

---

### Upload document

#### `POST /api/documents/upload`

Uploads and processes a PDF.

Request type:

* `multipart/form-data`
* field name: `file`

Response example:

```json
{
  "document_id": "123",
  "collection_name": "document_123",
  "filename": "sample.pdf",
  "pages": 1,
  "characters": 68,
  "text": "This is a sample PDF for testing...",
  "chunks": [
    {
      "index": 0,
      "text": "This is a sample PDF for testing...",
      "start_char": 0,
      "end_char": 68
    }
  ]
}
```

---

### List documents

#### `GET /api/documents`

Returns all stored documents.

---

### Get document by ID

#### `GET /api/documents/{document_id}`

Returns one stored document metadata entry.

---

### Download stored file

#### `GET /api/documents/{document_id}/file`

Returns the original PDF file.

---

### Delete document

#### `DELETE /api/documents/{document_id}`

Deletes:

* SQLite metadata
* stored file on disk
* Chroma collection

---

### Retrieve relevant chunks

#### `POST /api/documents/query`

Returns relevant chunks for a question without calling the LLM.

Request example:

```json
{
  "document_id": "123",
  "collection_name": "document_123",
  "question": "What is this PDF about?",
  "top_k": 3
}
```

---

### Ask the document

#### `POST /api/chat/ask`

Returns a natural-language answer plus sources.

Request example:

```json
{
  "document_id": "123",
  "collection_name": "document_123",
  "question": "What is this PDF about?",
  "top_k": 3
}
```

Response example:

```json
{
  "answer": "This document is about testing.",
  "sources": [
    {
      "chunk_index": 0,
      "text": "This PDF is about software testing.",
      "score": 0.1,
      "start_char": 0,
      "end_char": 35
    }
  ]
}
```

---

## How retrieval works

Retrieval is the step that finds the best context before calling the LLM.

### Detailed sequence

1. User sends a question
2. The question is converted into an embedding vector
3. Chroma compares that vector against stored chunk embeddings
4. Chroma returns the nearest chunks
5. The backend uses those chunks as context for the LLM

This means the LLM does not search the PDF itself. The backend retrieves context first.

---

## How generation works

Generation is the step where the backend asks the LLM to compose a final answer.

### Detailed sequence

1. Retrieval returns the top chunks
2. The backend creates a prompt including those chunks
3. The backend calls Ollama locally
4. Ollama runs the selected model
5. The LLM returns a text answer
6. The backend returns that answer plus the source chunks

---

## Why Ollama is used

Ollama is used as a local LLM runtime so the project can:

* run locally
* avoid API cost during learning
* swap models more easily
* keep the architecture close to a real AI product

The backend communicates with Ollama through HTTP.

---

## Technology stack

### Backend

* Python
* FastAPI
* Pydantic
* SQLAlchemy
* SQLite
* PyPDF
* sentence-transformers
* ChromaDB
* Ollama
* pytest

### AI components

* `sentence-transformers/all-MiniLM-L6-v2` for embeddings
* local LLM through Ollama for answer generation

---

## Local development setup

### 1. Create and activate virtual environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -U pip
pip install -r requirements.txt
```

### 3. Run Ollama

```bash
ollama serve
```

In another terminal, pull a model:

```bash
ollama pull llama3.2
```

### 4. Start the API

```bash
uvicorn main:app --reload
```

### 5. Open docs

```text
http://127.0.0.1:8000/docs
```

---

## How to test manually

### Upload a file

Use `POST /api/documents/upload` with `multipart/form-data` and a `file` field.

### List documents

Use `GET /api/documents`.

### Ask a question

Use `POST /api/chat/ask` with the returned `document_id` and `collection_name`.

### Download original file

Use `GET /api/documents/{document_id}/file`.

### Delete a document

Use `DELETE /api/documents/{document_id}`.

---

## Testing strategy

The project includes multiple testing layers.

### Unit tests

Used for isolated business logic such as:

* PDF extraction
* chunking
* prompt building
* service behavior

### Integration tests

Used for route-level and flow-level verification such as:

* upload route
* document listing
* retrieval flow
* delete route

### Mock-based tests

Used when a real embedding model or a real LLM should not run during test execution.

---

## Trade-offs in the current version

### Chroma collection per document

Pros:

* isolation is simple
* cleanup is straightforward
* easier debugging

Cons:

* not ideal for very large scale
* more collections to manage over time

### Local file storage

Pros:

* simple
* easy to inspect
* good for local development and demo

Cons:

* not cloud-ready by default
* not ideal for distributed systems

### SQLite

Pros:

* lightweight
* perfect for MVP and local development

Cons:

* not ideal for multi-user production scale

### Local Ollama runtime

Pros:

* no API cost during development
* more control

Cons:

* depends on local machine resources
* production setup would need more decisions

---

## Future improvements

### Backend

* add database migrations with Alembic
* persist chat history
* add reprocessing endpoint
* add score thresholds for retrieval
* improve delete robustness
* introduce structured logging
* add environment-based settings
* support multiple embedding models
* support cloud storage

### Retrieval quality

* improve chunking strategy
* chunk by semantic boundaries instead of character windows
* deduplicate retrieved chunks
* add reranking
* limit context size more intelligently

### Frontend

* upload UI
* document list page
* document detail page
* chat interface
* source viewer
* file download button
* delete actions with confirmation

### Production readiness

* authentication
* authorization
* Postgres instead of SQLite
* S3-compatible storage instead of local disk
* background processing queue
* monitoring and tracing

---

## Example end-to-end scenario

### Upload

User uploads `contract.pdf`.

The backend:

1. stores the PDF on disk
2. extracts its text
3. creates chunks
4. generates embeddings
5. stores vectors in Chroma
6. saves metadata in SQLite
7. returns the new document information

### Question

User asks:

> What is the cancellation policy?

The backend:

1. embeds the question
2. searches the document collection in Chroma
3. retrieves the most relevant chunks
4. builds a context-grounded prompt
5. sends the prompt to Ollama
6. receives the answer
7. returns the answer with sources

---

## Key learning outcomes from this project

This project demonstrates practical knowledge of:

* API design for AI applications
* file ingestion pipelines
* PDF parsing
* chunking strategies
* embedding-based retrieval
* vector databases
* prompt construction
* local LLM orchestration
* layered backend architecture
* metadata persistence
* testable AI workflows

---

## License

This project is for study, experimentation, and portfolio use.
