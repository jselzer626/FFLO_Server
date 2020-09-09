from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
from players.models import Player
import sys
import requests
import json


positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']
FLEX = ['WR', 'TE', 'RB']


def update_rankings():

    # get weather 
    currentWeekRaw = requests.get("https://www.fantasyfootballnerd.com/service/weather/json/8qb63ck2ibj4/").json()
    currentWeekClean = currentWeekRaw['Week']

    for position in positions:
        standardData = requests.get(f"https://www.fantasyfootballnerd.com/service/weekly-rankings/json/8qb63ck2ibj4/{position}/{currentWeekClean}")
        pprData = requests.get(f"https://www.fantasyfootballnerd.com/service/weekly-rankings/json/8qb63ck2ibj4/{position}/{currentWeekClean}/1")
        standardDataJson = standardData.json()
        pprDataJson = pprData.json()
        standardRankings = standardDataJson['Rankings']
        pprRankings = pprDataJson['Rankings']
        for rank, player in enumerate(standardRankings):
            try:
                playerDB = Player.objects.get(playerId=player['playerId'])
                playerDB.standardRanking = rank+1
                playerDB.save()
            except Exception:
                pass
        for rank, player in enumerate(pprRankings):
            try:
                playerDB = Player.objects.get(playerId=player['playerId'])
                playerDB.pprRanking = rank+1
                playerDB.save()
            except Exception:
                pass

'''def send_SMS():
    
    rosters = Roster.objects.filter(verified=True)
    for roster in rosters:
        destinationNumber = roster.owner.number
        params = eval(roster.parameters)
        currentPosCount = {key:[] for key in list(params.keys())}
        playerList = [{'name': player.displayName, 'position': player.position, 'standardRanking': player.standardRanking, 'pprRanking': player.pprRanking, 'team': player.team} for player in roster.players.all()]
        rosterToSend = {'starters': [], 'bench': []}
        for player in playerList:
            count = currentPosCount'''
                

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    #test
    scheduler.add_job(update_rankings, 'interval', hours=48)
    register_events(scheduler)
    scheduler.start()