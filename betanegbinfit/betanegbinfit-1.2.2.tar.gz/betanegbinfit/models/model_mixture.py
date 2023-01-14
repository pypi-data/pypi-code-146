# -*- coding: utf-8 -*-
"""Mixture of two (beta)negative-binomial components."""
from .. import distributions as dist
from functools import partial
from .model import Model, Parameter
from jax.scipy.special import logsumexp
from jax import jit
import jax.numpy as jnp
import numpy as np
from gmpy2 import mpfr
from collections import defaultdict


class ModelMixture(Model):
    def __init__(self, bad: float, left: int, dist='BetaNB',
                 estimate_p=False, regul_alpha=0.0, regul_n=True,
                 regul_slice=True, regul_prior='laplace', fix_params=None,
                 use_masking=True, left_k=1):
        """
        Construct a (Beta)Negative-Binomial mixture model.

        w * F(bad/(bad + 1), r,...) + (1 - w) F(1/(bad + 1), r,...)
        w and r are active parameters. F is either NB or BetaNB, both are
        left-truncated.
        Parameters
        ----------
        dist: str
            Distribution for mixture components. Can be either 'NB' or 'BetaNB'.
            The default is 'BetaNB'.
        bad : float, optional
            Background Allelic Dosage value.
        left : int, optional
            Left-bound for truncation.
        estimate_p : bool, optional
            If True, then p is estimated. If False, then then p's (plural) are
            fixed to [bad/(bad + 1), 1 / (bad + 1)]. The default is False.
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
        fix_params : dict, optional
            Mapping param_name -> fixed_value that will fix active parameters.
            The default is None.
        use_masking : bool, optional
            Masking and padding will be used to avoid JIT performance penalty
            due to changing data vector lengths. Usually results in a much
            greater performance. If True, it is advised to start with
            the most abudant with observations piece of data. The default is
            True.

        Returns
        -------
        None.

        """
        self.bad = bad
        self.left = left
        bad = mpfr(str(bad))
        self.ps = np.array([float(bad / (bad + 1)), float(1 / (bad + 1))])
        self.dist = dist
        parameters = [
            Parameter('r', [left + 1, 2 * (left + 1), (left + 1) * 5, (left + 1) * 10], None, (0.1, None)),
            Parameter('w', [0.02, 0.3, 0.7, 0.98], 1 if bad == 1 else None, (0.0, 1.0)),       
            ]
        p1 = Parameter('p1', [self.ps[0]],
                      None if estimate_p else self.ps[0], (0.0, 1.0))
        parameters.append(p1)
        if bad != 1:
            p2 = Parameter('p2', [self.ps[1]],
                           None if estimate_p else self.ps[1], (0.0, 1.0))
            parameters.append(p2)
        if dist == 'BetaNB':
            m = left_k + 26.0
            parameters.append(Parameter('k', [m, 10 * m], None,
                                        (left_k, None)))
        self.estimate_p = estimate_p
        self.regul_alpha = regul_alpha
        self.regul_n = regul_n
        self.regul_slice = regul_slice
        self.regul_prior = regul_prior
        super().__init__(parameters=parameters, use_masking=use_masking,
                         fix_params=fix_params, _allowed_const=left + 1)

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
        r = self.get_param('r', params)
        if len(data.shape) > 1:
            data = data[:, 0]
        if self.dist == 'NB':
            lp = dist.LeftTruncatedNB.logprob
            lp = lp(data, r, p, self.left)
        elif self.dist == 'BetaNB':
            k = self.get_param('k', params)
            lp = dist.LeftTruncatedBetaNB.logprob
            lp = lp(data, p, k, r, self.left)
        elif self.dist == 'Binom':
            lp = dist.LeftTruncatedNB.logprob
            lp = lp(data, r, p, self.left)
        return lp
    
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
    
    def prob_mode(self, params: jnp.ndarray,
                     data: jnp.ndarray, p: float) -> jnp.ndarray:
        """
        PMF of a single mode given parameters vector.

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
        Probs of data.

        """
        r = self.get_param('r', params)
        data = np.array(data)
        if len(data.shape) > 1:
            data = data[:, 0]
        if self.dist == 'NB':
            pmf = dist.LeftTruncatedNB.long_prob
            pmf = pmf(data, r, p, self.left)
        elif self.dist == 'BetaNB':
            k = self.get_param('k', params)
            pmf = dist.LeftTruncatedBetaNB.long_prob
            pmf = pmf(data, p, k, r, self.left)
        elif self.dist == 'Binom':
            pmf = dist.LeftTruncatedBinom.long_prob
            pmf = pmf(data, r, p, self.left)
        return pmf
    
    def prob_modes(self, params: jnp.ndarray, data: list) -> list:
        """
        Modes PMFs of data given a parameters vector.

        Parameters
        ----------
        paprams : jnp.ndarray
            1D param vector.
        data : list
            Data.

        Returns
        -------
        Tuple of PMFs, each for a mixture component.

        """
        p1 = self.get_param('p1', params)
        pmf1 = self.prob_mode(params, data, p1)
        if self.bad == 1:
            pmf2 = pmf1
        else:
            p2 = self.get_param('p2', params)
            pmf2= self.prob_mode(params, data, p2)
        return pmf1, pmf2


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
            w = self.get_param('w', params)
            p2 = self.get_param('p2', params)
            lp1 = self.logprob_mode(params, data, p1)
            lp2 = self.logprob_mode(params, data, p2)
            return logsumexp(jnp.array([lp1, lp2]).T, axis=1,
                             b=jnp.array([w, 1-w]))

    @partial(jit, static_argnums=(0,))
    def logprob_modes(self, params: jnp.ndarray,
                      data: jnp.ndarray) -> jnp.ndarray:
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
    
    def cdf_mode(self, params: jnp.ndarray,
                     data: list, p: float) -> list:
        """
        cdf of a single mode given parameters vector.

        Parameters
        ----------
        params : jnp.ndarray
            1d param vector.
        data : list
            Data.
        p : float
            Rate prob.

        Returns
        -------
        cdf of data.

        """
        r = self.get_param('r', params)
        if self.dist == 'NB':
            lp = dist.LeftTruncatedNB.long_cdf
            lp = lp(data, r, p, self.left)
        elif self.dist == 'BetaNB':
            k = self.get_param('k', params)
            lp = dist.LeftTruncatedBetaNB.long_cdf
            lp = lp(data, p, k, r, self.left)
        elif self.dist == 'Binom':
            lp = dist.LeftTruncatedNB.long_cdf
            lp = lp(data, r, p, self.left)
        return lp
    
    def cdf_modes(self, params: jnp.ndarray,
                      data: list) -> list:
        """
        Modes cdfs of data given a parameters vector.

        Parameters
        ----------
        paprams : jnp.ndarray
            1D param vector.
        data : list
            Data.

        Returns
        -------
        Tuple of cdfs, each for a mixture component.

        """
        p1 = self.get_param('p1', params)
        lp1 = self.cdf_mode(params, data, p1)
        if self.bad == 1:
            lp2 = lp1
        else:
            p2 = self.get_param('p2', params)
            lp2 = self.cdf_mode(params, data, p2)
        return lp1, lp2

    def mean(self, params=None, return_modes=False):
        if params is None:
            params = self.last_result.x
        p1 = self.get_param('p1', params)
        if self.bad == 1:
            p2 = p1
        else:
            p2 = self.get_param('p2', params)
        w = self.get_param('w', params)
        r = self.get_param('r', params)
        if self.dist == 'BetaNB':
            k = self.get_param('k', params)
            l1 = dist.LeftTruncatedBetaNB.mean(p1, k, r, self.left)
            if self.bad == 1:
                l2 = l1
            else:
                l2 = dist.LeftTruncatedBetaNB.mean(p2, k, r, self.left)
        else:
            l1 = dist.LeftTruncatedNB.mean(r, p1, self.left)
            if self.bad == 1:
                l2 = l1
            else:
                l2 = dist.LeftTruncatedNB.mean(r, p2, self.left)
        if return_modes:
            return l1, l2
        return w * l1 + (1.0 - w) * l2

    def sample(self, n: int, params=None):
        """
        Sample from the model given parameters.

        Parameters
        ----------
        n: int
            Number of samples.
        params : dict or np.ndarray, optional
            Parameters vector or dictionary. If None, then it is assumed that the model was fit and the fitted
            parameters are used. The default is None.

        Returns
        -------
        np.ndarray
            Sampled values.
        """
        
        if params is None:
            params = self.last_result.x
        elif type(params) in (dict, defaultdict):
            params = self.dict_to_vec(params)
        r = self.get_param('r', params)
        p1 = self.get_param('p1', params)
        if self.dist == 'BetaNB':
            k = self.get_params('k', params)
            sampler = lambda p, n: dist.LeftTruncatedBetaNB.sample(p, k, r, self.left, n)
        elif self.dist == 'NB':
            sampler = lambda p, n: dist.LeftTruncatedNB.sample(r, p, self.left, n)
        s1 = sampler(p1, n)
        if self.bad == 1:
            return s1
        p2 = self.get_param('p2', params)
        s2 = sampler(p2, n)
        w = self.get_param('w', params)
        w = np.random.choice([1, 0], size=n, p=[w, 1 - w])
        return w * s1 + (1 - w) * s2
