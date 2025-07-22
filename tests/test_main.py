from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_handle_task_echo():
    payload = {"question_text": "sample question"}
    response = client.post("/api/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "result" in data
    # Now also assert task_type and param fields
    assert data["result"] == {
        "echo": "sample question",
        "task_type": "unknown",
        "param": ""
    }
