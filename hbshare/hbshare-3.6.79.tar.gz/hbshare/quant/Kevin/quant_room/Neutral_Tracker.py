"""
市场中性策略模块
"""
import pandas as pd
import numpy as np
import hbshare as hbs
from datetime import datetime
from hbshare.quant.Kevin.quant_room.MyUtil.data_loader import get_trading_day_list, get_fund_nav_from_sql
from Arbitrage_backtest import cal_annual_return, cal_annual_volatility, cal_sharpe_ratio, cal_max_drawdown


class NeutralTracker:
    def __init__(self, start_date, end_date, config_df):
        self.start_date = start_date
        self.end_date = end_date
        self.config_df = config_df
        self._load_data()

    def _load_data(self):
        config_df = self.config_df.copy()
        config_df['运作日期'] = config_df['运作日期'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        config_df['指增起始'] = config_df['指增起始'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        neu_fund_dict = self.config_df.set_index('管理人')['基金代码'].to_dict()
        # 中性
        neu_start = config_df['运作日期'].min()
        neu_date_list = get_trading_day_list(neu_start, self.end_date, frequency="week")
        fund_nav = get_fund_nav_from_sql(neu_start, self.end_date, neu_fund_dict).reindex(neu_date_list).dropna(how='all')
        for fund_name in fund_nav.columns:
            act_start = config_df.set_index('管理人').loc[fund_name]['运作日期']
            fund_nav.loc[:act_start, fund_name] = np.NaN
        neu_nav = fund_nav.dropna(how='all').fillna(method='ffill')
        # 指增
        alpha_fund_dict = self.config_df.set_index('管理人')['对应指增'].to_dict()
        alpha_start = config_df['指增起始'].min()
        alpha_date_list = get_trading_day_list(alpha_start, self.end_date, frequency="week")
        fund_nav = get_fund_nav_from_sql(alpha_start, self.end_date, alpha_fund_dict).reindex(alpha_date_list).dropna(
            how='all')
        for fund_name in fund_nav.columns:
            act_start = config_df.set_index('管理人').loc[fund_name]['指增起始']
            fund_nav.loc[:act_start, fund_name] = np.NaN
        alpha_nav = fund_nav.dropna(how='all').fillna(method='ffill')

        self.neu_nav = neu_nav
        self.alpha_nav = alpha_nav

    def calculate_neu_ratio(self):
        nav_df = self.neu_nav.dropna()

        portfolio_index_df = pd.DataFrame(
            index=nav_df.columns, columns=['超额年化收益', '超额年化波动', '最大回撤', 'Sharpe', '胜率', '平均损益比',
                                           'period_1', 'period_2', 'period_3'])
        portfolio_index_df.loc[:, '超额年化收益'] = nav_df.pct_change().dropna(how='all').apply(cal_annual_return, axis=0)
        portfolio_index_df.loc[:, '超额年化波动'] = \
            nav_df.pct_change().dropna(how='all').apply(cal_annual_volatility, axis=0)
        portfolio_index_df.loc[:, '最大回撤'] = nav_df.apply(cal_max_drawdown, axis=0)
        portfolio_index_df.loc[:, 'Sharpe'] = \
            nav_df.pct_change().dropna(how='all').apply(lambda x: cal_sharpe_ratio(x, 0.015), axis=0)
        portfolio_index_df.loc[:, '胜率'] = \
            nav_df.pct_change().dropna(how='all').apply(lambda x: x.gt(0).sum() / len(x), axis=0)
        portfolio_index_df.loc[:, '平均损益比'] = \
            nav_df.pct_change().dropna(how='all').apply(lambda x: x[x > 0].mean() / x[x < 0].abs().mean(), axis=0)
        portfolio_index_df.loc[:, "period_1"] = nav_df.loc["20210917"] / nav_df.loc["20210416"] - 1
        portfolio_index_df.loc[:, "period_2"] = nav_df.loc["20220211"] / nav_df.loc["20210917"] - 1
        portfolio_index_df.loc[:, "period_3"] = nav_df.loc["20220916"] / nav_df.loc["20220211"] - 1

        portfolio_index_df.index.name = '产品名称'
        portfolio_index_df.reset_index(inplace=True)
        # 格式处理
        portfolio_index_df['超额年化收益'] = portfolio_index_df['超额年化收益'].apply(lambda x: format(x, '.2%'))
        portfolio_index_df['超额年化波动'] = portfolio_index_df['超额年化波动'].apply(lambda x: format(x, '.2%'))
        portfolio_index_df['最大回撤'] = portfolio_index_df['最大回撤'].apply(lambda x: format(x, '.2%'))
        portfolio_index_df['Sharpe'] = portfolio_index_df['Sharpe'].round(2)
        portfolio_index_df['胜率'] = portfolio_index_df['胜率'].apply(lambda x: format(x, '.1%'))
        portfolio_index_df['平均损益比'] = portfolio_index_df['平均损益比'].round(2)
        portfolio_index_df['period_1'] = portfolio_index_df['period_1'].apply(lambda x: format(x, '.2%'))
        portfolio_index_df['period_2'] = portfolio_index_df['period_2'].apply(lambda x: format(x, '.2%'))
        portfolio_index_df['period_3'] = portfolio_index_df['period_3'].apply(lambda x: format(x, '.2%'))

        return portfolio_index_df

    def hedge_compare(self, start_date="20210806"):
        nav_df = self.neu_nav.dropna().loc[start_date:]
        enhance_df = self.alpha_nav.loc[start_date:]

        sql_script = "SELECT JYRQ as TRADEDATE, ZQDM, SPJG as TCLOSE from funddb.ZSJY WHERE" \
                     " ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format("000905", start_date, enhance_df.index[-1])
        res = hbs.db_data_query('readonly', sql_script, page_size=5000)
        data = pd.DataFrame(res['data'])
        benchmark_series = data.set_index('TRADEDATE')['TCLOSE'].reindex(enhance_df.index)

        alpha_df = enhance_df.pct_change().dropna().sub(benchmark_series.pct_change().dropna(), axis=0).sort_index()
        neutral_df = nav_df.pct_change().dropna()

        assert (alpha_df.shape == neutral_df.shape)

        hedge_df = 1.2 * neutral_df - alpha_df

        # 收益拆解
        attr_list = []
        for col in alpha_df.columns:
            kt = np.log(1 + neutral_df[col]) / neutral_df[col]
            r = (1 + neutral_df[col]).prod() - 1
            k = np.log(1 + r) / r

            attr = alpha_df[col].to_frame('超额').merge(
                hedge_df[col].to_frame('对冲'), left_index=True, right_index=True) / 1.2

            cum_attr = attr.T.multiply(kt / k).sum(axis=1)

            attr_list.append(cum_attr.to_frame(col))

        attr_df = pd.concat(attr_list, axis=1).T

        # 风险拆解
        risk_list = []
        for col in alpha_df.columns:
            period_df = alpha_df[col].to_frame('超额').merge(
                hedge_df[col].to_frame('对冲'), left_index=True, right_index=True)
            cov_df = period_df.cov() * 10000.
            V = np.matrix(cov_df)
            w = np.matrix(np.array([1, 1]))
            sigma = np.sqrt((w * V * w.T)[0, 0])
            MRC = V * w.T
            # Risk Contribution
            RC = np.multiply(MRC, w.T) / sigma / 120

            attr = pd.DataFrame(index=['超额', '对冲'], columns=[col], data=RC.flatten().tolist()[0])
            risk_list.append(attr)

        risk_attr = pd.concat(risk_list, axis=1) * np.sqrt(52)
        risk_attr = risk_attr.T

        return attr_df, risk_attr


if __name__ == '__main__':
    config = pd.read_excel("D:\\研究基地\\G-专题报告\\市场中性专题\\专题报告数据.xlsx", sheet_name=0)

    NeutralTracker('20200101', '20220916', config).hedge_compare()