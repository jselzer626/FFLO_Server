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
positions = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF', 'Bench']
FLEX = ['WR', 'TE', 'RB']

#parameter is a roster object
#return will be string to send via SMS
def optimizeRoster(roster):
    rosterParameters = eval(roster.parameters)

    rankingToCheck = ""
    if rosterParameters['type'] == 'Standard':
        rankingToCheck = 'standardRanking'
    else:
        rankingToCheck = 'pprRanking'

    addedPlayers = {"RB": [], "QB": [], "WR": [], "TE": [], "FLEX": [], "K": [], "DEF": [], "Total": [], "Bench": []}
    
    playersUnsorted = [{"name": player.displayName, "position": player.position, "pprRanking": player.pprRanking, "standardRanking": player.standardRanking}
        for player in roster.players.all()]
    sortedPlayers = sorted(playersUnsorted, key = lambda player: player[rankingToCheck])
    
    for player in sortedPlayers:
        position = player['position']
        if len(addedPlayers[position]) < rosterParameters[position]:
            addedPlayers[position].append(player)
        elif len(addedPlayers['FLEX']) < rosterParameters['FLEX'] and position in FLEX:
            addedPlayers['FLEX'].append(player)
        else:
            addedPlayers['Bench'].append(player)

    finalMessage = "Based on this week's Fantasy Football Nerd rankings, here's your recommended lineup\n"
    for position in positions:
        finalMessage += f"{position}\n"
        for player in addedPlayers[position]:
            finalMessage += f"\t{player['name']}\n"
    finalMessage += "\nUpdate players here: https://jselzer626.github.io/FFLO_Client/"
    
    return finalMessage

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
            messageText =f"Thanks for adding your roster, {newRoster.name}\n"
            messageText += optimizeRoster(newRoster)
            try:
                rosterSend = client.messages.create(
                    body=messageText,
                    from_=origin_number,
                    to=f"+1{destinationNumber}"
                )
            except Exception:
                responseText = "error"
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
