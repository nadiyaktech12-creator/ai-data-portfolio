import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from pathlib import Path

# 1. Load data (semicolon separated)
def load_data():
   data_Path = Path(__file__).parent / "bank.csv"
   return pd.read_csv(data_Path, sep=';')

df = load_data()

print("Shape:", df.shape)
print(df["y"].value_counts())

# 2. Preprocessing
# 'duration' is only known after the call, so it leaks the answer. Drop it.
df = df.drop(columns=["duration"])

# Target: yes -> 1, no -> 0
y = df["y"].map({"yes": 1, "no": 0})
X = df.drop(columns=["y"])

# Fill missing values: median for numbers, mode for text
for col in X.columns:
    if pd.api.types.is_numeric_dtype(X[col]):
        X[col] = X[col].fillna(X[col].median())
    else:
        X[col] = X[col].fillna(X[col].mode()[0])

# Convert categoricals to dummy columns
X = pd.get_dummies(X, drop_first=True)

# 3. Train/test split (80/20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=12,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
)
model.fit(X_train, y_train)

# 4. Evaluate
preds = model.predict(X_test)
print("\nAccuracy:", round(accuracy_score(y_test, preds), 4))
print("\nClassification Report:\n", classification_report(y_test, preds))

# 5. Save model + exact feature column list
joblib.dump(model, "model.joblib")
joblib.dump(list(X.columns), "feature_columns.joblib")
print("Saved model.joblib and feature_columns.joblib")