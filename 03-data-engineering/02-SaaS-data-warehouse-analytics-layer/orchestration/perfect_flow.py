from prefect import flow, task
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DBT_DIR = PROJECT_ROOT / "dbt_project"

@task(retries=2)
def generate_sample_data():
    subprocess.run([sys.executable, str(PROJECT_ROOT / "generate_sample_data.py")], cwd=PROJECT_ROOT, check=True)

@task(retries=2)
def load_raw_data():
    subprocess.run([sys.executable, str(PROJECT_ROOT / "load_raw.py")], cwd=PROJECT_ROOT, check=True)

@task(retries=2)
def dbt_run():
    subprocess.run(["dbt", "run"], cwd=DBT_DIR, check=True)

@flow(name="saas-analytics-layer", log_prints=True)
def saas_analytics_pipeline():
    generate_sample_data()
    load_raw_data()
    dbt_run()
    print("SaaS analytics pipeline completed.")

if __name__ == "__main__":
    saas_analytics_pipeline()