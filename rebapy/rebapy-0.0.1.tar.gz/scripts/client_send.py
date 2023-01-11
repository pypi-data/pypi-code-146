import os

from web3 import Web3
from rebapy import RelayClient

PRIVATE_KEY = os.getenv("PK")
AVAX_URI = "https://api.avax.network/ext/bc/C/rpc"

if __name__ == "__main__":
    if not PRIVATE_KEY:
        raise Exception("Please set the PK environment variable")

    web3 = Web3(Web3.HTTPProvider(AVAX_URI))
    signer = web3.eth.account.from_key(PRIVATE_KEY)
    # get the current gas price
    gas_price = web3.eth.gasPrice

    client = RelayClient(PRIVATE_KEY)
    empty_tx = {
        "chainId": 43114,
        "to": signer.address,
        "value": 0,
        "nonce": web3.eth.getTransactionCount(signer.address),
        'gas': 250000,
        'gasPrice': gas_price
    }
    client.send_tx(empty_tx)
