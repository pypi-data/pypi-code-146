"""
多策略整理
"""
import pandas as pd
import numpy as np
from datetime import datetime
import hbshare as hbs
from hbshare.quant.Kevin.quant_room.MyUtil.data_loader import get_fund_nav_from_sql, get_trading_day_list
from Arbitrage_backtest import cal_annual_return, cal_annual_volatility, cal_sharpe_ratio, cal_max_drawdown

# 多策略
fund_dict = {
    "明汯多策略对冲1号": "S27825",
    "黑翼策略精选1号": "SGM050",
    "因诺启航1号": "S25540",
    "上海宽德飞凡一号": "SSD811",
    "白鹭鼓浪屿量化多策略一号": "SGY853",
    "白鹭群贤二号": "SCG820",
    "白鹭桃花岛量化对冲一号": "SEW887"
}

start_date = "20150612"
end_date = "20220930"

trading_day_list = get_trading_day_list(start_date, end_date, frequency="week")
nav_df = get_fund_nav_from_sql(start_date, end_date, fund_dict).reindex(trading_day_list)

# 佳期
nv_series = pd.read_excel("D:\\佳期海洋一期历史业绩_20220923.xlsx")
nv_series['净值日期'] = nv_series['净值日期'].apply(lambda x: datetime.strftime(x, "%Y%m%d"))
nv_series = nv_series.rename(
    columns={"净值日期": "trade_date", "单位净值": "佳期海洋一期"}).set_index('trade_date')[['佳期海洋一期']]

nav_df = nav_df.merge(nv_series, left_index=True, right_index=True, how='left')

# 调整
nav_df.loc[:"20181228", '因诺启航1号'] = np.NaN
nav_df.loc[:"20210806", '上海宽德飞凡一号'] = np.NaN
nav_df.loc[:"20190930", '白鹭鼓浪屿量化多策略一号'] = np.NaN
nav_df.loc[:"20190329", '白鹭桃花岛量化对冲一号'] = np.NaN
nav_df.loc[:"20191227", '白鹭群贤二号'] = np.NaN
nav_df.loc["20150904", '明汯多策略对冲1号'] = 1.23

performance_df = pd.DataFrame(
    index=nav_df.columns, columns=["年化收益率", "年化波动率", "最大回撤", "Sharpe比率", "投资胜率", "平均损益比"])

for col in nav_df.columns:
    nav_series = nav_df[col].dropna()
    return_series = nav_series.pct_change().dropna()

    performance_df.loc[col, "年化收益率"] = cal_annual_return(return_series)
    performance_df.loc[col, '年化波动率'] = cal_annual_volatility(return_series)
    performance_df.loc[col, "最大回撤"] = cal_max_drawdown(nav_series)
    performance_df.loc[col, "Sharpe比率"] = cal_sharpe_ratio(return_series, 0.015)
    performance_df.loc[col, "投资胜率"] = return_series.gt(0).sum() / len(return_series)
    performance_df.loc[col, "平均损益比"] = \
        return_series[return_series > 0].mean() / return_series[return_series < 0].abs().mean()

performance_df['年化收益率'] = performance_df['年化收益率'].apply(lambda x: format(x, '.2%'))
performance_df['年化波动率'] = performance_df['年化波动率'].apply(lambda x: format(x, '.2%'))
performance_df['最大回撤'] = performance_df['最大回撤'].apply(lambda x: format(x, '.2%'))
# performance_df['Sharpe比率'] = performance_df['Sharpe比率'].round(2)
performance_df['投资胜率'] = performance_df['投资胜率'].apply(lambda x: format(x, '.2%'))
# performance_df['平均损益比'] = performance_df['平均损益比'].round(2)

# 回测
tmp = nav_df.copy()
tmp['trade_date'] = tmp.index
tmp['trade_dt'] = tmp['trade_date'].apply(lambda x: datetime.strptime(x, "%Y%m%d"))
tmp['month'] = tmp['trade_dt'].apply(lambda x: x.month)
tmp['year'] = tmp['trade_dt'].apply(lambda x: x.year)
month_end = tmp[tmp['month'].shift(-1) != tmp['month']]['trade_date'].tolist()
reb_list = month_end[::3]

ret_list = []
for i in range(len(reb_list) - 1):
    t_date = reb_list[i]
    next_date = reb_list[i + 1]
    period_data = nav_df.loc[t_date: next_date].dropna(axis=1)
    period_data = period_data / period_data.iloc[0]
    period_ret = period_data.mean(axis=1).pct_change().dropna()
    period_df = period_ret.to_frame('ret')
    period_df['num'] = period_data.shape[1]
    ret_list.append(period_df)

ret_df = pd.concat(ret_list)
ret_df['port_nav'] = (1 + ret_df['ret']).cumprod()