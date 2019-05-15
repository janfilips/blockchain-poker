__version__ = "v0.1"

import os
import sys
import web3
import django
import datetime
import random
import time
import json
import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")
django.setup()

from game.models import Players, TopUps, Ticker
from django.conf import settings

from web3 import Web3, Account
from web3.providers.rpc import HTTPProvider

w3 = Web3(HTTPProvider(settings.ETHEREUM_PROVIDER))

import logging
logger = logging.getLogger(__name__)

TICKER_ADDRESS = "https://api.coinmarketcap.com/v1/ticker/"


def update_ticker(currency):

    ticker_address = TICKER_ADDRESS + currency + "/"
    resp = requests.get(ticker_address)
    price_usd = resp.json()[0]['price_usd']

    ticker, created = Ticker.objects.get_or_create(currency=currency)
    ticker.price = price_usd
    ticker.updated = datetime.datetime.now()
    ticker.save()

    return price_usd


def wait_for_tx_receipt(w3, tx_hash, poll_interval):

    while True:
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        if tx_receipt:
            return tx_receipt
        print(tx_hash.hex(),'is processing..')
        time.sleep(poll_interval)

    print('Obtained transaction receipt', tx_receipt)
    return tx_receipt


if __name__ == '__main__':

    print('TOPUP CREDITS ROBOT', __version__)

    print('Updating price ticker..')

    update_ticker('ethereum')

    if(settings.DEBUG):
        ETHEREUM_NETWORK = 'Testnet'
        ROBOT_WALLET = settings.ETHEREUM_TEST_WALLET
    else:
        ETHEREUM_NETWORK = 'Mainnet'.upper()
        ROBOT_WALLET = settings.ETHEREUM_MASTER_WALLET

    print('Ethereum network:', ETHEREUM_NETWORK)
    print('Contract', settings.ETHEREUM_CONTRACT_ADDRESS)

    print('Loading robot wallet...')
    # load player wallet
    with open(ROBOT_WALLET) as json_file:
        wallet_json = json.load(json_file)

    wallet_secret = wallet_json['secret']

    # decrypt account
    account_key = Account.decrypt(wallet_json, wallet_secret)
    account = Account.privateKeyToAccount(account_key)
    w3.eth.defaultAccount = account.address
    print('Player account succesfully decrypted.')
    print('Robot wallet', w3.eth.defaultAccount)
    player_balance = w3.eth.getBalance(account=account.address)
    print('Player wallet balanace eth-' + str(w3.fromWei(player_balance,'ether')),'ether')

    # initiating ethereum contract
    contract_instance = w3.eth.contract(
        address=w3.toChecksumAddress(settings.ETHEREUM_CONTRACT_ADDRESS),
        abi=settings.ETHEREUM_CONTRACT_ABI,
    )
    # setting up gas limit
    GAS_LIMIT = settings.ETHEREUM_GAS_LIMIT
    GAS_PRICE = settings.ETHEREUM_GAS_PRICE

    print('Contract instance initiated.')


    while True:

        # Updating the currency price ticker....

        ticker = Ticker.objects.get(currency="ethereum")
        ticker_delta = (datetime.datetime.now()-ticker.updated.replace(tzinfo=None)).total_seconds()
        print('Updating ticker in',60-ticker_delta,'seconds..')

        if(ticker_delta > 60):

            print('Updating ethereum price ticker...')
            price_usd = update_ticker("ethereum")
            print('Current ethereum price is $'+str(price_usd))

        print('-'*100)


        # Processing topup requests..

        topups = TopUps.objects.filter(credited=False,denied=False)

        if topups:

            for topup in topups:

                topup_delta_seconds = (datetime.datetime.now()-topup.last_check.replace(tzinfo=None)).total_seconds()

                print('topup request', topup.pk)
                print('eth_wallet', topup.eth_wallet)
                print('requested_amount_in_dollars', topup.requested_amount_in_dollars)
                print('payment_id', topup.payment_id)
                print('created', topup.created)
                print('delta_seconds', topup_delta_seconds)

                expected_paid_amount_minimum = topup.requested_amount_in_dollars / ticker.price / 100 * 90

                if(topup.paid_in_eth < expected_paid_amount_minimum):
                    topup.denied = True
                    topup.denied_message = "hackers attempt"
                    topup.save()

                if(topup_delta_seconds<10):
                    print('** topup request, last checked performed recently, skipping....')
                    continue

                if(topup.verification_attempts > 100):
                    print('***** topup request has too many verification requests, skipping....')
                    continue


                payment_id = w3.toBytes(hexstr=topup.payment_id)
                result = contract_instance.functions.verifyPayment(payment_id).call()      
                topup.last_check = datetime.datetime.now()
                topup.save()


                if(result==True):

                    topup.verified = True
                    topup.save()
                    topup.player.credit += topup.requested_amount_in_dollars
                    topup.player.save()
                    topup.credited = True
                    topup.save()

                    if(topup.requested_amount_in_dollars==20):
                        topup.player.credit += 2
                        topup.player.save()

                    if(topup.requested_amount_in_dollars==50):
                        topup.player.credit += 3
                        topup.player.save()

                    if(topup.requested_amount_in_dollars==100):
                        topup.player.credit += 10
                        topup.player.save()
                    

                    print('player was succesfuly credited..')


                # XXX check that minimum 10 seconds have passed

                topup.verification_attempts += 1
                topup.save()

            print('-'*100)


        # XXX TODO robot to populate progressive jackpot stats...

        # XXX TODO remember to consider bonus on crediting users..

        print('Waiting for the new credits requests on the queue...')
        print('Sleeping 1 second..')
        time.sleep(1)
