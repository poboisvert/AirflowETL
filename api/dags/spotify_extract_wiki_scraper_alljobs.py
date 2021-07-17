from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from spotify_extract_job import spotify_etl_func
from spotify_wiki_scraper_job import load
from spotify_weekly_email_job import spotify_weekly_email_function

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'catchup_by_default': False,

    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
}

dag = DAG(
    'spotify_extract_wikiScraper_email_alljobs', 
    default_args=default_args, 
    #schedule_interval=timedelta(days=1))
    schedule_interval= '*/10 * * * *',
    #schedule_interval='@once' # To run the all jobs once
    catchup=False
)

# t1, t2 and t3 are examples of tasks 
# created by instantiating operators
t1 = PythonOperator(
    task_id='extract_transform',
    python_callable=spotify_etl_func,
    dag=dag)

t2 = PythonOperator(
    task_id='load_redshift_db',
    python_callable=load,
    retries=3,
    dag=dag)

t3 = PythonOperator(
    task_id='emails_sender',
    python_callable=spotify_weekly_email_function,
    params={'my_param': 'Parameter I passed in'},
    dag=dag)

t2.set_upstream(t1)
t3.set_upstream(t2)