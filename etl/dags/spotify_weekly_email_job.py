import smtplib
from email.message import EmailMessage
import re
from datetime import datetime, timedelta
import psycopg2

import configparser
from dotenv import load_dotenv
from pathlib import Path
import os
from airflow.models import Variable
from utils.logger import logger

# load_dotenv()
# env_path = Path(".") / ".env"
# load_dotenv(dotenv_path=env_path)

# GMAILEMAILFROM = os.getenv("GMAILEMAILFROM")
# GMAILPASS = os.getenv("GMAILPASS")

GMAILEMAILFROM = Variable.get("GMAILEMAILFROM")
GMAILPASS = Variable.get("GMAILPASS")


def spotify_weekly_email_function():
    #config = configparser.ConfigParser()
    #config.read("../dwh.cfg")

    conn = psycopg2.connect(
        "host={} dbname={} user={} password={} port={}".format(
            Variable.get("HOST"), Variable.get("DB_NAME"),Variable.get("DB_USER"),Variable.get("DB_PASSWORD"),Variable.get("DB_PORT")
        )
    )
    cur = conn.cursor()

    # Top 5 Songs by Time Listened (MIN)
    top_5_songs_min = []
    cur.execute("SELECT TOP 5 * FROM staging_events_table")
    for row in cur.fetchall():
        song_name = row[2]
        min_listened = row[4]
        element = [song_name, min_listened]
        top_5_songs_min.append(element)

    # print(top_5_songs_min)
    top_5_count = []
    cur.execute(
        "SELECT song_name, count(*) FROM staging_events_table GROUP BY song_name ORDER BY count DESC LIMIT 5"
    )
    for row in cur.fetchall():
        song_name = row[0]
        min_listened = row[1]
        element = [song_name, min_listened]
        top_5_count.append(element)

    print(top_5_count)

    subject = "Test subject"
    message = "This is the message"
    destination = "pob944@gmail.com"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    # This is where you would replace your password with the app password - it's your gmail account (the sender account)
    server.login(GMAILEMAILFROM, GMAILPASS)

    msg = EmailMessage()

    message = f"{message}\n"
    msg.set_content(str(top_5_count))
    msg["Subject"] = subject
    msg["From"] = GMAILEMAILFROM
    msg["To"] = destination
    server.send_message(msg)


if __name__ == "__main__":
    spotify_weekly_email_function()
