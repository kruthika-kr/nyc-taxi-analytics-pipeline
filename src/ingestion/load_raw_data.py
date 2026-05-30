import logging
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine

# -----------------------------
# SQL Server Configuration
# -----------------------------
SERVER = "localhost\\SQLEXPRESS"
DATABASE = "nyc_taxi_pipeline"

CONN_STR = (
    f"mssql+pyodbc://@{SERVER}/{DATABASE}"
    "?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)

engine = create_engine(CONN_STR, fast_executemany=True)

# -----------------------------
# Paths
# -----------------------------
DATA_DIR = Path(r"E:\Portfolio\nyc-taxi-analytics-pipeline\data\raw")
LOG_DIR = Path(r"E:\Portfolio\nyc-taxi-analytics-pipeline\logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    filename=LOG_DIR / "ingestion.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

TABLE_NAME = "raw_yellow_taxi_trips"

# Small enough to avoid memory issues
# and safe for SQL Server insert handling
PARQUET_BATCH_SIZE = 5000
SQL_CHUNK_SIZE = 500

EXPECTED_COLUMNS = [
    "VendorID",
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "passenger_count",
    "trip_distance",
    "RatecodeID",
    "store_and_fwd_flag",
    "PULocationID",
    "DOLocationID",
    "payment_type",
    "fare_amount",
    "extra",
    "mta_tax",
    "tip_amount",
    "tolls_amount",
    "improvement_surcharge",
    "total_amount",
    "congestion_surcharge",
    "Airport_fee",
]

files = sorted(DATA_DIR.glob("*.parquet"))

print(f"Found {len(files)} parquet files")
logging.info(f"Found {len(files)} parquet files in {DATA_DIR}")

for file_path in files:
    print(f"\nProcessing: {file_path.name}")
    logging.info(f"Starting file: {file_path.name}")

    try:
        parquet_file = pq.ParquetFile(file_path)
        total_rows = 0

        for batch in parquet_file.iter_batches(batch_size=PARQUET_BATCH_SIZE):
            df = batch.to_pandas()

            # Keep only expected columns and order them correctly
            df = df[EXPECTED_COLUMNS]

            # Convert datetime columns
            df["tpep_pickup_datetime"] = pd.to_datetime(
                df["tpep_pickup_datetime"], errors="coerce"
            )
            df["tpep_dropoff_datetime"] = pd.to_datetime(
                df["tpep_dropoff_datetime"], errors="coerce"
            )

            # Replace NaN with None for SQL inserts
            df = df.where(pd.notnull(df), None)

            # Insert batch into SQL Server
            df.to_sql(
                name=TABLE_NAME,
                con=engine,
                if_exists="append",
                index=False,
                chunksize=SQL_CHUNK_SIZE,
            )

            total_rows += len(df)
            print(f"Loaded batch. Total rows so far: {total_rows}")

        print(f"Finished loading: {file_path.name} | Rows loaded: {total_rows}")
        logging.info(f"Finished file: {file_path.name} | Rows loaded: {total_rows}")

    except Exception as e:
        print(f"ERROR while processing {file_path.name}: {e}")
        logging.exception(f"Failed on file {file_path.name}")

print("\nAll files processed.")
logging.info("Pipeline finished.")