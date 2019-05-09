#!/usr/bin/env python3
import collections
import itertools
import random
import string
import time

import os
import django

from utils.evalcards import card, deck

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")
django.setup()

from game.models import Players, Decks

from random import randint, choice


def clear_first_hand(hand, deck):
    return "XXX TODO"

def clear_final_hand(hand, deck):
    # XXX TODO somewhat complicated.... 
    return "XXX TODO"


if __name__ == '__main__':


    hand = []
    cards_deck = deck()

    # temp
    player = Players.objects.get(pk=1)
    #print('player.credit', player.credit, 'player.bet_amount', player.bet_amount, )

    if(player.credit >= player.bet_amount):


        while True:

            hand = cards_deck.get_hand()
            evaluated_hand, numeral_dict, suit_dict = cards_deck.evaluate_hand(hand)

            if(evaluated_hand == "Nothing."):
                break

            if(random.randint(0,4) == 0 and evaluated_hand == "One-pair."):
                break

            if(random.randint(0,5) == 0 and evaluated_hand == "Jacks-or-better."):
                break

            if(random.randint(0,6) == 0 and evaluated_hand == "Two-pair."):
                break


        print('hand', hand, 'evaluated_hand', evaluated_hand)

        sugested_hand = cards_deck.suggest_hand(player, hand, evaluated_hand, numeral_dict, suit_dict)

        deck_hash = (''.join([choice(string.ascii_letters + string.digits) for i in range(25)]) + \
                            ''.join([choice(string.digits) for i in range(10)])).upper()

        cards_deck_ = ""
        for card in cards_deck:
            cards_deck_ += str(card) + "|"
        cards_deck = cards_deck_[:-1]

        #player_cards_deck = Decks.objects.create(player=player, bet_amount=player.bet_amount, deck=cards_deck, deck_hash=deck_hash)
        #player.credit -= player.bet_amount
        #player.save()
