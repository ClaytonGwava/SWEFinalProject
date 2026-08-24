from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "username": "test_student_auth",
            "email": "test_student_auth@example.com",
            "password": "password123",
            "role": "student"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "test_student_auth"
    assert data["email"] == "test_student_auth@example.com"
    assert data["role"] == "student"

    # Password must never be returned
    assert "password" not in data
    assert "password_hash" not in data


def test_duplicate_username_rejected():
    response = client.post(
        "/auth/register",
        json={
            "username": "test_student_auth",
            "email": "another@example.com",
            "password": "password123",
            "role": "student"
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Username already exists"
    )


def test_login_successfully():
    response = client.post(
        "/auth/login",
        data={
            "username": "test_student_auth",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert len(data["access_token"]) > 0


def test_login_with_wrong_password_fails():
    response = client.post(
        "/auth/login",
        data={
            "username": "test_student_auth",
            "password": "wrong_password"
        }
    )

    assert response.status_code == 401

    assert response.json()["detail"] == (
        "Invalid username or password"
    )


def test_login_with_unknown_user_fails():
    response = client.post(
        "/auth/login",
        data={
            "username": "user_that_does_not_exist",
            "password": "password123"
        }
    )

    assert response.status_code == 401

    assert response.json()["detail"] == (
        "Invalid username or password"
    )