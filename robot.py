__version__ = "v0.1"

import os
import sys
import web3
import django
import datetime
import random
import time
import json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "game.settings")
django.setup()

from game.models import Players, TopUps
from django.conf import settings

from web3 import Web3, Account
from web3.providers.rpc import HTTPProvider

w3 = Web3(HTTPProvider(settings.ETHEREUM_PROVIDER))

import logging
logger = logging.getLogger(__name__)



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

        # XXX TODO filter older than 10 seconds
        topups = TopUps.objects.filter(credited=False)

        if topups:

            for topup in topups:

                print('topup request', topup.pk)
                print('eth_wallet', topup.eth_wallet)
                print('requested_amount_in_dollars', topup.requested_amount_in_dollars)
                print('payment_id', topup.payment_id)
 
                payment_id = w3.toBytes(hexstr=topup.payment_id)
                result = contract_instance.functions.verifyPayment(payment_id).call()      
                print('result', result)


                if(result==True):

                    topup.verified = True
                    topup.save()
                    topup.player.credit += topup.requested_amount_in_dollars
                    topup.player.save()
                    topup.credited = True
                    topup.save()


                # XXX check that minimum 10 seconds have passed

                topup.verification_attempts += 1
                topup.save()

            print('-'*100)

        # XXX TODO robot to update price ticker...

        # XXX TODO robot to populate progressive jackpot stats...


        print('waiting for the new credits requests on the queue...')
        print('sleeping 1 second..')
        time.sleep(1)
