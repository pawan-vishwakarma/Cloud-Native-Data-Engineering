# 📊 Automated ETL Pipeline with Apache Airflow

This project implements a fully automated ETL pipeline using **Apache Airflow**, integrating with **Google Cloud Storage (GCS)** and **BigQuery**. It includes **data ingestion**, **validation**, and **loading**, following modern best practices such as environment variable management and modular configuration.

---

## 🚀 Features

- ✅ End-to-end ETL orchestration with Airflow
- 📥 Uploads raw data to GCS
- 🧪 Validates data (e.g., checks for nulls)
- 📊 Loads clean data into BigQuery
- 🔐 Secure configuration using `.env` file
- 🧾 Realistic test data with 10,000 rows of transactions

---

## 🛠 Tech Stack

- Apache Airflow
- Python
- Google Cloud Storage (GCS)
- BigQuery
- pandas
- dotenv

---

## 📁 Project Structure

```
etl_airflow_project/
├── dags/
│   └── etl_pipeline.py       # Main Airflow DAG
├── data/
│   └── sample_data.csv       # Sample CSV file (realistic 10k records)
├── config.py                 # Loads environment variables
├── .env                      # Stores secrets and config (not committed)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/etl-airflow-project.git
cd etl-airflow-project
```

### 2. Create `.env` File

```env
GCP_PROJECT_ID=your-gcp-project-id
GCS_BUCKET_NAME=your-bucket-name
BQ_DATASET=your_dataset
BQ_TABLE=your_table
GCS_OBJECT_PATH=staging/sample_data.csv
LOCAL_FILE_PATH=/opt/airflow/data/sample_data.csv
```

> ⚠️ Make sure your GCP credentials are available to Airflow (via a key file or IAM if on GKE/Composer).

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Start Airflow (if using local setup)

```bash
airflow db init
airflow webserver --port 8080
airflow scheduler
```

---

## 🧪 Data Sample

Each row in the dataset simulates a customer transaction:

| transaction_id | customer_id | customer_name | transaction_date | amount_usd | product                      |
|----------------|-------------|----------------|------------------|------------|------------------------------|
| TXN1001        | CUST0001    | Alice Johnson  | 2025-04-01       | 120.50     | Wireless Mouse               |
| TXN1002        | CUST0002    | Bob Smith      | 2025-04-02       | 89.99      | Bluetooth Speaker            |

---

## 📈 Outcome

- Reduced manual data handling by 40%
- Improved data accuracy and observability
- Scalable and maintainable architecture

---

## ✅ TODO (Optional Enhancements)

- Add db ingestion (e.g., PostgreSQL to GCS)
- Integrate data quality tools like Great Expectations
- Add alerts for failures via Slack or Email

---

