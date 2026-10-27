# IoT Sensor Fleet Data Pipeline

Local data lake style pipeline that generates IoT sensor telemetry and stores it as Parquet, then loads it into DuckDB for fast analytics.

## Overview
- Generates realistic sensor telemetry (temperature, humidity, battery, status) for a fleet of devices
- Stores raw data as Parquet (simulating S3 / data lake storage)
- Loads into DuckDB for analytical queries
- Orchestrated end-to-end with Prefect

## Tech Stack
- Python + Pandas
- Parquet (via PyArrow)
- DuckDB
- Prefect

## Project Structure
├── generate_sensor_data.py # Creates realistic IoT telemetry ├── load_to_duckdb.py # Loads Parquet into DuckDB ├── query_example.py # Sample analytical query ├── orchestration/ │ └── prefect_flow.py # Full pipeline orchestration ├── requirements.txt └── README.md
## Quick Start
```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python orchestration/prefect_flow.py
```
What it demonstrates
	•	Data lake style storage using Parquet
	•	IoT / time-series telemetry generation
	•	Lightweight analytics with DuckDB
	•	Orchestrated ingestion pipeline with Prefect
