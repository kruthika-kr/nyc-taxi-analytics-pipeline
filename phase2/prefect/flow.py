from pathlib import Path
import os
import subprocess

import pandas as pd
import pyarrow.parquet as pq
import snowflake.connector
from dotenv import load_dotenv
from prefect import flow, task
from snowflake.connector.pandas_tools import write_pandas


# Load values from .env
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data" / "raw"
DBT_DIR = PROJECT_ROOT / "phase2" / "dbt"
DBT_EXE = Path.home() / "AppData" / "Roaming" / "Python" / "Python312" / "Scripts" / "dbt.exe"


def get_snowflake_connection():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse="COMPUTE_WH",
        database="NYC_TAXI_DB",
        schema="RAW",
        role="ACCOUNTADMIN",
    )


@task
def truncate_raw_table() -> None:
    """Clear the raw table before a fresh full load."""
    conn = get_snowflake_connection()
    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE NYC_TAXI_DB.RAW.RAW_YELLOW_TAXI_TRIPS")
    cur.close()
    conn.close()
    print("RAW_YELLOW_TAXI_TRIPS truncated successfully.")


@task
def load_parquet_to_snowflake(file_path: str) -> int:
    """Load one parquet file into Snowflake."""
    parquet_file = pq.ParquetFile(file_path)
    conn = get_snowflake_connection()

    rows_loaded = 0

    for batch in parquet_file.iter_batches(batch_size=5000):
        df = batch.to_pandas()

        # Match Snowflake column naming
        df.columns = [c.upper() for c in df.columns]

        # Convert datetime columns to strings so Snowflake loads them safely
        if "TPEP_PICKUP_DATETIME" in df.columns:
            df["TPEP_PICKUP_DATETIME"] = pd.to_datetime(df["TPEP_PICKUP_DATETIME"]).dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        if "TPEP_DROPOFF_DATETIME" in df.columns:
            df["TPEP_DROPOFF_DATETIME"] = pd.to_datetime(df["TPEP_DROPOFF_DATETIME"]).dt.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        success, nchunks, nrows, _ = write_pandas(
            conn,
            df,
            table_name="RAW_YELLOW_TAXI_TRIPS",
            database="NYC_TAXI_DB",
            schema="RAW",
        )

        rows_loaded += nrows
        print(f"Loaded batch from {Path(file_path).name}. Total rows so far: {rows_loaded}")

    conn.close()
    print(f"Finished loading {Path(file_path).name}. Rows loaded: {rows_loaded}")
    return rows_loaded


@task
def run_dbt_models() -> None:
    """Run dbt models after loading data."""
    result = subprocess.run(
        [str(DBT_EXE), "run", "--profiles-dir", str(DBT_DIR)],
        cwd=str(DBT_DIR),
        capture_output=True,
        text=True,
        check=False,
    )

    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError("dbt run failed.")

    print("dbt run completed successfully.")


@flow
def nyc_taxi_pipeline() -> None:
    """Full pipeline: truncate raw table, load all parquet files, then run dbt."""
    truncate_raw_table()

    files = [
        DATA_DIR / "yellow_tripdata_2024-01.parquet",
        DATA_DIR / "yellow_tripdata_2024-02.parquet",
        DATA_DIR / "yellow_tripdata_2024-03.parquet",
    ]

    total_rows = 0
    for file_path in files:
        total_rows += load_parquet_to_snowflake(str(file_path))

    print(f"Total rows loaded across all files: {total_rows}")

    run_dbt_models()


if __name__ == "__main__":
    nyc_taxi_pipeline()