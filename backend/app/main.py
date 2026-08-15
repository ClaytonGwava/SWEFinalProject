import shutil
from pathlib import Path

from fastapi import File, UploadFile, Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.database.database import Base, engine
from app.database import models

from app.services.llm_service import ask_llm
from app.services.rag_service import search_documents
from app.routers.auth import router as auth_router
from app.dependencies import get_current_user
from app.database.models import User


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="EduAI",
    description="LLM-Based Academic Assistant",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "Welcome to EduAI",
        "status": "Backend is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer = ask_llm(
        request.question
    )

    return {
        "question": request.question,
        "answer": answer
    }


@app.post("/ask-rag")
def ask_rag_question(
    request: QuestionRequest
):

    documents = search_documents(
        request.question
    )

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    answer = ask_llm(
        request.question,
        context
    )

    return {
        "question": request.question,
        "answer": answer,
        "sources": [
            {
                "content": document.page_content,
                "metadata": document.metadata
            }
            for document in documents
        ]
    }
    
@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    upload_directory = Path("uploads")
    upload_directory.mkdir(
        exist_ok=True
    )

    file_path = upload_directory / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    from app.services.rag_service import create_vector_store

    chunk_count = create_vector_store(
        str(file_path)
    )

    return {
        "filename": file.filename,
        "message": "Document uploaded and indexed successfully",
        "chunks_created": chunk_count
    }
    
@app.get("/me")
def get_my_profile(
    current_user: User = Depends(
        get_current_user
    )
):

    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "role": current_user.role
    }