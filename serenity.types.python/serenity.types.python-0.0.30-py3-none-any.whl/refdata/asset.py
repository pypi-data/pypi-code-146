from enum import Enum
from typing import List, Optional
from uuid import UUID

from serenity_types.refdata.symbology import SymbolAuthority
from serenity_types.utils.serialization import CamelModel


class AssetType(Enum):
    """
    Simple classification of assets.
    """

    CURRENCY = 'CURRENCY'
    """
    Fiat currency, e.g. EUR.
    """

    TOKEN = 'TOKEN'
    """
    Generic tokenized assets.
    """

    PEGGED_TOKEN = 'PEGGED_TOKEN'
    """
    A tokenized asset whose price is linked to an exposure.
    """

    WRAPPED_TOKEN = 'WRAPPED_TOKEN'
    """
    A tokenized asset which represents a claim on a token, typically on another Network.
    """

    FUTURE = 'FUTURE'
    """
    An exchange-listed futures contract.
    """

    LISTED_OPTION = 'LISTED_OPTION'
    """
    An exchange-listed option.
    """

    OTC_OPTION = 'OTC_OPTION'
    """
    An OTC option contract.
    """

    INDEX = 'INDEX'
    """
    A basket of other assets.
    """

    STRATEGY = 'STRATEGY'
    """
    A multi-leg asset composed of positions in other assets.
    """


class Asset(CamelModel):
    """
    Base class for all financial assets tracked in Serenity.
    """

    asset_id: UUID
    """
    Unique, immutable ID for this asset. Symbols can change over time,
    but asset ID's are stable.
    """

    asset_type: AssetType
    """
    Basic classification of this asset. Based on the type, sub-classes of
    the Asset may carry additional details.
    """

    symbol: str
    """
    Serenity's unique symbol for this asset, e.g. tok.usdc.ethereum.
    """

    native_symbol: Optional[str]
    """
    Whatever is the issuer's symbol for this asset. For tokens this is typically the token smart contract symbol
    or native blockchain token symbol, e.g. ETH or DAI.
    """

    display_name: str
    """
    Human-readable name for this asset.
    """


class XRefSymbol(CamelModel):
    """
    Legacy representation of a cross-reference symbol for an AssetSummary.
    """

    authority: SymbolAuthority
    """
    Symbology for which this symbol is authoritative, e.g. COINGECKO or SEDOL.
    """

    symbol: str
    """
    String symbol in the given symbology as of the effective date loaded.
    Note the vendor symbols can and do change over time, so this should
    be mapped to a Serenity asset ID using inputs from the same day.
    """


class AssetSummary(CamelModel):
    """
    Flattened, lowest common denominator representation of assets. This is to
    support the legacy Refdata API, which only handled TOKEN and CURRENCY.
    We will be replacing this with a richer mechanism going forward.
    """
    asset_id: UUID
    """
    Serenity's unique internal identifier for this asset. This never changes.
    """

    asset_type: AssetType
    """
    Serenity's classification for this asset, e.g. TOKEN or CURRENCY.
    """

    asset_symbol: str
    """
    Serenity's human-readable symbol for this asset. This identifier may change.
    """

    native_symbol: str
    """
    The blockchain, listing exchange or other primary authority's symbol, e.g. BTC.
    """

    display_name: str
    """
    Serenity's human-readable display name for this asset, e.g. Bitcoin.
    """

    xref_symbols: List[XRefSymbol]
    """
    """
