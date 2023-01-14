# -*- coding: utf-8 -*-
"""Mixture of 2 (beta)-negative-binomial models that models all slices simultaneously.
No standard deviations from r-line are allowed. 
A variant for efficient logratio computation due to some JAX-limitations."""
from .model_line import ModelLine
from .model import Model, Parameter
from scipy.optimize import minimize_scalar
from scipy.stats import linregress
from jax.scipy.special import logsumexp
from .. import distributions as dist
from collections import defaultdict
from typing import List
from functools import partial
from gmpy2 import mpfr
from jax import jit, lax
import jax.numpy as jnp
import pandas as pd
import numpy as np
import logging


class ModelLine_(ModelLine):

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
       b = lax.stop_gradient(self.get_param('b', params))
       mu = lax.stop_gradient(self.get_param('mu', params))
       slices = data[:, 1]
       data = data[:, 0]
       r = self.calc_r(slices, b, mu)
       if self.dist == 'NB':
           lp = dist.LeftTruncatedNB.logprob
           lp = lp(data, r, p, self.left)
       elif self.dist == 'BetaNB':
           b = lax.stop_gradient(self.get_param('b_k', params))
           mu = lax.stop_gradient(self.get_param('mu_k', params))
           k = self.calc_k(slices, b, mu)
           lp = dist.LeftTruncatedBetaNB.logprob
           lp = lp(data, p, k, r, self.left)
       return lp

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
       data = super().load_dataset(data)
       if hasattr(self, 'x0_override'):
           self.x0_old = self.x0
           self.x0 = self.x0_override
       cs = self.slices[self.slices_inds]
       return np.vstack((data[:, 0], cs, data[:, -1])).T

   def override_start(self, x: List[np.ndarray]):
       self.x0_override = x

   def update_starting_values(self, refs: np.ndarray):
       pass
  
   # @partial(jit, static_argnums=(0, ))
   # def negloglikelihood(self, params: jnp.ndarray,
   #                       data: jnp.ndarray, mask=None,
   #                       weights=None, prior_arg=1.0) -> jnp.ndarray:
   #     full_params = prior_arg
   #     self.set_param('p1', full_params, params[0])
   #     lp = self.logprob(params, data)
   #     lp = jnp.where(~jnp.isfinite(lp), np.nan, lp)
   #     if weights is not None:
   #         lp *= weights 
   #     if self.use_masking:
   #         return -jnp.where(mask, 0.0, lp).sum()
   #     else:
   #         return -lp.sum()