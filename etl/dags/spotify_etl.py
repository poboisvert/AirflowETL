from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

from scripts.spotify_extract_job import spotify_etl_func
from scripts.spotify_db_job import load
from scripts.spotify_weekly_email_job import spotify_weekly_email_function

from datetime import timedelta, datetime
import os

START_DATE = datetime(2021, 12, 1)
DAG_ID = os.path.basename(__file__).replace(".py", "")

default_args = {
    "depends_on_past": False,
    "start_date": START_DATE,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG(
    DAG_ID,
    default_args=default_args,
    schedule_interval="*/10 * * * *",
    catchup=False,
    tags=["AWS", "Spotify", "GMAIL"],
)

t1 = PythonOperator(
    task_id="extract_transform", python_callable=spotify_etl_func, dag=dag
)

t2 = PythonOperator(
    task_id="load_db", python_callable=load, dag=dag
)

t3 = PythonOperator(
    task_id="emails",
    python_callable=spotify_weekly_email_function,
    dag=dag,
)

t2.set_upstream(t1)
t3.set_upstream(t2)
