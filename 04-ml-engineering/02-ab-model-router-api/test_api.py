from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "A/B Model Router API" in response.json()["message"]

def test_predict_returns_model():
    response = client.post("/predict", json={
        "age": 32,
        "income": 55000,
        "tenure_months": 8,
        "monthly_charges": 75.0
    })
    assert response.status_code == 200
    data = response.json()
    assert data["model_used"] in ["baseline", "challenger"]
    assert "churn_prediction" in data
    assert "churn_probability" in data

def test_stats():
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["challenger_traffic_percentage"] == 20
    assert data["baseline_traffic_percentage"] == 80