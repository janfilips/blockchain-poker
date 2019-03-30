# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")
django.setup()

import logging
logger = logging.getLogger(__name__)

from utils.evalcards import card, deck

from game.models import Players, Wins
from random import choice

if __name__ == '__main__':
    
    players = Players.objects.all()

    print('\nJacks or Better poker report\n')
    print(len(players),'players in total played the game\n')

    for player in players:
        print(player)

