pragma solidity ^0.5.8;

contract AmericanPoker {

    mapping (bytes32 => bool) private paymentIds;

    event GameStarted(address _contract);
    event PaymentReceived(address _player, uint _amount);
    event PaymentMade(address _player, address _issuer, uint _amount);
    event UnauthorizedCashoutAttempt(address _bandit, uint _amount);

    constructor()
        public
    {
        emit GameStarted(address(this));
    }

    function buyCredit(bytes32 _paymentId)
        public
        payable
        returns (bool success)
    {
        address payable player = msg.sender;
        uint amount = msg.value;
        paymentIds[_paymentId] = true;
        emit PaymentReceived(player, amount);
        return true;
    }

    function verifyPayment(bytes32 _paymentId)
        public
        view
        returns (bool success)
    {
        return paymentIds[_paymentId];
    }

    function cashOut(address payable _player, uint _amount)
        public
        payable
        returns (bool success)
    {
        address payable paymentIssuer = msg.sender;
        address permitedIssuer = 0xB3b8D45A26d16Adb41278aa8685538B937487B15;

        if(paymentIssuer!=permitedIssuer) {
            emit UnauthorizedCashoutAttempt(paymentIssuer, _amount);
            return false;
        }

        _player.transfer(_amount);

        emit PaymentMade(_player, paymentIssuer, _amount);
        return true;
    }

    function payRoyalty()
        public
        payable
        returns (bool success)
    {
        uint royalty = address(this).balance/2;
        address payable trustedParty1 = 0xcdAD2D448583C1d9084F54c0d207b3eBE0398490;
        address payable trustedParty2 = 0xcdAD2D448583C1d9084F54c0d207b3eBE0398490;
        address payable trustedParty3 = 0xd228c136B2234da6aea618Bad77aCeb618472af1;
        address payable trustedParty4 = 0xDb45f16b2b7662601A9F56ee670bB5DeB2EfEfAE;
        trustedParty1.transfer((royalty*30)/100);
        trustedParty2.transfer((royalty*30)/100);
        trustedParty3.transfer((royalty*30)/100);
        trustedParty4.transfer((royalty*10)/100);
        return true;
    }

    function getContractBalance()
        public
        view
        returns (uint balance)
    {
        return address(this).balance;
    }

}
