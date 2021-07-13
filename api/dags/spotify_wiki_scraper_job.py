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
        r = requests.get('https://musicbrainz.org/search?query={}+{}&type=release&method=indexed'.format(track.encode('utf8', 'ignore'), artist.encode('utf8', 'ignore')))
        soup = BeautifulSoup(r.content, 'lxml')
        match = soup.find_all('tr')[1]
        year = re.search("[0-9]+", str(match.find_all('td')[5])).group(0)
    except AttributeError:
        year = 'Year Not Found'

    # Get genre
    try:
        w = requests.get('https://en.wikipedia.org/wiki/{}'.format(
            wikipedia.search('{} {} {}'.format(track, artist, year))[0].replace(' ', '_')))
        soupW = BeautifulSoup(w.content, 'lxml')
        infobox = soupW.find_all('table', class_='infobox')[0]

        for row in infobox.find_all('tr'):
            if row.th:
                if 'Music genre' in str(row.th):
                    genre = row.td.get_text().strip().split('\n')[0]
                    for ch in string.punctuation:
                        genre = genre.split(ch)[0]
        print(year, genre)
        return year, genre
    except:
        return year, 'Genre Not Found'


if __name__ == '__main__':
    get_track_details("8 miles", "eminem")
