from datetime import date, datetime
from enum import Enum
from typing import List, Optional
from uuid import UUID

from serenity_types.utils.serialization import CamelModel


class CurveUsage(Enum):
    """
    Intended usage of this curve, e.g. for discounting or for projection purposes.
    """

    DISCOUNTING = "DISCOUNTING"
    """
    Curve points for discounting future cashflows.
    """

    PROJECTION = "PROJECTION"
    """
    Curve points indicating the market forward view.
    """


class RateSourceType(Enum):
    """
    Sources of rates & discount factors. In the most general case
    the yield curve can be built from multiple imports, so we
    tag each CurvePoint that is the input to the interpolated YC
    with the particular source, e.g. we might have an 8H rate
    at the short end from perpetual future funding rates and
    implied forwards backed out from calendar spreads.
    """

    FUTURE_PX = "FUTURE_PX"
    """
    Implied forward backed out from observed future prices.
    """

    OPTION_PX = "OPTION_PX"
    """
    Implied forward backed out from observed option prices & spreads.
    """

    FIXING = "FIXING"
    """
    Observed traditional rate fixings.
    """

    FUNDING_RATE = "FUNDING_RATE"
    """
    Observed exchange perpetual future funding rate.
    """

    LENDING_RATE = "LENDING_RATE"
    """
    Observed CeFi / OTC or DeFi lending rate.
    """

    STAKING_RATE = "STAKING_RATE"
    """
    Observed proof-of-stake protocol staking rate.
    """


class InterpolationMethod(Enum):
    """
    Specific interpolation method used. Currently only supports flat-forward.
    """
    FLAT_FWD = "FLAT_FWD"


class CurvePoint(CamelModel):
    """
    A discrete input point on the curve, with all the metadata describing
    what is being provided and its source to help reproduce the results.
    """

    tenor: Optional[str]
    """
    A relative date code, e.g. 1Y or 3M.
    """

    pillar_date: Optional[date]
    """
    The specific forward date for the given rate and DF, e.g. the 1W point for today would be the next
    business day a week ahead.
    """

    duration: Optional[float]
    """
    The duration for this point, expressed as a year fraction.
    """

    rate_source_type: RateSourceType
    """
    The type of input being provided for this CurvePoint, e.g. if it's from a 3M future,
    this would be FUTURE_PX, while if it's from traditional rates fixings, it would be FIXINGS.
    """

    rate_sources: Optional[List[str]]
    """
    The specific rate sources used, e.g. OIS, SOFR or LIBOR; for LENDING_RATE, DeFi or other sources
    used, e.g. CHAINLINK, IPOR or AAVE. For FUNDING_RATE this holds the UUID for the exchange Organization ID.
    """

    reference_assets: Optional[List[UUID]]
    """
    In the case where an implied forward is backed out from market observables, the assets observed.
    """

    mark_prices: Optional[List[float]]
    """
    In the case where a DF is backed out from the implied forward of a reference asset or basket thereof,
    the observed prices that should go into the bootstrapping method.
    """

    rate: float
    """
    The input rate value, if DF not provided.
    """

    discount_factor: float
    """
    The input DF value, if rate not provided.
    """


class YieldCurveDefinition(CamelModel):
    """
    A uniquely-identified set of YC parameters for bootstrapping a YieldCurve.
    """

    yield_curve_id: UUID
    """
    Unique ID for this particular combination of yield curve attributes; note yield curves are
    bootstrapped daily, and so there are going to be many versions over time.
    """

    curve_usage: CurveUsage
    """
    The curve's intended purpose, e.g. for discounting or representing market view on forward rates.
    """

    interpolation_method: InterpolationMethod
    """
    The specific interpolator type used to bootstrap this curve.
    """

    rate_source_type: RateSourceType
    """
    The type of input being provided for this CurvePoint, e.g. if it's from a 3M future,
    this would be FUTURE_PX, while if it's from traditional rates fixings, it would be FIXINGS.
    """

    underlier_asset_id: UUID
    """
    The linked asset for this curve, e.g. for an Ethereum staking curve, this would be ETH (tok.eth.ethereum).
    Note we will be switching to the Exposure UUID instead in a future release (e.g. tok.eth), once the
    reference data is available.
    """

    display_name: str
    """
    Human-readable description of this curve, e.g. OIS (FLAT_FWD)
    """


class YieldCurveAvailability(CamelModel):
    """
    Information about version availability for a given YC definition.
    """

    definition: YieldCurveDefinition
    """
    Description of the particular yield curve parameters that are available to load.
    """

    as_of_times: List[datetime]
    """
    The list of all available as_of_times in the requested window.
    """


class RawYieldCurve(CamelModel):
    """
    A term structure of yield curve inputs. The RAW representation is offered to clients so they
    can either do their own interpolation or for diagnostics.
    """

    points: List[CurvePoint]
    """
    The list of market data observations that went into this raw yield curve, e.g. rates, discount factors
    and futures prices corresponding to various tenors.
    """


class InterpolatedYieldCurve(CamelModel):
    """
    A term structure of rates and discount factors built from a RAW representation. This is the version
    that you should pass in for option valuation purposes, and is suitable for extracting rates and discount
    factors as well as plotting purposes.
    """

    definition: YieldCurveDefinition
    """
    The unique set of parameters used to bootstrap this yield curve.
    """

    durations: List[float]
    """
    Array of all durations along the curve, as year fractions.
    """

    rates: List[float]
    """
    Array of all interpolated rates along the curve.
    """

    discount_factors: List[float]
    """
    Array of all discount factors (DF's) along the curve.
    """


class YieldCurveVersion(CamelModel):
    """
    A single version of a YieldCurveDefinition, inclusive of its raw and interpolated YC content.
    """

    raw: RawYieldCurve
    """
    The raw yield curve input.
    """

    interpolated: InterpolatedYieldCurve
    """
    The bootstrapped yield curve.
    """

    as_of_time: datetime
    """
    The time window, generally UTC midnight, for which we have bootstrapped this yield curve; latest rates / input
    prices as of this time are used.
    """

    build_time: datetime
    """
    The actual time of the build; due to DQ or system issues this might be different from as_of_time.
    """
