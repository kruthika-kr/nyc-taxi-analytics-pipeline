import pyarrow.parquet as pq

file_path = r"data\raw\yellow_tripdata_2024-01.parquet"

parquet_file = pq.ParquetFile(file_path)
df = parquet_file.read_row_group(0).to_pandas()

print(df[["tpep_pickup_datetime", "tpep_dropoff_datetime"]].head(5))
print(df[["tpep_pickup_datetime", "tpep_dropoff_datetime"]].dtypes)