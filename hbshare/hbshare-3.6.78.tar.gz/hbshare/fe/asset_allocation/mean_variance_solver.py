# -*- coding: utf-8 -*-

from scipy.optimize import minimize
import cvxpy as cp
import numpy as np
import pandas as pd


class MaxReturn:
    def __init__(self, asset_list, ret, cov, target_risk, lb_list, ub_list, total_weight):
        self.asset_list = asset_list
        self.ret = np.matrix(ret)
        self.cov = np.matrix(cov)
        self.target_risk = target_risk
        self.lb_list = lb_list
        self.ub_list = ub_list
        self.total_weight = total_weight

    def solve(self):
        n = len(self.asset_list)
        w = cp.Variable(n)
        ret = self.ret.T @ w
        risk = cp.quad_form(w, self.cov)
        prob = cp.Problem(cp.Maximize(ret),
                          [risk <= self.target_risk ** 2.0,
                           cp.sum(w) == self.total_weight,
                           w >= self.lb_list,
                           w <= self.ub_list])
        prob.solve()
        if prob.status != 'optimal':
            weight = pd.Series(index=self.asset_list + ['cash'], data=[np.nan] * (len(self.asset_list) + 1))
            status = 'infeasible'
        else:
            arr_x = w.value
            for i in range(len(self.asset_list)):
                if arr_x[i] < self.lb_list[i]:
                    arr_x[i] = self.lb_list[i]
            for i in range(len(self.asset_list)):
                if arr_x[i] > self.ub_list[i]:
                    arr_x[i] = self.ub_list[i]
            if sum(arr_x) != self.total_weight:
                arr_x = arr_x / arr_x.sum() * self.total_weight

            weight = pd.Series(index=self.asset_list + ['cash'], data=list(arr_x) + [1.0 - arr_x.sum()])
            status = 'optimal'
        return weight, status


class MinRisk:
    def __init__(self, asset_list, ret, cov, target_return, lb_list, ub_list, total_weight):
        self.asset_list = asset_list
        self.ret = np.matrix(ret)
        self.cov = np.matrix(cov)
        self.target_return = target_return
        self.lb_list = lb_list
        self.ub_list = ub_list
        self.total_weight = total_weight

    def solve(self):
        n = len(self.asset_list)
        w = cp.Variable(n)
        ret = self.ret.T @ w
        risk = cp.quad_form(w, self.cov)
        prob = cp.Problem(cp.Minimize(risk),
                          [ret >= self.target_return,
                           cp.sum(w) == self.total_weight,
                           w >= self.lb_list,
                           w <= self.ub_list])
        prob.solve()
        if prob.status != 'optimal':
            weight = pd.Series(index=self.asset_list + ['cash'], data=[np.nan] * (len(self.asset_list) + 1))
            status = 'infeasible'
        else:
            arr_x = w.value
            for i in range(len(self.asset_list)):
                if arr_x[i] < self.lb_list[i]:
                    arr_x[i] = self.lb_list[i]
            for i in range(len(self.asset_list)):
                if arr_x[i] > self.ub_list[i]:
                    arr_x[i] = self.ub_list[i]
            if sum(arr_x) != self.total_weight:
                arr_x = arr_x / arr_x.sum() * self.total_weight

            weight = pd.Series(index=self.asset_list + ['cash'], data=list(arr_x) + [1.0 - arr_x.sum()])
            status = 'optimal'
        return weight, status


class MaxUtility:
    def __init__(self, asset_list, ret, cov, risk_aversion, lb_list, ub_list, total_weight):
        self.asset_list = asset_list
        self.ret = np.matrix(ret)
        self.cov = np.matrix(cov)
        self.risk_aversion = risk_aversion
        self.lb_list = lb_list
        self.ub_list = ub_list
        self.total_weight = total_weight

    def solve(self):
        n = len(self.asset_list)
        w = cp.Variable(n)
        ret = self.ret.T @ w
        risk = cp.quad_form(w, self.cov)
        prob = cp.Problem(cp.Maximize(ret - 0.5 * self.risk_aversion * risk),
                          [cp.sum(w) == self.total_weight,
                           w >= self.lb_list,
                           w <= self.ub_list])
        prob.is_dcp()
        prob.solve()
        if prob.status != 'optimal':
            weight = pd.Series(index=self.asset_list + ['cash'], data=[np.nan] * (len(self.asset_list) + 1))
            status = 'infeasible'
        else:
            arr_x = w.value
            for i in range(len(self.asset_list)):
                if arr_x[i] < self.lb_list[i]:
                    arr_x[i] = self.lb_list[i]
            for i in range(len(self.asset_list)):
                if arr_x[i] > self.ub_list[i]:
                    arr_x[i] = self.ub_list[i]
            if sum(arr_x) != self.total_weight:
                arr_x = arr_x / arr_x.sum() * self.total_weight

            weight = pd.Series(index=self.asset_list + ['cash'], data=list(arr_x) + [1.0 - arr_x.sum()])
            status = 'optimal'
        return weight, status


class MSR:
    def __init__(self, asset_list, ret, cov, lb_list, ub_list, total_weight):
        self.asset_list = asset_list
        self.ret = np.matrix(ret)
        self.cov = np.matrix(cov)
        self.lb_list = lb_list
        self.ub_list = ub_list
        self.total_weight = total_weight

    def solve(self):
        n = len(self.asset_list)
        w = cp.Variable(n)
        ret = self.ret.T @ w
        risk = cp.quad_form(w, self.cov)
        prob = cp.Problem(cp.Minimize(risk),
                          [ret == 1,
                           w >= self.lb_list])
        prob.solve()
        if prob.status != 'optimal':
            weight = pd.Series(index=self.asset_list + ['cash'], data=[np.nan] * (len(self.asset_list) + 1))
            status = 'infeasible'
        else:
            arr_x = w.value
            arr_x = arr_x / arr_x.sum() * self.total_weight
            for i in range(len(self.asset_list)):
                if arr_x[i] < self.lb_list[i]:
                    arr_x[i] = self.lb_list[i]
            for i in range(len(self.asset_list)):
                if arr_x[i] > self.ub_list[i]:
                    arr_x[i] = self.ub_list[i]
            if sum(arr_x) != self.total_weight:
                arr_x = arr_x / arr_x.sum() * self.total_weight

            weight = pd.Series(index=self.asset_list + ['cash'], data=list(arr_x) + [1.0 - arr_x.sum()])
            status = 'optimal'
        return weight, status


# class MSR:
#     def __init__(self, asset_list, ret, cov, lb_list, ub_list, total_weight):
#         self.asset_list = asset_list
#         self.ret = np.matrix(ret)
#         self.cov = np.matrix(cov)
#         self.lb_list = lb_list
#         self.ub_list = ub_list
#         self.total_weight = total_weight
#
#     def _target_func(self, x):
#         x = np.matrix(x).T
#         ret = float(x.T * self.ret)
#         std = float(np.sqrt(x.T * self.cov * x))
#         sharpe = - ret / std
#         return sharpe
#
#     def _get_cons(self):
#         cons = ({'type': 'eq', 'fun': lambda x: sum(x) - self.total_weight})
#         return cons
#
#     def _get_bnds(self):
#         x0 = 1 / (np.diag(self.cov) ** 0.5)
#         x0 = x0 / sum(x0)
#         bnds = tuple((self.lb_list[i], self.ub_list[i]) for i in range(len(x0)))
#         return bnds, x0
#
#     def solve(self, ftol=1e-20):
#         cons = self._get_cons()
#         bnds, x0 = self._get_bnds()
#         options = {'disp': False, 'maxiter': 500, 'ftol': ftol}
#
#         res = minimize(self._target_func, x0, bounds=bnds, constraints=cons, method='SLSQP', options=options)
#         if not res.success:
#             weight = pd.Series(index=self.asset_list + ['cash'], data=[np.nan] * (len(self.asset_list) + 1))
#             status = 'infeasible'
#         else:
#             arr_x = np.array(list(res.x))
#             for i in range(len(self.asset_list)):
#                 if arr_x[i] < self.lb_list[i]:
#                     arr_x[i] = self.lb_list[i]
#             for i in range(len(self.asset_list)):
#                 if arr_x[i] > self.ub_list[i]:
#                     arr_x[i] = self.ub_list[i]
#             if sum(arr_x) != self.total_weight:
#                 arr_x = arr_x / arr_x.sum() * self.total_weight
#
#             weight = pd.Series(index=self.asset_list + ['cash'], data=list(arr_x) + [1.0 - arr_x.sum()])
#             status = 'optimal'
#         return weight, status