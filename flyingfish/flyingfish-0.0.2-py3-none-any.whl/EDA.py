import statistics
from collections import Counter
import numpy as np
import pandas as pd


# ----------------------------------------------------------------
# estimates of location
# ----------------------------------------------------------------

def arithmetic_mean(data: list):
    """Returns arithmetic mean [float]."""
    return np.mean(data)


def weighted_arithmetic_mean(data: list, weights: list[float]):
    """Returns weighted (element-wise) arithmetic mean [float]."""
    return sum(np.multiply(data, weights))/sum(weights)


def trimmed_mean(data: list, p: int):
    """Returns trimmed arithmetic mean [float] with the smallest and
    largest p elements skipped.
    """
    trimmed = sorted(data)[p:-p]
    return np.mean(trimmed)


def geometric_mean(data: list):
    """Returns geometric mean [float]."""
    return statistics.geometric_mean(data)


def exponential_mean(data: list, m: float):
    """Returns exponential mean [float] using exponent m."""
    return (sum([x**m for x in data])/len(data))**(1/m)


def harmonic_mean(data: list):
    """Returns harmonic mean [float]."""
    return statistics.harmonic_mean(data)


def median(data: list):
    """Returns median [float]."""
    return statistics.median(data)


def weighted_median(data: list, weights: list[float]):
    """Returns (element-wise) weighted median [float]."""
    weighted_list = []
    for i in np.arange(len(data)):
        weighted_list.extend([data[i]]*weights[i])
    return statistics.median(weighted_list)


def percentile(data: list, per: int):
    """Return percentile value [float]."""
    sort = sorted(data)
    # return np.percentile(data, per)
    return sort[int(per/100*len(sort))]

# ----------------------------------------------------------------
# estimates of variability
# ----------------------------------------------------------------


def mu(data: list, k: int):
    """Returns the k-th statistical moment [float] related to the
    arithmetic mean.
    """
    mean = arithmetic_mean(data)
    return np.mean([(i-mean)**k for i in data])


def avg_absolute_deviation_from_mean(data: list):
    """Returns the mean deviation from the mean [float]."""
    mean = arithmetic_mean(data)
    return np.mean([abs(i-mean) for i in data])


def avg_absolute_deviation_from_median(data: list):
    """Returns the mean deviation from the median [float]."""
    med = median(data)
    return np.mean([abs(i-med) for i in data])


def median_absolute_deviaton(data: list):
    """Returns the median absolute deivation (MAD) [float]."""
    med = median(data)
    deviations = [abs(i-med) for i in data]
    return statistics.median(deviations)


def variance(data: list, biased: bool):
    """Returns the (biased/ unbiased) variance [float]"""
    mu2 = mu(data, k=2)
    n = len(data)
    if biased:
        return mu2
    else:
        return mu2 * n/(n-1)


def stdev(data: list, biased: bool):
    """Returns the (biased/ unbiased) standard deviation from
    arithmetic mean [float]."""
    mu2 = mu(data, k=2)
    n = len(data)
    if biased:
        return mu2**(1/2)
    else:
        return (mu2*n/(n-1))**(1/2)


def range(data: list):
    """Returns range [float]."""
    return max(data)-min(data)


def iqr(data: list):
    """Returns IQR [float]."""
    sort = sorted(data)
    index_25 = int(0.25*len(sort))
    index_75 = int(0.75*len(sort))
    # return np.subtract(*np.percentile(data, [75, 25]))
    return sort[index_75] - sort[index_25]

# ----------------------------------------------------------------
# estimates of distribution
# ----------------------------------------------------------------


def coefficient_of_skewness(data: list, biased: bool):
    """Returns (biased/ unbiased) skewness [float]."""
    s = stdev(data, biased=True)
    mu3 = mu(data, k=3)
    skew = mu3/s**3
    n = len(data)
    if biased:
        return skew
    else:
        return skew*(n**2)/((n-1)*(n-2))


def coefficient_of_kurtosis(data: list, biased: bool):
    """Returns (biased/ unbiased) kortosis [float]."""
    s = stdev(data, biased=True)
    mu4 = mu(data, k=4)
    kurt = mu4/s**4
    n = len(data)
    if biased:
        return kurt
    else:
        return kurt*(n**3)/((n-1)*(n-2)*(n-3))


def mode(data: list):
    """Returns mode [float]."""
    c = Counter(data)
    return [k for k, v in c.items() if v == c.most_common(1)[0][1]]


# ----------------------------------------------------------------
# quality investigation
# ----------------------------------------------------------------

def missing_days(df: pd.DataFrame):
    """Returns the number of missing days [int]"""
    diff = (df.index[-1]-df.index[0]).days
    n_missing = (diff+1) - len(df)
    return n_missing


def duplicates(df: pd.DataFrame):
    """Returns the number of duplicate dates [int]."""
    dates = list(df.index.values)
    n_duplicates = len(
        [item for item, count in Counter(dates).items() if count > 1])
    return n_duplicates


def outlier(data: list, solving_strategy: str = "none"):
    """Detect and handle outliers. Upper and lower outliers are defined
    as exceeding the 1.5 times IQR.

    Args:
        data (list): _description_
        solving_strategy (str, optional): 3 strategies are possible:
            1. drop_outlier, 2. cap_outlier, 3. none (default)

    Returns:
        tuple(list[float], list[float]): outliers and corrected data
    """
    # 1. find outliers
    upper_border = percentile(data, 75) + 1.5*iqr(data)
    lower_border = percentile(data, 25) - 1.5*iqr(data)
    outliers = [x for x in data if not lower_border <= x <= upper_border]

    # 2. handle outliers
    match solving_strategy:
        case "drop_outlier":
            data_corr = [x for x in data if lower_border <= x <= upper_border]
        case "cap_outlier":
            data_corr = [max(min(x, upper_border), lower_border) for x in data]
        case "none":
            data_corr = data

    return outliers, data_corr
