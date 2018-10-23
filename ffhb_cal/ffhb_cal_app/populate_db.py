
# -*- coding: utf-8 -*-
'''
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import requests
import os, os.path, csv

from icalendar import Calendar, Event

from django.conf import settings

import ftplib

DICT_URL_FFHB = {
    'ffhb_welcome_page : http://www.ff-handball.org/competitions.html',
    ''
}

def getDatasWelcomePageFF(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find('table', attrs={'class':'classement'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    calendar = []

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        calendar.append([ele for ele in cols])

    return calendar

def saveIntoDb():

    # championnats = getAllChampionnats()
    # championnats = saveAllChampionnats(championnats)
    #
    #
'''
