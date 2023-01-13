#!/usr/bin/python
# coding:utf-8
import pandas as pd
import numpy as np
import pymysql
import re
from datetime import datetime
from hbshare.quant.CChen.stk import trade_calendar, load_index
from hbshare.quant.CChen.cons import fut_sectors

pymysql.install_as_MySQLdb()


# 读取交易日日历
def load_calendar(start_date=None, end_date=None, freq=''):
    r"""
    交易日的日期戳(周度或月度)
    此功能只在好买内部网络环境下有效

    Parameters
    ----------
    start_date : datetime.date
        起始日期
    end_date : datetime.date
        结束日期
    freq : str
        日期频率
    """

    if start_date is None:
        start_date = datetime(2010, 1, 1).date()

    if end_date is None:
        end_date = datetime.now().date()

    trade_cal = trade_calendar(
        start_date=start_date,
        end_date=end_date
    )
    trade_cal = pd.DataFrame(
        {
            't_date': trade_cal
        }, index=range(len(trade_cal))
    )
    if freq.lower() in ['w', 'week', 'fund_stats']:
        trade_cal = trade_cal.set_index(pd.to_datetime(trade_cal['t_date'])).resample('W').max().reset_index(drop=True)
    elif freq.lower() in ['m', 'month', 'monthly']:
        trade_cal = trade_cal.set_index(pd.to_datetime(trade_cal['t_date'])).resample('M').max().reset_index(drop=True)
    return trade_cal[trade_cal['t_date'] >= start_date].reset_index(drop=True)


def load_calendar_extra(start_date=None, end_date=None, freq=''):
    r"""
    交易日的日期戳(周度或月度)
    如果当月未结束会以当月最后一个交易日当作当月的最后一个值
    此功能只在好买内部网络环境下有效
    """
    if start_date is None:
        start_date = datetime(2010, 1, 1).date()

    if end_date is None:
        end_date = datetime.now().date()

    if freq.lower() in ['w', 'week', 'fund_stats']:
        cal_spe = load_calendar(start_date=start_date, end_date=end_date, freq=freq)
    elif freq.lower() in ['month', 'monthly']:
        cal_spe = load_calendar(start_date=start_date, end_date=end_date, freq=freq)
        cal_week = load_calendar(start_date=start_date, end_date=end_date, freq='w')
        cal_extra = cal_week[cal_week['t_date'] > cal_spe['t_date'][len(cal_spe) - 1]].reset_index(drop=True)
        if len(cal_extra) > 0:
            cal_spe = cal_spe.append(cal_extra.loc[len(cal_extra) - 1]).reset_index(drop=True)
    else:
        cal_spe = load_calendar(start_date=start_date, end_date=end_date)
    return cal_spe


def load_funds_data(
        fund_list,
        first_date=None,
        end_date=None,
        freq='w',
        fillna=True,
        all_aligned=False,
        db_path='',
        # cal_db_path='',
        print_info=False,
        drop_1=False,
):
    r"""
    读取基金数据，同时对齐时间戳
    需要自行建立对应格式的数据库以及存入对应数据！

    Parameters
    ----------
    fund_list : DataFrame
        包含基金代码的dataframe，dataframe需包含code列作为读取对象
    first_date : datetime.date
        基金数据开始时间戳
        设置的太早会自动剔除前期空值
        如：first_date设置为1990/1/1，基金数据从2010/1/1开始，则返回的数据从2010/1/1开始
    end_date : datetime.date
        基金数据结束时间戳
    freq : str
        数据频率，日度：''，周度：['w', 'week', 'weekly']，月度：['m', 'month', 'monthly']
    fillna : bool
        缺失值是否前值填充
    all_aligned : bool
        读取月度数据时用
        True：使用每个月最后一个周五的净值作为月末净值
        False：使用每个月最后一个交易日净值最为月末净值（前提为基金必须披露当月最后一个交易日净值）
    db_path : str
        基金数据库地址
    cal_db_path : str
        交易日历数据库地址，好买内网环境下此项可不填
    print_info : bool
        读取数据时是否输出信息
    drop_1 : bool
        是否剔除基金运作前期长期为1的净值

    """
    if first_date is None:
        first_date = datetime.now().date()

    if end_date is None:
        end_date = datetime.now().date()

    cal = load_calendar(end_date=end_date)
    cal_weekly = load_calendar_extra(freq='w', end_date=end_date)

    cal_spe = load_calendar_extra(freq=freq, end_date=end_date)
    cal_all = cal_spe.copy()
    i_dates = []
    if len(fund_list) == 1:
        sql_l = 'code=\'' + fund_list['code'][0] + '\''
    else:
        sql_l = 'code in ' + str(tuple(fund_list['code']))

    fund_data_all = pd.read_sql_query(
        'select * from fund_data where ' + sql_l + ' and t_date<=' + end_date.strftime('%Y%m%d')
        + ' order by t_date',
        db_path
    )[['t_date', 'nav', 'code']]
    fund_data_all['code'] = fund_data_all['code'].apply(lambda x: x.lower())

    for i in range(len(fund_list)):
        fund_code = fund_list['code'][i].lower()
        fund_name = fund_list['name'][i]
        if print_info:
            print('Loading ' + fund_name + ' ' + freq + '；')
        # if first_date > fund_list['first_date'][i]:
        #     first_date = fund_list['first_date'][i]

        fund_data = fund_data_all[
            fund_data_all['code'] == fund_code
        ][['t_date', 'nav']].rename(columns={'nav': fund_name})
        fund_data = fund_data.drop_duplicates(['t_date'], keep='first').reset_index(drop=True)

        # 天眼赛能特殊处理
        if fund_code == 'P22984'.lower():
            fund_data = fund_data[fund_data['t_date'] >= datetime(2019, 8, 2).date()].reset_index(drop=True)

        fund_data = pd.merge(cal, fund_data, on='t_date', how='left')

        if fillna:
            # latest_date_i = fund_data[fund_data[fund_name] > 0].index[-1]
            # fund_data = fund_data.fillna(method='ffill')
            try:
                latest_date = fund_data[fund_data[fund_name] > 0].reset_index()['t_date'].tolist()[-1]
            except IndexError:
                latest_date = fund_data.reset_index()['t_date'].tolist()[0]
            if freq != '':
                try:
                    latest_date_week = cal_weekly[
                        cal_weekly['t_date'] >= latest_date
                    ].reset_index(drop=True)['t_date'][0]
                except:
                    latest_date_week = end_date
                latest_date_i = fund_data[fund_data['t_date'] >= latest_date_week].index[0]
            else:
                latest_date_i = fund_data[fund_data['t_date'] >= latest_date].index[0]
            fund_data = fund_data.fillna(method='ffill')

            # 最新净值之后不填充空置
            if (
                    len(fund_data) > latest_date_i + 1
            ) and (
                    fund_data['t_date'][latest_date_i] <= cal_spe['t_date'].tolist()[-2]
            ):
                fund_data.loc[latest_date_i + 1:, fund_name] = np.nan

            if freq in ['month', 'monthly']:
                if all_aligned:
                    # 算月度净值时先统一成周净值再转换成日净值，去掉部分日净值以同一所有产品净值频率，不直接按日净值转换为月净值
                    fund_data = pd.merge(cal_weekly, fund_data, on='t_date', how='left')
                try:
                    nav_end_date = fund_data[fund_data[fund_name] > 0]['t_date'].tolist()[-1]
                except IndexError:
                    nav_end_date = fund_data['t_date'].tolist()[0]
                fund_data = pd.merge(cal, fund_data, on='t_date', how='left')
                fund_data = fund_data.fillna(method='ffill')
                if cal_spe['t_date'].tolist()[-1] > nav_end_date:
                    date_i = cal_spe[cal_spe['t_date'] > nav_end_date]['t_date'].tolist()[0]
                    fund_data.loc[fund_data[fund_data['t_date'] >= date_i].index[0]:, fund_name] = np.nan
                else:
                    pass

        fund_data = pd.merge(cal_spe, fund_data, on='t_date', how='left')

        # 剔除产品运行前期净值长期横盘情况
        if drop_1:
            for d in range(len(fund_data)):
                if fund_data.iloc[d:d + 1][fund_name][d] == 1 and fund_data.iloc[d + 1:d + 2][fund_name][d + 1] != 1:
                    fund_data = fund_data.iloc[d:].reset_index(drop=True)
                    break
        try:
            i_dates.append(fund_data['t_date'][fund_data[fund_name] > 0].tolist()[0])
        except IndexError:
            pass
            # i_dates.append(np.nan)
        cal_all = pd.merge(cal_all, fund_data, on='t_date', how='left')

    i_date = np.nanmin(i_dates)
    if i_date > first_date:
        first_date = i_date
    return cal_all[cal_all['t_date'] >= first_date].reset_index(drop=True)


def load_funds_data1(
        fund_list,
        first_date=None,
        end_date=None,
        freq='w',
        fillna=True,
        db_path='',
        # cal_db_path='',
        drop_1=False,
        print_info=False,
):
    if first_date is None:
        first_date = datetime.now().date()

    if end_date is None:
        end_date = datetime.now().date()

    cal = load_calendar(end_date=end_date)
    cal_spe = load_calendar_extra(freq=freq, end_date=end_date)

    if len(fund_list) == 1:
        sql_l = 'code=\'' + fund_list['code'][0] + '\''
    else:
        sql_l = 'code in ' + str(tuple(fund_list['code']))

    fund_data_all = pd.read_sql_query(
        'select * from fund_data where ' + sql_l + ' and t_date<=' + end_date.strftime('%Y%m%d')
        + ' order by t_date',
        db_path
    )[['t_date', 'nav', 'code']].drop_duplicates(subset=['t_date', 'code'])
    fund_data_all['code'] = fund_data_all['code'].apply(
        lambda x: fund_list[fund_list['code'] == str(x).upper()]['name'].tolist()[0]
    )
    fund_data = fund_data_all.pivot(index='t_date', columns='code', values='nav')
    # 天眼赛能特殊处理
    if '天眼赛能' in fund_data.columns:
        fund_data.loc[:datetime(2019, 8, 2).date(), 'P22984'] = np.nan
    fund_data = fund_data.reset_index()
    fund_data = pd.merge(cal, fund_data, on='t_date', how='left').set_index('t_date')

    if fillna:
        if print_info:
            print('空缺净值填充前值，最新净值之后不填充')
        fund_data_is_na = fund_data.isna()
        fund_data_is_na[fund_data_is_na] = np.nan
        fund_data_is_na = fund_data_is_na.fillna(method='bfill').fillna(True)
        fund_data = fund_data.fillna(method='ffill')
        fund_data[fund_data_is_na] = np.nan

    fund_data = pd.merge(cal_spe, fund_data, on='t_date', how='left')

    if drop_1:
        if print_info:
            print('净值初期长期为1已去除')
        fund_data = fund_data.set_index('t_date')
        fund_data_bool = (fund_data.shift(-1) == fund_data) & (fund_data == 1)
        fund_data[fund_data_bool] = np.nan
        fund_data_is_na = fund_data.isna()
        fund_data = fund_data.fillna(method='ffill')
        fund_data[fund_data_is_na] = np.nan
        fund_data = fund_data.reset_index()

    i_date = fund_data.set_index('t_date').sum(axis=1)[fund_data.set_index('t_date').sum(axis=1) > 0].index[0]
    if i_date > first_date:
        first_date = i_date
    cal_all = fund_data
    return cal_all[cal_all['t_date'] >= first_date].reset_index(drop=True)


# 输入产品列表，输出对应产品的周超额净值或月超额净值
# 输入：DataFrame，输出：DataFrame
# 输入的DataFrame中需要包含对应benchmark的code列
# 如果first_date设置的太早会自动剔除前期空值
# 需要自行建立对应格式的数据库以及存入对应数据！
def load_funds_alpha(
        fund_list,
        first_date=datetime.now().date(),
        end_date=datetime.now().date(),
        freq='w',
        fillna=True,
        all_aligned=False,
        db_path='',
        # cal_db_path='',
        print_info=False
):
    cal = load_calendar(end_date=end_date)
    cal_weekly = load_calendar_extra(freq='w', end_date=end_date)

    cal_spe = load_calendar_extra(freq=freq, end_date=end_date)
    cal_eav = cal_spe.copy()
    cal_excess = cal_spe.copy()

    if len(fund_list) == 1:
        sql_l = 'code=\'' + fund_list['code'][0] + '\''
    else:
        sql_l = 'code in ' + str(tuple(fund_list['code']))

    fund_data_all = pd.read_sql_query(
        'select * from fund_data where ' + sql_l + ' and t_date<=' + end_date.strftime('%Y%m%d')
        + ' order by t_date',
        db_path
    )[['t_date', 'nav', 'code']]
    fund_data_all['code'] = fund_data_all['code'].apply(lambda x: x.lower())

    benchmarks = fund_list['benchmark'].drop_duplicates().apply(lambda x: x[:6])
    benchmarks_data = load_index(
        index_list=benchmarks.tolist(),
        end_date=end_date
    )[['TDATE', 'CODE', 'CLOSE']].rename(columns={'TDATE': 't_date'})
    benchmarks_data['t_date'] = pd.to_datetime(benchmarks_data['t_date']).dt.date
    benchmarks_data = benchmarks_data.pivot(index='t_date', columns='CODE', values='CLOSE')

    for i in range(len(fund_list)):
        fund_code = fund_list['code'][i].lower()
        fund_name = fund_list['name'][i]
        benchmark = fund_list['benchmark'][i][:6]
        if print_info:
            print('Loading ' + fund_name + ' ' + freq + ' 超额；')
        # if first_date > fund_list['first_date'][i]:
        #     first_date = fund_list['first_date'][i]

        fund_data = fund_data_all[
            fund_data_all['code'] == fund_code
            ][['t_date', 'nav']].rename(columns={'nav': fund_name})
        fund_data = fund_data.drop_duplicates(['t_date'], keep='first').reset_index(drop=True)

        # 衍复指增三号特殊处理
        if fund_code == 'SJH866'.lower():
            fund_data = fund_data[fund_data['t_date'] >= datetime(2020, 2, 14).date()].reset_index(drop=True)

        # 天眼赛能特殊处理
        if fund_code == 'P22984'.lower():
            fund_data = fund_data[fund_data['t_date'] >= datetime(2019, 8, 2).date()].reset_index(drop=True)

        # benchmark_data = load_index(
        #     index_list=[benchmark[:6]],
        #     end_date=end_date
        # )[['TDATE', 'CLOSE']].rename(columns={'TDATE': 't_date', 'CLOSE': 'bm'})
        # benchmark_data['t_date'] = pd.to_datetime(benchmark_data['t_date']).dt.date
        benchmark_data = benchmarks_data[benchmark].reset_index().rename(columns={benchmark: 'bm'})


        fund_aligned = pd.merge(cal, fund_data, on='t_date', how='left')
        if fillna:
            latest_date_i = fund_aligned[fund_aligned[fund_name] > 0].index[-1]
            fund_aligned = fund_aligned.fillna(method='ffill')

            # 最新净值之后不填充空置
            if len(fund_aligned) > latest_date_i + 1:
                fund_aligned.loc[latest_date_i + 1:, fund_name] = np.nan

            if freq in ['month', 'monthly']:
                if all_aligned:
                    # 算月度净值时先统一成周净值再转换成日净值，去掉部分日净值以同一所有产品净值频率，不直接按日净值转换为月净值
                    fund_aligned = pd.merge(cal_weekly, fund_aligned, on='t_date', how='left')
                fund_aligned = pd.merge(cal, fund_aligned, on='t_date', how='left')
                fund_aligned = fund_aligned.fillna(method='ffill')

        fund_aligned = pd.merge(cal_spe['t_date'], fund_aligned, on='t_date', how='left')

        # 剔除产品运行前期净值长期横盘情况
        # for d in range(len(fund_aligned)):
        #     if (
        #             fund_aligned.iloc[d:d + 1][fund_name][d] == 1
        #             and fund_aligned.iloc[d + 1:d + 2][fund_name][d + 1] != 1
        #     ):
        #         fund_aligned = fund_aligned.iloc[d + 1:].reset_index(drop=True)
        #         break

        fund_aligned = pd.merge(fund_aligned, benchmark_data, on='t_date', how='left')
        fund_aligned['ret'] = fund_aligned[fund_name] / fund_aligned[fund_name].shift(1) - 1
        fund_aligned['bm_ret'] = fund_aligned['bm'] / fund_aligned['bm'].shift(1) - 1
        fund_aligned['excess'] = fund_aligned['ret'] - fund_aligned['bm_ret']
        fund_aligned['eav'] = (fund_aligned['excess'] + 1).cumprod()
        fund_aligned.loc[fund_aligned[fund_aligned['eav'] > 0].index[0] - 1, 'eav'] = 1

        cal_spe = pd.merge(cal_spe, fund_aligned[['t_date', fund_name]], on='t_date', how='left')
        cal_eav = pd.merge(
            cal_eav, fund_aligned[['t_date', 'eav']].rename(columns={'eav': fund_name}), on='t_date', how='left'
        )
        cal_excess = pd.merge(
            cal_excess,
            fund_aligned[['t_date', 'excess']].rename(columns={'excess': fund_name}),
            on='t_date',
            how='left'
        )

    i_date = fund_list['first_date'].min()
    if i_date > first_date:
        first_date = i_date

    result = {
        'nav': cal_spe[cal_spe['t_date'] >= first_date].reset_index(drop=True),
        'eav': cal_eav[cal_eav['t_date'] >= first_date].reset_index(drop=True),
        'excess': cal_excess[cal_excess['t_date'] >= first_date].reset_index(drop=True)
    }
    return result


# 跟踪池标的列表传入HBDB
def fund_pool_to_hb(fund_df, table='fund_pool', sql_path='', sql_ip='', sql_user='', sql_pass='', database=''):
    sql_l = '''
    (
    id bigint not null AUTO_INCREMENT,
    name  varchar(100),
    type0  varchar(100),
    type1  varchar(100),
    primary key (id)
    )
    '''
    db = pymysql.connect(host=sql_ip, user=sql_user, password=sql_pass, database=database)
    cursor = db.cursor()

    sql = 'create table if not exists `' + table + '` ' + sql_l + ' comment=\'量化产品跟踪池\''
    cursor.execute(sql)
    print(table + ' generated')

    cursor.execute('truncate table ' + table)
    print('Clear ' + table)
    db.close()
    fund_df.to_sql(table, sql_path, if_exists='append', index=False)


# 跟踪池标的净值传入HBDB
def fund_data_to_hb(path_local, path_hb, sql_hb, database, tables=None):
    key_name = 'id'
    if tables is None:
        tables = [
            'fund_data',
            'fund_list',
        ]

    for t in tables:
        print(t)
        if t == 'fund_list':
            key_name = 'code'

        id_in_hb = pd.read_sql_query(
            'select `' + key_name + '` from ' + t + ' order by `' + key_name + '` desc', path_hb
        )
        id_in_local = pd.read_sql_query(
            'select `' + key_name + '` from ' + t + ' order by `' + key_name + '` desc', path_local
        )

        id_hb_diff = set(id_in_hb[key_name]).difference(set(id_in_local[key_name]))
        if len(id_hb_diff) > 0:
            db_hb = pymysql.connect(host=sql_hb['ip'], user=sql_hb['user'], password=sql_hb['pass'], database=database)
            cursor = db_hb.cursor()
            if len(id_hb_diff) > 1:
                cursor.execute(
                    'delete from ' + t + ' where `' + key_name + '` in ' + str(tuple(id_hb_diff))
                )
            else:
                cursor.execute(
                    'delete from ' + t + ' where `' + key_name + '`=\'' + str(list(id_hb_diff)[0]) + '\''
                )
            db_hb.commit()
            db_hb.close()
            print('\tdelete: ' + str(len(id_hb_diff)))

        if t == 'fund_list':
            id_local_diff = set(id_in_local[key_name]).difference(set(id_in_hb[key_name]))
            if len(id_local_diff) == 0:
                print('\tnew data: 0')
                continue

            if len(id_local_diff) == 1:
                data_list_new = pd.read_sql_query(
                    'select * from ' + t + ' where `' + key_name + '`=\'' + list(id_local_diff)[0] + '\'', path_local
                )
            else:
                data_list_new = pd.read_sql_query(
                    'select * from ' + t + ' where `' + key_name + '` in ' + str(tuple(id_local_diff)), path_local
                )

            data_list_new.to_sql(t, path_hb, if_exists='append', index=False)
            print('\tnew data: ' + str(len(data_list_new)))

        else:
            data_hb_last_one = pd.read_sql_query(
                'select `' + key_name + '` from ' + t + ' order by `' + key_name + '` desc limit 1', path_hb
            )
            if len(data_hb_last_one) > 0:
                id_num = data_hb_last_one[key_name][0]
            else:
                id_num = -1

            data_work_new = pd.read_sql_query(
                'select * from ' + t + ' where `' + key_name + '`>' + str(id_num), path_local
            )
            data_work_new.to_sql(t, path_hb, if_exists='append', index=False)
            print('\tnew data: ' + str(len(data_work_new)))


def load_gzb(name, start_date, end_date, db_path, table='gzb', c_diff=True):
    data = pd.read_sql_query(
        'select 日期, 基金名称, 科目代码, 科目名称, 市值占净值 from ' + table
        + ' where 日期<=' + end_date.strftime('%Y%m%d')
        + ' and 日期>=' + start_date.strftime('%Y%m%d')
        + ' and 基金名称="' + name + '"'
        + ' and 市价 > 0 order by 日期, 科目名称',
        db_path
    )
    data_info = data[['科目代码', '科目名称']].drop_duplicates(subset=['科目名称'])
    if c_diff:
        data = data.groupby(['日期', '科目名称'], as_index=False).sum()
        data = data.merge(data_info, on='科目名称', how='left')
    c_ind = data['科目代码'].str.split('310').str[0] == ''
    data.loc[c_ind, '品种'] = data.loc[c_ind, '科目代码'].apply(lambda x: re.findall(r'[a-zA-Z]+', x[8:])[0].upper())
    data['基金名称'] = name
    sec_df = pd.DataFrame()
    for i in fut_sectors:
        sec = pd.DataFrame(fut_sectors[i]).rename(columns={0: '品种'})
        sec['板块'] = i
        sec_df = sec_df.append(sec)
    data = data.merge(sec_df, on='品种', how='left')
    data.loc[data['板块'].isnull().values == True, '板块'] = data.loc[data['板块'].isnull().values == True, '科目名称']
    data['板块'] = data['板块'].apply(
        lambda x: x.replace('私募证券投资基金', '').replace('私募投资基金', '').replace('私募基金', '')
    )
    return data

