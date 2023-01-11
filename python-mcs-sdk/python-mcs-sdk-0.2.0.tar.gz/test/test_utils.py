import web3
from eth_account.messages import encode_defunct, defunct_hash_message
from eth_account import Account

from mcs import McsAPI
from mcs.common.params import Params

if __name__ == '__main__':
    api_mumbai = McsAPI(Params('mumbai').MCS_API)
    nonce = api_mumbai.user_register("0xde0Ee5761d86dbe9eb0aA570E9d107751875B03B")["data"]["nonce"]
    print(nonce)
    # nonce = "975789313157040720543785617726534150506"
    wallet_address = "0xde0Ee5761d86dbe9eb0aA570E9d107751875B03B"
    private_key = "d5051b1965a3572eaa4741d06809bf2bebac270175cda1ec55aa22df0bbe348d"

    message = encode_defunct(text=nonce)
    signed_message = Account.sign_message(message, private_key=private_key)["signature"]
    signature = web3.Web3.toHex(signed_message)
    login = api_mumbai.user_login(wallet_address, signature, nonce, "polygon.mumbai")
    jwt = login["data"]["jwt_token"]
    print(jwt)
