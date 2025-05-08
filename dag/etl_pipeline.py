from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from google.cloud import storage, bigquery
import os

GCP_PROJECT = "your-gcp-project-id"
GCS_BUCKET = "your-gcs-bucket-name"
BQ_DATASET = "your_dataset"
BQ_TABLE = "your_table"
LOCAL_FILE = "/opt/airflow/data/sample_data.csv"
GCS_PATH = "staging/sample_data.csv"

# Upload to GCS
def upload_to_gcs():
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET)
    blob = bucket.blob(GCS_PATH)
    blob.upload_from_filename(LOCAL_FILE)
    print(f"Uploaded {LOCAL_FILE} to GCS as {GCS_PATH}")

# Validate data (simple check: no nulls)
def validate_data():
    df = pd.read_csv(LOCAL_FILE)
    if df.isnull().values.any():
        raise ValueError("Data validation failed: Null values found.")
    print("Data validation passed.")

# Load into BigQuery
def load_to_bq():
    client = bigquery.Client()
    table_id = f"{GCP_PROJECT}.{BQ_DATASET}.{BQ_TABLE}"
    job = client.load_table_from_uri(
        f"gs://{GCS_BUCKET}/{GCS_PATH}",
        table_id,
        job_config=bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True, write_disposition="WRITE_TRUNCATE"
        ),
    )
    job.result()
    print(f"Loaded data into BigQuery: {table_id}")

with DAG("automated_etl_pipeline",
         start_date=datetime(2023, 1, 1),
         schedule_interval="@daily",
         catchup=False) as dag:

    upload = PythonOperator(task_id="upload_to_gcs", python_callable=upload_to_gcs)
    validate = PythonOperator(task_id="validate_data", python_callable=validate_data)
    load = PythonOperator(task_id="load_to_bq", python_callable=load_to_bq)

    validate >> upload >> load

