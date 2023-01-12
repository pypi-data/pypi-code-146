from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
import pandas as pd

def get_stock_industry():
    stock_industry = HBDB().read_stock_industry()
    stock_industry.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/stock_industry.hdf', key='table', mode='w')
    stock_industry = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/stock_industry.hdf', key='table')
    stock_industry = stock_industry.rename(columns={'zqdm': 'TICKER_SYMBOL', 'flmc': 'INDUSTRY_NAME', 'fldm': 'INDUSTRY_ID', 'hyhfbz': 'INDUSTRY_VERSION', 'fljb': 'INDUSTRY_TYPE', 'qsrq': 'BEGIN_DATE', 'jsrq': 'END_DATE', 'sfyx': 'IS_NEW'})
    stock_industry = stock_industry.dropna(subset=['BEGIN_DATE'])
    stock_industry['END_DATE'] = stock_industry['END_DATE'].fillna('20990101')
    stock_industry['BEGIN_DATE'] = stock_industry['BEGIN_DATE'].astype(int).astype(str)
    stock_industry['END_DATE'] = stock_industry['END_DATE'].astype(int).astype(str)
    stock_industry['INDUSTRY_VERSION'] = stock_industry['INDUSTRY_VERSION'].astype(int)
    stock_industry['INDUSTRY_TYPE'] = stock_industry['INDUSTRY_TYPE'].astype(int)
    stock_industry['IS_NEW'] = stock_industry['IS_NEW'].astype(int)
    stock_industry = stock_industry[stock_industry['INDUSTRY_VERSION'] == 2]
    stock_industry = stock_industry.loc[stock_industry['TICKER_SYMBOL'].str.len() == 6]
    stock_industry = stock_industry.loc[stock_industry['TICKER_SYMBOL'].astype(str).str.slice(0, 1).isin(['0', '3', '6'])]
    return stock_industry

if __name__ == '__main__':
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/'
    holding = pd.read_excel(data_path + '稳博持仓数据.xlsx')
    holding['ticker'] = holding['ticker'].apply(lambda x: str(x).zfill(6))
    stock_industry = get_stock_industry()
    stock_industry = stock_industry[stock_industry['IS_NEW'] == 1]
    stock_industry_sw1 = stock_industry[stock_industry['INDUSTRY_TYPE'] == 1][['TICKER_SYMBOL', 'INDUSTRY_ID', 'INDUSTRY_NAME']].rename(columns={'TICKER_SYMBOL': 'ticker', 'INDUSTRY_ID': '申万一级行业代码', 'INDUSTRY_NAME': '申万一级行业名称'})
    stock_industry_sw2 = stock_industry[stock_industry['INDUSTRY_TYPE'] == 2][['TICKER_SYMBOL', 'INDUSTRY_ID', 'INDUSTRY_NAME']].rename(columns={'TICKER_SYMBOL': 'ticker', 'INDUSTRY_ID': '申万二级行业代码', 'INDUSTRY_NAME': '申万二级行业名称'})
    stock_industry_sw3 = stock_industry[stock_industry['INDUSTRY_TYPE'] == 3][['TICKER_SYMBOL', 'INDUSTRY_ID', 'INDUSTRY_NAME']].rename(columns={'TICKER_SYMBOL': 'ticker', 'INDUSTRY_ID': '申万三级行业代码', 'INDUSTRY_NAME': '申万三级行业名称'})
    holding = holding.merge(stock_industry_sw1, on=['ticker'], how='left').merge(stock_industry_sw2, on=['ticker'], how='left').merge(stock_industry_sw3, on=['ticker'], how='left')
    holding.to_excel(data_path + '稳博持仓数据（行业）.xlsx')