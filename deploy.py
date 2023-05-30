from solcx import compile_standard, install_solc
import json 
import os
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# install solidity version if not installed 
install_solc('0.8.20')

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        }
    },
    solc_version="0.8.20"
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)
    

#ByteCode
#ABI

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = json.loads(
    compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["metadata"]
    )["output"]["abi"]

# Create new instance of the contract
w3 = Web3(Web3.HTTPProvider("https://sepolia.infura.io/v3/b65d25a7f30e43d681e9dc23637128a1"))
chain_id = 11155111
my_address = "0x75767610d15FA80425a2BDF6Cd8FCA6444786189"
private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi = abi, bytecode = bytecode)


#Nonce
nonce = w3.eth.get_transaction_count(my_address)

#Build the transaction
gas_estimate = 600000

try:
    transaction = SimpleStorage.constructor().build_transaction(
        {
        "chainId" : chain_id,
        "gas" : gas_estimate,
        "gasPrice" : w3.eth.gas_price,
        "from" : my_address,
        "nonce": nonce,
        }
    )
except ValueError as error:
    print(f"Error occurred while building transaction: {error}")

#Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)


#send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
print("Waiting for transaction to finish")
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

#work with deployed contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

#call --> simulate a call to get a value
#transact change state in the blockchain
print(simple_storage.functions.retrieve().call())

store_transaction = simple_storage.functions.store(15).build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce +1,
    }
       
)

signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
print("Updating stored value")

t_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(t_hash)

print(simple_storage.functions.retrieve().call())