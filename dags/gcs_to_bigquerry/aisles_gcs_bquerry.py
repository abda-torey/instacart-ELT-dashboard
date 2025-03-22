from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago

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
    tags=['aisles','gcs_to_bq']
) as dag:

    create_bq_table_aisles = BigQueryCreateEmptyTableOperator(
        task_id='create_bq_table_aisles',
        dataset_id='instacart_ELT_dashboard',
        table_id='aisles',
        schema_fields=[
            {'name': 'aisle_id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'aisle', 'type': 'STRING', 'mode': 'NULLABLE'}
        ],
        project_id='taxi-data-447320'
    )

    load_gcs_to_bq_aisles = GCSToBigQueryOperator(
        task_id='load_gcs_to_bq_aisles',
        bucket='fake-ecommerce-taxi-data-447320',
        source_objects=['aisles_output/aisles/*'],
        destination_project_dataset_table='taxi-data-447320.instacart_ELT_dashboard.aisles',
        write_disposition='WRITE_TRUNCATE',
        source_format='CSV'
    )

    create_bq_table_aisles >> load_gcs_to_bq_aisles
