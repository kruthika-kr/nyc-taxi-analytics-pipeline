import os
import pyarrow.parquet as pq
import snowflake.connector
from dotenv import load_dotenv
from snowflake.connector.pandas_tools import write_pandas

load_dotenv()

file_path = r"data\raw\yellow_tripdata_2024-01.parquet"
parquet_file = pq.ParquetFile(file_path)

df = parquet_file.read_row_group(0).to_pandas()
df = df.head(1000)

# Make all column names uppercase so they match Snowflake
df.columns = [c.upper() for c in df.columns]

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse="COMPUTE_WH",
    database="NYC_TAXI_DB",
    schema="RAW",
    role="ACCOUNTADMIN"
)

success, nchunks, nrows, _ = write_pandas(
    conn,
    df,
    table_name="RAW_YELLOW_TAXI_TRIPS",
    database="NYC_TAXI_DB",
    schema="RAW"
)

print(f"Loaded success={success}, chunks={nchunks}, rows={nrows}")

conn.close()