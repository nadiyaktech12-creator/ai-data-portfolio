from pathlib import Path
import joblib
import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "german_credit.csv"

def load_data():
    if not DATA_PATH.exists():  # download once, then reuse
        fetch_openml("credit-g", version=1, as_frame=True).frame.to_csv(
            DATA_PATH, index=False)
    return pd.read_csv(DATA_PATH)

df = load_data()
print("Shape:", df.shape)
print(df["class"].value_counts())

y = (df["class"] == "bad").astype(int)
X = df.drop(columns=["class"])
X = X.fillna(X.median(numeric_only=True))
X = pd.get_dummies(X).astype(float)

X_tr, X_te, y_tr, y_te = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)
model = RandomForestClassifier(
    n_estimators=200, random_state=42, class_weight="balanced")
model.fit(X_tr, y_tr)

print(classification_report(y_te, model.predict(X_te)))
joblib.dump(model, BASE_DIR / "model.joblib")
joblib.dump(list(X.columns), BASE_DIR / "feature_columns.joblib")