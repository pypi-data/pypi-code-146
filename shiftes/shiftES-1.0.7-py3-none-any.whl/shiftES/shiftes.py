"""Implimentation of some functions described in:

Wilcox, Rand. "A robust nonparametric measure of effect size based on an
analog of Cohen's d, plus inferences about the median of the typical difference."
Journal of Modern Applied Statistical Methods 17.2 (2019): 1.
https://dx.doi.org/10.22237/jmasm/1551905677

Functions:
    difference_dist(a, b): All of the difference between values in a, b
    Q(a, b): Calculate Q value.
"""


import numpy as np
import logging, typing
logging.basicConfig()

def difference_dist(X1, X2) -> np.ndarray:
    """All of the difference between values in X1, X2"""
    a_m = np.tile(X1, (X2.shape[0], 1))
    b_m = np.tile(X2, (X1.shape[0], 1))
    D = np.ravel(a_m.T - b_m)
    return D


def _clean_np_arrays(a, b):
    a, b = np.array(a), np.array(b)
    a, b = [ab[~np.isnan(ab)] for ab in (a, b)]
    return a, b

def effectsize(X1, X2, max_obsv=1000, report_Q=False):
    """Calculate Wilcox Ω effect size. This is a transformation of Q
    described in Wilcox (2018) ranging -1 to 1 with 0 indicating no effect.

    Guide to effect sizes (equiv to Cohen's d small/medium/large):
        |Ω|: small 0.1; medium 0.3; large 0.4
        Q: small 0.55; medium 0.65; large 0.70

    Args:
        X1, X2: 1D collections of numbers
        report_Q: Report Q value not Ω. Ω=(Q-0.5)/0.5
        max_obsv: If X1 or X2 contain more than max_obsv, they are resampled down
            to max_obsv. Set to False to always use all observations. (note
            an array of size len(a)*len(b) is generated)
    """


    def sampdown(ab):
        """sample down to max_obsv if we have more than that already"""
        if ab.shape[0] > max_obsv:
            return ab[np.random.randint(0, ab.shape[0], size=max_obsv)]
        return ab

    X1, X2 = _clean_np_arrays(X1, X2)
    X1, X2 = [sampdown(ab) for ab in (X1, X2)]

    D = difference_dist(X1, X2)
    # Y = D, were the null hyp true
    median = D.dtype.type(np.median(D))

    Y = D - median

    # Q: proportion of Y that are less than equal to actual median
    Q = np.sum(Y < median) / Y.shape[0]


    if not report_Q:
        return (Q-0.5)/0.5
    else:
        return Q


def effectsize_ci(X1, X2, ci=0.05, max_obsv=1000, nboot=500, report_Q=False) \
        -> typing.Tuple[float, float, float]:
    """Calculate confidence intervals of effect size. """

    es_kwargs = dict(report_Q=report_Q, max_obsv=max_obsv)

    X1, X2 = _clean_np_arrays(X1, X2)
    qs = np.empty(shape=nboot, dtype=np.float32)

    na, nb = [min(len(ab), max_obsv) for ab in (X1, X2)]

    es = effectsize(X1, X2, **es_kwargs)

    for i in range(nboot):
        resampled_ab = []
        for ab, n_ab in [(X1, na), (X2, nb)]:
            resampled_ab.append(
                ab[np.random.randint(0, len(ab), size=n_ab)]
            )
        qs[i] = np.float32(effectsize(*resampled_ab, **es_kwargs))
    lower = ci
    upper = 1-ci
    return es, np.quantile(qs, lower), np.quantile(qs, upper)










