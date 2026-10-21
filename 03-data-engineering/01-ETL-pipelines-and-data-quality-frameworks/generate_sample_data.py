import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Create sample raw sales data
np.random.seed(42)
n_orders = 500

start_date = datetime(2025, 1, 1)
dates = [start_date + timedelta(days=np.random.randint(0, 90)) for _ in range(n_orders)]

data = {
    "order_id": range(1001, 1001 + n_orders),
    "customer_id": np.random.randint(1, 101, n_orders),
    "order_date": [d.strftime("%Y-%m-%d") for d in dates],
    "product_category": np.random.choice(["Electronics", "Clothing", "Home", "Books", "Sports"], n_orders),
    "quantity": np.random.randint(1, 6, n_orders),
    "unit_price": np.round(np.random.uniform(10, 500, n_orders), 2),
    "discount_pct": np.round(np.random.uniform(0, 0.3, n_orders), 2),
    "status": np.random.choice(["completed", "shipped", "pending", "cancelled"], n_orders, p=[0.6, 0.2, 0.15, 0.05]),
    "region": np.random.choice(["North", "South", "East", "West", "Central"], n_orders),
}

df = pd.DataFrame(data)
df["total_amount"] = np.round(df["quantity"] * df["unit_price"] * (1 - df["discount_pct"]), 2)

# Introduce some data quality issues for testing
df.loc[5:7, "customer_id"] = None  # nulls
df.loc[10, "order_id"] = 1001  # duplicate
df.loc[15, "status"] = "invalid_status"  # bad value
df.loc[20, "total_amount"] = -50  # negative

os.makedirs("data/raw", exist_ok=True)
df.to_csv("data/raw/orders.csv", index=False)
print(f"Generated {len(df)} orders with intentional data quality issues.")
print(df.head())