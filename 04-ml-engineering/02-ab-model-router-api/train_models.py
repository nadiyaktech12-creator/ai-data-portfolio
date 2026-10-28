import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

np.random.seed(42)
n = 2000

X = pd.DataFrame({
    "age": np.random.randint(18, 70, n),
    "income": np.random.randint(25000, 120000, n),
    "tenure_months": np.random.randint(1, 48, n),
    "monthly_charges": np.random.uniform(25, 110, n)
})
y = (X["monthly_charges"] > 65).astype(int)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

os.makedirs("models", exist_ok=True)

# Baseline model
baseline = RandomForestClassifier(n_estimators=80, random_state=42)
baseline.fit(X_train, y_train)
baseline_acc = accuracy_score(y_test, baseline.predict(X_test))
joblib.dump(baseline, "models/baseline_model.joblib")
print(f"Baseline accuracy: {baseline_acc:.4f}")

# Challenger model
challenger = GradientBoostingClassifier(n_estimators=100, random_state=42)
challenger.fit(X_train, y_train)
challenger_acc = accuracy_score(y_test, challenger.predict(X_test))
joblib.dump(challenger, "models/challenger_model.joblib")
print(f"Challenger accuracy: {challenger_acc:.4f}")

print("Both models saved in models/")