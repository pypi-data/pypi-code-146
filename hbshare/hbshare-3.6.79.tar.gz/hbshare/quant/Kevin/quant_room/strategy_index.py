import pandas as pd
from datetime import datetime
import hbshare as hbs
from WindPy import w

w.start()


def strategy_index_compare(start_date, end_date):
    # Wind-招商
    res = w.wsd("CI013002.WI", "close", "2015-12-31", "2022-12-02", "Period=W")
    data = pd.DataFrame(res.Data, index=res.Codes, columns=res.Times).T
    data.index.name = 'trade_date'
    data.reset_index(inplace=True)
    data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
    data.rename(columns={"CI013002.WI": "招商私募指数股票多头"}, inplace=True)
    zs_index = data.set_index('trade_date')
    # 朝阳永续
    data = pd.read_excel("D:\\股票多头策略指数（朝阳+火富牛）.xlsx", sheet_name=0).dropna()
    data = data.rename(columns={"时间": "trade_date", "股票多头典型指数": "朝阳永续股票多头典型指数"})
    data['trade_date'] = data['trade_date'].apply(lambda x: x.replace('-', ''))
    data = data[data['trade_date'] >= '20150101'].set_index('trade_date')
    data.loc["20191231", '股票策略精选指数'] = 2623.03
    data.loc["20191231", '朝阳永续股票多头典型指数'] = 2462.66
    data = data.astype(float)
    zyyx_index = data[['朝阳永续股票多头典型指数']]
    # 火富牛
    data = pd.read_excel("D:\\股票多头策略指数（朝阳+火富牛）.xlsx", sheet_name=1, index_col=0).dropna()
    data['trade_date'] = data.index
    data['trade_date'] = data['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
    hfn_index = data.set_index('trade_date')[['火富牛指数增强精选指数', '火富牛股票多头精选指数']]
    # Howbuy
    sql_script = "SELECT * FROM st_hedge.t_st_sm_zhmzs WHERE zsdm = 'HB1002'"
    res = hbs.db_data_query('highuser', sql_script)
    data = pd.DataFrame(res['data'])
    hb_index = data.set_index('jyrq')['spjg'].to_frame('好买量化多头指数')

    index_df = zs_index.merge(zyyx_index, left_index=True, right_index=True).merge(
        hfn_index, left_index=True, right_index=True).merge(hb_index, left_index=True, right_index=True)
    index_df = index_df / index_df.iloc[0]

    return index_df


if __name__ == '__main__':
    strategy_index_compare("2015-12-31", "2022-12-02")