import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="SaaS MRR and Churn Dashboard", layout="wide")

st.title("SaaS MRR and Churn Snapshot Dashboard")
st.markdown("A clear view of Monthly Recurring Revenue, growth, and customer churn.")

# Load data
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "subscriptions.csv"
    df = pd.read_csv(data_path)
    df["month"] = pd.to_datetime(df["month"])
    return df

df = load_data()

# Get latest month
latest_month = df["month"].max()
previous_month = latest_month - pd.DateOffset(months=1)

# Filter data
latest = df[df["month"] == latest_month]
previous = df[df["month"] == previous_month]

# ---------- Key Metrics ----------
total_mrr = latest["mrr"].sum()
prev_mrr = previous["mrr"].sum()

# New MRR (customers who appear in latest but not in previous)
new_customers = set(latest["customer_id"]) - set(previous["customer_id"])
new_mrr = latest[latest["customer_id"].isin(new_customers)]["mrr"].sum()

# Churned MRR (customers who were in previous but not in latest)
churned_customers = set(previous["customer_id"]) - set(latest["customer_id"])
churned_mrr = previous[previous["customer_id"].isin(churned_customers)]["mrr"].sum()

net_new_mrr = new_mrr - churned_mrr

# Logo churn rate
logo_churn_rate = (len(churned_customers) / len(previous["customer_id"].unique())) * 100 if len(previous) > 0 else 0

# ---------- Metric Cards ----------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total MRR", f"${total_mrr:,.0f}")
col2.metric("New MRR", f"${new_mrr:,.0f}")
col3.metric("Churned MRR", f"${churned_mrr:,.0f}")
col4.metric("Net New MRR", f"${net_new_mrr:,.0f}")
col5.metric("Logo Churn Rate", f"{logo_churn_rate:.1f}%")

st.divider()

# ---------- MRR Trend (Last 12 months) ----------
st.subheader("Monthly Recurring Revenue Trend")

mrr_trend = df.groupby("month")["mrr"].sum().reset_index()
mrr_trend = mrr_trend.sort_values("month").tail(12)

fig_line = px.line(
    mrr_trend,
    x="month",
    y="mrr",
    markers=True,
    labels={"month": "Month", "mrr": "Monthly Recurring Revenue ($)"}
)
fig_line.update_layout(height=400)
st.plotly_chart(fig_line, width="stretch")

# ---------- Plan Mix ----------
st.subheader("Revenue by Plan (Current Month)")

plan_mix = latest.groupby("plan")["mrr"].sum().reset_index()

fig_pie = px.pie(
    plan_mix,
    values="mrr",
    names="plan",
    hole=0.4,
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_pie.update_layout(height=400)
st.plotly_chart(fig_pie, width="stretch")

# ---------- Footer note ----------
st.caption(f"Data as of: **{latest_month.strftime('%B %Y')}** | Total active customers: **{latest['customer_id'].nunique()}**")
