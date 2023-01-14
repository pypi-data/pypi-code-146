# -*- coding: utf-8 -*-
"""ModelMixtures that are ran a whole dataset."""
from .model_mixture import ModelMixture
from collections import defaultdict
from copy import copy
import pandas as pd
import numpy as np
import logging


class ModelMixtures(ModelMixture):
    def __init__(self, bad: float, left: int,
                 dist='BetaNB', estimate_p=False,
                 regul_alpha=0.0, regul_n=True,
                 regul_slice=True, regul_prior='laplace',
                 fix_params=None):
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

        Returns
        -------
        None.

        """
        super().__init__(bad=bad, left=left, dist=dist,
                         estimate_p=estimate_p, fix_params=fix_params,
                         regul_alpha=regul_alpha, regul_n=regul_n, 
                         regul_slice=regul_slice, regul_prior=regul_prior,
                         use_masking=True)


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
        logging.debug('Preparing ModelMixtures to work with provided'
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
        self.weights = weights
        self.inds_orig = np.array(inds_orig)
        self.slices = cs
        self.slices_inds = c_inds
        return np.vstack([df, self.weights]).T


    def fit(self, data, **kwargs):
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
        r = dict()
        slices = self.slices
        slices_inds = self.slices_inds
        x0s = copy(self.x0)
        for i, s in enumerate(slices):
            self.x0 = copy(x0s)
            sts = set()
            for x0 in x0s:
                x0 = list(x0)
                x0[0] = float(s)
                sts.add(tuple(x0))
            for x0 in sts:
                self.x0.insert(0, np.array(x0, dtype=float))
            self.x0 = list(map(np.array, sts))
            res = super().fit(data[slices_inds == i], use_prev='only', 
                              calc_std=False)
            if res and type(res) not in (float, int, bool):
                for n, v in res.items():
                    if n.startswith(('succ', 'loglik')):
                        continue
                    r[f'{n}{s}'] = v
        self.params = r
        self.data = data
        return r

    def mean(self, params=None):
        raise NotImplementedError

    def get_sliced_params(self, params=None):
        if params is None:
            params = self.params
        results = defaultdict(list)
        stds = params.get('std', dict())
        stds_res = defaultdict(list)
        for c in self.slices:
            for p in ('w', 'k', 'r', 'p1', 'p2'):
                pc = p + str(c)
                if pc in params:
                    results[p].append(params[pc])
            results['slice'].append(c)
        for p, v in stds.items():
            stds_res[p[0]].append(v)
        if stds_res:
            results['std'] = stds_res
        return results