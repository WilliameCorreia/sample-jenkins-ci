from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert isinstance(payload.get("version"), str)
    assert payload["version"]


def test_add_endpoint():
    response = client.get("/add", params={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 5}


def test_divide_endpoint():
    response = client.get("/divide", params={"a": 10, "b": 2})
    assert response.status_code == 200
    assert response.json() == {"result": 5}


def test_divide_by_zero():
    response = client.get("/divide", params={"a": 1, "b": 0})
    assert response.status_code == 400
    assert response.json() == {"detail": "division by zero"}
