from datetime import date, time
from enum import Enum
from typing import Optional
from uuid import UUID

from serenity_types.refdata.asset import Asset
from serenity_types.utils.serialization import CamelModel


class SettlementType(Enum):
    CASH = 'CASH'
    """
    Derivative contract settled in fiat or stablecoins.
    """

    PHYSICAL = 'PHYSICAL'
    """
    Derivative contract settled in an asset other than fiat or stablecoins.
    """


class PayoffType(Enum):
    LINEAR = 'LINEAR'
    """
    Linear payoff that follows the price movement of the underlier.
    """

    INVERSE = 'INVERSE'
    """
    Non-linear payoff that moves opposite the underlying price movements.
    """


class DerivativeAsset(Asset):
    """
    A listed or OTC derivative contract.
    """

    underlier_asset_id: UUID
    """
    The underlying asset for this derivative contract, e.g. BTC (tok.btc.bitcoin).
    Note we will be switching to the Exposure UUID instead in a future release (e.g. tok.btc),
    once the reference data is available.
    """

    reference_index_id: Optional[UUID]
    """
    The specific index, e.g. Deribit BTC Index, used to get a fair price for the underlying at settlement time.
    """

    contract_size: float
    """
    Size of the contract in qty of underlying.
    """

    settlement_asset_id: UUID
    """
    The asset that this derivatives settles in, e.g. on Deribit, CASH settled, it might be USD.
    Note we will be switching to the Exposure UUID instead in a future release.
    """

    settlement_type: SettlementType
    """
    Whether this contract settles in cash or in the underlying itself.
    """


class ListedDerivative(DerivativeAsset):
    """
    An exchange-listed derivative contract.
    """

    exchange_id: UUID
    """
    The exchange on which this contract is listed.
    """


class Expiry(CamelModel):
    expiration_date: date
    """
    The local expiration date in the contract specification; exact datetime requires a timezone.
    """

    expiration_time: time
    """
    The local expiration time in the contract specification; exact datetime requires a timezone.
    """
