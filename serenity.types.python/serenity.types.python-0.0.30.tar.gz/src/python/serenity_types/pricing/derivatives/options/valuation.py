from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import validator

from serenity_types.pricing.derivatives.options.volsurface import (
    InterpolatedVolatilitySurface, VolModel, DiscountingMethod, ProjectionMethod
)
from serenity_types.pricing.derivatives.rates.yield_curve import InterpolatedYieldCurve
from serenity_types.refdata.options import OptionStyle, OptionType
from serenity_types.utils.serialization import CamelModel


class MarketDataOverride(CamelModel):
    """
    Helper type for representing replacements and bumps for market data inputs in pricing.
    """

    replacement: Optional[float]
    """
    Replacement value for the given market data point.
    """

    additive_bump: Optional[float]
    """
    A value (potentially negative) to add the observed value from stored or live market data.
    """

    @validator('replacement', always=True)
    def check_bump_or_replace_but_not_both(cls, replacement, values):
        if values.get('additive_bump') and replacement:
            raise ValueError("Please specify only one of 'replacement' or 'additive_bump'")
        return replacement


class YieldCurveOverride(CamelModel):
    """
    Helper for representing explicitly either override by UUID (load that YieldCurveDefinition
    from the database for the appropriate as_of_time) or by value. The client can also specify
    mutations to make to this input market data. In the case where you want to replace the
    rate entirely do not specify either yield_curve_id or yield_curve; in the case where you
    want to do a shift of the yield curve, specify either ID or curve and then an additive_bump.
    Everything null or both yield_curve_id and yield_curve specified yields validation errors.
    """

    yield_curve_id: Optional[UUID]
    """
    Optionally specifies a supported YieldCurveDefinition UUID from the database. Not every
    definition is accepted, e.g. you cannot pass in a CurveUsage.PROJECTION curve for discounting.
    """

    yield_curve: Optional[InterpolatedYieldCurve]
    """
    Optionally specifies a supported yield curve bootstrapped by the client or loaded separately. Not every
    definition is accepted, e.g. you cannot pass in a CurveUsage.PROJECTION curve for discounting.
    """

    rate_override: Optional[MarketDataOverride]
    """
    Optionally modifies the input data. Note properly you should not need to both provide a yield_curve
    and modify it, but in case clients want to play back our stored yield_curve via API without
    having to mutate the curve themselves, it could make sense.
    """

    @validator('yield_curve', always=True)
    def check_yield_curve_ids_or_yield_curve(cls, yield_curve, values):
        if values.get('yield_curve_id') and yield_curve:
            raise ValueError("Please specify only one of 'yield_curve_id' or 'yield_curve'")
        return yield_curve


class OptionValuation(CamelModel):
    """
    A collection of option economics and market data overrides used to describe a single option valuation
    requested from the service. This is intentionally meant to support both listed contract pricing and
    more general pricing of option economics. For market data, everything is defaulted, but the client can
    override or bump (shift) any of the inputs to get the exact pricing scenario desired.
    """

    option_valuation_id: str
    """
    Correlation ID to use for this requested option valuation. If pricing based on a listed contract
    with optionAssetId, by convention the unique ID or symbol of that option should be used.
    """

    qty: Optional[int] = 1
    """
    Number of option contracts; used when computing the spot notional of the option position. If you take
    the default every scaled value (e.g. spot_notional, delta_ccy) will be a unit notional value.
    """

    option_asset_id: Optional[UUID]
    """
    Look up all option economics based on the unique ID of a specific listed option contract.
    """

    underlier_asset_id: Optional[UUID]
    """
    Serenity asset identifier of the underlier, e.g. BTC (tok.btc.bitcoin). Not required if optionAssetId provided.
    Note we will be switching to the Exposure UUID instead in a future release (e.g. tok.btc), once the reference
    data is available.
    """

    strike: Optional[float]
    """
    Absolute value of the strike. Not required if optionAssetId provided. In future we may wish to support different
    StrikeType representations here, but some cases (like DELTA) are potentially trickier, so not for initial version.
    """

    expiry: Optional[datetime]
    """
    Expiration expressed in absolute terms as a date/time. Not required if optionAssetId provided
    """

    option_type: Optional[OptionType]
    """
    Whether we are pricing a PUT or CALL option.
    """

    option_style: Optional[OptionStyle] = OptionStyle.EUROPEAN
    """
    The variety of option being priced. Our pricer only supports EUROPEAN at this time, so defaults accordingly.
    """

    contract_size: Optional[float] = 1
    """
    For scaling purposes, the # of underlying per contract. Only used if option_asset_id is not set, otherwise it's
    loaded from the contract specification in the database.
    """

    implied_vol_override: Optional[MarketDataOverride]
    """
    Replace or modify the stored volatility surface's IV for this option.
    """

    spot_price_override: Optional[MarketDataOverride]
    """
    Replace or modify the stored or observed spot price used when pricing this option.
    """


class OptionValuationRequest(CamelModel):
    """
    A batch request to run one or more option valuations using a single model configuration and base
    set of curves and the vol surface. Reasonable defaults will be provided for any missing inputs, e.g.
    if you price a set of Deribit BTC options, the latest BTC volatility surface will be used along with
    the latest discounting curves for BTC and USD. Note that because the request only references a single
    volatility surface this means all included options must have the same underlier as the one in
    VolatilitySurfaceVersion.interpolated.definition.underlier_asset_id.
    """

    as_of_time: Optional[datetime]
    """
    The as-of time to use for loading all marketdata, surfaces, yield curves and refdata from the database.
    Defaulted to the latest up to this time.
    """

    model_config_id: Optional[UUID]
    """
    The specific derivatives analytics model configuration to load; this is used to drive defaults.
    """

    base_currency_id: Optional[UUID]
    """
    Base currency to use for expressing all notional values. Defaults to USD.
    """

    discounting_method: Optional[DiscountingMethod] = DiscountingMethod.SELF_DISCOUNTING
    """
    How to derive the discount rate: from the projection rate (self-discounting),
    or from pre-built discounting curves either provided in API or loaded from the system.
    """

    projection_method: Optional[ProjectionMethod]
    """
    How to derive the projection rate when in real-time mode: from live futures prices, or from a curve.
    The default depends on as_of_time. In the case of as_of_time being None the system runs in real-time
    pricing mode and uses ProjectionMode.FUTURES. When as_of_time is provided the system runs in historical
    pricing mode and defaults to ProjectionMode.CURVE. Setting both as_of_time and ProjectionMode.FUTURES
    will yield a validation error from the API.
    """

    vol_surface_id: Optional[UUID]
    """
    The optional unique ID of the surface to load, latest version as-of the as_of_time.
    """

    vol_surface: Optional[InterpolatedVolatilitySurface]
    """
    The optional client-provided volatility surface to use. If the client provides neither a VS ID
    nor their own volatility surface, the system will load the default for the underlying as-of the as_of_time.
    """

    discounting_curve_override: Optional[YieldCurveOverride]
    """
    Various forms of modifications to the discounting curve: choosing a variant in the database; passing
    in a complete curve by value; and/or replacing or shifting the extracted rate.
    """

    projection_curve_override: Optional[YieldCurveOverride]
    """
    Various forms of modifications to the projection curve: choosing a variant in the database; passing
    in a complete curve by value; and/or replacing or shifting the extracted rate.
    """

    vol_model: Optional[VolModel] = VolModel.SVI
    """
    The volatility model used for valuation purposes.
    """

    options: List[OptionValuation]
    """
    The full set of option valuations to run with the given market data inputs. The client may provide
    individual overrides or bumps for all inputs as part of each valuation object.
    """

    @validator('vol_surface', always=True)
    def check_vol_surface_id_or_vol_surface(cls, vol_surface, values):
        if values.get('vol_surface_id') and vol_surface:
            raise ValueError("Please specify only one of 'vol_surface_id' or 'vol_surface'")
        return vol_surface

    @validator('options', always=False)
    def check_non_empty_options_list(cls, options, values):
        if len(options) == 0:
            raise ValueError("Please provide at least one option in 'options'")
        return options


class OptionValuationResult(CamelModel):
    """
    The result of a series of option valuations based on the parameters in the OptionValuationRequest.
    Note that the basic calculation is just Black-Scholes, but if you provide additional information
    regarding the position scaling it will also provide position notional and greek exposures
    in base currency to allow bucketing of greeks and NAV calculations.
    """

    option_valuation_id: str
    """
    Correlation ID for the original OptionValuation.
    """

    vol_model: VolModel
    """
    The specific volatility model used; as SVI calibrations yield different greeks, this needs to be explicit.
    """

    pv: float
    """
    Present value (PV) a.k.a. theoretical price or theo.
    """

    iv: float
    """
    Implied volatility (IV)
    """

    spot_notional: float
    """
    The base currency notional of the position: number of contracts (qty) X  spot_price X contract_size.
    """

    spot_price: float
    """
    Input spot price for this valuation.
    """

    forward_price: float
    """
    Input forward price for this valuation.
    """

    projection_rate: float
    """
    The projection rate used when computing the forward.
    """

    discounting_rate: float
    """
    The discounting rate used when computing the forward; equal to projection_rate with SELF_DISCOUNTING.
    """

    delta: float
    """
    Greek output: delta, the option's sensitivity to spot changes.
    """

    delta_qty: float
    """
    Delta X qty X contract_size, the delta exposure expressed in qty of underlying.
    """

    delta_ccy: float
    """
    Delta X value, a.k.a. the partial derivative of position value with respect to spot,
    expressed in base currency
    """

    gamma: float
    """
    Greek output: gamma, the delta's sensitivity to spot changes.
    """

    gamma_ccy: float
    """
    Gamma X value^2, a.k.a. the second derivative of position value with respect to spot,
    expressed in base currency.
    """

    vega: float
    """
    Greek output: vega, the option's sensitivity to volatility changes.
    """

    vega_ccy: float
    """
    Partial derivative of the position value of the contract with respect to vega X 1%, expressed in base currency.
    """

    rho: float
    """
    Greek output: rho, the delta's sensitivity to interest rate changes.
    """

    rho_ccy: float
    """
    Partial derivative of the spot notional value of the contract with respect to rho X 1bp, expressed in base currency.
    """

    theta: float
    """
    Greek output: theta, the delta's sensitivity to time decay.
    """

    theta_ccy: float
    """
    Partial derivative of the spot notional value of the contract with respect to theta X 1 day,
    expressed in base currency.
    """
