from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def register_and_login(username, email, password, role):
    # Register user
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "role": role
        }
    )

    assert register_response.status_code == 200

    # Login user
    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]


def test_faculty_can_create_course():

    token = register_and_login(
        "course_test_faculty",
        "course_faculty@example.com",
        "password123",
        "faculty"
    )

    response = client.post(
        "/courses/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_code": "TEST425",
            "course_name": "Test Software Engineering",
            "description": "Test course"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["course_code"] == "TEST425"
    assert data["course_name"] == "Test Software Engineering"
    assert data["description"] == "Test course"


def test_student_cannot_create_course():

    token = register_and_login(
        "course_test_student",
        "course_student@example.com",
        "password123",
        "student"
    )

    response = client.post(
        "/courses/",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "course_code": "STUDENT425",
            "course_name": "Unauthorized Course",
            "description": "Should not be created"
        }
    )

    assert response.status_code == 403


def test_student_can_enroll_in_course():

    faculty_token = register_and_login(
        "enroll_test_faculty",
        "enroll_faculty@example.com",
        "password123",
        "faculty"
    )

    course_response = client.post(
        "/courses/",
        headers={
            "Authorization": f"Bearer {faculty_token}"
        },
        json={
            "course_code": "ENROLL425",
            "course_name": "Enrollment Test",
            "description": "Enrollment test course"
        }
    )

    assert course_response.status_code == 200

    course_id = course_response.json()["id"]

    student_token = register_and_login(
        "enroll_test_student",
        "enroll_student@example.com",
        "password123",
        "student"
    )

    response = client.post(
        f"/courses/{course_id}/enroll",
        headers={
            "Authorization": f"Bearer {student_token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["course_id"] == course_id


def test_student_cannot_enroll_twice():

    faculty_token = register_and_login(
        "duplicate_enroll_faculty",
        "duplicate_faculty@example.com",
        "password123",
        "faculty"
    )

    course_response = client.post(
        "/courses/",
        headers={
            "Authorization": f"Bearer {faculty_token}"
        },
        json={
            "course_code": "DUP425",
            "course_name": "Duplicate Enrollment Test",
            "description": "Test"
        }
    )

    assert course_response.status_code == 200

    course_id = course_response.json()["id"]

    student_token = register_and_login(
        "duplicate_enroll_student",
        "duplicate_student@example.com",
        "password123",
        "student"
    )

    first_response = client.post(
        f"/courses/{course_id}/enroll",
        headers={
            "Authorization": f"Bearer {student_token}"
        }
    )

    assert first_response.status_code == 200

    second_response = client.post(
        f"/courses/{course_id}/enroll",
        headers={
            "Authorization": f"Bearer {student_token}"
        }
    )

    assert second_response.status_code == 400

    assert second_response.json()["detail"] == (
        "Already enrolled"
    )


def test_student_can_unenroll():

    faculty_token = register_and_login(
        "unenroll_test_faculty",
        "unenroll_faculty@example.com",
        "password123",
        "faculty"
    )

    course_response = client.post(
        "/courses/",
        headers={
            "Authorization": f"Bearer {faculty_token}"
        },
        json={
            "course_code": "UNENROLL425",
            "course_name": "Unenrollment Test",
            "description": "Test"
        }
    )

    assert course_response.status_code == 200

    course_id = course_response.json()["id"]

    student_token = register_and_login(
        "unenroll_test_student",
        "unenroll_student@example.com",
        "password123",
        "student"
    )

    enroll_response = client.post(
        f"/courses/{course_id}/enroll",
        headers={
            "Authorization": f"Bearer {student_token}"
        }
    )

    assert enroll_response.status_code == 200

    unenroll_response = client.delete(
        f"/courses/{course_id}/unenroll",
        headers={
            "Authorization": f"Bearer {student_token}"
        }
    )

    assert unenroll_response.status_code == 200

    assert unenroll_response.json()["message"] == (
        "Successfully unenrolled from course"
    )


def test_student_can_get_my_courses():

    faculty_token = register_and_login(
        "mycourses_test_faculty",
        "mycourses_faculty@example.com",
        "password123",
        "faculty"
    )

    course_response = client.post(
        "/courses/",
        headers={
            "Authorization": f"Bearer {faculty_token}"
        },
        json={
            "course_code": "MY425",
            "course_name": "My Courses Test",
            "description": "Test"
        }
    )

    assert course_response.status_code == 200

    course_id = course_response.json()["id"]

    student_token = register_and_login(
        "mycourses_test_student",
        "mycourses_student@example.com",
        "password123",
        "student"
    )

    enroll_response = client.post(
        f"/courses/{course_id}/enroll",
        headers={
            "Authorization": f"Bearer {student_token}"
        }
    )

    assert enroll_response.status_code == 200

    response = client.get(
        "/courses/my-courses",
        headers={
            "Authorization": f"Bearer {student_token}"
        }
    )

    assert response.status_code == 200

    courses = response.json()

    assert len(courses) >= 1

    course_ids = [
        course["id"]
        for course in courses
    ]

    assert course_id in course_ids