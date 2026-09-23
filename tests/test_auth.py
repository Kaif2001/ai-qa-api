import os

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

USERNAME = os.getenv("DEMO_USERNAME", "admin")
PASSWORD = os.getenv("DEMO_PASSWORD", "admin123")


def test_login_success():
    response = client.post(
        "/auth/login",
        data={
            "username": USERNAME,
            "password": PASSWORD,
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_wrong_password():
    response = client.post(
        "/auth/login",
        data={
            "username": USERNAME,
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_chat_without_token():
    response = client.post(
        "/chat",
        json={
            "question": "What is DevOps?"
        },
    )

    assert response.status_code == 401