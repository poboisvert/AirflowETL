import configparser
import psycopg2
from sql_queries import copy_table_queries
import logging
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

from pathlib import Path
import os

from airflow.models import Variable


logging.basicConfig(level=20, datefmt="%I:%M:%S", format="[%(asctime)s] %(message)s")

#BUCKET_NAME = os.getenv("BUCKET_NAME")
BUCKET_NAME = Variable.get("BUCKET_NAME")

# CONFIG
def upload_file(path):
    session = boto3.resource(
        "s3",
        region_name="us-east-1",
        aws_access_key_id=Variable.get("KEY_IAM_AWS"),
        aws_secret_access_key=Variable.get("SECRET_IAM_AWS"),
    )

    session = boto3.session.Session()

    s3 = session.resource("s3")
    bucket = s3.Bucket(BUCKET_NAME)

    print("Bucket Online")

    with open(path, "rb") as data:
        bucket.put_object(Key=path, Body=data)


def load_staging_tables(cur, conn):
    """load the datasets in S3 AWS into SQL tables
    Arguments:
        cur: the cursor object.
        conn: the conection to the postgresSQL.
    Returns:
        None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def load():
    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            Variable.get("HOST"), Variable.get("DB_NAME"),Variable.get("DB_USER"),Variable.get("DB_PASSWORD"),Variable.get("DB_PORT")
        )
    )
    cur = conn.cursor()

    upload_file("data/db_etl.csv")
    upload_file("data/lyrics_etl.csv")
    load_staging_tables(cur, conn)
    conn.close()


if __name__ == "__main__":
    load()
