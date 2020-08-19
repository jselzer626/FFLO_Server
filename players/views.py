from django.shortcuts import render
from django.http import JsonResponse
from .models import Player, Roster, PlayerSerializer

# Create your views here.
def loadInitial(request):
    fullPlayerSet = [{'id': player.playerId, 'displayName': player.displayName, 'team': player.team, 'position': player.position}
    for player in Player.objects.all()]
    
    
    return JsonResponse(fullPlayerSet, safe=False)