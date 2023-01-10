# -*- coding: utf-8 -*-


import os;os.chdir("S:/siat")
from siat import *

if __name__ =="__main__":
    start='2000-1-1'; end='2022-10-9'
    measures=['pe','pb']; methods='lyr'; values='value'; statistics='median'
    df1,df2=valuation_market_china(start,end,measures=['pe','pb'],methods='lyr',values='value',statistics='median')

    df1,df2=valuation_market_china(start,end,measures=['pe','pb'],methods='lyr', \
                                   values='value',statistics='median', \
                                       loc1='upper left',loc2='upper right')


    df1,df2=valuation_market_china(start,end,measures=['pe'],methods='lyr', \
                                   values='value',statistics='median', \
                                       loc1='upper left',loc2='upper right')


    df1,df2=valuation_market_china(start,end,measures=['pe'],methods=['ttm','lyr'], \
                                   values='value',statistics='median', \
                                       loc1='upper left',loc2='upper right')

    df1,df2=valuation_market_china(start,end,measures=['pe'],methods=['ttm'], \
                                   values=['value','quantile'],statistics='median', \
                                       loc1='upper left',loc2='upper right')


    df1,df2=valuation_market_china(start,end,measures=['pe'],methods=['ttm'], \
                                   values=['value'],statistics=['median','equal-weighted'], \
                                       loc1='upper left',loc2='upper right')



