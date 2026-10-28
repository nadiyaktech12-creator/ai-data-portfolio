from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(title="Churn Prediction API")

# Load the trained model
model = joblib.load("models/churn_model.joblib")

class CustomerFeatures(BaseModel):
    age: int
    income: int
    tenure_months: int
    monthly_charges: float

@app.get("/")
def home():
    return {"message": "Churn Prediction API is running"}

@app.post("/predict")
def predict(features: CustomerFeatures):
    data = pd.DataFrame([features.model_dump()])
    prediction = model.predict(data)[0]
    probability = model.predict_proba(data)[0][1]
    
    return {
        "churn_prediction": int(prediction),
        "churn_probability": round(float(probability), 4)
    }