from datetime import datetime
from uuid import UUID

from serenity_types.refdata.derivatives import SettlementType
from serenity_types.refdata.options import OptionStyle, OptionType
from serenity_types.utils.serialization import CamelModel


class Future(CamelModel):
    """
    Legacy futures reference data; use serenity_types.refdata.futures.Future instead.
    """

    asset_id: UUID
    listed_on: UUID
    underlier_asset_id: UUID
    expiry_datetime: datetime
    settlement_asset_id: UUID
    settlement_type: SettlementType


class Index(CamelModel):
    """
    Legacy index reference data; use serenity_types.refdata.index.Index instead.
    """

    asset_id: UUID
    provider_id: UUID
    symbol: str
    family: str
    display_name: str


class ListedOption(CamelModel):
    """
    Legacy options reference data; use serenity_types.refdata.options.Option instead.
    """

    asset_id: UUID
    listed_on: UUID
    underlier_asset_id: UUID
    option_type: OptionType
    option_style: OptionStyle
    strike_price: float
    expiry_datetime: datetime
    settlement_asset_id: UUID
    settlement_type: SettlementType


class Perpetual(CamelModel):
    """
    Legacy perpetuals reference data; use serenity_types.refdata.futures.Perpetual instead.
    """

    asset_id: UUID
    listed_on: UUID
    underlier_asset_id: UUID
    settlement_asset_id: UUID
    settlement_type: SettlementType


class ReferenceRate(CamelModel):
    """
    Legacy reference index reference data; use serenity_types.refdata.index.ReferenceIndex instead.
    """

    asset_id: UUID
    provider_id: UUID
    linked_asset_id: UUID
    index_asset_id: UUID
    display_name: str


class Currency(CamelModel):
    """
    Legacy fiat currency reference data; use serenity_types.refdata.currency.Currency instead.
    """

    asset_id: UUID
    iso_currency_code: str
    display_name: str


class Token(CamelModel):
    """
    Legacy token reference data; use serenity_types.refdata.exposure.Exposure instead.
    """

    token_id: UUID
    blockchain_network_id: UUID
    symbol: str
    native_symbol: str
    display_name: str
    logo: str


class TokenAsset(CamelModel):
    """
    Legacy token asset reference data; use serenity_types.refdata.token.TokenAsset instead.
    """

    asset_id: UUID
    token: Token
