import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

# ----- HubSpot Contacts -----
n_contacts = 200
contacts = pd.DataFrame({
    "contact_id": range(1, n_contacts + 1),
    "email": [f"user{i}@example.com" for i in range(1, n_contacts + 1)],
    "first_name": np.random.choice(["Alex", "Sam", "Jordan", "Taylor", "Casey"], n_contacts),
    "last_name": np.random.choice(["Smith", "Johnson", "Lee", "Brown", "Davis"], n_contacts),
    "company": np.random.choice(["Acme", "Globex", "Initech", "Umbrella", "Stark"], n_contacts),
    "created_at": [datetime(2024, 1, 1) + timedelta(days=np.random.randint(0, 400)) for _ in range(n_contacts)],
    "lifecycle_stage": np.random.choice(["lead", "opportunity", "customer", "churned"], n_contacts, p=[0.3, 0.2, 0.4, 0.1])
})

# ----- Stripe Customers (linked to some contacts) -----
n_customers = 120
stripe_customers = pd.DataFrame({
    "customer_id": [f"cus_{i:04d}" for i in range(1, n_customers + 1)],
    "contact_id": np.random.choice(contacts["contact_id"], n_customers),
    "email": None,  # will fill later
    "created_at": [datetime(2024, 6, 1) + timedelta(days=np.random.randint(0, 200)) for _ in range(n_customers)]
})
stripe_customers["email"] = stripe_customers["contact_id"].map(contacts.set_index("contact_id")["email"])

# ----- Stripe Subscriptions / Payments -----
n_subs = 180
plans = ["starter", "pro", "enterprise"]
prices = {"starter": 29, "pro": 99, "enterprise": 299}

subscriptions = pd.DataFrame({
    "subscription_id": [f"sub_{i:04d}" for i in range(1, n_subs + 1)],
    "customer_id": np.random.choice(stripe_customers["customer_id"], n_subs),
    "plan": np.random.choice(plans, n_subs, p=[0.5, 0.35, 0.15]),
    "status": np.random.choice(["active", "canceled", "past_due"], n_subs, p=[0.7, 0.2, 0.1]),
    "started_at": [datetime(2024, 7, 1) + timedelta(days=np.random.randint(0, 180)) for _ in range(n_subs)],
    "canceled_at": None
})
subscriptions["monthly_amount"] = subscriptions["plan"].map(prices)
# Set some canceled dates
canceled_mask = subscriptions["status"] == "canceled"
subscriptions.loc[canceled_mask, "canceled_at"] = subscriptions.loc[canceled_mask, "started_at"] + timedelta(days=90)

# ----- Save -----
os.makedirs("data/raw", exist_ok=True)
contacts.to_csv("data/raw/hubspot_contacts.csv", index=False)
stripe_customers.to_csv("data/raw/stripe_customers.csv", index=False)
subscriptions.to_csv("data/raw/stripe_subscriptions.csv", index=False)

print(f"Generated {len(contacts)} contacts, {len(stripe_customers)} customers, {len(subscriptions)} subscriptions")