import os

from django.conf import settings
from django.db import models

class Players(models.Model):
    address = models.CharField(max_length=128, default="")
    session_key = models.CharField(max_length=128)
    credit = models.IntegerField(default=0)
    mini_bonus = models.FloatField(default=0)

class Decks(models.Model):
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    deck_id = models.AutoField(primary_key=True)
    deck = models.CharField(max_length=1024)

class Wins(models.Model):
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    deck = models.ForeignKey(Decks, on_delete=models.CASCADE)
    winning_hand = models.CharField(max_length=64)
