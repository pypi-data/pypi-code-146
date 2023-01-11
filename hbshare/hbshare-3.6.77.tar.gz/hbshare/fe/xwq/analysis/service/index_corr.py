# -*- coding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['kaiti']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

from WindPy import w
w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒
w.isconnected()  # 判断WindPy是否已经登录成功

index = pd.read_excel('D:/Git/hbshare/hbshare/fe/xwq/data/index_corr/index_1.xlsx')
index['INDEX_SYMBOL'] = index['INDEX_SYMBOL'].astype(str)
index['INDEX_NAME'] = index['INDEX_NAME'].astype(str)
index_list = index['INDEX_SYMBOL'].unique().tolist()[:10]
index_list = ",".join(index_list)
index_dict = index.set_index('INDEX_SYMBOL')['INDEX_NAME'].to_dict()
index_data = pd.read_excel('D:/Git/hbshare/hbshare/fe/xwq/data/index_corr/index_1_data.xlsx')
index_data['TRADE_DATE'] = index_data['TRADE_DATE'].apply(lambda x: x.date().strftime('%Y%m%d'))
index_data = index_data.set_index('TRADE_DATE')

for year in ['2000', '2008', '2015', '2020']:
    start = str(int(year) - 1) + '-12-31'
    end = year + '-12-31'
    index_daily_k = w.wsd(index_list, "close", start, end, usedf=True)[1].reset_index()
    index_daily_k = index_daily_k.rename(columns={'index': 'TRADE_DATE'})
    index_daily_k['TRADE_DATE'] = index_daily_k['TRADE_DATE'].apply(lambda x: x.strftime('%Y%m%d'))
    index_daily_k = index_daily_k.set_index('TRADE_DATE')
    index_corr = index_daily_k.merge(index_data, left_index=True, right_index=True, how='left')
    index_corr = index_corr.corr()
    index_corr = index_corr.rename(columns=index_dict)
    index_corr = index_corr.rename(index=index_dict)

    plt.figure(figsize=(12, 8))
    sns.heatmap(index_corr, annot=False, fmt='.2f', cmap='coolwarm')
    plt.xlabel('')
    plt.ylabel('')
    plt.title(year, fontdict={'font': 'kaiti', 'weight': 'bold', 'size': 16})
    plt.tight_layout()
    plt.savefig('D:/Git/hbshare/hbshare/fe/xwq/data/index_corr/{0}.png'.format(year))

index = pd.read_excel('D:/Git/hbshare/hbshare/fe/xwq/data/index_corr/index_2.xlsx')
index['INDEX_SYMBOL'] = index['INDEX_SYMBOL'].astype(str)
index['INDEX_NAME'] = index['INDEX_NAME'].astype(str)
index_list = index['INDEX_SYMBOL'].unique().tolist()[:-1]
index_list = ",".join(index_list)
index_dict = index.set_index('INDEX_SYMBOL')['INDEX_NAME'].to_dict()
index_data = pd.read_excel('D:/Git/hbshare/hbshare/fe/xwq/data/index_corr/index_2_data.xlsx')
index_data['TRADE_DATE'] = index_data['TRADE_DATE'].apply(lambda x: x.date().strftime('%Y%m%d'))
index_data['YEAR'] = index_data['TRADE_DATE'].apply(lambda x: str(x)[:4])
index_data = index_data.sort_values('TRADE_DATE').drop_duplicates('YEAR', keep='last')
index_data = index_data.drop('TRADE_DATE', axis=1).set_index('YEAR')

index_daily_k = w.wsd(index_list, "close", "2009-12-31", "2022-10-31", "Period=Y;Days=Alldays", usedf=True)[1].reset_index()
index_daily_k = index_daily_k.rename(columns={'index': 'TRADE_DATE'})
index_daily_k['TRADE_DATE'] = index_daily_k['TRADE_DATE'].apply(lambda x: x.strftime('%Y%m%d'))
index_daily_k['YEAR'] = index_daily_k['TRADE_DATE'].apply(lambda x: str(x)[:4])
index_daily_k = index_daily_k.sort_values('TRADE_DATE').drop_duplicates('YEAR', keep='last')
index_daily_k = index_daily_k.drop('TRADE_DATE', axis=1).set_index('YEAR')

index_ret = index_daily_k.merge(index_data, left_index=True, right_index=True, how='left')
index_ret = index_ret.pct_change().dropna(how='all')
index_ret = index_ret.rename(columns=index_dict)
index_ret = index_ret.T
index_ret.to_excel('D:/Git/hbshare/hbshare/fe/xwq/data/index_corr/index_ret.xlsx')
