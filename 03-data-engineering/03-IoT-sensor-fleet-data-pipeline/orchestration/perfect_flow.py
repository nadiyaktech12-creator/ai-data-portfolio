from prefect import flow, task
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

@task(retries=2, retry_delay_seconds=10)
def generate_sensor_data():
    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "generate_sensor_data.py")],
        cwd=PROJECT_ROOT,
        check=True
    )

@task(retries=2, retry_delay_seconds=10)
def load_to_duckdb():
    subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "load_to_duckdb.py")],
        cwd=PROJECT_ROOT,
        check=True
    )

@flow(name="iot-sensor-fleet-pipeline", log_prints=True)
def iot_pipeline():
    generate_sensor_data()
    load_to_duckdb()
    print("IoT sensor fleet pipeline completed.")

if __name__ == "__main__":
    iot_pipeline()