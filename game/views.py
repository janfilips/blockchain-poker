# -*- coding: utf-8 -*-
import os
import django
import uuid
import string

from datetime import timedelta

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")
django.setup()

import logging
logger = logging.getLogger(__name__)

from utils.evalcards import card, deck

from game.models import Players, Decks, Wins, Jackpot
from random import choice

def home(request):

    try:
        player_session_key = request.COOKIES["player_session_key"]
    except:
        player_session_key = (''.join([choice(string.ascii_letters + string.digits) for i in range(28)]))

    player, created = Players.objects.get_or_create(session_key=player_session_key)
    print('player', player, 'is_new', created)

    hand = []
    cards_deck = deck()
    starting_nonreduced_cards_deck = cards_deck.copy()

    # Note: this would be an example how to work with cards individually
    # card1 = card('2','S')
    # card2 = card('Q','S')
    # card3 = card('J','S')
    # card4 = card('K','S')
    # card5 = card('A','D')
    # hand.insert(0, card1)
    # hand.insert(0, card2)
    # hand.insert(0, card3)
    # hand.insert(0, card4)
    # hand.insert(0, card5)

    hand = cards_deck.get_hand()
    evaluated_hand, numeral_dict, suit_dict = cards_deck.evaluate_hand(hand)
    sugested_hand = cards_deck.suggest_hand(player, hand, evaluated_hand, numeral_dict, suit_dict)

    # XXX TODO jackpot sa navysuje z kazdej prehranej hry

    deck_hash = (''.join([choice(string.ascii_letters + string.digits) for i in range(25)]) + \
                        ''.join([choice(string.digits) for i in range(10)])).upper()

    starting_nonreduced_cards_deck_ = ""
    for card in starting_nonreduced_cards_deck:
        starting_nonreduced_cards_deck_ += str(card) + "|"
    starting_cards_deck = starting_nonreduced_cards_deck_[:-1]

    player_cards_deck = Decks.objects.create(player=player, deck=starting_cards_deck, deck_hash=deck_hash)
    print('player_cards_deck', player_cards_deck)

    #########################################################################
    # XXX temporarily simulating credit
    if(player.credit == 0):
        player.credit = 30
        player.save()
    player.credit -= 5
    player.save()
    #########################################################################

    #########################################################################
    # XXX delete this shit it's for debug purposes only #####################
    XXX_DELETEME_TEMP_ONLY_DECKS = Decks.objects.all().order_by('-pk')[:100]
    #########################################################################

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
            'DELETEME_TEMP_ONLY_DECKS': XXX_DELETEME_TEMP_ONLY_DECKS,
            },
    )
    response.set_cookie(key="player_session_key",value=player_session_key)

    return response


def about(request):

    try:
        player_session_key = request.COOKIES["player_session_key"]
    except:
        player_session_key = (''.join([choice(string.ascii_letters + string.digits) for i in range(28)]))

    player, created = Players.objects.get_or_create(session_key=player_session_key)
    print('player', player, 'is_new', created)

    response = render(
        request=request,
        template_name='about.html',
        context={
            'player_session_key': player_session_key,
            },
    )
    response.set_cookie(key="player_session_key",value=player_session_key)

    return response


def tmp_about_desired_look(request):

    response = render(
        request=request,
        template_name='tmp_about_desired_look.html',
    )

    return response


def tos(request):

    try:
        player_session_key = request.COOKIES["player_session_key"]
    except:
        player_session_key = (''.join([choice(string.ascii_letters + string.digits) for i in range(28)]))

    player, created = Players.objects.get_or_create(session_key=player_session_key)
    print('player', player, 'is_new', created)

    response = render(
        request=request,
        template_name='tos.html',
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
        player_session_key = (''.join([choice(string.ascii_letters + string.digits) for i in range(28)]))

    player, created = Players.objects.get_or_create(session_key=player_session_key)
    print('player', player, 'is_new', created)

    # XXX TODO reveal deck really shoul reveal player deck
    # XXX TODO for now we display just the deck since we're not yet recoding wins
    #player_deck = Decks.objects.get(deck_hash=deck_hash)
    #player_wins = Wins.objects.get(deck=player_deck)

    cards_deck = Decks.objects.get(deck_hash=deck_hash)
    tmp_cards_deck = cards_deck.deck
    tmp_cards_deck = tmp_cards_deck.split('|')

    response = render(
        request=request,
        template_name='deck.html',
        context={
            'deck_hash': deck_hash,
            'tmp_cards_deck': tmp_cards_deck,
            'deck_shuffled_at': cards_deck.shuffled_at,
            'player_session_key': player_session_key,
            },
    )
    response.set_cookie(key="player_session_key",value=player_session_key)

    return response

def credit(request):

    try:
        player_session_key = request.COOKIES["player_session_key"]
    except:
        player_session_key = (''.join([choice(string.ascii_letters + string.digits) for i in range(28)]))

    player, created = Players.objects.get_or_create(session_key=player_session_key)
    print('player', player, 'is_new', created)

    response = render(
        request=request,
        template_name='credit.html',
        context={
            'credit': player.credit,
            'player_session_key': player_session_key,
            },
    )
    response.set_cookie(key="player_session_key",value=player_session_key)

    return response

def ajax_bet(request):

    set_new_bet_amount = request.POST['bet_amount']
    player_session_key = request.POST['player_session_key']

    player, created = Players.objects.get_or_create(session_key=player_session_key)
    print('player', player, 'is_new', created)


    return HttpResponse(10)

def ajax_draw(request):
    # XXX this thing will receive info about which cards to hold,
    # XXX replaces the cards it's supposed to
    # XXX returns the new cards, info about the actual new credit (including the win if there is any)

    held_cards = request.POST.get('hold_cards')

    xxx_credit = "xxx"
    xxx_final_hand = "xxx"
    xxx_evaluated_hand = "xxx"
    xxx_contrats_you_won_flag = True

    response = {
        'credit': xxx_credit,
        'final_hand': xxx_final_hand,
        'evaluated_hand': xxx_evaluated_hand,
        'congrats_you_won_flag': xxx_contrats_you_won_flag,
    }

    return HttpResponse("xxx working on this currently")
    #return JsonResponse({"result": "true"})

def ajax_swap_bet_amount(request):
    return HttpResponse("xxx working on this currently")
