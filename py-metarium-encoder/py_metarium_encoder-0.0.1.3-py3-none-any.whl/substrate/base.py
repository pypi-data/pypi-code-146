# Author: MetariumProject

# third party libraries
from substrateinterface import SubstrateInterface, Keypair, ExtrinsicReceipt
from substrateinterface.base import GenericCall
# metarium libraries
from py_metarium import (
    Metarium, LABEL_SUBSTRATE
)

METARIUM_EXTRINSIC = "Metarium"


class SubstrateBaseEncoder:

    SUBSTRATE_EXTRINSIC = "Metarium"

    def __init__(self, url:str=None, mnemonic:str=None) -> None:
        self.__reset()
        initialization_parameters = {
            "chain": {
                "type": LABEL_SUBSTRATE,
                "parameters": {
                    "url" : url
                }
            }
        }

        self.metarium = Metarium(**initialization_parameters)
        self.metarium_node = SubstrateInterface(url=url)
        self.key_pair = Keypair.create_from_mnemonic(mnemonic)
        self.current_nonce = self.metarium_node.get_account_nonce(self.key_pair.ss58_address)

    def __reset(self):
        self.key_pair = None

    def info(self):
        return self.metarium.chain.info()

    def __encode_signed(self,
            call:GenericCall=None,
            wait_for_inclusion:bool=False, wait_for_finalization:bool=False) -> ExtrinsicReceipt:
        # get the nonce for the account
        # print(f"Nonce: {self.current_nonce}")
        # generate the signature payload for the transaction call
        signature_payload = self.metarium_node.generate_signature_payload(call=call, nonce=self.current_nonce)
        # print(f"Signature payload: {signature_payload}")
        # sign the payload
        signature = self.key_pair.sign(signature_payload)
        # print(f"Signature: {signature}")
        # create the signed transaction call to the chain
        transaction = self.metarium_node.create_signed_extrinsic(
            call=call,
            keypair=self.key_pair,
            signature=signature,
            nonce=self.current_nonce
        )
        print(f"Transaction: {transaction}")
        # submit the transaction call to the chain
        result = self.metarium_node.submit_extrinsic(
            transaction,
            wait_for_inclusion=wait_for_inclusion,
            wait_for_finalization=wait_for_finalization
        )
        # return the transaction hash
        # print(f"Result: {result}")
        return result

    def encode(self, data:dict={}, wait_for_inclusion:bool=False, wait_for_finalization:bool=False):
        # check if data is valid
        assert self.is_valid_data(data=data)
        # check if keypair is valid
        assert self.key_pair is not None
        # compose the transaction call
        call = self.compose_call(data=data)
        receipt = self.__encode_signed(
            call=call,
            wait_for_inclusion=wait_for_inclusion, wait_for_finalization=wait_for_finalization)
        
        if receipt.is_success:
            self.current_nonce += 1
            return receipt.extrinsic_hash
        else:
            print(f"\n\n\nERROR : Transaction failed\n\n{receipt.error_message}\n\n")


    # child classes should implement these methods
    def is_valid_data(self, data:dict={}):
        raise NotImplementedError
    
    def compose_call(self, data:dict={}):
        raise NotImplementedError
