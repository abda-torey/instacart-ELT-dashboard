from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

# Default args for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# instantiate the DAG
dag = DAG(
    'orders_to_gcs',
    default_args=default_args,
    description = 'A simple dag to save orders csv to bucket',
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['orders','flink_job'],
)

run_flink_command= """
docker exec flink-jobmanager ./bin/flink run -py /opt/src/job/orders_gcs_job.py --pyFiles /opt/src -d
"""
# Task to run the Flink job
run_flink_orders_task = BashOperator(
    task_id='orders_to_gcs',
    bash_command=run_flink_command,
    dag=dag,
)

run_flink_orders_task