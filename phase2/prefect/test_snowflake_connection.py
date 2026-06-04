import os
from dotenv import load_dotenv
import snowflake.connector

load_dotenv(override=True)

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse="COMPUTE_WH",
    database="NYC_TAXI_DB",
    schema="RAW",
    role="ACCOUNTADMIN"
)

cur = conn.cursor()
cur.execute("SELECT CURRENT_USER();")
print(cur.fetchone())

cur.close()
conn.close()