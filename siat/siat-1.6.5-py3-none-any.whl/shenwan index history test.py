# -*- coding: utf-8 -*-
"""
功能：获取申万一级行业历史行情指数
"""

from opendatatools import swindex
import pandas as pd

# 1. 获取申万指数列表
cata, msg = swindex.get_index_list()
cata.head(20)

# 2. 获取申万指数成分信息

content, msg = swindex.get_index_cons('801040')

# 3. 获取申万指数日线

daily, msg = swindex.get_index_daily('801040','2010-01-01', '2021-02-24')
daily.tail(20)

# 4. 获取申万指数每日的量化指标（pe、pb等）

quant, msg = swindex.get_index_dailyindicator('801040', '2010-01-01', '2021-02-24',freq='d')
quant.head(20)

# 示例：查取申万所有一级行业任意时间区间走势
def get_price_sw_industry(start_date, end_date):
    cata, msg = swindex.get_index_list()
    first_industry = cata.iloc[18:46, 0:2].reset_index(drop=True)
    price = pd.DataFrame()
    for i in range(0,len(first_industry)):
        daily, msg = swindex.get_index_daily(first_industry.iloc[i,0],start_date, end_date)
        close = daily[['date', 'close']].sort_values(by="date", ascending=True).set_index('date').rename(columns={'close': first_industry.iloc[i,1]})
        price = pd.concat([price,close],axis=1, join='outer').astype('float')
        
        price.to_excel('data/申万一级行业行情走势.xlsx', sheet_name='指数')

    return price

get_price_sw_industry('2020-10-01','2020-12-31')
