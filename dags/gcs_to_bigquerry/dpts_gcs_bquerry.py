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
    'gcs_to_bigquery_departments',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['departments','gcs_to_bq']
) as dag:

    create_bq_table_departments = BigQueryCreateEmptyTableOperator(
        task_id='create_bq_table_departments',
        dataset_id='instacart_ELT_dashboard',
        table_id='departments',
        schema_fields=[
            {'name': 'department_id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'department', 'type': 'STRING', 'mode': 'NULLABLE'}
        ],
        project_id='taxi-data-447320'
    )

    load_gcs_to_bq_departments = GCSToBigQueryOperator(
        task_id='load_gcs_to_bq_departments',
        bucket='fake-ecommerce-taxi-data-447320',
        source_objects=['departments_output/departments/*'],
        destination_project_dataset_table='taxi-data-447320.instacart_ELT_dashboard.departments',
        write_disposition='WRITE_TRUNCATE',
        source_format='CSV'
    )

    create_bq_table_departments >> load_gcs_to_bq_departments
