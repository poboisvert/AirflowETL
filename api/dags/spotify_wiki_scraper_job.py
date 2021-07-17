#!/bin/python
import json
import string
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import psycopg2

import logging
import configparser

## importing the load_dotenv from the python-dotenv module
from dotenv import load_dotenv
 
## using existing module to specify location of the .env file
from pathlib import Path
import os
 
logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')

config = configparser.ConfigParser()
config.read('../../dwh.cfg')

def get_track_details(artist = "2Pac", track = "California Love"):

    # SQL Connection
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    today = datetime.today().date()
    six_days_ago = today - timedelta(days=6)

    #Top 5 Songs by Time Listened (MIN)
    top_5_songs_min = []
    cur.execute('SELECT TOP 5 * FROM staging_events_table')
    for row in cur.fetchall():
        song_name = row[2]
        min_listened = row[4]
        element = [song_name,min_listened]
        top_5_songs_min.append(element)

    #print(top_5_songs_min)
    top_5_count = []
    cur.execute('SELECT song_name, count(*) FROM staging_events_table GROUP BY song_name ORDER BY count DESC LIMIT 5')
    for row in cur.fetchall():
        song_name = row[0]
        min_listened = row[1]
        element = [song_name,min_listened]
        top_5_count.append(element)

    print(top_5_count)

    conn.close()


if __name__ == '__main__':
    get_track_details()
