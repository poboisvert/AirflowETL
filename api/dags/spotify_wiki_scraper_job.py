import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries
import logging
import boto3
from botocore.exceptions import ClientError

## importing the load_dotenv from the python-dotenv module
from dotenv import load_dotenv
 
## using existing module to specify location of the .env file
from pathlib import Path
import os
 
logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')


load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)

# CONFIG
def upload_file(path="data/db_etl.csv"):
    session = boto3.resource(
        's3',
        region_name='us-east-1',
        aws_access_key_id=os.getenv("KEY_IAM_AWS"),
        aws_secret_access_key=os.getenv("SECRET_IAM_AWS")
    )

    session = boto3.session.Session()

    s3 = session.resource('s3')
    bucket = s3.Bucket('bhoodpreprod')

    print("Bucket Online")

    with open(path, 'rb') as data:
                bucket.put_object(Key='data/db_etl.csv', Body=data)

def load_staging_tables(cur, conn):
    """
    Description: load the datasets in S3 AWS into SQL tables  

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
    config = configparser.ConfigParser()
    config.read('../dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()    

    # Log data into the table
    upload_file()
    load_staging_tables(cur, conn)

    conn.close()

if __name__ == "__main__":
    load()