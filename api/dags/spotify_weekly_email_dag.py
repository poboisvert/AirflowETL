from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils.dates import days_ago

from spotify_weekly_email_job import spotify_weekly_email_function

my_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': ['test@test.com'],
    'email_on_failure': True,
    'email_on_retry': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
my_dag = DAG(
    'spotify_email_dag',
    default_args = my_args,
    description= 'Spotify Weekly Email',
    #schedule_interval= '* * * * *'
    schedule_interval='@once'
    )


run_email = PythonOperator(
    task_id='spotify_weekly_email',
    python_callable= spotify_weekly_email_function,
    dag=my_dag
)
run_email