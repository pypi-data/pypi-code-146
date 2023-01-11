"""
日度净值归因模块
"""
import pandas as pd
import numpy as np
import hbshare as hbs
from datetime import datetime
from hbshare.quant.Kevin.quant_room.MyUtil.data_loader import get_trading_day_list, get_fund_nav_from_sql
from hbshare.quant.Kevin.rm_associated.config import style_names, industry_names
import statsmodels.api as sm
from hbshare.quant.Kevin.quant_room.MyUtil.data_loader import get_daily_nav_from_work
from hbshare.quant.Kevin.quant_room.MyUtil.data_config import daily_fund_nav_dict
from statsmodels.stats.outliers_influence import variance_inflation_factor


class AlphaNavAttribution:
    def __init__(self, start_date, end_date, token):
        self.start_date = start_date
        self.end_date = end_date
        self.token = token
        self._load_data()

    @staticmethod
    def nav_transform(nav_df):
        nav_df['div'] = nav_df['dividend'].diff()
        nav_df['div'] = nav_df['div'].fillna(nav_df['dividend'].iloc[0])
        nav_df['adj_factor'] = nav_df['jjjz'].shift(1) / (nav_df['jjjz'].shift(1) - nav_df['div'])
        nav_df['adj_factor'] = nav_df['adj_factor'].fillna(1.).cumprod()
        nav_df['adj_nav'] = nav_df['adj_factor'] * nav_df['jjjz']

        return nav_df['adj_nav']

    @staticmethod
    def nav_check(adj_nav, fund_id):
        start_date, end_date = adj_nav.index[0], adj_nav.index[-1]
        nv_series = get_fund_nav_from_sql(start_date, end_date, {"actual": fund_id})
        trading_day_list = get_trading_day_list(start_date, end_date, "week")
        compare_df = adj_nav.to_frame('calculate').merge(
            nv_series, left_index=True, right_index=True).reindex(trading_day_list)

        return compare_df

    def nav_process(self, all_data, fund_name, fof_name):
        selected_data = all_data[all_data['jjmc'] == fund_name].dropna(subset=['jjjz', 'ljjz'])
        selected_data = selected_data[selected_data['khmc'] == fof_name].sort_values(by='jzrq')  # longest period
        fund_id = selected_data['jjdm'].unique()[0]
        selected_data = selected_data.set_index('jzrq')[['jjjz', 'ljjz']]
        start_date, end_date = selected_data.index[0], selected_data.index[-1]
        date_list = get_trading_day_list(start_date, end_date)
        origin_nav = selected_data.reindex(date_list).astype(float)
        origin_nav['dividend'] = (origin_nav['ljjz'] - origin_nav['jjjz']).round(4)
        adj_nav = self.nav_transform(origin_nav).sort_index()
        # test
        test_df = self.nav_check(adj_nav, fund_id)
        test_df = test_df.pct_change().dropna()
        test_df['delta'] = (test_df['calculate'] - test_df['actual']).abs()
        print("【{}】在区间内日度收益的总误差为: {}".format(fund_name, test_df['delta'].sum()))

        return adj_nav

    def _load_data(self):
        # 所有数据
        all_data = hbs.commonQuery('FOF_ZJJLIST', startDate=self.start_date, endDate=self.end_date,
                                   sorts=[{"field": "jzrq", "sort": "desc"}],
                                   access_token=self.token,
                                   fields=['jjdm', 'jjmc', 'khdm', 'khmc', 'jjjz', 'jzrq', 'ljjz'])
        # 乾象、伯兄、启林、因诺、明汯(1000)、星阔(500 + 全市场)、概率(500 + 1000)、诚奇
        nav_dict = {
            "500指增": {},
            "1000指增": {},
            "全市场": {}
        }
        # special treat
        all_data.replace({'乾象中证500指数增强1号私募证券投资基金B类': '乾象中证500指数增强1号私募证券投资基金B',
                          '明汯量化中小盘增强1号私募证券投资基金A': '明汯量化中小盘增强1号私募证券投资基金'}, inplace=True)

        # 乾象(特殊处理)
        tmp = all_data[(all_data['jjmc'].str.contains('乾象')) & (all_data['jjmc'].str.contains('500指数增强'))]
        tmp = tmp.dropna(subset=['jjjz', 'ljjz'])
        tmp = tmp[tmp['khmc'] == '新方程大类配置基金'].sort_values(by='jzrq')  # 最长的净值
        tmp = tmp.set_index('jzrq')[['jjjz', 'ljjz']]
        trading_day_list = get_trading_day_list(tmp.index[0], tmp.index[-1])
        tmp = tmp.reindex(trading_day_list)
        tmp.loc['20220429'] = ['0.8434', '1.1350']  # 手动填充
        tmp = tmp.astype(float)
        tmp['dividend'] = (tmp['ljjz'] - tmp['jjjz']).round(4)
        adj_nav = self.nav_transform(tmp).sort_index()
        test_df = self.nav_check(adj_nav, 'P48470').pct_change().dropna()
        test_df['delta'] = (test_df['calculate'] - test_df['actual']).abs()
        print("区间内日度收益的总误差为: {}".format(test_df['delta'].sum()))
        nav_dict['500指增']['乾象'] = adj_nav
        # 伯兄
        adj_nav = self.nav_process(all_data, '伯兄熙宁中证500指数增强私募证券投资基金', '新方程量化中小盘精选二号私募证券投资基金')
        nav_dict['500指增']['伯兄'] = adj_nav
        # 启林(500 + 1000)
        adj_nav = self.nav_process(all_data, '启林中证500指数增强1号私募证券投资基金', '新方程量化中小盘精选私募证券投资基金')
        nav_dict['500指增']['启林'] = adj_nav
        adj_nav = self.nav_process(all_data, '启林玉成一号私募证券投资基金B', '新方程量化中小盘精选二号私募证券投资基金')
        nav_dict['1000指增']['启林'] = adj_nav.loc["20211231":]
        # 因诺
        adj_nav = self.nav_process(all_data, '因诺聚配中证500指数增强私募证券投资基金', '新方程量化中小盘精选私募证券投资基金')
        adj_nav.loc['20211126'] = 2.2350
        nav_dict['500指增']['因诺'] = adj_nav
        # 明汯(500 + 1000)
        adj_nav = self.nav_process(all_data, '明汯价值成长1期3号私募投资基金', '新方程大类配置基金')
        nav_dict['500指增']['明汯'] = adj_nav
        adj_nav = self.nav_process(all_data, '明汯量化中小盘增强1号私募证券投资基金', '新方程量化中小盘精选私募证券投资基金')
        adj_nav.loc['20211126'] = 2.5951
        nav_dict['1000指增']['明汯'] = adj_nav
        # 星阔
        adj_nav = self.nav_process(all_data, '星阔广厦1号中证500指数增强私募证券投资基金', '新方程量化中小盘精选私募证券投资基金')
        nav_dict['500指增']['星阔'] = adj_nav
        adj_nav = self.nav_process(all_data, '星阔山海6号股票优选私募证券投资基金', '新方程对冲精选H1号基金')
        nav_dict['全市场']['星阔'] = adj_nav
        # 概率(500 + 1000)
        adj_nav = self.nav_process(all_data, '概率500指增2号私募证券投资基金', '新方程量化中小盘精选二号私募证券投资基金')
        nav_dict['500指增']['概率'] = adj_nav
        adj_nav = self.nav_process(all_data, '概率1000指增1号私募证券投资基金', '新方程量化中小盘精选二号私募证券投资基金')
        nav_dict['1000指增']['概率'] = adj_nav
        # 诚奇
        adj_nav = self.nav_process(all_data, '诚奇睿盈500指数增强私募证券投资基金A', '新方程好买臻选3号私募证券投资母基金')
        nav_dict['500指增']['诚奇'] = adj_nav
        # 幻方
        adj_nav = self.nav_process(all_data, '幻方500指数增强欣享6号私募证券投资基金', '新方程量化中小盘精选私募证券投资基金')
        nav_dict['500指增']['幻方'] = adj_nav
        # 天演(500 + 全市场)
        adj_nav = self.nav_process(all_data, '天演中证500指数增强证券投资基金', '新方程量化中小盘精选私募证券投资基金')
        nav_dict['500指增']['天演'] = adj_nav.loc['20210625':]
        adj_nav = self.nav_process(all_data, '天演赛能证券投资基金', '新方程大类配置基金')
        nav_dict['全市场']['天演'] = adj_nav
        # 衍复(500 + 1000, 500特殊处理)
        tmp = all_data[(all_data['jjmc'].str.contains('衍复')) & (all_data['jjmc'].str.contains('指增三号'))]
        tmp = tmp.dropna(subset=['jjjz', 'ljjz'])
        tmp = tmp[tmp['khmc'] == '新方程量化中小盘精选私募证券投资基金'].sort_values(by='jzrq')  # 最长的净值
        tmp = tmp.set_index('jzrq')[['jjjz', 'ljjz']]
        trading_day_list = get_trading_day_list(tmp.index[0], tmp.index[-1])
        tmp = tmp.reindex(trading_day_list)
        tmp.loc['20211126'] = ['1.4791', '1.8191']
        tmp.loc['20220113'] = ['1.3665', '1.8065']  # 手动填充
        tmp = tmp.astype(float).reindex(trading_day_list)
        tmp['dividend'] = (tmp['ljjz'] - tmp['jjjz']).round(4)
        adj_nav = self.nav_transform(tmp).sort_index()
        test_df = self.nav_check(adj_nav, 'SJH866').pct_change().dropna()
        test_df['delta'] = (test_df['calculate'] - test_df['actual']).abs()
        print("衍复500区间内日度收益的总误差为: {}".format(test_df['delta'].sum()))
        nav_dict['500指增']['衍复'] = adj_nav

        adj_nav = self.nav_process(all_data, '衍复1000指增一号私募证券投资基金', '新方程量化中小盘精选私募证券投资基金')
        nav_dict['1000指增']['衍复'] = adj_nav
        # 世纪前沿
        adj_nav = self.nav_process(all_data, '世纪前沿指数增强24号私募证券投资基金', '新方程大类配置二号私募证券投资基金')
        nav_dict['500指增']['世纪前沿'] = adj_nav
        # 赫富
        adj_nav = self.nav_process(all_data, '赫富500指数增强一号私募基金', '新方程大类配置基金')
        nav_dict['500指增']['赫富'] = adj_nav.loc['20210602':]
        # a = pd.pivot_table(tmp, index='jzrq', columns='khmc', values='jjjz').sort_index()

        "===========================================500================================================================"
        nav_df_500 = pd.concat(nav_dict['500指增'], axis=1).sort_index()
        sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format('000905', nav_df_500.index[0], nav_df_500.index[-1])
        index_data = pd.DataFrame(
            hbs.db_data_query('readonly', sql_script, page_size=5000)['data']).set_index('TRADEDATE')['TCLOSE']
        index_nav = index_data.reindex(nav_df_500.index).to_frame('benchmark')

        excess_return = nav_df_500.pct_change().sub(index_nav.pct_change()['benchmark'].squeeze(), axis=0)
        "===========================================1000==============================================================="
        nav_df_1000 = pd.concat(nav_dict['1000指增'], axis=1).sort_index()
        # 手动添加赫富
        nav_hf = pd.read_excel('D:\\Daily-赫富1000指数增强一号日数据-20220722.xlsx', header=3)
        nav_hf.rename(columns={"净值日期": "trade_date", "累计单位净值": "赫富"}, inplace=True)
        nav_hf['trade_date'] = nav_hf['trade_date'].apply(lambda x: x.replace('-', '') if type(x) == str else datetime.strftime(x, '%Y%m%d'))
        nav_hf = nav_hf.set_index('trade_date')[['赫富']]
        nav_df_1000 = pd.merge(nav_df_1000, nav_hf, left_index=True, right_index=True, how='left')
        # 添加九坤
        nv_series = get_fund_nav_from_sql('20220101', '20220729', {"九坤": "SCP381"})
        nav_df_1000 = pd.merge(nav_df_1000, nv_series, left_index=True, right_index=True, how='left')

        sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format('000852', nav_df_1000.index[0], nav_df_1000.index[-1])
        index_data = pd.DataFrame(
            hbs.db_data_query('readonly', sql_script, page_size=5000)['data']).set_index('TRADEDATE')['TCLOSE']
        index_nav = index_data.reindex(nav_df_1000.index).to_frame('benchmark')

        excess_return = nav_df_1000.pct_change().sub(index_nav.pct_change()['benchmark'].squeeze(), axis=0)

        attr_start = '20220701'
        # attr_start = '20210630'
        attr_end = '20220819'
        period_data = excess_return[(excess_return.index >= attr_start) & (excess_return.index <= attr_end)]
        period_data = period_data.dropna(axis=1, how='any').sort_index()

        sql_script = "SELECT * FROM st_ashare.r_st_barra_factor_return where " \
                     "TRADE_DATE >= '{}' and TRADE_DATE <= '{}'".format(attr_start, attr_end)
        res = hbs.db_data_query('alluser', sql_script, page_size=50000)
        factor_return = pd.DataFrame(res['data'])[['trade_date', 'factor_name', 'factor_ret']]
        factor_return = pd.pivot_table(
            factor_return, index='trade_date', columns='factor_name', values='factor_ret').sort_index()[style_names]

        # vif检验
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        vif = [variance_inflation_factor(factor_return.values, factor_return.columns.get_loc(i)) for i in
               factor_return.columns]

        exposure_list = []
        attr_list = []
        for col in excess_return.columns:
            y = np.array(excess_return[col])
            x = factor_return.copy()
            model = sm.OLS(y, x).fit()

            style_attr = x.multiply(model.params)
            # style_attr['resid'] = model.resid
            # style_attr['alpha'] = style_attr['const'] + style_attr['resid']
            style_attr['alpha'] = model.resid
            style_attr = style_attr[['alpha'] + style_names]

            # cum
            kt = np.log(1 + excess_return[col]) / excess_return[col]
            r = (1 + excess_return[col]).prod() - 1
            k = np.log(1 + r) / r

            cum_attr = style_attr.T.multiply(kt / k).sum(axis=1)

            exposure = model.params.loc[style_names].to_frame(col)
            exposure.loc['r_square'] = model.rsquared
            exposure_list.append(exposure)

            ret_attr = cum_attr.to_frame(col)
            attr_list.append(ret_attr)

        factor_map_dict = {"size": "规模", "beta": "Beta", "momentum": "动量", "resvol": "波动率", "btop": "估值",
                           "earnyield": "盈利", "growth": "成长", "leverage": "杠杆",
                           "sizenl": "非线性规模", "liquidity": "流动性", "alpha": "alpha"}

        exposure_df = pd.concat(exposure_list, axis=1).T
        exposure_df.columns = [factor_map_dict[x] for x in exposure_df.columns]
        attr_df = pd.concat(attr_list, axis=1).T
        attr_df.columns = [factor_map_dict[x] for x in attr_df.columns]
        attr_df['风格收益'] = attr_df[attr_df.columns[1:]].sum(axis=1)
        attr_df = attr_df[attr_df.columns[1:].tolist() + ['alpha']]


def daily_attr(start_date, end_date, mode="500指增"):
    if mode == "500指增":
        benchmark_id = "000905"
    else:
        benchmark_id = "000852"

    nav_df = get_daily_nav_from_work(start_date, end_date, daily_fund_nav_dict[mode])

    # 诚奇的拼接
    # nav_df.loc[nav_df['诚奇睿盈500指数增强A'].isnull(), '诚奇睿盈500指数增强A'] = nav_df['诚奇睿盈500指数增强A-former']

    # 明汯1000的拼接
    # nav_df.loc[nav_df['明汯量化中小盘增强1号'].isnull(), '明汯量化中小盘增强1号'] = nav_df['明汯量化中小盘增强1号A']
    # nav_df.loc["20220826", "九坤日享中证1000指数增强1号"] = 3.8730

    nav_df = nav_df.dropna(axis=1).sort_index()

    sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                 "and JYRQ >= {} and JYRQ <= {}".format(benchmark_id, nav_df.index[0], nav_df.index[-1])
    index_data = pd.DataFrame(
        hbs.db_data_query('readonly', sql_script, page_size=5000)['data']).set_index('TRADEDATE')['TCLOSE']
    index_nav = index_data.reindex(nav_df.index).to_frame('benchmark')

    assert (nav_df.shape[0] == index_nav.shape[0])

    excess_return = nav_df.pct_change().sub(index_nav.pct_change()['benchmark'].squeeze(), axis=0)
    excess_return = excess_return.dropna()

    sql_script = "SELECT * FROM st_ashare.r_st_barra_factor_return where " \
                 "TRADE_DATE >= '{}' and TRADE_DATE <= '{}'".format(excess_return.index[0], excess_return.index[-1])
    res = hbs.db_data_query('alluser', sql_script, page_size=50000)
    factor_return = pd.DataFrame(res['data'])[['trade_date', 'factor_name', 'factor_ret']]
    factor_return = pd.pivot_table(
        factor_return, index='trade_date', columns='factor_name', values='factor_ret').sort_index()[style_names]

    # vif检验

    vif = [variance_inflation_factor(factor_return.values, factor_return.columns.get_loc(i)) for i in
           factor_return.columns]

    exposure_list = []
    attr_list = []
    for col in excess_return.columns:
        y = np.array(excess_return[col])
        x = factor_return.copy()
        model = sm.OLS(y, x).fit()

        style_attr = x.multiply(model.params)
        # style_attr['resid'] = model.resid
        # style_attr['alpha'] = style_attr['const'] + style_attr['resid']
        style_attr['alpha'] = model.resid
        style_attr = style_attr[['alpha'] + style_names]

        # cum
        kt = np.log(1 + excess_return[col]) / excess_return[col]
        r = (1 + excess_return[col]).prod() - 1
        k = np.log(1 + r) / r

        cum_attr = style_attr.T.multiply(kt / k).sum(axis=1)

        exposure = model.params.loc[style_names].to_frame(col)
        exposure.loc['r_square'] = model.rsquared
        exposure_list.append(exposure)

        ret_attr = cum_attr.to_frame(col)
        attr_list.append(ret_attr)

    factor_map_dict = {"size": "规模", "beta": "Beta", "momentum": "动量", "resvol": "波动率", "btop": "估值",
                       "earnyield": "盈利", "growth": "成长", "leverage": "杠杆",
                       "sizenl": "非线性规模", "liquidity": "流动性", "alpha": "alpha", "r_square": "r_square"}

    exposure_df = pd.concat(exposure_list, axis=1).T
    exposure_df.columns = [factor_map_dict[x] for x in exposure_df.columns]
    attr_df = pd.concat(attr_list, axis=1).T
    attr_df.columns = [factor_map_dict[x] for x in attr_df.columns]
    attr_df['风格收益'] = attr_df[attr_df.columns[1:]].sum(axis=1)
    attr_df = attr_df[attr_df.columns[1:].tolist() + ['alpha']]

    return exposure_df, attr_df


if __name__ == '__main__':
    # AlphaNavAttribution('20201231', '20220819', '92c89fa3cc884540ba215920e005aa85')
    daily_attr('20221028', '20221202', mode="1000指增")
