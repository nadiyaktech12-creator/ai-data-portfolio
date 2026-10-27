import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)

# Device fleet
n_devices = 50
devices = [f"device_{i:03d}" for i in range(1, n_devices + 1)]
regions = np.random.choice(["North", "South", "East", "West", "Central"], n_devices)

# Generate 7 days of hourly telemetry
start_date = datetime(2025, 10, 1)
records = []

for device, region in zip(devices, regions):
    current = start_date
    for _ in range(7 * 24):  # 7 days, hourly
        records.append({
            "device_id": device,
            "region": region,
            "timestamp": current,
            "temperature_c": np.random.normal(22, 4),
            "humidity_pct": np.random.uniform(30, 80),
            "battery_pct": max(5, np.random.normal(70, 15)),
            "status": np.random.choice(["online", "offline", "warning"], p=[0.85, 0.08, 0.07])
        })
        current += timedelta(hours=1)

df = pd.DataFrame(records)

# Introduce a few data quality issues
df.loc[df.sample(frac=0.01).index, "temperature_c"] = np.nan
df.loc[df.sample(frac=0.005).index, "battery_pct"] = -1

# Save as Parquet (data lake style)
os.makedirs("data/raw", exist_ok=True)
output_path = "data/raw/sensor_telemetry.parquet"
df.to_parquet(output_path, index=False)

print(f"Generated {len(df)} telemetry records")
print(f"Saved to {output_path}")
print(df.head(3))