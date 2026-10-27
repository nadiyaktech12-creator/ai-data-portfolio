import duckdb
from pathlib import Path

def load_raw_to_duckdb():
    db_path = Path(__file__).parent / "data" / "saas_warehouse.duckdb"
    raw_dir = Path(__file__).parent / "data" / "raw"
    
    db_path.parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(db_path))

    for csv_file in raw_dir.glob("*.csv"):
        table_name = csv_file.stem  # e.g. hubspot_contacts
        con.execute(f"""
            CREATE OR REPLACE TABLE main.{table_name} AS
            SELECT * FROM read_csv_auto('{csv_file.as_posix()}')
        """)
        count = con.execute(f"SELECT COUNT(*) FROM main.{table_name}").fetchone()[0]
        print(f"Loaded {count} rows into {table_name}")

    con.close()
    print(f"Database created at {db_path}")

if __name__ == "__main__":
    load_raw_to_duckdb()