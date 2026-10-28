from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Churn Prediction API is running"

def test_predict():
    response = client.post("/predict", json={
        "age": 35,
        "income": 60000,
        "tenure_months": 12,
        "monthly_charges": 85.5
    })
    assert response.status_code == 200
    data = response.json()
    assert "churn_prediction" in data
    assert "churn_probability" in data
    assert data["churn_prediction"] in [0, 1]