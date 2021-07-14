# SpotifyETL

## Project Overview

This project is an ETL using Spotipy and general a weekly email of all the songs played and web scraper additionnal information for each artist listenned.

This program uses Spotipy, Regex, Apache Airflow and AWS Redshift.

After the extraction, I web scrape additionnal information like birthday of the artist and transform the data using python to clean it up, create unique identifiers, and load it into a Redshift database.

The loading step uses (1) SQL to query the data (2) and python to automate a weekly email that gets sent to my email giving a summary of my Spotify listening for that week.

### Preview

![preview](airflow_init.png)

> python3 -m venv env

> source env/bin/activate

> cd api && export AIRFLOW_HOME=$PWD

## Airflow Installation

> airflow db init

> cd api && airflow scheduler

> cd api && airflow webserver

### Venv

> python3 -m venv env

> pip freeze > requirements.txt (To generate)

> pip install -r requirements.txt

## Web Scraper

- Selenium / Beautiful Soup
