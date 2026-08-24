import shutil
from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    File,
    UploadFile
)

from sqlalchemy.orm import Session

from app.database.database import get_db

from app.database.models import (
    Course,
    Enrollment,
    User,
    Document
)

from app.dependencies import (
    get_current_user,
    require_faculty,
    require_student
)

from app.schemas.course import (
    CourseCreate,
    CourseResponse,
    EnrollmentResponse
)

from app.services.rag_service import (
    create_vector_store
)

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.post(
    "/",
    response_model=CourseResponse
)
def create_course(
    course_data: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_faculty
    )
):

    existing = db.query(Course).filter(
        Course.course_code ==
        course_data.course_code
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Course already exists"
        )

    course = Course(
        course_code=course_data.course_code,
        course_name=course_data.course_name,
        description=course_data.description,
        faculty_id=current_user.id
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course

@router.post(
    "/{course_id}/documents"
)
async def upload_course_document(
    course_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_faculty
    )
):

    # 1. Find the course
    course = (
        db.query(Course)
        .filter(
            Course.id == course_id
        )
        .first()
    )

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    # 2. Make sure faculty owns the course
    if course.faculty_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not own this course"
        )

    # 3. Validate file type
    allowed_extensions = {
        ".pdf",
        ".docx",
        ".pptx"
    }

    file_extension = Path(
        file.filename
    ).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Only PDF, DOCX and PPTX "
                "files are allowed."
            )
        )

    # 4. Create course-specific upload directory
    upload_directory = Path(
        "uploads"
    ) / f"course_{course_id}"

    upload_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    # 5. Save file
    file_path = (
        upload_directory /
        file.filename
    )

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    # 6. Create database record
    document = Document(
        filename=file.filename,
        file_path=str(file_path),
        uploaded_by=current_user.id,
        course_id=course_id
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # 7. Create course-specific FAISS index
    chunk_count = create_vector_store(
        str(file_path),
        course_id
    )

    return {
        "id": document.id,
        "filename": document.filename,
        "course_id": course_id,
        "message": (
            "Document uploaded and "
            "indexed successfully"
        ),
        "chunks_created": chunk_count
    }
    
    
@router.get(
    "/",
    response_model=list[CourseResponse]
)
def get_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    return db.query(Course).all()


@router.post(
    "/{course_id}/enroll",
    response_model=EnrollmentResponse
)
def enroll_student(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_student
    )
):

    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    existing = db.query(Enrollment).filter(
        Enrollment.student_id ==
        current_user.id,
        Enrollment.course_id ==
        course_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Already enrolled"
        )

    enrollment = Enrollment(
        student_id=current_user.id,
        course_id=course_id
    )

    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)

    return enrollment


@router.get(
    "/my-courses",
    response_model=list[CourseResponse]
)
def get_my_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_student
    )
):

    courses = (
        db.query(Course)
        .join(Enrollment)
        .filter(
            Enrollment.student_id ==
            current_user.id
        )
        .all()
    )

    return courses

@router.delete(
    "/{course_id}/unenroll"
)
def unenroll_student(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_student)
):

    enrollment = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == current_user.id,
            Enrollment.course_id == course_id
        )
        .first()
    )

    if not enrollment:
        raise HTTPException(
            status_code=404,
            detail="You are not enrolled in this course"
        )

    db.delete(enrollment)
    db.commit()

    return {
        "message": "Successfully unenrolled from course"
    }