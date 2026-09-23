from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_metrics():
    response = client.get("/metrics")

    assert response.status_code == 200

    metrics = response.text

    assert "chat_requests_total" in metrics
    assert "chat_errors_total" in metrics