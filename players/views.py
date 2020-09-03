import os
from django.shortcuts import render
from django.http import JsonResponse
from .models import Player, Roster, Owner
from twilio.rest import Client
from random import randint


client = Client(os.environ.get("ACCOUNT_SID"), os.environ.get("AUTH_TOKEN"))
origin_number = '+12057829884'

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


def generateCode(request):

    destinationNumber = request.POST['number']
    # check if number has already been verified
    responseText = ''
    try:
        Owner.objects.get(number=destinationNumber)
        responseText="verified"
    except Exception:
        # this is a token sent to the user to configure message receipt
        code = randint(100000, 999999)
        newNumber = Owner(number=destinationNumber, verify=code)
        newNumber.save()

        responseText = "send success"
        try:
            numberVerification = client.messages.create(
                body=f"Your code for Lineup Reminder is {code}",
                from_=origin_number,
                to=f"+1{destinationNumber}"
            )
        except Exception:
            responseText = "error"

    response = JsonResponse(responseText, safe=False)
    response["Access-Control-Allow-Origin"] = '*'
    return response

def verifyCode(request):

    code = request.POST['code']
    number = request.POST['number']
    responseText = ''
    try:
        if Owner.objects.get(verify=code) != Owner.objects.get(number=number):
            responseText = "verified"
    except Exception:
        responseText = "error"
    
    response=JsonResponse(verifySuccess)
    response["Access-Control-Allow-Origin"] = '*'
    return response
    