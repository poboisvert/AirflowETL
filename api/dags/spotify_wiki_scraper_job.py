#!/bin/python
import json
import string
import requests
from bs4 import BeautifulSoup
import re
import datetime

def get_track_details(artist = "2Pac", track = "California Love"):
    # Get year
    try:
        r = requests.get('https://musicbrainz.org/search?query={}+{}&type=release&method=indexed'.format(artist, track).replace(' ', '+'))
        soup = BeautifulSoup(r.content, 'lxml')
        yearHTML = soup.find_all('span', 'release-date')[0] # Select first result

        year = re.findall(r'[0-9]+', str(yearHTML))

        print(year)

    except AttributeError:
        year = 'Year Not Found'

    # Get genre
    try:
        w = requests.get('https://en.wikipedia.org/wiki/{}'.format(artist).replace(' ', '_'))
        soupW = BeautifulSoup(w.content, 'lxml')

        bdayHTML = soupW.find_all('span', class_='bday')
        year = re.findall(r'(\d{4})[-](\d{2})[-](\d{2})', str(bdayHTML))
        print(year)

        return 1
    except:
        return 'Bday Not Found'


get_track_details()
