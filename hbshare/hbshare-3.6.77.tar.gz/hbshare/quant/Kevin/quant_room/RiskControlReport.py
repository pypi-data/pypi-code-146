"""
风险控制专题报告-代码1，代码2在组合优化项目中
"""
import numpy as np
import pandas as pd
import hbshare as hbs
from tqdm import tqdm
import statsmodels.api as sm
import datetime
import os
from sqlalchemy import create_engine
from hbshare.quant.Kevin.rm_associated.config import engine_params
from hbshare.fe.common.util.config import style_name, industry_name
from hbshare.fe.common.util.data_loader import get_trading_day_list
from hbshare.quant.Kevin.rm_associated.config import style_names


def save_mkt_data_to_csv(start_date, end_date):
    trading_day_list = get_trading_day_list(start_date, end_date)

    for date in tqdm(trading_day_list):
        # MKT
        sql_script = "SELECT SYMBOL, TDATE, TCLOSE, VATURNOVER, PCHG, MCAP, TCAP FROM finchina.CHDQUOTE WHERE" \
                     " TDATE = {}".format(date)
        res = hbs.db_data_query('readonly', sql_script, page_size=6000)
        df = pd.DataFrame(res['data'])
        df = df[df['SYMBOL'].str[0].isin(['0', '3', '6'])]
        df.rename(columns={"SYMBOL": "ticker", "TDATE": "tradeDate", "TCAP": "marketValue",
                           "MCAP": "negMarketValue", "VATURNOVER": "turnoverValue",
                           "PCHG": "dailyReturnReinv"}, inplace=True)
        # BP
        sql_script = "SELECT a.TradingDay, a.PB, b.SecuCode From " \
                     "hsjy_gg.LC_DIndicesForValuation a join hsjy_gg.SecuMain b on a.InnerCode = b.InnerCode where " \
                     "to_char(a.TradingDay,'yyyymmdd') = {}".format(date)
        res = hbs.db_data_query('readonly', sql_script, page_size=6000)
        bp_data_main = pd.DataFrame(res['data']).rename(columns={"SECUCODE": "ticker"})[['ticker', 'PB']]
        sql_script = "SELECT a.TradingDay, a.PB, b.SecuCode From " \
                     "hsjy_gg.LC_STIBDIndiForValue a join hsjy_gg.SecuMain b on a.InnerCode = b.InnerCode where " \
                     "to_char(a.TradingDay,'yyyymmdd') = {}".format(date)
        res = hbs.db_data_query('readonly', sql_script, page_size=6000)
        if len(res['data']) == 0:
            bp_data = bp_data_main
        else:
            bp_data_stib = pd.DataFrame(res['data']).rename(columns={"SECUCODE": "ticker"})[['ticker', 'PB']]
            bp_data = pd.concat([bp_data_main, bp_data_stib])
            bp_data = bp_data[bp_data['ticker'].str[0].isin(['0', '3', '6'])]

        data = df.merge(bp_data, on='ticker')
        include_cols = ['ticker', 'negMarketValue', 'marketValue', 'turnoverValue', 'dailyReturnReinv', 'PB']
        data[include_cols].to_csv('D:\\MarketInfoSaver\\market_info_{}.csv'.format(date), index=False)
        print("{}: 有效数据{}条".format(date, data.shape[0]))


def cal_illiq_factor(start_date, end_date):
    """
    计算非流动性因子
    """
    month_list = get_trading_day_list(start_date, end_date, frequency="month")
    illiq = []
    for i in tqdm(range(1, len(month_list))):
        pre_date, t_date = month_list[i - 1], month_list[i]
        path = "D:\\MarketInfoSaver"
        listdir = os.listdir(path)
        listdir = [x for x in listdir if pre_date < x.split('_')[-1].split('.')[0] <= t_date]
        data = []
        for filename in listdir:
            trade_date = filename.split('.')[0].split('_')[-1]
            date_t_data = pd.read_csv(os.path.join(path, filename))
            date_t_data['ticker'] = date_t_data['ticker'].apply(lambda x: str(x).zfill(6))
            date_t_data['trade_date'] = trade_date
            data.append(date_t_data)
        data = pd.concat(data)
        data.loc[data['turnoverValue'] < 1e-8, 'dailyReturnReinv'] = np.NaN
        data['illiq'] = data['dailyReturnReinv'].abs() / (data['turnoverValue'] / 1e+9)
        data = pd.pivot_table(data, index='trade_date', columns='ticker', values='illiq').sort_index()

        na_counts = data.isnull().sum()
        exclude_list = na_counts[na_counts >= data.shape[0] * 0.7].index.tolist()

        t_factor = data.mean().to_frame('illiq')
        t_factor.loc[exclude_list] = np.NaN
        t_factor['trade_date'] = t_date
        t_factor = t_factor.reset_index()

        illiq.append(t_factor)

    illiq = pd.concat(illiq)
    illiq.to_csv("D:\\研究基地\\G-专题报告\\alpha策略的风控管理\\非流动性因子.csv", index=False)


def ols(y, x):
    x_ = sm.add_constant(x.copy())
    model = sm.OLS(y, x_, )
    results = model.fit()
    return np.std(results.resid), results.rsquared


def call_ivff_factor(start_date, end_date):
    """
    计算特质波动率（特异度）因子
    """
    month_list = get_trading_day_list(start_date, end_date, frequency="month")
    ivr_list = []
    for i in tqdm(range(1, len(month_list))):
        pre_date, t_date = month_list[i - 1], month_list[i]
        path = "D:\\MarketInfoSaver"
        listdir = os.listdir(path)
        listdir = [x for x in listdir if pre_date < x.split('_')[-1].split('.')[0] <= t_date]
        data = []
        for filename in listdir:
            trade_date = filename.split('.')[0].split('_')[-1]
            date_t_data = pd.read_csv(os.path.join(path, filename))
            date_t_data['ticker'] = date_t_data['ticker'].apply(lambda x: str(x).zfill(6))
            date_t_data['trade_date'] = trade_date
            data.append(date_t_data)
        data = pd.concat(data)
        data.loc[data['turnoverValue'] < 1e-8, 'dailyReturnReinv'] = np.NaN

        stock_return = data[['trade_date', 'ticker', 'dailyReturnReinv', 'negMarketValue', 'PB']].dropna()
        stock_return['negMarketValue'] /= 1e+9
        stock_return['dailyReturnReinv'] /= 100.

        grouped_df = stock_return.groupby('trade_date')
        quantile_df = grouped_df['negMarketValue'].quantile(0.33).to_frame('mkv_lower').merge(
            grouped_df['negMarketValue'].quantile(0.66).to_frame('mkv_upper'), left_index=True, right_index=True).merge(
            grouped_df['PB'].quantile(0.33).to_frame('pb_lower'), left_index=True, right_index=True).merge(
            grouped_df['PB'].quantile(0.66).to_frame('pb_upper'), left_index=True, right_index=True).reset_index()
        stock_return = stock_return.merge(quantile_df, on='trade_date')
        stock_return['w_ret'] = stock_return['dailyReturnReinv'] * stock_return['negMarketValue']
        # 市场收益
        market_return = stock_return.groupby('trade_date').apply(
            lambda x: (x['w_ret'] / x['negMarketValue'].sum()).sum())
        # 市值因子收益
        size_return_small = stock_return.groupby('trade_date').apply(
            lambda x: (x[x['negMarketValue'] <= x['mkv_lower']]['w_ret']).sum() /
                      (x[x['negMarketValue'] <= x['mkv_lower']]['negMarketValue']).sum())
        size_return_large = stock_return.groupby('trade_date').apply(
            lambda x: (x[x['negMarketValue'] >= x['mkv_upper']]['w_ret']).sum() /
                      (x[x['negMarketValue'] >= x['mkv_upper']]['negMarketValue']).sum())
        size_return = size_return_small - size_return_large
        # 估值因子收益
        pb_return_low = stock_return.groupby('trade_date').apply(
            lambda x: (x[x['PB'] <= x['pb_lower']]['w_ret']).sum() /
            (x[x['PB'] <= x['pb_lower']]['negMarketValue']).sum())
        pb_return_high = stock_return.groupby('trade_date').apply(
            lambda x: (x[x['PB'] >= x['pb_upper']]['w_ret']).sum() /
            (x[x['PB'] >= x['pb_upper']]['negMarketValue']).sum())
        pb_return = pb_return_low - pb_return_high
        reg_data = market_return.to_frame('beta').merge(
            size_return.to_frame('size'), left_index=True, right_index=True).merge(
            pb_return.to_frame('value'), left_index=True, right_index=True)
        reg_data = stock_return[['trade_date', 'ticker', 'dailyReturnReinv']].merge(reg_data, on='trade_date')
        # regression
        res = reg_data.groupby(by='ticker').apply(lambda x: ols(x['dailyReturnReinv'], x[['beta', 'size', 'value']]))
        index = [i[0] for i in reg_data.groupby(by='ticker')]

        ivol = pd.Series(index=index, data=[x[0] for x in res]) * np.sqrt(252)
        ivr = 1 - pd.Series(index=index, data=[x[1] for x in res])

        t_factor = ivol.to_frame('ivff').merge(ivr.to_frame('ivr'), left_index=True, right_index=True).reset_index()
        t_factor['trade_date'] = t_date

        ivr_list.append(t_factor)

    ivr_df = pd.concat(ivr_list)
    ivr_df.to_csv("D:\\研究基地\\G-专题报告\\alpha策略的风控管理\\特质波动率因子.csv", index=False)


def factor_preprocess(factor_df, factor_name):
    df = factor_df.copy()
    date_list = sorted(factor_df['trade_date'].unique())
    processed_factor = []
    for date in tqdm(date_list):
        t_df = df[df['trade_date'] == date].dropna()
        # 去极值
        median = df[factor_name].median()
        new_median = abs(df[factor_name] - median).median()
        up = median + 5 * new_median
        down = median - 5 * new_median
        t_df[factor_name] = t_df[factor_name].clip(down, up)
        # 中性化
        sql_script = "SELECT * FROM st_ashare.r_st_barra_style_factor where TRADE_DATE = '{}'".format(date)
        res = hbs.db_data_query('alluser', sql_script, page_size=5000)
        style_factor = pd.DataFrame(res['data'])[['ticker'] + style_names]
        t_df = t_df.merge(style_factor, on='ticker')
        x = np.array(t_df[style_names])
        x_ = sm.add_constant(x.copy())
        model = sm.OLS(t_df[factor_name], x_, )
        t_df[factor_name + '_neu'] = model.fit().resid
        # 标准化
        t_df[factor_name + '_std'] = \
            (t_df[factor_name + '_neu'] - t_df[factor_name + '_neu'].mean()) / t_df[factor_name + '_neu'].std()

        processed_factor.append(t_df)

    processed_factor = pd.concat(processed_factor)
    # processed_factor.groupby('trade_date').apply(lambda x: x.corr().loc['illiq', style_names]).mean()

    return processed_factor[['trade_date', 'ticker', factor_name, factor_name + '_neu', factor_name + '_std']]


def cal_factor_ic(factor_df, factor_name):
    df = factor_df.copy()
    month_list = get_trading_day_list('20191220', '20221120', frequency="month")
    ic_list = []
    for i in tqdm(range(1, len(month_list))):
        pre_date, t_date = month_list[i - 1], month_list[i]
        path = "D:\\MarketInfoSaver"
        listdir = os.listdir(path)
        listdir = [x for x in listdir if pre_date < x.split('_')[-1].split('.')[0] <= t_date]
        data = []
        for filename in listdir:
            trade_date = filename.split('.')[0].split('_')[-1]
            date_t_data = pd.read_csv(os.path.join(path, filename))
            date_t_data['ticker'] = date_t_data['ticker'].apply(lambda x: str(x).zfill(6))
            date_t_data['trade_date'] = trade_date
            data.append(date_t_data)
        data = pd.concat(data)
        data.loc[data['turnoverValue'] < 1e-8, 'dailyReturnReinv'] = np.NaN
        data['dailyReturnReinv'] /= 100.

        data = data.pivot(index='trade_date', columns='ticker', values='dailyReturnReinv').sort_index()
        future_ret = (1 + data).prod() - 1
        t_df = df[df['trade_date'] == pre_date].copy()
        t_df = t_df.set_index('ticker').merge(future_ret.to_frame('f_ret'), left_index=True, right_index=True)
        del t_df['trade_date']
        corr_df = t_df.corr().loc['f_ret', [factor_name, factor_name + '_neu', factor_name + '_std']].to_frame(pre_date)
        ic_list.append(corr_df)

    ic_df = pd.concat(ic_list, axis=1)
    print(ic_df.mean(axis=1))


class PortfolioRiskPredict:
    """
    组合风险预测类
    """
    def __init__(self, trade_date, fund_name, fund_id, benchmark_id="000905"):
        self.trade_date = trade_date
        self.fund_name = fund_name
        self.fund_id = fund_id
        self.benchmark_id = benchmark_id
        self._load_data()

    def _load_shift_date(self):
        trade_dt = datetime.datetime.strptime(self.trade_date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=100)).strftime('%Y%m%d')

        sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            pre_date, self.trade_date)
        res = hbs.db_data_query('readonly', sql_script, page_size=5000)
        df = pd.DataFrame(res['data']).rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                     "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

        trading_day_list = df[df['isMonthEnd'] == 1]['calendarDate'].tolist()

        return trading_day_list[-1]

    def _load_portfolio_weight_series(self):
        sql_script = "SELECT * FROM private_fund_holding where fund_name = '{}' and trade_date = {}".format(
            self.fund_name, self.trade_date)
        engine = create_engine(engine_params)
        holding_df = pd.read_sql(sql_script, engine)
        holding_df['trade_date'] = holding_df['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))

        return holding_df.set_index('ticker')['weight'] / 100.

    def _load_benchmark_weight_series(self, date):
        sql_script = "SELECT * FROM hsjy_gg.SecuMain where SecuCategory = 4 and SecuCode = '{}'".format(
            self.benchmark_id)
        res = hbs.db_data_query('readonly', sql_script)
        index_info = pd.DataFrame(res['data'])
        inner_code = index_info.set_index('SECUCODE').loc[self.benchmark_id, 'INNERCODE']

        sql_script = "SELECT (select a.SecuCode from hsjy_gg.SecuMain a where a.InnerCode = b.InnerCode and " \
                     "rownum = 1) SecuCode, b.EndDate, b.Weight FROM hsjy_gg.LC_IndexComponentsWeight b WHERE " \
                     "b.IndexCode = '{}' and b.EndDate = to_date('{}', 'yyyymmdd')".format(inner_code, date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
        weight_df = data.rename(
            columns={"SECUCODE": "consTickerSymbol", "ENDDATE": "effDate", "WEIGHT": "weight"})

        return weight_df.set_index('consTickerSymbol')['weight'] / 100.

    @staticmethod
    def _load_style_exposure(date):
        sql_script = "SELECT * FROM st_ashare.r_st_barra_style_factor where TRADE_DATE = '{}'".format(date)
        res = hbs.db_data_query('alluser', sql_script, page_size=5000)
        exposure_df = pd.DataFrame(res['data']).set_index('ticker')
        ind_names = [x.lower() for x in industry_name['sw'].values()]
        exposure_df = exposure_df[style_name + ind_names + ['country']]

        return exposure_df

    @staticmethod
    def _load_factor_cov(date):
        sql_script = "SELECT * FROM st_ashare.r_st_barra_factor_cov where TRADE_DATE = '{}'".format(date)
        res = hbs.db_data_query('alluser', sql_script, page_size=1000)
        factor_cov = pd.DataFrame(res['data'])
        factor_cov['factor_name'] = factor_cov['factor_name'].apply(lambda x: x.lower())
        ind_names = [x.lower() for x in industry_name['sw'].values()]
        factor_list = style_name + ind_names + ['country']
        factor_cov = factor_cov.set_index('factor_name').reindex(factor_list)[factor_list]

        return factor_cov

    @staticmethod
    def _load_srisk(date):
        sql_script = "SELECT * FROM st_ashare.r_st_barra_s_risk where TRADE_DATE = '{}'".format(date)
        res = hbs.db_data_query('alluser', sql_script, page_size=5000)
        srisk = pd.DataFrame(res['data']).set_index('ticker')
        srisk.rename(columns={"s_ret": "srisk"}, inplace=True)

        return srisk[['srisk']]

    def _load_fund_ret(self, start_date):
        sql_params = {
            "ip": "192.168.223.152",
            "user": "readonly",
            "pass": "c24mg2e6",
            "port": "3306",
            "database": "work"
        }
        engine_params1 = "mysql+pymysql://{}:{}@{}:{}/{}".format(sql_params['user'], sql_params['pass'],
                                                                 sql_params['ip'],
                                                                 sql_params['port'], sql_params['database'])
        engine1 = create_engine(engine_params1)
        sql_script = "SELECT * FROM daily_nav where code = '{}' and date >= '{}'".format(
            self.fund_id, start_date)
        data = pd.read_sql(sql_script, engine1)
        data['date'] = data['date'].map(str)

        nav_df = data.set_index('date')['fqjz']

        sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format(self.benchmark_id, nav_df.index[0], nav_df.index[-1])
        index_data = pd.DataFrame(
            hbs.db_data_query('readonly', sql_script, page_size=5000)['data']).set_index('TRADEDATE')['TCLOSE']
        index_nav = index_data.reindex(nav_df.index).to_frame('benchmark')

        assert (nav_df.shape[0] == index_nav.shape[0])

        excess_return = nav_df.pct_change().sub(index_nav.pct_change()['benchmark'].squeeze(), axis=0)
        excess_return = excess_return.dropna()

        return excess_return.head(21)

    def _load_data(self):
        shift_date = self._load_shift_date()
        self.portfolio_weight_series = self._load_portfolio_weight_series()
        self.benchmark_weight_series = self._load_benchmark_weight_series(shift_date)
        self.exposure_df = self._load_style_exposure(shift_date)
        self.factor_cov = self._load_factor_cov(shift_date)
        self.srisk = self._load_srisk(shift_date)
        self.fund_ret = self._load_fund_ret(shift_date)

    def run(self):
        weight_df = self.portfolio_weight_series.to_frame('port').merge(
            self.benchmark_weight_series.to_frame('bm'), left_index=True, right_index=True, how='outer').fillna(0.)
        weight_df['active'] = weight_df['port'] - weight_df['bm']
        exposure_df = self.exposure_df.astype(float)
        factor_cov = self.factor_cov.divide(12 * 10000)
        srisk = self.srisk ** 2 * 21

        idx = set(weight_df.index).intersection(set(exposure_df.index)).intersection(set(srisk.index))

        weight = weight_df.reindex(idx)[['active']]
        exposure_df = exposure_df.reindex(idx)
        srisk = srisk.reindex(idx)['srisk']

        common_risk = np.mat(weight).T.dot(
            np.mat(exposure_df).dot(np.mat(factor_cov)).dot(np.mat(exposure_df).T)).dot(np.mat(weight))
        specific_risk = np.mat(weight).T.dot(np.diag(srisk)).dot(np.mat(weight))

        risk = np.sqrt(np.array(common_risk + specific_risk)[0][0]) * np.sqrt(12)
        # common_risk = np.array(common_risk)[0][0]
        # specific_risk = np.array(specific_risk)[0][0]

        actual_risk = self.fund_ret.std() * np.sqrt(252)

        print("{}_{}：预期风险: {}, 实际风险: {}".format(self.fund_name, self.trade_date, risk, actual_risk))

        # a = pd.Series(data=[common_risk * 12, specific_risk * 12, risk, actual_risk])

        return risk, actual_risk


if __name__ == '__main__':
    save_mkt_data_to_csv('20221128', '20221206')
    # cal_illiq_factor('20191120', '20221031')
    # call_ivff_factor('20191120', '20221031')

    # factor = pd.read_csv("D:\\研究基地\\G-专题报告\\alpha策略的风控管理\\特质波动率因子.csv", dtype={"trade_date": str})
    # factor.rename(columns={"index": "ticker"}, inplace=True)
    # factor['ticker'] = factor['ticker'].apply(lambda x: str(x).zfill(6))
    # p_factor = factor_preprocess(factor, 'ivr')
    # ic = cal_factor_ic(p_factor, 'ivr')

    # factor = pd.read_csv("D:\\研究基地\\G-专题报告\\alpha策略的风控管理\\非流动性因子.csv", dtype={"trade_date": str})
    # factor['ticker'] = factor['ticker'].apply(lambda x: str(x).zfill(6))
    # p_factor = factor_preprocess(factor, 'illiq')
    # ic = cal_factor_ic(p_factor, 'illiq')

    # ic_df = pd.read_excel("D:\\研究基地\\G-专题报告\\alpha策略的风控管理\\数据记录.xlsx", sheet_name=1, index_col=0)

    # PortfolioRiskPredict('20220630', '星阔广厦1号中证500指数增强', 'SNU706').run()
    # PortfolioRiskPredict('20220630', '因诺聚配中证500指数增强', 'SGX346').run()
    # PortfolioRiskPredict('20220630', '赫富500指数增强一号', 'SEP463').run()
    # PortfolioRiskPredict('20220630', '概率500指增2号', 'STJ128').run()
    # PortfolioRiskPredict('20220630', '伯兄熙宁', 'STR792').run()
    # PortfolioRiskPredict('20220630', '白鹭精选量化鲲鹏十号', 'P48487').run()
    # PortfolioRiskPredict('20220630', '乾象中证500指数增强1号', 'P48470').run()