
# Application Layer Structure
The backend follows a layered structure.

```text

app/
│
├── database/
│   ├── database.py
│   └── models.py
│
├── routers/
│   ├── auth.py
│   ├── courses.py
│   └── questions.py
│
├── schemas/
│   ├── auth.py
│   ├── course.py
│   └── question.py
│
├── services/
│   ├── auth_service.py
│   ├── document_service.py
│   ├── llm_service.py
│   └── rag_service.py
│
├── dependencies.py
├── main.py
└── __init__.py
```

# Controller / Router Layer
FastAPI routers handle HTTP requests.

Examples include:

```text
/auth/register
/auth/login

/courses/
/courses/{course_id}/enroll
/courses/{course_id}/unenroll
/courses/{course_id}/documents

/questions/ask
/questions/history
```

# Service Layer

Business logic is separated into services.

Important services include:

## Authentication Service

Responsible for:
- Password hashing.
- Password verification.
- JWT creation.
- JWT decoding.

## Document Service

Responsible for:

- Document processing.
- Document type handling.
- Text extraction.

## RAG Service

Responsible for:

- Creating vector stores.
- Splitting documents into chunks.
- Embedding documents.
- Searching relevant documents.

## LLM Service

Responsible for:

- Building prompts.
- Passing retrieved context to the LLM.
- Generating the final answer.

# Database Layer

EduAI uses SQLAlchemy with SQLite.

The database stores application information such as:

- Users
- Courses
- Enrollments
- Documents
- Questions / Question History

The database configuration is located in:

```text
app/database/database.py
```

The SQLAlchemy models are located in:

```text
app/database/models.py
```

# Database Relationships

The main relationships are:

```text
User
 |
 +----< Course
 |
 +----< Enrollment >---- Course
 |
 +----< Document
 |
 +----< Question
```

- A faculty user can create courses.

- A student can enroll in multiple courses.

- A course can have multiple students.

- A course can contain multiple documents.

- A student can have multiple question-history records.


# RAG Architecture

EduAI uses a course-specific RAG architecture.

```text
Document Ingestion
Uploaded Document
       |
       v
Document Loader
       |
       v
Extract Text
       |
       v
Split into Chunks
       |
       v
Generate Embeddings
       |
       v
FAISS Vector Store
Question Answering
Student Question
       |
       v
Selected Course
       |
       v
FAISS Similarity Search
       |
       v
Relevant Chunks
       |
       v
Prompt Construction
       |
       v
LLM
       |
       v
Answer + Sources
```
