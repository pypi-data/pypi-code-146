from enum import Enum
from typing import Union, Optional

from eth_typing import ChecksumAddress, Address
from web3 import Web3
from web3.types import TxParams

from eulith_web3.contract_bindings.i_e_r_c20 import IERC20
from eulith_web3.contract_bindings.w_e_t_h_interface import WETHInterface


class TokenSymbol(str, Enum):
    USDT = 'USDT'
    BNB = 'BNB'
    USDC = 'USDC'
    BUSD = 'BUSD'
    MATIC = 'MATIC'
    STETH = 'stETH'
    WETH = 'WETH'
    LDO = "LDO"
    CRV = 'CRV'
    CVX = 'CVX'
    BAL = 'BAL'
    BADGER = 'BADGER'
    ONEINCH = '1INCH'
    UNI = 'UNI'
    LINK = 'LINK'
    APE = 'APE'
    GMT = 'GMT'


class EulithERC20(IERC20):
    def __init__(self, web3: Web3, contract_address: Optional[Union[Address, ChecksumAddress]] = None):
        super().__init__(web3, contract_address)


# WETH is special because you can deposit native ETH to the contract to get WETH back
class EulithWETH(WETHInterface, EulithERC20):
    def __init__(self, web3: Web3, contract_address: Optional[Union[Address, ChecksumAddress]] = None):
        super().__init__(web3, contract_address)

    def deposit_eth(self, whole_eth_as_float: float):
        wei = int(whole_eth_as_float * 1e18)  # convert to wei
        return self.deposit_wei(wei)

    def deposit_wei(self, wei: int) -> TxParams:
        tx = self.deposit()
        tx['value'] = hex(wei)
        tx['gas'] = 60000  # estimates are a little flaky here
        return tx

    # You must have sufficient WETH balance for this to succeed
    def withdraw_eth(self, whole_eth_as_float: float) -> TxParams:
        wei = int(whole_eth_as_float * 1e18)
        tx = self.withdraw(wei)
        tx['gas'] = 60000  # estimates are a little flaky here
        return tx
