import duckdb
from pathlib import Path

def load_raw_to_duckdb():
    """Load raw CSV into DuckDB as a source table."""
    db_path = Path(__file__).parent / "data" / "retail_orders.duckdb"
    csv_path = Path(__file__).parent / "data" / "raw" / "orders.csv"
    
    # Ensure data folder exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    con = duckdb.connect(str(db_path))
    con.execute(f"""
        CREATE OR REPLACE TABLE main.orders AS
        SELECT * FROM read_csv_auto('{csv_path.as_posix()}')
    """)
    count = con.execute("SELECT COUNT(*) FROM main.orders").fetchone()[0]
    con.close()
    print(f"Loaded {count} rows into DuckDB at {db_path}")
    return count

if __name__ == "__main__":
    load_raw_to_duckdb()