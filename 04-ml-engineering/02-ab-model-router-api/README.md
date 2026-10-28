
# A/B Model Router API
![A/B Router](https://github.com/nadiyaktech12-creator/ai-data-portfolio/actions/workflows/ab-router.yml/badge.svg) 

FastAPI service that routes prediction traffic between a baseline model and a challenger model.

## Overview
- Trains two different models (RandomForest baseline + GradientBoosting challenger)
- Routes incoming requests with a configurable traffic split (default 80/20)
- Returns which model was used along with the prediction

## Tech Stack
- FastAPI
- scikit-learn
- joblib
- pandas

## Quick Start
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python train_models.py
python -m uvicorn app:app --reload
```
Open http://127.0.0.1:8000/docs to test.

What it demonstrates
	•	A/B testing of ML models in production
	•	Traffic routing logic
	•	Serving multiple models from a single API
