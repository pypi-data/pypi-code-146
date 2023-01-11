from typing import (
    Callable,
)

from platon._utils.rpc_abi import (
    RPC,
)
from platon.method import (
    Method,
)
from platon.module import (
    Module,
)


class BaseVersion(Module):
    retrieve_caller_fn = None

    _get_node_version: Method[Callable[[], str]] = Method(RPC.web3_clientVersion)
    _get_protocol_version: Method[Callable[[], str]] = Method(RPC.platon_protocolVersion)

    @property
    def api(self) -> str:
        from platon import __version__
        return __version__


class AsyncVersion(BaseVersion):
    is_async = True

    @property
    async def node(self) -> str:
        # types ignored b/c mypy conflict with Version properties
        return await self._get_node_version()  # type: ignore

    @property
    async def platon(self) -> int:
        return await self._get_protocol_version()  # type: ignore


class Version(BaseVersion):
    @property
    def node(self) -> str:
        return self._get_node_version()

    @property
    def platon(self) -> str:
        return self._get_protocol_version()

    @property
    def chain(self) -> str:
        return self.web3.pip.get_chain_version()
