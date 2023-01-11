from typing import (
    TYPE_CHECKING,
)

from platon._utils.normalizers import (
    abi_ens_resolver,
)
from platon._utils.rpc_abi import (
    RPC_ABIS,
    abi_request_formatters,
)
from platon.types import (
    Middleware,
)

from .formatting import (
    construct_formatting_middleware,
)

if TYPE_CHECKING:
    from platon import Web3


def name_to_address_middleware(w3: "Web3") -> Middleware:
    normalizers = [
        abi_ens_resolver(w3),
    ]
    return construct_formatting_middleware(
        request_formatters=abi_request_formatters(normalizers, RPC_ABIS)
    )
