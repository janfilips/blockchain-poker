import os
import random
import datetime
import json

from django import template
from django.conf import settings
from django.utils import timezone

register = template.Library()

from game.models import Players

@register.filter(name='dict_get')
def dict_get(h, key):
    try:
        return h[key]
    except:
        return None

@register.filter(name="random_int")
def random_int(a, b=None):
    if b is None:
        a, b = 0, a
    return random.randint(a, b)

@register.filter(name="extrapolate_hand")
def extrapolate_hand(hand):
    return hand.split('|')


@register.filter(name="payout_with_bonus")
def payout_with_bonus(player_session_key):
    player = Players.objects.get(session_key=player_session_key)
    return player.credit + player.mini_bonus

