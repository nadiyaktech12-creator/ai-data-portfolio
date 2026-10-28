import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
import mlflow
import mlflow.sklearn
from mlflow.models import infer_signature
import joblib
import os

# Generate simple synthetic data (churn-style)
np.random.seed(42)
n = 1000
X = pd.DataFrame({
    "age": np.random.randint(18, 70, n),
    "income": np.random.randint(20000, 150000, n),
    "tenure_months": np.random.randint(1, 60, n),
    "monthly_charges": np.random.uniform(20, 120, n)
})
y = (X["monthly_charges"] > 70).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

mlflow.set_experiment("churn-classifier")

with mlflow.start_run():
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    proba = model.predict_proba(X_test)[:, 1]

    acc = accuracy_score(y_test, preds)
    auc = roc_auc_score(y_test, proba)

    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", acc)
    mlflow.log_metric("auc", auc)

    # Save model locally (skip mlflow.sklearn.log_model to avoid the error)
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/churn_model.joblib")

    print(f"Accuracy: {acc:.4f}")
    print(f"AUC: {auc:.4f}")
    print("Model saved to models/churn_model.joblib")