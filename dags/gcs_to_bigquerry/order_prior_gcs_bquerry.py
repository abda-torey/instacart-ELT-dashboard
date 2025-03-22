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
    'gcs_to_bigquery_order_products_prior',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
    tags=['prior_orders','gcs_to_bq']
) as dag:

    create_bq_table_order_products_prior = BigQueryCreateEmptyTableOperator(
        task_id='create_bq_table_order_products_prior',
        dataset_id='instacart_ELT_dashboard',
        table_id='order_products_prior',
        schema_fields=[
            {'name': 'order_id', 'type': 'STRING', 'mode': 'NULLABLE'},
            {'name': 'product_id', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'add_to_cart_order', 'type': 'INTEGER', 'mode': 'NULLABLE'},
            {'name': 'reordered', 'type': 'INTEGER', 'mode': 'NULLABLE'}
        ],
        project_id='taxi-data-447320'
    )

    load_gcs_to_bq_order_products_prior = GCSToBigQueryOperator(
        task_id='load_gcs_to_bq_order_products_prior',
        bucket='fake-ecommerce-taxi-data-447320',
        source_objects=['order_products_prior_output/order_products_prior/*'],
        destination_project_dataset_table='taxi-data-447320.instacart_ELT_dashboard.order_products_prior',
        write_disposition='WRITE_TRUNCATE',
        source_format='CSV'
    )

    create_bq_table_order_products_prior >> load_gcs_to_bq_order_products_prior
