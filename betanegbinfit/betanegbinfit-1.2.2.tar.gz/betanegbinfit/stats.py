  # -*- coding: utf-8 -*-
"""Fit indices"""
import numpy as np
import mpmath
import gmpy2
from .models import ModelLine, ModelMixture, Model
from itertools import accumulate
from scipy.optimize import minimize


def calc_dof(model: ModelMixture, data=None):
    """
    Calculate degrees of freedom statistic.

    dof = len(data) - effective number of parameters.
    Parameters
    ----------
    model : ModelMixture
        Model with estimated parameters.
    data, optional : np.ndarray
        Data array of shape n x m, where n is a number of observations and m
        is arbitrary dimensions. The default is None.

    Returns
    -------
    int
        DoF.

    """
    if data is None:
        data = model.data
    n = np.sum(data[:, -1]) if len(np.shape(data)) > 1 else len(data)
    return n - model.num_params


def power_divergence(model: ModelMixture, data, lambda_=0, max_tr=None,
                     count_tr=None, normalize=False, return_unique=False,
                     params=None, n_pads=None):
    """
    Power divergence statistic.

    Parameters
    ----------
    model : ModelMixture
        Model with estimated parameters.
    data : np.ndarray
        Data array of shape n x m.
    lambda_ : float, optional
        Lambda parameter of power divergence statistic. If _lambda = 0, it is
        equal to G-test. If _lambda = 1, it is chi2. The default is 0.
    max_tr : int, optional
        Values higher than max_tr will be trimmed. The default is None.
    count_tr : int, optional
        Values that occur less than count_tr times will be trimmed. The default
        is None.
    normalize : bool, optional
        If True, sum of expected counts is rescaled to equal number of observed
        counts.
    return_unique : bool, optional
        If True, then (possibly, trimmed) unique values are returned. The
        default is False.
    params : np.ndarray, optional
        Parameters vector for ModelMixture. If None, then it is assumed
        thatm model is already supplied with estimated parameters. The default
        is None.
    n_pads : int, optional
        Number of pads for masking. Should not be used by an external user.
        The default is None.

    Returns
    --------
    float
        PD Statistic.

    """
    uqs = data[:, 0]
    cnts = data[:, -1]
    # n = cnts.sum()
    # prc = (np.cumsum(cnts[::-1])[::-1] / n) > 0.25
    # data = data[prc, :]
    # uqs = uqs[prc]
    # cnts = cnts[prc]
    if max_tr is not None:
        inds = uqs < max_tr
        cnts = cnts[inds]
        uqs = uqs[inds]
    if count_tr is not None:
        inds = cnts > count_tr
        cnts = cnts[inds]
        uqs = uqs[inds]
    if params is None:
        params = model.last_result.x
    m = len(uqs)
    if n_pads is not None and m < n_pads:
        probs = np.exp(model.logprob(params,
                                     np.pad(uqs, (0, n_pads - m)))[:m])
    else:
        probs = np.exp(model.logprob(params, uqs))
    expected = cnts.sum() * probs
    if normalize:
        cnts *= expected.sum() / cnts.sum()
    if lambda_ == 0:
        r = 2 * (cnts * (np.log(cnts) - np.log(expected))).sum()
    else:
        r = 2 / (lambda_ * (lambda_ + 1)) * (cnts * ((cnts / expected) ** lambda_ - 1)).sum()
    if return_unique:
        return r, uqs
    return r


def rmsea(model: ModelMixture, data, dof=None, stat=None, ddof=0, max_tr=None,
          count_tr=None, lambda_=0, normalize=False, params=None, n_pads=None):
    """
    Root Mean Square Error of Approximation statistic.

    Parameters
    ----------
    model : ModelMixture
        Model with estimated parameters.
    data : np.ndarray
        Data array of shape n x m.
    dof : int, optional
        Degree of Freedom statistic. If None, then it will be estimated. The
        default is None.
    stat : float, optional
        Fit statistic. If None, then power-divergence with lambda_ will be
        used. The default is None.
    ddof : int, optional
        ddof will be subtracted from dof. The default is 0.
    max_tr : int, optional
        Values higher than max_tr will be trimmed. The default is None.
    count_tr : int, optional
        Values that occur less than count_tr times will be trimmed. The default
        is None.
    lambda_ : float, optional
        Lambda parameter of power divergence statistic. If _lambda = 0, it is
        equal to G-test. If _lambda = 1, it is chi2. The default is 0.
    normalize : bool, optional
        If True, sum of expected counts is rescaled to equal number of observed
        counts.
    params : np.ndarray, optional
        Parameters vector for ModelMixture. If None, then it is assumed
        thatm model is already supplied with estimated parameters. The default
        is None.
    n_pads : int, optional
        Number of pads for masking. Should not be used by an external user.
        The default is None.

    Returns
    -------
    float
        RMSEA statistic.
    """
    if stat is None:
        stat, uqs = power_divergence(model, data, max_tr=max_tr,
                                     count_tr=count_tr, lambda_=lambda_,
                                     return_unique=True, normalize=normalize,
                                     params=params, n_pads=n_pads)
    if dof is None:
        dof = calc_dof(model, uqs)
    dof -= ddof
    n = data[:, -1].sum()
    if (n - 1) * dof <= 0:
        return np.nan, (stat, dof)
    return np.sqrt(max(stat - dof, 0) / ((n - 1) * dof)), (stat, dof)


def _sum_two_vectors(a: np.ndarray, b: np.ndarray, w: float):
    a = list(map(gmpy2.mpfr, a.tolist()))
    b = list(map(gmpy2.mpfr, b.tolist()))
    w1 = gmpy2.mpfr(w)
    w2 = gmpy2.mpfr('1') - w1
    return [w1 * a + w2 * b for a, b in zip(a, b)]

def _fill_negs_f(x: np.ndarray, logs, nums):
    return np.sum((nums ** x[0] + x[1] - logs) ** 2)

def _fill_negs_g(x: np.ndarray, logs, nums):
    v = 2 * (nums ** x[0] + x[1] - logs)
    g = list()
    # g.append((v * nums ** x[1]).sum())
    g.append((v * nums ** x[0] * np.log(nums)).sum())
    g.append(v.sum())
    return np.array(g)    
    

def _fill_negs(sfs: np.ndarray, nums: np.ndarray,
               min_samples=np.inf) -> np.ndarray:
    sfs = np.array(list(map(float, sfs)))
    inds = sfs > 0
    tsfs = sfs[inds]
    tnums = nums[inds]
    sfs[~inds] = sfs[inds].min()
    return sfs
    if np.all(inds) or len(tsfs) < min_samples:
        m = tsfs.min()
        if m == 0:
            m = 1e-14
        sfs[~inds] = m
        return sfs
    tsfs = -np.log(tsfs).astype(np.longdouble)
    tnums = tnums.astype(np.longdouble)
    r = minimize(lambda x: _fill_negs_f(x, tsfs, tnums),
                 jac=lambda x: _fill_negs_g(x, tsfs, tnums),
                 x0=np.array([0.5, 1.0],
                             dtype=np.longdouble))
    x = r.x
    sfs[~inds] = np.exp(nums[~inds] ** x[0] + x[1])
    return sfs


# def calc_pvalues_mixture_long(model: ModelMixture, data=None,
#                               sep_modes=False, params=None,
#                               mask_n=None, use_cache=False,
#                               return_list=False) -> np.ndarray:
#     if data is None:
#         data = model.data
#     left = model.left + 1
#     if params is None:
#         params = model.last_result.x
#     m = data[:, 0].max()
#     nums = np.arange(left, 2 * (200 + m + 1))
#     pmfs = model.prob_modes(params, list(nums))
#     pmf_l, pmf_r = pmfs
#     i = list(nums).index(data[:, 0].max())
#     nums = nums[:i + 1]
#     one = gmpy2.mpfr('1')
#     pvals = list()
#     for n in data[:, 0]:
#         c = pmf_l[n - left]
#         tot_s = sum(pmf for pmf in pmf_l if pmf > c)
#         pvals.append(one - tot_s)
#     if return_list:
#         return pvals
#     pvals = list(map(float, pvals))
#     return np.clip(pvals, 0.0, 1.0)

def calc_pvalues_mixture_long(model: ModelMixture, data=None,
                              sep_modes=False, params=None,
                              mask_n=None, return_list=False) -> np.ndarray:
    if data is None:
        data = model.data
    left = model.left + 1
    if params is None:
        params = model.last_result.x
    m = data[:, 0].max()
    nums = np.arange(left, m + 1)
    cdfs = model.cdf_modes(params, list(nums))
    cdfs_l, cdfs_r = cdfs
    i = list(nums).index(data[:, 0].max())
    nums = nums[:i + 1]
    cdfs_l = cdfs_l[:i + 1]
    cdfs_r = cdfs_r[:i + 1]
    for c in (cdfs_l, cdfs_r):
        tmax = 0
        for j in range(len(c)):
            if c[j] >= 1.0:
                break
            elif c[j] > tmax:
                tmax = c[j]
        for j in range(j, len(c)):
            c[j] = tmax
    w  = model.get_param('w', params)
    one = gmpy2.mpfr('1')
    if sep_modes:
        inds = np.argmax([[w * v for v in cdfs_l],
                          [(1 - w) * v for v in cdfs_r]], axis=0)
        sfs = [one - cdfr if i else one - cdfl
                for i, cdfl, cdfr in zip(inds, cdfs_l, cdfs_r)]
    else:
        sfs = [one - (w * l + (one - w) * r) for l, r in zip(cdfs_l, cdfs_r)]
    if return_list:
        pvals = [None] * len(data)
    else:
        pvals = np.zeros(len(data), dtype=float)
    for i, v in enumerate(data[:, 0]):
        if v <= left:
            pvals[i] = 1.0
        else:
            if return_list:
                pvals[i] = sfs[int(v - nums[0] - 1)]
            else:
                pvals[i] = float(sfs[int(v - nums[0] - 1)])
    if return_list:
        return pvals
    return np.clip(pvals, 0.0, 1.0)


def _calc_sfs(model: ModelMixture, params, nums, mask_n, sep_modes):
    if mask_n is not None and len(nums) < mask_n:
        n = len(nums)
        nums = np.pad(nums, (0, int(mask_n) - len(nums)))
        pdfs_l, pdfs_r = model.logprob_modes(params, nums)
        pdfs_l = pdfs_l[:n]
        pdfs_r = pdfs_r[:n]
    else:
        pdfs_l, pdfs_r = model.logprob_modes(params, nums)
    pdfs_l = np.exp(pdfs_l)
    pdfs_r = np.exp(pdfs_r)
    w  = model.get_param('w', params)
    one = gmpy2.mpfr('1.0')
    if sep_modes:
        inds = np.argmax([pdfs_l * w, pdfs_r * (1 - w)], axis=0)
        pdfs_l = list(map(gmpy2.mpfr, pdfs_l))
        pdfs_r = list(map(gmpy2.mpfr, pdfs_r)) 
        cdfs_l = list(accumulate(pdfs_l))
        cdfs_r = list(accumulate(pdfs_r))
        sfs = [one - cdfr if i else one - cdfl
                for i, cdfl, cdfr in zip(inds, cdfs_l, cdfs_r)]
    else:
        pdfs = _sum_two_vectors(pdfs_l, pdfs_r, w)
        sfs = [one - cdf for cdf in accumulate(pdfs)]
    return sfs

def calc_pvalues_mixture(model: ModelMixture, data=None,
                          sep_modes=False, params=None,
                          mask_n=None, 
                          min_samples=np.inf) -> np.ndarray:
    if data is None:
        data = model.data
    left = model.left + 1
    nums = np.arange(left, data[:, 0].max() + 1)
    if params is None:
        params = model.last_result.x
    # if model.dist == 'NB':
    #     sfs = _calc_sfs(model, params, nums, mask_n, sep_modes)
    # else:
    sfs = np.repeat(-1, len(nums))
    inds = list(); ns = list()
    for i, n in enumerate(nums):
        if sfs[i] <= 0:
            inds.extend(np.arange(i, len(nums))) 
            ns.extend(nums[i:])
            break
    if inds:
        sfs = list(sfs)
        data_sub = np.array([ns, [1] * len(ns)], dtype=int).T
        sfs2 = calc_pvalues_mixture_long(model, data_sub, sep_modes, params,
                                         return_list=True)
        for ind, sf in zip(inds, sfs2):
            sfs[ind] = sf
    pvals = np.zeros(len(data), dtype=float)
    for i, v in enumerate(data[:, 0]):
        if v < left:
            pvals[i] = 1.0
        else:
            pvals[i] = float(sfs[int(v - nums[0])])
    return np.clip(pvals, 0.0, 1.0)

def calc_eff_sizes(model: ModelLine, data=None, params=None):
    if data is None:
        data = model.data
    return np.log2(data[:, 0]) - np.log2(model.mean(params))

def adjust_w(model: ModelLine, data=None):
    ind_slices = model.slices_inds
    slices = model.slices
    if data is None:
        data = model.data
    if len(data.shape) > 1:
        refs = data[:, 0]
        counts = data[:, 1]
    else:
        counts = 1
    ws = np.array(model.get_sliced_params(model.last_result.x)['w'])[ind_slices]
    bf = np.zeros_like(ws)
    ms1, ms2 = model.logprob_modes(model.last_result.x, data)
    for i, s in enumerate(slices):
        inds = ind_slices == i
        for u in np.unique(data[inds]):
            inds_sub = (data[:, 0] == u) & inds
            bf[inds_sub] = (ms1[inds_sub] - ms2[inds_sub]).sum()
    params = model.last_result.x
    ws = 1 / (1 + np.exp(bf) * (1 / ws - 1))
    params[:len(slices)] = ws
    return params

def calc_pvalues_line(model: ModelLine, sep_modes=True,
                      w_adjustment=False) -> np.ndarray:
    data = model.data
    pvals = np.zeros(len(model.data))
    modmix = ModelMixture(model.bad, model.left, model.mod_name,
                          estimate_p=model.estimate_p)
    param_names = list(modmix.params_active)
    params = model.last_result.x
    if w_adjustment:
        params = adjust_w(model)
    params_sliced = model.get_sliced_params(params)
    params = [params_sliced[p] for p in param_names]
    inds_slices = model.slices_inds
    mask_n = data[:, 0].max()
    for i, params in enumerate(zip(*params)):
        params = np.array(params)
        inds = inds_slices == i
        df = data[inds]
        pv = calc_pvalues_mixture(modmix, df, sep_modes, params, mask_n)
        pvals[inds] = pv
    return pvals

    
def calc_pvalues(model: Model, sep_modes=True,
                 w_adjustement=False) -> np.ndarray:
    """
    Calculate p-values for each snp.

    Parameters
    ----------
    model : Model
        Either ModelMixture of ModelLine instance.
    sep_modes : bool, optional
        If True, then only the most probable mode is used. The default is True.
    w_adjustement : bool, optional
        If True, then 'bayes factors' are applied beforehand. The default is
        False.

    Returns
    -------
    np.ndarray
        Array of p-values.

    """
    
    if type(model) is ModelMixture:
        return calc_pvalues_mixture(model, sep_modes=sep_modes)
    else:
        return calc_pvalues_line(model, sep_modes=sep_modes)

def adjusted_loglik(model: Model, data: np.ndarray, params: np.ndarray,
                    loglik: float, omit_zeros=True):
    fim = model.calc_cov(data, params=params, return_fim=True)
    eigs = np.linalg.eigh(fim)[0]
    if omit_zeros:
        eigs = eigs[eigs > 1e-12]
    eigs = np.log(eigs)
    return loglik - eigs.sum() / data[:, 1].sum()