
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

import datetime

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


def getSaisonPoules(url_poule_gen):
    response = requests.get(url_poule_gen)
    soup = BeautifulSoup(response.text, "lxml")

    try:
        saisons = soup.find(
            'select', attrs={
                'onchange': 'selectSaison(this);'}).find_all('option')
    except AttributeError:
        saisons = []

    cleaned_seasons = []

    if len(saisons) == 0:
        # TODO - Find Good rule for season name : if month after august, start
        # of the year, else end of the year
        now = datetime.datetime.now()
        if (now.month >= 8):
            nom_saison = str(now.year) + '-' + str(now.year + 1)
        else:
            nom_saison = str(now.year - 1) + '-' + str(now.year)
        cleaned_seasons.append(
            {'nom_saison': nom_saison, 'url_saison': url_poule_gen})
    else:
        for saison in saisons:
            nom_saison = saison.text.encode('utf-8')
            url_saison = BASE_URL + saison['value']
            cleaned_seasons.append(
                {'nom_saison': nom_saison, 'url_saison': url_saison})

    return cleaned_seasons


def getSousPoules(url_saison, nom_poule_gen):
    response = requests.get(url_saison)
    soup = BeautifulSoup(response.text, "lxml")
    poules = soup.find('select', attrs={'onchange': 'selectPhases(this);'})

    try:
        sous_poules_groupes = poules.find_all('optgroup')
    except AttributeError:
        sous_poules_groupes = []

    cleaned_poules = []

    if len(sous_poules_groupes) > 0:
        for spg in sous_poules_groupes:
            poules = spg.find_all('option')
            for poule in poules:
                poule_name = (
                    spg['label'] +
                    ' - ' +
                    poule.text).encode('utf-8')
                url_poule = BASE_URL + poule['value']
                cleaned_poules.append(
                    {'url_poule': url_poule, 'nom_poule': poule_name})
    else:
        try:
            poules = poules.find_all('option')
        except AttributeError:
            poules = []

        if len(poules) == 0:
            cleaned_poules.append(
                {'url_poule': url_saison, 'nom_poule': nom_poule_gen})
        else:
            for poule in poules:
                if poule.text.encode('utf-8') != 'Sélectionner le championnat':
                    poule_name = poule.text.encode('utf-8')
                    url_poule = BASE_URL + poule['value']
                    cleaned_poules.append(
                        {'url_poule': url_poule, 'nom_poule': poule_name})

    return cleaned_poules


def getPoules(url_poule_gen, nom_poule_gen):
    '''
    Liste de liens pour tester :
    - http://www.ff-handball.org/competitions/championnats-departementaux/85-comite-de-la-vendee.html?tx_obladygesthand_pi1%5Bcompetition_id%5D=10894&cHash=3e683ff504f9378636e6c00cebdbe3de
    - http://www.ff-handball.org/competitions/championnats-nationaux/prod2/resultats.html
    - http://www.ff-handball.org/competitions/championnats-regionaux/corse.html?tx_obladygesthand_pi1%5Bcompetition_id%5D=11795&cHash=356a7510711584e2fc2b7d7420467537
    '''
    saisons = getSaisonPoules(url_poule_gen)

    for saison in saisons:
        poules = getSousPoules(saison['url_saison'], nom_poule_gen)
        for poule in poules:
            poule['saison'] = saison['nom_saison']

    return poules


if __name__ == '__main__':
    competitions = getCompetitions()

    # TODO : Save competition in DB
    # TODO : Iterate on all competitions to get all poule gen

    #poules_gen = getPoulesGen('http://www.ff-handball.org/competitions/championnats-departementaux/85-comite-de-la-vendee.html')

    # TODO : Save poulegen in DB
    # TODO : Iterate on all competitions to get all poule gen

    # TODO : Think to replace "coucou_nom, par le nom de la poule générale"
    poules = getPoules(
        "http://www.ff-handball.org/competitions/championnats-regionaux/corse.html?tx_obladygesthand_pi1%5Bcompetition_id%5D=11795&cHash=356a7510711584e2fc2b7d7420467537",
        "coucou_nom")
    print(poules)
