from typing import (
    TYPE_CHECKING,
    Optional,
    cast,
)

from platon.types import (
    BlockIdentifier,
    TxParams,
    Von,
)

if TYPE_CHECKING:
    from platon import Web3
    from platon.platon import AsyncPlaton


async def get_block_gas_limit(
    web3_platon: "AsyncPlaton", block_identifier: Optional[BlockIdentifier] = None
) -> Von:
    if block_identifier is None:
        block_identifier = await web3_platon.block_number
    block = await web3_platon.get_block(block_identifier)
    return block['gasLimit']


async def get_buffered_gas_estimate(
    web3: "Web3", transaction: TxParams, gas_buffer: Von = Von(100000)
) -> Von:
    gas_estimate_transaction = cast(TxParams, dict(**transaction))

    gas_estimate = await web3.platon.estimate_gas(gas_estimate_transaction)  # type: ignore

    gas_limit = await get_block_gas_limit(web3.platon)  # type: ignore

    if gas_estimate > gas_limit:
        raise ValueError(
            "Contract does not appear to be deployable within the "
            "current network gas limits.  Estimated: {0}. Current gas "
            "limit: {1}".format(gas_estimate, gas_limit)
        )

    return Von(min(gas_limit, gas_estimate + gas_buffer))
