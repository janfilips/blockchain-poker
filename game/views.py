# -*- coding: utf-8 -*-
import os
import django
import uuid

from datetime import timedelta

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")
django.setup()

import logging
logger = logging.getLogger(__name__)

from utils.evalcards import deck, card


def home(request):

    try:
        player_session_key = request.COOKIES["player_session_key"]
    except:
        player_session_key = uuid.uuid4()


    cards_deck = deck()

    hand = []
    card1 = card('3','D')
    card2 = card('4','D')
    card3 = card('5','D')
    card4 = card('6','D')
    card5 = card('J','H')
    hand.insert(0, card1)
    hand.insert(0, card2)
    hand.insert(0, card3)
    hand.insert(0, card4)
    hand.insert(0, card5)

    #hand = deck().get_hand()
    evaluated_hand, numeral_dict, suit_dict = deck().evaluate_hand(hand)
    sugested_hand = deck().suggest_hand(hand, evaluated_hand, numeral_dict, suit_dict)

    credit = 0

    response = render(
        request=request,
        template_name='index.html',
        context={
            'player_session_key': player_session_key,
            'deck': cards_deck,
            'hand': hand,
            'evaluated_hand': evaluated_hand,
            'numeral_dict': numeral_dict,
            'suit_dict':suit_dict,
            'credit': credit,
            'sugested_hand': sugested_hand,
            },
    )
    response.set_cookie(key="player_session_key",value=player_session_key)

    return response


def about(request):

    try:
        player_session_key = request.COOKIES["player_session_key"]
    except:
        player_session_key = uuid.uuid4()


    response = render(
        request=request,
        template_name='about.html',
        context={
            'player_session_key': player_session_key,
            },
    )
    response.set_cookie(key="player_session_key",value=player_session_key)

    return response
