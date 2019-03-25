# -*- coding: utf-8 -*-
import os
import django
import uuid
import string
import pickle

from datetime import timedelta

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")
django.setup()

import logging
logger = logging.getLogger(__name__)

from utils.evalcards import deck, card

from game.models import Players, Decks, Wins, Jackpot
from random import choice

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

    deck_hash = (''.join([choice(string.ascii_letters + string.digits) for i in range(15)]) + \
                        ''.join([choice(string.digits) for i in range(10)])).upper()

    cards_deck_ = []
    for card in cards_deck:
        cards_deck_.append(card)

    cards_deck_pickled = pickle.dumps(cards_deck_)
    player_cards_deck = Decks.objects.create(player=player, deck=cards_deck_pickled, deck_hash=deck_hash)


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

def reveal_deck(request, deck_hash):


    try:
        player_session_key = request.COOKIES["player_session_key"]
    except:
        player_session_key = uuid.uuid4()

    # XXX TODO reveal deck really shoul reveal player deck
    # XXX TODO for now we display just the deck since we're not yet recoding wins
    #player_deck = Decks.objects.get(deck_hash=deck_hash)
    #player_wins = Wins.objects.get(deck=player_deck)

    tmp_cards_deck = Decks.objects.get(deck_hash=deck_hash)
    tmp_cards_deck = pickle.loads(tmp_cards_deck)

    response = render(
        request=request,
        template_name='deck.html',
        context={
            'deck_hash': deck_hash,
            'tmp_cards_deck': tmp_cards_deck,
            'player_session_key': player_session_key,
            },
    )
    response.set_cookie(key="player_session_key",value=player_session_key)

    return response
