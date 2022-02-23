# Spotify - Apache Airflow & Redshift ETL

<img src="https://i.ibb.co/hK65k3x/helmet.png" height="400">

## Project Overview

![preview](https://media3.giphy.com/media/TzNjdLQJGL2SqTZB1C/giphy.gif?cid=790b7611408b01116c27972a7f85e97db510f8360004aa06&rid=giphy.gif&ct=g)

This project is an ETL using Spotipy and generate a weekly email of all the songs played and web scraper additionnal information for each artist listenned. I build an ETL pipeline for a data lake hosted on S3 and Redshift. Therefore I fetch data from the API, clean & process the data into analytics tables using Python, and load them back into S3 & Redshift.

> This program uses: Spotipy, Regex, Apache Airflow and AWS Redshift.

After the extraction, (1) a web scraper get additionnal information (e.g. birthday of the artist) (2) and transform the data using python to clean it up, create unique identifiers, and load it into an AWS Redshift database.

The loading step uses (1) SQL to query the data (2) and python to automate a weekly email that gets sent to my email giving a summary of my Spotify listening for that week.

![preview](email.png)

```
The S3 bucket is under the region: us-east-1
The Redshit DB is under: us-east-2
```

# Resources

- create_tables.py : drops (clear) all tables and create all tables

- python spotify_load_job.py : load the file api/data/db_etl.csv into AWS Redshift

- sql_queries.py : contain all SQL queries with executing create_tables.py

- create_cluster_redshift.py : create the initial redshift cluster and an IAM role to access other AWS services S3

- delete_cluster_redshift.py : delete redshift cluster and IAM role created and you will avoid an invoice.

### Data Pipeline Design

- The ETL pipeline uses Python (pandas), that simplifies data manipulation and the exportation to a csv and boto3 also allows connection to Redshift Database. At this moment, the data are store as a staging stage with the structure below:

```
   CREATE TABLE staging_events_table (
      id VARCHAR(500) PRIMARY KEY,
      song_id VARCHAR(500),
      song_name VARCHAR(500),
      img VARCHAR(500),
      duration_ms VARCHAR(500),
      song_explicit VARCHAR(500),
      url VARCHAR(500),
      popularity VARCHAR(500),
      date_time_played VARCHAR(500),
      album_id VARCHAR(500),
      artist_id VARCHAR(500),
      scraper1 VARCHAR(500),
      scraper2 VARCHAR(500)
    )
   """
```

## Commands

### Venv

> python3 -m venv env

> source env/bin/activate

> cd api && export AIRFLOW_HOME=$PWD

---

> pip freeze > requirements.txt (To generate a .txt)

> pip install -r requirements.txt

Do not forget to validate the command: python spotify_load_job.py

```
NOTE: Make sure you set load_example variable to "False" in airflow.cfg file.
```

- Do not forget to either change the guest setting to public OR create an admin user.

## init_aws

- To run this project in local mode, create a file "dwh.cfg"

#### IAM Access

- IAM user in our AWS account Give it "AdministratorAccess"

#### Steps

All files used to create load and delete he redshift

- Step 1: Create Redshift

  - python create_cluster_redshift.py

- Step 2: Initialize Redshift Database

  - python create_tables.py

- Step 5: Delete Redshift (When done with the project)

  - python delete_cluster_redshift.py (Please do it in order to reduce your invoice)

## etl/init

### Init variables

> airflow variables import init/variables.json

## Airflow Installation

> airflow db init

> cd api && airflow scheduler | TO RUN DO NOT FORGET cd etl && export AIRFLOW_HOME=$PWD and PYTHONPATH

> cd api && airflow webserver | TO RUN DO NOT FORGET cd etl && export AIRFLOW_HOME=$PWD and PYTHONPATH

### AWS Redshift

Redshift is a fully managed, cloud-based, petabyte-scale data warehouse service by Amazon Web Services (AWS). This solution offer to collect and store all data and enables analysis using various business intelligence tools like Power BI.

![preview](redshift_port.png)

> EC2 - Security Groups - default

> Select Redshift from the Type dropdown menu

> You now have 2 new Redshift rules (0.0.0.0/0 AND ::/0)

## Web Scraper

Using Beautiful Soup, the python service is schedule to confirm the birthday date and the release date from:

- Wikipedia
- musicbrainz.org

## References

- https://ruslanmv.com/blog/Create-Data-Warehouse-with-Redshift

- https://hevodata.com/learn/load-csv-to-redshift-3-easy-methods/

- https://www.astronomer.io/guides/managing-dependencies

- https://www.applydatascience.com/airflow/writing-your-first-pipeline/

- https://github.com/SwagLyrics/SwagLyrics-For-Spotify/blob/master/swaglyrics/cli.py (Lyrics Module)
