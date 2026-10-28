# End-to-End MLOps Pipeline

Lightweight MLOps demonstration: train a model with MLflow tracking, save it, and serve predictions via FastAPI.

## Overview
- Generates synthetic churn-style data
- Trains a RandomForest classifier
- Logs parameters and metrics with MLflow
- Serves the model through a FastAPI endpoint
- Includes basic API tests

## Tech Stack
- scikit-learn
- MLflow
- FastAPI + Uvicorn
- joblib
- pytest

## Quick Start
```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python train.py
python -m uvicorn app:app --reload
```
Open http://127.0.0.1:8000/docs to test the API.

Run Tests
```bash
pip install pytest httpx
pytest test_api.py -v
```
Project Structure
.
├── train.py                 # Training script with MLflow
├── app.py                   # FastAPI serving
├── test_api.py              # API tests
├── models/                  # Saved model (generated)
├── requirements.txt
└── README.md

What it demonstrates
•  Experiment tracking with MLflow
•  Model serialization and loading
•  Production-style model serving with FastAPI
•  Basic automated testing


