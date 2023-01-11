"""
因子拥挤度
"""
import pandas as pd
import datetime
import os
import hbshare as hbs
import statsmodels.api as sm
from hbshare.fe.common.util.data_loader import get_trading_day_list
from hbshare.quant.Kevin.asset_allocation.macro_index.util import create_table, delete_duplicate_records, WriteToDB
from sqlalchemy import create_engine
from hbshare.quant.Kevin.rm_associated.config import engine_params, style_names, industry_names


class FactorCrowdCalculator:
    """
    个股的换手、波动及beta数据，周度
    """
    def __init__(self, trade_date, data_path, is_increment=1):
        self.trade_date = trade_date
        self.data_path = data_path
        self.is_increment = is_increment
        self._load_pre_date()

    def _load_pre_date(self):
        trade_dt = datetime.datetime.strptime(self.trade_date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=200)).strftime('%Y%m%d')
        trading_day_list = get_trading_day_list(pre_date, self.trade_date)
        self.pre_date = trading_day_list[-60:][0]
        self.start_date = trading_day_list[-61:][0]

    def _calc_turnover_rate(self):
        # 换手率数据
        path = os.path.join(self.data_path, 'turnover_rate')
        listdir = os.listdir(path)
        listdir = [x for x in listdir if self.pre_date <= x.split('.')[0] <= self.trade_date]
        turnover_date = []
        for filename in listdir:
            date_t_rate = pd.read_json(os.path.join(path, '{}'.format(filename)),
                                       typ='series').to_frame('turnover_rate')
            date_t_rate.index.name = 'ticker'
            date_t_rate = date_t_rate.reset_index()
            date_t_rate['trade_date'] = filename.split('.')[0]

            turnover_date.append(date_t_rate)

        turnover_date = pd.concat(turnover_date, axis=0)
        turnover_date['ticker'] = turnover_date['ticker'].apply(lambda x: str(x).zfill(6))
        turnover_date = turnover_date[turnover_date['ticker'].str[0].isin(('0', '3', '6'))]

        turnover_df = pd.pivot_table(
            turnover_date, index='trade_date', columns='ticker', values='turnover_rate').sort_index()
        count_df = turnover_df.isnull().sum()
        included_list = count_df[count_df <= 20].index.tolist()
        turnover_df = turnover_df[included_list]

        return turnover_df.mean().to_frame('mean_to')

    def _calc_volatility(self):
        # 个股收益数据
        path = os.path.join(self.data_path, 'chg_pct')
        listdir = os.listdir(path)
        listdir = [x for x in listdir if self.pre_date <= x.split('.')[0] <= self.trade_date]
        chg_pct = []
        for filename in listdir:
            date_chg_pct = pd.read_csv(os.path.join(path, '{}'.format(filename)),
                                       dtype={'ticker': str, "tradeDate": str})
            chg_pct.append(date_chg_pct)
        chg_pct = pd.concat(chg_pct, axis=0)
        chg_pct.rename(columns={'dailyReturnReinv': 'chg_pct', 'tradeDate': 'trade_date'}, inplace=True)

        chg_pct.loc[chg_pct['chg_pct'] < -0.2, 'chg_pct'] = -0.2
        chg_pct.loc[chg_pct['chg_pct'] > 0.2, 'chg_pct'] = 0.2

        stock_return = pd.pivot_table(chg_pct, index='trade_date', columns='ticker', values='chg_pct').sort_index()
        count_df = stock_return.isnull().sum()
        included_list = count_df[count_df <= 20].index.tolist()
        stock_return = stock_return[included_list]

        return stock_return.std().to_frame('stock_vol'), stock_return

    def _calc_beta(self, stock_return):
        # 指数收益-Wind全A
        sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format('801813', self.start_date, self.trade_date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
        index_return = data.set_index('TRADEDATE')['TCLOSE'].pct_change().dropna().reindex(stock_return.index)

        reg_x = sm.add_constant(index_return)

        beta_series = stock_return.apply(lambda y: sm.OLS(y, reg_x, missing='drop').fit().params[1], axis=0)

        return beta_series.to_frame('beta')

    def daily_calc(self):
        mean_to = self._calc_turnover_rate()
        stock_vol, stock_return = self._calc_volatility()
        beta = self._calc_beta(stock_return)

        result_df = mean_to.merge(stock_vol, left_index=True, right_index=True).merge(
            beta, left_index=True, right_index=True).reset_index()
        result_df['trade_date'] = self.trade_date

        return result_df

    def get_construct_result(self):
        if self.is_increment == 1:
            data = self.daily_calc()
            sql_script = "delete from factor_crowd where trade_date in ({})".format(
                ','.join(data['trade_date'].tolist()))
            # delete first
            delete_duplicate_records(sql_script)
            # add new records
            WriteToDB().write_to_db(data, 'factor_crowd')
        else:
            sql_script = """
                create table factor_crowd(
                id int auto_increment primary key,
                trade_date date not null,
                ticker varchar(20),
                mean_to decimal(6, 4),
                stock_vol decimal(6, 4),
                beta decimal(6,4 )) 
            """
            create_table('factor_crowd', sql_script)
            data = self.daily_calc()
            WriteToDB().write_to_db(data, 'factor_crowd')


def get_style_factor(trade_date, factor_name):
    sql_script = "SELECT * FROM st_ashare.r_st_barra_style_factor where TRADE_DATE = '{}'".format(trade_date)
    res = hbs.db_data_query('alluser', sql_script, page_size=5000)
    style_factor = pd.DataFrame(res['data']).set_index('ticker')[factor_name]

    return style_factor


def get_style_factor_local(trade_date, factor_name):
    factor_path = r'D:\kevin\risk_model_jy\RiskModel\data'
    factor_path = os.path.join(factor_path, r'zzqz_sw\style_factor')
    style_factor = pd.read_csv(
        os.path.join(factor_path, '{0}.csv'.format(trade_date)), dtype={"ticker": str}).set_index('ticker')[factor_name]

    return style_factor


class FactorCrowdTest:
    def __init__(self, trade_date, factor_series):
        self.trade_date = trade_date
        self.factor_series = factor_series

    def _load_future_date(self):
        trade_dt = datetime.datetime.strptime(self.trade_date, '%Y%m%d')
        next_date = (trade_dt + datetime.timedelta(days=30)).strftime('%Y%m%d')
        trading_day_list = get_trading_day_list(self.trade_date, next_date, frequency="week")

        return trading_day_list[trading_day_list.index(self.trade_date) + 1]

    def _load_industry_data(self):
        path = r'D:\kevin\risk_model_jy\RiskModel\data'
        data = pd.read_json(os.path.join(path, r'common_data/sw_new.json'), dtype={'ticker': str})
        data['outDate'] = data['outDate'].fillna(20991231)
        data['intoDate'] = data['intoDate'].map(int).map(str)
        data['outDate'] = data['outDate'].map(int).map(str)

        data = data[(data['intoDate'] <= self.trade_date) &
                    (data['outDate'] >= self.trade_date)].drop_duplicates(subset='ticker')

        return data.set_index('ticker')['industryName1']

    def _load_future_ret(self, next_week):
        # 个股收益数据
        path = r'D:\kevin\risk_model_jy\RiskModel\data\common_data\chg_pct'
        listdir = os.listdir(path)
        listdir = [x for x in listdir if self.trade_date < x.split('.')[0] <= next_week]
        chg_pct = []
        for filename in listdir:
            date_chg_pct = pd.read_csv(os.path.join(path, '{}'.format(filename)),
                                       dtype={'ticker': str, "tradeDate": str})
            chg_pct.append(date_chg_pct)
        chg_pct = pd.concat(chg_pct, axis=0)
        chg_pct.rename(columns={'dailyReturnReinv': 'chg_pct', 'tradeDate': 'trade_date'}, inplace=True)

        chg_pct.loc[chg_pct['chg_pct'] < -0.2, 'chg_pct'] = -0.2
        chg_pct.loc[chg_pct['chg_pct'] > 0.2, 'chg_pct'] = 0.2

        stock_return = pd.pivot_table(chg_pct, index='trade_date', columns='ticker', values='chg_pct').sort_index()

        week_ret = (1 + stock_return).prod() - 1

        return week_ret.to_frame('week_ret')

    def run(self, ind_neu=True):
        next_week = self._load_future_date()
        industry = self._load_industry_data()
        future_ret = self._load_future_ret(next_week)

        calc_df = self.factor_series.to_frame('factor').merge(industry, left_index=True, right_index=True).merge(
            future_ret, left_index=True, right_index=True)
        calc_df['ticker'] = calc_df.index

        upper_qt = calc_df.groupby(
            'industryName1').apply(lambda x: x['factor'].quantile(0.9)).to_frame('upper_qt').reset_index()
        lower_qt = calc_df.groupby(
            'industryName1').apply(lambda x: x['factor'].quantile(0.1)).to_frame('lower_qt').reset_index()

        calc_df = calc_df.merge(upper_qt, on='industryName1').merge(lower_qt, on='industryName1').set_index('ticker')
        # crowd data
        sql_script = "SELECT * FROM factor_crowd where trade_date = '{}'".format(self.trade_date)
        engine = create_engine(engine_params)
        data = pd.read_sql(sql_script, engine)
        data['trade_date'] = data['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
        crowd_df = data.set_index('ticker')[['mean_to', 'stock_vol', 'beta']]

        df = pd.merge(calc_df, crowd_df, left_index=True, right_index=True)
        crowd_list = ['mean_to', 'stock_vol', 'beta']

        if ind_neu:
            long_ratio = df[df['factor'] >= df['upper_qt']][crowd_list].mean()
            short_ratio = df[df['factor'] <= df['lower_qt']][crowd_list].mean()
            long_ret = df[df['factor'] >= df['upper_qt']]['week_ret'].mean()
            short_ret = df[df['factor'] <= df['lower_qt']]['week_ret'].mean()
        else:
            long_ratio = df[df['factor'] >= df['factor'].quantile(0.9)][crowd_list].mean()
            short_ratio = df[df['factor'] <= df['factor'].quantile(0.1)][crowd_list].mean()
            long_ret = df[df['factor'] >= df['factor'].quantile(0.9)]['week_ret'].mean()
            short_ret = df[df['factor'] <= df['factor'].quantile(0.1)]['week_ret'].mean()

        ratio = long_ratio / short_ratio
        t_ratio_df = ratio.to_frame(self.trade_date)
        t_ratio_df.loc['ls_return'] = 0.5 * (long_ret - short_ret)

        return t_ratio_df


class MainFactorCrowd:
    def __init__(self, trade_date, is_increment=1):
        self.trade_date = trade_date
        self.is_increment = is_increment

    def _load_pre_date(self):
        trade_dt = datetime.datetime.strptime(self.trade_date, '%Y%m%d')
        start_date = (trade_dt + datetime.timedelta(days=-20)).strftime('%Y%m%d')
        trading_day_list = get_trading_day_list(start_date, self.trade_date, frequency="week")

        return trading_day_list[trading_day_list.index(self.trade_date) - 1]

    @staticmethod
    def get_style_factor(trade_date, factor_list):
        factor_path = r'D:\kevin\risk_model_jy\RiskModel\data'
        factor_path = os.path.join(factor_path, r'zzqz_sw\style_factor')
        style_factor = pd.read_csv(
            os.path.join(factor_path, '{0}.csv'.format(trade_date)), dtype={"ticker": str}).set_index(
            'ticker')[factor_list]

        return style_factor

    def _load_week_ret(self, pre_week):
        # 个股收益数据
        path = r'D:\kevin\risk_model_jy\RiskModel\data\common_data\chg_pct'
        listdir = os.listdir(path)
        listdir = [x for x in listdir if pre_week < x.split('.')[0] <= self.trade_date]
        chg_pct = []
        for filename in listdir:
            date_chg_pct = pd.read_csv(os.path.join(path, '{}'.format(filename)),
                                       dtype={'ticker': str, "tradeDate": str})
            chg_pct.append(date_chg_pct)
        chg_pct = pd.concat(chg_pct, axis=0)
        chg_pct.rename(columns={'dailyReturnReinv': 'chg_pct', 'tradeDate': 'trade_date'}, inplace=True)

        chg_pct.loc[chg_pct['chg_pct'] < -0.2, 'chg_pct'] = -0.2
        chg_pct.loc[chg_pct['chg_pct'] > 0.2, 'chg_pct'] = 0.2

        stock_return = pd.pivot_table(chg_pct, index='trade_date', columns='ticker', values='chg_pct').sort_index()

        week_ret = (1 + stock_return).prod() - 1

        return week_ret.to_frame('week_ret')

    def calc_factor_crowd(self, df, factor_name):
        crowd_list = ['mean_to', 'stock_vol', 'beta']
        long_ratio = df[df[factor_name] >= df[factor_name].quantile(0.9)][crowd_list].mean()
        short_ratio = df[df[factor_name] <= df[factor_name].quantile(0.1)][crowd_list].mean()

        ratio = long_ratio / short_ratio
        ratio_df = ratio.to_frame(self.trade_date).T
        ratio_df['trade_date'] = ratio_df.index
        ratio_df['factor_name'] = factor_name
        ratio_df.reset_index(drop=True, inplace=True)

        return ratio_df

    def calc_ls_return(self, df, factor_name):
        long_ret = df[df[factor_name] >= df[factor_name].quantile(0.9)]['week_ret'].mean()
        short_ret = df[df[factor_name] <= df[factor_name].quantile(0.1)]['week_ret'].mean()
        ls_return = 0.5 * (long_ret - short_ret)
        ls_df = pd.DataFrame({"factor_name": [factor_name], "trade_date": [self.trade_date], "ls_return": [ls_return]})

        return ls_df

    def weekly_calculate(self):
        pre_week = self._load_pre_date()
        # 手动调整20150904
        if self.trade_date == "20150904":
            self.trade_date = "20150902"
        if pre_week == "20150904":
            pre_week = "20150902"
        # style factor
        style_list = ['size', 'momentum', 'btop', 'growth']
        p_factor_df = self.get_style_factor(pre_week, style_list)
        p_factor_df['size'] *= -1.
        factor_df = self.get_style_factor(self.trade_date, style_list)
        factor_df['size'] *= -1.
        # week ret
        week_ret = self._load_week_ret(pre_week)
        # crowd data
        sql_script = "SELECT * FROM factor_crowd where trade_date = '{}'".format(self.trade_date)
        engine = create_engine(engine_params)
        data = pd.read_sql(sql_script, engine)
        data['trade_date'] = data['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
        crowd_df = data.set_index('ticker')[['mean_to', 'stock_vol', 'beta']]
        # t_crowd
        calc_df = factor_df.merge(crowd_df, left_index=True, right_index=True)
        ratio_list = []
        for factor_name in style_list:
            ratio_df = self.calc_factor_crowd(calc_df, factor_name)
            ratio_list.append(ratio_df)
        t_ratio = pd.concat(ratio_list)
        # pre_ls_return
        sql_script = "SELECT * FROM factor_crowd where trade_date = '{}'".format(pre_week)
        engine = create_engine(engine_params)
        data = pd.read_sql(sql_script, engine)
        data['trade_date'] = data['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
        pre_crowd_df = data.set_index('ticker')[['mean_to', 'stock_vol', 'beta']]
        calc_df = p_factor_df.merge(week_ret, left_index=True, right_index=True).merge(
            pre_crowd_df, left_index=True, right_index=True)
        ret_list = []
        for factor_name in style_list:
            ret_df = self.calc_ls_return(calc_df, factor_name)
            ret_list.append(ret_df)
        t_ret = pd.concat(ret_list)

        return t_ratio, t_ret

    def get_construct_result(self):
        t_ratio, t_ret = self.weekly_calculate()
        if self.is_increment == 1:
            # t_ratio
            sql_script = "delete from crowd_ratio where trade_date in ({})".format(
                ','.join(t_ratio['trade_date'].tolist()))
            delete_duplicate_records(sql_script)
            WriteToDB().write_to_db(t_ratio, 'crowd_ratio')
            # ls_return
            sql_script = "delete from ls_return where trade_date in ({})".format(
                ','.join(t_ret['trade_date'].tolist()))
            delete_duplicate_records(sql_script)
            WriteToDB().write_to_db(t_ret, 'ls_return')
        else:
            # t_ratio
            sql_script = """
                create table crowd_ratio(
                id int auto_increment primary key,
                trade_date date not null,
                factor_name varchar(20),
                mean_to decimal(8, 6),
                stock_vol decimal(8, 6),
                beta decimal(8, 6)) 
            """
            create_table('crowd_ratio', sql_script)
            WriteToDB().write_to_db(t_ratio, 'crowd_ratio')
            # t_ret
            sql_script = """
                create table ls_return(
                id int auto_increment primary key,
                trade_date date not null,
                factor_name varchar(20),
                ls_return decimal(8, 6)) 
            """
            create_table('ls_return', sql_script)
            WriteToDB().write_to_db(t_ret, 'ls_return')


if __name__ == '__main__':
    # import time
    #
    # start_time = time.time()
    # FactorCrowdCalculator('20220826', r'D:\kevin\risk_model_jy\RiskModel\data\common_data').get_construct_result()
    # end_time = time.time()
    # print('程序用时：%s秒' % (end_time - start_time))

    # start_date = '20101015'
    # end_date = '20220930'
    # from tqdm import tqdm
    # date_list = get_trading_day_list(start_date, end_date, frequency="week")
    # for date in tqdm(date_list):
    #     FactorCrowdCalculator(date, r'D:\kevin\risk_model_jy\RiskModel\data\common_data').get_construct_result()

    # FactorCrowdCalculator('20101015', r'D:\kevin\risk_model_jy\RiskModel\data\common_data').get_construct_result()

    # t_date = '20220819'
    # factor = get_style_factor_local(t_date, 'size')
    #
    # FactorCrowdTest(t_date, factor).run()

    # start_date = '20101010'
    # end_date = '20220930'
    # date_list = get_trading_day_list(start_date, end_date, frequency="week")
    # date_list = [x for x in date_list if x != '20150904']
    # from tqdm import tqdm
    # ratio_list = []
    # for date in tqdm(date_list):
    #     factor = get_style_factor_local(date, 'momentum')
    #     t_ratio = FactorCrowdTest(date, factor).run(ind_neu=False)
    #     ratio_list.append(t_ratio)
    #
    # ratio_df = pd.concat(ratio_list, axis=1).T
    # ratio_df['ls_nav'] = (1 + ratio_df['ls_return']).cumprod()
    # ratio_df['mean_ratio'] = ratio_df[['mean_to', 'stock_vol', 'beta']].mean(axis=1)
    #
    # ratio_df.to_csv('D:\\123.csv')

    # 对比
    # data1 = pd.read_excel('D:\\研究基地\\G-专题报告\\因子拥挤度\\因子拥挤-回测数据集合.xlsx', sheet_name=7)
    # data1['日期'] = data1['日期'].apply(lambda x: x.strftime('%Y%m%d'))
    # data1 = data1.set_index('日期')
    # data1['fu_rtn_1M'] = data1['ls_return'].rolling(4).apply(lambda x: (1 + x).prod() - 1).shift(-3)
    # data1['fu_rtn_2M'] = data1['ls_return'].rolling(8).apply(lambda x: (1 + x).prod() - 1).shift(-7)
    # data1['fu_rtn_3M'] = data1['ls_return'].rolling(12).apply(lambda x: (1 + x).prod() - 1).shift(-11)
    # corr_df = data1.dropna().corr()
    # include_list = ['mean_to', 'stock_vol', 'beta', '因子拥挤度', 'fu_rtn_1M', 'fu_rtn_2M', 'fu_rtn_3M']
    # corr_df = corr_df.loc[include_list][include_list]

    # Summary
    # data1 = pd.read_excel('D:\\研究基地\\G-专题报告\\因子拥挤度\\因子拥挤-回测数据集合.xlsx', sheet_name=7)
    # data1['日期'] = data1['日期'].apply(lambda x: x.strftime('%Y%m%d'))
    # data1 = data1.set_index('日期')
    #
    # for col in data1.columns:
    #     data1[col] = (data1[col] - data1[col].mean()) / data1[col].std()

    # sdate = '20101010'
    # # start_date = "20220902"
    # edate = '20220930'
    # date_list = get_trading_day_list(sdate, edate, frequency="week")
    # from tqdm import tqdm
    # for date in tqdm(date_list):
    #     MainFactorCrowd(date).get_construct_result()

    "==================================================更新流程=========================================================="

    date = "20221202"
    FactorCrowdCalculator(date, r'D:\kevin\risk_model_jy\RiskModel\data\common_data').get_construct_result()
    MainFactorCrowd(date).get_construct_result()

