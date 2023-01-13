# -*- coding: utf-8 -*-

from scipy.optimize import minimize
import numpy as np
import pandas as pd


class RiskParity:
    def __init__(self, asset_list, cov, lb_list, ub_list, total_weight):
        self.asset_list = asset_list
        self.omega = np.matrix(cov)
        self.lb_list = lb_list
        self.ub_list = ub_list
        self.total_weight = total_weight

    def _target_func(self, x):
        tmp = np.sqrt((np.matrix(x) * self.omega * np.matrix(x).T).A1)
        risk = np.multiply(np.matrix(x).T, self.omega * np.matrix(x).T).A1 / tmp
        delta_risk = sum([sum((i - risk) ** 2) for i in risk])
        return delta_risk

    def _get_cons(self):
        cons = ({'type': 'eq', 'fun': lambda x: sum(x) - self.total_weight})
        return cons

    def _get_bnds(self):
        x0 = 1 / (np.diag(self.omega) ** 0.5)
        x0 = x0 / sum(x0)
        bnds = tuple((self.lb_list[i], self.ub_list[i]) for i in range(len(x0)))
        return bnds, x0

    def solve(self, ftol=1e-20):
        cons = self._get_cons()
        bnds, x0 = self._get_bnds()
        options = {'disp': False, 'maxiter': 500, 'ftol': ftol}

        res = minimize(self._target_func, x0, bounds=bnds, constraints=cons, method='SLSQP', options=options)
        if not res.success:
            weight = pd.Series(index=self.asset_list + ['cash'], data=[np.nan] * (len(self.asset_list) + 1))
            status = 'infeasible'
        else:
            arr_x = np.array(list(res.x))
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


class RiskBudget:
    def __init__(self, asset_list, cov, lb_list, ub_list, total_weight, risk_budget_list):
        self.asset_list = asset_list
        self.omega = np.matrix(cov)
        self.lb_list = lb_list
        self.ub_list = ub_list
        self.total_weight = total_weight
        self.risk_budget_list = risk_budget_list

    def _target_func(self, x):
        tmp = np.sqrt((np.matrix(x) * self.omega * np.matrix(x).T).A1)
        r_risk = np.multiply(np.matrix(x).T, self.omega * np.matrix(x).T).A1 / tmp
        b_risk = self.risk_budget_list * tmp
        delta_risk = sum((b_risk - r_risk) ** 2)
        return delta_risk

    def _get_cons(self):
        cons = ({'type': 'eq', 'fun': lambda x: sum(x) - self.total_weight})
        return cons

    def _get_bnds(self):
        x0 = 1 / (np.diag(self.omega) ** 0.5)
        x0 = x0 / sum(x0)
        bnds = tuple((self.lb_list[i], self.ub_list[i]) for i in range(len(x0)))
        return bnds, x0

    def solve(self, ftol=1e-20):
        cons = self._get_cons()
        bnds, x0 = self._get_bnds()
        options = {'disp': False, 'maxiter': 500, 'ftol': ftol}

        res = minimize(self._target_func, x0, bounds=bnds, constraints=cons, method='SLSQP', options=options)
        if not res.success:
            weight = pd.Series(index=self.asset_list + ['cash'], data=[np.nan] * (len(self.asset_list) + 1))
            status = 'infeasible'
        else:
            arr_x = np.array(list(res.x))
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
