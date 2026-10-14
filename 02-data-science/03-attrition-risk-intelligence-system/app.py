import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Employee Attrition Risk Intelligence", layout="wide")

# Path setup (important for deployment)
BASE = Path(__file__).parent

st.title("Employee Attrition Risk Intelligence System")
st.markdown("""
Predict the likelihood of an employee leaving, understand the key drivers, 
and estimate the business impact. Built for HR decision support.
""")

# Load model and feature columns using Path
@st.cache_resource
def load_model():
    model = joblib.load(BASE / "attrition_model.joblib")
    feature_columns = joblib.load(BASE / "feature_columns.joblib")
    return model, feature_columns

model, feature_columns = load_model()

# ---------- Input Form ----------
with st.form("attrition_form"):
    st.subheader("Employee Details")
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input("Age", min_value=18, max_value=65, value=35)
        monthly_income = st.number_input("Monthly Income", min_value=1000, max_value=20000, value=5000)
        years_at_company = st.number_input("Years at Company", min_value=0, max_value=40, value=5)
        distance = st.number_input("Distance From Home (miles)", min_value=1, max_value=30, value=10)
        overtime = st.selectbox("OverTime", ["Yes", "No"])
        job_satisfaction = st.selectbox("Job Satisfaction (1=Low → 4=Very High)", [1, 2, 3, 4], index=2)
        env_satisfaction = st.selectbox("Environment Satisfaction (1=Low → 4=Very High)", [1, 2, 3, 4], index=2)

    with col2:
        work_life = st.selectbox("Work Life Balance (1=Bad → 4=Best)", [1, 2, 3, 4], index=2)
        department = st.selectbox("Department", ["Research & Development", "Sales", "Human Resources"])
        job_role = st.selectbox("Job Role", [
            "Sales Executive", "Research Scientist", "Laboratory Technician",
            "Manufacturing Director", "Healthcare Representative", "Manager",
            "Sales Representative", "Research Director", "Human Resources"
        ])
        business_travel = st.selectbox("Business Travel", ["Travel_Rarely", "Travel_Frequently", "Non-Travel"])
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
        gender = st.selectbox("Gender", ["Male", "Female"])
        job_involvement = st.selectbox("Job Involvement (1=Low → 4=Very High)", [1, 2, 3, 4], index=2)

    submitted = st.form_submit_button("Predict Attrition Risk", type="primary")

# ---------- Prediction Logic ----------
def predict_probability(input_dict):
    input_data = pd.DataFrame([input_dict])
    input_encoded = pd.get_dummies(input_data, drop_first=True)
    input_encoded = input_encoded.reindex(columns=feature_columns, fill_value=0)
    return model.predict_proba(input_encoded)[0][1]

if submitted:
    base_input = {
        "Age": age,
        "MonthlyIncome": monthly_income,
        "YearsAtCompany": years_at_company,
        "DistanceFromHome": distance,
        "OverTime": overtime,
        "JobSatisfaction": job_satisfaction,
        "EnvironmentSatisfaction": env_satisfaction,
        "WorkLifeBalance": work_life,
        "Department": department,
        "JobRole": job_role,
        "BusinessTravel": business_travel,
        "MaritalStatus": marital_status,
        "Gender": gender,
        "JobInvolvement": job_involvement
    }

    probability = predict_probability(base_input)
    probability_pct = round(probability * 100, 1)

    # Risk tier
    if probability < 0.30:
        risk = "Low"
        risk_color = "green"
        risk_func = st.success
    elif probability < 0.60:
        risk = "Medium"
        risk_color = "orange"
        risk_func = st.warning
    else:
        risk = "High"
        risk_color = "red"
        risk_func = st.error

    # Estimated replacement cost (50% of annual salary)
    annual_salary = monthly_income * 12
    replacement_cost = annual_salary * 0.5

    # ---------- Results Dashboard ----------
    st.divider()
    st.subheader("Risk Assessment")

    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Attrition Probability", f"{probability_pct}%")
    with metric_col2:
        st.metric("Risk Level", risk)
    with metric_col3:
        st.metric("Est. Replacement Cost", f"${replacement_cost:,.0f}")

    # Visual gauge
    st.progress(probability)
    st.caption(f"Probability of leaving: {probability_pct}%")

    risk_func(f"Risk Level: **{risk}**")

    # ---------- What-If Analysis ----------
    st.subheader("What-If Analysis")
    whatif_col1, whatif_col2 = st.columns(2)

    with whatif_col1:
        st.write("**Current Scenario**")
        st.write(f"OverTime: **{overtime}** → {probability_pct}%")

    with whatif_col2:
        # Toggle OverTime and re-predict
        flipped_overtime = "No" if overtime == "Yes" else "Yes"
        whatif_input = base_input.copy()
        whatif_input["OverTime"] = flipped_overtime
        whatif_prob = predict_probability(whatif_input)
        whatif_pct = round(whatif_prob * 100, 1)
        difference = round(probability_pct - whatif_pct, 1)

        st.write("**Alternative Scenario**")
        st.write(f"OverTime: **{flipped_overtime}** → {whatif_pct}%")
        if difference > 0:
            st.success(f"Risk decreases by **{difference} percentage points**")
        else:
            st.info(f"Risk increases by **{abs(difference)} percentage points**")

    # ---------- Feature Importance ----------
    st.subheader("Top Drivers of Attrition")
    importance_df = pd.DataFrame({
        "Feature": feature_columns,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False).head(10)

    fig = px.bar(
        importance_df, 
        x="Importance", 
        y="Feature", 
        orientation="h",
        title="Top 10 Feature Importances",
        color="Importance",
        color_continuous_scale="Blues"
    )
    fig.update_layout(yaxis={'categoryorder':'total ascending'}, height=400)
    st.plotly_chart(fig, use_container_width=True)

    # ---------- Suggested Actions ----------
    st.subheader("Suggested Actions")
    actions = []
    if overtime == "Yes":
        actions.append("Review overtime load — OverTime is a strong attrition driver.")
    if job_satisfaction <= 2:
        actions.append("Improve job satisfaction through manager check-ins, recognition, or role clarity.")
    if env_satisfaction <= 2:
        actions.append("Address work environment concerns (team dynamics, resources, or culture).")
    if monthly_income < 4000:
        actions.append("Review compensation against market rates and internal equity.")
    if work_life <= 2:
        actions.append("Discuss work-life balance and flexible arrangements if possible.")
    if not actions:
        actions.append("Employee appears lower risk. Maintain regular engagement and development opportunities.")

    for action in actions:
        st.write(f"• {action}")