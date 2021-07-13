from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from spotify_job import spotify_etl_func
from airflow.utils.dates import days_ago

my_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'email': ['culpgrant21@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
my_dag = DAG(
    'spotify_etl_dag',
    default_args = my_args,
    description= 'Spotify ETL',
    schedule_interval= '*/5 * * * *'
)


run_etl = PythonOperator(
    task_id='spotify_etl_sql',
    python_callable=spotify_etl_func,
    dag=my_dag
)
run_etl