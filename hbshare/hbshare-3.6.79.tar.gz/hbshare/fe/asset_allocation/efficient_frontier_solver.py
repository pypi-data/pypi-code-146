# -*- coding: utf-8 -*-

from hbshare.fe.asset_allocation.mean_variance_solver import MaxReturn, MinRisk
import numpy as np
import pandas as pd


class EF:
    def __init__(self, asset_list, ret, cov, risk_free_rate, lb_list, ub_list, total_weight, weight):
        self.asset_list = asset_list
        self.ret = np.matrix(ret)
        self.cov = np.matrix(cov)
        self.target_risk = 99
        self.target_return = -99
        self.risk_free_rate = risk_free_rate
        self.lb_list = lb_list
        self.ub_list = ub_list
        self.total_weight = total_weight
        self.weight = weight
        self.w_star = self.weight[self.asset_list].T if len(self.weight[self.asset_list].dropna()) > 0 else None

    def solve(self):
        # 最小方差组合（最左侧点）
        min_weight, min_status = MinRisk(self.asset_list, self.ret, self.cov, self.target_return, self.lb_list, self.ub_list, self.total_weight).solve()
        if min_status == 'optimal':
            min_weight = pd.DataFrame(min_weight).loc[self.asset_list]
            min_sigma2 = (np.matrix(min_weight).T * self.cov * np.matrix(min_weight))[0, 0]
            min_sigma = np.sqrt(min_sigma2)
            min_r = (np.matrix(min_weight).T * self.ret)[0, 0]
        else:
            min_weight = pd.DataFrame(index=self.asset_list, columns=[0], data=[np.nan] * len(self.asset_list))
            min_sigma = np.nan
            min_r = self.ret.mean()
        # 最大收益组合（最上侧点）
        max_weight, max_status = MaxReturn(self.asset_list, self.ret, self.cov, self.target_risk, self.lb_list, self.ub_list, self.total_weight).solve()
        if max_status == 'optimal':
            max_weight = pd.DataFrame(max_weight).loc[self.asset_list]
            max_sigma2 = (np.matrix(max_weight).T * self.cov * np.matrix(max_weight))[0, 0]
            max_sigma = np.sqrt(max_sigma2)
            max_r = (np.matrix(max_weight).T * self.ret)[0, 0]
        else:
            max_weight = pd.DataFrame(index=self.asset_list, columns=[0], data=[np.nan] * len(self.asset_list))
            max_sigma = np.nan
            max_r = self.ret.max()
        # 有效前沿曲线
        delta = ((max_r - min_r) / 20.0) - 1e-8
        ret_list = [(min_r + delta * i) for i in range(1, 20)]
        weight_P, sigma_P, r_P = [], [], []
        for ret in ret_list:
            weight, status = MinRisk(self.asset_list, self.ret, self.cov, ret, self.lb_list, self.ub_list, self.total_weight).solve()
            if status == 'optimal':
                weight = pd.DataFrame(weight).loc[self.asset_list]
            else:
                weight = pd.DataFrame(index=self.asset_list, columns=[0], data=[np.nan] * len(self.asset_list))
            sigma2 = (np.matrix(weight).T * self.cov * np.matrix(weight))[0, 0]
            sigma = np.sqrt(sigma2)
            r = (np.matrix(weight).T * self.ret)[0, 0]
            weight_P.append(weight)
            sigma_P.append(sigma)
            r_P.append(r)
        weight_P = [min_weight] + weight_P + [max_weight]
        sigma_P = [min_sigma] + sigma_P + [max_sigma]
        r_P = [min_r] + r_P + [max_r]
        # try:
        #     min_weight, min_status = MinRisk(self.asset_list, self.ret, self.cov, min_r, self.lb_list, self.ub_list, self.total_weight).solve()
        #     min_weight = pd.DataFrame(min_weight).loc[self.asset_list]
        #     min_sigma2 = (np.matrix(min_weight).T * self.cov * np.matrix(min_weight))[0, 0]
        #     min_sigma = np.sqrt(min_sigma2)
        #     min_r = (np.matrix(min_weight).T * self.ret)[0, 0]
        # except:
        #     pass
        # weight_P = [min_weight] + weight_P
        # sigma_P = [min_sigma] + sigma_P
        # r_P = [min_r] + r_P
        # try:
        #     max_weight, max_status = MinRisk(self.asset_list, self.ret, self.cov, max_r, self.lb_list, self.ub_list, self.total_weight).solve()
        #     max_weight = pd.DataFrame(max_weight).loc[self.asset_list]
        #     max_sigma2 = (np.matrix(max_weight).T * self.cov * np.matrix(max_weight))[0, 0]
        #     max_sigma = np.sqrt(max_sigma2)
        #     max_r = (np.matrix(max_weight).T * self.ret)[0, 0]
        # except:
        #     pass
        # weight_P = weight_P + [max_weight]
        # sigma_P = sigma_P + [max_sigma]
        # r_P = r_P + [max_r]
        # 优化组合
        if self.w_star is not None:
            sigma2_star = (np.matrix(self.w_star).T * self.cov * np.matrix(self.w_star))[0, 0]
            sigma_star = np.sqrt(sigma2_star)
            r_star = (np.matrix(self.w_star).T * self.ret)[0, 0]
        else:
            sigma_star = np.nan
            r_star = np.nan
        # # 有效前沿曲线绘制
        # from matplotlib.ticker import FuncFormatter
        # import matplotlib.pyplot as plt
        # plt.rcParams['font.sans-serif'] = ['SimHei']
        # plt.rcParams['axes.unicode_minus'] = False
        # def to_100percent_r2(temp, position):
        #     return '%.2f' % (temp * 100) + '%'
        # plt.figure(figsize=(6, 6))
        # plt.plot(sigma_P, r_P, 'o-', color='#F04950', label='有效前沿')
        # plt.plot(sigma_star, r_star, 'o', color='#6268A2', label='最优方案')
        # plt.gca().xaxis.set_major_formatter(FuncFormatter(to_100percent_r2))
        # plt.gca().yaxis.set_major_formatter(FuncFormatter(to_100percent_r2))
        # plt.xlabel('年化风险')
        # plt.ylabel('年化收益')
        # plt.title('{0}'.format(self.weight.index[0]))
        # plt.legend(loc=2)
        # plt.tight_layout()
        # plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/aam/{0}.png'.format(self.weight.index[0]))

        # 数据结果
        ef_weight = pd.concat(weight_P, axis=1).T
        ef_weight.index = range(len(ef_weight))
        ef_weight.loc[:, 'cash'] = 1.0 - ef_weight.sum(axis=1)
        ef_weight.loc['result', :] = self.weight.iloc[0]
        sigma = pd.DataFrame(sigma_P)
        sigma.columns = ['sigma']
        sigma.loc['result', 'sigma'] = sigma_star
        r = pd.DataFrame(r_P)
        r.columns = ['r']
        r.loc['result', 'r'] = r_star
        ef_weight = pd.concat([ef_weight, sigma, r], axis=1)
        ef_weight = pd.concat([ef_weight.iloc[:-1].dropna(), ef_weight.iloc[-1:]])
        ef_weight = ef_weight.reset_index().rename(columns={'index': 'group'})
        return ef_weight