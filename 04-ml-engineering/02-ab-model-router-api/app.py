from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import random

app = FastAPI(title="A/B Model Router API")

# Load both models
baseline = joblib.load("models/baseline_model.joblib")
challenger = joblib.load("models/challenger_model.joblib")

# Traffic split: 80% baseline, 20% challenger
CHALLENGER_TRAFFIC = 0.2

class CustomerFeatures(BaseModel):
    age: int
    income: int
    tenure_months: int
    monthly_charges: float

@app.get("/")
def home():
    return {"message": "A/B Model Router API is running"}

@app.post("/predict")
def predict(features: CustomerFeatures):
    data = pd.DataFrame([features.model_dump()])

    # Route traffic
    use_challenger = random.random() < CHALLENGER_TRAFFIC
    model_name = "challenger" if use_challenger else "baseline"
    model = challenger if use_challenger else baseline

    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]

    return {
        "model_used": model_name,
        "churn_prediction": int(prediction),
        "churn_probability": round(float(probability), 4)
    }

@app.get("/stats")
def stats():
    return {
        "challenger_traffic_percentage": int(CHALLENGER_TRAFFIC * 100),
        "baseline_traffic_percentage": int((1 - CHALLENGER_TRAFFIC) * 100)
    }