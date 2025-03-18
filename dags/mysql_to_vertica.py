from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 3, 17),
    'retries': 1
}

with DAG('mysql_to_vertica', default_args=default_args, schedule_interval='@daily') as dag:
    extract_load = BashOperator(
        task_id='extract_transform_load',
        bash_command='docker exec transfer python /scripts/transfer_data.py'
    )

extract_load
