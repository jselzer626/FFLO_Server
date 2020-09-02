from django.shortcuts import render
from django.http import JsonResponse
from .models import Player, Roster, Owner
from twilio.rest import Client
from random import randint

# Create your views here.
def loadInitial(request):
    fullPlayerSet = [
        {'id': player.playerId, 'displayName': player.displayName, 'team': player.team, 'position': player.position,
        'profileImg': player.profileImg, 'standardRanking': player.standardRanking, "pprRanking": player.pprRanking}
        for player in Player.objects.all()]
    
    response = JsonResponse(fullPlayerSet, safe=False)
    #CORS
    response["Access-Control-Allow-Origin"] = '*'
    return response


def GenerateCode(request):

    destinationNumber = request.POST['number']
    # this is a token sent to the user to configure message receipt
    code = randint(100000, 999999)
    newNumber = Owner(number=desintationNumber, verify=code)