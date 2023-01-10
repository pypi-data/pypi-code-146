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
    r"""
    !!! summary "Summary"
        Calculate the autocorrelation function.

    ???+ info "Details"
        The acf at lag `0` (ie., `1`) is returned.

        For very long time series it is recommended to use `fft` convolution instead. When `fft` is `False` uses a simple, direct estimator of the autocovariances that only computes the first $nlag + 1$ values. This can be much faster when the time series is long and only a small number of autocovariances are needed.

        If `adjusted` is `True`, the denominator for the autocovariance is adjusted for the loss of data.

    Args:
        x (array_like):
            The time series data.
        adjusted (bool, optional):
            If `True`, then denominators for auto-covariance are $n-k$, otherwise $n$.<br>
            Defaults to `False`.
        nlags (int, optional):
            Number of lags to return autocorrelation for. If not provided, uses $min(10 * np.log10(nobs), nobs - 1)$. The returned value includes $lag 0$ (ie., $1$) so size of the acf vector is $(nlags + 1,)$.<br>
            Defaults to `None`.
        qstat (bool, optional):
            If `True`, returns the Ljung-Box $q$ statistic for each autocorrelation coefficient. See q_stat for more information.<br>
            Defaults to `False`.
        fft (bool, optional):
            If `True`, computes the ACF via FFT.<br>
            Defaults to `True`.
        alpha (float, optional):
            If a number is given, the confidence intervals for the given level are returned. For instance if $alpha=.05$, a $95\%$ confidence intervals are returned where the standard deviation is computed according to Bartlett"s formula.<br>
            Defaults to `None`.
        bartlett_confint (bool, optional):
            Confidence intervals for ACF values are generally placed at 2 standard errors around $r_k$. The formula used for standard error depends upon the situation. If the autocorrelations are being used to test for randomness of residuals as part of the ARIMA routine, the standard errors are determined assuming the residuals are white noise. The approximate formula for any lag is that standard error of each $r_k = 1/sqrt(N)$. See section 9.4 of [2] for more details on the $1/sqrt(N)$ result. For more elementary discussion, see section 5.3.2 in [3]. For the ACF of raw data, the standard error at a lag $k$ is found as if the right model was an $MA(k-1)$. This allows the possible interpretation that if all autocorrelations past a certain lag are within the limits, the model might be an $MA$ of order defined by the last significant autocorrelation. In this case, a moving average model is assumed for the data and the standard errors for the confidence intervals should be generated using Bartlett's formula. For more details on Bartlett formula result, see section 7.2 in [2].<br>
            Defaults to `True`.
        missing (str, optional):
            A string in `["none", "raise", "conservative", "drop"]` specifying how the `NaN`'s are to be treated.

            - `"none"` performs no checks.
            - `"raise"` raises an exception if NaN values are found.
            - `"drop"` removes the missing observations and then estimates the autocovariances treating the non-missing as contiguous.
            - `"conservative"` computes the autocovariance using nan-ops so that nans are removed when computing the mean and cross-products that are used to estimate the autocovariance.

            When using `"conservative"`, $n$ is set to the number of non-missing observations.<br>
            Defaults to `"none"`.

    Returns:
        acf (np.ndarray):
            The autocorrelation function for lags `0, 1, ..., nlags`.<br>
            Shape `(nlags+1,)`.
        confint (np.ndarray):
            Confidence intervals for the ACF at lags `0, 1, ..., nlags`.<br>
            Shape `(nlags + 1, 2)`.<br>
            Returned if `alpha` is not `None`.
        qstat (np.ndarray):
            The Ljung-Box Q-Statistic for lags `1, 2, ..., nlags` (excludes lag zero).<br>
            Returned if `q_stat` is `True`.
        pvalues (np.ndarray):
            The p-values associated with the Q-statistics for lags `1, 2, ..., nlags` (excludes lag zero).<br>
            Returned if `q_stat` is `True`.

    !!! success "Credit"
        - All credit goes to the [`statsmodels`](https://www.statsmodels.org/) library.

    !!! example "Examples"
        _description_
        ```python linenums="1" title="Python"
        >>> _description_
        ```

    ??? question "References"
        1. Parzen, E., 1963. On spectral analysis with missing observations and amplitude modulation. Sankhya: The Indian Journal of Statistics, Series A, pp.383-392.
        1. Brockwell and Davis, 1987. Time Series Theory and Methods.
        1. Brockwell and Davis, 2010. Introduction to Time Series and Forecasting, 2nd edition.

    ??? tip "See Also"
        - [`statsmodels.tsa.stattools.acf`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.acf.html#statsmodels.tsa.stattools.acf): Estimate the autocorrelation function.
        - [`ts_stat_tests.correlation.pacf`][src.ts_stat_tests.correlation.pacf]: Partial autocorrelation estimate.
        - [`statsmodels.tsa.stattools.pacf`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html#statsmodels.tsa.stattools.pacf): Partial autocorrelation estimation.
    """
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
    x: array_like,
    nlags: int = None,
    method: str = "ywadjusted",
    alpha: float = None,
) -> Union[np.ndarray, Tuple[Union[np.ndarray, Optional[np.ndarray]]]]:
    r"""
    !!! summary "Summary"
        Partial autocorrelation estimate.

    ???+ info "Details"
        Based on simulation evidence across a range of low-order ARMA models, the best methods based on root MSE are Yule-Walker (MLW), Levinson-Durbin (MLE) and Burg, respectively. The estimators with the lowest bias included included these three in addition to OLS and OLS-adjusted.

        Yule-Walker (adjusted) and Levinson-Durbin (adjusted) performed consistently worse than the other options.

    Args:
        x (array_like):
            Observations of time series for which pacf is calculated.
        nlags (int, optional):
            Number of lags to return autocorrelation for. If not provided, uses $min(10 * np.log10(nobs), nobs // 2 - 1)$. The returned value includes lag `0` (ie., `1`) so size of the pacf vector is $(nlags + 1,)$.<br>
            Defaults to `None`.
        method (str, optional):
            Specifies which method for the calculations to use.

            - `"yw"` or `"ywadjusted"`: Yule-Walker with sample-size adjustment in denominator for acovf. Default.
            - `"ywm"` or `"ywmle"`: Yule-Walker without adjustment.
            - `"ols"`: regression of time series on lags of it and on constant.
            - `"ols-inefficient"`: regression of time series on lags using a single common sample to estimate all pacf coefficients.
            - `"ols-adjusted"`: regression of time series on lags with a bias adjustment.
            - `"ld"` or `"ldadjusted"`: Levinson-Durbin recursion with bias correction.
            - `"ldb"` or `"ldbiased"`: Levinson-Durbin recursion without bias correction.<br>

            Defaults to `"ywadjusted"`.
        alpha (float, optional):
            If a number is given, the confidence intervals for the given level are returned. For instance if `alpha=.05`, $95\%$ confidence intervals are returned where the standard deviation is computed according to $1/sqrt(len(x))$.<br>
            Defaults to `None`.

    Returns:
        pacf (np.ndarray):
            The partial autocorrelations for lags `0, 1, ..., nlags`.<br>
            Shape `(nlags+1,)`.
        confint (np.ndarray):
            Confidence intervals for the PACF at lags `0, 1, ..., nlags`.<br>
            Shape `(nlags + 1, 2)`.<br>
            Returned if `alpha` is not `None`.

    !!! success "Credit"
        - All credit goes to the [`statsmodels`](https://www.statsmodels.org/) library.

    !!! example "Examples"
        _description_
        ```python linenums="1" title="Python"
        >>> _description_
        ```

    ??? question "References"
        1. Box, G. E., Jenkins, G. M., Reinsel, G. C., & Ljung, G. M. (2015). Time series analysis: forecasting and control. John Wiley & Sons, p. 66.
        1. Brockwell, P.J. and Davis, R.A., 2016. Introduction to time series and forecasting. Springer.

    ??? tip "See Also"
        - [`ts_stat_tests.correlation.acf`][src.ts_stat_tests.correlation.acf]: Estimate the autocorrelation function.
        - [`statsmodels.tsa.stattools.acf`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.acf.html#statsmodels.tsa.stattools.acf): Estimate the autocorrelation function.
        - [`statsmodels.tsa.stattools.pacf`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf.html#statsmodels.tsa.stattools.pacf): Partial autocorrelation estimation.
        - [`statsmodels.tsa.stattools.pacf_yw`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf_yw.html#statsmodels.tsa.stattools.pacf_yw): Partial autocorrelation estimation using Yule-Walker.
        - [`statsmodels.tsa.stattools.pacf_ols`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf_ols.html#statsmodels.tsa.stattools.pacf_ols): Partial autocorrelation estimation using OLS.
        - [`statsmodels.tsa.stattools.pacf_burg`](https://www.statsmodels.org/stable/generated/statsmodels.tsa.stattools.pacf_burg.html#statsmodels.tsa.stattools.pacf_burg): Partial autocorrelation estimation using Burg's method.
    """
    return st_pacf(x=x, nlags=nlags, method=method, alpha=alpha)


@typechecked
def ccf(
    x: array_like,
    y: array_like,
    adjusted: bool = True,
    fft: bool = True,
) -> np.ndarray:
    """
    !!! summary "Summary"
        The cross-correlation function.

    ???+ info "Details"
        If `adjusted` is `True`, the denominator for the autocovariance is adjusted.

    Args:
        x (array_like):
            The time series data to use in the calculation.
        y (array_like):
            The time series data to use in the calculation.
        adjusted (bool, optional):
            If `True`, then denominators for cross-correlation is $n-k$, otherwise $n$.<br>
            Defaults to `True`.
        fft (bool, optional):
            If `True`, use FFT convolution. This method should be preferred for long time series.<br>
            Defaults to `True`.

    Returns:
        (np.ndarray):
            The cross-correlation function of `x` and `y`.

    !!! success "Credit"
        - All credit goes to the [`statsmodels`](https://www.statsmodels.org/) library.

    !!! example "Examples"
        _description_
        ```python linenums="1" title="Python"
        >>> _description_
        ```
    """
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
