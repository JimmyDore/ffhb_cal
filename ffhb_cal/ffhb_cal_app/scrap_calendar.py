# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

import requests
import os, os.path, csv

from icalendar import Calendar, Event

from django.conf import settings

import ftplib

def getDatas(url):
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

def getICS(calendar_hbcn):
    """ 
    """
    def getStartEndDate(date):
        """
            Possible date format input :
            11/11/2018 – 18h00
            21-22/11/2018
            20/12/2018
            #TODO : REFACTO THIS PART, it's not really beautiful(soup)
        """
        date_v2 = date.split('–')
        if len(date_v2) >= 2: #Date type : 11/11/2018 – 18h00
            date_v3 = date_v2[0].split('/')
            date_v4 = date_v2[1].split('h')
            #if['20', '10', '2018 '] == date_v3:
            #    import ipdb; ipdb.set_trace()
            start_date = datetime(int(date_v3[2]),int(date_v3[1]),int(date_v3[0]),int(date_v4[0].replace("\xc2\xa0", "")),int(date_v4[1]),0)
            end_date = start_date + timedelta(hours=1.5)
        else:
            date_v2 = date.split('-')
            if len(date_v2) >= 2: #Date type : 21-22/11/2018                    
                date_v3 = date_v2[1].split('/')
                start_date = datetime(int(date_v3[2]),int(date_v3[1]),int(date_v3[0])-1,0,0,1)
                end_date = start_date + timedelta(hours=23)
            else: #Date type : 20/12/2018
                date_v3 = date_v2[0].split('/')
                start_date = datetime(int(date_v3[2]),int(date_v3[1]),int(date_v3[0]),0,0,1)
                end_date = start_date + timedelta(hours=23)

        return start_date,end_date

    cal = Calendar()

    for game in calendar_hbcn:
        """ 
        Structure de la table
        <th class="classement-journee">Journée</th>
        <th class="classement-date">Date</th>
        <th class="classement-equipe-domicile">Équipe à domicile</th>
        <td class="classement-separateur" style="text-align: center;"> &#8211;</td>
        <th class="classement-equipe-exterieur">Équipe extérieur</th>
        <th class="classement-competition">Compétition</th>
        <th class="classement-tele">Passage télé</th>
        """
        event = Event()
        
        #--Title event
        summary = 'D1 Hand : ' + game[2] + '-' + game[4]
        event.add('summary', summary)

        #--Dates event
        start_date, end_date = getStartEndDate(game[1])
        event.add('dtstart', start_date)
        event.add('dtend', end_date)

        #Description event
        description = summary + '\n' + game[0] + '\n' + game[5] + '\n'
        if len(game[3]) > 0:
            description += "Score du match : game[3]"

        event.add('description', description)

        #--Location event
        #event.add('location', location)

        cal.add_component(event)

    f = open('hbcn_calendar.ics', 'wb')
    f.write(cal.to_ical())
    f.close()

def sendFileToFTPServer():
    session = ftplib.FTP(settings.HOST_FTP,settings.USERNAME_FTP,settings.PASSWORD_FTP)
    session.cwd('/ics_ffhb')
    file = open('hbcn_calendar.ics','rb')                  # file to send
    session.storbinary('STOR hbcn_calendar.ics', file)     # send the file
    file.close()                                                    # close file and FTP
    session.quit()

def generateICS(url):
    datas_calendar = getDatas(url)
    getICS(datas_calendar)
    sendFileToFTPServer()

    return True
