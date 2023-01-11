"""
雪球产品测算
"""
import hbshare as hbs
import pandas as pd
from hbshare.fe.common.util.data_loader import get_trading_day_list


def snow_ball_simulation(start_date, end_date, duration, knock_in_price, knock_out_price, mode="common"):
    """
    start_date: 回测起始时间
    end_date: 回测结束时间
    duration: 合约期限, 以日计算
    knock_in_price: 敲入价格
    knock_out_price: 敲出价格
    mode: common代表普通雪球, worst代表亏损有限型, step_down代表敲出下移型
    """
    sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                 "and JYRQ >= {} and JYRQ <= {}".format('000905', start_date, end_date)
    index_df = pd.DataFrame(hbs.db_data_query('readonly', sql_script, page_size=5000)['data'])
    index_series = index_df.set_index('TRADEDATE')['TCLOSE']
    # 每个交易日发一只雪球产品
    date_list = get_trading_day_list(start_date, end_date)

    res_df = pd.DataFrame(index=date_list[:-duration], columns=['c1', 'c2', 'c3', 'ko_time', 'lose_ratio'])

    if mode in ["common", "worst"]:
        for i in range(len(date_list) - duration):
            start_dt, end_dt = date_list[i], date_list[i + duration]
            period_data = index_series.loc[start_dt: end_dt]
            period_data = period_data / period_data.iloc[0]
            ko_date = period_data.index.tolist()[::20][3:]

            if period_data.loc[ko_date].gt(knock_out_price).sum() > 0:  # 情形1：敲出获利:
                tmp = period_data.loc[ko_date].to_frame('nav')
                tmp.loc[tmp['nav'] > knock_out_price, 'sign'] = 1
                ko_time = tmp.index.to_list().index(tmp['sign'].first_valid_index()) + 3
                res_df.loc[start_dt, 'c1'] = 1
                res_df.loc[start_dt, 'ko_time'] = ko_time
            elif period_data[1:].min() >= knock_in_price:  # 情形2：既未敲出也未敲入
                res_df.loc[start_dt, 'c2'] = 1
            else:
                res_df.loc[start_dt, 'c3'] = 1
                lose_ratio = \
                    max(0,
                        (period_data.loc[start_dt] - period_data.loc[end_dt]) / period_data.loc[start_dt])
                res_df.loc[start_dt, 'lose_ratio'] = lose_ratio * (-1)
    else:
        price_list = [1.03 - 0.015 * i for i in range(10)]
        for i in range(len(date_list) - duration):
            start_dt, end_dt = date_list[i], date_list[i + duration]
            period_data = index_series.loc[start_dt: end_dt]
            period_data = period_data / period_data.iloc[0]
            ko_date = period_data.index.tolist()[::20][3:]

            price_series = pd.Series(index=ko_date, data=price_list)
            compare_df = period_data.loc[ko_date].to_frame('price').merge(
                price_series.to_frame('ko_price'), left_index=True, right_index=True)
            compare_df.loc[compare_df['price'] > compare_df['ko_price'], 'sign'] = 1.

            if compare_df['sign'].gt(0).sum() > 0:  # 情形1：敲出获利:
                ko_time = compare_df.index.to_list().index(compare_df['sign'].first_valid_index()) + 3
                res_df.loc[start_dt, 'c1'] = 1
                res_df.loc[start_dt, 'ko_time'] = ko_time
            elif period_data[1:].min() >= knock_in_price:  # 情形2：既未敲出也未敲入
                res_df.loc[start_dt, 'c2'] = 1
            else:
                res_df.loc[start_dt, 'c3'] = 1
                lose_ratio = \
                    max(0,
                        (period_data.loc[start_dt] - period_data.loc[end_dt]) / period_data.loc[start_dt])
                res_df.loc[start_dt, 'lose_ratio'] = lose_ratio * (-1)

    if mode == "worst":
        tmp = res_df[res_df['lose_ratio'] < knock_in_price - 1]
        ratio = tmp.shape[0] / res_df.shape[0]
        print("尾部风险概率: {}".format(format(ratio, '.2%')))
        res_df.loc[res_df['lose_ratio'] < knock_in_price - 1, 'lose_ratio'] = knock_in_price - 1
    print("各情景比例: c1: {}, c2: {}, c3: {}".format(
        format(res_df['c1'].sum() / res_df.shape[0], '.2%'), format(res_df['c2'].sum() / res_df.shape[0], '.2%'),
        format(res_df['c3'].sum() / res_df.shape[0], '.2%')))
    print("平均敲出时间(月): {}".format(round(res_df['ko_time'].mean(), 2)))
    print("平均亏损比例: {}".format(format(res_df['lose_ratio'].mean(), '.2%')))

    return res_df


if __name__ == '__main__':
    snow_ball_simulation('20100101', '20220930', 240, 0.8, 1.0, "step_down")
