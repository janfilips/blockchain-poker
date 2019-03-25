import os

from django.conf import settings
from django.db import models

class Players(models.Model):
    address = models.CharField(max_length=128, default="")
    session_key = models.CharField(max_length=128)
    credit = models.IntegerField(default=0)
    mini_bonus = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now=True)

class Decks(models.Model):
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    deck_id = models.AutoField(primary_key=True)
    deck_hash = models.CharField(max_length=25)
    deck = models.CharField(max_length=256)
    shuffled_at = models.DateTimeField(auto_now=True)

class Wins(models.Model):
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    deck = models.ForeignKey(Decks, on_delete=models.CASCADE)
    winning_hand = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now=True)

class Jackpot(models.Model):
    super_jackpot = models.FloatField(default=0)
    mega_jackpot = models.FloatField(default=0)
    major_jackpot = models.FloatField(default=0)
    minor_jackpot = models.FloatField(default=0)
