"""操作"""
import numpy as np
import polars as pl
from scipy.stats import percentileofscore, linregress, pearsonr
from .functions import rolling_apply_cols


Feature = pl.col


def Abs(feature: Feature):
    """Feature Abs

    Parameters
    ----------
    feature : Expression
        feature instance

    Returns
    ----------
    Expression
        a feature instance with Abs
    """
    return Feature.abs()


def Sign(feature: Feature):
    """Feature Sign

    Parameters
    ----------
    feature : Expression
        feature instance

    Returns
    ----------
    Expression
        a feature instance with Sign
    """
    return Feature.sign()


def Log(feature: Feature):
    """Feature Log

    Parameters
    ----------
    feature : Expression
        feature instance

    Returns
    ----------
    Expression
        a feature instance with log
    """
    return feature.log()


def Log10(feature: Feature):
    """Feature Log10

    Parameters
    ----------
    feature : Expression
        feature instance

    Returns
    ----------
    Expression
        a feature instance with log10
    """
    return feature.log10()


# * def Mask(feature: Feature):
# *
# * class Mask(NpElemOperator):
# *    """Feature Mask
# *
# *    Parameters
# *    ----------
# *    feature : Expression
# *        feature instance
# *    instrument : str
# *        instrument mask
# *
# *    Returns
# *    ----------
# *    Expression
# *        a feature instance with masked instrument
# *    """
# *
# *    def __init__(self, feature, instrument):
# *        super(Mask, self).__init__(feature, "mask")
# *        self.instrument = instrument
# *
# *    def __str__(self):
# *        return f"{type(self).__name__}({self.feature},{self.instrument.lower()})"
# *
# *    def _load_internal(self, instrument, start_index, end_index, *args):
# *        return self.feature.load(self.instrument, start_index, end_index, *args)


def Not(feature: Feature):
    """Not Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        feature elementwise not output
    """
    return feature.is_not()


def Power(left: Feature, right: Feature):
    """Power Operator

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance

    Returns
    ----------
    Feature:
        The bases in feature_left raised to the exponents in feature_right
    """
    return left.pow(right)


def If(condition: Feature, left: Feature, right: Feature) -> Feature:
    return pl.when(condition).then(left).otherwise(right)


def Ref(feature: Feature, N: int) -> Feature:
    """Feature Reference

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        N = 0, retrieve the first data; N > 0, retrieve data of N periods ago; N < 0, future data

    Returns
    ----------
    Expression
        a feature instance with target reference
    """
    return feature.shift(N)


def Mean(feature: Feature, N: int) -> Feature:
    """Rolling Mean (MA)

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling average
    """
    return feature.rolling_mean(N)


def Sum(feature: Feature, N: int) -> Feature:
    """Rolling Sum

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling sum
    """
    return feature.rolling_sum(N)


def Std(feature: Feature, N: int) -> Feature:
    """Rolling Std

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling std
    """
    return feature.rolling_std(N)


def Var(feature: Feature, N: int) -> Feature:
    """Rolling Variance

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling variance
    """
    return feature.rolling_var(N)


def Skew(feature: Feature, N: int) -> Feature:
    """Rolling Skewness

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling skewness
    """
    return feature.rolling_skew(N)


def Kurt(feature: Feature, N: int) -> Feature:
    """Rolling Kurtosis

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling kurtosis
    """
    return feature.rolling_apply(lambda x: x.kurtosis(), N)


def Max(feature: False, N: int) -> Feature:
    """Rolling Max

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling max
    """
    return feature.rolling_max(N)


def IdxMax(feature: Feature, N: int) -> Feature:
    """Rolling Max Index

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling max index
    """
    return feature.rolling_apply(lambda s: s.arr.arg_max(), N)


def Min(feature: Feature, N: int) -> Feature:
    """Rolling Min

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling min
    """
    return feature.rolling_min(N)


def IdxMin(feature: Feature, N: int) -> Feature:
    """Rolling Min Index

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling min index
    """
    return feature.rolling_apply(lambda s: s.arr.arg_min(), N)


def Quantile(feature: Feature, N: int) -> Feature:
    """Rolling Quantile

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling quantile
    """
    return feature.rollout_quantile(N)


def Med(feature: Feature, N: int) -> Feature:
    """Rolling Median

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling median
    """

    return feature.rolling_median(N)


def Mad(feature: Feature, N: int) -> Feature:
    """Rolling Mean Absolute Deviation

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling mean absolute deviation
    """
    return (feature - feature.rolling_mean(N)).abs().rolling_mean(N)


def _rank(x):
    x = x.to_numpy()
    if np.isnan(x[-1]):
        return np.nan
    x1 = x[~np.isnan(x)]
    return np.nan if x1.shape[0] == 0 else percentileofscore(x1, x1[-1]) / len(x1)


def Rank(feature: Feature, N: int) -> Feature:
    """Rolling Rank (Percentile)

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling rank
    """
    return feature.rolling_apply(_rank, N)


def Count(feature: Feature, N: int) -> Feature:
    """Rolling Count

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling count of number of non-NaN elements
    """
    return feature.rolling_apply(lambda x: x.count(), N)


def Delta(feature: Feature, N: int) -> Feature:
    """Rolling Delta

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with end minus start in rolling window
    """
    return feature - feature.shift(N)


def Slope(left: Feature, right: Feature, N: int) -> Feature:
    """Rolling Slope `Slope(A, B, N)`
    This operator calculate the slope between `left` and `right`.

    Usage Example:
    - "Slope($high, %low, 10)/$close"

    Parameters
    ----------
    left : Expression
        feature instance
    right : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with linear regression slope of given window
    """

    def _slope(x, y):
        slope_ret, _ = linregress(x, y)
        return slope_ret

    return rolling_apply_cols([left, right], _slope, N)


def Rsquare(left: Feature, right: Feature, N: int) -> Feature:
    """Rolling R-value Square

    Parameters
    ----------
    left : Expression
        feature instance
    right : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with linear regression r-value square of given window
    """

    def _r_value(x, y):
        _, _, r, _, _ = linregress(x, y)
        return r

    return rolling_apply_cols([left, right], _r_value, N)


def Resi(left: Feature, right: Feature, N: int) -> Feature:
    """Rolling Regression Residuals

    Parameters
    ----------
    left : Expression
        feature instance
    right : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with regression residuals of given window
    """

    def _resi(x, y):
        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        return std_err

    return rolling_apply_cols([left, right], _resi, N)


def WMA(feature: Feature, N: int) -> pl.Expr:
    """Rolling WMA

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with weighted moving average output
    """

    def weighted_mean(x):
        w = np.arange(len(x))
        w = w / w.sum()
        return np.nanmean(w * x)

    return feature.rolling_apply(weighted_mean, N)


def EMA(feature: Feature, N: int) -> pl.Expr:
    """Rolling Exponential Mean (EMA)

    Parameters
    ----------
    feature : Expression
        feature instance
    N : int, float
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with regression r-value square of given window
    """

    def exp_weighted_mean(x):
        a = 1 - 2 / (1 + len(x))
        w = a ** np.arange(len(x))[::-1]
        w /= w.sum()
        return np.nansum(w * x)

    return feature.rolling_apply(exp_weighted_mean, N)


def Corr(left: Feature, right: Feature, N: int) -> pl.Expr:
    """Rolling Correlation

    Parameters
    ----------
    left : Expression
        feature instance
    right : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling correlation of two input features
    """
    return rolling_apply_cols([left, right], pearsonr, N)


def Cov(left: Feature, right: Feature, N: int) -> pl.Expr:
    """Rolling Covariance

    Parameters
    ----------
    feature_left : Expression
        feature instance
    feature_right : Expression
        feature instance
    N : int
        rolling window size

    Returns
    ----------
    Expression
        a feature instance with rolling max of two input features
    """

    def _cov(x, y):
        return np.cov(x, y)[0, 1]

    return rolling_apply_cols([left, right], _cov, N)


def Tanh(feature: Feature) -> pl.Expr:
    return feature.tanh()
