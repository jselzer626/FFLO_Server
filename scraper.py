import json
from selenium import webdriver
from bs4 import BeautifulSoup
import requests


fb_base_url = 'https://www.nfl.com/players/'


data = requests.get('https://www.fantasyfootballnerd.com/service/players/json/8qb63ck2ibj4/')
dataJson = data.json()
players = dataJson["Players"]
testPlayer = players[0]['displayName']
testPlayerSearchable = testPlayer.replace(" ", "-")
print(testPlayer)

driver = webdriver.Chrome(executable_path=r'C:/webdrivers/chromedriver.exe')
driver.get(f"{fb_base_url}/{testPlayerSearchable}")
content = driver.page_source
soup=BeautifulSoup(content)
tag = soup.find('img', attrs={'alt': testPlayer, 'class': 'img-responsive'})
print(tag.attrs['src'])