from typing import (
    Callable,
)

from platon_typing import HexStr

from platon.method import (
    Method, default_root_munger,
)

from platon._utils.rpc_abi import (
    RPC,
)

from platon.module import (
    Module,
)


class Debug(Module):
    economic_config: Method[Callable[[], str]] = Method(RPC.debug_economicConfig)
    get_wait_slashing_node_list: Method[Callable[[], str]] = Method(RPC.debug_getWaitSlashingNodeList)
    get_bad_blocks: Method[Callable[[], str]] = Method(RPC.debug_getBadBlocks)

    accountRange: Method[Callable[[HexStr, int], str]] = Method(
        RPC.debug_accountRange,
        mungers=[default_root_munger],
    )

    chaindbProperty: Method[Callable[[str], str]] = Method(
        RPC.debug_chaindbProperty,
        mungers=[default_root_munger],
    )
