import pandas as pd
import numpy as np
from datetime import timedelta

np.random.seed(42)

# Create 18 months of data
months = pd.date_range(start="2024-01-01", periods=18, freq="MS")
customers = [f"C{str(i).zfill(4)}" for i in range(1, 301)]  # 300 customers
plans = ["Basic", "Pro", "Enterprise"]
plan_prices = {"Basic": 29, "Pro": 79, "Enterprise": 199}

records = []

for customer in customers:
    # Convert to pandas Timestamp so we can use strftime later
    start_month = pd.Timestamp(np.random.choice(months[:12]))
    plan = np.random.choice(plans, p=[0.5, 0.35, 0.15])
    status = "active"
    
    for month in months:
        if month < start_month:
            continue
            
        # Random churn after some time
        if status == "active" and np.random.rand() < 0.04 and month > start_month + timedelta(days=60):
            status = "churned"
            
        if status == "active":
            records.append({
                "customer_id": customer,
                "plan": plan,
                "mrr": plan_prices[plan],
                "month": month.strftime("%Y-%m"),
                "status": status,
                "start_date": start_month.strftime("%Y-%m-%d")
            })

df = pd.DataFrame(records)
df.to_csv("subscriptions.csv", index=False)
print("subscriptions.csv created successfully!")
print(df.head())
print(f"\nTotal rows: {len(df)}")
