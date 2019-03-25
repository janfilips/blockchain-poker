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

from game.models import Players, Decks, Wins, Jackpot


def home(request):

    try:
        player_session_key = request.COOKIES["player_session_key"]
    except:
        player_session_key = uuid.uuid4()

    player, created = Players.objects.get_or_create(session_key=player_session_key)
    print('player', player, 'is_new', created)

    cards_deck = deck()

    # hand = []
    # card1 = card('2','S')
    # card2 = card('4','S')
    # card3 = card('J','S')
    # card4 = card('6','S')
    # card5 = card('2','D')
    # hand.insert(0, card1)
    # hand.insert(0, card2)
    # hand.insert(0, card3)
    # hand.insert(0, card4)
    # hand.insert(0, card5)

    hand = deck().get_hand()
    evaluated_hand, numeral_dict, suit_dict = deck().evaluate_hand(hand)
    sugested_hand = deck().suggest_hand(player, hand, evaluated_hand, numeral_dict, suit_dict)

    # XXX TODO jackpot sa navysuje z kazdej prehranej hry
    # XXX TODO zistit ako presne funguje jackpot na mega moolah

    player_cards_deck = Decks.objects.create(player=player, deck=cards_deck)
    print('deck', player_cards_deck)

    ###################################
    # XXX temporarily simulating credit
    if(player.credit == 0):
        player.credit = 101
        player.save()
    player.credit -= 1
    player.save()
    ###################################

    response = render(
        request=request,
        template_name='index.html',
        context={
            'player_session_key': player_session_key,
            'deck': cards_deck,
            'hand': hand,
            'evaluated_hand': evaluated_hand,
            'sugested_hand': sugested_hand,
            'numeral_dict': numeral_dict,
            'suit_dict':suit_dict,
            'credit': player.credit,
            'mini_bonus': player.mini_bonus,
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

def deck(request, deck_id):
    return HttpResponse("working on this currently", deck_id)
