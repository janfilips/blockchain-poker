import os

from django.conf import settings
from django.db import models

class Players(models.Model):
    address = models.CharField(max_length=128, default="")
    session_key = models.CharField(max_length=128)
    bet_amount = models.IntegerField(default=1)
    credit = models.IntegerField(default=0)
    mini_bonus = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now=True)

class Decks(models.Model):
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    player_wins = models.BooleanField(default=False)
    deck_id = models.AutoField(primary_key=True)
    deck_hash = models.CharField(max_length=25)
    deck = models.CharField(max_length=256)
    bet_amount = models.IntegerField()
    win_amount = models.IntegerField(default=0)
    winning_hand = models.CharField(max_length=64)
    winning_hand_extrapolated = models.CharField(max_length=64)
    winning_hand_result = models.CharField(max_length=64)
    swapped_cards = models.CharField(max_length=64,blank=True)
    swapped_cards_count = models.IntegerField(default=0)
    shuffled_at = models.DateTimeField(auto_now=True)

class Jackpot(models.Model):
    super_jackpot = models.FloatField(default=0)
    mega_jackpot = models.FloatField(default=0)
    major_jackpot = models.FloatField(default=0)
    minor_jackpot = models.FloatField(default=0)

class Logs(models.Model):
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    action = models.CharField(max_length=16)
    text = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now=True)
