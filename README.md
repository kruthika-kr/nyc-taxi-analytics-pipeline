# 🚕 NYC Taxi Analytics Pipeline (Cloud Data Engineering Project)

## Overview

This project demonstrates an end-to-end cloud data engineering pipeline built using NYC Yellow Taxi trip data.

The objective was to modernize a traditional local ETL workflow into a cloud-based analytics platform using Snowflake, dbt, and Power BI.

### Pipeline Architecture

```text
NYC Taxi Parquet Files
          │
          ▼
       Python
          │
          ▼
      Snowflake
      RAW Layer
   (9.55M Records)
          │
          ▼
         dbt
 Analytics Layer
          │
          ▼
      Power BI
      Dashboard
```

---

# Dataset

Source: NYC Taxi & Limousine Commission (TLC)

Files Processed:

* yellow_tripdata_2024-01.parquet
* yellow_tripdata_2024-02.parquet
* yellow_tripdata_2024-03.parquet

Total Records Loaded:

```text
9,554,778 Rows
```

---

# Technology Stack

### Data Engineering

* Python
* Pandas
* PyArrow
* Snowflake
* dbt

### Analytics

* Power BI

### Version Control

* Git
* GitHub

### Security

* Environment Variables
* python-dotenv
* dbt env_var()

---

# Snowflake Setup

### Database

```sql
NYC_TAXI_DB
```

### Schemas

```sql
RAW
ANALYTICS
```

### Warehouse

```sql
COMPUTE_WH
```

---

# Data Loading

Loaded Parquet files into:

```sql
NYC_TAXI_DB.RAW.RAW_YELLOW_TAXI_TRIPS
```

Final Row Count:

```sql
SELECT COUNT(*)
FROM NYC_TAXI_DB.RAW.RAW_YELLOW_TAXI_TRIPS;
```

Result:

```text
9,554,778 Rows
```

---

# dbt Analytics Layer

Created analytics model:

```sql
DAILY_TAXI_METRICS
```

Metrics generated:

* Trip Date
* Total Trips
* Average Trip Distance
* Average Fare
* Total Revenue

Example Transformation:

```sql
SELECT
    CAST(TPEP_PICKUP_DATETIME AS DATE) AS TRIP_DATE,
    COUNT(*) AS TOTAL_TRIPS,
    ROUND(AVG(TRIP_DISTANCE), 2) AS AVG_TRIP_DISTANCE,
    ROUND(AVG(TOTAL_AMOUNT), 2) AS AVG_FARE,
    ROUND(SUM(TOTAL_AMOUNT), 2) AS TOTAL_REVENUE
FROM RAW_YELLOW_TAXI_TRIPS
GROUP BY CAST(TPEP_PICKUP_DATETIME AS DATE)
```

---

# Power BI Dashboard

The dashboard includes:

### KPI Metrics

* Total Trips
* Total Revenue
* Average Fare
* Average Trip Distance

### Trend Analysis

* Daily Trips Trend
* Daily Revenue Trend
* Average Fare Trend
* Average Trip Distance Trend

---

# Dashboard Preview

## Power BI Dashboard

![Power BI Dashboard](phase2/dashboard/screenshots/dashboard.png)

## Snowflake Row Count

![Snowflake Row Count](phase2/dashboard/screenshots/snowflake_row_count.png)

## dbt Successful Run

![dbt Run](phase2/dashboard/screenshots/dbt_success.png)

---

# Security Improvements

Removed hardcoded Snowflake credentials and implemented environment variable configuration.

Example:

```python
user=os.getenv("SNOWFLAKE_USER")
password=os.getenv("SNOWFLAKE_PASSWORD")
account=os.getenv("SNOWFLAKE_ACCOUNT")
```

Implemented:

* .env configuration
* python-dotenv
* dbt env_var()
* GitHub secret cleanup

---

# Snowflake Time Travel Recovery

During development, an accidental:

```sql
TRUNCATE TABLE RAW_YELLOW_TAXI_TRIPS;
```

removed all loaded data.

The dataset was successfully recovered using Snowflake Time Travel and table cloning, restoring:

```text
9,554,778 Records
```

This demonstrates cloud data recovery and operational troubleshooting skills.

---

# Results

| Metric                   | Value     |
| ------------------------ | --------- |
| Records Processed        | 9,554,778 |
| Months Loaded            | 3         |
| Cloud Warehouse          | Snowflake |
| Transformation Tool      | dbt       |
| Dashboard Tool           | Power BI  |
| Analytics Rows Generated | 96        |

---

# Future Enhancements

* Prefect Workflow Orchestration
* Automated Data Refresh
* Docker Containerization
* GitHub Actions CI/CD
* Incremental dbt Models
* Data Quality Testing

---

# Author

**Kruthika Kadurhalli Raghu**

Graduate Student – Data Science
Arizona State University

GitHub: https://github.com/kruthika-kr
