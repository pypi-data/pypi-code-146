from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from hbshare.quant.CChen.cta_factor.factor_func import factor_compute, get_stock_data, get_mr_data
from hbshare.quant.CChen.stk import trade_calendar
from hbshare.quant.CChen.cta_factor.const import stock_data_indicator
from hbshare.quant.CChen.cta_factor.factor_algo import (
    tscarry, carry, tsmom, tsrev, xsmom, xsrev, tswr, xswr, mr, mrchg, tsmr,
    tsbasismom, xsbasismom, tspoichg, xspoichg, xssigma,
    xsmr, xstsmr, xsmrchg, tspvolchg, xspvolchg, tsskew, xsskew, xsmr2, xsmrchg2
    # tsstock, xsstock
)


def run(sql_path, sql_info):
    start_date = datetime(2010, 1, 1).date()
    # end_date = datetime(2021, 4, 9).date()
    end_date = datetime.now().date()

    window_days_list = [1, 2, 3, 5, 10, 20, 30, 40, 50, 60, 90, 100, 150, 200, 250]
    liq_d = 20

    table = 'hsjy_fut_com_index'
    table_wr = 'hsjy_fut_wr'
    table_mr = 'hsjy_fut_memberrank'
    table_contracts_info = 'hsjy_fut_info_c'
    table_p_info = 'hsjy_fut_info_p'
    table_raw = 'hsjy_fut_com'

    data = pd.read_sql_query(
        'select * from ' + table + ' where TDATE<='
        + end_date.strftime('%Y%m%d')
        + ' and TDATE>=' + (start_date - timedelta(days=500)).strftime('%Y%m%d')
        + ' order by TDATE',
        sql_path
    )
    col_adj = ['VOL', 'AMT', 'OI', 'PVOL', 'POI', 'PAMT']
    date_2020 = data.index[data['TDATE'] < datetime(2020, 1, 1).date()]
    data.loc[date_2020, col_adj] = data.loc[date_2020, col_adj] / 2
    data_wr0 = pd.read_sql_query(
        'select TDATE, EXCHANGE, PCODE, PNAME, WRQCURRENT from ' + table_wr + ' where TDATE<='
        + end_date.strftime('%Y%m%d')
        + ' and TDATE>=' + (start_date - timedelta(days=500)).strftime('%Y%m%d')
        + ' and FREQ=5 order by TDATE, EXCHANGE, PCODE',
        sql_path
    ).drop_duplicates(subset=['TDATE', 'EXCHANGE', 'PCODE']).reset_index(drop=True)
    calendar = data[['TDATE']].sort_values(by='TDATE').drop_duplicates().reset_index(drop=True)
    data_wr = pd.DataFrame()
    for e in data['EXCHANGE'].drop_duplicates().tolist():
        PCODEs = data[data['EXCHANGE'] == e]['PCODE'].drop_duplicates().tolist()
        for p in PCODEs:
            data_wr_p = data_wr0[np.array(data_wr0['EXCHANGE'] == e) & np.array(data_wr0['PCODE'] == p)]
            data_wr_p = pd.merge(calendar, data_wr_p, on='TDATE', how='left').fillna(method='ffill')
            data_wr_p = data_wr_p[data_wr_p['WRQCURRENT'] >= 0].reset_index(drop=True)
            data_wr = pd.concat([data_wr, data_wr_p])
    data_wr = data_wr.reset_index(drop=True).rename(columns={'WRQCURRENT': 'x'})

    data_mr = get_mr_data(start_date=start_date, end_date=end_date, path=sql_path, table=table_mr)
    # data_mr = data_mr[data_mr['SIDE'] != 1]
    data_mr['SIDE'] = data_mr['SIDE'].apply(lambda x: 1 if x == 3 else (-1 if x == 4 else 0))
    data_mr['MR'] = data_mr['MR'] * data_mr['SIDE']
    data_mr['MRCHG'] = data_mr['MRCHG'] * data_mr['SIDE']
    data_info = pd.read_sql_query(
        'select * from ' + table_contracts_info, sql_path
    )
    data_mr = pd.merge(data_mr, data_info[['CCODE', 'EXCHANGE', 'PCODE']], on='CCODE', how='left')
    data_mr = data_mr.groupby(by=['TDATE', 'SIDE', 'EXCHANGE', 'PCODE']).sum().reset_index()

    data_contracts = pd.read_sql_query(
        'select * from ' + table_raw + ' where CCODE in ' + str(tuple(np.unique(data[['CCODE', 'CCODE2']].dropna())))
        + ' order by CCODE, TDATE',
        sql_path
    ).drop_duplicates(subset=['TDATE', 'CCODE'])

    # 库存数据
    data_stock = get_stock_data(
        data_indicator=stock_data_indicator, path=sql_path, table_p=table_p_info
    ).rename(columns={'WRQCURRENT': 'x'})

    factor_compute(
        window_days_list=[10, 20, 30, 50, 90, 150, 250],
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xssigma,
        liq_days=liq_d,
        data_raw=data_contracts,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list[:10],
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xsbasismom,
        liq_days=liq_d,
        data_raw=data_contracts,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list[:10],
        data=data,
        factor_func=tsbasismom,
        liq_days=liq_d,
        data_raw=data_contracts,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=[20, 50],
        hedge_ratio_list=[50, 60, 70, 80, 90],
        data=data,
        factor_func=carry,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        factor_func=tsmom,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        factor_func=tscarry,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list[2:],
        data=data, factor_func=tsskew,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        factor_func=tsrev,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xsmom,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list[2:],
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xsskew,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xsrev,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        factor_func=tspoichg,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        factor_func=tspvolchg,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xspoichg,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        factor_func=xspvolchg,
        liq_days=liq_d,
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        data_wr=data_wr,
        factor_func=xswr,
        liq_days=liq_d,
        price='OPEN',
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        data_wr=data_wr,
        factor_func=tswr,
        liq_days=liq_d,
        price='OPEN',
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        data_wr=data_stock,
        factor_func=xswr,
        liq_days=liq_d,
        price='OPEN',
        sql_info=sql_info,
        to_sql_path=sql_path,
        name='stock',
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        data_wr=data_stock,
        factor_func=tswr,
        liq_days=liq_d,
        price='OPEN',
        sql_info=sql_info,
        to_sql_path=sql_path,
        name='stock',
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        data_mr=data_mr,
        factor_func=mr,
        liq_days=liq_d,
        price='OPEN',
        sql_info=sql_info, to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        data_mr=data_mr,
        factor_func=xsmr,
        liq_days=liq_d,
        price='OPEN',
        sql_info=sql_info, to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        data_mr=data_mr,
        factor_func=xsmr2,
        liq_days=liq_d,
        price='OPEN',
        sql_info=sql_info, to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        data_mr=data_mr,
        factor_func=mrchg,
        liq_days=liq_d,
        price='OPEN',
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        data_mr=data_mr,
        factor_func=xsmrchg,
        liq_days=liq_d,
        price='OPEN',
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        data_mr=data_mr,
        factor_func=xsmrchg2,
        liq_days=liq_d,
        price='OPEN',
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        data=data,
        data_mr=data_mr,
        factor_func=tsmr,
        liq_days=liq_d,
        price='OPEN',
        sql_info=sql_info,
        to_sql_path=sql_path
    )

    factor_compute(
        window_days_list=window_days_list,
        hedge_ratio_list=[50, 75],
        data=data,
        data_mr=data_mr,
        factor_func=xstsmr,
        liq_days=liq_d,
        price='OPEN',
        sql_info=sql_info, to_sql_path=sql_path
    )


if __name__ == '__main__':
    from hbshare.quant.CChen.db_const import sql_write_path_work, sql_user_work
    run(
        sql_path=sql_write_path_work['daily'],
        sql_info=sql_user_work
    )

