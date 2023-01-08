from enum import Enum
from typing import Optional
from uuid import UUID

from serenity_types.utils.serialization import CamelModel


class ExposureType(Enum):
    COUNTERPARTY = 'COUNTERPARTY'
    """
    Bilateral exposure to a particular counterparty.
    """

    TOKEN_ISSUANCE = 'TOKEN_ISSUANCE'
    """
    Exposure to an issuance of a token.
    """

    DEBT_ISSUANCE = 'DEBT_ISSUANCE'
    """
    Exposure to an issuance of debt by a sovereign or corporate entity.
    """

    EQUITY_ISSUANCE = 'EQUITY_ISSUANCE'
    """
    Exposure to an issuance of equity by a corporate entity, whether public or private.
    """

    FIAT_ISSUANCE = 'FIAT_ISSUANCE'
    """
    Exposure to a sovereign, supranational central bank (ECB) or multinational
    organization (the IMF, for SDR).
    """


class Exposure(CamelModel):
    """
    Generic exposure to some bundle of financial risks. In multiple contexts we sometimes
    want to refer not to a specific tradable instrument but instead to the exposure. For
    instance, a centralized exchange listing DAI-USDT is not going to guarantee for you
    that the DAI tokens are specifically those issued on the Ethereum blockchain. In Serenity,
    the latter is an Asset, while the general idea of DAI, which entails exposure to everything
    issued by MakerDAO as a DAI token on any blockchain, is an Exposure. This also lets us
    express things like USDT is pegged to USD, but that doesn't necessarily mean Tether holds
    USD currency positions; it aims to track the price of the dollar. Tether is a token Exposure
    which is pegged to a fiat Exposure, USD, which may be tokenized as an asset on Ethereum
    and then held in a wallet. Considering all of this more generally, when we assess the risks
    in a portfolio, we must consider that, say, USDT on Binance is just a SQL record; it is,
    at the end of the day, a claim on Binance to get that exposure which may or may not be
    honored, just as USDT is a claim on USD exposure which is not risk-free. Even a tokenized
    USD deposit embeds a dual counterparty risk: to the smart contract, and to the bank -- yet
    we still want to express this idea that it's holding dollars and this is in theory the
    same as what you could by redeeming USDT for USD.
    """

    exposure_id: UUID
    """
    Unique identifier for this exposure.
    """

    exposure_type: ExposureType
    """
    Category of exposure.
    """

    party_org_id: Optional[UUID]
    """
    Where relevant, the legal entity / party that creates this particular
    exposure, e.g the token issuer (e.g. Circle, MakerDAO), or in the case of a counterparty
    exposure to an OTC desk, the DEALER (e.g. Galaxy Digital). In the case of
    a fiat currency exposure, the party is the soverign or, in the case of EUR, the ECB.
    """

    symbol: str
    """
    Serenity's unique symbol for this exposure, e.g. tok.usdc or ccy.usd.
    """

    display_name: str
    """
    Human-readable name for this exposure, e.g. Ethereum or U.S. Dollar.
    """

    icon_uri: Optional[str]
    """
    Optional path for loading an icon representing this exposure; typically a URL.
    """
