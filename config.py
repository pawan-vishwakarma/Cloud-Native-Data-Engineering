from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env file

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
BQ_DATASET = os.getenv("BQ_DATASET")
BQ_TABLE = os.getenv("BQ_TABLE")
GCS_OBJECT_PATH = os.getenv("GCS_OBJECT_PATH")
LOCAL_FILE_PATH = os.getenv("LOCAL_FILE_PATH")

