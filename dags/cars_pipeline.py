from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
# Import your existing logic
from main import run_pipeline 

default_args = {
    'owner': 'vinicius',
    'depends_on_past': False,
    'start_date': datetime(2026, 3, 11),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'oncar_elt_flow',
    default_args=default_args,
    description='Extract from API, Load to Postgres, Transform with dbt',
    schedule_interval='@daily',
    catchup=False
) as dag:

    # Task 1: Run your Python Extraction/Load
    extract_load = PythonOperator(
        task_id='extract_and_load_python',
        python_callable=run_pipeline
    )

    # Task 2: Run dbt Transformation
    # We use BashOperator to run the exact command you tested manually
    transform_dbt = BashOperator(
        task_id='transform_with_dbt',
    # We remove "python3 -m" and just call "dbt" directly
    bash_command='cd /opt/airflow/transform && dbt --no-write-json run --profiles-dir ../.dbt'    
    )

    # Define the Dependency (The "Arrow" in your diagram)
    extract_load >> transform_dbt