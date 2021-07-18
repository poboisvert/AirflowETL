import configparser

import logging

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
config = configparser.ConfigParser()
config.read('../dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs_table"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

staging_events_table_create= (
   """
   CREATE TABLE staging_events_table (
      id VARCHAR(255) PRIMARY KEY,
      song_id VARCHAR(255),
      song_name VARCHAR(255),
      img VARCHAR(255),
      duration_ms VARCHAR(255),
      song_explicit VARCHAR(255),
      url VARCHAR(255),
      popularity VARCHAR(255),
      date_time_played VARCHAR(255),
      album_id VARCHAR(255),
      artist_id VARCHAR(255),
      scraper1 VARCHAR(255),
      scraper2 VARCHAR(255),
      lyrics_song VARCHAR(255)
    )
   """
)

# STAGING TABLES
staging_events_copy = (
    """
    COPY staging_events_table (id,song_id, song_name, img, duration_ms,song_explicit,url,popularity,date_time_played,album_id,artist_id, scraper1, scraper2, lyrics_song)
    FROM '{}'
    credentials 'aws_access_key_id={};aws_secret_access_key={}'
    csv
    IGNOREHEADER 1
    region 'us-east-1';
    """
).format(os.getenv("LOG_DATA"), os.getenv("KEY_IAM_AWS"), os.getenv("SECRET_IAM_AWS"))



# FINAL TABLES

songplay_table_insert = (
   """
   INSERT INTO songplays (start_time, user_id, level, song_id, artist_id, 
                          session_id, location, user_agent)
   SELECT se.ts, se.userId, se.level, sa.song_id, sa.artist_id, se.sessionId, 
          se.location, se.userAgent 
   FROM staging_events_table se
   JOIN (
         SELECT s.song_id AS song_id, a.artist_id AS artist_id, s.title AS song, 
         a.name AS artist, s.duration AS length 
         FROM songs s
         JOIN artists a ON s.artist_id=a.artist_id
   ) sa 
   ON se.song=sa.song AND se.artist=sa.artist AND se.length=sa.length; 
   """
)



count_staging_rows = "SELECT COUNT(*) AS count FROM {}"

# QUERY LISTS
create_table_queries = [staging_events_table_create]

drop_table_queries = [staging_events_table_drop]

copy_table_queries = [staging_events_copy]

copy_staging_order = ['staging_events_table']

count_staging_queries = [count_staging_rows.format(copy_staging_order[0])]

insert_table_queries = [songplay_table_insert]

insert_table_order = ['songplays']

count_fact_dim_queries = [count_staging_rows.format(insert_table_order[0])]