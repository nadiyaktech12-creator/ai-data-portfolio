# ETL Pipelines & Data Quality Frameworks

Lightweight Modern Data Stack mini project demonstrating production-oriented data engineering practices.

## Overview
End-to-end pipeline that:
- Generates raw retail orders data (with intentional data quality issues)
- Loads data into DuckDB
- Transforms data through staging → intermediate → marts layers using dbt
- Enforces data quality with dbt tests
- Orchestrates the full flow with Prefect

## Tech Stack
- **DuckDB** — local analytical warehouse
- **dbt-core + dbt-duckdb** — SQL transformations and data quality tests
- **Prefect** — orchestration (flows, tasks, retries)
- **Python** — data generation and loading

## Project Structure
. ├── generate_sample_data.py # Creates raw orders.csv with DQ issues ├── load_raw.py # Loads CSV into DuckDB ├── dbt_project/ # dbt models, tests, and configs │ ├── models/ │ │ ├── staging/ │ │ ├── intermediate/ │ │ └── marts/ │ ├── dbt_project.yml │ └── profiles.yml ├── orchestration/ │ └── prefect_flow.py # Full pipeline orchestration ├── requirements.txt └── README.md

## Quick Start
```bash
# 1. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the full pipeline
python orchestration/prefect_flow.py
```

Data Quality
The sample data intentionally contains issues (nulls, duplicates, invalid values, negative amounts) so that dbt tests fail in a controlled way. 


