import os
import json
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from .models import Player, Roster, Owner
from twilio.rest import Client
from random import randint


client = Client(os.environ.get("ACCOUNT_SID"), os.environ.get("AUTH_TOKEN"))
origin_number = '+12057829884'

# Create your views here.
def loadInitial(request):
    fullPlayerSet = [
        {'id': player.playerId, 'systemId': player.id, 'displayName': player.displayName, 'team': player.team, 'position': player.position,
        'profileImg': player.profileImg, 'standardRanking': player.standardRanking, "pprRanking": player.pprRanking}
        for player in Player.objects.all()]
    
    response = JsonResponse(fullPlayerSet, safe=False)
    #CORS
    response["Access-Control-Allow-Origin"] = '*'
    return response


def generateCode(request):

    destinationNumber = request.POST['number']
    roster = request.POST['roster']
    parameters = request.POST['parameters']
    responseText = ''

    # check if number has already been verified
    try:
        try:
            owner = Owner.objects.get(number=destinationNumber)
        except Exception:
            code = randint(100000, 999999)
            owner = Owner(number=destinationNumber, verify=code)
            owner.save()

        playersToAdd = json.loads(roster)
        if Roster.objects.filter(name=playersToAdd['name'],owner=owner):
            raise Exception
        newRoster = Roster(owner=owner, name=playersToAdd['name'], parameters=parameters)
        newRoster.save()
        for player in playersToAdd['Total']:
            playerDB = Player.objects.get(playerId = player['id'])
            newRoster.players.add(playerDB)
        
        if owner.verified:
            responseText="verified"
        else:
            responseText="send success"
            try:
                numberVerification = client.messages.create(
                    body=f"Your code for Lineup Reminder is {code}",
                    from_=origin_number,
                    to=f"+1{destinationNumber}"
                )
            except Exception:
                responseText = "error"
    except Exception:
        responseText = "error"

    response = JsonResponse(responseText, safe=False)
    response["Access-Control-Allow-Origin"] = '*'
    return response

def verifyCode(request):

    number = request.POST['number']
    code = request.POST['code']
    responseText = ''
    try:
        owner = Owner.objects.get(number=number)
        if owner == Owner.objects.get(verify=code):
            ownerToUpdate = Owner.objects.get(verify=code)
            ownerToUpdate.verified = True
            ownerToUpdate.save()
            responseText='verified'

    except Exception:
        responseText = "error"
    
    response=JsonResponse(responseText, safe=False)
    response["Access-Control-Allow-Origin"] = '*'
    return response

def getRosters(request):

    number=request.POST['number']
    response = ''
    
    try:
        owner = Owner.objects.get(number=number)
        rosters = Roster.objects.filter(owner=owner)
        data = serializers.serialize('json', rosters, fields=("name", "players", "parameters"))
        response = JsonResponse(data, safe=False)
    except Exception:
        response = JsonResponse("error", safe=False)

    response["Access-Control-Allow-Origin"] = '*'
    return response