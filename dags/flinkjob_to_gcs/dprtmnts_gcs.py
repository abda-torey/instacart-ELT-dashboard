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
    'departments_to_gcs',
    default_args=default_args,
    description='Move departments to GCS using Flink job',
    schedule_interval=None,
    start_date=days_ago(1),
    tags=['departments','flink_job'],
)

run_flink_command = """
docker exec flink-jobmanager ./bin/flink run -py /opt/src/job/dprtmnts_gcs_job.py --pyFiles /opt/src -d
"""

run_flink_departments_task = BashOperator(
    task_id='run_departments_flink_job',
    bash_command=run_flink_command,
    dag=dag,
)

run_flink_departments_task
