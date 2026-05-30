USE nyc_taxi_pipeline;
GO

SELECT TOP 10
    CAST(tpep_pickup_datetime AS DATE) AS trip_date,
    COUNT(*) AS total_trips,
    ROUND(AVG(trip_distance), 2) AS avg_distance,
    ROUND(AVG(total_amount), 2) AS avg_fare,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM dbo.raw_yellow_taxi_trips
WHERE YEAR(tpep_pickup_datetime) = 2024
GROUP BY CAST(tpep_pickup_datetime AS DATE)
ORDER BY total_revenue DESC;
GO

SELECT
    DATEPART(HOUR, tpep_pickup_datetime) AS pickup_hour,
    COUNT(*) AS total_trips
FROM dbo.raw_yellow_taxi_trips
WHERE YEAR(tpep_pickup_datetime) = 2024
GROUP BY DATEPART(HOUR, tpep_pickup_datetime)
ORDER BY total_trips DESC;

-- Top Revenue Pickup Zones

SELECT TOP 10
    PULocationID,
    COUNT(*) AS total_trips,
    ROUND(SUM(total_amount),2) AS total_revenue
FROM dbo.raw_yellow_taxi_trips
WHERE YEAR(tpep_pickup_datetime) = 2024
GROUP BY PULocationID
ORDER BY total_revenue DESC;

SELECT
    payment_type,
    COUNT(*) AS trips,
    ROUND(AVG(total_amount),2) AS avg_fare,
    ROUND(SUM(total_amount),2) AS revenue
FROM dbo.raw_yellow_taxi_trips
WHERE YEAR(tpep_pickup_datetime)=2024
GROUP BY payment_type
ORDER BY revenue DESC;