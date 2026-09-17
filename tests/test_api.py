import pytest
from fastapi.testclient import TestClient
from src.api.main import app

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_health_check(client):
    response = client.get("/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "ok"

def test_predict_segment_valid_data(client):
    payload = {
        "recency": 10.0,
        "frequency": 5.0,
        "monetary": 150.0
    }
    response = client.post("/v1/predict/segment", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "cluster_id" in data["data"]

def test_predict_segment_invalid_data(client):
    payload = {
        "recency": -10.0,  # Invalid due to ge=0
        "frequency": 5.0,
        "monetary": 150.0
    }
    response = client.post("/v1/predict/segment", json=payload)
    assert response.status_code == 422

def test_predict_forecast_default(client):
    response = client.get("/v1/predict/forecast")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]["forecast"]) == 4

def test_predict_forecast_custom_weeks(client):
    response = client.get("/v1/predict/forecast?weeks=8")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["forecast"]) == 8

def test_predict_forecast_invalid_weeks(client):
    response = client.get("/v1/predict/forecast?weeks=0")  # Invalid due to gt=0
    assert response.status_code == 422
