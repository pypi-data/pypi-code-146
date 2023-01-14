# -*- coding: utf-8 -*-
"""Abstract model class that is inherited by all the other models."""
from abc import abstractmethod, ABC
from scipy.optimize import minimize
from dataclasses import dataclass
from functools import partial
from jax import jit, grad, jacfwd
from itertools import product
import jax.numpy as jnp
import numpy as np
import logging


@dataclass
class Parameter:
    """Structure for basic parameter info used internally in Model."""

    name: str
    starts: list
    value: float
    bound: tuple
    size: int = 1

@dataclass
class _OptimizeResult:
    """Structure for imitating scipy optimize result. For internal usage only."""
    
    fun: float
    success: bool
    x: np.ndarray

class Model(ABC):
    def __init__(self, parameters: list, use_masking=True, jit_fim=True,
                 fix_params=None, _allowed_const=5, ):
        """
        Construct an abstract Model instantance.

        This is not supposed to be used by anyone.
        Parameters
        ----------
        x0 : list[jnp.ndarray]
            List of starting points.
        parameters: list[Parameter]
            List of parameters info to embed into the model.
        use_masking : bool, optional
            Masking and padding will be used to avoid JIT performance penalty
            due to changing data vector lengths. Usually results in a much
            greater performance. If True, it is advised to start with
            the most abudant with observations piece of data. The default is
            True.
        jit_fim : bool, optional
            If True, then Fisher Information Matrix is jitted. The issue is
            that it takes some time and pre-compiling might be feasible only
            if one want to run model multiple times. The default is True.
        fix_params : dict, optional
            Mapping param_name -> fixed_value that will fix active parameters.
            The default is None.
        _allowed_const : int, optional
            Constant that is used for padding if use_masking is True. The
            default is 5.

        Returns
        -------
        None.

        """
        self._allowed_const = _allowed_const
        self.build(parameters, fix_params)
        self.grad_loglik = jit(grad(self.negloglikelihood, argnums=(0, )))
        if jit_fim:
            self.calc_fim = jit(jacfwd(self.grad_loglik, argnums=(0, )))
        else:
            self.calc_fim = jacfwd(self.grad_loglik, argnums=(0,))
        self.use_masking = use_masking
        self.weights = None
        if use_masking:
            self.mask = np.zeros(0)

    def build(self, params: list, fix_params=None):
        """
        Build model structures from a list of parameters.

        Parameters
        ----------
        params : list[Parameter]
            A list of parameters.
        fix_params : dict, optional
            Mapping param_name -> fixed_value that will fix active parameters.
            The default is None.

        Returns
        -------
        None.

        """
        bounds = list()
        fixed = dict()
        active = dict()
        starts = list()
        if fix_params:
            for p in params:
                try:
                    p.value = fix_params[p.name]
                except KeyError:
                    continue
        i = 0
        for param in params:
            if param.value is None:
                size = param.size
                b = param.bound
                if b is None:
                    b = (None, None)
                bounds.extend([b] * size)
                if size > 1:
                    active[param.name] = slice(i, i + size)
                    start = list()
                    for s in param.starts:
                        start.append([s] * size)
                    starts.append(start)
                else:
                    active[param.name] = i
                    starts.append(param.starts)
                i += size
            else:
                fixed[param.name] = param.value
        x0 = list()
        for t in product(*starts):
            t0 = list()
            for item in t:
                if type(item) is list:
                    t0.extend(item)
                else:
                    t0.append(item)
            if t0:
                x0.append(np.array(t0, dtype=float))
        self.x0 = x0
        self.bounds = bounds
        self.params_fixed = fixed
        self.params_active = active
        self.num_params = i


    def get_param(self, name: str, vals: np.ndarray):
        """
        Retrieve parameter value by its name.

        Parameters
        ----------
        name : str
            Parameter name.
        vals : np.ndarray
            List of active parameter values. If the parameter of interest is
            not active, then it can be None.

        Returns
        -------
        float
            Parameter value.

        """
        try:
            return vals[self.params_active[name]]
        except KeyError:
            return self.params_fixed[name]

    def set_param(self, name: str, vals: np.ndarray, x, fixed=False):
        """
        Set parameter to some value by its name.

        Parameters
        ----------
        name : str
            Parameter name.
        vals : np.ndarray
            List of active parameter values. If the parameter of interest is
            not active, then it can be None.
        x : float or np.ndarray
            Value.
        fixed : bool, optional
            If True, then setting fixed values is allowed. The default is
            False;

        Returns
        -------
        None.

        """
        try:
            vals[self.params_active[name]] = x
        except KeyError:
            if fixed:
                self.params_fixed[name] = x
            else:
                raise KeyError(f"Unknown active parameter {name}.")

    def fit(self, data, use_prev='add', calc_std=False, stop_first=False, slsqp=True, prior_arg=1.0, **kwargs):
        """
        Fit model to data.

        Parameters
        ----------
        data : np.ndarray
            Array of shape (number of observations x 1 or 2). If shape of the
            latter dimension is 2, then it is assumed the first column contains
            only unique values and the second one consists of counts.
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
        slsqp: bool, optional
            If True, then SLSQP is used instead of L-BFGS-B.Then in case of SLSQP failure L-BFGS-B will be attempted
            instead. The default is True.
        **kwargs : dict
            Extra arguments to be passed to the optimizer (if applicable).

        Returns
        -------
        params : dict
            Dictionary of estimated parameters and loglikelihood.

        """
        if len(data.shape) == 1 or data.shape[1] == 1:
            data, self.inv_inds, weights = np.unique(data,
                                                     return_counts=True,
                                                     return_inverse=True)
            self.data = np.hstack((data, weights)).T
        else:
            self.data = data
            data, weights = data[:, :-1], data[:, -1]

        df, weights, mask = self.update_mask(data, weights)
        jac = partial(self.grad_loglik, data=df, mask=mask,
                      weights=weights, prior_arg=prior_arg)
        fun = partial(self.negloglikelihood, data=df, mask=mask,
                      weights=weights, prior_arg=prior_arg)
        best_r = None
        best_loglik = -np.inf
        x0s = self.x0
        if use_prev and hasattr(self, 'params'):
            prev_succ = self.last_result.success
            prev = [self.prepare_start(self.last_result.x)]
            x0s = prev + x0s
        else:
            prev_succ = False
        r = None
        for i, x0 in enumerate(x0s):
            logging.debug(f'Fitting model to data: starting point {i}/{len(x0s)}.')
            if not slsqp:
                r = minimize(fun, x0, jac=jac, method='L-BFGS-B',
                             bounds=self.bounds, 
                             options={'maxiter': 1000, 'disp': False,
                                      'maxcor': 30, 'gtol': 1e-10, 'ftol': 1e-12})
            else:
                r = minimize(fun, x0, jac=jac, method='SLSQP',
                             bounds=self.bounds, 
                             options={'maxiter': 1000, 'disp': False})
            loglik = -r.fun
            if loglik > best_loglik:
                best_loglik = loglik
                best_r = r
                if r.success and ((use_prev == 'only' and prev_succ) or stop_first):
                    break
        if not x0s:
            x = np.array([])
            best_r = _OptimizeResult(fun=-fun(x), success=True, x=x)
            best_loglik = best_r.fun
        if best_r is None or not best_r.success:
            logging.debug("Optimizer didn't converge.")
            if slsqp:
                return Model.fit(self, self.data, use_prev=use_prev, calc_std=calc_std, stop_first=stop_first,
                                  slsqp=False, **kwargs)
        if best_r is None:
            return np.nan
        params = self.vec_to_dict(best_r.x)
        self.last_result = best_r
        if calc_std:
            cov = self.calc_cov(df, weights=weights, params=best_r.x,
                                mask=mask)
            stds = np.sqrt(np.diag(cov))
            stds = {p: stds[i] for p, i in self.params_active.items()}
            params['std'] = stds
        params['loglik'] = float(best_loglik) 
        params['success'] = best_r.success
        self.params = params
        return params

    def prepare_start(self, start: np.ndarray, standoff=0.04,
                      eps=0.01) -> np.ndarray:
        start = start.copy()
        bounds = self.bounds
        for i, ((a, b), v) in enumerate(zip(bounds, start)):
            if a is not None and b is not None:
                t = (v - a) / (b - a) 
                if t < standoff:
                    start[i] = a + (b - a) * standoff
                elif t > (1 - standoff):
                    start[i] = b - (b - a) * standoff
            elif a is not None:
                if (v - a) < eps:
                    start[i] = eps
            elif b is not None:
                if (b - v) < eps:
                    start[i] = eps
        return start


    def update_mask(self, data, weights):
        df = data
        mask = None
        if self.use_masking:
            mask = self.mask
            if len(data) > len(mask):
                mask = np.zeros(len(data) * 2, dtype=bool)
                self.mask = mask
            mask[:len(data)] = False
            mask[len(data):] = True
            npad = [(0, len(mask) - len(data))]
            try:
                npad = npad + [(0, 0)] * (data.shape[1] - 1)
            except IndexError:
                pass
            df = np.pad(data, npad,
                        constant_values=self._allowed_const)
            weights = np.pad(weights, (0, len(mask) - len(data)))
        return df, weights, mask
        

    def calc_cov(self, data=None, weights=None, params=None, mask=None,
                 update_mask=True, return_fim=False):
        if data is None:
            data = self.weights
            weights = data[:, 1]
            data = data[:, 0]
        elif  weights is None:
            if len(data.shape) == 1 or data.shape[1] == 1:
                data, self.inv_inds, weights = np.unique(data,
                                                         return_counts=True,
                                                         return_inverse=True)
            else:
                data, weights = data[:, 0], data[:, -1]
        if params is None:
            params = self.last_result.x
        if mask is None and update_mask:
            data, weights, mask = self.update_mask(data, weights)
        fim = self.calc_fim(params, data=data, mask=mask,
                            weights=weights)[0][0]
        if return_fim:
            return fim
        try:
            return np.linalg.pinv(fim)
        except np.linalg.LinAlgError:
            return np.identity(fim.shape[0])


    @abstractmethod
    def logprob(self, params: jnp.ndarray, data: jnp.ndarray) -> jnp.ndarray:
        """
        Logprobability of data given a parameters vector.

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
        pass

    # @partial(jit, static_argnums=(0, ))
    def prior(self, params: jnp.ndarray, data: jnp.ndarray, mask=None, weights=None, prior_arg=1.0):
        return 0.0

    @partial(jit, static_argnums=(0, ))
    def negloglikelihood(self, params: jnp.ndarray,
                         data: jnp.ndarray, mask=None,
                         weights=None, prior_arg=1.0, param_mask=None) -> jnp.ndarray:
        """
        Negative loglikelihood of data given a parameters vector.

        Should be jitted for the best performance.
        Parameters
        ----------
        paprams : jnp.ndarray
            1D param vector.
        data : jnp.ndarray
            Data.
        mask : jnp.ndarray, optional
            Masking array. The default is None.
        weights : jnp.ndarray, optional
            Weights array. The default is None.
        prior_arg : float, optional
            Extra argument for prior. The default is 0.0.

        Returns
        -------
        Logprobs of data.

        """
        if param_mask is not None:
            params = params * param_mask
        lp = self.logprob(params, data)
        lp = jnp.where(~jnp.isfinite(lp), np.nan, lp)
        if weights is not None:
            lp *= weights 
        if self.use_masking:
            return -jnp.where(mask, 0.0, lp).sum() - self.prior(params, data, mask, weights, prior_arg)
        else:
            return -lp.sum() - self.prior(params, data, mask, weights)

    def vec_to_dict(self, v: np.ndarray) -> dict:
        return {n: v[i] for n, i in self.params_active.items()}

    def dict_to_vec(self, d: dict) -> np.ndarray:
        pa = self.params_active
        r = np.zeros(self.num_params)
        for n, v in d.items():
            try:
                r[pa[n]] = v
            except KeyError:
                continue
        return r

    @abstractmethod
    def mean(self, params=None):
        pass

    #@abstractmethod
    def sample(self, params=None):
        pass