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
    'gcs_to_bigquery_products',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['products','gcs_to_bq']
) as dag:

    create_bq_table_products = BigQueryCreateEmptyTableOperator(
        task_id='create_bq_table_products',
        dataset_id=DATASET_ID,
        table_id='products',
        schema_fields=[
            {'name': 'product_id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'product_name', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'aisle_id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'department_id', 'type': 'INTEGER', 'mode': 'NULLABLE'}
        ],
        project_id=PROJECT_ID
    )

    load_gcs_to_bq_products = GCSToBigQueryOperator(
        task_id='load_gcs_to_bq_products',
        bucket='fake-ecommerce-taxi-data-447320',
        source_objects=['insta_cart/products/*'],
        destination_project_dataset_table=f'{PROJECT_ID}.{DATASET_ID}.products',
        write_disposition='WRITE_TRUNCATE',
        skip_leading_rows=1,  # Skip the header row
        source_format='CSV'
    )

    create_bq_table_products >> load_gcs_to_bq_products
