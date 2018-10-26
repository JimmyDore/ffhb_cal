
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import requests
import os
import os.path
import csv

from icalendar import Calendar, Event

from django.conf import settings

import ftplib

BASE_URL = 'http://www.ff-handball.org/'


def getCompetitions():
    # On recup la liste des compétitions
    welcome_page = BASE_URL + "competitions.html"
    response = requests.get(welcome_page)
    soup = BeautifulSoup(response.text, "html.parser")
    liste_competitions = soup.find('ul', attrs={'class': 'compo'})
    rows = liste_competitions.find_all('li')

    competitions = []

    for row in rows:
        nom = row.find('span').text.encode('utf-8')
        if nom.decode('utf-8') != "Recherche":
            url = BASE_URL + row.find('a')['href']
            type = 'Nat'
            num_dep = '00'
            if nom.decode('utf-8') == "Championnats régionaux":
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                liste_competitions = soup.find('ul', attrs={'class': 'reg'})
                rows_regions = liste_competitions.find_all('li')
                type = 'Reg'
                for row_reg in rows_regions:
                    nom = row_reg.find('span').find(
                        'span').text.encode('utf-8')
                    url = BASE_URL + row_reg.find('a')['href']
                    competitions.append([nom, url, type, num_dep])
            elif nom.decode('utf-8') == "Championnats départementaux":
                response = requests.get(url)
                soup = BeautifulSoup(response.text, "html.parser")
                liste_competitions = soup.find('ul', attrs={'id': 'depts'})
                rows_deps = liste_competitions.find_all('li')
                type = 'Dep'
                for row_dep in rows_deps:
                    nom = row_dep.find('a').text.split(' ')[-1].encode('utf-8')
                    num_dep = row_dep.find('a').find(
                        'span').text.replace(' ', '').encode('utf-8')
                    url = BASE_URL + row_dep.find('a')['href']
                    competitions.append([nom, url, type, num_dep])
            else:
                competitions.append([nom, url, type, num_dep])
    return competitions


def getPoulesGen(url_compet):
    response = requests.get(url_compet)
    soup = BeautifulSoup(response.text, "lxml")
    liste_poules_gen = soup.find('ul', attrs={'class': 'chpts'})
    rows = liste_poules_gen.find_all('li', recursive=False)

    poules_gen = []

    for row in rows:
        nom = row.find('span').text.encode('utf-8')
        url = BASE_URL + row.find('a')['href']
        poules_gen.append([nom, url])

    return poules_gen


def getPoules(url_poule_gen):
    # TODO : Check if multiple seasons
    # TODO : Check if multiple poules in the page
    response = requests.get(url_poule_gen)
    soup = BeautifulSoup(response.text, "lxml")

    return 0


if __name__ == '__main__':
    #competitions = getCompetitions()

    # TODO : Save competition in DB
    # TODO : Iterate on all competitions to get all poule gen

    #poules_gen = getPoulesGen('http://www.ff-handball.org/competitions/championnats-departementaux/85-comite-de-la-vendee.html')

    # TODO : Save poulegen in DB
    # TODO : Iterate on all competitions to get all poule gen

    poules = getPoules("http://www.ff-handball.org/competitions/championnats-departementaux/85-comite-de-la-vendee.html?tx_obladygesthand_pi1%5Bcompetition_id%5D=10818&cHash=df38231f13f8bd62a6260775bbba8f16")
