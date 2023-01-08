from typing import Dict
from typing import Union

import numpy as np
from pmdarima.arima.arima import ARIMA
from pmdarima.arima.auto import auto_arima
from pmdarima.arima.seasonality import CHTest
from pmdarima.arima.seasonality import OCSBTest
from scipy.stats import chi2
from statsmodels.tools.validation import array_like
from statsmodels.tools.validation import bool_like
from statsmodels.tsa.seasonal import STL
from typeguard import typechecked

from src.ts_stat_tests.correlation import acf


"""
For a really good article on CH & OCSB tests, check: [When A Time Series Only Quacks Like A Duck: Testing for Stationarity Before Running Forecast Models. With Python. And A Duckling Picture.](https://towardsdatascience.com/when-a-time-series-only-quacks-like-a-duck-10de9e165e)
"""


__all__ = ["qs", "ocsb", "ch", "seasonal_strength", "trend_strength", "spikiness"]


@typechecked
def qs(
    x: array_like,
    freq: int = 0,
    diff: bool_like = True,
    residuals: bool_like = False,
    autoarima: bool_like = True,
) -> Dict[str, Union[str, float, ARIMA, None]]:
    """
    Summary:
        Implement the `QS` Seasonality test.

    Params:
        x (array_like):
            The univariate time series data to test.
        freq (int, optional):
            The frequency of the time series data. Defaults to `0`.
        diff (bool_like, optional):
            Whether or not to run `np.diff()` over the data. Defaults to `True`.
        residuals (bool_like, optional):
            Whether or not to run & return the residuals from the function. Defaults to `False`.
        autoarima (bool_like, optional):
            Whether or not to run the `AutoARIMA()` algorithm over the data. Defaults to `True`.

    Raises:
        AttributeError:
            If `x` is empty, or `freq` is too low for the data to be adequately tested.
        ValueError:
            If, after differencing the data (by using `np.diff()`), any of the values are `None` (or `Null` or `np.nan`), then it cannot be used for QS Testing.

    Returns:
        Dict[str, Union[str,float,ARIMA,type(None)]]:
            The dictionary containing the information, attributes, and model from running the tests.

    ???+ Info "Details"
        This is a translation from the `R` language, which can be found in `qs()` function of the `seastests` package.
        For more details on the original function, see:
            - [github/seastests/qs.R](https://github.com/cran/seastests/blob/master/R/qs.R)
            - [rdrr/seastests/qs](https://rdrr.io/cran/seastests/man/qs.html)
            - [rdocumentation/seastests/qs](https://www.rdocumentation.org/packages/seastests/versions/0.15.4/topics/qs)
            - [Machine Learning Mastery/How to Identify and Remove Seasonality from Time Series Data with Python](https://machinelearningmastery.com/time-series-seasonality-with-python)
            - [StackOverflow/Simple tests for seasonality in Python](https://stackoverflow.com/questions/62754218/simple-tests-for-seasonality-in-python)

    ???+ Example "Examples"
        Basic usage:
        ```python linenums="1"
        >>> from sktime.datasets import load_airline
        >>> data = load_airline()
        >>> qs(x=data, freq=12)
        {'stat': 194.4692892087745,
         'Pval': 5.90922325801522e-43,
         'test': 'QS',
         'model': None}
        ```
        Advanced usage:
        ```python linenums="1"
        >>> from sktime.datasets import load_airline
        >>> data = load_airline()
        >>> qs(x=data, freq=12, diff=True, residuals=True, autoarima=True)
        {'stat': 101.85929391917927,
         'Pval': 7.612641184541459e-23,
         'test': 'QS',
         'model': ARIMA(order=(1, 1, 1), scoring_args={}, suppress_warnings=True)}
    """
    if x.isnull().all():
        raise AttributeError(f"All observations are NaN.")
    if diff and residuals:
        print(
            f"The differences of the residuals of a non-seasonal ARIMA model are computed and used."
            f"It may be better to either only take the differences or use the residuals."
        )
    if freq < 2:
        raise AttributeError(
            f"The number of observations per cycle is '{freq}', which is too small."
        )

    if residuals:
        if autoarima:
            max_order = 1 if freq < 8 else 3
            allow_drift = True if freq < 8 else False
            try:
                model = auto_arima(
                    y=x,
                    max_P=1,
                    max_Q=1,
                    max_p=3,
                    max_q=3,
                    seasonal=False,
                    stepwise=False,
                    max_order=max_order,
                    allow_drift=allow_drift,
                )
            except:
                try:
                    model = ARIMA(order=(0, 1, 1)).fit(y=x)
                except:
                    x = x
                    print(
                        f"Could not estimate any ARIMA model, original data series is used."
                    )
            else:
                x = model.resid()
        else:
            try:
                model = ARIMA(order=(0, 1, 1)).fit(y=x)
            except:
                x = x
                print(
                    f"Could not estimate any ARIMA model, original data series is used."
                )
            else:
                x = model.resid()
    else:
        model = None

    # Do diff
    y = np.diff(x) if diff else x

    # Pre-check
    if np.var(y[~np.isnan(y)]) == 0:
        raise ValueError(
            f"The Series is a constant (possibly after transformations)."
            f"QS-Test cannot be computed on constants."
        )

    # Test Statistic
    ## Note, ignoring `mypy` check on this line because the message is:
    ## >>> error: Invalid tuple index type (actual type "List[int]", expected type "Union[int, slice]")
    ## >>>    rho = acf(x=y, nlags=freq * 2, missing="drop")[[freq, freq * 2]]
    ## >>>                                                   ^
    ## However, the type is functionally correct... so just ignoring it.
    rho: Union[np.ndarray, Tuple[Union[np.ndarray, Optional[np.ndarray]]]] = acf(x=y, nlags=freq * 2, missing="drop")[[freq, freq * 2]]  # type: ignore
    rho = np.array([0, 0]) if any(rho <= 0) else rho
    N = len(y[~np.isnan(y)])
    QS = N * (N + 2) * (rho[0] ** 2 / (N - freq) + rho[1] ** 2 / (N - freq * 2))
    Pval = chi2.sf(QS, 2)

    return {"stat": QS, "Pval": Pval, "test": "QS", "model": model}


@typechecked
def ocsb(x: array_like, m: int, lag_method: str = "aic", max_lag: int = 3):
    return OCSBTest(
        m=m, lag_method=lag_method, max_lag=max_lag
    ).estimate_seasonal_differencing_term(x)


@typechecked
def ch(x: array_like, m: int):
    return CHTest(m=m).estimate_seasonal_differencing_term(x)


def _get_stlfit(x: array_like, m: int) -> Dict[str, Union[np.ndarray, STL]]:
    stlfit = STL(x, m, 13).fit()
    return {
        "model": stlfit,
        "trend": stlfit.trend,
        "seasonal": stlfit.seasonal,
        "residuals": stlfit.resid,
    }


def _get_stlvar(x: array_like, m: int) -> Dict[str, np.ndarray]:
    stlfit = _get_stlfit(x=x, m=m)
    return {
        "varx": np.nanvar(x, ddof=1),
        "vare": np.nanvar(stlfit["residuals"], ddof=1),
        "vara": np.nanvar(stlfit["residuals"] + stlfit["seasonal"], ddof=1),
        "vardeseason": np.nanvar(x - stlfit["seasonal"]),
        "vardetrend": np.nanvar(x - stlfit["trend"]),
    }


def seasonal_strength(x: array_like, m: int) -> float:
    """
    Summary:
        The seasonal strength of a univariate timeseries data set.

    Params:
        x (array_like):
            The time series data set.
        m (int):
            The frequency of the time series data set.

    Returns:
        float:
            The seasonal strength score.

    ???+ Info "Details"
        All credit to the [`tsfeatures`](http://pkg.robjhyndman.com/tsfeatures/) library.
        This code is a direct copy+paste from the [`tsfeatures.py`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py) module.

    ???+ Example "Examples"
        _description_
        ```python linenums="1"
        >>> _description_
        ```
    """
    if not m > 1:
        return 0
    else:
        stlvar = _get_stlvar(x=x, m=m)
        if stlvar["varx"] < np.finfo(float).eps or stlvar["vara"] < np.finfo(float).eps:
            return 0
        else:
            return max(0, min(1, 1 - stlvar["vare"] / stlvar["vara"]))


def trend_strength(x: array_like, m: int) -> float:
    """
    Summary:
        The trend strength of a univariate timeseries data set.

    Params:
        x (array_like):
            The time series data set.
        m (int):
            The frequency of the time series data set.

    Returns:
        float:
            The trend strength score.

    ???+ Info "Details"
        All credit to the [`tsfeatures`](http://pkg.robjhyndman.com/tsfeatures/) library.
        This code is a direct copy+paste from the [`tsfeatures.py`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py) module.

    ???+ Example "Examples"
        _description_
        ```python linenums="1"
        >>> _description_
        ```
    """
    if not m > 1:
        return 0
    else:
        stlvar = _get_stlvar(x=x, m=m)
        if (
            stlvar["varx"] < np.finfo(float).eps
            or stlvar["vardeseason"] / stlvar["varx"] < 1e-10
        ):
            return 0
        else:
            return max(0, min(1, 1 - stlvar["vare"] / stlvar["vardeseason"]))


def spikiness(x: array_like, m: int) -> float:
    """
    Summary:
        The spikiness of a univariate timeseries data set.

    Params:
        x (array_like):
            The time series data set.
        m (int):
            The frequency of the time series data set.

    Returns:
        float:
            The spikiness score.

    ???+ Info "Details"
        All credit to the [`tsfeatures`](http://pkg.robjhyndman.com/tsfeatures/) library.
        This code is a direct copy+paste from the [`tsfeatures.py`](https://github.com/Nixtla/tsfeatures/blob/master/tsfeatures/tsfeatures.py) module.

    ???+ Example "Examples"
        _description_
        ```python linenums="1"
        >>> _description_
        ```
    """
    n = len(x)
    stlfit = _get_stlfit(x=x, m=m)
    d = (stlfit["residuals"] - np.nanmean(stlfit["residuals"])) ** 2
    varloo = (np.nanvar(stlfit["residuals"], ddof=1) * (n - 1) - d) / (n - 2)
    return np.nanvar(varloo, ddof=1)
