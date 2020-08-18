import json
from selenium import webdriver
from bs4 import BeautifulSoup
import requests


fb_base_url = 'https://www.nfl.com/players/'


data = requests.get('https://www.fantasyfootballnerd.com/service/players/json/8qb63ck2ibj4/')
dataJson = data.json()
players = dataJson["Players"]
duplicate_names = []
for i in range(1, len(players)):
    if players[i-1]['displayName'] == players[i]['displayName']:
        duplicate_names.append(players[i-1])
        duplicate_names.append(players[i])

print(duplicate_names)

'''testPlayer = players[0]['displayName']
testPlayerSearchable = testPlayer.replace(" ", "-")'''


'''driver = webdriver.Chrome(executable_path=r'C:/webdrivers/chromedriver.exe')
driver.get(f"{fb_base_url}/{testPlayerSearchable}")
content = driver.page_source
soup=BeautifulSoup(content)
tag = soup.find('img', attrs={'alt': testPlayer, 'class': 'img-responsive'})
print(tag.attrs['src'])'''