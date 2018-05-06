contract_source_code = '''
pragma solidity ^0.4.2;

contract Loyalty {

    address admin;
    string public vendorName;
    mapping(address=>uint256) public pointBalance;

    event EventAddPoint(address indexed target, uint256 point);
    event EventTransferPoint(address indexed from, address indexed to, uint256 point);
    event EventExchangeReward(address indexed sender, uint itemId, uint256 point);

    modifier onlyAdmin {
        require(admin == msg.sender);
        _;
    }

    function Loyalty(string _vendorName) public{
        admin = msg.sender;
        vendorName = _vendorName;
    }


    function AddPoint(address target, uint256 point) onlyAdmin public{
        pointBalance[target] += point;
        emit EventAddPoint(target,point);
    }

    function TransferPoint(address sender, address receiver, uint256 point) public{
        require(pointBalance[sender]>=point);
        pointBalance[receiver] += point;
        pointBalance[sender] -= point;
        emit EventTransferPoint(sender,receiver,point);
    }

    function ExchangeReward(address target, uint rewardId, uint256 point) public returns (uint){
        require(pointBalance[target]>=point);
        pointBalance[target] -= point;
        emit EventExchangeReward(target,rewardId,point);
        return rewardId;
    }
}
'''