from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
from players.models import Player
import sys
import requests
import json


positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']


def update_rankings():
    for position in positions:
        standardData = requests.get(f"https://www.fantasyfootballnerd.com/service/weekly-rankings/json/8qb63ck2ibj4/{position}/1")
        pprData = requests.get(f"https://www.fantasyfootballnerd.com/service/weekly-rankings/json/8qb63ck2ibj4/{position}/1/1")
        standardDataJson = standardData.json()
        pprDataJson = pprData.json()
        standardRankings = standardDataJson['Rankings']
        pprRankings = pprDataJson['Rankings']
        for rank, player in enumerate(standardRankings):
            try:
                playerDB = Player.objects.get(id=player['playerId'])
                playerDB.standardRanking = rank+1
                playerDB.save()
            except Exception:
                pass
        for rank, player in enumerate(pprRankings):
            try:
                playerDB = Player.objects.get(id=player['playerId'])
                playerDB.pprRanking = rank+1
                playerDB.save()
            except Exception:
                pass

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    #test
    scheduler.add_job(update_rankings, 'interval', hours=48)
    register_events(scheduler)
    scheduler.start()