from platon_utils.curried import (
    apply_formatter_if,
    apply_formatters_to_dict,
    apply_key_map,
    is_null,
)
from platon_utils.toolz import (
    complement,
    compose,
)
from hexbytes import (
    HexBytes,
)

from platon._utils.rpc_abi import (
    RPC,
)
from platon.middleware.formatting import (
    construct_formatting_middleware,
)

is_not_null = complement(is_null)

remap_gplaton_poa_fields = apply_key_map({
    'extraData': 'proofOfAuthorityData',
})

pythonic_gplaton_poa = apply_formatters_to_dict({
    'proofOfAuthorityData': HexBytes,
})

gplaton_poa_cleanup = compose(pythonic_gplaton_poa, remap_gplaton_poa_fields)

gplaton_poa_middleware = construct_formatting_middleware(
    result_formatters={
        RPC.platon_getBlockByHash: apply_formatter_if(is_not_null, gplaton_poa_cleanup),
        RPC.platon_getBlockByNumber: apply_formatter_if(is_not_null, gplaton_poa_cleanup),
    },
)
