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
from django.conf import settings

from web3 import Web3, Account
from web3.providers.rpc import HTTPProvider

w3 = Web3(HTTPProvider(settings.ETHEREUM_PROVIDER))

# XXX TODO robot to update price ticker...
# XXX TODO robot to populate progressive jackpot stats...

if __name__ == '__main__':

    print('TOPUP CREDITS ROBOT', __version__)
    print('Contract', settings.ETHEREUM_CONTRACT_ADDRESS)

    while True:

        topups = TopUps.objects.filter(was_credited=False)

        for topup in topups:

            print('topup request', topup.pk)
            print('player', topup.player)
            print('eth_wallet', topup.eth_wallet)
            print('requested_amount_in_dollars', topup.requested_amount_in_dollars)
            print('paid_in_eth', topup.paid_in_eth)
            print('payment_id', topup.payment_id)
            print('paid_and_verified', topup.paid_and_verified)
            print('was_credited', topup.was_credited)
            print('-'*100)

        print('waiting for the new credits requests on the queue...')
        print('sleeping 1 second..')
        time.sleep(1)
