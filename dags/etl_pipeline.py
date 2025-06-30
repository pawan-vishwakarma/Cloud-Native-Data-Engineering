from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
from google.cloud import storage, bigquery
from config import (
    GCP_PROJECT_ID,
    GCS_BUCKET_NAME,
    BQ_DATASET,
    BQ_TABLE,
    GCS_OBJECT_PATH,
    LOCAL_FILE_PATH,
)

def upload_to_gcs():
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(GCS_OBJECT_PATH)
    blob.upload_from_filename(LOCAL_FILE_PATH)
    print(f"Uploaded {LOCAL_FILE_PATH} to GCS as {GCS_OBJECT_PATH}")

def validate_data():
    df = pd.read_csv(LOCAL_FILE_PATH)
    if df.isnull().values.any():
        raise ValueError("Data validation failed: Null values found.")
    print("Data validation passed.")

def load_to_bq():
    client = bigquery.Client()
    table_id = f"{GCP_PROJECT_ID}.{BQ_DATASET}.{BQ_TABLE}"
    job = client.load_table_from_uri(
        f"gs://{GCS_BUCKET_NAME}/{GCS_OBJECT_PATH}",
        table_id,
        job_config=bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            write_disposition="WRITE_TRUNCATE"
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
