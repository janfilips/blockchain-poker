__version__ = "v0.1"

import os
import sys
import web3
import django
import datetime
import random
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")
django.setup()

from game.models import Players, TopUps


if __name__ == '__main__':

    print('TOPUP CREDITS ROBOT', __version__)

    while True:

        # player = models.ForeignKey(Players, on_delete=models.CASCADE)
        # eth_wallet = models.CharField(max_length=128)
        # credit_amount = models.IntegerField()
        # payment_id = models.CharField(max_length=64)
        # paid_and_verified = models.BooleanField(default=False)
        # was_credited = models.BooleanField(default=False)

        print('waiting for the new credits requests on the queue...')
        print('sleeping 1 second..')
        time.sleep(1)
