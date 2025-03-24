from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago
import os
from dotenv import load_dotenv

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
    'gcs_to_bigquery_aisles',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['aisles', 'gcs_to_bq']
) as dag:

    create_bq_table_aisles = BigQueryCreateEmptyTableOperator(
        task_id='create_bq_table_aisles',
        dataset_id=DATASET_ID,  
        table_id='aisles',
        schema_fields=[
            {'name': 'aisle_id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'aisle', 'type': 'STRING', 'mode': 'NULLABLE'}
        ],
        project_id=PROJECT_ID  
    )

    load_gcs_to_bq_aisles = GCSToBigQueryOperator(
        task_id='load_gcs_to_bq_aisles',
        bucket=BUCKET_NAME,
        source_objects=['insta_cart/aisles/*'],
        destination_project_dataset_table=f'{PROJECT_ID}.{DATASET_ID}.aisles',  # Use f-string for formatting
        write_disposition='WRITE_TRUNCATE',
        source_format='CSV',
        skip_leading_rows=1  # Skip the header row
    )

    create_bq_table_aisles >> load_gcs_to_bq_aisles
