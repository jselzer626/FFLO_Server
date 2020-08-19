from django.db import models
from django.conf import settings
from rest_framework import serializers

# Create your models here.
class Roster(models.Model):
    name=models.CharField(max_length=30)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Player(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    displayName=models.CharField(max_length=40)
    position=models.CharField(max_length=3)
    team=models.CharField(max_length=3)
    roster=models.ManyToManyField(Roster, blank=True)
    pprRanking=models.IntegerField(default=999)
    standardRanking=models.IntegerField(default=999)
    profileImg=models.CharField(max_length=150)
    playerId=models.IntegerField(default=999)

    def __str__(self):
        return f"{self.displayName} {self.position} {self.team}"

class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ['displayName', 'team']