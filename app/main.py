import shutil
from pathlib import Path

from fastapi import (
    File,
    UploadFile,
    Depends,
    FastAPI,
    HTTPException
)
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.database.database import (
    Base,
    engine,
    get_db
)
from sqlalchemy.orm import Session
from app.database import models

from app.services.llm_service import ask_llm
from app.services.rag_service import search_documents
from app.routers.auth import router as auth_router
from app.dependencies import get_current_user
from app.database.models import (
    User,
    Course,
    Enrollment
)
from app.routers.courses import router as courses_router

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
app.include_router(courses_router)


class QuestionRequest(BaseModel):
    question: str
    course_id: int


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
    request: QuestionRequest,
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    # Verify that the course exists
    course = (
        db.query(Course)
        .filter(
            Course.id == request.course_id
        )
        .first()
    )

    if not course:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # Faculty can access their course.
    if current_user.role == "faculty":

        if course.faculty_id != current_user.id:

            raise HTTPException(
                status_code=403,
                detail="You do not own this course"
            )

    # Students must be enrolled.
    elif current_user.role == "student":

        enrollment = (
            db.query(Enrollment)
            .filter(
                Enrollment.student_id ==
                current_user.id,

                Enrollment.course_id ==
                request.course_id
            )
            .first()
        )

        if not enrollment:

            raise HTTPException(
                status_code=403,
                detail="You are not enrolled in this course"
            )

    else:

        raise HTTPException(
            status_code=403,
            detail="Invalid user role"
        )


    # Search the course-specific RAG index
    documents = search_documents(
        request.question,
        request.course_id
    )


    context = "\n\n".join(
        document.page_content
        for document in documents
    )


    answer = ask_llm(
        request.question,
        context
    )
    
        # Save question and answer to database
    question_record = models.Question(
        user_id=current_user.id,
        course_id=request.course_id,
        question=request.question,
        answer=answer
    )

    db.add(question_record)
    db.commit()
    db.refresh(question_record)


    return {
        "question": request.question,
        "course_id": request.course_id,
        "answer": answer,
        "sources": [
            {
                "content": document.page_content,
                "metadata": document.metadata
            }
            for document in documents
        ]
    }


@app.get("/questions/my-history")
def get_my_question_history(
    current_user: User = Depends(
        get_current_user
    ),
    db: Session = Depends(get_db)
):

    questions = (
        db.query(models.Question)
        .filter(
            models.Question.user_id ==
            current_user.id
        )
        .order_by(
            models.Question.created_at.desc()
        )
        .all()
    )

    return [
        {
            "id": question.id,
            "course_id": question.course_id,
            "question": question.question,
            "answer": question.answer,
            "created_at": question.created_at
        }
        for question in questions
    ]
    
        
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