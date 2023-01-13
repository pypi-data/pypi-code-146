#!/usr/bin/python
# coding:utf-8
import pandas as pd
import numpy as np
from datetime import timedelta


def xs_weight(data):
    pos_long = sum(data['POS'] == 1)
    pos_short = sum(data['POS'] == -1)
    data['WEIGHT'] = data['POS'].apply(
        lambda x: 0.5 / pos_long if x == 1 else (0.5 / pos_short if x == -1 else 0)
    )
    print('\t%.2f%%' % (data['RETURN'] * data['WEIGHT'] * data['POS'] * 100).sum())
    return data


def ts_weight(data):
    if sum(data['POS'] != 0) > 0:
        data['WEIGHT'] = 1 / sum(data['POS'] != 0)
    else:
        data['WEIGHT'] = 0
    print('\t%.2f%%' % (data['RETURN'] * data['WEIGHT'] * data['POS'] * 100).sum())
    return data


def ts_pos(data, direction=1):
    data['POS'] = data['FACTORVALUE'] / data['FACTORVALUE'].abs() * direction
    data = data[~np.isnan(data['POS'])].reset_index(drop=True)
    return ts_weight(data)


def xs_pos_mat(factor, xs_q, direction=1):
    factor0 = factor.T.copy()
    factor_upper = factor0 > factor0.quantile(xs_q / 100)
    factor_lower = factor0 < factor0.quantile(1 - xs_q / 100)
    factor0.loc[:] = np.nan
    factor0[factor_upper] = direction
    factor0[factor_lower] = -direction

    fa = factor0.T
    # weights = factor / factor
    # weights = weights[~factor_a.isna()]
    weights = factor.copy()
    weights.loc[:] = np.nan
    weights[fa > 0] = fa[fa > 0].div(fa[fa > 0].count(axis=1) * 2, axis=0)
    weights[fa < 0] = fa[fa < 0].div(fa[fa < 0].count(axis=1) * -2, axis=0)
    # weights = weights.div(weights.count(axis=1), axis=0)
    return fa, weights


def ts_pos_mat(factor, direction=1):
    fa = factor / factor.abs() * direction
    weights = factor / factor
    weights = weights[~fa.isna()]
    weights = weights.div(weights.count(axis=1), axis=0)
    return fa, weights


def pos_summary(positions, fv100=True):
    if len(positions) == 0:
        return
    # print(100)
    positions['WEIGHT'] = positions['WEIGHT'] * 100
    positions['RETURN'] = positions['RETURN'] * 100
    if fv100:
        positions['FACTORVALUE'] = positions['FACTORVALUE'] * 100
    return positions[
        ['TDATE', 'EXCHANGE', 'PCODE', 'UCODE', 'CLOSE', 'CLOSE1', 'POS', 'RETURN', 'FACTORVALUE', 'FACTOR', 'WEIGHT']
    ].reset_index(drop=True)


def pre_data(price, **kwargs):
    data = kwargs['data']
    liq_days = kwargs['liq_days']
    data.loc[:, 'UCODE'] = data['EXCHANGE'].apply(lambda x: str(x)) + data['PCODE'].apply(lambda x: str(x))
    calendar = data['TDATE'].drop_duplicates().tolist()

    data_price = data.pivot(index='TDATE', columns='UCODE', values=price)
    data_vol = data.pivot(
        index='TDATE', columns='UCODE', values='VOL'
    ).rolling(max(liq_days, kwargs['ts_n'])).mean()
    price_liq = data_price.shift(-1 if price in ['OPEN', 'SETTLE'] else 0)[data_vol > kwargs['min_volume']]
    return data, liq_days, calendar, price_liq


def mom(data_t, calendar, i, ts_n, factor, data):
    lookback_date = calendar[i - ts_n]

    data_t = data_t.merge(
        data[data['TDATE'] == lookback_date][['UCODE', factor]].rename(columns={factor: 'x0'}),
        on='UCODE', how='left'
    ).merge(
        data[data['TDATE'] == calendar[i]][['UCODE', factor]].rename(columns={factor: 'x1'}),
        on='UCODE', how='left'
    )
    data_t['FACTORVALUE'] = data_t['x1'] / data_t['x0'] - 1
    return data_t


def basismom(data, data_c, ts_n):
    # matrix
    data = data[data['TDATE'] >= data_c['TDATE'].sort_values().tolist()[0]].reset_index(drop=True)
    code_ldate = data_c.drop_duplicates(subset=['CCODE']).reset_index(drop=True)[['CCODE', 'LDATE']]
    code1 = data.pivot(index='TDATE', columns='UCODE', values='CCODE')
    code2 = data.pivot(index='TDATE', columns='UCODE', values='CCODE2')
    contracts = data_c.pivot(index='TDATE', columns='CCODE', values='CLOSE')
    con_chg = contracts / contracts.shift(ts_n) - 1
    factor = pd.DataFrame()
    for i in code1.index:
        print(i)
        factor_0 = pd.DataFrame(code1.loc[i].dropna()).rename(columns={i: 'CCODE'}).reset_index().merge(
            con_chg.loc[i].reset_index().rename(columns={i: 'r1'}), on='CCODE', how='left'
        ).merge(
            code_ldate, on='CCODE', how='left'
        ).merge(
            pd.DataFrame(code2.loc[i].dropna()).rename(columns={i: 'CCODE'}).reset_index().merge(
                con_chg.loc[i].reset_index().rename(columns={i: 'r2'}), on='CCODE', how='left'
            ).merge(
                code_ldate.rename(columns={'LDATE': 'LDATE2'}), on='CCODE', how='left'
            ), on='UCODE', how='inner'
        )
        factor_0['FACTORVALUE'] = (
                                          factor_0['r1'] - factor_0['r2']
                                  ) * (factor_0['LDATE2'] - factor_0['LDATE']).apply(lambda x: x.days)
        factor_0['TDATE'] = i
        factor = factor.append(factor_0[['TDATE', 'UCODE', 'FACTORVALUE']])
    factor = factor.pivot(index='TDATE', columns='UCODE', values='FACTORVALUE')
    return factor.replace([np.inf, -np.inf], np.nan)


def to_pos(data, factor, pos, weights, price_liq, index_name, start_date):
    # weights = factor / factor
    # weights = weights[~pos.isna()]
    # weights = weights.div(weights.count(axis=1), axis=0)
    positions = price_liq.shift(1).reset_index().melt(id_vars='TDATE').rename(columns={'value': 'CLOSE'}).merge(
        factor.shift(1).reset_index().melt(id_vars='TDATE').rename(columns={'value': 'FACTORVALUE'}),
        on=['TDATE', 'UCODE'], how='left'
    ).merge(
        pos.shift(1).reset_index().melt(id_vars='TDATE').rename(columns={'value': 'POS'}),
        on=['TDATE', 'UCODE'], how='left'
    ).merge(
        weights.shift(1).reset_index().melt(id_vars='TDATE').rename(
            columns={
                'value': 'WEIGHT',
                # 'variable': 'UCODE'
            }
        ),
        on=['TDATE', 'UCODE'], how='left'
    # ).merge(
    #     price_liq.reset_index().melt(id_vars='TDATE').rename(columns={'value': 'CLOSE1'}),
    #     on=['TDATE', 'UCODE'], how='left'
    ).merge(
        data.reset_index().melt(id_vars='TDATE').rename(columns={'value': 'CLOSE1'}),
        on=['TDATE', 'UCODE'], how='left'
    )
    positions['RETURN'] = positions['CLOSE1'] / positions['CLOSE'] - 1
    positions['FACTOR'] = index_name
    positions = positions[positions['TDATE'] > max(start_date, factor.index[0])].reset_index(drop=True)
    # positions = positions[~positions['POS'].isna()].reset_index(drop=True)
    positions['EXCHANGE'] = positions['UCODE'].apply(lambda x: x[:2])
    positions['PCODE'] = positions['UCODE'].apply(lambda x: x[2:])
    return positions


def pre_loop(i, calendar, data, data_liq, price='CLOSE'):
    data_price = data.pivot(index='TDATE', columns='UCODE', values=price).shift(
        -1 if price in ['OPEN', 'SETTLE'] else 0
    )
    liq_u = data_liq.loc[[calendar[i]]]
    liq_u = liq_u.T[liq_u.T[calendar[i]] > 0]
    data_t = data_price.loc[[calendar[i], calendar[i + 1]], list(liq_u.index)].T.reset_index().rename(
        columns={
            calendar[i]: 'CLOSE',
            calendar[i + 1]: 'CLOSE1'
        }
    )
    data_t['RETURN'] = data_t['CLOSE1'] / data_t['CLOSE'] - 1
    data_t['TDATE'] = calendar[i + 1]
    data_t['EXCHANGE'] = data_t['UCODE'].apply(lambda x: x[:2])
    data_t['PCODE'] = data_t['UCODE'].apply(lambda x: x[2:])
    return data_t


def get_index(calendar, date):
    return calendar.index(np.array(calendar)[np.array(calendar) >= date][0])


def compute_factor(x, i, calendar, ts_n):
    x_0 = x[
        np.array(x['TDATE'] >= calendar[i - ts_n])
        & np.array(x['TDATE'] < calendar[i])
        ][['UCODE', 'x']].groupby(by=['UCODE'], as_index=False).mean()
    x_t = x[x['TDATE'] == calendar[i]][['UCODE', 'x']]

    x_range = pd.merge(
        x_0.rename(columns={'x': 'x0'}),
        x_t.rename(columns={'x': 'x1'}),
        on='UCODE', how='left'
    )
    x_range['FACTORVALUE'] = x_range['x1'] - x_range['x0']
    return x_range


def compute_factor_mat(data, ts_n, lag_n=0):
    data = data.pivot(index='TDATE', columns='UCODE', values='x')
    return data.shift(lag_n) / data.shift(ts_n + lag_n) - 1


def xs_pos(data, direction=1, quantile=50):
    # data = data[~np.isnan(data['FACTORVALUE'])].reset_index(drop=True)
    quantile_p = data['FACTORVALUE'].quantile(quantile / 100)
    quantile_n = data['FACTORVALUE'].quantile(1 - quantile / 100)
    data['POS'] = data['FACTORVALUE'].apply(
        lambda x: direction if x > quantile_p else (-direction if x < quantile_n else np.nan)
    )
    data = data[~np.isnan(data['POS'])].reset_index(drop=True)
    return xs_weight(data)


def tsmom(start_date, name='mom', direction=1, price='CLOSE', factor='CLOSE', loop=False, **kwargs):
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']

    index_name = 'ts' + name + '_d' + str(ts_n)
    start_index = get_index(calendar=calendar, date=start_date)

    # loop
    if loop:
        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]
            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
            )

            data_t = mom(data_t, calendar, i, ts_n, factor, data)

            data_t['FACTOR'] = index_name
            data_t = ts_pos(data_t, direction=direction)

            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:
        # matrix
        factor_raw = data.pivot(index='TDATE', columns='UCODE', values=factor)
        factor = factor_raw - factor_raw.shift(ts_n)
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        # factor = (price_liq / price_liq.shift(ts_n) - 1)
        pos, weights = ts_pos_mat(factor=factor, direction=direction)
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions)


def xsmom(start_date, name='mom', direction=1, price='CLOSE', factor='CLOSE', loop=False, **kwargs):
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    quantile = kwargs['quantile']

    index_name = 'xs' + name + '_d' + str(ts_n) + '_q' + str(quantile)
    start_index = get_index(calendar=calendar, date=start_date)

    if loop:
        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]
            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
            )

            data_t = mom(data_t, calendar, i, ts_n, factor, data)

            data_t['FACTOR'] = index_name
            data_t = xs_pos(data=data_t, direction=direction, quantile=quantile)

            data_t['FACTOR'] = index_name
            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:
        # matrix
        factor_raw = data.pivot(index='TDATE', columns='UCODE', values=factor)
        factor = factor_raw / factor_raw.shift(ts_n) - 1
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        # factor = (price_liq / price_liq.shift(ts_n) - 1)
        pos, weights = xs_pos_mat(factor=factor, xs_q=quantile, direction=direction)
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions)


def tsrev(start_date, loop=False, **kwargs):
    return tsmom(start_date=start_date, name='rev', direction=-1, loop=loop, **kwargs)


def tswr(start_date, name='wr', price='CLOSE', loop=False, **kwargs):
    # 根据前一日仓单数据计算
    # 当日收盘价开平仓
    data_wr = kwargs['data_wr']
    data_wr['UCODE'] = data_wr['EXCHANGE'].apply(lambda x: str(int(x))) + data_wr['PCODE'].apply(lambda x: str(int(x)))
    # data_wr = data_wr.drop_duplicates(subset=['TDATE', 'UCODE'])
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)
    ts_n = kwargs['ts_n']
    index_name = 'ts' + name + '_d' + str(ts_n)
    start_index = get_index(calendar=calendar, date=start_date)

    if loop:

        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]
            factor = compute_factor(
                x=data_wr,
                i=i,
                calendar=calendar,
                ts_n=ts_n,
            )
            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
                price=price,
            )
            data_t = data_t.merge(factor, on='UCODE', how='inner')
            data_t['FACTOR'] = index_name
            data_t = ts_pos(data=data_t, direction=-1)
            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:
        # matrix
        factor = compute_factor_mat(data=data_wr, ts_n=ts_n)
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = ts_pos_mat(factor=factor, direction=-1)
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions, fv100=False)


def xswr(start_date, name='wr', price='CLOSE', loop=False, **kwargs):
    # 根据前一日仓单数据计算
    # 当日收盘价开平仓
    data_wr = kwargs['data_wr']
    data_wr['UCODE'] = data_wr['EXCHANGE'].apply(lambda x: str(int(x))) + data_wr['PCODE'].apply(lambda x: str(int(x)))
    # data_wr = data_wr.drop_duplicates(subset=['TDATE', 'UCODE'])
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    quantile = kwargs['quantile']
    index_name = 'xs' + name + '_d' + str(ts_n) + '_q' + str(quantile)
    start_index = get_index(calendar=calendar, date=start_date)

    if loop:

        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]
            factor = compute_factor(
                x=data_wr,
                i=i,
                calendar=calendar,
                ts_n=ts_n,
            )

            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
                price=price,
            )

            data_t = data_t.merge(factor, on='UCODE', how='inner')

            data_t['FACTOR'] = index_name
            data_t = xs_pos(data=data_t, direction=-1, quantile=quantile)
            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:
        # matrix
        factor = compute_factor_mat(data=data_wr, ts_n=ts_n)
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = xs_pos_mat(factor=factor, direction=-1, xs_q=quantile)
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions)


def carry(start_date, price='CLOSE', loop=False, **kwargs):
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    quantile = kwargs['quantile']
    index_name = 'carry_d' + str(ts_n) + '_q' + str(quantile)
    start_index = get_index(calendar=calendar, date=start_date)

    if loop:

        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]
            lookback_date = calendar[i - ts_n]
            data_ry = data[
                np.array(data['TDATE'] <= t_date)
                & np.array(data['TDATE'] > lookback_date)
                ].groupby('UCODE').mean().reset_index()[['UCODE', 'RY']]
            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq
                # price=price_field,
            )
            data_t = pd.merge(data_t.rename(columns={'RY': 'RY0'}), data_ry, on='UCODE')
            data_t = data_t.rename(columns={'RY': 'FACTORVALUE'})
            data_t = xs_pos(data=data_t, quantile=quantile)
            data_t['FACTOR'] = index_name

            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:

        # matrix
        factor = data.pivot(index='TDATE', columns='UCODE', values='RY').rolling(ts_n, min_periods=1).mean()
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = xs_pos_mat(factor=factor, xs_q=quantile)
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions)


def tscarry(start_date, price='CLOSE', loop=False, **kwargs):
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    index_name = 'tscarry_d' + str(ts_n)

    start_index = get_index(calendar=calendar, date=start_date)
    if loop:

        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]
            lookback_date = calendar[i - ts_n]
            data_ry = data[
                np.array(data['TDATE'] <= t_date)
                & np.array(data['TDATE'] > lookback_date)
                ].groupby('UCODE').mean().reset_index()[['UCODE', 'RY']]
            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq
                # price=price_field,
            )

            data_t = pd.merge(data_t.rename(columns={'RY': 'RY0'}), data_ry, on='UCODE')
            data_t = data_t.rename(columns={'RY': 'FACTORVALUE'})
            data_t = ts_pos(data=data_t)
            data_t['FACTOR'] = index_name

            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:
        # matrix
        factor = data.pivot(index='TDATE', columns='UCODE', values='RY').rolling(ts_n).mean()
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = ts_pos_mat(
            factor=factor,
            # xs_q=quantile
        )
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions)


def tsbasismom(start_date, price='CLOSE', loop=False, **kwargs):
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    index_name = 'tsbasismom_d' + str(ts_n)
    data_raw = kwargs['data_raw']
    data_raw = data_raw[data_raw['TDATE'] >= start_date - timedelta(days=max(ts_n, liq_days) * 2)].reset_index(drop=True)

    start_index = get_index(calendar=calendar, date=start_date)
    if loop:
        code_ldate = kwargs['data_raw'].drop_duplicates(subset=['CCODE']).reset_index(drop=True)[['CCODE', 'LDATE']]

        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]

            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq
                # price=price_field,
            )
            data_code = data[data['TDATE'] == t_date]

            data_t = data_t.merge(
                data_code[['UCODE', 'CCODE', 'CCODE2', ]],
                on='UCODE', how='left'
            )
            code_close = kwargs['data_raw'].pivot(index='TDATE', columns='CCODE', values='CLOSE')
            code_chg = code_close / code_close.shift(ts_n) - 1

            data_t = data_t.merge(
                code_chg.loc[t_date].reset_index().rename(columns={t_date: 'return1'}),
                on='CCODE', how='left'
            ).merge(
                code_chg.loc[t_date].reset_index().rename(
                    columns={
                        t_date: 'return2',
                        'CCODE': 'CCODE2'
                    }
                ),
                on='CCODE2', how='left'
            ).merge(
                code_ldate, on='CCODE', how='left'
            ).merge(
                code_ldate.rename(columns={'CCODE': 'CCODE2', 'LDATE': 'LDATE2'}), on='CCODE2', how='left'
            )

            data_t['FACTORVALUE'] = (
                                            data_t['return1'] - data_t['return2']
                                    ) * (data_t['LDATE2'] - data_t['LDATE']).apply(lambda x: x.days)
            data_t = data_t[~np.isinf(data_t['FACTORVALUE'])].reset_index(drop=True)

            data_t = ts_pos(data_t)
            data_t['FACTOR'] = index_name

            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:

        # matrix
        factor = basismom(data=data, data_c=data_raw, ts_n=ts_n)
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = ts_pos_mat(
            factor=factor,
            # xs_q=quantile
        )
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions)


def xsbasismom(start_date, price='CLOSE', loop=False, **kwargs):
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    quantile = kwargs['quantile']
    index_name = 'xsbasismom_d' + str(ts_n) + '_q' + str(quantile)
    data_raw = kwargs['data_raw']
    data_raw = data_raw[data_raw['TDATE'] >= start_date - timedelta(days=max(ts_n, liq_days) * 2)].reset_index(drop=True)

    start_index = get_index(calendar=calendar, date=start_date)
    if loop:
        code_ldate = kwargs['data_raw'].drop_duplicates(subset=['CCODE']).reset_index(drop=True)[['CCODE', 'LDATE']]
        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]

            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
                # price=price_field,
            )
            data_code = data[data['TDATE'] == t_date]

            data_t = data_t.merge(
                data_code[['UCODE', 'CCODE', 'CCODE2', ]],
                on='UCODE', how='left'
            )
            code_close = kwargs['data_raw'].pivot(index='TDATE', columns='CCODE', values='CLOSE')
            code_chg = code_close / code_close.shift(ts_n) - 1

            data_t = data_t.merge(
                code_chg.loc[t_date].reset_index().rename(columns={t_date: 'return1'}),
                on='CCODE', how='left'
            ).merge(
                code_chg.loc[t_date].reset_index().rename(
                    columns={
                        t_date: 'return2',
                        'CCODE': 'CCODE2'
                    }
                ),
                on='CCODE2', how='left'
            ).merge(
                code_ldate, on='CCODE', how='left'
            ).merge(
                code_ldate.rename(columns={'CCODE': 'CCODE2', 'LDATE': 'LDATE2'}), on='CCODE2', how='left'
            )

            data_t['FACTORVALUE'] = (
                                            data_t['return1'] - data_t['return2']
                                    ) * (data_t['LDATE2'] - data_t['LDATE']).apply(lambda x: x.days)
            data_t = data_t[~np.isinf(data_t['FACTORVALUE'])].reset_index(drop=True)

            data_t = xs_pos(data_t, quantile=quantile)
            data_t['FACTOR'] = index_name

            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:

        # matrix
        factor = basismom(data=data, data_c=data_raw, ts_n=ts_n)
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = xs_pos_mat(
            factor=factor,
            xs_q=quantile
        )
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions)


def xsrev(start_date, loop=False, **kwargs):
    return xsmom(start_date=start_date, name='rev', direction=-1, loop=loop, **kwargs)


# n日净持仓
# 净头寸区间总和为正做多
def mr(start_date, price='CLOSE', loop=False, **kwargs):
    data_mr = kwargs['data_mr']
    data_mr['UCODE'] = data_mr['EXCHANGE'].apply(lambda x: str(x)) + data_mr['PCODE'].apply(lambda x: str(x))
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    index_name = 'mr_d' + str(ts_n)
    start_index = get_index(calendar=calendar, date=start_date)
    if loop:

        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]

            data_mr_t = data_mr[
                np.array(data_mr['TDATE'] >= calendar[i - ts_n])
                & np.array(data_mr['TDATE'] <= calendar[i])
                ].groupby(by=['UCODE']).sum()[['MR']].reset_index()
            data_mr_range = data_mr_t

            data_mr_range['FACTORVALUE'] = data_mr_range['MR']

            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
                price=price,
            )

            data_t = pd.merge(data_t, data_mr_range, on='UCODE', how='inner')

            data_t['FACTOR'] = index_name
            data_t = ts_pos(data=data_t)
            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:

        # matrix
        data_mr = data_mr.groupby(by=['TDATE', 'UCODE']).sum().reset_index()
        factor = data_mr.pivot(index='TDATE', columns='UCODE', values='MR').rolling(ts_n).sum()
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = ts_pos_mat(
            factor=factor,
            # xs_q=quantile
        )
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions, fv100=False)


# n日净持仓
# 净头寸比总头寸区间总和为正做多
def mr2(start_date, price='CLOSE', **kwargs):
    data_mr = kwargs['data_mr']
    data_mr['UCODE'] = data_mr['EXCHANGE'].apply(lambda x: str(x)) + data_mr['PCODE'].apply(lambda x: str(x))
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    index_name = 'mr2_d' + str(ts_n)
    start_index = get_index(calendar=calendar, date=start_date)

    # matrix
    data_mr['MRabs'] = data_mr['MR'].abs()
    data_mr = data_mr.groupby(by=['TDATE', 'UCODE']).sum().reset_index()
    factor = data_mr.pivot(index='TDATE', columns='UCODE', values='MR').rolling(ts_n).sum()
    factor1 = data_mr.pivot(index='TDATE', columns='UCODE', values='MRabs').rolling(ts_n).sum()
    factor = factor / factor1
    factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
    pos, weights = ts_pos_mat(
        factor=factor,
        # xs_q=quantile
    )
    data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
    positions = to_pos(
        data=data_m,
        factor=factor,
        pos=pos,
        weights=weights,
        price_liq=price_liq,
        index_name=index_name,
        start_date=calendar[start_index]
    )
    return pos_summary(positions=positions)


# n日净持仓
# 净头寸区间总和排序
def xsmr(start_date, price='CLOSE', loop=False, **kwargs):
    data_mr = kwargs['data_mr']
    data_mr['UCODE'] = data_mr['EXCHANGE'].apply(lambda x: str(x)) + data_mr['PCODE'].apply(lambda x: str(x))
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    quantile = kwargs['quantile']
    ts_n = kwargs['ts_n']
    index_name = 'xsmr_d' + str(ts_n) + '_q' + str(quantile)
    start_index = get_index(calendar=calendar, date=start_date)
    if loop:

        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]

            data_mr_t = data_mr[
                np.array(data_mr['TDATE'] >= calendar[i - ts_n])
                & np.array(data_mr['TDATE'] <= calendar[i])
                ].groupby(by=['UCODE']).sum()[['MR']].reset_index()
            data_mr_range = data_mr_t

            data_mr_range['FACTORVALUE'] = data_mr_range['MR']

            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
                price=price,
            )

            data_t = pd.merge(data_t, data_mr_range, on='UCODE', how='inner')

            data_t['FACTOR'] = index_name
            data_t = xs_pos(data=data_t, quantile=quantile)
            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:

        # matrix
        data_mr = data_mr.groupby(by=['TDATE', 'UCODE']).sum().reset_index()
        factor = data_mr.pivot(index='TDATE', columns='UCODE', values='MR').rolling(ts_n).sum()
        factor0 = data.pivot(index='TDATE', columns='UCODE', values='POI').rolling(ts_n).sum()
        factor = factor / factor0
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = xs_pos_mat(
            factor=factor,
            xs_q=quantile
        )
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions)


# n日净持仓
# 净头寸比总头寸区间总和排序
def xsmr2(start_date, price='CLOSE', **kwargs):
    data_mr = kwargs['data_mr']
    data_mr['UCODE'] = data_mr['EXCHANGE'].apply(lambda x: str(x)) + data_mr['PCODE'].apply(lambda x: str(x))
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    quantile = kwargs['quantile']
    ts_n = kwargs['ts_n']
    index_name = 'xsmr2_d' + str(ts_n) + '_q' + str(quantile)
    start_index = get_index(calendar=calendar, date=start_date)

    # matrix
    data_mr['MRabs'] = data_mr['MR'].abs()
    data_mr = data_mr.groupby(by=['TDATE', 'UCODE']).sum().reset_index()
    factor = data_mr.pivot(index='TDATE', columns='UCODE', values='MR').rolling(ts_n).sum()
    factor1 = data_mr.pivot(index='TDATE', columns='UCODE', values='MRabs').rolling(ts_n).sum()
    factor = factor / factor1
    factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
    pos, weights = xs_pos_mat(
        factor=factor,
        xs_q=quantile
    )
    data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
    positions = to_pos(
        data=data_m,
        factor=factor,
        pos=pos,
        weights=weights,
        price_liq=price_liq,
        index_name=index_name,
        start_date=calendar[start_index]
    )
    return pos_summary(positions=positions)


# n日净持仓变化
# 净头寸时序增加做多
def tsmr(start_date, price='CLOSE', loop=False, **kwargs):
    data_mr = kwargs['data_mr']
    data_mr['UCODE'] = data_mr['EXCHANGE'].apply(lambda x: str(x)) + data_mr['PCODE'].apply(lambda x: str(x))
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    index_name = 'tsmr_d' + str(ts_n)
    start_index = get_index(calendar=calendar, date=start_date)
    if loop:

        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]
            data_mr_0 = data_mr[
                data_mr['TDATE'] == calendar[i - ts_n]
            ].groupby(by=['UCODE']).sum()[['MR']].reset_index()
            data_mr_t = data_mr[
                data_mr['TDATE'] == calendar[i]
            ].groupby(by=['UCODE']).sum()[['MR']].reset_index()

            data_mr_range = pd.merge(
                data_mr_0.rename(columns={'MR': 'MR0'}),
                data_mr_t.rename(columns={'MR': 'MR1'}),
                on='UCODE', how='left'
            )
            data_mr_range['FACTORVALUE'] = data_mr_range['MR1'] - data_mr_range['MR0']
            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
                price=price,
            )

            data_t = pd.merge(data_t, data_mr_range, on='UCODE', how='inner')
            data_t['FACTOR'] = index_name
            data_t = ts_pos(data=data_t)
            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:

        # matrix
        data_mr = data_mr.groupby(by=['TDATE', 'UCODE']).sum().reset_index()
        factor = data_mr.pivot(index='TDATE', columns='UCODE', values='MR')
        factor = factor - factor.shift(ts_n)
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = ts_pos_mat(
            factor=factor,
            # xs_q=quantile
        )
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions, fv100=False)


# n日净持仓变化
# 净头寸时序增加率排序
def xstsmr(start_date, price='CLOSE', loop=False, **kwargs):
    data_mr = kwargs['data_mr']
    data_mr['UCODE'] = data_mr['EXCHANGE'].apply(lambda x: str(x)) + data_mr['PCODE'].apply(lambda x: str(x))
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    quantile = kwargs['quantile']
    ts_n = kwargs['ts_n']
    index_name = 'xstsmr_d' + str(ts_n) + '_q' + str(quantile)
    start_index = get_index(calendar=calendar, date=start_date)
    if loop:

        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]
            data_mr_0 = data_mr[
                data_mr['TDATE'] == calendar[i - ts_n]
                ].groupby(by=['UCODE']).sum()[['MR']].reset_index()
            data_mr_t = data_mr[
                data_mr['TDATE'] == calendar[i]
                ].groupby(by=['UCODE']).sum()[['MR']].reset_index()

            data_mr_range = pd.merge(
                data_mr_0.rename(columns={'MR': 'MR0'}),
                data_mr_t.rename(columns={'MR': 'MR1'}),
                on='UCODE', how='left'
            )
            # data_mr_range['FACTORVALUE'] = data_mr_range['MR1'] - data_mr_range['MR0']
            data_mr_range['FACTORVALUE'] = (
                    data_mr_range[data_mr_range['MR0'] > 0]['MR1'] / data_mr_range[data_mr_range['MR0'] > 0]['MR0'] - 1
            )

            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
                price=price,
            )

            data_t = pd.merge(data_t, data_mr_range, on='UCODE', how='inner')
            data_t['FACTOR'] = index_name
            data_t = xs_pos(data=data_t, quantile=quantile)
            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:

        # matrix
        data_mr = data_mr.groupby(by=['TDATE', 'UCODE']).sum().reset_index()
        factor = data_mr.pivot(index='TDATE', columns='UCODE', values='MR')
        factor = factor / factor.shift(ts_n) - 1
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = xs_pos_mat(
            factor=factor,
            xs_q=quantile
        )
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions)


# n日净增减
# 净变化为正做多
def mrchg(start_date, price='CLOSE', loop=False, **kwargs):
    data_mr = kwargs['data_mr']
    data_mr['UCODE'] = data_mr['EXCHANGE'].apply(lambda x: str(x)) + data_mr['PCODE'].apply(lambda x: str(x))
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    index_name = 'mrchg_d' + str(ts_n)
    start_index = get_index(calendar=calendar, date=start_date)
    if loop:

        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]
            data_mr_t = data_mr[
                np.array(data_mr['TDATE'] >= calendar[i - ts_n])
                & np.array(data_mr['TDATE'] <= calendar[i])
                ].groupby(by=['UCODE']).sum()[['MRCHG']].reset_index()
            data_mr_range = data_mr_t

            data_mr_range['FACTORVALUE'] = data_mr_range['MRCHG']
            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
                price=price,
            )

            data_t = pd.merge(data_t, data_mr_range, on='UCODE', how='inner')
            data_t['FACTOR'] = index_name
            data_t = ts_pos(data=data_t)
            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:

        # matrix
        data_mr = data_mr.groupby(by=['TDATE', 'UCODE']).sum().reset_index()
        factor = data_mr.pivot(index='TDATE', columns='UCODE', values='MRCHG').rolling(ts_n).sum()
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = ts_pos_mat(
            factor=factor,
            # xs_q=quantile
        )
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions, fv100=False)


# n日净增减
# 净变化排序
def xsmrchg(start_date, price='CLOSE', loop=False, **kwargs):
    data_mr = kwargs['data_mr']
    data_mr['UCODE'] = data_mr['EXCHANGE'].apply(lambda x: str(x)) + data_mr['PCODE'].apply(lambda x: str(x))
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    quantile = kwargs['quantile']
    ts_n = kwargs['ts_n']
    index_name = 'xsmrchg_d' + str(ts_n) + '_q' + str(quantile)
    start_index = get_index(calendar=calendar, date=start_date)
    if loop:

        positions = pd.DataFrame()
        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]
            data_mr_t = data_mr[
                np.array(data_mr['TDATE'] >= calendar[i - ts_n])
                & np.array(data_mr['TDATE'] <= calendar[i])
                ].groupby(by=['UCODE']).sum()[['MRCHG']].reset_index()
            data_mr_range = data_mr_t

            data_mr_range['FACTORVALUE'] = data_mr_range['MRCHG']

            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
                price=price,
            )

            data_t = pd.merge(data_t, data_mr_range, on='UCODE', how='inner')
            data_t['FACTOR'] = index_name
            data_t = xs_pos(data=data_t, quantile=quantile)
            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:

        # matrix
        data_mr = data_mr.groupby(by=['TDATE', 'UCODE']).sum().reset_index()
        factor = data_mr.pivot(index='TDATE', columns='UCODE', values='MRCHG').rolling(ts_n).sum()
        factor0 = data.pivot(index='TDATE', columns='UCODE', values='POI').rolling(ts_n).sum()
        factor = factor / factor0
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = xs_pos_mat(
            factor=factor,
            xs_q=quantile
        )
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions)


# n日净增减
# 净变化比总变化排序
def xsmrchg2(start_date, price='CLOSE', **kwargs):
    data_mr = kwargs['data_mr']
    data_mr['UCODE'] = data_mr['EXCHANGE'].apply(lambda x: str(x)) + data_mr['PCODE'].apply(lambda x: str(x))
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    quantile = kwargs['quantile']
    ts_n = kwargs['ts_n']
    index_name = 'xsmrchg2_d' + str(ts_n) + '_q' + str(quantile)
    start_index = get_index(calendar=calendar, date=start_date)

    # matrix
    data_mr['MRCHGabs'] = data_mr['MRCHG'].abs()
    data_mr = data_mr.groupby(by=['TDATE', 'UCODE']).sum().reset_index()
    factor = data_mr.pivot(index='TDATE', columns='UCODE', values='MRCHG').rolling(ts_n).sum()
    factor1 = data_mr.pivot(index='TDATE', columns='UCODE', values='MRCHGabs').rolling(ts_n).sum()
    factor = factor / factor1
    factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
    pos, weights = xs_pos_mat(
        factor=factor,
        xs_q=quantile
    )
    data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
    positions = to_pos(
        data=data_m,
        factor=factor,
        pos=pos,
        weights=weights,
        price_liq=price_liq,
        index_name=index_name,
        start_date=calendar[start_index]
    )
    return pos_summary(positions=positions)


def tspoichg(start_date, price='CLOSE', loop=False, **kwargs):
    return tsmom(start_date=start_date, name='poichg', factor='POI', price=price, loop=loop, direction=-1, **kwargs)


def tspvolchg(start_date, price='CLOSE', loop=False, **kwargs):
    return tsmom(start_date=start_date, name='pvolchg', factor='PVOL', price=price, loop=loop, **kwargs)


def xspvolchg(start_date, price='CLOSE', loop=False, **kwargs):
    return xsmom(start_date=start_date, name='pvolchg', factor='PVOL', price=price, loop=loop, **kwargs)


def xspoichg(start_date, price='CLOSE', loop=False, **kwargs):
    return xsmom(start_date=start_date, name='poichg', factor='POI', price=price, loop=loop, **kwargs)


def xssigma(start_date, price='CLOSE', loop=False, **kwargs):
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    quantile = kwargs['quantile']

    index_name = 'xssigma_d' + str(ts_n) + '_q' + str(quantile)
    start_index = get_index(calendar=calendar, date=start_date)

    if loop:

        positions = pd.DataFrame()
        data_close = data.pivot(index='TDATE', columns='UCODE', values='CLOSE')
        data_vol = data.pivot(index='TDATE', columns='UCODE', values='VOL')
        data_sigma = data_close.pct_change().rolling(ts_n).std(ddof=1) * np.sqrt(240)

        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]

            ucode_vol = data_vol.columns[data_vol.loc[t_date, :] > kwargs['min_volume']].tolist()
            ucode_liq = data_vol.columns[
                data_vol.loc[calendar[i - max(liq_days, ts_n)], :] > kwargs['min_volume']
            ].tolist()
            ucode = list(set(ucode_liq).intersection(set(ucode_vol)))
            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
                # price=price_field,
            )
            data_t = data_t.merge(
                pd.DataFrame(data_sigma.loc[t_date, ucode]).rename(columns={t_date: 'FACTORVALUE'}).reset_index(),
                on='UCODE', how='inner'
            )

            data_t = xs_pos(data=data_t, quantile=quantile)

            data_t['FACTOR'] = index_name
            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:
        # matrix
        factor_raw = data.pivot(index='TDATE', columns='UCODE', values='CLOSE').pct_change()
        factor = factor_raw.rolling(ts_n).std(ddof=1)
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = xs_pos_mat(
            factor=factor,
            xs_q=quantile,
            # direction=-1
        )
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions)


def xsskew(start_date, price='CLOSE', loop=False, **kwargs):
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    quantile = kwargs['quantile']

    index_name = 'xsskew_d' + str(ts_n) + '_q' + str(quantile)
    start_index = get_index(calendar=calendar, date=start_date)
    if loop:

        positions = pd.DataFrame()

        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]
            lookback_date = calendar[i - ts_n]
            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
                # price=price_field,
            )
            data_lookback = data[
                np.array(data['TDATE'] >= lookback_date) & np.array(data['TDATE'] <= t_date)
            ][['TDATE', 'UCODE', 'CLOSE']]
            data_lookback_skew = data_lookback.pivot(index='TDATE', columns='UCODE', values='CLOSE').skew().reset_index()

            data_t = pd.merge(
                data_t,
                data_lookback_skew[['UCODE', 0]].rename(columns={0: 'FACTORVALUE'}),
                on='UCODE', how='left'
            )

            data_t = xs_pos(data=data_t, quantile=quantile)

            data_t['FACTOR'] = index_name
            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:
        # matrix
        factor_raw = data.pivot(index='TDATE', columns='UCODE', values='CLOSE').pct_change()
        factor = factor_raw.rolling(ts_n).skew()
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = xs_pos_mat(
            factor=factor,
            xs_q=quantile,
            # direction=-1
        )
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions)


def tsskew(start_date, price='CLOSE', loop=False, **kwargs):
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']

    index_name = 'tsskew_d' + str(ts_n)
    start_index = get_index(calendar=calendar, date=start_date)
    if loop:

        positions = pd.DataFrame()

        for i in range(start_index, len(calendar) - 1):
            t_date = calendar[i]
            lookback_date = calendar[i - ts_n]
            data_t = pre_loop(
                i=i,
                calendar=calendar,
                data=data,
                data_liq=price_liq,
                # price=price_field,
            )
            data_lookback = data[
                np.array(data['TDATE'] >= lookback_date) & np.array(data['TDATE'] <= t_date)
                ][['TDATE', 'UCODE', 'CLOSE']]
            data_lookback_skew = data_lookback.pivot(index='TDATE', columns='UCODE', values='CLOSE').skew().reset_index()

            data_t = pd.merge(
                data_t,
                data_lookback_skew[['UCODE', 0]].rename(columns={0: 'FACTORVALUE'}),
                on='UCODE', how='left'
            )
            data_t = ts_pos(data=data_t)

            data_t['FACTOR'] = index_name
            positions = pd.concat([positions, data_t])
            print(index_name + ', ' + t_date.strftime('%Y-%m-%d') + ', ' + str(sum(data_t['POS'] != 0)))
    else:
        # matrix
        factor_raw = data.pivot(index='TDATE', columns='UCODE', values='CLOSE').pct_change()
        factor = factor_raw.rolling(ts_n).skew()
        factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
        pos, weights = ts_pos_mat(
            factor=factor,
            # xs_q=quantile,
            # direction=-1
        )
        data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
        positions = to_pos(
            data=data_m,
            factor=factor,
            pos=pos,
            weights=weights,
            price_liq=price_liq,
            index_name=index_name,
            start_date=calendar[start_index]
        )
    return pos_summary(positions=positions)


def tssigmachg(start_date, price='CLOSE', **kwargs):
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    ts_n2 = kwargs['ts_n2']
    # quantile = kwargs['quantile']

    index_name = 'tssigmachg_d' + str(ts_n) #+ '_q' + str(quantile)
    start_index = get_index(calendar=calendar, date=start_date)

    # matrix
    factor_raw = data.pivot(index='TDATE', columns='UCODE', values='CLOSE').pct_change()
    factor = factor_raw.rolling(ts_n).std(ddof=1)
    factor = factor - factor.shift(ts_n2)
    factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
    pos, weights = ts_pos_mat(
        factor=factor,
        # xs_q=quantile,
        # direction=-1
    )
    data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
    positions = to_pos(
        data=data_m,
        factor=factor,
        pos=pos,
        weights=weights,
        price_liq=price_liq,
        index_name=index_name,
        start_date=calendar[start_index]
    )
    return pos_summary(positions=positions)


def xssigmachg(start_date, price='CLOSE', **kwargs):
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    ts_n2 = kwargs['ts_n2']
    quantile = kwargs['quantile']

    index_name = 'xssigmachg_d' + str(ts_n) + '_q' + str(quantile)
    start_index = get_index(calendar=calendar, date=start_date)

    # matrix
    factor_raw = data.pivot(index='TDATE', columns='UCODE', values='CLOSE').pct_change()
    factor = factor_raw.rolling(ts_n).std(ddof=1)
    factor = factor - factor.shift(ts_n2)
    factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
    pos, weights = xs_pos_mat(
        factor=factor,
        xs_q=quantile,
        # direction=-1
    )
    data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
    positions = to_pos(
        data=data_m,
        factor=factor,
        pos=pos,
        weights=weights,
        price_liq=price_liq,
        index_name=index_name,
        start_date=calendar[start_index]
    )
    return pos_summary(positions=positions)


def tsskewchg(start_date, price='CLOSE', **kwargs):
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    ts_n2 = kwargs['ts_n2']

    index_name = 'tsskew_d' + str(ts_n)
    start_index = get_index(calendar=calendar, date=start_date)

    # matrix
    factor_raw = data.pivot(index='TDATE', columns='UCODE', values='CLOSE').pct_change()
    factor = factor_raw.rolling(ts_n).skew()
    factor = factor - factor.shift(ts_n2)
    factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
    pos, weights = ts_pos_mat(
        factor=factor,
        # xs_q=quantile,
        # direction=-1
    )
    data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
    positions = to_pos(
        data=data_m,
        factor=factor,
        pos=pos,
        weights=weights,
        price_liq=price_liq,
        index_name=index_name,
        start_date=calendar[start_index]
    )
    return pos_summary(positions=positions)


def xsskewchg(start_date, price='CLOSE', **kwargs):
    data, liq_days, calendar, price_liq = pre_data(price, **kwargs)

    ts_n = kwargs['ts_n']
    ts_n2 = kwargs['ts_n2']
    quantile = kwargs['quantile']

    index_name = 'tsskew_d' + str(ts_n)
    start_index = get_index(calendar=calendar, date=start_date)

    # matrix
    factor_raw = data.pivot(index='TDATE', columns='UCODE', values='CLOSE').pct_change()
    factor = factor_raw.rolling(ts_n).skew()
    factor = factor - factor.shift(ts_n2)
    factor = factor[~price_liq.isna()].replace([np.inf, -np.inf], np.nan)
    pos, weights = xs_pos_mat(
        factor=factor,
        xs_q=quantile,
        # direction=-1
    )
    data_m = data.pivot(index='TDATE', columns='UCODE', values=price).shift(-1 if price in ['OPEN', 'SETTLE'] else 0)
    positions = to_pos(
        data=data_m,
        factor=factor,
        pos=pos,
        weights=weights,
        price_liq=price_liq,
        index_name=index_name,
        start_date=calendar[start_index]
    )
    return pos_summary(positions=positions)

