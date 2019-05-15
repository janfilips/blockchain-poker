var rps = function() {
    return {
        inited: false,
        _test: false,
        web3js: false,
        contract: null,
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
                                cb()
                            }).catch(error => {
                                console.log(error);
                                // client error
                            });
                        }
                    } catch (e) {
                        // private network
                    }

                    // console.log(error);
                } else {
                    console.log('No web3? You should consider trying MetaMask!')
                }
            } else {
                "function" == typeof cb && cb();
            }

        },
        credit: (a, c) => {
            rps.init(() => {
                var paymentId = Math.ceil(Math.random() * 2147483640 + 1);
                const transactionParameters = {
                    // i have got rid off gas from here ... maybe we should put it back?
                    to: window.contract_address,
                    from: ethereum.selectedAddress,
                    value: "50000000000000", //web3.toWei(a / window.ethusdprice, 'ether'), // Only required to send ether to the recipient from the initiating external account.
                    data: rps.contract.buyCredit.getData(paymentId), // Optional, but used for defining smart contract creation and interaction.
                }
                console.log('wei: ' + transactionParameters.value);

                ethereum.sendAsync({
                    method: 'eth_sendTransaction',
                    params: [transactionParameters],
                    from: ethereum.selectedAddress,
                }, function(b, c) {
                    if (typeof c.result !== 'undefined') {
                        $.ajax({
                            type: "POST",
                            url: '/ajax/buy/credit/',
                            headers: {
                                'X-CSRFToken': csrf_token
                            },
                            data: {
                                payment_id: paymentId,
                                tx_id: c.result,
                                paid_in_eth: web3.fromWei(transactionParameters.value),
                                requested_amount_in_dollars: a,
                                player_ethereum_wallet: transactionParameters.from,
                                player_session_key: session_key,
                            },
                            success: (d) => {
                                console.log(d);
                            }
                        });
                    }
                })
            });

        }
    }
}();
