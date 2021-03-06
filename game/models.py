import os

from django.conf import settings
from django.db import models

class Players(models.Model):
    session_key = models.CharField(max_length=128)
    eth_wallet = models.CharField(max_length=128, default="")
    bet_amount = models.IntegerField(default=1)
    future_swap_bet_amount = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    autoplay = models.BooleanField(default=False)
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
    drawn_cards = models.CharField(max_length=64,blank=True)
    shuffled_at = models.DateTimeField(auto_now=True)
    game_finalized = models.BooleanField(default=False)
    fake_bet = models.BooleanField(default=False)

class Jackpot(models.Model):
    super_jackpot = models.FloatField(default=0)
    mega_jackpot = models.FloatField(default=0)
    major_jackpot = models.FloatField(default=0)
    minor_jackpot = models.FloatField(default=0)

class TopUps(models.Model):
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    eth_wallet = models.CharField(max_length=128)
    requested_amount_in_dollars = models.IntegerField()
    paid_in_eth = models.FloatField()
    payment_id = models.CharField(max_length=128)
    tx_id = models.CharField(max_length=128)
    verification_attempts = models.IntegerField(default=0)
    credited = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    denied = models.BooleanField(default=False)
    denied_message = models.CharField(max_length=1024)
    last_check = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)

class Payouts(models.Model):
    player = models.ForeignKey(Players, on_delete=models.CASCADE)
    requested_usd = models.FloatField()
    calculated_eth = models.FloatField(default=0)
    paid = models.BooleanField(default=False)
    failed_payment = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)

class Ticker(models.Model):
    currency = models.CharField(max_length=10)
    price = models.FloatField(default=0)
    updated = models.DateTimeField(auto_now=True)
