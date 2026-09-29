import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="E-commerce Cohort Retention", layout="wide")

st.title("E-commerce Sales Cohort Retention Heatmap")

st.markdown("""
This dashboard shows customer retention by cohort.  
It tells us what percentage of customers who made their first purchase in a particular month came back to buy again in the following months.

- **Rows** = Cohort month (when the customer first bought)
- **Columns** = Number of months since their first purchase
- **Values** = % of that cohort still buying
""")

# Load the data
@st.cache_data
def load_data():
    df = pd.read_excel("online_retail.xlsx")
    df = df.dropna(subset=["CustomerID"])
    df = df[df["Quantity"] > 0]  # remove returns / cancelled orders
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    return df

df = load_data()

# Create order month
df["order_month"] = df["InvoiceDate"].dt.to_period("M")

# Find first purchase month for each customer
first_purchase = df.groupby("CustomerID")["order_month"].min().reset_index()
first_purchase.columns = ["CustomerID", "cohort_month"]

df = df.merge(first_purchase, on="CustomerID")

# Calculate how many months have passed since first purchase
def get_month_diff(row):
    return (row["order_month"].year - row["cohort_month"].year) * 12 + (row["order_month"].month - row["cohort_month"].month)

df["month_number"] = df.apply(get_month_diff, axis=1)

# Count unique customers for each cohort + month
cohort_data = (
    df.groupby(["cohort_month", "month_number"])["CustomerID"]
    .nunique()
    .reset_index()
)

# Create pivot table
cohort_pivot = cohort_data.pivot_table(
    index="cohort_month",
    columns="month_number",
    values="CustomerID"
)

# Convert to retention percentage
cohort_sizes = cohort_pivot[0]
retention = cohort_pivot.divide(cohort_sizes, axis=0)

# Keep only first 13 months for cleaner view
retention = retention.iloc[:, :13]

st.subheader("Customer Retention Heatmap")

fig = px.imshow(
    retention,
    labels=dict(x="Months Since First Purchase", y="Cohort Month", color="Retention %"),
    x=[str(i) for i in retention.columns],
    y=[str(i) for i in retention.index],
    color_continuous_scale="Blues",
    aspect="auto",
    text_auto=".0%",
    zmin=0,
    zmax=1
)

fig.update_layout(
    height=650,
    xaxis_title="Months Since First Purchase",
    yaxis_title="Cohort Month",
    coloraxis_colorbar=dict(title="Retention %", tickformat=".0%")
)

st.plotly_chart(fig, width="stretch")

st.caption(f"Total unique customers: **{df['CustomerID'].nunique():,}**")

with st.expander("View retention table"):
    st.dataframe(retention.style.format("{:.1%}").background_gradient(cmap="Blues", axis=None))