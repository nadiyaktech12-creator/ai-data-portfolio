import joblib
import pandas as pd
import streamlit as st
from pathlib import Path

BASE = Path(__file__).parent
model = joblib.load(BASE / "model.joblib")
feature_columns = joblib.load(BASE / "feature_columns.joblib")

st.title("Customer Propensity-to-Buy Classifier")
st.write("Enter customer details to estimate the chance they subscribe to a term deposit.")

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 17, 98, 40)
    job = st.selectbox("Job", ["admin.", "blue-collar", "entrepreneur", "housemaid",
        "management", "retired", "self-employed", "services", "student",
        "technician", "unemployed", "unknown"])
    marital = st.selectbox("Marital status", ["divorced", "married", "single", "unknown"])
    education = st.selectbox("Education", ["basic.4y", "basic.6y", "basic.9y",
        "high.school", "illiterate", "professional.course", "university.degree", "unknown"])
    default = st.selectbox("Credit in default?", ["no", "unknown", "yes"])
    housing = st.selectbox("Housing loan?", ["no", "unknown", "yes"])
    loan = st.selectbox("Personal loan?", ["no", "unknown", "yes"])
    contact = st.selectbox("Contact type", ["cellular", "telephone"])
    month = st.selectbox("Last contact month", ["jan", "feb", "mar", "apr", "may", "jun",
        "jul", "aug", "sep", "oct", "nov", "dec"], index=4)
    day_of_week = st.selectbox("Last contact day", ["mon", "tue", "wed", "thu", "fri"])

with col2:
    campaign = st.number_input("Contacts this campaign", 1, 56, 2)
    pdays = st.number_input("Days since last contact (999 = never)", 0, 999, 999)
    previous = st.number_input("Contacts before this campaign", 0, 7, 0)
    poutcome = st.selectbox("Previous campaign outcome", ["failure", "nonexistent", "success"], index=1)
    emp_var_rate = st.number_input("Employment variation rate", -3.4, 1.4, 1.1)
    cons_price_idx = st.number_input("Consumer price index", 92.0, 95.0, 93.99)
    cons_conf_idx = st.number_input("Consumer confidence index", -51.0, -26.0, -36.4)
    euribor3m = st.number_input("Euribor 3-month rate", 0.5, 5.1, 4.86)
    nr_employed = st.number_input("Number employed (thousands)", 4900.0, 5300.0, 5191.0)

if st.button("Predict"):
    row = pd.DataFrame([{
        "age": age, "job": job, "marital": marital, "education": education,
        "default": default, "housing": housing, "loan": loan, "contact": contact,
        "month": month, "day_of_week": day_of_week, "campaign": campaign,
        "pdays": pdays, "previous": previous, "poutcome": poutcome,
        "emp.var.rate": emp_var_rate, "cons.price.idx": cons_price_idx,
        "cons.conf.idx": cons_conf_idx, "euribor3m": euribor3m,
        "nr.employed": nr_employed,
    }])

    row = pd.get_dummies(row)
    row = row.reindex(columns=feature_columns, fill_value=0)

    prob = model.predict_proba(row)[0][1]
    st.metric("Probability of buying", f"{prob:.0%}")
    st.progress(float(prob))