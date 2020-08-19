from django.shortcuts import render
from django.http import JsonResponse
from .models import Player, Roster

# Create your views here.
def loadInitial(request):
    fullPlayerSet = [
        {'id': player.playerId, 'displayName': player.displayName, 'team': player.team, 'position': player.position,
        'profileImg': player.profileImg}
        for player in Player.objects.all()]
    
    response = JsonResponse(fullPlayerSet, safe=False)
    #CORS
    response["Access-Control-Allow-Origin"] = '*'
    return response