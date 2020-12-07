# -*- coding: utf-8 -*-
"""
Created on Wed May  6 23:46:43 2020

@author: Andrew

This script will crawl basketball-reference.com for NBA player numbers in the 1990 to 2019 NBA seasons.
"""

from bs4 import BeautifulSoup
import pandas as pd
import urllib.request as urllib2
import re
from time import sleep
import random

URL_BASE = 'https://www.basketball-reference.com'
url = 'https://www.basketball-reference.com/leagues/'
response = urllib2.urlopen(url).read()
soup = BeautifulSoup(response, 'html.parser')
soup.prettify()

# Collect links for each season recorded on the site
seasons = soup.select('table#stats th[data-stat="season"] a')
season_urls = []
for link in seasons:
    season_urls.append(URL_BASE + link['href'])

season_urls = season_urls[:30]  # Crawling only the last 30 years

# Go through each season to access the team data and create a list
# of teams that played during the season
team_urls = []
for season in season_urls:
    sleep(random.randint(1,5))  # Don't want to get flagged for too many requests
    print(season)
    response = urllib2.urlopen(season).read()
    soup = BeautifulSoup(response, 'html.parser')
    soup.prettify()
    
    teams = soup.select('tbody th[data-stat="team_name"] a')
    for link in teams:
        temp_url = URL_BASE + link['href']
        if temp_url not in team_urls:
            team_urls.append(temp_url)

# Go through each team and grab the roster. From the roster, store the team's official
# abbreviation, the year of the season, the player's number, and the player's name.
player_nos = []    
for team_url in team_urls:
    sleep(random.randint(5,10))
    print(team_url)
    response = urllib2.urlopen(team_url).read()
    soup = BeautifulSoup(response, 'html.parser')
    soup.prettify()
    players = soup.select('table#roster tbody tr')

    teamname = re.findall(r"teams/(.+)/\d+", team_url)
    teamname = teamname[0]
    
    year = re.findall(r"\d+\.html", team_url)
    year = year[0].replace('.html','')
    year = int(year)-1
    
    for player in players:
        pnum = player.find('th', {'data-stat':'number'}).text
        pname = player.find('td', {'data-stat':'player'}).text
        
        player_nos.append([year, teamname, pnum, pname])

# Create DataFrame out of the crawled data and export
df_player_nos = pd.DataFrame(player_nos, columns=['season', 'team', 'number', 'name'])
print(df_player_nos.head())
print(df_player_nos.info())
df_player_nos.to_csv(r'C:\Users\Andrew\Desktop\player_nos.csv', index=True)
