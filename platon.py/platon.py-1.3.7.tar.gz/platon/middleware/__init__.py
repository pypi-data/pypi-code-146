import functools
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Sequence,
)

from platon.types import (
    RPCEndpoint,
    RPCResponse,
    Middleware,
)
from .abi import (
    abi_middleware,
)
from .attrdict import (
    attrdict_middleware,
)
from .buffered_gas_estimate import (
    async_buffered_gas_estimate_middleware,
    buffered_gas_estimate_middleware,
)
from .cache import (
    _latest_block_based_cache_middleware as latest_block_based_cache_middleware,
    _simple_cache_middleware as simple_cache_middleware,
    _time_based_cache_middleware as time_based_cache_middleware,
    construct_latest_block_based_cache_middleware,
    construct_simple_cache_middleware,
    construct_time_based_cache_middleware,
)
from .exception_handling import (
    construct_exception_handler_middleware,
)
from .exception_retry_request import (
    http_retry_request_middleware,
)
from .filter import (
    local_filter_middleware,
)
from .fixture import (
    construct_error_generator_middleware,
    construct_fixture_middleware,
    construct_result_generator_middleware,
)
from .formatting import (
    construct_formatting_middleware,
)
from .gas_price_strategy import (
    async_gas_price_strategy_middleware,
    gas_price_strategy_middleware,
)
from .gplaton_poa import (
    gplaton_poa_middleware,
)
from .names import (
    name_to_address_middleware,
)
from .normalize_request_parameters import (
    request_parameter_normalizer,
)
from .pythonic import (
    pythonic_middleware,
)
from .signing import (
    construct_sign_and_send_raw_middleware,
)
from .stalecheck import (
    make_stalecheck_middleware,
)
from .validation import (
    validation_middleware,
)

if TYPE_CHECKING:
    from platon import Web3


def combine_middlewares(
    middlewares: Sequence[Middleware],
    web3: 'Web3',
    provider_request_fn: Callable[[RPCEndpoint, Any], Any]
) -> Callable[..., RPCResponse]:
    """
    Returns a callable function which will call the provider.provider_request
    function wrapped with all of the middlewares.
    """
    return functools.reduce(
        lambda request_fn, middleware: middleware(request_fn, web3),
        reversed(middlewares),
        provider_request_fn,
    )


async def async_combine_middlewares(
    middlewares: Sequence[Middleware],
    web3: 'Web3',
    provider_request_fn: Callable[[RPCEndpoint, Any], Any]
) -> Callable[..., RPCResponse]:
    """
    Returns a callable function which will call the provider.provider_request
    function wrapped with all of the middlewares.
    """
    accumulator_fn = provider_request_fn
    for middleware in reversed(middlewares):
        accumulator_fn = await construct_middleware(middleware, accumulator_fn, web3)
    return accumulator_fn


async def construct_middleware(
    middleware: Middleware,
    fn: Callable[..., RPCResponse],
    w3: 'Web3'
) -> Callable[[RPCEndpoint, Any], Any]:
    return await middleware(fn, w3)
