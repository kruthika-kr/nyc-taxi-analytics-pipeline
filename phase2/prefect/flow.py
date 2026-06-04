from prefect import flow, task
import pandas as pd
from pathlib import Path


@task
def extract_data(file_path: str) -> pd.DataFrame:
    return pd.read_parquet(file_path)


@task
def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.dropna(subset=["tpep_pickup_datetime", "tpep_dropoff_datetime", "trip_distance", "total_amount"])
    df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["tpep_dropoff_datetime"] = pd.to_datetime(df["tpep_dropoff_datetime"])
    return df


@task
def load_data(df: pd.DataFrame) -> None:
    print(f"Loaded {len(df)} rows into the pipeline step.")


@flow
def nyc_taxi_pipeline(file_path: str):
    df = extract_data(file_path)
    cleaned_df = transform_data(df)
    load_data(cleaned_df)


if __name__ == "__main__":
    sample_file = r"data\raw\yellow_tripdata_2024-01.parquet"
    nyc_taxi_pipeline(sample_file)