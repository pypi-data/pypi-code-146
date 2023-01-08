from datetime import datetime
from enum import Enum
from typing import Dict, List
from uuid import UUID

from serenity_types.utils.serialization import CamelModel


class VolModel(Enum):
    """
    Currently supported volatility models.
    """

    SVI = "SVI"
    """
    Stochastic volatility (SVI) calibrated volatility model.
    """

    BLACK_SCHOLES = "BLACK_SCHOLES"
    """
    Classic Black-Scholes volatility model.
    """


class StrikeType(Enum):
    """
    Currently supported strike representations.
    """

    ABSOLUTE = "ABSOLUTE"
    """
    Absolute value of strike, e.g. the 20000 option.
    """

    LOG_MONEYNESS = "LOG_MONEYNESS"
    """
    Relative value of strike vs. current spot with log transformation: log(strike / spot).
    """


class DiscountingMethod(Enum):
    """
    The strategy to use for deriving the discount rate, i.e. the assumed interest rate to
    use when discounting prices to present.
    """

    CURVE = "CURVE"
    """
    Extract a discount factor from discount curves, either provided via API or loaded from database.
    """

    SELF_DISCOUNTING = "SELF_DISCOUNTING"
    """
    Use the base asset's projection rate as the discount rate instead of a discount curve.
    This is the default, and the option you should choose if you want to reproduce the Deribit
    forward pricing model.
    """


class ProjectionMethod(Enum):
    """
    The strategy to use for deriving the projection rates, i.e. the forward interest rates.
    """

    CURVE = "CURVE"
    """
    Projection rate is extracted from a projection curve, either provided via API or loaded from database.
    This option is respected in both real-time pricing and historical pricing modes, though in real-time
    the curve version loaded is always the very latest. Select CURVE if you want a more stable forward.
    """

    FUTURES = "FUTURES"
    """
    Projection rate is snapped from the corresponding Deribit futures prices; this option is only
    supported in real-time pricing mode. Select FUTURES if in real-time you want to reproduce
    Deribit forward pricing model and incorporate up-to-the-moment market view on the forward.
    """


class VolatilitySurfaceDefinition(CamelModel):
    """
    A uniquely-identified set of VS parameters for fitting a VolatilitySurface.
    """

    vol_surface_id: UUID
    """
    Unique ID for this volatility surface's collection of attributes; note that surfaces
    are re-fitted hourly, and so there are going to be many versions over time.
    """

    vol_model: VolModel
    """
    Volatility model used for this surface.
    """

    strike_type: StrikeType
    """
    Strike representation used for this surface, e.g. ABSOLUTE or LOG_MONEYNESS.
    """

    underlier_asset_id: UUID
    """
    The linked asset for this surface, e.g. for a Bitcoin volatility surface, this is BTC (tok.btc.bitcoin).
    Note we will be switching to the Exposure UUID instead in a future release (e.g. tok.btc), once the
    reference data is available.
    """

    display_name: str
    """
    Human-readable description of this curve, e.g. Deribit BTC (SVI, ABSOLUTE)
    """


class VolatilitySurfaceAvailability(CamelModel):
    """
    Information about version availability for a given volsurface definition.
    """

    definition: VolatilitySurfaceDefinition
    """
    Description of the particular volsurface parameters that are available to load.
    """

    as_of_times: List[datetime]
    """
    The list of all available as_of_times in the requested window.
    """


class VolPoint(CamelModel):
    """
    An individual IV input point.
    """

    option_asset_id: UUID
    """
    The specific option that was used for vol fitting purposes.
    """

    time_to_expiry: float
    """
    The time to expiry for this point, expressed as a year fraction.
    """

    strike_value: float
    """
    Value of strike for this point, unit defined by StrikeType.
    """

    mark_price: float
    """
    The observed option premium used as input to the IV calculation.
    """

    projection_rate: float
    """
    The projection rate used when computing the forward.
    """

    discounting_rate: float
    """
    The discounting rate used when computing the forward; equal to projection_rate with SELF_DISCOUNTING,
    which is currently the default for our IV calculations.
    """

    forward_price: float
    """
    The computed forward price that went into the IV calculation.
    """

    iv: float
    """
    The computed implied volatility (IV) that corresponds to the given mark_price and other inputs.
    """


class RawVolatilitySurface(CamelModel):
    strike_type: StrikeType
    """
    Strike representation used for this surface, e.g. ABSOLUTE or LOG_MONEYNESS.
    """

    spot_price: float
    """
    The observed spot price that went into the IV calculations.
    """

    vol_points: List[VolPoint]
    """
    The discrete IV points available for fitting as a volatility surface.
    """


class InterpolatedVolatilitySurface(CamelModel):
    """
    A calibrated volatility surface with a dense grid of fitted vols. Each array
    is of equal length and corresponds to (x, y, z) for the mesh.
    """

    definition: VolatilitySurfaceDefinition
    """
    The unique set of parameters used to calibrate / fit this surface.
    """

    strikes: List[float]
    """
    All strikes expressed as log-money values, the x-axis in the mesh.
    """

    time_to_expiries: List[float]
    """
    All times to expiry expressed as year fractions, the y-axis in the mesh.
    """

    vols: List[float]
    """
    All fitted vols, the z-axis in the mesh.
    """

    input_params: Dict[str, object]
    """
    Informational set of input parameters, e.g. yield curves used for the forward. May be empty
    and keys will depend on the configuration, e.g. DiscountingType.
    """

    calibration_params: Dict[float, Dict[str, float]]
    """
    Informational set of calibration parameters, e.g. the SVI parameters. Keying is time_to_expiry
    expressed in year fractions to parameter set, where the parameter keys are VolModel-specific.
    """


class VolatilitySurfaceVersion(CamelModel):
    """
    A single version of a fitted volatility surface, with both the raw and interpolated content.
    """

    raw: RawVolatilitySurface
    """
    The raw volatility surface inputs.
    """

    interpolated: InterpolatedVolatilitySurface
    """
    The interpolated volatility surface.
    """

    as_of_time: datetime
    """
    The time window, generally top of the hour, for which we have fitted the volatility surface; latest prices
    as of this time are used as input to the surface calibration.
    """

    build_time: datetime
    """
    The actual time of the build; due to DQ or system issues this might be different from as_of_time.
    """
