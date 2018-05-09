from web3 import Web3, HTTPProvider

from .compiled_contract import compiled_contract
from ..models import Vendor, User
from ..settings import blockchain_url
import uuid

print('connecting to blockchain blockchain network')
w3 = Web3(HTTPProvider(endpoint_uri=blockchain_url))
print(w3.isConnected())
print('successfully connected to blockchain network')
compiled_sol = compiled_contract
contract_interface = compiled_sol['<stdin>:Loyalty']


def get_master_wallet_info():
    print('getting master wallet info')
    print(w3.eth)
    print(w3.eth.accounts)
    master_wallet = {
        'wallet_address':w3.eth.accounts[0],
        'ether':w3.eth.getBalance(w3.eth.accounts[0])
    }
    print('success')
    print(master_wallet)
    return master_wallet


def random_string():
    return uuid.uuid4().hex[:6].upper()


def create_wallet():
    passphrase = random_string()
    wallet_address = w3.personal.newAccount(passphrase)
    w3.personal.unlockAccount(wallet_address,passphrase=passphrase)
    return wallet_address


def add_point(user_id,vendor_id,point):
    user = User.objects.get(id=user_id)
    vendor = Vendor.objects.get(id=vendor_id)

    contract = w3.eth.contract(address=vendor.contract_address,abi=contract_interface['abi'])
    contract.functions.AddPoint(user.wallet_address,int(point)).transact(transaction={'from': w3.eth.accounts[0]})


def get_all_account():
    return w3.eth.accounts


def exchange_reward(user_id, reward_id,vendor_id,point):
    user = User.objects.get(id=user_id)
    vendor = Vendor.objects.get(id=vendor_id)
    contract = w3.eth.contract(address=vendor.contract_address,abi=contract_interface['abi'])
    contract.functions.ExchangeReward(user.wallet_address,int(reward_id), int(point)).transact(transaction={'from': w3.eth.accounts[0]})


def transfer_point(sender_id,receiver_id,vendor_id,point):
    sender = User.objects.get(id=sender_id)
    receiver = User.objects.get(id=receiver_id)
    vendor = Vendor.objects.get(id=vendor_id)
    contract = w3.eth.contract(address=vendor.contract_address,abi=contract_interface['abi'])
    contract.functions.TransferPoint(sender.wallet_address,receiver.wallet_address,int(point)).transact(transaction={'from': w3.eth.accounts[0]})


def query_vendors_points_by_user_id(user_id,vendor_id_list):
    result = []
    user = User.objects.get(id=user_id)
    for vendor_id in vendor_id_list:
        vendor = Vendor.objects.get(id=vendor_id)
        contract = w3.eth.contract(address=vendor.contract_address,abi=contract_interface['abi'])
        point = contract.call().pointBalance(user.wallet_address)
        result.append({'vendor_id':vendor_id,'point':point})

    return result


def create_contract(vendor_name):

    # Instantiate and deploy contract
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    # Get transaction hash from deployed contract
    tx_hash = contract.deploy(args=[vendor_name], transaction={'from': w3.eth.accounts[0]})

    # Get tx receipt to get contract address
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    contract_address = tx_receipt['contractAddress']

    return contract_address


def test():

    return query_vendors_points_by_user_id(19,[10])
    # contract = w3.eth.contract(address='0x5cf6788E355B13b0247C5096CCEAC1313cd3A2be', abi=contract_interface['abi'])
    # point = contract.call().pointBalance('0x423F0beeA991D188Df6a7cBe4c7898Fa43dE5b35')
    # return point