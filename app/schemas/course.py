from pydantic import BaseModel
from typing import Optional


class CourseCreate(BaseModel):
    course_code: str
    course_name: str
    description: Optional[str] = None


class CourseResponse(BaseModel):
    id: int
    course_code: str
    course_name: str
    description: Optional[str]
    faculty_id: int

    class Config:
        from_attributes = True


class EnrollmentResponse(BaseModel):
    id: int
    student_id: int
    course_id: int

    class Config:
        from_attributes = True