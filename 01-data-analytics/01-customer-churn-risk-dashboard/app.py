import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config
st.set_page_config(page_title="Customer Churn Risk Dashboard", layout="wide")

st.title("Customer Churn Risk Dashboard")
st.markdown("### Telco Customer Churn Analysis")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("churn.csv")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")

contract_type = st.sidebar.multiselect(
    "Select Contract Type",
    options=df["Contract"].unique(),
    default=df["Contract"].unique()
)

internet_service = st.sidebar.multiselect(
    "Select Internet Service",
    options=df["InternetService"].unique(),
    default=df["InternetService"].unique()
)

# Filter Data
df_filtered = df[
    (df["Contract"].isin(contract_type)) &
    (df["InternetService"].isin(internet_service))
]

# KPIs
total_customers = len(df_filtered)
churned_customers = len(df_filtered[df_filtered["Churn"] == "Yes"])
churn_rate = (churned_customers / total_customers) * 100 if total_customers > 0 else 0
avg_tenure = df_filtered["tenure"].mean()
avg_monthly_charges = df_filtered["MonthlyCharges"].mean()

# Display KPIs
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Customers", f"{total_customers:,}")
col2.metric("Churned Customers", f"{churned_customers:,}")
col3.metric("Churn Rate", f"{churn_rate:.2f}%")
col4.metric("Avg Tenure (months)", f"{avg_tenure:.1f}")

st.markdown("---")

# Charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Churn by Contract Type")
    fig1 = px.histogram(df_filtered, x="Contract", color="Churn", barmode="group")
    st.plotly_chart(fig1, use_container_width=True)

with col_right:
    st.subheader("Churn by Internet Service")
    fig2 = px.histogram(df_filtered, x="InternetService", color="Churn", barmode="group")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Monthly Charges Distribution")
fig3 = px.histogram(df_filtered, x="MonthlyCharges", color="Churn", nbins=40)
st.plotly_chart(fig3, use_container_width=True)

st.subheader("Tenure vs Monthly Charges")
fig4 = px.scatter(df_filtered, x="tenure", y="MonthlyCharges", color="Churn", opacity=0.6)
st.plotly_chart(fig4, use_container_width=True)

# Data Preview
with st.expander("View Filtered Data"):
    st.dataframe(df_filtered)
