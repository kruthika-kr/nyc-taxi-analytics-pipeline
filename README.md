Project Overview

This project demonstrates an end-to-end cloud data engineering pipeline using NYC Yellow Taxi trip data. The goal was to transform a traditional local ETL workflow into a modern cloud-based analytics platform using Snowflake, dbt, and Power BI.

The pipeline processes over 9.5 million NYC taxi trip records and generates analytics-ready datasets for business intelligence reporting.

Architecture
NYC Taxi Parquet Files
          │
          ▼
      Python
          │
          ▼
     Snowflake
      RAW Layer
 (9,554,778 Rows)
          │
          ▼
         dbt
 Analytics Layer
          │
          ▼
      Power BI
      Dashboard
Dataset

Source: NYC Taxi & Limousine Commission (TLC)

Files Processed:

yellow_tripdata_2024-01.parquet
yellow_tripdata_2024-02.parquet
yellow_tripdata_2024-03.parquet

Total Records Loaded:

9,554,778
Technology Stack
Data Engineering
Python
Pandas
PyArrow
Snowflake
dbt
Analytics & Visualization
Power BI
Version Control
Git
GitHub
Configuration & Security
Environment Variables
.env
python-dotenv
Snowflake Setup

Created:

Database
NYC_TAXI_DB
Schemas
RAW
ANALYTICS
Warehouse
COMPUTE_WH
Data Loading

Taxi data was loaded from Parquet files into:

NYC_TAXI_DB.RAW.RAW_YELLOW_TAXI_TRIPS
Final Row Count
SELECT COUNT(*)
FROM NYC_TAXI_DB.RAW.RAW_YELLOW_TAXI_TRIPS;

Result:

9,554,778 Rows
dbt Transformation Layer
Source Configuration

dbt sources were configured against the Snowflake RAW schema.

Model

Created:

DAILY_TAXI_METRICS

Metrics generated:

Trip Date
Total Trips
Average Trip Distance
Average Fare
Total Revenue
Example Transformation
SELECT
    CAST(TPEP_PICKUP_DATETIME AS DATE) AS TRIP_DATE,
    COUNT(*) AS TOTAL_TRIPS,
    ROUND(AVG(TRIP_DISTANCE), 2) AS AVG_TRIP_DISTANCE,
    ROUND(AVG(TOTAL_AMOUNT), 2) AS AVG_FARE,
    ROUND(SUM(TOTAL_AMOUNT), 2) AS TOTAL_REVENUE
FROM RAW_YELLOW_TAXI_TRIPS
GROUP BY CAST(TPEP_PICKUP_DATETIME AS DATE)
Power BI Dashboard

The Power BI dashboard provides:

KPI Cards
Total Trips
Total Revenue
Average Fare
Average Trip Distance
Trend Analysis
Daily Revenue Trend
Daily Trip Trend
Average Fare Trend
Average Trip Distance Trend
Dashboard Preview
Power BI Dashboard




Snowflake Row Count




dbt Successful Run




Security Improvements

Removed hardcoded credentials from source code.

Implemented:

Environment Variables
.env configuration
dbt env_var() integration
GitHub secret cleanup

Example:

user=os.getenv("SNOWFLAKE_USER")
password=os.getenv("SNOWFLAKE_PASSWORD")
account=os.getenv("SNOWFLAKE_ACCOUNT")
Data Recovery Using Snowflake Time Travel

During development, an accidental:

TRUNCATE TABLE RAW_YELLOW_TAXI_TRIPS;

removed all loaded data.

The table was successfully restored using Snowflake Time Travel and table cloning, recovering:

9,554,778 Records

This demonstrated real-world cloud data recovery and operational troubleshooting skills.

Key Results
Metric	Value
Records Processed	9,554,778
Months Loaded	3
Cloud Warehouse	Snowflake
Transformation Tool	dbt
Dashboard Tool	Power BI
Analytics Rows Generated	96
Future Improvements
Prefect Workflow Orchestration
Automated Data Refresh
Docker Containerization
GitHub Actions CI/CD
Incremental dbt Models
Snowflake Stages & COPY INTO
Data Quality Tests
