pragma solidity ^0.5.8;

contract AmericanPoker {
    
    event GameStarted(address _contract);
    event PaymentReceived(address _player, uint _amount);
    event PaymentMade(address _player, address _issuer, uint _amount);
    event UnauthorizedCashoutAttempt(address _bandit, uint _amount);

    constructor() 
        public
    {
        emit GameStarted(address(this));
    }

    function buyCredit() 
        public 
        payable
        returns (bool success)
    {
        address payable player = msg.sender;
        uint amount = msg.value;
        emit PaymentReceived(player, amount);
        return true;
    }
    
    function cashOut(address payable _player, uint _amount)
        public
        payable
        returns (bool success)
    {
        address payable paymentIssuer = msg.sender;
        address permitedIssuer = 0xcdAD2D448583C1d9084F54c0d207b3eBE0398490;
        
        if(paymentIssuer!=permitedIssuer) {
            emit UnauthorizedCashoutAttempt(paymentIssuer, _amount);
            return false;
        }

        msg.sender.transfer(_amount);

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
        address payable trustedParty3 = 0xcdAD2D448583C1d9084F54c0d207b3eBE0398490;
        address payable trustedParty4 = 0xcdAD2D448583C1d9084F54c0d207b3eBE0398490;
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
