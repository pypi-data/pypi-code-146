# -*- coding: utf-8 -*-
"""Auxilarily functions."""
from .models import Model, ModelMixture
from .models import ModelLine, ModelWindow, ModelMixtures
from .stats import rmsea, calc_pvalues, calc_eff_sizes, adjusted_loglik
from . import distributions as dists
import multiprocessing as mp
from collections import defaultdict
from functools import partial
from itertools import product
from scipy.special import logsumexp
from copy import deepcopy
import pandas as pd
import numpy as np
import pickle
import logging
import os




def collect_stats(model: Model, data=None, params=None, calc_pvals=True,
                  calc_es=True, sep_modes=True, n_pads=None, calc_adjusted_loglik=True) -> dict:
    results = dict()
    if data is None:
        data = model.data
    if params is None:
        params = model.params
    elif type(params) is np.ndarray:
        params = model.vec_to_dict(params)
        params['loglik'] = -model.last_result.fun / data[:, -1].sum()
    if type(model) is ModelMixture:
        params_vec = model.dict_to_vec(params)
        loglik = params['loglik']
        results['loglik'] = loglik
        if calc_adjusted_loglik:
            results['loglik_adjusted'] = adjusted_loglik(model, data, params_vec,
                                                          loglik)
        results['n'] = int(data[:, -1].sum())
        results['rmsea'], (results['stat'], results['dof']) = rmsea(model, data, params=params_vec, n_pads=n_pads)
        if calc_pvals:
            results['pvalues'] = calc_pvalues(model, sep_modes=sep_modes)
        try:
            if calc_es:
                results['es'] = calc_eff_sizes(model)
        except:
            pass
        return results
    modmix = ModelMixture(model.bad, model.left, model.dist,
                          estimate_p=model.estimate_p)
    param_names = list(modmix.params_active.keys())
    params_sliced = model.get_sliced_params()
    params = [params_sliced[p] for p in param_names if p in params_sliced]
    inds_slices = model.slices_inds
    slices = model.slices
    if calc_pvals:
        pvals = calc_pvalues(model)
    if calc_es:
        es = calc_eff_sizes(model)
    n_max = 0
    for i, params in enumerate(zip(*params)):
        params = {name: p for name, p in zip(param_names, params)}
        for p, est in model.params.items():
            if p not in params and p in param_names:
                params[p] = est
        inds = inds_slices == i
        df = data[inds]
        n = len(df)
        if n > n_max:
            n_max = n * 3
        else:
            df = np.pad(df, ((0, n_max - n), (0, 0)))
        t = df[:, -1][:n]
        params['loglik'] = float((modmix.logprob(modmix.dict_to_vec(params),
                                                df[:, 0])[:n] * t).sum() / t.sum())
        results[slices[i]] = collect_stats(modmix, df[:n], params=params,
                                           calc_pvals=False, 
                                           calc_es=False,
                                           sep_modes=sep_modes,
                                           n_pads=n_max,
                                           calc_adjusted_loglik=calc_adjusted_loglik)
        if calc_pvals:
            results[slices[i]]['pvalues'] = pvals[inds]
        if calc_es:
            results[slices[i]]['es'] = es[inds]
    return results


def get_params_at_slice(params: dict, s: int, slices=None,
                        clip_at_max_slice=False, s_at=None, nan_min=False,
                        std=False, shift=0) -> dict:
    s = int(s)
    ret = {n[0]: params[n]
           for n in filter(lambda x: x in params, (f'w{s}', f'r{s}', f'k{s}', 
                                                   f't{s}'))}
    for p in ('p1', 'p2', 'w', 't'):
        if p in params:
            ps = params[p]
            if slices is not None and not np.isscalar(ps) and len(ps) == len(slices):
                ret[p] = ps[list(slices).index(s)]
            else:
                ret[p] = ps
    power = params.get('slice_power', 1.0)
    std_p = 2 if std else 1
    if s_at is None:
        s_at = s
    s_at += shift
    if 'mu' in params:
        ret['r'] = params.get('b', 0.0) * s_at ** power ** std_p + params['mu'] ** std_p
    elif f'mu{s}' in params:
        ret['r'] = params.get(f'b{s}', 0.0) * s_at ** power ** std_p + params[f'mu{s}'] ** std_p
    if 'mu_c' in params:
        ret['r_c'] = params.get('b_c', 0.0) * s_at ** std_p + params['mu_c'] ** std_p
    elif f'mu_c{s}' in params:
        ret['r_c'] = params.get(f'b_c{s}', 0.0) * s_at ** std_p + params[f'mu_c{s}'] ** std_p
    if 'mu_k' in params:
        # ret['k'] = np.log10(1 + s_at * params.get('b_k', 0.0)) + params['mu_k'] + 4
        ret['k'] = params.get('b_k', 0.0) * np.log(s_at) ** std_p + params['mu_k'] ** std_p
        # ret['k'] = -params.get('b_k', 0.0) * s_at + params['mu_k']
    elif f'mu_k{s}' in params:
        # ret['k'] = np.log10(1 + params.get(f'b_k{s}', 0.0) * s_at) + params[f'mu_k{s}'] + 4
        ret['k'] = params.get(f'b_k{s}', 0.0) * np.log(s_at) ** std_p + params[f'mu_k{s}'] ** std_p
        # ret['k'] = -params.get(f'b_k{s}', 0.0) * s_at + params[f'mu_k{s}']
    if f'p1{s}' in params:
        ret['p1'] = params[f'p1{s}'] ** std_p
    if f'p2{s}' in params:
        ret['p2'] = params[f'p2{s}'] ** std_p
    if 'r' not in ret:
        s_at = None if clip_at_max_slice else s
        s_old = s
        s = -float('inf')
        if nan_min and s_old < min(int(k[2:]) for k in params if k.startswith('mu') and k[2].isdigit()):
            return ret
        for k in params:
            try:
                s = min(s, int(k.split('mu')[1]), key=lambda x: abs(x-s_old))
            except (ValueError, IndexError):
                continue
        return get_params_at_slice(params, s, slices, False,
                                   s_at=s_at)       
    if std:
        ret = {n: v ** 0.5 for n, v in ret.items()}
    return ret


def calc_logpdf(m, n=100,  b=None, truncation=True) -> dict:
    if b is None:
        # x = np.linspace(0, m.data[:, 0].max() + 5)
        x = np.arange(0, m.data[:, 0].max() + 1)
    else:
        x = np.arange(0, b + 1)
    model = ModelMixture(m.bad, m.left if truncation else -1, dist=m.dist,
                         estimate_p=m.estimate_p)
    p = m.params
    res = {'x': x}
    modes = dict()
    for s in m.slices:
        t = get_params_at_slice(p, s, slices=m.slices)
        w = t.get('w', 1.0)
        t = model.dict_to_vec(t)
        l, r = model.logprob_modes(t, x)
        res[s] = logsumexp(np.array([l, r]).T, axis=1,
                           b=np.array([w, 1-w]))
        modes[s] = (l, r)
    res['modes'] = modes
    return res
    
def finalize_w(model, fit_dict) -> pd.DataFrame:
    fit_dict = deepcopy(fit_dict)
    if model.bad == 1:
        return fit_dict
    mapping = {'w': 'w', 'r': 'r', 'k': 'concentration'}
    slices = model.slices
    if model.dist == 'NB':
        dist = dists.NB
        vn = 'p'
        params = ('w', 'r', )
    elif model.dist == 'BetaNB':
        dist = dists.BetaNB
        vn = 'mu'
        params = ('w', 'k', 'r', )
    p1, p2 = model.ps
    for s in slices:
        ps = get_params_at_slice(fit_dict, s)
        w = ps['w']
        d = dict()
        for p, v in ps.items():
            if p != 'w' and p in params and p in mapping:
                d[mapping[p]] = v
        d[vn] = p1
        c1 = float(dist.cdf(model.left, **d))
        d[vn] = p2
        c2 = float(dist.cdf(model.left, **d))
        wname = f'w{s}'
        t = np.clip(1 - (c2 - 1) * w / (w * (c2 - c1) + c1 - 1), 0.0, 1.0)
        fit_dict[wname] = t
    return fit_dict

def readjust_w(dist: str, parameters: dict, left: int,
               p1: float, p2: float) -> float:
    mapping = {'w': 'w', 'r': 'r', 'k': 'concentration'}
    if dist == 'NB':
        dist = dists.NB
        vn = 'p'
        params = ('w', 'r', )
    elif dist == 'BetaNB':
        dist = dists.BetaNB
        vn = 'mu'
        params = ('w', 'k', 'r', )
    d = {vn: p1}
    w = parameters['w']
    for p, v in parameters.items():
        if p in mapping and p in params and p != 'w':
            d[mapping[p]] = v
    d[vn] = p1
    c1 = float(dist.cdf(left, **d))
    d[vn] = p2
    c2 = float(dist.cdf(left, **d))
    return np.clip((c1 * (1  - w) + w - 1) / (w * (c2 - c1) + c1 - 1), 0.0,
                   1.0)
    
    

def _run(bad: float, data, output_folder: str, left: int, max_count: int,
         max_count_alt: int,  mod: str, dist: str, concentration: float,
         estimate_p: bool, window_size: int, c_bad: str, c_ref: str, c_alt: str,
         apply_weights: bool, window_behavior: str, min_slices: int,
         adjust_line: bool, start_est=True, compute_pdf=False, k_left_bound=1,
         use_cpu=False, estimate_snp_stats=False):
    if use_cpu:
        os.environ["JAX_PLATFORM_NAME"] = 'cpu'
        os.environ["XLA_PYTHON_CLIENT_ALLOCATOR"] = 'cpu'
    if type(bad) is tuple:
        bad, switch = bad
        if switch:
            c_ref, c_alt = c_alt, c_ref
            prefix = 'alt_'
        else:
            prefix = 'ref_'
    logging.info(f'[BAD={bad}, {prefix[:-1]}] Optimization...')
    output_folder = os.path.join(output_folder, 'BAD{:.2f}'.format(bad))
    os.makedirs(output_folder, exist_ok=True)
    if type(data) is pd.DataFrame:
        data = data[data[c_bad] == bad]
        df = data[[c_ref, c_alt]].values.astype(float)
    else:
        df = data[bad]
        if switch:
            df = np.array(df, dtype=float)[:, [1, 0, 2]]
    df = df[(df[:, 0] < max_count) & (df[:, 1] < max_count_alt)]
    df = df[(df[:, 0] > left) & (df[:, 1] > left)]
    if mod == 'line':
        M = partial(ModelLine, concentration=concentration, left_k=k_left_bound,
                    start_est=start_est, apply_weights=apply_weights)
    elif mod == 'slices':
        M = ModelMixtures
    elif mod == 'window':
        M = partial(ModelWindow, window_size=window_size, left_k=k_left_bound,
                    window_behavior=window_behavior, min_slices=min_slices,
                    adjust_line=adjust_line, start_est=start_est,
                    apply_weights=apply_weights)
    model = M(bad=bad, left=left, dist=dist, estimate_p=estimate_p)
    fit = model.fit(df, calc_std=True if mod == 'line' else False)
    with open(os.path.join(output_folder, f'{prefix}result.txt'), 'w') as f:
        f.write(f'{model.dist}\n')
        if mod == 'line':
            loglik  = fit['loglik']
            adj_loglik = adjusted_loglik(model, model.data, model.last_result.x,
                                          loglik)
            f.write(f'(1/n)Loglikelihood: {loglik}\nAdjusted (1/n)loglikelihood:'
                    f' {adj_loglik}\n{model.last_result}')
    b = max_count if np.isfinite(max_count) else None
    logpdf = calc_logpdf(model, b=b, truncation=True)
    with open(os.path.join(output_folder, f'{prefix}logpdf.pickle'), 'wb') as f:
        pickle.dump(logpdf, f)
    logpdf_notrunc = calc_logpdf(model, b=b, truncation=False)
    with open(os.path.join(output_folder,
                           f'{prefix}logpdf_notrunc.pickle'), 'wb') as f:
        pickle.dump(logpdf_notrunc, f)
    stds = list()
    ests = list()
    names = list()
    fit = finalize_w(model, fit)
    if 'std' in fit:
        for n, std in fit['std'].items():
            fn = fit[n]
            if np.isscalar(fn):
                ests.append(fn)
                stds.append(std)
                names.append(n)
            else:
                for i, s in enumerate(model.slices):
                    ests.append(fn[i])
                    stds.append(std[i])
                    names.append(f'{n}{s}')
                
        params = pd.DataFrame([ests, stds], index=['Estimate', 'Std.Error'],
                              columns=names).T
    else:
        for n, est in fit.items():
            if np.isscalar(est):
                ests.append(est)
                names.append(n)
            else:
                for i, s in enumerate(model.slices):
                    ests.append(est[i])
                    names.append(f'{n}{s}')
        params = pd.DataFrame([ests, ], index=['Estimate',],
                              columns=names).T
    params.to_csv(os.path.join(output_folder, f'{prefix}params.tsv'),
                  sep='\t')
    if hasattr(model, 'slice_res'):
        slice_res = model.slice_res
        slices = slice_res['slice']
        del slice_res['slice']
        params = pd.DataFrame(slice_res)
        params.index = slices
        params.index.name = 'slice'
        params.to_csv(os.path.join(output_folder, f'{prefix}params_slices.tsv'),
                      sep='\t')
    logging.info(f'[BAD={bad}, {prefix[:-1]}] Calculating p-values and fit indices...')
    stats = collect_stats(model, calc_pvals=estimate_snp_stats,
                          calc_es=estimate_snp_stats)
    stats_df = pd.DataFrame(stats).T
    if estimate_snp_stats:
        stats_df = stats_df.drop(['pvalues', 'es'], axis=1)
    stats_df.index.name = 'slice'
    stats_df.to_csv(os.path.join(output_folder, f'{prefix}stats.tsv'), sep='\t')
    r =  {'params': params, 'logpdf': logpdf, 'stats': stats_df.to_dict(),
          'logpdf_notrunc': logpdf_notrunc}
    if estimate_snp_stats:
        pvalues = np.zeros(len(model.data), dtype=float)
        es = np.zeros_like(pvalues)
        inds = model.slices_inds
        for i, s in enumerate(model.slices):
            pvalues[inds == i] = stats[s]['pvalues']
            es[inds == i] = stats[s]['es']
        snps = data.copy()
        snps[f'{prefix}p-value'] = pvalues[model.inds]
        snps[f'{prefix}ES'] = es[model.inds]
        snps = snps.set_index('index_')
        logging.info(f'[BAD={bad}. {prefix[:-1]}] Done.')
        r['snp'] = snps
    return r
    

def _run_pandas(data, output_folder: str, bads=None, model='line', dist='BetaNB', left=4,
        concentration=50.0, estimate_p=False, window_size=1000,
        window_behavior='both', min_slices=10, adjust_line=False, k_left_bound=1,
        c_bad=None, c_ref=None, c_alt=None, min_count=-np.inf, max_count=np.inf,
        max_count_alt=np.inf, apply_weights=False,  start_est=True,
        snp_filename='snps.tsv', estimate_snp_stats=False, n_jobs=1):
    """

    Parameters
    ----------
    data : pd.DataFrame
        Pandas DataFrame.
    output_folder : str
        Name of output folder where results will be stored.
    bads : list, optional
        List of BADs. If None, then bads will be guessed from the table. The
        default is None.
    model : str, optional
        Model name. Currently, can be either 'line' (ModelLine) or 'window'
        (ModelWindow). The default is 'line'.
    dist : str, optional
        Which mixture distribution to use. Can be either 'NB' or 'BetaNB'. The
        default is 'BetaNB'.
    left : int, optional
        Left-truncation bound. The default is 4.
    concentration : float, optional
        Concentration parameter for BetaNB. Can be None: then it will be
        estimated. The default is 50.0.
    estimate_p : bool, optional
        If True, then p will be estimated instead of assuming it to be fixed to
        bad / (bad + 1). The default is False.
    window_size : int, optional
        Has effect only if model = 'window', sets the required window size. The
        default is 1000.
    c_bad : str, optional
        Name of BAD column. If None, it is guessed. The default is None.
    c_ref : str, optional
        Name of REF_COUNTS column. If None, it is guessed. The default is None.
    c_alt : str, optional
        Name of ALT_COUNTS column. If None, it is guessed. The default is None.
    min_count : str, optional
        Minimal number of counts per slice. The default is -np.inf.
    max_count : int, optional
        Maximal number of counts per slice. The default is np.inf.
    max_count_alt: int, optional
        Maximal number of counts per alternative slice. The default is np.inf.
    return_results : bool, optional
        If True, then function also returns estimated parameters, logpdfs and
        a model for each BAD. The dicitonary maps to the set of REF or ALT
        alleles first, then continues to map into BADs and then to their
        respective parameter estimates and aux. data. Might be troublesome if
        you need free RAM ASAP. The default is True.
    snp_filename : str, optional
        Filename of SNP dataframe with p-values and ES. The default is
        'snps.tsv'.
    estimate_snp_stats : bool, optional
        If True, then snp statistics (p-values and ES) are estimated. The
        default is False.
    n_jobs : int, optional
        Number of parallel jobs to run. If -1, then it is determined
        automatically. The default is -1.

    Returns
    -------
    Dictionary with results if return_results is True.

    """
    min_count = max(min_count, left)
    mcount = max(max_count, max_count_alt)
    data = data[(data[c_ref] >= min_count) & (data[c_alt] >= min_count) & \
                (data[c_ref] < mcount) & (data[c_alt] < mcount)]
    data['index_'] = list(range(len(data)))
    if bads is None:
        bads = sorted(set(data[c_bad]))
    bads = list(product(bads, (False, True)))
    if n_jobs == -1:
        n_jobs = max(1, mp.cpu_count())
    n_jobs = min(len(bads), n_jobs)
    fun = partial(_run, data=data, left=left, output_folder=output_folder,
                  mod=model, dist=dist, concentration=concentration, c_bad=c_bad,
                  window_behavior=window_behavior, min_slices=min_slices,
                  c_ref=c_ref, c_alt=c_alt, apply_weights=apply_weights,
                  start_est=start_est, max_count=max_count,
                  max_count_alt=max_count_alt, k_left_bound=k_left_bound,
                  window_size=window_size, estimate_p=estimate_p,
                  adjust_line=adjust_line, use_cpu=(n_jobs != 1))
    result = defaultdict(lambda: defaultdict())
    ralt = {True: 'alt', False: 'ref'}
    if n_jobs == 1:
        for (bad, alt), res in zip(bads, map(fun, bads)):
            result[ralt[alt]][bad] = res
    else:
        ctx = mp.get_context("forkserver")
        with ctx.Pool(n_jobs) as p:
            for (bad, alt), res in zip(bads, p.map(fun, bads)):
                result[ralt[alt]][bad] = res
    if estimate_snp_stats:
        snps = None
        for bad, _ in bads:
            ref = result['ref'][bad]['snp']
            alt = result['alt'][bad]['snp']
            ref['alt_p-value'] = alt['alt_p-value']
            ref['alt_ES'] = alt['alt_ES']
            if snps is None:
                snps = ref
            else:
                snps = pd.concat([snps, ref])
        snps.to_csv(os.path.join(output_folder, 'snps.tsv'), sep='\t',
                    index=False)
    return result


def _run_dict(data, output_folder: str, model='line', dist='BetaNB', left=4,
              concentration=50.0, estimate_p=False, window_size=1000,
              window_behavior='both', min_slices=10, adjust_line=False,
              min_count=-np.inf, max_count=np.inf, max_count_alt=np.inf,
              k_left_bound=1,
              apply_weights=False, start_est=True, snp_filename='snps.tsv',
              estimate_snp_stats=False, n_jobs=1):
    """

    Parameters
    ----------
    data : pd.DataFrame
        Pandas DataFrame.
    output_folder : str
        Name of output folder where results will be stored.
    model : str, optional
        Model name. Currently, can be either 'line' (ModelLine) or 'window'
        (ModelWindow). The default is 'line'.
    dist : str, optional
        Which mixture distribution to use. Can be either 'NB' or 'BetaNB'. The
        default is 'BetaNB'.
    left : int, optional
        Left-truncation bound. The default is 4.
    concentration : float, optional
        Concentration parameter for BetaNB. Can be None: then it will be
        estimated. The default is 50.0.
    estimate_p : bool, optional
        If True, then p will be estimated instead of assuming it to be fixed to
        bad / (bad + 1). The default is False.
    window_size : int, optional
        Has effect only if model = 'window', sets the required window size. The
        default is 1000.
    min_count : str, optional
        Minimal number of counts per slice. The default is -np.inf.
    max_count : int, optional
        Maximal number of counts per slice. The default is np.inf.
    max_count_alt : int, optional
        Maximal number of counts per alternative slice. The default is np.inf.
    return_results : bool, optional
        If True, then function also returns estimated parameters, logpdfs and
        a model for each BAD. The dicitonary maps to the set of REF or ALT
        alleles first, then continues to map into BADs and then to their
        respective parameter estimates and aux. data. Might be troublesome if
        you need free RAM ASAP. The default is True.
    snp_filename : str, optional
        Filename of SNP dataframe with p-values and ES. The default is
        'snps.tsv'.
    estimate_snp_stats : bool, optional
        If True, then snp statistics (p-values and ES) are estimated. The
        default is False.
    n_jobs : int, optional
        Number of parallel jobs to run. If -1, then it is determined
        automatically. The default is -1.

    Returns
    -------
    Dictionary with results if return_results is True.

    """
    min_count = max(min_count, left)
    bads = list()
    ndict = dict()
    mcount = max(max_count, max_count_alt)
    for bad, d in data.items():
        bads.append(bad)
        d = d[(d['ref'] >= min_count) & (d['ref'] < mcount) & \
              (d['alt'] >= min_count) & (d['alt'] < mcount)]
        ndict[bad] = d.values
        
    bads = list(product(bads, (False, True)))
    if n_jobs == -1:
        n_jobs = max(1, mp.cpu_count())
    n_jobs = min(len(bads), n_jobs)
    fun = partial(_run, data=ndict, left=left, output_folder=output_folder,
                  mod=model, dist=dist, concentration=concentration, c_bad=0,
                  window_behavior=window_behavior, min_slices=min_slices,
                  c_ref=0, c_alt=1, apply_weights=apply_weights,
                  start_est=start_est, max_count=max_count,
                  max_count_alt=max_count_alt, k_left_bound=k_left_bound,
                  window_size=window_size, estimate_p=estimate_p,
                  adjust_line=adjust_line, use_cpu=(n_jobs != 1))
    result = defaultdict(lambda: defaultdict())
    ralt = {True: 'alt', False: 'ref'}
    if n_jobs == 1:
        for (bad, alt), res in zip(bads, map(fun, bads)):
            result[ralt[alt]][bad] = res
    else:
        ctx = mp.get_context("forkserver")
        with ctx.Pool(n_jobs) as p:
            for (bad, alt), res in zip(bads, p.map(fun, bads)):
                result[ralt[alt]][bad] = res
    return result


def run(data, output_folder: str, bads=None, model='line', dist='BetaNB', left=4,
        concentration=50.0, estimate_p=False, window_size=1000,
        window_behavior='both', min_slices=10, adjust_line=False,
        c_bad=None, c_ref=None, c_alt=None, min_count=-np.inf, max_count=np.inf,
        max_count_alt=None, apply_weights=False,  start_est=True, k_left_bound=1,
        snp_filename='snps.tsv', estimate_snp_stats=False, n_jobs=1):
    """

    Parameters
    ----------
    data : pd.DataFrame, str or dict[bad, np.ndarray]
        Either pandas DataFrame or path to file.
    output_folder : str
        Name of output folder where results will be stored.
    bads : list, optional
        List of BADs. If None, then bads will be guessed from the table. The
        default is None.
    model : str, optional
        Model name. Currently, can be either 'line' (ModelLine), 'window'
        (ModelWindow) or 'slices' (ModelMixtures). The default is 'line'.
    dist : str, optional
        Which mixture distribution to use. Can be either 'NB' or 'BetaNB'. The
        default is 'BetaNB'.
    left : int, optional
        Left-truncation bound. The default is 4.
    concentration : float, optional
        Concentration parameter for BetaNB. Can be None: then it will be
        estimated. The default is 50.0.
    estimate_p : bool, optional
        If True, then p will be estimated instead of assuming it to be fixed to
        bad / (bad + 1). The default is False.
    window_size : int, optional
        Has effect only if model = 'window', sets the required window size. The
        default is 1000.
    c_bad : str, optional
        Name of BAD column. If None, it is guessed. The default is None.
    c_ref : str, optional
        Name of REF_COUNTS column. If None, it is guessed. The default is None.
    c_alt : str, optional
        Name of ALT_COUNTS column. If None, it is guessed. The default is None.
    min_count : str, optional
        Minimal number of counts per slice. The default is -np.inf.
    max_count : int, optional
        Maximal number of counts per slice. The default is np.inf.
    max_count_alt : int, optional
        Maximal number of counts per salternative lice. If None, the it is the
        same as max_count. The default is None.
    return_results : bool, optional
        If True, then function also returns estimated parameters, logpdfs and
        a model for each BAD. The dicitonary maps to the set of REF or ALT
        alleles first, then continues to map into BADs and then to their
        respective parameter estimates and aux. data. Might be troublesome if
        you need free RAM ASAP. The default is True.
    snp_filename : str, optional
        Filename of SNP dataframe with p-values and ES. The default is
        'snps.tsv'.
    estimate_snp_stats : bool, optional
        If True, then snp statistics (p-values and ES) are estimated. The
        default is False.
    n_jobs : int, optional
        Number of parallel jobs to run. If -1, then it is determined
        automatically. The default is -1.

    Returns
    -------
    Dictionary with results if return_results is True.

    """
    if max_count_alt is None:
        max_count_alt = max_count
    if type(data) is str:
        if data.endswith(('.tsv', '.vcf')):
            sep = '\t'
        elif data.endswith('.csv'):
            sep = ','
        else:
            sep = ' '
        data = pd.read_csv(data, sep=sep)
    elif type(data) in (dict, defaultdict):
        r = _run_dict(data=data, output_folder=output_folder,  model=model,
                      dist=dist, left=left, concentration=concentration,
                      estimate_p=estimate_p, window_size=window_size,
                      window_behavior=window_behavior, min_slices=min_slices,
                      adjust_line=adjust_line, 
                      min_count=min_count, max_count=max_count,
                      max_count_alt=max_count_alt, k_left_bound=k_left_bound,
                      apply_weights=apply_weights, start_est=start_est,
                      snp_filename=snp_filename,
                      estimate_snp_stats=estimate_snp_stats,
                      n_jobs=n_jobs)
        return r
    
    if c_ref is None:
        try:
            c_ref = next(filter(lambda x: 'ref' in x.lower() \
                                and data[x].dtype not in ('object', 'str'),
                                data.columns))
            c_alt = next(filter(lambda x: 'alt' in x.lower() and x != c_ref and\
                                data[x].dtype not in ('object', 'str'),
                                data.columns))
            c_bad = next(filter(lambda x: 'bad' in x.lower() and x != c_ref and\
                                x != c_alt and data[x].dtype not in ('object', 'str'),
                                data.columns))
            logging.warning(f"Using columns {c_ref}, {c_alt} and {c_bad}.")
        except StopIteration:
            assert bads is not None
            bads = bads[0] if type(bads) in (list, tuple) else bads
            d = {bads: data}
            r = _run_dict(data=d, output_folder=output_folder,  model=model,
                          dist=dist, left=left, concentration=concentration,
                          estimate_p=estimate_p, window_size=window_size,
                          window_behavior=window_behavior, min_slices=min_slices,
                          adjust_line=adjust_line, c_bad=c_bad, c_ref=c_ref,
                          c_alt=c_alt, min_count=min_count, max_count=max_count,
                          max_count_alt=max_count_alt, k_left_bound=k_left_bound,
                          apply_weights=apply_weights, start_est=start_est,
                          snp_filename=snp_filename,
                          estimate_snp_stats=estimate_snp_stats,
                          n_jobs=n_jobs)
            return r
    
    r = _run_pandas(data=data, output_folder=output_folder, bads=bads, model=model,
                    dist=dist, left=left, concentration=concentration,
                    estimate_p=estimate_p, window_size=window_size,
                    window_behavior=window_behavior, min_slices=min_slices,
                    adjust_line=adjust_line, c_bad=c_bad, c_ref=c_ref, c_alt=c_alt,
                    min_count=min_count, max_count=max_count,
                    max_count_alt=max_count_alt, k_left_bound=k_left_bound,
                    apply_weights=apply_weights, start_est=start_est,
                    snp_filename=snp_filename, estimate_snp_stats=estimate_snp_stats,
                    n_jobs=n_jobs)
    return r
