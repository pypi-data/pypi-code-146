# -*- coding: utf-8 -*-
"""Mixture of 2 (beta)-negative-binomial models that models all slices simultaneously.
No standard deviations from r-line are allowed."""
from .model_mixture import ModelMixture
from .model import Model, Parameter
from scipy.optimize import minimize_scalar
from scipy.stats import linregress
from jax.scipy.special import logsumexp
from .. import distributions as dist
from collections import defaultdict
from functools import partial
from gmpy2 import mpfr
from jax import jit
import jax.numpy as jnp
import pandas as pd
import numpy as np
import logging


class ModelLine(Model):
    def __init__(self, bad: float, left: int,
                 dist='BetaNB',  concentration='line',
                 estimate_p=False, fix_params=None,
                 start_est=True, apply_weights=False,
                 left_k=1):
        """
        Construct a (Beta)Negative-Binomial mixture model.

        w * F(bad/(bad + 1), r,...) + (1 - w) F(1/(bad + 1), r,...)
        w is an active parameters. F is either NB or BetaNB, both are
        left-truncated. r is modeled as r = b * slice + mu, where b and mu are
        active parameters.
        Parameters
        ----------
        bad : float, optional
            Background Allelic Dosage value.
        left : int, optional
            Left-bound for truncation.
        dist: str
            Distribution for mixture components. Can be either 'NB' or 'BetaNB'.
            The default is 'BetaNB'.
        concentration : str, optional
            Can be either 'line' or 'intercept'. If the latter, than concentration
            parameter is modeled as a single value for all slices. If 'line',
            then it is assumed that concentration behaves itself as b * log(s) + mu,
            where b and mu are some parameters and s is a slice number. The
            default is 'line'.
        estimate_p : bool, optional
            If True, then p is estimated. If False, then then p's (plural) are
            fixed to [bad/(bad + 1), 1 / (bad + 1)]. The default is False.
        fix_params : dict, optional
            Mapping param_name -> fixed_value that will fix active parameters.
            The default is None.
        start_est : bool, optional
            If True, then starting values are estimated from individual
            models. Takes time. The default is False.
        apply_weights : bool, optional
            If True, then weighted likelihood will be used instead of an
            ordinary one. Weights are computed from slices size. It can be
            useful when there is little concentration of observations in the
            most abundant slices. The default is False.

        Returns
        -------
        None.

        """
        self.bad = bad
        self.left = left
        bad = mpfr(str(bad))
        self.ps = np.array([float(bad / (bad + 1)), float(1 / (bad + 1))])
        self.start_est = start_est
        self.concentration = concentration
        self.estimate_p = estimate_p
        self.dist = dist
        parameters = [
            Parameter('b', [1.0, 0.1], None, (None, None)),
            Parameter('mu', [0.0], None, (None, None)),
            ]
        if dist == 'BetaNB':
            parameters.append(Parameter('b_k', [2.0], None,
                                        (None, None)))
            parameters.append(Parameter('mu_k', [16.0 + left_k], None, (left_k, None)))
        p1 = Parameter('p1', [self.ps[0]],
                      None if estimate_p else self.ps[0], (0.0, 1.0))
        parameters.append(p1)
        if bad != 1:
            p2 = Parameter('p2', [self.ps[1]],
                           None if estimate_p else self.ps[1], (0.0, 1.0))
            parameters.append(p2)
        self.parameters = parameters
        self.fix_params = fix_params
        if fix_params:
            self.slice_power = fix_params.get('slice_power', 1.00)
        else:
            self.slice_power = 1.00
        self.apply_weights = apply_weights
        super().__init__(parameters, jit_fim=False, use_masking=True,
                         _allowed_const=left+1)

    def load_dataset(self, data: np.ndarray):
        """
        Runs preprocessing routine on the data.

        Build starting values, parse data into a internally usable form.
        Parameters
        ----------
        data : np.ndarray
            Either a nx(2 or 3) ndarray or pandas DataFrame or a tuple of 2
            lists. If it is an ndarray of shape 3, then it is assumed that
            first two columns form unique rows, whereas the third column
            contains counts.

        Returns
        -------
        None.

        """
        logging.debug('Preparing ModelMixtureCombined to work with provided'
                     ' dataset.')
        cs = list()
        c_inds = list()
        df = list()
        if type(data) is pd.DataFrame:
            c_ref = next(filter(lambda x: 'ref' in x.lower() \
                                and data[x].dtype not in ('object', 'str'),
                                data.columns))
            c_alt = next(filter(lambda x: 'alt' in x.lower() and x != c_ref and\
                                data[x].dtype not in ('object', 'str'),
                                data.columns))
            logging.warning(f"Using columns {c_ref} and {c_alt}.")
            data = data[(data[c_ref] > self.left) & (data[c_alt] > self.left)]
            data = data[[c_ref, c_alt]].values.astype(int)
            data, inds, w = np.unique(data, axis=0, return_counts=True,
                                      return_inverse=True)
            refs = data[:, 0].astype(float)
            alts = data[:, 1].astype(float)
        elif type(data) in (tuple, list):
            data = np.array(list(map(np.array, data)), dtype=float).T
            data = data[(data[:, 0] > self.left) & (data[:, 1] > self.left)]
            data, inds, w = np.unique(data, axis=0, return_counts=True,
                                      return_inverse=True)
        else:
            data = data[(data[:, 0] > self.left) & (data[:, 1] > self.left)]
            if data.shape[1] > 2:
                refs = data[:, 0].astype(float)
                alts = data[:, 1].astype(float)
                w = data[:, 2]
                inds = None
            else:
                data, inds, w = np.unique(data.astype(int), axis=0,
                                          return_counts=True,
                                          return_inverse=True)
                refs = data[:, 0].astype(float)
                alts = data[:, 1].astype(float)
        self.inv_inds = inds
        self.orig_counts = np.hstack((data, w[:, np.newaxis]))
        w = w.astype(float)
        m = 0
        min_slice = int(alts.min())
        max_slice = int(alts.max())
        sizes = list()
        weights = list()
        inds_orig = list()
        for c in range(min_slice, max_slice + 1):
            inds = alts == c
            n = sum(inds)
            if not n:
                continue
            c_inds.extend([m] * n)
            cs.append(c)
            df.extend(refs[inds])
            weights.extend(w[inds])
            inds_orig.extend(np.where(inds)[0])
            sizes.append(n)
            m += 1
        cs = np.array(cs)
        c_inds = np.array(c_inds)
        df = np.array(df)
        weights = np.array(weights)
        if self.apply_weights:
            sizes = np.array(sizes, dtype=float)
            sizes /= sizes.sum()
            # sizes = sizes ** 2
            self.weights = weights / sizes[c_inds]
            # self.weights = np.ones_like(self.weights)
        else:
            self.weights = weights
        self.inds_orig = np.array(inds_orig)
        self.slices = cs
        self.slices_inds = c_inds
        params = self.parameters
        params.append(Parameter('w', [0.2, 0.8],
                                1.0 if self.bad == 1 else None, 
                                (0.0, 1.0), len(cs)))
        self.build(params, self.fix_params)
        self.update_starting_values(np.vstack([df, weights]).T)
        return np.vstack([df, self.weights]).T

    def update_starting_values(self, refs: np.ndarray):
        """
        Internal method. Retrieves starting values for parameters.

        Parameters
        ----------
        refs : np.ndarray
            Reference counts.

        Returns
        -------
        None.

        """
        slices = self.slices
        num_slices = len(slices)
        x0s = self.x0
        logging.debug('Computing starting values...')
        weights = list()
        inds = self.slices_inds
        sep_res = defaultdict(list)
        m = ModelMixture(self.bad, self.left, self.dist)
        len_cutoff = 500
        for i in range(num_slices):
            data = refs[inds == i]
            if data[:, -1].sum() < len_cutoff:
                continue
            p = m.fit(data, use_prev='only')
            if not m.last_result.success:
                continue
            sep_res['slice'].append(slices[i])
            for p, v in p.items():
                if type(v) not in (list, np.ndarray):
                    sep_res[p].append(v)
                else:
                    sep_res[p].extend(list(v))
            weights.append(len(data))
        if not weights:
            logging.warning("There is no slice with a number of samples"
                            f" greater than {len_cutoff} for BAD {self.bad}."
                            " Using default starting-values instead.")
            self.sep_res = sep_res
            return
        x0 = x0s[0].copy()
        slc_1d = np.array(sep_res['slice'])
        rs = np.array(sep_res['r'])
        sp = minimize_scalar(lambda p: np.log(linregress(slc_1d ** p,
                                                         rs).pvalue), 
                             (0.25, 2.0))
        self.slice_power = sp.x

        weights = np.array(weights, dtype=float)
        weights /= weights.sum()
        x = np.ones((len(slc_1d), 2), dtype=float)
        x[:, 0] = slc_1d ** self.slice_power
        try:
            i = self.params_active['w']
            ws = np.clip(np.poly1d(np.polyfit(slc_1d, sep_res['w'], 3,
                                              w=weights))(slices), 0.01, 0.99)
            x0[i] = ws
        except KeyError:
            pass
        if 'k' in sep_res:
            y = np.array(sep_res['k'])
            inds = y < 3900
            w = weights[inds]
            w /= w.sum()
            w = np.sqrt(w)
            y = w * y[inds]
            try:
                i = self.params_active['b_k']
                j = self.params_active['mu_k']
                y = y[:, np.newaxis]
                xt = x[inds, :] * w[:, np.newaxis]
                b, mu = (np.linalg.pinv(xt.T @ xt) @ xt.T @ y).flatten()
                x0[i] = b
                x0[j] = mu
            except KeyError:
                try:
                    x0[self.params_active['mu_k']] = np.mean(y)
                except KeyError:
                    pass
        try:
            i = self.params_active['b']
            j = self.params_active['mu']
            weights = np.sqrt(weights)
            x *= weights[:, np.newaxis]
            y = (weights * np.array(rs))[:, np.newaxis]
            b, mu = (np.linalg.pinv(x.T @ x) @ x.T @ y).flatten()
            x0[i] = b
            x0[j] = j
        except KeyError:
            pass
        x0s.append(x0)
        self.slice_res = sep_res
        self.x0 = x0s

    def fit(self, data, use_prev='add', min_samples=1, min_slice=0,
            max_slice=None, try_ests_only=True, **kwargs):
        """
        Fit model to data.

        Parameters
        ----------
        data : np.ndarray
            Array of shape number of observations x other dimensions.
        use_prev : str, optional
            If 'add', then a previous optima will be added to the pool of
            starting points. If 'only', then only the previous point will be
            used in optimization. If None or empty string, then previous points
            are ignored.
        try_ests_only : bool, optional
            If True and start_ests is True, then only the estimated starting
            point will tried at first (and if it fails, other starting
            points will be considered). All starting points are evaluated
            otherwise. The default is True.
        **kwargs : dict
            Extra arguments to be passed to the optimizer (if applicable).

        Returns
        -------
        res : dict
            Parameter estimates and loglikelihood.

        """
        data = self.load_dataset(data)
        if try_ests_only and self.start_est:
            tx = self.x0
            if len(tx) >= 2:
                self.x0 = [tx[-1], tx[-2]]
            elif len(tx) == 1:
                self.x0 = [tx[0]]
            else:
                self.x0 = list()
            r = super().fit(data, use_prev=use_prev, stop_first=True,
                            **kwargs)
            if type(r) is not dict and not np.isfinite(r):
                if len(tx) >= 2:
                    self.x0 = tx[:-2]
                elif len(tx) == 1:
                    self.x0 = tx[:-1]
                else:
                    self.x0 = list()
                r = super().fit(data, use_prev=use_prev, **kwargs)
            self.x0 = tx
        else:
            r = super().fit(data, use_prev=use_prev, **kwargs)
        self.inds = self.inds_orig[self.inv_inds]
        r['slice_power'] = self.slice_power
        if 'std' in r:
            r['std']['slice_power'] = '-'
        return r

    def logprob_mode(self, params: jnp.ndarray,
                     data: jnp.ndarray, p: float) -> jnp.ndarray:
        """
        Log probability of a single mode given parameters vector.
    
        Parameters
        ----------
        params : jnp.ndarray
            1d param vector.
        data : jnp.ndarray
            Data.
        p : float
            Rate prob.
    
        Returns
        -------
        Logprobs of data.
    
        """
        if len(data.shape) > 1:
            data = data[:, 0]
        inds = self.slices_inds
        slices = self.slices
        b = self.get_param('b', params)
        mu = self.get_param('mu', params)
        r = self.calc_r(slices, b, mu)
        r = r[inds]
        if self.dist == 'NB':
            lp = dist.LeftTruncatedNB.logprob
            lp = lp(data, r, p, self.left)
        elif self.dist == 'BetaNB':
            b = self.get_param('b_k', params)
            mu = self.get_param('mu_k', params)
            k = self.calc_k(slices, b, mu)
            k = k[inds]
            lp = dist.LeftTruncatedBetaNB.logprob
            lp = lp(data, p, k, r, self.left)
        return lp

    @partial(jit, static_argnums=(0,))
    def logprob(self, params: jnp.ndarray, data: jnp.ndarray) -> jnp.ndarray:
        """
        Log probability of data given a parameters vector.

        Should be jitted for the best performance.
        Parameters
        ----------
        paprams : jnp.ndarray
            1D param vector.
        data : jnp.ndarray
            Data.

        Returns
        -------
        Logprobs of data.

        """
        p1 = self.get_param('p1', params)
        if self.bad == 1:
            return self.logprob_mode(params, data, p1)
        else:
            p2 = self.get_param('p2', params)
            lp1 = self.logprob_mode(params, data, p1)
            lp2 = self.logprob_mode(params, data, p2)
            w = self.get_param('w', params)[self.slices_inds]
            return logsumexp(jnp.array([lp1, lp2]), axis=0,
                             b=jnp.array([w, 1.0 - w]))

    # @partial(jit, static_argnums=(0,))
    def logprob_modes(self, params: jnp.ndarray, data: jnp.ndarray) -> jnp.ndarray:
        """
        Modes probabilities of data given a parameters vector.

        Should be jitted for the best performance.
        Parameters
        ----------
        paprams : jnp.ndarray
            1D param vector.
        data : jnp.ndarray
            Data.

        Returns
        -------
        Tuple of probabilities, each for a mixture component.

        """
        p1 = self.get_param('p1', params)
        lp1 = self.logprob_mode(params, data, p1)
        if self.bad == 1:
            lp2 = lp1
        else:
            p2 = self.get_param('p2', params)
            lp2 = self.logprob_mode(params, data, p2)
        return lp1, lp2

    def get_sliced_params(self, params=None):
        if params is None:
            params = self.params
        else:
            if type(params) is not dict:
                params = self.vec_to_dict(params)
        b = params['b']
        mu = params['mu']
        if self.dist == 'BetaNB':
            bk = params['b_k']
            muk = params['mu_k']
        results = defaultdict(list)
        stds = params.get('std', dict())
        stds_res = defaultdict(list)
        for c in self.slices:
            for p in (f'w{c}', f'k{c}'):
                if p in params:
                    results[p[0]].append(params[p])
            for p in ('w', 'k'):
                if p in params:
                    pt = params[p]
                    if (not np.isscalar(pt)) and (len(pt) == len(self.slices)):
                        results[p].append(pt[list(self.slices).index(c)])
            r = self.calc_r(c, b, mu)
            results['r'].append(r)
            if self.dist == 'BetaNB':
                k = self.calc_k(c, bk, muk)
                results['k'].append(k)
            results['slice'].append(c)
        for p, v in stds.items():
            stds_res[p[0]].append(v)
        if stds_res:
            results['std'] = stds_res
        return results

    def calc_r(self, s, b, mu):
        return b * s ** self.slice_power + mu

    def calc_k(self, s, b, mu):
        return b * s + mu
        return b * np.log(s) + mu

    def mean(self, params=None):
        if params is None:
            params = self.last_result.x
        p1 = self.get_param('p1', params)
        inds = self.slices_inds
        slices = self.slices
        b = self.get_param('b', params)
        mu = self.get_param('mu', params)
        r = self.calc_r(slices, b, mu) 
        r = r[inds]
        w = self.get_param('w', params)
        if self.bad != 1:
            w = w[inds]
            p2 = self.get_param('p2', params)
        if self.dist == 'BetaNB':
            b = self.get_param('b_k', params)
            mu = self.get_param('mu_k', params)
            k = self.calc_k(slices, b, mu)
            k = k[inds]
            l1 = dist.LeftTruncatedBetaNB.mean(p1, k, r, self.left)
            if self.bad != 1:
                l2 = dist.LeftTruncatedBetaNB.mean(p2, k, r, self.left)
            else:
                l2 = l1
        else:
            l1 = dist.LeftTruncatedNB.mean(r, p1, self.left)
            if self.bad != 1:
                l2 = dist.LeftTruncatedNB.mean(r, p2, self.left)
            else:
                l2 = l1
        return w * l1 + (1.0 - w) * l2


    def sample(self, n=None, params=None, return_array=True, sampler_model=None, return_sampler_model=False):
        """
        Sample from the model given parameters.
    
        Parameters
        ----------
        n: dict
            Mapping: slice -> number of samplers. If None, then
        params : dict or np.ndarray, optional
            Parameters vector or dictionary. If None, then it is assumed that the model was fit and the fitted
            parameters are used. The default is None.
        return_array : bool, optional
            If False, then dict[fixed_allele_count] -> list of counts is returned. The default is True.
        sampler_model : ModelMixture, optional
            The model that will be used for an actual sampling. It is automatically created in the sample method
            if it is None. It might be reasonable to reuse it later instead of re-instantiating it each time if
            you plan to use sample actively. The default is None.
        return_sampler_model : bool, optional
            If True, the sample_model is also returned. The default is False.
    
        Returns
        -------
        np.ndarray
            Sampled values.
        """
        if params is None:
            params = self.last_result.x
        elif type(params) in (dict, defaultdict):
            params = self.dict_to_vec(params)
        if sampler_model is None:
            sampler_model = ModelMixture(self.bad, self.left, dist=self.dist, estimate_p=self.estimate_p, fix_params=self.fix_params)
        inds = self.slices_inds
        slices = self.slices
        if n is None:
            n = defaultdict(int)
            for s in slices[inds]:
                n[s] += 1
        pdict = dict()
        b, mu = self.get_param('b', params), self.get_param('mu', params)
        r = self.calc_r(slices, b, mu) 
        r = r[inds]
        if self.dist == 'BetaNB':
            bk, muk = self.get_param('b_k', params), self.get_params('mu_k', params)
            k = self.calc_k(slices, bk, muk)
            k = k[inds]
        p1 = self.get_param('p1', params)
        pdict['p1'] = p1
        if self.bad != 1:
            w = self.get_param('w', params)[inds]
            p2 = self.get_param('p2', params)
            pdict['p2'] = p2
        res = dict()
        for i, slc in enumerate(slices[inds]):
            pdict['r'] = r[i]
            if self.bad != 1:
                pdict['w'] = w[i]
            if self.dist == 'BetaNB':
                pdict['k'] = k[i]
            res[slc] = sampler_model.sample(n[slc], pdict)
        if return_array:
            counts = defaultdict(int)
            for alt, cnts in res.items():
                for main in cnts:
                    counts[(main, alt)] += 1
            res = list()
            for (main, alt) in sorted(counts.keys()):
                res.append((main, alt, counts[(main, alt)]))
            res = np.array(res, dtype=int)
        if return_sampler_model:
            return res, sampler_model
        return res
        