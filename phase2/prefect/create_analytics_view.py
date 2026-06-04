import os
from dotenv import load_dotenv
import snowflake.connector

load_dotenv()

conn = snowflake.connector.connect(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse="COMPUTE_WH",
    database="NYC_TAXI_DB",
    schema="ANALYTICS",
    role="ACCOUNTADMIN"
)

cur = conn.cursor()

cur.execute("""
CREATE OR REPLACE VIEW DAILY_TAXI_METRICS AS
WITH raw_data AS (
    SELECT
        CAST(TPEP_PICKUP_DATETIME AS DATE) AS TRIP_DATE,
        TRIP_DISTANCE,
        TOTAL_AMOUNT
    FROM NYC_TAXI_DB.RAW.RAW_YELLOW_TAXI_TRIPS
    WHERE YEAR(TPEP_PICKUP_DATETIME) = 2024
)
SELECT
    TRIP_DATE,
    COUNT(*) AS TOTAL_TRIPS,
    ROUND(AVG(TRIP_DISTANCE), 2) AS AVG_TRIP_DISTANCE,
    ROUND(AVG(TOTAL_AMOUNT), 2) AS AVG_FARE,
    ROUND(SUM(TOTAL_AMOUNT), 2) AS TOTAL_REVENUE
FROM raw_data
GROUP BY TRIP_DATE
ORDER BY TRIP_DATE
""")

print("Analytics view created successfully.")

cur.close()
conn.close()