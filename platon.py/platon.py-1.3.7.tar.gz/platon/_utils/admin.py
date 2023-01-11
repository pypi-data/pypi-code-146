from typing import (
    Callable,
    List,
    Tuple,
)

from platon._utils.compat import (
    Protocol,
)
from platon._utils.rpc_abi import (
    RPC,
)
from platon.method import (
    Method,
    default_root_munger,
)
from platon.module import (
    Module,
)
from platon.types import (
    EnodeURI,
    NodeInfo,
    Peer,
)


def admin_start_params_munger(
        module: Module, host: str = 'localhost', port: int = 8546, cors: str = '',
        apis: str = 'web3,net,platon'
) -> Tuple[str, int, str, str]:
    return (host, port, cors, apis)


add_peer: Method[Callable[[EnodeURI], bool]] = Method(
    RPC.admin_addPeer,
    mungers=[default_root_munger],
)

rmeove_peer: Method[Callable[[EnodeURI], bool]] = Method(
    RPC.admin_removePeer,
    mungers=[default_root_munger],
)

data_dir: Method[Callable[[], str]] = Method(
    RPC.admin_datadir,
    mungers=None,
)

node_info: Method[Callable[[], NodeInfo]] = Method(
    RPC.admin_nodeInfo,
    mungers=None,
)

peers: Method[Callable[[], List[Peer]]] = Method(
    RPC.admin_peers,
    mungers=None,
)


class ServerConnection(Protocol):
    def __call__(
            self, host: str = "localhost", port: int = 8546, cors: str = "", apis: str = "web3,net,platon"
    ) -> bool:
        pass


start_rpc: Method[ServerConnection] = Method(
    RPC.admin_startRPC,
    mungers=[admin_start_params_munger],
)

start_ws: Method[ServerConnection] = Method(
    RPC.admin_startWS,
    mungers=[admin_start_params_munger],
)

stop_rpc: Method[Callable[[], bool]] = Method(
    RPC.admin_stopRPC,
    mungers=None,
)

stop_ws: Method[Callable[[], bool]] = Method(
    RPC.admin_stopWS,
    mungers=None,
)

import_chain: Method[Callable[[str], str]] = Method(
    RPC.admin_importChain,
    mungers=[default_root_munger],
)

export_chain: Method[Callable[[str, int, int], str]] = Method(
    RPC.admin_exportChain,
    mungers=[default_root_munger],
)

get_program_version: Method[Callable[[], str]] = Method(
    RPC.admin_getProgramVersion,
    mungers=None,
)

get_schnorr_NIZK_prove: Method[Callable[[], str]] = Method(
    RPC.admin_getSchnorrNIZKProve,
    mungers=None,
)

# set_solc: Method[Callable[[], str]] = Method(
#     RPC.admin_setSolc,
#     mungers=None,
# )
