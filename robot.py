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

from game.models import Players, TopUps, Ticker, Payouts
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

                expected_paid_amount_minimum = topup.requested_amount_in_dollars / ticker.price
                expected_paid_amount_minimum = expected_paid_amount_minimum / 100 * 90

                if(topup.paid_in_eth < expected_paid_amount_minimum):
                    topup.denied = True
                    topup.denied_message = "hackers attempt"
                    print('attempted hack '*100)
                    print('expected_paid_amount_minimum', expected_paid_amount_minimum)
                    print('topup.paid_in_eth', topup.paid_in_eth)
                    topup.save()

                if(topup_delta_seconds<10):
                    print('** topup request, last check performed recently, skipping....')
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


                topup.verification_attempts += 1
                topup.save()

            print('-'*100)


        # Processing cashout requests..

        payouts = Payouts.objects.filter(paid=False,failed_payment=False)

        for payout in payouts:

            if(payout.failed_payment):
                print('**** failed transaction, skipping for good security measure..')
                continue

            print('New payout request from', payout.player.eth_wallet)
            print('Requested $USD', payout.requested_usd)

            ticker = Ticker.objects.get(currency="ethereum")

            calculated_eth = payout.requested_usd / ticker.price
            payout.calculated_eth = calculated_eth
            payout.save()

            print('Calculated ETH', calculated_eth)        
            print('Player wallet', payout.player.eth_wallet)    

            print('Sending money...')

            player_wallet = w3.toChecksumAddress(payout.player.eth_wallet)
            calculated_eth_in_wei = w3.toWei(calculated_eth,'ether')

            # result = contract_instance.functions.cashOut(player_wallet,calculated_eth_in_wei).call()
            # print('Result', result)

            transaction = contract_instance.functions.cashOut(player_wallet,calculated_eth_in_wei).buildTransaction({'gas':GAS_LIMIT,})
            # constructing rollDice transaction    
            transaction['gas'] = GAS_LIMIT
            transaction['gasPrice'] = GAS_PRICE
            transaction['chainId'] = settings.ETHEREUM_CHAINID
            transaction['from'] = account.address
            transaction['nonce'] = w3.eth.getTransactionCount(account=account.address,block_identifier=w3.eth.defaultBlock)
            print('transaction', transaction)

            signed_transaction = account.signTransaction(transaction)
            #print('signed_transaction.rawTransaction', signed_transaction.rawTransaction)
            #print(signed_transaction)

            transaction_sent = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
            print('transaction_sent', w3.toHex(transaction_sent))

            transaction_recepipt = wait_for_tx_receipt(w3, transaction_sent, 2)
            print('tx_recept.tx_hash', w3.toHex(transaction_recepipt.transactionHash))

            print('transaction_status', transaction_recepipt.status)
            print('transaction_recepipt', transaction_recepipt)

            processed_receipt = contract_instance.events.PaymentMade().processReceipt(transaction_recepipt)[0]
            print('processed_receipt', processed_receipt)

            if(processed_receipt['event']=='PaymentMade'):
                payout.paid = True
                payout.save()
                print('Moneyz sent..')
            else:
                payout.failed_payment = True
                payout.save()
                print('Failed transaction..')

            print('-'*100)


        print('Waiting for the new credits requests on the queue...')
        print('Sleeping 1 second..')
        time.sleep(1)
