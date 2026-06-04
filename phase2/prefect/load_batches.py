import os
import pyarrow.parquet as pq
import snowflake.connector
from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas

load_dotenv()

FILE_PATH = r"data\raw\yellow_tripdata_2024-01.parquet"
BATCH_SIZE = 5000

parquet_file = pq.ParquetFile(FILE_PATH)

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse="COMPUTE_WH",
    database="NYC_TAXI_DB",
    schema="RAW",
    role="ACCOUNTADMIN"
)

rows_loaded = 0

for batch in parquet_file.iter_batches(batch_size=BATCH_SIZE):
    df = batch.to_pandas()

    df.columns = [c.upper() for c in df.columns]

    df["TPEP_PICKUP_DATETIME"] = df["TPEP_PICKUP_DATETIME"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df["TPEP_DROPOFF_DATETIME"] = df["TPEP_DROPOFF_DATETIME"].dt.strftime("%Y-%m-%d %H:%M:%S")

    success, nchunks, nrows, _ = write_pandas(
        conn,
        df,
        table_name="RAW_YELLOW_TAXI_TRIPS",
        database="NYC_TAXI_DB",
        schema="RAW"
    )

    rows_loaded += nrows
    print(f"Loaded batch. Total rows so far: {rows_loaded}")

conn.close()
print(f"Finished loading {rows_loaded} rows.")