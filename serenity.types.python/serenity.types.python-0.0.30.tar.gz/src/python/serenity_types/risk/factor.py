from datetime import date
from typing import List, Optional
from uuid import UUID

from serenity_types.portfolio.core import AssetPosition
from serenity_types.pricing.core import MarkTime
from serenity_types.utils.serialization import CamelModel


class AssetFactorExposureMatrixElement(CamelModel):
    """
    A single element from the matrix of asset factor exposures, for one day.
    """

    asset_id: UUID
    """
    The unique ID of the asset from the portfolio.
    """

    factor: str
    """
    The name of the factor from the risk model, e.g. Momentum.
    """

    value: float
    """
    Factor loading for the given factor-asset pair (betas from the regression).
    """


class AssetFactorIndexWeight(CamelModel):
    """
    A single entry in a factor portfolio index, with the asset's weight in the portfolio.
    """

    asset_id: UUID
    """
    The unique ID of the asset from the portfolio.
    """

    weight: float
    """
    signed weight (long or short) of this asset in the factor index; this is a fraction, e.g. 0.25 for 25%.
    For long-only they sum to 1.0 and for long-short they sum to 0.0 in the current methodology.
    """


class AssetMatrixElement(CamelModel):
    """
    A single cell in an asset-asset matrix, e.g. a covariance matrix.
    """

    asset_id1: UUID
    """
    First unique asset ID in the pair.
    """

    asset_id2: UUID
    """
    Second unique asset ID in the pair.
    """

    value: float
    """
    Matrix cell value, e.g. correlation.
    """


class AssetResidualValue(CamelModel):
    """
    A single entry in a list of asset residuals from the covariance matrix.
    """

    asset_id: UUID
    """
    Unique asset ID being referenced.
    """

    value: float
    """
    Asset residual covariance value.
    """


class Risk(CamelModel):
    """
    Common triplet for risk measures used across the API.
    """
    factor_risk: float
    """
    The volatility or variance explained by the factor risk model.
    """

    specific_risk: float
    """
    The volatility or variance not explained by the model.
    """

    total_risk: float
    """
    The total volatility or variance along the measured dimension.
    """


class AssetRisk(Risk):
    """
    This object supports the “Breakdown” view By Asset as well as the sector breakdowns.
    """

    asset_id: UUID
    """
    The unique asset ID for the asset break-down of risk.
    """

    sector_levels: List[str]
    """
    A list of sector level names that identifies a “path” to a particular level in the sector taxonomy,
    as defined above; however, in this instance, this is the fully-qualified path to this particular asset,
    i.e. the leaf level.
    """


class FactorExposureValue(CamelModel):
    """
    A decimal or base currency exposure to a risk factor.
    """

    factor_exposure: float
    """
    Asset-level factor loading.
    """

    factor_exposure_base_ccy: float
    """
    The factor exposure expressed in base currency terms.
    """


class FactorReturn(CamelModel):
    """
    A single daily return for a factor portfolio.
    """
    factor: str
    """
    Name of the factor from the risk model, e.g. Momentum.
    """
    close_date: date

    value: float
    """
    Daily return for this particular factor on the given close date.
    """


class FactorMatrixElement(CamelModel):
    """
    A single cell in a factor-factor matrix, e.g. factor covariance.
    """
    factor1: str
    """
    Name of the first factor from the risk model, e.g. Momentum
    """

    factor2: str
    """
    Name of the second factor from the risk model, e.g. Size.
    """

    value: float
    """
    Matrix cell value, e.g. a covariance or a correlation.
    """


class RiskAttributionRequest(CamelModel):
    """
    Request to run a risk attribution on the given portfolio.
    """

    as_of_date: Optional[date]
    """
    UTC date midnight; default to latest, as yyyy-mm-dd.
    """

    portfolio: List[AssetPosition]
    """
    Portfolio constituents to analyze.
    """

    model_config_id: Optional[UUID]
    """
    A reference to a factor risk model configuration from [ModelOps API, e.g. a specific parameterization
    of SFRMv1; if not specified then the system will select the most appropriate model.
    """

    sector_taxonomy_id: Optional[UUID]
    """
    References a taxonomy UUID from the Refdata API, specifically the getSectorTaxonomies call; defaults to DACS.
    """

    mark_time: Optional[MarkTime]
    """
    Time to use for close, defaults to MarkTime.NY_EOD.
    """

    base_currency_id: Optional[UUID]
    """
    Base currency for value reporting, defaults to USD.
    """

    strict: Optional[bool] = False
    """
    Should the request fail if there are any warnings?
    """


class SectorLevelRisk(Risk):
    """
    This object supports the “Breakdown” views By Sector & Asset and By Sector & Factor.
    The way to think about this one is the factor, specific & total risk for each supported risk
    contribution type, absolute and marginal at each level in the sector hierarchy gets one of these objects.
    """

    sector_levels: List[str]
    """
    A list of sector level names that identifies a “path” to a particular level in the sector taxonomy; as many of the
    risk values are non-additive, the output must provide every level explicitly, e.g.
    ['Sector A'], ['Sector A', 'Sub-sector A'] and ['Sector A', 'Sub-sector A', 'Industry A'] would
    all be in the by_sector array.
    """


class RiskBreakdown(CamelModel):
    """
    Collection of dimensions along which risk can be broken down.
    """

    by_sector: List[SectorLevelRisk]
    """
    The risk values at each level in the sector hierarchy for all of the sectors represented in the portfolio
    for the given risk measure, e.g. absolute vs. relative risk.
    """

    by_asset: List[AssetRisk]
    """
    The risk values for all of the assets in the portfolio for the given risk measure, e.g. absolute vs. relative risk.
    """


class SectorFactorExposure(CamelModel):
    """
    This object supports breaking down risk by sector and factor.
    """

    factor: str
    """
    Name of the factor from the risk model, e.g. Momentum.
    """

    sector_levels: List[str]
    """
    A list of sector level names that identifies a “path” to a particular level in the
    sector taxonomy, as defined above.
    """

    absolute_risk: float
    """
    Absolute contribution of this factor to the portfolio's overall volatility,
    i.e. the total amount of volatility attributable to this factor.
    """

    relative_risk: float
    """
    Relative contribution of this factor to the portfolio's overall volatility,
    i.e. the fraction of the volatility attributable to this factor.
    """

    marginal_risk: float
    """
    Marginal contribution of this factor to the portfolio's overall volatility,
    i.e. how much additional exposure to this factor would increase the volatility
    """

    factor_exposure: FactorExposureValue
    """
    The exposure at this hierarchy level to this factor.
    """


class TotalFactorRisk(CamelModel):
    """
    This object supports the Breakdown view By Factor, which shows the portfolio-level
    factor risk contributions and exposures.
    """

    factor: str
    """
    Name of the factor from the risk model, e.g. Momentum.
    """

    absolute_contribution: float
    """
    Absolute contribution of this factor to the portfolio's overall volatility,
    i.e. the total amount of volatility attributable to this factor
    """

    relative_contribution: float
    """
    Relative contribution of this factor to the portfolio's overall volatility,
    i.e. the fraction of the volatility attributable to this factor
    """

    marginal_contribution: float
    """
    Marginal contribution of this factor to the portfolio's overall volatility,
    i.e. how much would additional exposure to this factor increase the volatility
    """

    factor_exposure: FactorExposureValue
    """
    The exposure of the whole portfolio to this factor.
    """


class TotalRisk(CamelModel):
    """
    This object, returned at the top level, gives you a summary of the factor, specific and total risk expressed
    in both volatility and variance for the whole portfolio.
    """
    volatility: Risk
    """
    Factor, specific and total volatility of the portfolio.
    """

    variance: Risk
    """
    Factor, specific and total variance of the portfolio.
    """


class RiskAttributionResponse(CamelModel):
    """
    Consolidated response for a single risk attribution run using a factor risk model.
    """

    total_risk: TotalRisk
    """
    Portfolio risk in volatility and variance terms; volatility is non-additive, so factor and specific
    volatility do not sum to total volatility, but variance does.
    """

    absolute_contribution_risk: RiskBreakdown
    """
    Sector and asset absolute contribution to the volatility of the portfolio; cross-check sums by asset to equal
    total factor, specific and total volatility for all assets.
    """

    relative_contribution_risk: RiskBreakdown
    """
    Sector and asset relative contribution to the variance of the portfolio; cross-check sums by asset to equal
    total factor and specific variance divided by total variance.
    """

    asset_marginal_risk: List[AssetRisk]
    """
    By-asset marginal weighted contribution of volatility to the portfolio.
    """

    factorRisk: List[TotalFactorRisk]
    """
    By-factor absolute, relative and marginal contribution to risk, as well as the portfolio’s exposure to each factor.
    """

    sectorFactorExposures: List[SectorFactorExposure]
    """
    Aggregations of factor exposure by factor and sector.
    """
