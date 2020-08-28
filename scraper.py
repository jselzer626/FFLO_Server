import json
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from random import randint
from time import sleep


#goal is to update db with info including player image url for each player

fb_base_url = 'https://www.nfl.com/players/'

positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']
'''data = requests.get('https://www.fantasyfootballnerd.com/service/players/json/8qb63ck2ibj4/')
dataJson = data.json()
players = json.dumps(dataJson["Players"])
error_url = 'https://static.www.nfl.com/image/private/t_player_profile_landscape/f_auto/league/fxv8ozrp13i9st1qwok9'
print(len(players))'''

#need to have this start rankings from one and not zero
f = open("playerData.json", 'w')
rankingsDict = {}
for position in positions:
    standardData = requests.get(f"https://www.fantasyfootballnerd.com/service/weekly-rankings/json/8qb63ck2ibj4/{position}/1")
    pprData = requests.get(f"https://www.fantasyfootballnerd.com/service/weekly-rankings/json/8qb63ck2ibj4/{position}/1/1")
    standardDataJson = standardData.json()
    pprDataJson = pprData.json()
    standardRankings = standardDataJson['Rankings']
    pprRankings = pprDataJson['Rankings']
    for rank, ranking in enumerate(standardRankings):
        rankingsDict.update({ranking['playerId']: [{'standardRanking': rank+1}]})
    for rank, ranking in enumerate(pprRankings):
        if rankingsDict[ranking['playerId']]:
            rankingsDict[ranking['playerId']].append({'pprRanking': rank+1})
        else:
            rankingsDict.update({ranking.playerId: [{'pprRanking': rank+1}]})

f.write(json.dumps(rankingsDict))
    

f.close()

'''testPlayerSet = [{'displayName': player['displayName']} for player in players[:5]]
# testPlayerSearchable = testPlayer.replace(" ", "-")


for player in testPlayerSet:
    searchableName = player.displayName.replace(" ", "-")
    driver = webdriver.Chrome(executable_path=r'C:/webdrivers/chromedriver.exe')
    driver.get(f"{fb_base_url}/{searchableName}")
    sleep(randint(10,20))
    content = driver.page_source
    soup=BeautifulSoup(content)
    try:
        tag = soup.find('img', attrs={'alt': player.displayName, 'class': 'img-responsive'})
        src = tag.attrs['src']
    except Exception:
        src = error_url
    driver.close()
    player.update({'ranking': 999, 'imageUrl': src})
    
print(testPlayerSet)'''
