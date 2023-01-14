# -*- coding: utf-8 -*-
"""ModelLine in a sliding window."""
from .model import Model, Parameter
from .model_mixture import ModelMixture
from jax.scipy.special import logsumexp
from scipy.optimize import minimize
from .. import distributions as dist
from collections import defaultdict
from functools import partial
from gmpy2 import mpfr
from jax import jit
import jax.numpy as jnp
import pandas as pd
import numpy as np
import logging


class ModelWindow(Model):
    def __init__(self, bad: float, left: int, window_size=1000, min_slices=10,
                 window_behavior='both', dist='BetaNB', x0=None,
                 concentration='line', adjust_line=False,
                 estimate_p=False, fix_params=None, left_k=1,
                 start_est=True, apply_weights=False, regul_alpha=0.0, regul_n=True,
                 regul_slice=True, regul_prior='laplace'):
        """
        ModelWindow is effectively a ModelLine, but ran against data that is
        split into chunks of certain minimal sizes.

        This approach lacks rigiourness of the ModelLine, but might produce
        better fits as parameters are allowed for a greater variation within
        the whole dataset.
        Parameters
        ----------
        bad : float
            Background Allelic Dosage value.
        left : int
            Left-bound for truncation.
        window_size: int, optional
            Minimal required window size. The default is 1000.
        min_slices: int, optional
            Minimal number of slices per window. The default is 10.
        window_behavior: str, optional
            If 'both', then window is expanded in 2 directions. If 'right',
            then the window is expanded only to the right (except for cases
            when such an expansion is not possible but the minimal slice
            or window size requirement is not met). The default is 'both'.
        dist: str
            Distribution for mixture components. Can be either 'NB' or 'BetaNB'.
            The default is 'BetaNB'.
        concentration : str, optional
            Can be either 'line' or 'intercept'. If the latter, than concentration
            parameter is modeled as a single value for all slices. If 'line',
            then it is assumed that concentration behaves itself as b * s + mu,
            where b and mu are some parameters and s is a slice number. The
            default is 'line'.
        adjust_line : bool, optional
            If True, then line parameter beta and mu will reestimated without
            a loss of likelihood so they differ as little as possible with
            the previous b and mu estimates. The default is False.
        estimate_p : bool, optional
            If True, then p is estimated. If False, then then p's (plural) are
            fixed to [bad/(bad + 1), 1 / (bad + 1)]. The default is False.
        fix_params : dict, optional
            Mapping param_name -> fixed_value that will fix active parameters.
            The default is None.
        regul_alpha: float, optional
            Alpha multiplier of regularization/prior part of the objective
            function for the concentration parameter kappa. The default is 0.0.
        regul_n: bool, optional
            If True, then alpha is multiplied by a number of observations captured
            by a particular window. The default is True.
        regul_slice: bool, optional
           If True, then alpha is multiplied by an average slice number captured
           by a particular window. The default is True.
       regul_prior: bool, optional
           A name of prior distribution used to penalize small kappa values. Can
           be 'laplace' (l1) or 'normal' (l2). The default is 'laplace'.

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
        self.req_size = window_size
        self.adjust_line = adjust_line
        self.min_slices = min_slices
        self.window_behavior = window_behavior
        self.fix_params = fix_params if fix_params is not None else dict()
        self.dist = dist
        self.left_k = left_k
        self.regul_alpha = regul_alpha
        self.regul_n = regul_n
        self.regul_slice = regul_slice
        self.regul_prior = regul_prior
        parameters = [
            Parameter('w', [0.2, 0.8], None if bad != 1 else 1.0, (0.0, 1.0)),
            Parameter('b', [1.0, 0.1], None, (0.0, None)),
            Parameter('mu', [0.001], None, (0.0, None)),
            ]
        if dist.startswith('BetaNB'):
            parameters.append(Parameter('b_k', [0.0, 1.0], 0.0,
                                        (0.0, None)))
            parameters.append(Parameter('mu_k', [left_k + 1, max(1, left_k + 26.0)], None, (self.left_k, None)))
        p1 = Parameter('p1', [self.ps[0]],
                      None if estimate_p else self.ps[0], (0.0, 1.0))
        parameters.append(p1)
        if bad != 1:
            p2 = Parameter('p2', [self.ps[1]],
                           None if estimate_p else self.ps[1], (0.0, 1.0))
            parameters.append(p2)
        super().__init__(parameters, fix_params=fix_params,
                         jit_fim=True, use_masking=True,
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
        logging.debug('Preparing ModelWindow to work with a provided dataset.')
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
            data = data[[c_ref, c_alt]].values.astype(float)
            data, inds, w = np.unique(data, axis=0, return_counts=True,
                                      return_inverse=True)
            refs = data[:, 0]
            alts = data[:, 1]
        elif type(data) in (tuple, list):
            data = np.array(list(map(np.array, data)), dtype=int).T
            data = data[(data[:, 0] > self.left) & (data[:, 1] > self.left)]
            data, inds, w = np.unique(data, axis=0, return_counts=True,
                                      return_inverse=True)
            data = data.astype(float)
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
        if inds is None:
            self.orig_counts = data
        else:
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
            n = inds.sum()
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
        self.weights = weights
        self.inds_orig = np.array(inds_orig)
        self.slices = cs
        self.slices_inds = c_inds
        tcs = cs[c_inds]
        slice_inds = list()
        req_size = self.req_size
        max_sz = 0
        min_slices = self.min_slices
        for i, s in enumerate(cs):
            inds = tcs == s
            n = weights[inds].sum()
            c = 1
            l = i - 1
            r = i + 1
            if self.window_behavior == 'right':
                while (r < len(sizes)) and (n < req_size or c < min_slices):
                    inds = inds | (tcs == cs[r])
                    n = weights[inds].sum()
                    r += 1
                    c += 1
                while (n < req_size or c < min_slices):
                    inds = inds | (tcs == cs[l])
                    n = weights[inds].sum()
                    l -= 1
                    c += 1
            else:
                while (n < req_size or c < min_slices) and (l >= 0 or r < len(sizes)):
                    if r < len(sizes):
                        inds = inds | (tcs == cs[r])
                        n = weights[inds].sum()
                        r += 1
                        c += 1
                    if l >= 0 and (n < req_size or c < min_slices):
                        inds = inds | (tcs == cs[l])
                        n = weights[inds].sum()
                        l -= 1
                        c += 1
            slice_inds.append((c, inds))
            max_sz = max(max_sz, inds.sum())
        self.mask = np.ones(max_sz, dtype=bool)
        self.slices_at_window = slice_inds
        return np.vstack([df, tcs, self.weights]).T

    def _fit(self, data, use_prev='only', calc_std=False, stop_first=False, prior_arg=1.0,
             param_mask=None, **kwargs):
        """
        Fit model to data.

        Parameters
        ----------
        data : np.ndarray
            Array of shape (number of observations x 3), where columns are ref
            counts, alt counts and number of occurences.
        use_prev : str, optional
            If 'add', then a previous optima will be added to the pool of
            starting points. If 'only', then only the previous point will be
            used in optimization. If None or empty string, then previous points
            are ignored.
        calc_std : bool, optional
            If True, then standard deviations of parameter estimates are
            calculated. The default is False.
        stop_first : bool, optional
            If True, the procedure stops at the first successful optimization.
            The default is False.
        **kwargs : dict
            Extra arguments to be passed to the optimizer (if applicable).

        Returns
        -------
        params : dict
            Dictionary of estimated parameters and loglikelihood.

        """
        assert data.shape[1] == 3, data.shape
        weights = data[:, -1]
        data = data[:, :-1]
        df, weights, mask = self.update_mask(data, weights)
        
        jac = partial(self.grad_loglik, data=df, mask=mask,
                      weights=weights, prior_arg=prior_arg, 
                      param_mask=param_mask)
        fun = partial(self.negloglikelihood, data=df, mask=mask,
                      weights=weights, prior_arg=prior_arg,
                      param_mask=param_mask)
        best_r = None
        best_loglik = -np.inf
        x0s = self.x0
        if use_prev and hasattr(self, 'params'):
            prev = [self.prepare_start(self.last_result.x)]
            x0s = prev + x0s
            prev_succ = self.last_result.success
        else:
            prev_succ = False
        for i, x0 in enumerate(x0s):
            logging.debug(f'Fitting model to data: starting point {i}/{len(x0s)}.')
            r = minimize(fun, x0, jac=jac, method='SLSQP',
                         bounds=self.bounds, options={'maxiter': 1000, 'disp': False,
                                                      'ftol': 1e-12}
                         )
            loglik = -r.fun
            if loglik > best_loglik:
                best_loglik = loglik
                best_r = r
                if r.success and ((prev_succ and use_prev == 'only') or stop_first):
                    break
        if best_r is None or not best_r.success:
            logging.debug("Optimizer didn't converge.")
        if best_r is None:
            return np.nan
        params = self.vec_to_dict(best_r.x)
        params['loglik'] = float(best_loglik) / sum(weights)
        params['success'] = best_r.success
        self.params = params
        self.last_result = best_r
        self.prev_res = self.last_result.x
        if calc_std:
            cov = self.calc_cov(df, weights=weights, params=best_r.x,
                                mask=mask)
            stds = {p: v for p, v in zip (self.params_active,
                                          np.sqrt(np.diag(cov)))}
            params['std'] = stds
        return params
    
    @partial(jit, static_argnums=(0, ))
    def prior(self, params: jnp.ndarray, data: jnp.ndarray, mask=None, weights=None, prior_arg=1.0):
        if not self.regul_alpha:
            return 0.0
        regm = self.regul_alpha
        if self.regul_n:
            regm *= jnp.where(mask, 0.0, weights).sum()
        if self.regul_slice:
            regm *= prior_arg # jnp.where(mask, 0.0, data[:, 1]).sum() / (~mask).sum()
        if self.regul_prior == 'laplace':
            return -regm / params[-1] - 2 * jnp.log(params[-1])
        elif self.regul_prior == 'normal':
            return -regm / params[-1] ** 2 - 2 * jnp.log(params[-1])

    def fit(self, data, calc_std=True, **kwargs):
        """
        Fit model to data.

        Parameters
        ----------
        data : np.ndarray
            Array of shape number of observations x other dimensions.
        **kwargs : dict
            Extra arguments to be passed to the optimizer (if applicable).

        Returns
        -------
        res : dict
            Parameter estimates and loglikelihood.

        """
        data = self.load_dataset(data)
        self.data = data
        ests = dict()
        fix_params = self.fix_params
        if not self.x0:
            self.prev_res = []
            self.params = ests
            if calc_std:
                ests['std'] = dict()
            return ests
        if 'mu' in fix_params:
            fix_params['r'] = fix_params['mu']
        if 'mu_k' in fix_params:
            fix_params['k'] = fix_params['mu_k']
        # mod_single = ModelMixture(self.bad, self.left, self.dist,
        #                           estimate_p=self.estimate_p,
        #                           fix_params=self.fix_params,
        #                           left_k=self.left_k,
        #                           regul_alpha=self.regul_alpha,
        #                           regul_n=self.regul_n,
        #                           regul_slice=self.regul_slice,
        #                           regul_prior=self.regul_prior)
        # mod_single.mask = self.mask
        first_line = True
        prev_r = None
        self._lambda = 1.0
        prev_slc = None
        param_mask = np.ones_like(self.x0[0], dtype=float)
        try:
            self.set_param('mu', param_mask, 0.0)
        except KeyError:
            pass
        for s, (n, slc) in zip(self.slices, self.slices_at_window):
            tdata = data[slc]
            if n > 1:
                try:
                    self.set_param('mu', param_mask, 1.0)
                except KeyError:
                    pass
            # if n > 0:
            if prev_slc is not None and np.all(prev_slc == slc):
                r = prev_r
            else:
                if hasattr(self, 'prev_res'):
                    prev_res = self.prev_res
                    if first_line:
                        prev_res[prev_res == 0] += 0.001
                else:
                    prev_res = None
                    
                r = self._fit(tdata, calc_std=calc_std, use_prev='add' if first_line else 'only',
                              prior_arg=s, param_mask=param_mask)
                if type(r) in (float, np.float64, np.float128, np.float32):
                    logging.warning(f'Total optimization failure at slice {s} for slices {slc}.'
                                    ' Thats likely due to very low coverage and fits are meaningless'
                                    ' regardless of whether optimization was reported successful or not.'
                                    ' Using previous fit.')
                    if prev_r is None:
                        raise Exception('No previous fit found.')
                    else:
                        r = prev_r
                else:
                    prev_r = r
                    prev_slc = slc
            first_line = False
            if prev_res is not None and self.adjust_line:
                _prev_res = [self.get_param('b', prev_res),
                            self.get_param('mu', prev_res)]
                _cur_res = [r.get('b', 0.0), r.get('mu', 0.0)]
                adj = self.adjust_line_params(_cur_res, _prev_res,
                                              np.unique(tdata[:, 1]),
                                              self.calc_r)
                if adj.success:
                    try:
                        self.set_param('b', self.prev_res, adj.x[0])
                        r['b'] = adj.x[0]
                    except KeyError:
                        pass
                    try:
                        self.set_param('mu', self.prev_res, adj.x[1])
                        r['mu'] = adj.x[1]
                    except KeyError:
                        pass
            if self.dist == 'BetaNB' and 'b_k' not in r:
                r['b_k'] = 0.0
            if n == 1 and 'mu' in r:
                r['mu'] = 0
                if 'std' in r:
                    r['std']['mu'] = 0
            for p, est in r.items():
                if p == 'std':
                    if p not in ests:
                        d = dict()
                        ests[p] = d
                    else:
                        d = ests[p]
                    for p, std in est.items():
                        d[f'{p}{s}'] = std
                else:
                    ests[f'{p}{s}'] = est
            # else:
            #     t = tdata[0, 1]
            #     tdata = tdata[:, [0, 2]]
            #     r = mod_single.fit(tdata, use_prev='only', prior_arg=s, calc_std=calc_std)
            #     tr = r['r']
            #     # r['r'] = t
            #     # if 'w' in r:
            #     #     r['w'] = max(0.01, r['w'] - 0.05)
            #     # mod_single.prev_res = mod_single.dict_to_vec(r)
            #     b = tr / t
            #     r['b'] = b * 0.95
            #     r['mu'] = 0.05 * tr
            #     del r['r']
            #     if self.dist == 'BetaNB':
            #         r['b_k'] = 0.0 
            #         r['mu_k'] = r['k']
            #         del r['k']
            #     self.prev_res = self.dict_to_vec(r)
            #     r['b'] = 0
            #     r['mu'] = b * t
            for p, est in r.items():
                if not p.startswith(('succ', 'loglik', 'std')):
                    ests[f'{p}{s}'] = est
        self.params = ests
        return ests

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
        data, slices = data[:, 0], data[:, 1]
        b = self.get_param('b', params)
        mu = self.get_param('mu', params)
        if self.dist == 'Binom':
            slices = slices + data
        r = self.calc_r(slices, b, mu)
        if self.dist == 'NB':
            lp = dist.LeftTruncatedNB.logprob
            lp = lp(data, r, p, self.left)
        elif self.dist == 'BetaNB':
            b = self.get_param('b_k', params)
            mu = self.get_param('mu_k', params)
            k = self.calc_k(slices, b, mu)
            lp = dist.LeftTruncatedBetaNB.logprob
            lp = lp(data, p, k, r, self.left)
        elif self.dist == 'Binom':
            lp = dist.LeftTruncatedBinom.logprob
            lp = lp(data, r, p, self.left)
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
        #data = data[:, 0]
        p1 = self.get_param('p1', params)
        if self.bad == 1:
            return self.logprob_mode(params, data, p1)
        else:
            p2 = self.get_param('p2', params)
            lp1 = self.logprob_mode(params, data, p1)
            lp2 = self.logprob_mode(params, data, p2)
            w = self.get_param('w', params)
            return logsumexp(jnp.array([lp1, lp2]).T, axis=1,
                             b=jnp.array([w, 1.0 - w]))

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
        results = defaultdict(list)
        stds = params.get('std', dict())
        stds_res = defaultdict(list)
        for c in self.slices:
            for p in (f'w{c}', f'k{c}', f't{c}'):
                if p in params:
                    results[p[0]].append(params[p])
            b = params.get(f'b{c}', 0.0)
            mu = params[f'mu{c}']
            results['b'].append(b)
            results['mu'].append(mu)
            r = self.calc_r(c, b, mu)
            results['r'].append(r)
            if self.dist.startswith('BetaNB'):
                b = params.get(f'b_k{c}', 0.0)
                mu = params[f'mu_k{c}']
                results['b_k'].append(b)
                results['mu_k'].append(mu)
                k = self.calc_k(c, b, mu)
                results['k'].append(k)
                if '-NB' in self.dist:
                    b = params.get(f'b_c{c}', 0.0)
                    mu = params[f'mu_c{c}']
                    results['b_c'].append(b)
                    results['mu_c'].append(mu)
                    r = self.calc_r(c, b, mu)
                    results['r_c'].append(r)
            results['slice'].append(c)
        for p, v in stds.items():
            stds_res[p[0]].append(v)
        if stds_res:
            results['std'] = stds_res
        return results

    def calc_r(self, s, b, mu):
        return b * s + mu

    def calc_k(self, s, b, mu):
        return b * jnp.log(s) + mu

    def mean(self, params=None):
        raise NotImplementedError

    def adjust_line_params(self, cur_est, prev_est, x, fun, eps=1e-1):
        prev_fun = fun(x, *cur_est)
        eps *= len(x)
        con = lambda p: -np.sum((fun(x, *p) - prev_fun) ** 2) + eps
        x0 = np.array(list(np.array(prev_est).flatten())) #+ [1.0, 0.0])
        cur_est = np.array(cur_est)
        prev_est = np.array(prev_est)
        def min_fun(p):
            diff = np.sum((p - prev_est) ** 2)
            return diff #+ p[-2] * ineq
        return minimize(min_fun, x0, 
                        constraints=[{'type': 'ineq', 'fun': con}])
