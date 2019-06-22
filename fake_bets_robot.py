import os
import django

import time
import random
import string
from random import choice

from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")
django.setup()

from game.models import Decks, Players

while True:

    random_winning_deck = Decks.objects.filter(player_wins=True).order_by("?").first()

    new_deck_hash = (''.join([choice(string.ascii_letters + string.digits) for i in range(25)]) + \
                        ''.join([choice(string.digits) for i in range(10)])).upper()

    random_player = Players.objects.order_by("?").first()

    new_fake_deck = Decks.objects.create(
        player = random_player,
        player_wins = random_winning_deck.player_wins,
        deck_hash = new_deck_hash,
        deck = random_winning_deck.deck,
        bet_amount = random_winning_deck.bet_amount * 2,
        win_amount = random_winning_deck.win_amount * 2,
        winning_hand = random_winning_deck.winning_hand,
        winning_hand_extrapolated = random_winning_deck.winning_hand_extrapolated,
        winning_hand_result = random_winning_deck.winning_hand_result,
        swapped_cards = random_winning_deck.swapped_cards,
        swapped_cards_count = random_winning_deck.swapped_cards_count,
        drawn_cards = random_winning_deck.drawn_cards,
        shuffled_at = random_winning_deck.shuffled_at,
        game_finalized = random_winning_deck.game_finalized,
    )

    print('Placed new fake bet', new_fake_deck)
    sleep_time = random.randint(200,1800)
    print('Sleeping for', sleep_time, 'seconds..')
    time.sleep(sleep_time)
