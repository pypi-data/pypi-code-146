from hbshare.quant.CChen.data.data import load_calendar
from hbshare.quant.CChen.cons import fut_sectors
from hbshare.quant.CChen.cta_factor.const import composite_factor
from hbshare.quant.CChen.db_const import sql_write_path_work
import pandas as pd
from datetime import datetime, timedelta


def cta_factor_line(cta_factors, start_date, end_date, table=None, sql_path=None, freq=''):
    if table is None:
        table = 'cta_index'

    if sql_path is None:
        sql_path = sql_write_path_work['daily']

    cal = load_calendar(
        start_date=start_date, end_date=end_date, freq=freq
    )
    data_all = pd.read_sql_query(
        'select TDATE, CLOSE, FACTOR from ' + table
        + ' where TDATE<=' + end_date.strftime('%Y%m%d')
        + ' and TDATE>=' + start_date.strftime('%Y%m%d')
        + ' and FACTOR in ' + str(tuple(cta_factors.keys())).replace(',)', ')')
        + ' order by TDATE',
        sql_path
    )
    data_all['FACTOR'] = data_all['FACTOR'].apply(lambda x: cta_factors[x])
    data_all = data_all.pivot(index='TDATE', columns='FACTOR', values='CLOSE')
    # data_all = data_all / data_all.loc[data_all.index[0], :]

    data = cal.merge(data_all.reset_index().rename(columns={'TDATE': 't_date'}), on='t_date', how='left')
    data = data.set_index(data['t_date'])[list(cta_factors.values())]
    data = data / data.loc[data.index[0], :]
    return data


# 收益拆分
def cta_factor_analysis(cta_factors, sql_path, start_date, end_date):
    codes = pd.read_sql_query(
        'select EXCHANGE, PCODE, CODE from hsjy_fut_info_p', sql_path
    )
    codes['UCODE'] = codes['EXCHANGE'] * 1000 + codes['PCODE']
    codes = codes.drop_duplicates('UCODE')

    sector_df = pd.DataFrame()
    for i in fut_sectors:
        sector_df = sector_df.append(
            pd.DataFrame(
                {
                    'CODE': fut_sectors[i],
                    'SECTOR': i
                }
            )
        )

    sector_comntribution = None
    for i in cta_factors:
        print(i)
        if i in composite_factor:
            factor_data = pd.read_sql_query(
                'select * from cta_factor where TDATE<=' + end_date.strftime('%Y%m%d')
                + ' and TDATE >=' + start_date.strftime('%Y%m%d')
                + ' and FACTOR in ' + str(tuple(composite_factor[i])) + '',
                sql_path
            )
        else:
            factor_data = pd.read_sql_query(
                'select * from cta_factor where TDATE<=' + end_date.strftime('%Y%m%d')
                + ' and TDATE >=' + start_date.strftime('%Y%m%d')
                + ' and FACTOR=\'' + i + '\'',
                sql_path
            )
        factor_data = factor_data.drop_duplicates(subset=['TDATE', 'UCODE', 'FACTOR'])
        factor_data['ret'] = factor_data['WEIGHT'] * factor_data['RETURN'] * factor_data['POS'] / 10000
        # factor_return = factor_data.pivot(index='TDATE', columns='UCODE', values='ret')
        # factor_return = factor_return.mul((factor_return.sum(axis=1) + 1).shift(1).cumprod().fillna(1), axis=0)
        # return_contribute = factor_return.sum(axis=0)
        return_contribute = factor_data.groupby(by='UCODE').sum()[['ret']].reset_index()

        return_contribute = return_contribute.reset_index().merge(
            codes, on='UCODE', how='left'
        ).merge(
            sector_df, on='CODE', how='left'
        )

        rrr = return_contribute.groupby(by='SECTOR').sum()[['ret']].reset_index()
        if sector_comntribution is None:
            sector_comntribution = rrr.rename(columns={'ret': cta_factors[i]})
        else:
            sector_comntribution = sector_comntribution.merge(
                rrr.rename(columns={'ret': cta_factors[i]}), on='SECTOR', how='left'
            )
    return sector_comntribution


if __name__ == '__main__':

    endDate = datetime(2022, 7, 1).date()
    # startDate = datetime(2022, 6, 13).date()
    startDate = endDate - timedelta(days=365 * 2)
    startDate_analysis = datetime(2022, 6, 1).date()

    factors = {
        'tsrev_d1': '短反转',
        'tsmom_d3': '短时序动量',
        'tsmom_d10': '中时序动量',
        'tsmom_d250': '长时序动量',
        'xsmom_d20_q75': '中截面动量',
        'xsmom_d250_q75': '长截面动量',
        'carry_d20_q70': '截面展期',
        'tscarry_d50': '时序展期',
        'tsbasismom_d3': '短基差动量',
        'xssigma_d20_q75': '波动率',
        # 'xsmrchg_d1_q50': '会员持仓'
    }

    data_table = 'cta_index'
    path = sql_write_path_work['daily']

    factor_line = cta_factor_line(
        cta_factors=factors,
        start_date=startDate,
        end_date=endDate,
        table=data_table,
        sql_path=path,
        freq='w'
    )
    factor_analysis = cta_factor_analysis(
        cta_factors=factors,
        sql_path=path,
        start_date=startDate_analysis,
        end_date=endDate
    )

    factor_line.to_excel(endDate.strftime('%Y%m%d') + '_cta_factors.xlsx')
    # factor_analysis.to_excel(endDate.strftime('%Y%m%d') + '_cta_分板块贡献.xlsx')


