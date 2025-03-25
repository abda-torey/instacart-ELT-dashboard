from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

BUCKET_NAME = os.getenv("GCP_BUCKET_NAME")
DATASET_ID = os.getenv("DATASET_ID")
PROJECT_ID = os.getenv("PROJECT_ID")

default_args = {
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

with DAG(
    'gcs_to_bigquery_departments',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['departments','gcs_to_bq']
) as dag:

    create_bq_table_departments = BigQueryCreateEmptyTableOperator(
        task_id='create_bq_table_departments',
        dataset_id=DATASET_ID,
        table_id='departments',
        schema_fields=[
            {'name': 'department_id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'department', 'type': 'STRING', 'mode': 'NULLABLE'}
        ],
        project_id=PROJECT_ID
    )

    load_gcs_to_bq_departments = GCSToBigQueryOperator(
        task_id='load_gcs_to_bq_departments',
        bucket=BUCKET_NAME,
        source_objects=['insta_cart/departments/*'],
        destination_project_dataset_table=f'{PROJECT_ID}.{DATASET_ID}.departments',
        write_disposition='WRITE_TRUNCATE',
        skip_leading_rows=1,  # Skip the header row
        source_format='CSV'
    )

    create_bq_table_departments >> load_gcs_to_bq_departments
