# -*- coding: utf-8 -*-

from scipy import linalg
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class EF:
    def __init__(self, date, asset_list, ret, cov, risk_free_rate, weight):
        self.date = date
        self.asset_list = asset_list
        self.ret = np.matrix(ret)
        self.cov = np.matrix(cov)
        self.risk_free_rate = risk_free_rate
        self.weight = weight
        self.w_star = np.matrix(self.weight.loc[self.date, self.asset_list] / self.weight.loc[self.date, self.asset_list].sum()).T if len(self.weight.dropna()) > 0 else None

    def solve(self):
        n = len(self.asset_list)
        e = np.matrix(np.ones(n)).T
        mu = self.ret
        rf = self.risk_free_rate
        f = mu - rf
        V = self.cov
        V_inv = linalg.inv(V)

        # 最小方差组合
        w_C = V_inv * e / (e.T * V_inv * e)
        sigma2_C = (w_C.T * V * w_C)[0, 0]
        sigma_C = np.sqrt(sigma2_C)
        f_C = (w_C.T * f)[0, 0]
        # 夏普组合
        w_Q = V_inv * f / (e.T * V_inv * f)
        sigma2_Q = (w_Q.T * V * w_Q)[0, 0]
        sigma_Q = np.sqrt(sigma2_Q)
        f_Q = (w_Q.T * f)[0, 0]
        # 有效前沿曲线
        f_P = np.linspace(f_C, np.max(self.w_star.T * f) * 1.5, 21)  # 只取上半部分抛物线
        get_w_P = lambda fp: (f_Q - fp) / (f_Q - f_C) * w_C + (fp - f_C) / (f_Q - f_C) * w_Q
        w_P = [get_w_P(fp) for fp in f_P]
        k = (sigma2_Q - sigma2_C) / (f_Q - f_C) ** 2
        sigma2_P = sigma2_C + k * (f_P - f_C) ** 2
        sigma_P = np.sqrt(sigma2_P)
        r_P = np.array([(rf + wp.T * f)[0, 0] for wp in w_P])
        # 优化组合
        if self.w_star is not None:
            sigma2_star = (self.w_star.T * V * self.w_star)[0, 0]
            sigma_star = np.sqrt(sigma2_star)
            r_star = (rf + self.w_star.T * f)[0, 0]
        else:
            sigma_star = np.nan
            r_star = np.nan
        # 有效前沿曲线绘制
        # plt.figure(figsize=(6, 6))
        # plt.plot(sigma_P, r_P, 'o-', color='#F04950')
        # plt.plot(sigma_star, r_star, 'o', color='#6268A2')
        # plt.show()

        # 数据结果
        ef_weight = pd.concat([pd.DataFrame(wp) for wp in w_P], axis=1).T
        ef_weight.columns = self.asset_list
        ef_weight.index = range(len(w_P))
        ef_weight.loc[:, 'cash'] = 1.0 - ef_weight.sum(axis=1)
        ef_weight.loc['result', :] = self.weight.loc[self.date]
        sigma = pd.DataFrame(sigma_P)
        sigma.columns = ['sigma']
        sigma.loc['result', 'sigma'] = sigma_star
        r = pd.DataFrame(r_P)
        r.columns = ['r']
        r.loc['result', 'r'] = r_star
        ef_weight = pd.concat([ef_weight, sigma, r], axis=1)
        return ef_weight