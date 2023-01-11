from typing import (
    Callable,
)

from platon._utils.rpc_abi import (
    RPC,
)
from platon.method import (
    Method,
)
from platon.types import (
    TxPoolContent,
    TxPoolInspect,
    TxPoolStatus,
)

content: Method[Callable[[], TxPoolContent]] = Method(
    RPC.txpool_content,
    mungers=None,
)


inspect: Method[Callable[[], TxPoolInspect]] = Method(
    RPC.txpool_inspect,
    mungers=None,
)


status: Method[Callable[[], TxPoolStatus]] = Method(
    RPC.txpool_status,
    mungers=None,
)
