from django.db import models
from django.conf import settings

# Create your models here.
class Owner(models.Model):
    number=models.CharField(max_length=10)
    verify=models.CharField(max_length=7)

    def __str__(self):
        return f"{self.number}"

class Player(models.Model):
    fname=models.CharField(max_length=20)
    lname=models.CharField(max_length=20)
    displayName=models.CharField(max_length=40)
    position=models.CharField(max_length=3)
    team=models.CharField(max_length=3)
    pprRanking=models.IntegerField(default=999)
    standardRanking=models.IntegerField(default=999)
    profileImg=models.CharField(max_length=150)
    playerId=models.IntegerField(default=999)

    def __str__(self):
        return f"{self.displayName} {self.position} {self.team}"

class Roster(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    owner=models.ForeignKey(Owner, on_delete=models.CASCADE)
    players=models.ManyToManyField(Player, blank=True)
    parameters=models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.owner} - {self.name}"