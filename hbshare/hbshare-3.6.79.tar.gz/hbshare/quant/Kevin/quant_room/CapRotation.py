"""
大小盘风格的代理变量
"""
import pandas as pd
import hbshare as hbs
import os
from tqdm import tqdm
from hbshare.fe.common.util.data_loader import get_trading_day_list


def get_benchmark_index(start_date, end_date):
    index_codes = ['000300', '000852', '801811', '801813']
    sql_script = "SELECT jyrq as TRADEDATE, zqmc as INDEXNAME, spjg as TCLOSE from " \
                 "st_market.t_st_zs_hqql WHERE " \
                 "ZQDM in ({}) and JYRQ >= {} and " \
                 "JYRQ <= {}".format(','.join("'{0}'".format(x) for x in index_codes),
                                     start_date, end_date)
    res = hbs.db_data_query('alluser', sql_script, page_size=10000)
    index_data = pd.DataFrame(res['data'])
    index_data = index_data.rename(
        columns={"INDEXNAME": "factor_name", "TRADEDATE": "trade_date"})
    index_data['trade_date'] = index_data['trade_date'].map(str)
    index_data = pd.pivot_table(
        index_data, index='trade_date', columns='factor_name', values='TCLOSE').sort_index()
    index_data = index_data / index_data.iloc[0]

    return index_data


def get_mkt_info(start_date, end_date):
    path = r'D:\kevin\risk_model_jy\RiskModel\data\common_data\chg_pct'
    listdir = os.listdir(path)
    listdir = [x for x in listdir if start_date < x.split('.')[0] <= end_date]
    data = []
    for filename in listdir:
        date_t_rate = pd.read_csv(os.path.join(path, filename), dtype={"tradeDate": str})
        date_t_rate['ticker'] = date_t_rate['ticker'].apply(lambda x: str(x).zfill(6))
        data.append(date_t_rate)

    data = pd.concat(data)
    # filter
    data = data[(data['dailyReturnReinv'] >= -0.2) & (data['dailyReturnReinv'] <= 0.2)]
    data = pd.pivot_table(data, index='tradeDate', columns='ticker', values='dailyReturnReinv').sort_index()
    data = data.dropna(how='any', axis=1)

    return data


def get_industry_class(trade_date):
    path = r'D:\kevin\risk_model_jy\RiskModel\data'
    data = pd.read_json(os.path.join(path, r'common_data/sw_new.json'), dtype={'ticker': str})

    data['outDate'] = data['outDate'].fillna(20991231)
    data['intoDate'] = data['intoDate'].map(int).map(str)
    data['outDate'] = data['outDate'].map(int).map(str)

    data = data[(data['intoDate'] <= trade_date) & (data['outDate'] >= trade_date)].drop_duplicates(subset='ticker')

    return data.set_index('ticker')['industryName1']


def get_style_factor_local(trade_date, factor_name):
    factor_path = r'D:\kevin\risk_model_jy\RiskModel\data'
    factor_path = os.path.join(factor_path, r'zzqz_sw\style_factor')
    style_factor = pd.read_csv(
        os.path.join(factor_path, '{0}.csv'.format(trade_date)), dtype={"ticker": str}).set_index('ticker')[factor_name]

    return style_factor


def calculate_index(start_date, end_date, top_ratio=0.5, bottom_ratio=0.5):
    month_end = get_trading_day_list(start_date, end_date, frequency="month")
    month_end.append("20220916")
    all_ret = []
    for i in tqdm(range(len(month_end) - 1)):
        t_month, next_month = month_end[i], month_end[i + 1]
        ind_cls = get_industry_class(t_month).to_frame('industry')
        mkt = get_style_factor_local(t_month, 'size').to_frame('cap')
        df = pd.merge(ind_cls, mkt, left_index=True, right_index=True).reset_index()

        period_data = get_mkt_info(t_month, next_month).fillna(0.)

        upper_qt = df.groupby(
            'industry').apply(lambda x: x['cap'].quantile(1 - top_ratio)).to_frame('upper_qt').reset_index()
        lower_qt = df.groupby(
            'industry').apply(lambda x: x['cap'].quantile(bottom_ratio)).to_frame('lower_qt').reset_index()
        df = df.merge(upper_qt, on='industry').merge(lower_qt, on='industry')
        top_list = df[df['cap'] >= df['upper_qt']]['ticker'].tolist()
        top_list = [x for x in top_list if x in period_data.columns]
        bottom_list = df[df['cap'] <= df['lower_qt']]['ticker'].tolist()
        bottom_list = [x for x in bottom_list if x in period_data.columns]

        top_nav = (1 + period_data[top_list]).cumprod().mean(axis=1)
        top_ret = top_nav.pct_change()
        top_ret.iloc[0] = top_nav.iloc[0] - 1

        bottom_nav = (1 + period_data[bottom_list]).cumprod().mean(axis=1)
        bottom_ret = bottom_nav.pct_change()
        bottom_ret.iloc[0] = bottom_nav.iloc[0] - 1

        period_ret = top_ret.to_frame('top').merge(bottom_ret.to_frame('bottom'), left_index=True, right_index=True)

        all_ret.append(period_ret)

    all_df = pd.concat(all_ret).sort_index()

    return all_df

if __name__ == '__main__':
    benchmark_index = get_benchmark_index('20151231', '20220916')
    calc_index = calculate_index('20151231', '20220916')
    calc_index.loc["20151231"] = 0.
    calc_index = (1 + calc_index.sort_index()).cumprod()

    index_df = pd.concat([benchmark_index, calc_index], axis=1)

    index_ret = index_df.pct_change().fillna(0.)
    index_ret['中证1000 - 沪深300'] = index_ret['中证1000'] - index_ret['沪深300']
    index_ret['小盘指数 - 大盘指数'] = index_ret['小盘指数'] - index_ret['大盘指数']
    index_ret['bottom - top'] = index_ret['bottom'] - index_ret['top']

    tmp = (1 + index_ret).cumprod()[['中证1000 - 沪深300', '小盘指数 - 大盘指数', 'bottom - top']]