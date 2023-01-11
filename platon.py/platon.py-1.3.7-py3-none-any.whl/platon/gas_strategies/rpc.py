from typing import (
    Optional,
)

from platon import Web3
from platon._utils.rpc_abi import (
    RPC,
)
from platon.types import (
    TxParams,
    Von,
)


def rpc_gas_price_strategy(web3: Web3,
                           transaction_params: Optional[TxParams] = None) -> Von:
    """
    A simple gas price strategy deriving it's value from the platon_gasPrice JSON-RPC call.
    """
    return web3.manager.request_blocking(RPC.platon_gasPrice, [])
