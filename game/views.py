# -*- coding: utf-8 -*-
import os
import django
import uuid
import string
import json
import ast

from datetime import datetime, timedelta

from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")
django.setup()

import logging
logger = logging.getLogger(__name__)

from utils.evalcards import card, deck

from game.models import Players, Decks, Jackpot
from random import randint, choice





def tmp_about_desired_look(request):

    response = render(
        request=request,
        template_name='tmp_about_desired_look.html',
    )

    return response

def tmp_add_credit(request):

    player_session_key = request.COOKIES["player_session_key"]
    player, created = Players.objects.get_or_create(session_key=player_session_key)
    player.credit += 10
    player.save()

    return HttpResponse(player.credit)



def home(request):

    try:
        player_session_key = request.COOKIES["player_session_key"]
    except:
        player_session_key = (''.join([choice(string.ascii_letters + string.digits) for i in range(28)]))

    player, created = Players.objects.get_or_create(session_key=player_session_key)
    print('player', player, 'is_new', created)


    # try:
    #     last_draw = request.COOKIES["last_draw"]
    # except:
    #     last_draw = None

    last_draw = None


    hand = []
    evaluated_hand = None
    sugested_hand = None
    # Note: this would be an example how to work with cards individually
    # card1 = card('7','S')
    # card2 = card('7','D')
    # card3 = card('J','S')
    # card4 = card('K','S')
    # card5 = card('A','D')
    # hand.insert(0, card1)
    # hand.insert(0, card2)
    # hand.insert(0, card3)
    # hand.insert(0, card4)
    # hand.insert(0, card5)

    if(last_draw):

        # XXX BUG checkni ze ma dostatocny kredit......
        # XXX prepnutie stavky ked mas kredit 7 a stavka 10.....

        cards_deck = deck()
        starting_nonreduced_cards_deck = cards_deck.copy()

        hand = cards_deck.get_hand()
        evaluated_hand, numeral_dict, suit_dict = cards_deck.evaluate_hand(hand)
        sugested_hand = cards_deck.suggest_hand(player, hand, evaluated_hand, numeral_dict, suit_dict)

        # print('evaluated_hand debug', evaluated_hand, numeral_dict, suit_dict)
        # print('suggested_hand debug', sugested_hand)

        deck_hash = (''.join([choice(string.ascii_letters + string.digits) for i in range(25)]) + \
                            ''.join([choice(string.digits) for i in range(10)])).upper()

        starting_nonreduced_cards_deck_ = ""
        for card in starting_nonreduced_cards_deck:
            starting_nonreduced_cards_deck_ += str(card) + "|"
        starting_cards_deck = starting_nonreduced_cards_deck_[:-1]

        player_cards_deck = Decks.objects.create(player=player, bet_amount=player.bet_amount, deck=starting_cards_deck, deck_hash=deck_hash)
        print('player_cards_deck', player_cards_deck)

        player.credit -= player.bet_amount
        player.save()


    #########################################################################
    # XXX temporarily simulating credit
    # if(player.credit <= 0):
    #     player.credit = 10
    #     player.save()
    #########################################################################
    # player.credit = 10
    # player.save()


    winning_decks = Decks.objects.filter(player_wins=True).order_by('-pk')[:100]

    if(player.swap_bet_amount):
        player.bet_amount = player.swap_bet_amount
        player.swap_bet_amount = 0
        player.save()


    autoplay = "false"
    if(player.autoplay):
        autoplay = "true"

    response = render(
        request=request,
        template_name='index.html',
        context={
            'player_session_key': player_session_key,
            'autoplay': autoplay,
            'hand': hand,
            'evaluated_hand': evaluated_hand,
            'sugested_hand': sugested_hand,
            'credit': player.credit,
            'bet_amount': player.bet_amount,
            'mini_bonus': player.mini_bonus,
            'winning_decks': winning_decks,
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

    cards_deck = Decks.objects.get(deck_hash=deck_hash)
    cards_deck_split = cards_deck.deck
    cards_deck_split = cards_deck_split.split('|')

    starting_hand = []
    for i in range(0,5):
        starting_hand.append(cards_deck_split[i])

    swapped_cards = ast.literal_eval(cards_deck.swapped_cards)

    response = render(
        request=request,
        template_name='deck.html',
        context={
            'deck_hash': deck_hash,
            'starting_hand': starting_hand,
            'swapped_cards': swapped_cards,
            'cards_deck': cards_deck,
            'cards_deck_split': cards_deck_split,
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


def ajax_deal_cards(request):

    player_session_key = request.POST['player_session_key']
    player = Players.objects.get(session_key=player_session_key)

    print('player', player)

    hand = []
    cards_deck = deck()
    starting_nonreduced_cards_deck = cards_deck.copy()

    if(player.credit >= player.bet_amount):

        hand = cards_deck.get_hand()
        evaluated_hand, numeral_dict, suit_dict = cards_deck.evaluate_hand(hand)
        sugested_hand = cards_deck.suggest_hand(player, hand, evaluated_hand, numeral_dict, suit_dict)

        # print('evaluated_hand debug', evaluated_hand, numeral_dict, suit_dict)
        # print('suggested_hand debug', sugested_hand)

        deck_hash = (''.join([choice(string.ascii_letters + string.digits) for i in range(25)]) + \
                            ''.join([choice(string.digits) for i in range(10)])).upper()

        starting_nonreduced_cards_deck_ = ""
        for card in starting_nonreduced_cards_deck:
            starting_nonreduced_cards_deck_ += str(card) + "|"
        starting_cards_deck = starting_nonreduced_cards_deck_[:-1]

        player_cards_deck = Decks.objects.create(player=player, bet_amount=player.bet_amount, deck=starting_cards_deck, deck_hash=deck_hash)
        print('player_cards_deck', player_cards_deck)

        player.credit -= player.bet_amount
        player.save()

    else:

        hand = []
        evaluated_hand = ""
        sugested_hand = ""


    if(hand):
        decoupled_hand = []
        for card in hand:
            decoupled_hand.append(str(card))
        hand = decoupled_hand

    if(sugested_hand):
        decoupled_hand = []
        for card in sugested_hand:
            decoupled_hand.append(str(card))
        sugested_hand = decoupled_hand

    response = {
            'hand': hand,
            'evaluated_hand': evaluated_hand,
            'sugested_hand': sugested_hand,
    }

    return HttpResponse(json.dumps(response))


def ajax_bet(request):

    bet_amount = request.POST['bet_amount']
    player_session_key = request.POST['player_session_key']

    player = Players.objects.get(session_key=player_session_key)

    deck = Decks.objects.filter(player=player).order_by("-pk")

    if(deck):

        deck = deck[0]
        if(deck.game_finalized):
            player.bet_amount = int(bet_amount)
        else:
            player.swap_bet_amount = int(bet_amount)
        player.save()

    if(not deck):

        player.bet_amount = int(bet_amount)
        player.save()


    print('player', player, 'changed bet_amount', bet_amount)

    return HttpResponse(bet_amount)


def ajax_autoplay(request):

    print('autoplay POST', request.POST)

    autoplay = request.POST['autoplay']
    player_session_key = request.POST['player_session_key']

    player = Players.objects.get(session_key=player_session_key)

    if(autoplay=="true"):
        player.autoplay = True
    else:
        player.autoplay = False

    player.save()

    return HttpResponse(player.autoplay)


def ajax_draw_cards(request):

    hold_cards = request.POST.getlist('cardData[]')
    print('hold_cards', hold_cards)

    player_session_key = request.POST['player_session_key']
    player = Players.objects.get(session_key=player_session_key)

    player_deck_obj = Decks.objects.filter(player=player).order_by("-pk")[0]
    player_deck = player_deck_obj.deck.split('|')

    if(player_deck_obj.game_finalized):
        # XXX toto log this type of activity
        print('*** WARNING ATTEMPT TO ACCESS FINALIZED GAME *** ' * 100)
        return HttpResponse("Sorry this game was already finalized.")

    swapped_cards = []

    final_hand_ = []
    for i in range(0,5):
        if(hold_cards[i]):
            final_hand_.append(player_deck[i])
        if(hold_cards[i]==""):
            final_hand_.append(player_deck[i+5])
            swapped_cards.append(player_deck[i])

    player_deck_obj.swapped_cards = swapped_cards
    player_deck_obj.swapped_cards_count = len(swapped_cards)
    player_deck_obj.save()

    final_hand = []
    for c_ in final_hand_:
        if(len(c_)==2):
            c = card(c_[0],c_[1])
        if(len(c_)==3):
            c = card(c_[0:2],c_[2])
        final_hand.insert(0, c)

    evaluated_hand, numeral_dict, suit_dict = deck().evaluate_hand(final_hand)

    final_hand_ = final_hand
    final_hand = []

    for c in final_hand_:
        final_hand.append(str(c))

    final_hand.reverse()

    print('final_hand', final_hand)


    win_amount = 0

    row_selector = 0

    if(evaluated_hand=="Jacks-or-better."):
        row_selector = 9
        win_amount = player.bet_amount

    if(evaluated_hand=="Two-pair."):
        row_selector = 8
        win_amount = player.bet_amount * 2

    if(evaluated_hand=="Three-of-a-kind."):
        row_selector = 7
        win_amount = player.bet_amount * 3

    if(evaluated_hand=="Full-house."):
        row_selector = 4
        win_amount = player.bet_amount * 9

    if(evaluated_hand=="Four-of-a-kind."):
        row_selector = 3
        win_amount = player.bet_amount * 25

    if(evaluated_hand=="Straight."):
        row_selector = 6
        win_amount = player.bet_amount * 4

    if(evaluated_hand=="Flush."):
        row_selector = 5
        win_amount = player.bet_amount * 6

    if(evaluated_hand=="Straight-flush."):
        row_selector = 2
        win_amount = player.bet_amount * 50

    if(evaluated_hand=="Royal-flush."):
        row_selector = 1
        if(player.bet_amount == 1):
            win_amount = 250
        if(player.bet_amount == 2):
            win_amount = 500
        if(player.bet_amount == 3):
            win_amount = 750
        if(player.bet_amount == 5):
            win_amount = 1500
        if(player.bet_amount == 10):
            win_amount = 5000

    player.credit = player.credit + win_amount
    player.save()

    # print('win amount', win_amount)
    # print('player credit', player.credit)


    congrats_you_won_flag = False

    if(evaluated_hand!="Nothing." and evaluated_hand!="One-pair."):

        congrats_you_won_flag = True

        winning_hand_extrapolated = ""
        for c_ in final_hand:
            winning_hand_extrapolated += c_ + "|"

        winning_hand_extrapolated = winning_hand_extrapolated[:-1]

        player_deck_obj.winning_hand_extrapolated = winning_hand_extrapolated
        player_deck_obj.player_wins = True
        player_deck_obj.bet_amount = player.bet_amount
        player_deck_obj.win_amount = win_amount
        player_deck_obj.winning_hand = final_hand
        player_deck_obj.winning_hand_result = evaluated_hand.replace('-',' ')
        player_deck_obj.save()

    player_deck_obj.game_finalized = True
    player_deck_obj.save()

    if(congrats_you_won_flag):
        congrats_you_won_flag = "true"
    else:
        congrats_you_won_flag = "false"

    response = render(
        request=request,
        template_name='ajax_cards.html',
        context={
            'credit': player.credit,
            'final_hand': str(final_hand).replace("'",'"'),
            'evaluated_hand': evaluated_hand,
            'congrats_you_won_flag': congrats_you_won_flag,
            'win_amount': win_amount,
            'row_selector': row_selector,
            },
    )
    response.set_cookie(key="last_draw", value=datetime.now(), max_age=300)
    return response


def ajax_jackpot_stats(request):

    # XXX TODO this needs to be fed / pulled form the DB
    super_jackpot = randint(1000000,2000000)
    mega_jackpot = randint(200000,500000)
    major_jackpot = randint(100000,200000)
    minor_jackpot = randint(10000,20000)

    response = {
        'super': super_jackpot,
        'mega': mega_jackpot,
        'major': major_jackpot,
        'minor': minor_jackpot,
    }

    return JsonResponse(response)
