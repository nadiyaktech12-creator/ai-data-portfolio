import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load data
df = pd.read_csv("HR-Employee-Attrition.csv")

# Drop useless columns
df = df.drop(["EmployeeCount", "EmployeeNumber", "Over18", "StandardHours"], axis=1)

# Target
df["Attrition"] = (df["Attrition"] == "Yes").astype(int)

# Selected features (manageable for the form + high predictive power)
features = [
    "Age", "MonthlyIncome", "YearsAtCompany", "DistanceFromHome",
    "OverTime", "JobSatisfaction", "EnvironmentSatisfaction", "WorkLifeBalance",
    "Department", "JobRole", "BusinessTravel", "MaritalStatus", "Gender",
    "JobInvolvement"
]

X = df[features]
y = df["Attrition"]

# One-hot encode
X_encoded = pd.get_dummies(X, drop_first=True)

# Save feature columns (critical for the app)
feature_columns = list(X_encoded.columns)
joblib.dump(feature_columns, "feature_columns.joblib")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42, stratify=y
)

# Model (balanced because attrition is ~16%)
model = RandomForestClassifier(
    n_estimators=150,
    random_state=42,
    class_weight="balanced",
    max_depth=10
)
model.fit(X_train, y_train)

# Evaluation
print("Accuracy:", accuracy_score(y_test, model.predict(X_test)))
print(classification_report(y_test, model.predict(X_test)))

# Save model
joblib.dump(model, "attrition_model.joblib")
print("Model and feature columns saved.")