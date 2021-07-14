#!/bin/python
import json
import string
import requests
from bs4 import BeautifulSoup
import re
import wikipedia
import sys


def get_track_details(track, artist):
    # Get year
    try:
        r = requests.get('https://musicbrainz.org/search?query=Mockingbird+Eminem&type=release&limit=25&method=indexed')
        soup = BeautifulSoup(r.content, 'lxml')
        year = soup.find_all('span', 'release-date')[0] # Select first result
        print(year)
    except AttributeError:
        year = 'Year Not Found'

    # Get genre
    try:
        w = requests.get('https://en.wikipedia.org/wiki/Eminem')
        soupW = BeautifulSoup(w.content, 'lxml')

        bday = soupW.find_all('span', class_='bday')
        print(bday)

        return year, bday
    except:
        return bday, 'Bday Not Found'


if __name__ == '__main__':
    get_track_details("Mockingbird", "Eminem")
