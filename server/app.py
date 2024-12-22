import os
from web3 import Web3

FLAG = os.getenv('FLAG', 'flag{fake_flag}')
SETUP_ADDRESS = os.getenv('SETUP_ADDRESS', '0x0')
RPC = os.getenv('RPC', 'https://rpc.bordel.wtf/test')

def main():
	print("verifiyer 0.1.0")
	print(f"Using {RPC}")
	print("Enter your address: ", end='')
	address = input()

	w3 = Web3(Web3.HTTPProvider(RPC))

	def is_solved(address):
		contract = w3.eth.contract(address=SETUP_ADDRESS, abi=[{
			"constant": True,
			"inputs": [{"name": "address", "type": "address"}],
			"name": "isSolved",
			"outputs": [{"name": "", "type": "bool"}],
			"payable": False,
			"stateMutability": "view",
			"type": "function"
		}])
		return contract.functions.isSolved(address).call()

	if is_solved(address):
		print("Challenge solved!")
		print(FLAG)
	else:
		print("Challenge not solved.")

main()