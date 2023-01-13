"""
Class for Linear Gaussian SEMs parametrized
by a matrix B representing regression coefficients
and a matrix Omega representing correlated errors
"""

import functools

import autograd.numpy as anp
import numpy as np
import pandas as pd
import statsmodels.api as sm
from autograd import grad, hessian
from scipy.optimize import minimize


def is_positive_definite(X):
    try:
        np.linalg.cholesky(X)
        return True
    except LinAlgError:
        return False


class LinearGaussianSEM:
    def __init__(self, graph):
        """
        Fits a linear Gaussian structural equation model to an :class:`ADMG` using the recursive iterative conditional fitting algorithm as proposed by Drton and Richardson.

        :param graph: graph (:class:`ADMG`) corresponding to the linear Gaussian SEM.
        """

        self.graph = graph
        # for a linear Gaussian SEM each edge is a parameter + noise for each vertex
        self.n_params = (
            len(graph.di_edges) + len(graph.bi_edges) + len(graph.vertices)
        )
        self._vertex_index_map = {v: i for i, v in enumerate(graph.vertices)}
        self._parent_index_map = {
            v: [self._vertex_index_map[p] for p in graph.parents([v])]
            for v in graph.vertices
        }
        self._sibling_index_map = {
            v: [self._vertex_index_map[s] for s in graph.siblings([v])]
            for v in graph.vertices
        }

        self.X_ = None  # data matrix
        self.S_ = None  # sample covariance matrix
        self.B_ = None  # direct edge coefficients
        self.omega_ = None  # correlation of errors

    def neg_loglikelihood(self, X):
        """
        Calculate log-likelihood of the data given the model.

        :param X: a N x M dimensional data matrix.
        :param weights: optional 1d numpy array with weights for each data point
                        (rows with higher weights are given greater importance).
        :return: a float corresponding to the log-likelihood.
        """
        assert self.B_ is not None

        S = np.cov(X.T)
        assert is_positive_definite(
            S
        ), "Sample covariance matrix is not positive definite"
        n, d = X.shape
        sigma = (
            np.linalg.inv(np.eye(d) - self.B_)
            @ (self.omega_)
            @ np.linalg.inv((np.eye(d) - self.B_).T)
        )
        # assert is_positive_definite(sigma)
        neg_lld = (n / 2) * (
            np.log(np.linalg.det(sigma))
            + np.trace(np.dot(np.linalg.inv(sigma), S))
        )

        return neg_lld

    def bic(self, X):
        """
        Calculate Bayesian information criterion of the data given the model.

        :param X: a N x M dimensional data matrix.
        :param weights: optional 1d numpy array with weights for each data point
                        (rows with higher weights are given greater importance).
        :return: a float corresponding to the log-likelihood.
        """

        return 2 * self.neg_loglikelihood(X) + np.log(len(X)) * self.n_params

    def fit(self, X, tol=1e-6, disp=None, standardize=False, max_iters=100):
        """
        Fit the model to data via (weighted) maximum likelihood estimation

        :param X: data -- a N x M dimensional pandas data frame.
        :param weights: optional 1d numpy array with weights for each data point
                        (rows with higher weights are given greater importance).
        :return: self.
        """

        # make copy of the data and standardize if necessary
        self.X_ = X.values.copy()
        n, d = self.X_.shape
        if standardize:
            self.X_ = (self.X_ - np.mean(self.X_, axis=0)) / np.std(
                self.X_, axis=0
            )

        # compute sample covariance
        self.S_ = np.cov(self.X_.T)

        # initialize B and omega
        self.B_, self.omega_ = np.zeros((d, d)), np.eye(d)

        # keep going until desired convergence
        cur_lld = self.neg_loglikelihood(self.X_)
        lld_diff = tol + 1
        n_iters = 0
        while np.abs(lld_diff) > tol or n_iters == max_iters:
            n_iters += 1

            for var in self.graph.vertices:

                # get index of the vertex
                var_index = self._vertex_index_map[var]

                # get epsilon_minusi
                epsilon = self.X_ - self.X_ @ self.B_.T
                epsilon_minusi = np.delete(epsilon, var_index, axis=1)

                # get omega and calculate pseudo variables Zi
                omega_minusi = np.delete(self.omega_, var_index, axis=0)
                omega_minusii = np.delete(omega_minusi, var_index, axis=1)
                omega_minusii_inv = np.linalg.inv(omega_minusii)

                # calculate Z_minusi
                Z_minusi = (omega_minusii_inv @ epsilon_minusi.T).T

                # insert a column of zeros to maintain the shape
                Z = np.insert(Z_minusi, var_index, 0, axis=1)

                Y = self.X_[:, var_index]
                parent_mat = self.X_[:, self._parent_index_map[var]]
                pseudo_mat = Z[:, self._sibling_index_map[var]]
                Xmat = np.hstack((np.ones((n, 1)), parent_mat, pseudo_mat))
                results = sm.OLS(Y, Xmat).fit()

                # need to now extract results and put it in the right spots
                i = 1
                for idx in self._parent_index_map[var]:
                    self.B_[var_index, idx] = results.params[i]
                    i += 1
                for idx in self._sibling_index_map[var]:
                    self.omega_[var_index, idx] = results.params[i]
                    self.omega_[idx, var_index] = results.params[i]
                    i += 1

                parent_mat = np.hstack((np.ones((n, 1)), parent_mat))
                _, cols = parent_mat.shape

                omega_i_minusi = np.delete(self.omega_, var_index, axis=1)[
                    var_index, :
                ]
                omega_minusi_i = np.delete(self.omega_, var_index, axis=0)[
                    :, var_index
                ]
                omega_ii = results.scale + (
                    omega_i_minusi @ omega_minusii_inv @ omega_minusi_i
                )
                self.omega_[var_index, var_index] = omega_ii
            new_lld = self.neg_loglikelihood(self.X_)
            lld_diff = new_lld - cur_lld

            cur_lld = new_lld

        return self

    def total_effect(self, A, Y):
        """
        Calculate the total causal effect of a set of treatments A on
        a set of outcomes Y.

        :param A: iterable corresponding to variable names that act as treatments.
        :param Y: iterable corresponding to variable names that act as outcomes.
        :return: a float corresponding to the total causal effect.
        """

        directed_paths = self.graph.directed_paths(A, Y)

        # if there are no directed paths, the effect is 0
        if len(directed_paths) == 0:
            return 0

        # otherwise do path analysis
        total_effect = 0
        for path in directed_paths:

            path_effect = 1
            for u, v in path:

                path_effect *= self.B_[
                    self._vertex_index_map[v], self._vertex_index_map[u]
                ]

            total_effect += path_effect

        return total_effect

    def draw(self, direction=None):
        """
        Visualize the graph.

        :return : dot language representation of the graph.
        """

        from graphviz import Digraph

        if self.B_ is None:
            raise AssertionError("Model must be fit before model can be drawn.")
        dot = Digraph()

        # set direction from left to right if that's preferred
        if direction == "LR":
            dot.graph_attr["rankdir"] = direction

        for v in self.graph.vertices.values():
            dot.node(v.name, shape="plaintext", height=".5", width=".5")

        for parent, child in self.graph.di_edges:
            i, j = self._vertex_index_map[child], self._vertex_index_map[parent]
            dot.edge(
                parent,
                child,
                color="blue",
                label=str(round(self.B_[i, j], 2)),
                fontsize="12",
            )
        for sib1, sib2 in self.graph.bi_edges:
            i, j = self._vertex_index_map[sib1], self._vertex_index_map[sib2]
            dot.edge(
                sib1,
                sib2,
                dir="both",
                color="red",
                label=str(round(self.omega_[i, j], 2)),
                fontsize="12",
            )

        return dot
