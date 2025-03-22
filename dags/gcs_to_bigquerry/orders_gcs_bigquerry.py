from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago

# Default args for the DAG
default_args = {
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the DAG
with DAG(
    'gcs_to_bigquery_orders',
    default_args=default_args,
    schedule_interval=None,  # Schedule to run daily
    catchup=False,
    tags=['orders','gcs_to_bq']
) as dag:

    # Create BigQuery table if it doesn't exist
    create_bq_table = BigQueryCreateEmptyTableOperator(
        task_id='create_bq_table_orders',
        dataset_id='instacart_ELT_dashboard',  # Replace with your dataset name
        table_id='orders',  # Table name in BigQuery
        schema_fields=[
            {'name': 'order_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'user_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'eval_set', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'order_number', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'order_dow', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'order_hour_of_day', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'days_since_prior_order', 'type': 'FLOAT', 'mode': 'NULLABLE'}
        ],
        project_id='taxi-data-447320'  # Replace with your GCP project ID
    )

    # Load data from GCS to BigQuery
    load_gcs_to_bq = GCSToBigQueryOperator(
        task_id='load_gcs_to_bq_orders',
        bucket='fake-ecommerce-taxi-data-447320',  # Your GCS bucket
        source_objects=['orders_output/orders/*'],  # Path to the orders CSV file in GCS
        destination_project_dataset_table='taxi-data-447320.instacart_ELT_dashboard.orders',  # Adjust to match your project and dataset
        schema_fields=[
            {'name': 'order_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'user_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'eval_set', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'order_number', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'order_dow', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'order_hour_of_day', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'days_since_prior_order', 'type': 'FLOAT', 'mode': 'NULLABLE'}
        ],
        write_disposition='WRITE_TRUNCATE',  # Overwrite the table each time (use WRITE_APPEND to append data)
        source_format='CSV'  # File format in GCS
    )

    # Define task dependencies
    create_bq_table >> load_gcs_to_bq
