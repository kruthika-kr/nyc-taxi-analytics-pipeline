CREATE OR ALTER VIEW dbo.vw_trip_summary AS
SELECT
    CAST(tpep_pickup_datetime AS DATE) AS trip_date,
    COUNT(*) AS total_trips,
    AVG(trip_distance) AS avg_distance,
    AVG(total_amount) AS avg_fare,
    SUM(total_amount) AS revenue
FROM dbo.raw_yellow_taxi_trips
WHERE YEAR(tpep_pickup_datetime) = 2024
GROUP BY CAST(tpep_pickup_datetime AS DATE);
GO


CREATE OR ALTER VIEW dbo.vw_payment_analysis AS
SELECT
    payment_type,
    COUNT(*) AS total_trips,
    AVG(total_amount) AS avg_fare,
    SUM(total_amount) AS revenue
FROM dbo.raw_yellow_taxi_trips
WHERE YEAR(tpep_pickup_datetime) = 2024
GROUP BY payment_type;
GO