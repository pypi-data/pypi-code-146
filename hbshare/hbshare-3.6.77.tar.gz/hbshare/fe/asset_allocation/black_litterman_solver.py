# -*- coding: utf-8 -*-

import cvxpy as cp
import numpy as np
import pandas as pd


class BL:
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