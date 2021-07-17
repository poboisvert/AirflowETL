from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from spotify_wiki_scraper_job import load
from airflow.utils.dates import days_ago

my_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email': ['job@job.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

my_dag = DAG(
    'spotify_wiki_dag',
    default_args = my_args,
    description= 'Spotify Wiki Information',
    #schedule_interval= '*/2 * * * *'
    schedule_interval='@once'
)


run_etl = PythonOperator(
    task_id='spotify_wiki',
    python_callable=load,
    dag=my_dag
)
run_etl