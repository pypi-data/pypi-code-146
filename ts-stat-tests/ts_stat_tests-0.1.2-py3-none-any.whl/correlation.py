from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
from statsmodels.regression.linear_model import RegressionResults
from statsmodels.stats.api import acorr_breusch_godfrey
from statsmodels.stats.api import acorr_ljungbox
from statsmodels.stats.api import acorr_lm
from statsmodels.stats.diagnostic import ResultsStore
from statsmodels.tools.validation import array_like
from statsmodels.tsa.api import acf as st_acf
from statsmodels.tsa.api import ccf as st_ccf
from statsmodels.tsa.api import pacf as st_pacf
from typeguard import typechecked


__all__ = ["acf", "pacf", "ccf", "alb", "alm", "abg"]


@typechecked
def acf(
    x: array_like,
    adjusted: bool = False,
    nlags: int = None,
    qstat: bool = False,
    fft: bool = True,
    alpha: float = None,
    bartlett_confint: bool = True,
    missing: str = "none",
) -> Union[np.ndarray, Tuple[Union[np.ndarray, Optional[np.ndarray]]]]:
    return st_acf(
        x=x,
        adjusted=adjusted,
        nlags=nlags,
        qstat=qstat,
        fft=fft,
        alpha=alpha,
        bartlett_confint=bartlett_confint,
        missing=missing,
    )


@typechecked
def pacf(
    x: array_like, nlags: int = None, method: str = "ywadjusted", alpha: float = None
) -> Union[np.ndarray, Tuple[Union[np.ndarray, Optional[np.ndarray]]]]:
    return st_pacf(x=x, nlags=nlags, method=method, alpha=alpha)


@typechecked
def ccf(
    x: array_like, y: array_like, adjusted: bool = True, fft: bool = True
) -> np.ndarray:
    return st_ccf(x=x, y=y, adjusted=adjusted, fft=fft)


def alb(
    x=array_like,
    lags: Union[int, array_like] = None,
    boxpierce: bool = False,
    model_df: int = 0,
    period: int = None,
    return_df: bool = True,
    auto_lag: bool = True,
) -> Tuple[Union[float, np.ndarray, None]]:
    return acorr_ljungbox(
        x=x,
        lags=lags,
        boxpierce=boxpierce,
        model_df=model_df,
        period=period,
        return_df=return_df,
        auto_lag=auto_lag,
    )


def alm(
    resid: array_like,
    nlags: int = None,
    autolag: str = None,
    store: bool = False,
    *,
    period: int = None,
    ddof: int = 0,
    cov_type: str = "nonrobust",
    cov_kwargs: dict = None
) -> Tuple[Union[float, ResultsStore]]:
    return acorr_lm(
        resid=resid,
        nlags=nlags,
        autolag=autolag,
        store=store,
        period=period,
        ddof=ddof,
        cov_type=cov_type,
        cov_kwargs=cov_kwargs,
    )


def abg(
    res: RegressionResults, nlags: int = None, store: bool = False
) -> Tuple[Union[float, ResultsStore]]:
    return acorr_breusch_godfrey(res=res, nlags=nlags, store=store)
