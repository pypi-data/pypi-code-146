#!/usr/bin/python
# coding:utf-8
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from datetime import datetime
from hbshare.quant.CChen.cons import (
    sql_write_path_hb,
    properties_com_k,
    properties_fin_k,
    db,
    db_tables,
    HSJY_EXCHANGE_INE,
    HSJY_EXCHANGE_CZCE,
    HSJY_EXCHANGE_SHFE,
    HSJY_EXCHANGE_DCE
)
from hbshare.quant.CChen.data.data import load_calendar_extra
from hbshare.quant.CChen.cons import wind_sec
import hbshare as hbs
import pymysql
import re

pymysql.install_as_MySQLdb()

page_size_con = 49999


def trade_calendar(start_date=None, end_date=None, page_size=None):
    if start_date is None:
        start_date = datetime(2010, 1, 1).date()
    if end_date is None:
        end_date = datetime.now().date()
    if page_size is None:
        page_size = page_size_con

    sql = 'select distinct ENDDATE from ' + db_tables['hsjy_com_daily_quote'] \
          + ' where ENDDATE<=TRUNC(to_date(' + end_date.strftime('%Y%m%d') \
          + ', \'yyyymmdd\')) and ENDDATE>=TRUNC(to_date(' + start_date.strftime('%Y%m%d') \
          + ', \'yyyymmdd\')) order by ENDDATE'
    data = hbs.db_data_query(db=db, sql=sql, page_size=page_size)
    if data['pages'] > 1:
        for p in range(2, data['pages'] + 1):
            data['data'] = data['data'] + hbs.db_data_query(db=db, sql=sql, page_size=page_size, page_num=p)['data']

    return pd.to_datetime(pd.DataFrame(data['data'])['ENDDATE']).dt.date.tolist()


def wind_product_index_perc(
        start_date, end_date,
        db_path=sql_write_path_hb['daily'],
        table='fut_index_wind',
        min_volume=10000
):
    engine = create_engine(db_path)
    data = pd.read_sql_query(
        'select `code`, `name`, `t_date`, `close`, `product`, `volume` from ' + table
        + ' where `t_date`<=' + end_date.strftime('%Y%m%d')
        + ' and `t_date`>=' + start_date.strftime('%Y%m%d')
        + ' and `code` like \'%FI.WI\''
        + ' and `product` not in (\'index\') order by `t_date` desc',
        engine
    )

    products = data.drop_duplicates(['product'])['product'].reset_index(drop=True)

    price_perc = []
    name_list = []
    for i in range(len(products)):
        product_data = data[data['product'] == products[i]].reset_index(drop=True)
        if product_data['volume'][:60].mean() < min_volume:
            continue

        product_price_perc = (
                                product_data['close'][0] - min(product_data['close'])
                             ) / (
                                max(product_data['close']) - min(product_data['close'])
                            )
        price_perc.append(product_price_perc)
        name_list.append(product_data['name'][0].replace('指数', ''))

    result = pd.DataFrame(
        {
            'name': name_list,
            'price_perc': price_perc
        }
    )

    return result.sort_values(by='price_perc', ascending=False).reset_index(drop=True)


def wind_product_index_sigma_xs(
        start_date, end_date,
        db_path=sql_write_path_hb['daily'], table='fut_index_wind', freq=''
):
    engine = create_engine(db_path)
    data_raw = pd.read_sql_query(
        'select `code`, `name`, `t_date`, `close`, `product`, `volume` from ' + table
        + ' where `t_date`<=' + end_date.strftime('%Y%m%d')
        + ' and `t_date`>=' + start_date.strftime('%Y%m%d')
        + ' and `code` like \'%FI.WI\''
        + ' and `product` not in (\'index\') order by `t_date`',
        engine
    )

    calendar = load_calendar_extra(freq=freq, start_date=start_date, end_date=end_date, db_path=db_path)
    result = calendar.copy()

    products = data_raw.drop_duplicates(['product'])['product'].tolist()
    names = []
    for i in products:
        print(i)
        data = data_raw[data_raw['product'] == i].reset_index(drop=True)
        data_clean = calendar.merge(data[['t_date', 'close']], on='t_date')
        data_clean['ret'] = data_clean['close'] / data_clean['close'].shift(1) - 1
        result = result.merge(
            data_clean[['t_date', 'ret']].rename(
                columns={'ret': data['name'][0].replace('指数', '').replace('南华', '')}
            ),
            on='t_date', how='left'
        )
        names.append(data['name'][0].replace('指数', '').replace('南华', ''))
    result['sigma'] = result[names].apply(lambda x: np.std(x, ddof=1), axis=1)
    result['mean'] = result[names].apply(lambda x: np.nanmean(x), axis=1)
    return result


def wind_com_fut_sec_index(
        db_path,
        start_date=datetime(2015, 1, 1).date(),
        end_date=datetime.now().date(),
        table='fut_index_wind',
        decimal=100000000,
        key='amount',
):
    engine = create_engine(db_path)
    data = pd.read_sql_query(
        'select `code`, `name`, `t_date`, `close`, `product`, `volume`, `amount`, `oi_amount` from ' + table
        + ' where `t_date`<=' + end_date.strftime('%Y%m%d')
        + ' and `t_date`>=' + start_date.strftime('%Y%m%d')
        + ' and `code` in ' + str(tuple(wind_sec.keys()))
        + ' and `code`!=\'CCFI.WI\' order by `t_date`',
        engine
    )
    data['code'] = data['code'].apply(lambda x: wind_sec[x])
    df = data.pivot(index='t_date', columns='code', values=key)
    df /= decimal
    df.loc[df.index < datetime(2020, 1, 1).date(), :] = df.loc[df.index < datetime(2020, 1, 1).date(), :] / 2
    return df.reset_index()


def wind_fin_fut_index(
        db_path,
        start_date=datetime(2015, 1, 1).date(),
        end_date=datetime.now().date(),
        table='futures_wind',
        decimal=100000000,
        key='amount',
):
    engine = create_engine(db_path)
    data = pd.read_sql_query(
        'select `code`, `symbol`, `t_date`, `close`, `product`, `volume`, `amount`, `oi_amount` from ' + table
        + ' where `t_date`<=' + end_date.strftime('%Y%m%d')
        + ' and `t_date`>=' + start_date.strftime('%Y%m%d')
        + ' and `product` in (\'IC\', \'IF\', \'IH\', \'T\', \'TF\', \'TS\') order by `t_date`, `product`',
        engine
    )
    data = data[['t_date', 'product', key]].groupby(by=['t_date', 'product']).sum().round(2).reset_index()
    df = data.pivot(index='t_date', columns='product', values=key)
    df /= decimal
    return df.reset_index()


def wind_stk_index_basis(code, start_date, end_date, sql_path, table='futures_wind', annualize=True):
    data_raw = pd.read_sql_query(
        'select * from ' + table
        + ' where `t_date`<=' + end_date.strftime('%Y%m%d')
        + ' and `t_date`>=' + start_date.strftime('%Y%m%d')
        + ' and `product`=\'' + code + '\' order by `t_date`',
        sql_path
    )

    data_00 = data_raw[data_raw['symbol'] == code + '00.CFE'].reset_index(drop=True)
    data_01 = data_raw[data_raw['symbol'] == code + '01.CFE'].reset_index(drop=True)
    data_02 = data_raw[data_raw['symbol'] == code + '02.CFE'].reset_index(drop=True)
    data_03 = data_raw[data_raw['symbol'] == code + '03.CFE'].reset_index(drop=True)

    if annualize:
        data_00['remain'] = (data_00['delist_date'] - data_00['t_date']).map(lambda x: x.days)
        data_00['basis'] = round(-data_00['basis'] / data_00['underlying'] / data_00['remain'] * 365 * 100, 2)
        data_01['remain'] = (data_01['delist_date'] - data_01['t_date']).map(lambda x: x.days)
        data_01['basis'] = round(-data_01['basis'] / data_01['underlying'] / data_01['remain'] * 365 * 100, 2)
        data_02['remain'] = (data_02['delist_date'] - data_02['t_date']).map(lambda x: x.days)
        data_02['basis'] = round(-data_02['basis'] / data_02['underlying'] / data_02['remain'] * 365 * 100, 2)
        data_03['remain'] = (data_03['delist_date'] - data_03['t_date']).map(lambda x: x.days)
        data_03['basis'] = round(-data_03['basis'] / data_03['underlying'] / data_03['remain'] * 365 * 100, 2)

    data_00['basis_chg'] = round(
        -(
                data_00['close'] / data_00['close'].shift(1)
                - data_00['underlying'] / data_00['underlying'].shift(1)
        ) * 100, 2
    )

    data_01['basis_chg'] = round(
        (
                data_01['close'] / data_01['close'].shift(1)
                - data_01['underlying'] / data_01['underlying'].shift(1)
        ) * 100, 2
    )

    data_02['basis_chg'] = round(
        (
                data_02['close'] / data_02['close'].shift(1)
                - data_02['underlying'] / data_02['underlying'].shift(1)
        ) * 100, 2
    )

    data_03['basis_chg'] = round(
        (
                data_03['close'] / data_03['close'].shift(1)
                - data_03['underlying'] / data_03['underlying'].shift(1)
        ) * 100, 2
    )

    return data_00, data_01, data_02, data_03


def fin_fut_daily_k_by_contracts(contract_list, start_date=None, end_date=None, page_size=None):
    if start_date is None:
        start_date = datetime(2010, 1, 1).date()
    if end_date is None:
        end_date = datetime.now().date()
    if page_size is None:
        page_size = page_size_con

    if len(contract_list) == 0:
        raise ValueError('code_list 未传入参数')
    elif len(contract_list) > 1:
        sql_contract = 'ContractInnerCode in ' + str(tuple(contract_list))
    elif len(contract_list) > 999:
        raise ValueError('code_list 参数过多')
    else:
        sql_contract = 'ContractInnerCode=' + str(contract_list[0])

    sql = 'select ' + ', '.join(properties_fin_k) + ' from ' + db_tables['hsjy_fin_daily_quote'] \
          + ' where ' + sql_contract + ' and TradingDay<=TRUNC(to_date(' + end_date.strftime('%Y%m%d') \
          + ', \'yyyymmdd\')) and TradingDay>=TRUNC(to_date(' + start_date.strftime('%Y%m%d') \
          + ', \'yyyymmdd\')) order by TradingDay, ContractInnerCode'

    data = hbs.db_data_query(db=db, sql=sql, page_size=page_size)
    if data['pages'] > 1:
        for p in range(2, data['pages'] + 1):
            data['data'] = data['data'] + hbs.db_data_query(db=db, sql=sql, page_size=page_size, page_num=p)['data']

    return data


def daily_ret_by_vol(start_date=None, end_date=None, ex_list=None, min_vol=10000, page_size=None):
    if ex_list is None:
        ex_list = [
            HSJY_EXCHANGE_SHFE,
            HSJY_EXCHANGE_DCE,
            HSJY_EXCHANGE_CZCE,
            HSJY_EXCHANGE_INE
        ]
    if start_date is None:
        start_date = datetime(2010, 1, 1).date()
    if end_date is None:
        end_date = datetime.now().date()
    if page_size is None:
        page_size = page_size_con

    if len(ex_list) == 0:
        raise ValueError('code_list 未传入参数')
    elif len(ex_list) > 1:
        sql_contract = 'EXCHANGE in ' + str(tuple(ex_list))
    elif len(ex_list) > 999:
        raise ValueError('code_list 参数过多')
    else:
        sql_contract = 'EXCHANGE=' + str(ex_list[0])

    sql = 'select ' + ', '.join(properties_com_k) + ' from ' + db_tables['hsjy_com_daily_quote'] \
          + ' where ' + sql_contract + ' and ENDDATE<=TRUNC(to_date(' + end_date.strftime('%Y%m%d') \
          + ', \'yyyymmdd\')) and ENDDATE>=TRUNC(to_date(' + start_date.strftime('%Y%m%d') \
          + ', \'yyyymmdd\')) and VOLUME>=' + str(min_vol) + ' order by ENDDATE, OPTIONCODE'
    data = hbs.db_data_query(db=db, sql=sql, page_size=page_size)
    if data['pages'] > 1:
        for p in range(2, data['pages'] + 1):
            data['data'] = data['data'] + hbs.db_data_query(db=db, sql=sql, page_size=page_size, page_num=p)['data']

    return data


def fut_com_amount_by_ex(start_date=None, end_date=None, page_size=None):

    ex_list = [
        HSJY_EXCHANGE_SHFE,
        HSJY_EXCHANGE_DCE,
        HSJY_EXCHANGE_CZCE,
        HSJY_EXCHANGE_INE
    ]
    if start_date is None:
        start_date = datetime(2010, 1, 1).date()
    if end_date is None:
        end_date = datetime.now().date()
    if page_size is None:
        page_size = page_size_con

    sql_e = 'EXCHANGE in ' + str(tuple(ex_list))

    sql = 'select ENDDATE, SUM(TURNOVER) from ' + db_tables['hsjy_com_daily_quote'] \
          + ' where ENDDATE<=TRUNC(to_date(' + end_date.strftime('%Y%m%d') \
          + ', \'yyyymmdd\')) and ENDDATE>=TRUNC(to_date(' + start_date.strftime('%Y%m%d') \
          + ', \'yyyymmdd\')) and ' + sql_e + ' group by ENDDATE order by ENDDATE'
    data = hbs.db_data_query(db=db, sql=sql, page_size=page_size)
    if data['pages'] > 1:
        for p in range(2, data['pages'] + 1):
            data['data'] = data['data'] + hbs.db_data_query(db=db, sql=sql, page_size=page_size, page_num=p)['data']

    return data


def rolling_volatility(data, vol_params=None):
    if vol_params is None:
        vol_params = [
            '20日', '30日', '60日', '90日', '120日', '150日', '200日'
        ]

    vol_max = []
    vol_75 = []
    vol_50 = []
    vol_25 = []
    vol_min = []
    vol_current = []

    for i in vol_params:
        data[i] = data['ret'].rolling(int(re.findall(r'\d+', i)[0])).std(ddof=1) * np.sqrt(250) * 100
        vol_max.append(np.nanmax(data[str(i)]))
        vol_75.append(np.nanpercentile(data[str(i)], 75))
        vol_50.append(np.nanpercentile(data[str(i)], 50))
        vol_25.append(np.nanpercentile(data[str(i)], 25))
        vol_min.append(np.nanmin(data[str(i)]))
        vol_current.append(data[str(i)].tolist()[-1])

    vol_data = pd.DataFrame(
        {
            '时间': vol_params,
            '最大值': vol_max,
            '75分位': vol_75,
            '中位值': vol_50,
            '25分位': vol_25,
            '最小值': vol_min,
            '最新值': vol_current
        }
    )
    return vol_data, data


