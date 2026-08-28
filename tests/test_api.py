from fastapi.testclient import TestClient
from model.serve import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_predict_with_valid_input():
    response = client.post("/predict", json={
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    })
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "model_version" in data


def test_predict_with_invalid_input_returns_clean_error():
    response = client.post("/predict", json={
        "sepal_length": -5,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    })
    assert response.status_code == 422  # not a crash, a clean validation error


def test_predict_with_missing_field():
    response = client.post("/predict", json={
        "sepal_length": 5.1,
        "sepal_width": 3.5
    })
    assert response.status_code == 422