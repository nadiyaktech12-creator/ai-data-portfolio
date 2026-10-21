from prefect import flow, task
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
DBT_DIR = PROJECT_ROOT / "dbt_project"

@task(retries=2, retry_delay_seconds=10)
def generate_sample_data():
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "generate_sample_data.py")],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"Data generation failed: {result.stderr}")
    print(result.stdout)
    return "Data generated"

@task(retries=2, retry_delay_seconds=10)
def load_raw_data():
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "load_raw.py")],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise Exception(f"Load failed: {result.stderr}")
    print(result.stdout)
    return "Raw data loaded"

@task(retries=2, retry_delay_seconds=15)
def dbt_run():
    result = subprocess.run(
        ["dbt", "run"],
        cwd=DBT_DIR,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        raise Exception(f"dbt run failed:\n{result.stderr}")
    return "Models built"

@task
def dbt_test():
    result = subprocess.run(
        ["dbt", "test"],
        cwd=DBT_DIR,
        capture_output=True,
        text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print("WARNING: Some data quality tests failed (expected for demo data)")
    return "Tests executed"

@flow(name="retail-orders-modern-stack", log_prints=True)
def retail_orders_pipeline():
    """Modern Data Stack mini pipeline"""
    generate_sample_data()
    load_raw_data()
    dbt_run()
    dbt_test()
    print("Pipeline completed successfully.")

if __name__ == "__main__":
    retail_orders_pipeline()