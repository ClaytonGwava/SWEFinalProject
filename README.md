# EduAI – AI-Powered Academic Assistant

## CS425 Software Engineering Project

**Student Name:** Clayton Gwava  
**Course:** CS425 – Software Engineering  
**Project:** EduAI – AI-Powered Academic Assistant  
**Technology:** Python, FastAPI, React, SQLite, FAISS, OpenAI  
**Deployment:** Local Development

---

# Technology Stack

## Frontend
- React
- Vite
- JavaScript
- CSS

## Backend
- Python
- FastAPI
- SQLAlchemy
- Pydantic

## Database
- SQLite

## Authentication
- JWT
- Password hashing

## AI / RAG
- OpenAI API
- FAISS
- Embeddings
- Retrieval-Augmented Generation

## Document Processing
- PDF processing
- DOCX processing
- PPTX processing

## Testing
- pytest
- FastAPI TestClient

## Development Tools
- Visual Studio Code
- Git
- GitHub
- Python virtual environment

# Project Directory Structure

```text
eduAI/
│
├── app/
│   ├── database/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── routers/
│   │   ├── auth.py
│   │   ├── courses.py
│   │   └── questions.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── course.py
│   │   └── question.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── document_service.py
│   │   ├── llm_service.py
│   │   └── rag_service.py
│   │
│   ├── dependencies.py
│   ├── main.py
│   └── __init__.py
│
├── frontend/
│
├── tests/
│   ├── test_auth.py
│   ├── test_courses.py
│   ├── test_document_service.py
│   ├── test_llm_service.py
│   ├── test_main.py
│   └── test_rag.py
│
├── uploads/
├── vector_store/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

# 32. Installation

Prerequisites

Install:
```text
Python 3.11+
Node.js
npm
Git
```

# 33. Clone the Repository

```text
git clone <https://github.com/ClaytonGwava/SWEFinalProject.git>
cd eduAI
```

# 34. Create Python Virtual Environment

Windows:
```text
python -m venv venv
```

Activate:
```text
venv\Scripts\Activate.ps1
```

# 35. Install Backend Dependencies
pip install -r requirements.txt

# 36. Configure Environment Variables

Create a .env file in the project root.

Example:
```text
OPENAI_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
```

Do not commit the .env file to GitHub.

The actual values must remain private.

# 37. Run the Backend

From the project root:
```text
uvicorn app.main:app --reload
```

The backend should be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## 38. Run the Frontend

Open another terminal.

Navigate to the frontend directory:
```text
cd frontend
```

Install dependencies:

```text
npm install
```
Start the development server:

```text
npm run dev
```

Open the URL displayed by Vite in the terminal.

# 39. Database Setup

EduAI uses SQLite.

The database is configured through:
```text
app/database/database.py
```
The default database is:
```text
eduai.db
```
The application creates the required database tables during application startup.

For a clean local development database, remove the existing database:
```text
Remove-Item .\eduai.db
```
Then restart the backend.

# 40. Running Automated Tests

EduAI uses pytest.

From the project root:
```text
pytest -v
```
The project currently contains 17 automated tests.

The tests cover:

- Authentication.
- User registration.
- Duplicate username handling.
- Login.
- Invalid passwords.
- Unknown users.
- Course creation.
- Role authorization.
- Course enrollment.
- Duplicate enrollment.
- Course unenrollment.
- My Courses.
- Document validation.
- LLM service behavior.
- API endpoints.
- RAG retrieval.

# 41. Test Results

The complete automated test suite currently passes:
```text
17 passed
```

Example:
```text
============================== test session starts ==============================

collected 17 items

tests/test_auth.py ................
tests/test_courses.py ............
tests/test_document_service.py ...
tests/test_llm_service.py .......
tests/test_main.py ..............
tests/test_rag.py ...............

============================== 17 passed ==============================
```

The exact output may vary depending on pytest formatting and the environment.

# 42. Testing Strategy

Testing was performed at multiple levels.

## API Testing

FastAPI's TestClient is used to test REST endpoints.

Examples include:

- Registration.
- Login.
- Course creation.
- Enrollment.
- Unenrollment.
- Protected endpoints.
- Authentication Testing

Tests verify:

- Successful registration.
- Duplicate username rejection.
- Successful login.
- Invalid password rejection.
- Unknown user rejection.

## Authorization Testing

Tests verify that:

- Students cannot create courses.
- Students cannot perform faculty-only operations.
- Protected functionality requires authentication.

## Document Testing

Tests verify that unsupported document types are rejected.

## RAG Testing

The RAG system is tested to ensure relevant documents can be retrieved.

## LLM Testing

The LLM service is tested using a mocked response so the test does not need to make a real OpenAI API call.

This makes the automated tests faster, more reliable, and less dependent on external services.

# 43. Screenshots
Please refer to the screenshots folder

# 44. Security

EduAI includes several security mechanisms.

## Password Hashing

Passwords are not stored directly.

The system stores password hashes.

## JWT Authentication

Successful login generates a JWT access token.

The backend validates the token before allowing access to protected endpoints.

## Role-Based Authorization

Backend dependencies enforce student and faculty permissions.

Examples:
```text
require_student
require_faculty
```
This prevents users from gaining access simply by modifying frontend components.

## Course Ownership

Faculty members can only upload documents to courses that they own.

## Input Validation

The API validates incoming data using Pydantic schemas and explicit validation logic.

## Secret Management

API keys and signing secrets are stored in environment variables.

They should never be committed to GitHub.

# 45. Known Limitations

The current system has several limitations.

## 1. Local Deployment

The application currently runs locally and is not deployed to a public cloud environment.

## 2. SQLite

SQLite is appropriate for this academic project but may not be ideal for a large production deployment.

## 3. External LLM Dependency

AI answer generation depends on the OpenAI API.

## 4. Supported Documents

The current system supports:

- PDF
- DOCX
- PPTX

Other document types are not currently supported.

## 5. AI Accuracy

Although RAG grounds responses in course material, AI-generated answers should still be reviewed by students and faculty.

## 6. Large Document Collections

Very large collections of documents may require additional indexing and storage optimization.

## 7. No Cloud Deployment

Cloud deployment is outside the scope of the current project.

# 46. Future Improvements

Possible future enhancements include:

- Cloud deployment.
- PostgreSQL database.
- More document formats.
- Improved document management.
- Faculty document deletion.
- Document versioning.
- Student performance analytics.
- Course announcements.
- Assignment management.
- Chat conversation management.
- Streaming AI responses.
- Improved citation and source navigation.
- More advanced search.
- Mobile application.
- Multi-model AI support.
- Administrative dashboard.

# 47. Design Decisions
## Why FastAPI?

FastAPI provides:

- Simple REST API development.
- Automatic API documentation.
- Pydantic validation.
- Dependency injection.
- Good Python ecosystem support.

## Why React?

React provides a component-based frontend architecture and makes it easy to create interactive dashboards.

## Why SQLite?

SQLite is lightweight and appropriate for a university software engineering project.

## Why FAISS?

FAISS provides efficient similarity search over document embeddings and works well for a local RAG application.

## Why RAG?

RAG allows EduAI to retrieve relevant course material before generating an answer.

This reduces dependence on the LLM's general knowledge and allows responses to be grounded in course-specific content.

# 48. Example Application Flow

A typical student interaction is:

```text
1. Student registers
        |
2. Student logs in
        |
3. Student views courses
        |
4. Student enrolls in CS425
        |
5. Faculty uploads course material
        |
6. Documents are processed
        |
7. FAISS index is created
        |
8. Student asks a question
        |
9. EduAI searches CS425 documents
        |
10. Relevant content is retrieved
        |
11. Retrieved content is sent to LLM
        |
12. LLM generates answer
        |
13. EduAI displays answer
        |
14. EduAI displays sources
        |
15. Question is saved in history
```

# 49. Example Question

Student asks:

```text
What are software engineering processes?
```

EduAI retrieves relevant course material and generates an answer based on the retrieved context.

The application also displays the source document and relevant page information.

This provides both:

- AI assistance
- Source transparency

# 50. Project Achievements

The completed EduAI application demonstrates:

- Full-stack application development.
- REST API development.
- React frontend development.
- Database design.
- Authentication.
- Authorization.
- Role-based access.
- Course management.
- Document processing.
- Vector search.
- Retrieval-Augmented Generation.
- LLM integration.
- Automated testing.
- Software architecture.
- UML/design documentation.



# 52. Presentation Demonstration Plan

The application demonstration can follow this sequence:

## Step 1 – Introduce EduAI

Explain the problem and purpose.

## Step 2 – Faculty Login

Demonstrate faculty authentication.

## Step 3 – Create Course

Create or show a course such as:

CS425 – Software Engineering

## Step 4 – Upload Course Material

Upload a PDF/DOCX/PPTX document.

Demonstrate successful indexing.

## Step 5 – Student Login

Log in as a student.

## Step 6 – Enroll

Enroll in the course.

## Step 7 – Ask Question

Ask a question based on the course material.

## Step 8 – Demonstrate RAG

Explain that EduAI retrieves relevant course content before generating the answer.

## Step 9 – Show Sources

Show the retrieved source documents.

## Step 10 – Show History

Show the question appearing in Recent Questions.

## Step 11 – Demonstrate Unenrollment

Show the student removing the course.

## Step 12 – Demonstrate Testing

Run:
```text
pytest -v
```
and show:

```text
17 passed
```

## Step 13 – Demonstrate DB records


# 53. Conclusion

EduAI provides an integrated academic assistance platform that combines course management, document processing, vector search, Retrieval-Augmented Generation, and AI-powered question answering.

The system demonstrates the principles of software engineering through:

Layered architecture.
Separation of responsibilities.
Authentication and authorization.
Database persistence.
Automated testing.
REST API design.
Frontend/backend integration.
RAG-based AI functionality.
Source transparency.

The final application provides students with a practical way to interact with their course materials using natural language while giving faculty control over the academic content used by the system.

# 54. License

This project was developed for academic purposes as part of the CS425 Software Engineering course.

