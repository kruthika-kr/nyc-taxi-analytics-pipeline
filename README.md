# 🚖 NYC Taxi Analytics Pipeline

## Overview

This project implements an end-to-end ETL (Extract, Transform, Load) and analytics pipeline using the NYC Yellow Taxi dataset.

The pipeline extracts raw taxi trip data stored in Parquet format, performs data cleaning and transformation using Python and Pandas, loads the processed data into Microsoft SQL Server, and generates business insights through SQL analytics queries and views.

The project processes over **9.5 million taxi trip records**, demonstrating practical data engineering skills including data ingestion, transformation, storage, and analytical reporting.

---

## Project Architecture

```text
NYC Taxi Parquet Files
          │
          ▼
Python + Pandas
(Data Cleaning & Validation)
          │
          ▼
SQLAlchemy
          │
          ▼
SQL Server
(raw_yellow_taxi_trips)
          │
          ▼
SQL Views & Analytics Queries
          │
          ▼
Business Insights
```

---

## Dataset

### Source

NYC Taxi & Limousine Commission (TLC)

### Files Used

```text
yellow_tripdata_2024-01.parquet
yellow_tripdata_2024-02.parquet
yellow_tripdata_2024-03.parquet
```

### Records Processed

```text
9,554,778 rows
```

---

## Technologies Used

### Programming Languages

- Python
- SQL

### Python Libraries

- Pandas
- SQLAlchemy
- PyODBC

### Database

- Microsoft SQL Server Express 2022

### File Format

- Apache Parquet

### Development Tools

- Visual Studio Code
- SQL Server Management Studio (SSMS)
- Git
- GitHub

---

## ETL Pipeline

### Extract

Raw NYC Yellow Taxi trip data is extracted from Parquet files using Pandas.

### Transform

Data transformation includes:

- Data type standardization
- Datetime conversion
- Null value handling
- Basic data quality checks
- Record validation

### Load

Cleaned records are loaded into SQL Server.

Target table:

```sql
raw_yellow_taxi_trips
```

Total records loaded:

```text
9,554,778
```

---

## Database Design

### Raw Data Layer

```sql
raw_yellow_taxi_trips
```

Stores detailed taxi trip information including:

- Pickup time
- Dropoff time
- Passenger count
- Trip distance
- Fare amount
- Payment type
- Pickup location
- Dropoff location

---

## Analytics Views

### 1. Daily Trip Summary View

```sql
vw_trip_summary
```

Provides:

- Daily trip counts
- Average trip distance
- Average fare amount
- Daily revenue

---

### 2. Payment Analysis View

```sql
vw_payment_analysis
```

Provides:

- Trips by payment type
- Revenue by payment type
- Average fare by payment type

---

## Business Analytics

### Peak Pickup Hours Analysis

Query used:

```sql
SELECT
    DATEPART(HOUR, tpep_pickup_datetime) AS pickup_hour,
    COUNT(*) AS total_trips
FROM dbo.raw_yellow_taxi_trips
WHERE YEAR(tpep_pickup_datetime) = 2024
GROUP BY DATEPART(HOUR, tpep_pickup_datetime)
ORDER BY total_trips DESC;
```

### Results

| Pickup Hour | Trips |
|------------|--------:|
| 18 (6 PM) | 690,932 |
| 17 (5 PM) | 653,781 |
| 19 (7 PM) | 614,084 |

### Insight

Taxi demand peaks between **5 PM and 7 PM**, with **6 PM** being the busiest hour.

This pattern reflects evening commuter traffic across New York City.

---

## Top Revenue Pickup Zones

Query used:

```sql
SELECT TOP 10
    PULocationID,
    COUNT(*) AS total_trips,
    SUM(total_amount) AS total_revenue
FROM dbo.raw_yellow_taxi_trips
WHERE YEAR(tpep_pickup_datetime)=2024
GROUP BY PULocationID
ORDER BY total_revenue DESC;
```

### Results

| Pickup Zone | Revenue |
|------------|---------:|
| 132 | $33.1M |
| 138 | $18.7M |
| 161 | $10.8M |

### Insight

Pickup Zone **132** generated more than **$33 million** in revenue, making it the highest-performing pickup location in the dataset.

---

## Payment Type Analysis

Query used:

```sql
SELECT
    payment_type,
    COUNT(*) AS trips,
    AVG(total_amount) AS avg_fare,
    SUM(total_amount) AS revenue
FROM dbo.raw_yellow_taxi_trips
WHERE YEAR(tpep_pickup_datetime)=2024
GROUP BY payment_type;
```

### Results

| Payment Type | Trips | Revenue |
|-------------|--------:|---------:|
| 2 | 1,330,099 | $30.4M |
| 1 | 725,814 | $20.7M |
| 0 | 751,962 | $18.1M |

### Insight

Payment Type **2** generated the highest overall revenue among analyzed trips.

---

## Project Structure

```text
nyc-taxi-analytics-pipeline/
│
├── data/
│
├── src/
│   └── ingestion/
│       └── load_raw_data.py
│
├── sql/
│   ├── analytics_queries.sql
│   ├── create_views.sql
│   └── create_summary_tables.sql
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Key Skills Demonstrated

### Data Engineering

- ETL Pipeline Development
- Data Ingestion
- Data Transformation
- Data Validation
- Large Dataset Processing

### Database Engineering

- SQL Server Administration
- Data Modeling
- SQL Query Optimization
- View Creation
- Aggregation Analysis

### Analytics

- Revenue Analysis
- Operational Metrics
- Trend Analysis
- Business Intelligence Reporting

---

## Future Enhancements

Planned improvements include:

- Automated workflow orchestration using Prefect
- Cloud data warehouse integration using BigQuery
- dbt transformation layer
- Interactive dashboard using Power BI or Streamlit
- Docker containerization
- CI/CD using GitHub Actions

---

## Author

**Kruthika Kadurhalli Raghu**

Graduate Student – Data Science  
Arizona State University

---
