from typing import (
    Callable,
)

from platon._utils.rpc_abi import (
    RPC,
)
from platon.method import (
    Method,
    default_root_munger,
)
from platon.types import (
    Von,
)


# set_extra: Method[Callable[[str], bool]] = Method(
#     RPC.miner_setExtra,
#     mungers=[default_root_munger],
# )


set_gas_price: Method[Callable[[Von], bool]] = Method(
    RPC.miner_setGasPrice,
    mungers=[default_root_munger],
)
