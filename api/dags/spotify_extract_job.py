#This is the Python file to extract the songs from Spotify, transform the data and then load it into PostgreSQL.
#It is placed into a function for my Airflow DAG to call

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import numpy as np

import psycopg2
from sqlalchemy import create_engine
import sys

import json
import logging

## importing the load_dotenv from the python-dotenv module
from dotenv import load_dotenv
 
## using existing module to specify location of the .env file
from pathlib import Path
import os
import requests
from bs4 import BeautifulSoup
import re

from lyrics_queries import lyrics

logging.basicConfig(level=20, datefmt='%I:%M:%S', format='[%(asctime)s] %(message)s')


load_dotenv()
env_path = Path('.')/'.env'
load_dotenv(dotenv_path=env_path)


# retrieving keys and adding them to the project
# from the .env file through their key names
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def spotify_etl_func():

    # Setup the Developer ENV from Spotify Website
    spotify_client_id = CLIENT_ID
    spotify_client_secret = CLIENT_SECRET
    spotify_redirect_url = "http://localhost:8080"
    spotify_req_limit = 25

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id,
                                                   client_secret=spotify_client_secret,
                                                   redirect_uri=spotify_redirect_url,
                                                   scope="user-read-recently-played")) # Here is what we cant to fetch from the API
    
    logging.info('Connected to Spotify...')
    data = sp.current_user_recently_played(limit=spotify_req_limit) # API limitation on requests

    # Check if dataframe is empty
    if data is None:
        logging.info('No songs downloaded. Finishing execution')
        return False

    # Print the DF - json format
    logging.info('Writing raw JSON file...')
    with open("data/dump.json", 'w', encoding='utf-8') as f:
            json.dump(data, f)

    # Reading the JSON and converting to dict
    # Based on https://github.com/karolina-sowinska/free-data-engineering-course-for-beginners/blob/master/dags/spotify_etl.py
    song_list = []
    lyrics_list = []

    for song in data['items']:
        song_id = song['track']['id']
        song_name = song['track']['name']
        song_img = song['track']['album']['images'][0]['url']
        song_url = song['track']['external_urls']['spotify']
        song_duration = song['track']['duration_ms']
        song_explicit = song['track']['explicit']
        song_popularity = song['track']['popularity']
        date_time_played = song['played_at']
        album_id = song['track']['album']['id']
        artist_id = song['track']['album']['artists'][0]['name']

        # bs4 - Scraper
        try:
            r = requests.get('https://musicbrainz.org/search?query={}+{}&type=release&method=indexed'.format(artist_id, song_name).replace(' ', '+'))
            soup = BeautifulSoup(r.content, 'lxml')
            yearHTML = soup.find_all('span', 'release-date')[0] # Select first result

            year = re.findall(r'[0-9]+', str(yearHTML))

            scraper_year = str(year)[1:-1].replace("'", "").replace(",", "-")

            if not len(scraper_year):
                scraper_bday = scraper_bday.fillna(0, inplace=True)
                
        except IndexError:
            scraper_year = 0

        # Get genre
        try:
            w = requests.get('https://en.wikipedia.org/wiki/{}'.format(artist_id).replace(' ', '_'))
            soupW = BeautifulSoup(w.content, 'lxml')

            bdayHTML = soupW.find_all('span', class_='bday')

            bday = re.findall(r'(\d{4})[-](\d{2})[-](\d{2})', str(bdayHTML))
            scraper_bday = str(bday)[1:-1].replace('(','').replace(')','').replace("'", "").replace(",", "-")

            if not len(scraper_bday):
                scraper_bday = 0

        except IndexError:
            scraper_bday = 0

        # Find Lyrics
        try:
           lyrics_song = lyrics(song_name, artist_id)

        except IndexError:
            lyrics_song = 0

        # Generate the row
        song_element = {'song_id':song_id,'song_name':song_name, 'img':song_img, 'duration_ms':song_duration,'song_explicit':song_explicit, 'url':song_url,
                        'popularity':song_popularity,'date_time_played':date_time_played,'album_id':album_id,
                        'artist_id':artist_id, 'scrape1': scraper_year, 'scraper2': scraper_bday
                       }

        song_list.append(song_element)

        lyrics_element = {'song_id':song_id,'song_name':song_name, 'date_time_played':date_time_played, "lyrics": lyrics_song}
        lyrics_list.append(lyrics_element)

    # Converting to DataFrame
    song_df = pd.DataFrame.from_dict(song_list)
    lyrics_df = pd.DataFrame.from_dict(lyrics_list)

    # Primary Key Check
    if pd.Series(song_df['date_time_played']).is_unique:
        pass
    else:
        raise Exception("Primary Key check is violated")

    #date_time_played is an object (data type) changing to a timestamp
    song_df['date_time_played'] = pd.to_datetime(song_df['date_time_played'])


    # Check for nulls
    if song_df.isnull().values.any():
        raise Exception("Null values found")

    # Save in data folder
    logging.info('Writing CSV file...')
    song_df.to_csv("data/db_etl.csv")
    lyrics_df.to_csv("data/lyrics_etl.csv")
    
    return "Finished Extract, Transform"

if __name__ == '__main__':
    spotify_etl_func()