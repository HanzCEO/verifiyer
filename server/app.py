import os, hashlib
from web3 import Web3
import rlp
from eth_utils import keccak

FLAG = os.getenv('FLAG', 'flag{fake_flag}')
SETUP_BYTECODE = os.getenv('SETUP_BYTECODE', None)
SETUP_GAS = int(os.getenv('SETUP_GAS', 400000))
SETUP_GAS_PRICE = int(os.getenv('SETUP_GAS_PRICE', 5))
CONSTRUCTOR_VALUE = int(os.getenv('CONSTRUCTOR_VALUE', 1))
PRIVATE_KEY = os.getenv('PRIVATE_KEY', None)
DIFFICULTY = int(os.getenv('DIFFICULTY', 6))
CHAIN_ID = int(os.getenv('CHAIN_ID', 39438141))
RPC = os.getenv('RPC', 'https://rpc.bordel.wtf/test')

SETUP_ABI = [{
	"constant": False,
	"inputs": [{"name": "_player", "type": "address"}],
	"name": "constructor",
	"outputs": [],
	"payable": True,
	"stateMutability": "payable",
	"type": "constructor"
}, {
	"constant": True,
	"inputs": [],
	"name": "challenge",
	"outputs": [{"name": "", "type": "address"}],
	"payable": False,
	"stateMutability": "view",
	"type": "function"
},{
	"constant": True,
	"inputs": [],
	"name": "isSolved",
	"outputs": [{"name": "", "type": "bool"}],
	"payable": False,
	"stateMutability": "view",
	"type": "function"
}]

assert SETUP_BYTECODE is not None
assert PRIVATE_KEY is not None

w3 = Web3(Web3.HTTPProvider(RPC))

def verifyPoW(pow):
	if pow.isdigit():
		pow = int(pow)
		if pow not in range(100000, 10000000000000000):
			return False
	hashed = hashlib.sha256(str(pow).encode()).hexdigest()
	hashed = hashlib.sha256(hashed.encode()).hexdigest()
	return hashed.startswith('0' * DIFFICULTY)

def generate_eth_account_from(uid):
	uid = int(uid)
	private_key = hashlib.sha256(str(uid).encode()).hexdigest()
	private_key_bytes = bytes.fromhex(private_key)
	account = w3.eth.account.from_key(private_key_bytes)
	return account

def generate_contract_address_from(address):
	nonce = 0
	sender_bytes = bytes.fromhex(address[2:])
	rlp_encoded = rlp.encode([sender_bytes, nonce])
	contract_address = keccak(rlp_encoded)[-20:]
	return Web3.to_checksum_address(contract_address.hex())

def check_contract_exists(address):
	contract_address = generate_contract_address_from(address)
	return len(w3.eth.get_code(contract_address)) > 0

def is_solved(address):
	setup_contract = generate_contract_address_from(address)
	contract = w3.eth.contract(address=setup_contract, abi=SETUP_ABI)
	return contract.functions.isSolved().call()

def giveStartingEth(account):
	host_account = w3.eth.account.from_key(PRIVATE_KEY)
	creation_tx = make_contract_tx(account)
	tx = host_account.sign_transaction({
		'to': account.address,
		'value': w3.to_wei(CONSTRUCTOR_VALUE + calculate_tx_fee(creation_tx), 'ether'),
		'nonce': w3.eth.get_transaction_count(host_account.address),
		'gas': 21000,
		'gasPrice': w3.to_wei(SETUP_GAS_PRICE, 'gwei'),
		"chainId": CHAIN_ID
	})
	tx_hash = w3.eth.send_raw_transaction(tx.raw_transaction)
	w3.eth.wait_for_transaction_receipt(tx_hash)

def calculate_tx_fee(tx):
	# TODO: accurately calculate tx fee
	return w3.from_wei(tx['gas'] * tx['gasPrice'], 'ether')

def make_contract_tx(account):
	contract = w3.eth.contract(bytecode=SETUP_BYTECODE, abi=SETUP_ABI)
	tx = contract.constructor(account.address).build_transaction({
		'from': account.address,
		'value': w3.to_wei(CONSTRUCTOR_VALUE, 'ether'),
		'nonce': 0,
		'gas': SETUP_GAS,
		'gasPrice': w3.to_wei(SETUP_GAS_PRICE, 'gwei'),
		"chainId": CHAIN_ID
	})
	return tx

def create_setup_contract(account):
	giveStartingEth(account)
	tx = make_contract_tx(account)
	signed_tx = w3.eth.account.sign_transaction(tx, private_key=account.key)
	tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
	tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
	return tx_receipt.contractAddress

def get_challenge_address(setup_address):
	contract = w3.eth.contract(address=setup_address, abi=[{
		"constant": True,
		"inputs": [],
		"name": "challenge",
		"outputs": [{"name": "", "type": "address"}],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	}])
	return contract.functions.challenge().call()

def main():
	print("verifiyer 0.1.0")
	print(f"Using {RPC}")
	print()
	print("Enter your PoW: ", end='')
	pow = input()
	
	if verifyPoW(pow):
		print("PoW is valid.")
		
		account = generate_eth_account_from(pow)
		if check_contract_exists(account.address):
			if is_solved(account.address):
				print("Challenge solved!")
				print(FLAG)
			else:
				print("Instance exists.")
				print("Challenge remains unsolved.")
				setup_address = generate_contract_address_from(account.address)
				challenge_address = get_challenge_address(setup_address)
		else:
			print("Creating setup contract...")
			setup_address = create_setup_contract(account)
			challenge_address = get_challenge_address(setup_address)
		print(f"Setup       : {setup_address}")
		print(f"Challenge   : {challenge_address}")
		print(f"Your Address: {account.address}")
		print(f"Private Key : 0x{account.key.hex()}")
		print(f"RPC         : {RPC}")
	else:
		print("PoW is invalid.")

main()