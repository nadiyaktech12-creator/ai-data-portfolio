import duckdb
from pathlib import Path

def load_parquet():
    db_path = Path(__file__).parent / "data" / "iot_fleet.duckdb"
    parquet_path = Path(__file__).parent / "data" / "raw" / "sensor_telemetry.parquet"
    
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db_path))
    
    con.execute(f"""
        CREATE OR REPLACE TABLE main.sensor_telemetry AS
        SELECT * FROM read_parquet('{parquet_path.as_posix()}')
    """)
    
    count = con.execute("SELECT COUNT(*) FROM main.sensor_telemetry").fetchone()[0]
    print(f"Loaded {count} rows into DuckDB")
    con.close()

if __name__ == "__main__":
    load_parquet()