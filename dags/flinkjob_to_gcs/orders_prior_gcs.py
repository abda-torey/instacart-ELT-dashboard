from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'order_prior_to_gcs',
    default_args=default_args,
    description='Move order_prior to GCS using Flink job',
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['order_prior','flink_job'],
)

run_flink_command = """
docker exec flink-jobmanager ./bin/flink run -py /opt/src/job/order_prior_gcs_job.py --pyFiles /opt/src -d
"""

run_flink_order_prior_task = BashOperator(
    task_id='run_order_prior_flink_job',
    bash_command=run_flink_command,
    dag=dag,
)

run_flink_order_prior_task
