from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Optional,
)

from platon_abi import (
    decode_single,
)
from platon_abi.exceptions import (
    InsufficientDataBytes,
)

from platon._utils.compat import (
    Literal,
)
from platon.providers import (
    BaseProvider,
)
from platon.providers.async_base import (
    AsyncBaseProvider,
)
from platon.types import (
    RPCEndpoint,
    RPCResponse,
)

from .middleware import (
    default_transaction_fields_middleware,
    platon_tester_middleware,
)

if TYPE_CHECKING:
    from platon_tester import (
        PlatonTester,
    )


class AsyncPlatonTesterProvider(AsyncBaseProvider):
    def __init__(self) -> None:
        self.platon_tester = PlatonTesterProvider()

    async def make_request(
        self, method: RPCEndpoint, params: Any
    ) -> RPCResponse:
        return self.platon_tester.make_request(method, params)


class PlatonTesterProvider(BaseProvider):
    middlewares = (
        default_transaction_fields_middleware,
        platon_tester_middleware,
    )
    platon_tester = None
    api_endpoints = None

    def __init__(
        self,
        platon_tester: Optional["PlatonTester"] = None,
        api_endpoints: Optional[Dict[str, Dict[str, Callable[..., RPCResponse]]]] = None
    ) -> None:
        # do not import platon_tester until runtime, it is not a default dependency
        from platon_tester import PlatonTester
        from platon_tester.backends.base import BaseChainBackend
        if platon_tester is None:
            self.platon_tester = PlatonTester()
        elif isinstance(platon_tester, PlatonTester):
            self.platon_tester = platon_tester
        elif isinstance(platon_tester, BaseChainBackend):
            self.platon_tester = PlatonTester(platon_tester)
        else:
            raise TypeError(
                "Expected platon_tester to be of type `platon_tester.PlatonTester` or "
                "a subclass of `platon_tester.backends.base.BaseChainBackend`, "
                f"instead received {type(platon_tester)}. "
                "If you would like a custom platon-tester instance to test with, see the "
                "platon-tester documentation. https://github.com/platonnetwork/platon-tester."
            )

        if api_endpoints is None:
            # do not import platon_tester derivatives until runtime, it is not a default dependency
            from .defaults import API_ENDPOINTS
            self.api_endpoints = API_ENDPOINTS
        else:
            self.api_endpoints = api_endpoints

    def make_request(self, method: RPCEndpoint, params: Any) -> RPCResponse:
        namespace, _, endpoint = method.partition('_')
        from platon_tester.exceptions import TransactionFailed
        try:
            delegator = self.api_endpoints[namespace][endpoint]
        except KeyError:
            return RPCResponse(
                {"error": f"Unknown RPC Endpoint: {method}"}
            )
        try:
            response = delegator(self.platon_tester, params)
        except NotImplementedError:
            return RPCResponse(
                {"error": f"RPC Endpoint has not been implemented: {method}"}
            )
        except TransactionFailed as e:
            try:
                reason = decode_single('(string)', e.args[0].args[0][4:])[0]
            except (InsufficientDataBytes, AttributeError):
                reason = e.args[0]
            raise TransactionFailed(f'execution reverted: {reason}')
        else:
            return {
                'result': response,
            }

    def isConnected(self) -> Literal[True]:
        return True
