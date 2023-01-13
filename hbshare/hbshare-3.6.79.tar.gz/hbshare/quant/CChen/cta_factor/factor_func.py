#!/usr/bin/python
# coding:utf-8
from hbshare.quant.CChen.func import generate_table
from hbshare.quant.CChen.cta_factor.const import composite_factor
from hbshare.quant.CChen.stk import trade_calendar
import pandas as pd
import numpy as np
import pymysql
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from pandas.plotting import register_matplotlib_converters
from datetime import datetime, timedelta

register_matplotlib_converters()
plt.rcParams['font.sans-serif'] = ['SimHei']

sql_l = '''(
    `ID` bigint not null AUTO_INCREMENT,
    `TDATE`  date not null,
    `EXCHANGE`  int,
    `PCODE`  int,
    `UCODE`  int,
    `CLOSE0`  float,
    `CLOSE` float,
    `CLOSE1` float,
    `POS` int,
    `WEIGHT`  double,
    `RETURN` double,
    `FACTORVALUE` double,
    `FACTOR`  varchar(255),
    primary key (`ID`)
    )
    '''

sql_index = '''(
    `ID` bigint not null AUTO_INCREMENT,
    `TDATE`  date not null,
    `CLOSE` float,
    `TURNOVER` float,
    `FACTOR`  varchar(255),
    primary key (`ID`)
    )
    '''

stock_info_file = 'E:\\codes\\hbshare\\hbshare\\quant\\CChen\\data\\wind_edb.csv'


def factor_table_gen(table, sql_info):

    generate_table(
        database='daily_data',
        table=table,
        generate_sql=sql_l,
        sql_ip=sql_info['ip'],
        sql_user=sql_info['user'],
        sql_pass=sql_info['pass'],
        table_comment='CTA factor based on hsjy data'
    )
    print(table + ' generated')


def index_table_gen(table, sql_info):

    generate_table(
        database='daily_data',
        table=table,
        generate_sql=sql_index,
        sql_ip=sql_info['ip'],
        sql_user=sql_info['user'],
        sql_pass=sql_info['pass'],
        table_comment='CTA INDEX'
    )
    print(table + ' generated')


def index_gen_in_loop(data, factor, index0, table, path):
    data['RETURN'] = data['RETURN'] * data['WEIGHT'] * data['POS']
    data_g = data.groupby(by='TDATE').sum()[['RETURN']].reset_index()
    data_g['ret'] = data_g['RETURN'] / 10000 + 1.0
    data['WEIGHT'] = data['WEIGHT'] * data['POS']
    w = data.pivot(index='TDATE', columns='UCODE', values='WEIGHT')
    data_turnover = pd.DataFrame(
        (w.shift(1) - w).abs().sum(axis=1)
    ).rename(columns={0: 'TURNOVER'}).reset_index()
    data_g = data_g.merge(data_turnover, on='TDATE', how='left')
    data_g = data_g.iloc[1:]
    data_g['CLOSE'] = data_g['ret'].cumprod()
    data_g['CLOSE'] = data_g['CLOSE'] * index0
    data_g['FACTOR'] = factor
    data_g[['TDATE', 'CLOSE', 'FACTOR', 'TURNOVER']].to_sql(table, path, if_exists='append', index=False)
    print('\t' + str(len(data_g)) + ', to sql, ' + data_g['TDATE'].tolist()[len(data_g) - 1].strftime('%Y-%m-%d'))


def index_gen(sql_path, sql_info, table_factor='cta_factor', table_index='cta_index'):
    index_table_gen(table=table_index, sql_info=sql_info)
    end_date_all = pd.read_sql_query(
        'select distinct TDATE from ' + table_factor + ' order by TDATE desc limit 1', sql_path
    )
    factors = pd.read_sql_query('select distinct FACTOR from ' + table_factor, sql_path)
    if len(factors) == 0:
        print('No factor return')
        return
    else:
        for i in range(len(factors['FACTOR'])):
            # factor = 'xswr_d1_q75'
            factor = factors['FACTOR'][i]
            last_factor_index = pd.read_sql_query(
                'select * from ' + table_index
                + ' where TDATE<=' + end_date_all['TDATE'][0].strftime('%Y%m%d')
                + ' and FACTOR=\'' + factor
                + '\' order by TDATE desc limit 1',
                sql_path
            )
            if len(last_factor_index) == 0:
                date0 = datetime(1990, 1, 1).date()
                index0 = 1000
            else:
                date0 = last_factor_index['TDATE'][0]
                index0 = last_factor_index['CLOSE'][0]

            print(
                str(i + 1) + '/' + str(len(factors['FACTOR'])) + ', '
                + factor + ', start date: ' + date0.strftime('%Y-%m-%d')
            )

            if date0 == end_date_all['TDATE'][0]:
                print('\tNo new date, ' + date0.strftime('%Y-%m-%d'))
                continue

            factor_data = pd.read_sql_query(
                'select * from ' + table_factor + ' where TDATE>=' + date0.strftime('%Y%m%d')
                + ' and FACTOR=\'' + factor + '\' order by TDATE',
                sql_path
            )
            if len(factor_data) > 0:
                index_gen_in_loop(data=factor_data, factor=factor, index0=index0, table=table_index, path=sql_path)
            else:
                print('\tNo new data')


def index_compose(sql_path, sql_info, table_factor='cta_factor', table_index='cta_index', factors=composite_factor):
    index_table_gen(table=table_index, sql_info=sql_info)
    end_date_all = pd.read_sql_query(
        'select distinct TDATE from ' + table_factor + ' order by TDATE desc limit 1', sql_path
    )
    for i in factors:
        last_factor_index = pd.read_sql_query(
            'select * from ' + table_index
            + ' where  FACTOR=\'' + i + '\' order by TDATE desc limit 1',
            sql_path
        )
        if len(last_factor_index) == 0:
            date0 = datetime(1990, 1, 1).date()
            index0 = 1000
        else:
            date0 = last_factor_index['TDATE'][0]
            index0 = last_factor_index['CLOSE'][0]

        print(
            i + ', start date: ' + date0.strftime('%Y-%m-%d')
        )

        if date0 == end_date_all['TDATE'][0]:
            print('\tNo new date, ' + date0.strftime('%Y-%m-%d'))
            continue

        base_factor_data = pd.read_sql_query(
            'select * from ' + table_factor + ' where TDATE>=' + date0.strftime('%Y%m%d')
            + ' and FACTOR in ' + str(tuple(factors[i])) + ' order by TDATE',
            sql_path
        )
        base_factor_data['WEIGHT'] = base_factor_data['POS'] * base_factor_data['WEIGHT']
        base_factor_data['POS'] = 1

        b_w = base_factor_data.groupby(by=['TDATE', 'UCODE'], as_index=False).mean()[['TDATE', 'UCODE', 'WEIGHT']]
        b_info = base_factor_data.drop_duplicates(subset=['TDATE', 'UCODE'])
        b_data = b_info.drop(columns=['WEIGHT']).merge(b_w, on=['TDATE', 'UCODE'], how='left')
        if len(base_factor_data) > 0:
            index_gen_in_loop(data=b_data, factor=i, index0=index0, table=table_index, path=sql_path)
        else:
            print('\tNo new data')


def get_last_position(table, before_date, factor, sql_path):
    existing_cal = pd.read_sql_query(
        'select distinct `TDATE` from ' + table + ' where `TDATE`<=' + before_date.strftime('%Y%m%d')
        + ' and `FACTOR`=\'' + factor + '\' order by `TDATE` desc limit 1',
        sql_path
    )
    if len(existing_cal) >= 1:
        pos = pd.read_sql_query(
            'select * from ' + table + ' where `TDATE`=' + existing_cal['TDATE'][0].strftime('%Y%m%d')
            + ' and `FACTOR`=\'' + factor + '\'',
            sql_path
        )
        print(factor + ', load last date: ' + existing_cal['TDATE'][0].strftime('%Y-%m-%d'))
        return pos

    else:
        print(factor + ', load last date: None')
        return None


def load_factor(sql_path, factor_name, table='cta_factor'):
    index = factor_name

    data = pd.read_sql_query(
        'select * from ' + table + ' where FACTOR=\'' + index + '\'',
        sql_path
    )
    return data


def factor_summary(data, trade_days=250, show=False):
    data['RETURN'] = data['RETURN'] * data['WEIGHT'] * data['POS']
    data['WEIGHT'] = data['WEIGHT'] * data['POS']
    factor_w = data.pivot(index='TDATE', columns='UCODE', values='WEIGHT').fillna(0)
    factor_data_turnover = pd.DataFrame(
        (factor_w.shift(1) - factor_w).abs().sum(axis=1)
    ).rename(columns={0: 'TURNOVER'}).reset_index()
    factor_data_turnover.loc[0, 'TURNOVER'] = factor_w.abs().sum(axis=1)[0]

    data_g = data.groupby(by='TDATE').sum()[['RETURN']].reset_index()
    data_g = data_g.merge(factor_data_turnover, on='TDATE', how='left')
    # data_g = data.groupby(by='TDATE').mean()[['RETURN']].reset_index()
    data_g['ret'] = data_g['RETURN'] / 10000
    annualized_return_average = (data_g['ret'].mean() + 1) ** trade_days - 1
    data_g['ind'] = (data_g['ret'] + 1).cumprod()
    data_g['max_ind'] = data_g['ind'].cummax()
    cumulative_return = data_g['ind'][len(data_g) - 1] / data_g['ind'][0] - 1.0
    annualized_return = (cumulative_return + 1.0) ** (
            365 / (data_g['TDATE'][len(data_g) - 1] - data_g['TDATE'][0]).days
    ) - 1
    return_sample = (data_g['ind'] / data_g['ind'].shift(1) - 1)[1:]
    sigma = return_sample.std(ddof=1) * np.sqrt(trade_days)

    data_g['dd'] = (data_g['ind'] - data_g['max_ind']) / data_g['max_ind']
    data_g['year'] = data_g['TDATE'].apply(lambda x: x.year)

    range_dates = [data_g['TDATE'][0]]

    year_slice = data_g.drop_duplicates(subset=['year'], keep='last')

    if len(year_slice) > 0:
        range_dates += year_slice['TDATE'].tolist()

    result = {
        '累计收益': cumulative_return,
        '最大回撤': min(data_g['dd'][1:]),
        '年化收益率（头尾）': annualized_return,
        '年化收益率（平均）': annualized_return_average,
        '波动率': sigma,
        '换手率': data_g['TURNOVER'].mean()
    }

    if show:
        print(
            '累计收益： \n\t%.2f%%' % round(cumulative_return * 100, 2)
        )
        print(
            '最大回撤：      \n\t%.2f%%' % round(min(data_g['dd'][1:]) * 100, 2)
        )
        print(
            '年化收益率（头尾）： \n\t%.2f%%' % round(annualized_return * 100, 2)
        )
        print(
            '年化收益率（平均）： \n\t%.2f%%' % round(annualized_return_average * 100, 2)
        )
        print(
            '波动率： \n\t%.2f%%' % round(sigma * 100, 2)
        )
        print(
            '换手率： \n\t%.2f%%' % round(data_g['TURNOVER'].mean(), 2)
        )
        print(
            '收益波动比： \n\t%.2f' % round(annualized_return_average / sigma, 2)
        )
        if min(data_g['dd'][1:]) != 0:
            print(
                '收益回撤比：        \n\t%.2f' % round(-annualized_return_average / min(data_g['dd'][1:]), 2)
            )
        else:
            print(
                '收益回撤比：       \n\tinf'
            )

        print('')
        for i in range(1, len(range_dates)):
            range_return = (
                                   data_g[data_g['TDATE'] == range_dates[i]]['ind'].tolist()[0]
                                   / data_g[data_g['TDATE'] == range_dates[i - 1]]['ind'].tolist()[0]
                           ) - 1
            result[range_dates[i - 1].strftime('%Y/%m/%d') + ' - ' + range_dates[i].strftime('%Y/%m/%d')] = range_return
            print(
                range_dates[i - 1].strftime('%Y/%m/%d') + ' - ' + range_dates[i].strftime('%Y/%m/%d')
                + ':\t收益：%.2f%%' % round(range_return * 100, 2)
            )
    return data_g, result


def factor_plot(data, plot_title, cost=0.0001, size=(10, 6)):
    def to_percent(temp, position):
        return '%.2f' % (100 * temp) + '%'

    fig = plt.figure(figsize=size)
    ax1 = fig.add_subplot(2, 1, 1)

    ax1.plot(data['TDATE'], data['ind'])
    ax2 = ax1.twinx()
    ax2.fill_between(data['TDATE'], data['dd'], color='gray', alpha=0.3)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.title(plot_title)

    ax3 = fig.add_subplot(2, 1, 2)
    ax3.plot(data['TDATE'], data['ind'])
    ax3.plot(data['TDATE'], ((data['RETURN'] / 10000 - data['TURNOVER'] / 100 * cost) + 1).cumprod())
    ax3.plot(data['TDATE'], ((data['RETURN'] / 10000 - data['TURNOVER'] / 100 * cost * 2) + 1).cumprod())
    ax3.plot(data['TDATE'], ((data['RETURN'] / 10000 - data['TURNOVER'] / 100 * cost * 3) + 1).cumprod())
    ax3.plot(data['TDATE'], ((data['RETURN'] / 10000 - data['TURNOVER'] / 100 * cost * 5) + 1).cumprod())
    plt.legend(['原始', '1倍交易成本', '2倍交易成本', '3倍交易成本', '5倍交易成本'])

    ax4 = ax3.twinx()
    ax4.bar(data['TDATE'], data['TURNOVER'] / 100, color='r', alpha=0.3)
    plt.gca().yaxis.set_major_formatter(FuncFormatter(to_percent))

    plt.show()


def factor_compute(
        window_days_list,
        to_sql_path,
        sql_info,
        start_date=datetime(2010, 1, 1).date(),
        end_date=datetime.now(),
        to_table='cta_factor',
        data=None,
        factor_func=None,
        **kwargs
):
    if 'min_volume' in kwargs:
        min_volume = kwargs['min_volume']
    else:
        min_volume = 10000

    factor_table_gen(table=to_table, sql_info=sql_info)

    def get_existing_date():
        exist_index = get_last_position(
            table=to_table,
            before_date=end_date,
            factor=index_name,
            sql_path=to_sql_path
        )
        if exist_index is not None:
            date0 = exist_index['TDATE'][0]
        else:
            date0 = start_date
        return date0

    for window_days in window_days_list:
        if 'hedge_ratio_list' in kwargs:
            for quantile in kwargs['hedge_ratio_list']:
                if 'name' in kwargs:
                    index_name = 'xs' + kwargs['name'] + '_d' + str(window_days) + '_q' + str(quantile)
                else:
                    index_name = factor_func.__name__ + '_d' + str(window_days) + '_q' + str(quantile)
                start_date0 = get_existing_date()
                if data['TDATE'].sort_values().tolist()[-1] == start_date0:
                    print('\t' + index_name + ', no new data. ' + str(datetime.now()))
                    continue
                data_s = data[data['TDATE'] >= start_date0 - timedelta(days=max(window_days, kwargs['liq_days']) * 2)]
                pos = factor_func(
                    start_date=start_date0,
                    data=data_s,
                    ts_n=window_days,
                    quantile=quantile,
                    min_volume=min_volume,
                    **kwargs
                )
                if pos is not None:
                    pos.to_sql(to_table, to_sql_path, if_exists='append', index=False)
                    print(
                        '\t' + index_name + ' to sql, ' + pos['TDATE'].sort_values().tolist()[-1].strftime('%Y-%m-%d')
                        + '. ' + str(datetime.now())
                    )
                else:
                    print('\t' + index_name + ', no new data. ' + str(datetime.now()))

        else:
            if 'name' in kwargs:
                index_name = 'ts' + kwargs['name'] + '_d' + str(window_days)
            else:
                index_name = factor_func.__name__ + '_d' + str(window_days)
            start_date0 = get_existing_date()
            if data['TDATE'].sort_values().tolist()[-1] == start_date0:
                print('\t' + index_name + ', no new data. ' + str(datetime.now()))
                continue
            data_s = data[data['TDATE'] >= start_date0 - timedelta(days=max(window_days, kwargs['liq_days']) * 2)]
            pos = factor_func(
                start_date=start_date0,
                data=data_s,
                ts_n=window_days,
                min_volume=min_volume,
                **kwargs
            )
            if pos is not None:
                pos.to_sql(to_table, to_sql_path, if_exists='append', index=False)
                print(
                    '\t' + index_name + ' to sql, ' + pos['TDATE'].tolist()[-1].strftime('%Y-%m-%d')
                    + '. ' + str(datetime.now())
                )
            else:
                print('\t' + index_name + ', no new data. ' + str(datetime.now()))


def get_stock_data(
        data_indicator, path, products=None, table='wind_edb', table_p='hsjy_fut_info_p', info_file=None, date_lag=0
):
    stock_data_code = []
    for i in data_indicator:
        if products is not None:
            if i not in products:
                continue
        stock_data_code += data_indicator[i]

    stock_data_raw = pd.read_sql_query(
        'select * from ' + table + ' where code in ' + str(tuple(stock_data_code)).replace(',)', ')'),
        path
    ).pivot(index='t_date', columns='code', values='close').ffill()
    if date_lag > 0:
        stock_data_raw['t_date'] = pd.Series(stock_data_raw.index).shift(-date_lag).values
        stock_data_raw = stock_data_raw.set_index('t_date')
        stock_data_raw = stock_data_raw.iloc[:-date_lag]
    if info_file is None:
        stock_data_info = pd.read_csv(stock_info_file)
    else:
        stock_data_info = pd.read_csv(info_file)

    for i in stock_data_raw.columns:
        stock_data_raw.loc[:, i] = (
                stock_data_raw.loc[:, i] * stock_data_info[stock_data_info['指标ID'] == i]['乘数'].tolist()[0]
        )
    tdate_list = trade_calendar(
        start_date=stock_data_raw.index[0],
        end_date=stock_data_raw.index[len(stock_data_raw) - 1]
    )

    stock_data = pd.DataFrame(
        {
            't_date': tdate_list
        }, index=range(len(tdate_list))
    ).merge(stock_data_raw, on='t_date', how='left').rename(columns={'t_date': 'TDATE'}).set_index('TDATE')

    hsjy_p_info = pd.read_sql_query(
        'select * from ' + table_p, path
    )

    data_stock = pd.DataFrame()
    for i in data_indicator:
        if products is not None:
            if i not in products:
                continue
        data_p = pd.DataFrame(stock_data[data_indicator[i]].dropna(axis=0, how='all').sum(axis=1)).rename(
            columns={0: 'WRQCURRENT'}
        )

        p_info = hsjy_p_info[hsjy_p_info['CODE'] == i]

        data_p['EXCHANGE'] = p_info['EXCHANGE'].tolist()[0]
        data_p['PCODE'] = p_info['PCODE'].tolist()[0]
        data_p['PNAME'] = p_info['PNAME'].tolist()[0]
        data_stock = data_stock.append(data_p.reset_index())
    return data_stock.reset_index(drop=True)


def get_mr_data(start_date, end_date, path, table='hsjy_fut_memberrank', ts_n=365):
    data_mr = pd.read_sql_query(
        'select TDATE, CCODE, INDICATORCODE, MCODE , INDICATORVOL, INDICATORCHG from ' + table
        + ' where TDATE<=' + end_date.strftime('%Y%m%d')
        + ' and TDATE>=' + (start_date - timedelta(days=ts_n)).strftime('%Y%m%d')
        + ' and INDICATORCODE in (3, 4) order by TDATE, CCODE, INDICATORCODE',
        path
    ).drop_duplicates(subset=['TDATE', 'CCODE', 'INDICATORCODE', 'MCODE'])
    data_mr = data_mr.groupby(by=['TDATE', 'CCODE', 'INDICATORCODE'], as_index=False).sum().rename(
        columns={
            'INDICATORCODE': 'SIDE',
            'INDICATORVOL': 'MR',
            'INDICATORCHG': 'MRCHG'
        }
    ).reset_index(drop=True)
    date_2020 = data_mr.index[data_mr['TDATE'] < datetime(2020, 1, 1).date()]
    data_mr.loc[date_2020, ['MR', 'MRCHG']] = data_mr.loc[date_2020, ['MR', 'MRCHG']] / 2
    return data_mr

# if __name__ == '__main__':
#     index_gen()
