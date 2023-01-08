from datetime import date
from typing import List, Optional
from uuid import UUID

from serenity_types.portfolio.core import AssetPosition
from serenity_types.pricing.core import MarkTime
from serenity_types.utils.serialization import CamelModel


class VaRAnalysisRequest(CamelModel):
    """
    A request to compute VaR (Value at Risk) for a single portfolio using a given model.
    """

    as_of_date: Optional[date]
    """
    UTC date for the analysis; default to today.
    """

    horizon_days: Optional[int]
    """
    Loss forecast horizon in days, defaults to 1 day; it is used to scale single day
    VaR by sqrt(horizonDays). Must be positive.
    """

    lookback_period: Optional[int]
    """
    Length of price time series data used to calibrate VaR, measured in days;
    defaults to 365 days.
    """

    mark_time: Optional[MarkTime]
    """
    Enum for close timestamp to use for prices; defaults to NY_EOD.
    """

    base_currency_id: Optional[UUID]
    """
    Base currency to report absolute VaR numbers in, defaults to USD.
    """

    quantiles: Optional[List[float]]
    """
    Loss forecast quantiles used in VaR calculation; defaults to [95, 97.5, 99],
    and must be both unique and > 0 and < 100.
    """

    portfolio: List[AssetPosition]
    """
    The portfolio to analyze.
    """

    model_config_id: UUID
    """
    The specific VaR model ID to use from the repository based on model configuration identifiers from [ModelOps API.
    """


class VaRQuantile(CamelModel):
    """
    Absolute and relative VaR results for a single VaR forecast quantile, e.g. 99%.
    """

    quantile: float
    """
    VaR forecast quantile, e.g. 99 (expressed as percent).
    """

    var_absolute: float
    """
    VaR level (forecasted portfolio loss) in base ccy.
    """

    var_relative: float
    """
    VaR level (forecasted portfolio loss) as a percentage of the baseline portfolio value.
    """


class VaRAnalysisResult(CamelModel):
    """
    The analysis result for a single day returns the baseline value and the various confidence
    interval values around that baseline.
    """

    run_date: date
    """
    The UTC date for which VaR was computed.
    """

    baseline: float
    """
    The value of the portfolio on the preceding day (runDate - 1).
    """

    quantiles: List[VaRQuantile]
    """
    VaR result object, one for each quantile requested.
    """

    excluded_asset_ids: List[UUID]
    """
    Assets excluded from VaR calculation due to insufficient history.
    """


class VaRBacktestRequest(CamelModel):
    """
    A request to backtest VaR (Value at Risk) for a single portfolio over a period using a given model.
    """
    start_date: date
    """
    UTC date for start of analysis run.
    """

    end_date: Optional[date]
    """
    UTC date for end of analysis run, inclusive; default to yesterday.
    """

    lookback_period: Optional[int]
    """
    Length of price time series data used to calibrate VaR, measured in days;
    defaults to 365 days for one year lookback.
    """

    mark_time: Optional[MarkTime]
    """
    Enum for close timestamp to use for prices; defaults to NY_EOD.
    """

    base_currency_id: Optional[UUID]
    """
    Base currency to report absolute VaR numbers in, defaults to USD.
    """

    quantiles: Optional[List[float]]
    """
    Loss forecast quantiles used in VaR calculation; defaults to [95, 97.5, 99],
    and must be both unique and > 0 and < 100.
    """

    portfolio: List[AssetPosition]
    """
    The portfolio to backtest.
    """

    model_config_id: UUID
    """
    The specific VaR model ID to use from the repository based on model configuration identifiers from [ModelOps API.
    """


class VaRBreach(CamelModel):
    """
    Information about a day when the portfolio loss exceeded the VaR forecasted level in a backtest.
    """

    breach_date: date
    """
    Aate when portfolio loss exceeds VaR forecasted level.
    """

    portfolio_loss_absolute: float
    """
    Portfolio loss on breachDate in base ccy.
    """

    portfolio_loss_relative: float
    """
    Portfolio loss on breach_date as a percentage of the baseline value.
    """

    quantiles: List[VaRQuantile]
    """
    VaR levels (absolute & relative) for all breaches this date.
    """


class VaRBacktestResult(CamelModel):
    """
    The result of a full VaR backtest of a portfolio.
    """

    results: List[VaRAnalysisResult]
    """
    VaR computed results for every day in the backtest.
    """

    breaches: List[VaRBreach]
    """
    Days when the portfolio loss exceeded the VaR forecasted level in a backtest.
    """
