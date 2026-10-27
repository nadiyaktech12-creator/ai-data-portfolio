# SaaS Data Warehouse Analytics Layer

Dimensional (Kimball) modeling of Stripe + HubSpot-style data using dbt and DuckDB.

## Overview
Transforms raw SaaS data into clean analytics models:
- Staging: cleaned source views
- Marts: `dim_customers`, `fct_subscriptions`, `fct_monthly_mrr`

## Tech Stack
- DuckDB
- dbt-core + dbt-duckdb
- Prefect

## Quick Start
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python orchestration/prefect_flow.py
```
# Models
	•	dim_customers — customer dimension enriched with HubSpot contact data
	•	fct_subscriptions — subscription fact with current MRR
	•	fct_monthly_mrr — monthly MRR by plan

What it demonstrates
	•	Kimball dimensional modeling
	•	Staging → marts pattern
	•	Joining multiple sources (Stripe + HubSpot)
	•	Orchestrated pipeline with Prefect

