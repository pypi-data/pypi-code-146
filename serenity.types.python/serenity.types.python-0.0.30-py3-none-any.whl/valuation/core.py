from typing import Dict, List

from serenity_types.portfolio.core import AssetPosition
from serenity_types.pricing.core import PricingContext
from serenity_types.utils.serialization import CamelModel


class PositionValue(CamelModel):
    """
    Value of a single position in the portfolio.
    """

    value: float
    """
    The value of this position in base currency, e.g. qty * price for simple asset types.
    """

    price: float
    """
    The price for this position according to the chosen mark time.
    """

    qty: float
    """
    The quantity of assets, e.g. 0.7 BTC.
    """

    weight: float
    """
    The weight of this position in the overall portfolio, as a fraction, e.g. 0.12.
    This is just the position's value divided by the portfolio value.
    """


class PositionValuation(CamelModel):
    """
    Close, previous and current values of a single position in the portfolio.
    """

    close: PositionValue
    """
    The value of the asset at the MarkTime, as of the most recent close.
    """

    previous: PositionValue
    """
    The value of the asset at the MarkTime, as of the previous close.
    """

    current: PositionValue
    """
    The value of the position as of the current moment. Requires real-time
    data that will be connected in Q1'23.
    """


class PortfolioValue(CamelModel):
    """
    Total value of the portfolio as of a certain time.
    """

    net_holdings_value: float
    """
    The sum of the values of all non-cash positions.
    """

    gross_holdings_value: float
    """
    The sum of the absolute values of all non-cash positions.
    """

    cash_position_value: float
    """
    The fiat position or stablecoin equivalent based on settings determining whether stablecoins count as cash.
    """

    net_asset_value: float
    """
    NAV, i.e. net_position_value + cash_position_value.
    """


class PortfolioValuationRequest(CamelModel):
    """
    Request to do a NAV calculation for a portfolio. This is simple right now,
    but once we support non-linear assets we will need to extend it.
    """

    portfolio: List[AssetPosition]
    """
    Basic, moment-in time image of the portfolio to be valued.
    """

    pricing_context: PricingContext
    """
    Common settings related to how to value the portfolio, e.g. which prices to load.
    """


class PortfolioValuationResponse(CamelModel):
    """
    Response with the value of the portfolio at top level plus all position values.
    """

    pricing_context: PricingContext
    """
    The context that was used to value this portfolio. DEPRECATED, not needed.
    """

    close: PortfolioValue
    """
    The value of the whole portfolio as of the most recent close date.
    """

    previous: PortfolioValue
    """
    The value of the whole portfolio as of the previous close date.
    """

    positions: Dict[str, PositionValue]
    """
    The values of each of the individual positions in the portfolio keyed by asset UUID.
    """
