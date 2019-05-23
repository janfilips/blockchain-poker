var rps = function() {
    return {
        inited: false,
        _test: false,
        web3js: false,
        contract: null,
        b32: (a) => {
            var __padToBytes32 = (n) => {
                while (n.length < 64) {
                    n = "0" + n;
                }
                return "0x" + n;
            }
            return __padToBytes32(new BN(a).toTwos(256).toString(16));
        },
        init: function(cb) {
            if (this.inited === false) {
                this.inited = true;

                if (typeof window.ethereum !== 'undefined' || (typeof window.web3 !== 'undefined')) {
                    // Web3 browser user detected. You can now use the provider.
                    this.web3js = new Web3(window['ethereum'] || window.web3.currentProvider);
                    this._test = ethereum.networkVersion != '1';
                    this.contract = this.web3js.eth.contract(window.contract_abi).at(window.contract_address);

                    try {
                        var promise = ethereum.enable();
                        if (promise !== undefined) {
                            promise.then(a => {
                                if (typeof ethereum.selectedAddress === 'undefined') {
                                    console.log('promise typeof ethereum.selectedAddress === undefined')
                                    $('#popup3').show();
                                } else {
                                    cb()
                                }
                            }).catch(error => {
                                console.log(error);
                                $('#popup2').show();
                            });
                        }
                    } catch (e) {
                        console.log(e);
                        $('#popup2').show();
                    }
                } else {
                    $('#popup1').show();
                }
            } else {
                if (typeof ethereum.selectedAddress === 'undefined') {
                    console.log('else typeof ethereum.selectedAddress === undefined');
                    $('#popup3').show();
                } else {
                    "function" == typeof cb && cb();
                }
            }

        },
        credit: (a, c) => {
            rps.init(() => {
                if (rps._test === false || window.debug) {
                    var paymentId = rps.b32(Math.ceil(Math.random() * 2147483640 + 1));
                    const transactionParameters = {
                        // i have got rid off gas from here ... maybe we should put it back?
                        to: window.contract_address,
                        from: ethereum.selectedAddress,
                        value: web3.toHex(web3.toWei(a / window.ethusdprice, 'ether')), // Only required to send ether to the recipient from the initiating external account.
                        data: rps.contract.buyCredit.getData(paymentId), // Optional, but used for defining smart contract creation and interaction.
                    }

                    ethereum.sendAsync({
                        method: 'eth_sendTransaction',
                        params: [transactionParameters],
                        from: ethereum.selectedAddress,
                    }, function(b, c) {
                        if (typeof c.result !== 'undefined') {
                            $.removeCookie('game_already_played');
                            $.ajax({
                                type: "POST",
                                url: '/ajax/buy/credit/',
                                headers: {
                                    'X-CSRFToken': csrf_token
                                },
                                data: {
                                    payment_id: paymentId,
                                    tx_id: c.result,
                                    paid_in_eth: a / window.ethusdprice,
                                    requested_amount_in_dollars: a,
                                    player_ethereum_wallet: transactionParameters.from,
                                    player_session_key: session_key,
                                },
                                success: (d) => {
                                    if (d === 'True') {
                                        window.location.href = '/payment/verifying#' + paymentId;
                                    }
                                }
                            });
                        }
                    })
                } else {
                    console.log('rps._test === false || window.debug');
                    $('#popup2').show();
                }
            });

        }
    }
}();
