import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events_table"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs_table"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"



ARN             = config.get('IAM_ROLE', 'ARN')
LOG_DATA        = config.get('S3', 'LOG_DATA')
LOG_JSONPATH    = config.get('S3', 'LOG_JSONPATH')
SONG_DATA       = config.get('S3', 'SONG_DATA')

# CREATE TABLES

staging_events_table_create= (
   """
   CREATE TABLE staging_events_table (
      stagingEventId bigint IDENTITY(0,1) PRIMARY KEY,
      artist VARCHAR(500),
      auth VARCHAR(20),
      firstName VARCHAR(500),
      gender CHAR(1),
      itemInSession SMALLINT,
      lastName VARCHAR(500),
      length NUMERIC,
      level VARCHAR(10),
      location VARCHAR(500),
      method VARCHAR(20),
      page VARCHAR(500),
      registration NUMERIC,
      sessionId SMALLINT,
      song VARCHAR,
      status SMALLINT,
      ts BIGINT,
      userAgent VARCHAR(500),
      userId SMALLINT
    )
   """
)

# STAGING TABLES

staging_events_copy = (
   """
   copy staging_events_table (
      artist, auth, firstName, gender,itemInSession, lastName, 
      length, level, location, method, page, registration, 
      sessionId, song, status, ts, userAgent, userId
   )
   from {}
   iam_role {}
   json {} region 'us-west-2';
   """
).format(config['S3']['log_data'], config['IAM_ROLE']['arn'], config['S3']['log_jsonpath'])


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
