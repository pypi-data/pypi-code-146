"""
市值指数
"""
import pandas as pd
import numpy as np
import hbshare as hbs
import os
from tqdm import tqdm
from hbshare.fe.common.util.data_loader import get_trading_day_list
from hbshare.fe.common.util.config import style_name, industry_name
from hbshare.fe.common.util.config import factor_map_dict


class CapIndex:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def get_mkt_info(start_date, end_date):
        path = r'D:\kevin\risk_model_jy\RiskModel\data\common_data\chg_pct'
        listdir = os.listdir(path)
        listdir = [x for x in listdir if start_date <= x.split('.')[0] <= end_date]
        data = []
        for filename in listdir:
            date_t_rate = pd.read_csv(os.path.join(path, filename), dtype={"tradeDate": str})
            date_t_rate['ticker'] = date_t_rate['ticker'].apply(lambda x: str(x).zfill(6))
            data.append(date_t_rate)

        data = pd.concat(data)
        # filter
        data = data[(data['dailyReturnReinv'] >= -0.2) & (data['dailyReturnReinv'] <= 0.2)]
        data = pd.pivot_table(data, index='tradeDate', columns='ticker', values='dailyReturnReinv').sort_index()
        data = data.dropna(how='any', axis=1)

        return data

    @staticmethod
    def _load_benchmark_components(date):
        sql_script = "SELECT * FROM hsjy_gg.SecuMain where SecuCategory = 4 and " \
                     "SecuCode in ('000300', '000905', '000852', '000985')"
        res = hbs.db_data_query('readonly', sql_script)
        index_info = pd.DataFrame(res['data'])
        inner_code_series = index_info.set_index('SECUCODE')['INNERCODE']

        weight = []
        for benchmark_id in ['000300', '000905', '000852', '000985']:
            inner_code = inner_code_series.loc[benchmark_id]
            sql_script = "SELECT (select a.SecuCode from hsjy_gg.SecuMain a where a.InnerCode = b.InnerCode and " \
                         "rownum = 1) SecuCode, b.EndDate, b.Weight FROM hsjy_gg.LC_IndexComponentsWeight b WHERE " \
                         "b.IndexCode = '{}' and b.EndDate = to_date('{}', 'yyyymmdd')".format(inner_code, date)
            data = pd.DataFrame(hbs.db_data_query('readonly', sql_script, page_size=5000)['data'])
            weight_df = data.rename(
                columns={"SECUCODE": "ticker", "ENDDATE": "effDate", "WEIGHT": "weight"})
            weight_df['benchmark_id'] = benchmark_id
            weight.append(weight_df[['ticker', 'benchmark_id']])

        return pd.concat(weight)

    @staticmethod
    def _load_style_exposure(date):
        sql_script = "SELECT * FROM st_ashare.r_st_barra_style_factor where TRADE_DATE = '{}'".format(date)
        res = hbs.db_data_query('alluser', sql_script, page_size=5000)
        exposure_df = pd.DataFrame(res['data']).set_index('ticker')
        ind_names = [x.lower() for x in industry_name['sw'].values()]
        exposure_df = exposure_df[style_name + ind_names]

        return exposure_df

    def calculate_cap_index(self):
        month_list = get_trading_day_list(self.start_date, self.end_date, frequency="month")
        month_list.append(self.end_date)
        reverse_ind = dict([(value.lower(), key) for (key, value) in industry_name['sw'].items()])
        ret_list = []
        style_dict = {}
        industry_dict = {}
        ret_attr = {}
        for i in tqdm(range(1, len(month_list))):
            p_date, t_date = month_list[i - 1], month_list[i]
            period_data = self.get_mkt_info(p_date, t_date).fillna(0.)
            bm_components = self._load_benchmark_components(p_date)
            mkv_info = pd.read_json(
                r'D:\kevin\risk_model_jy\RiskModel\data\common_data/market_value/%s.json' % p_date,
                dtype={'ticker': str})
            mkv_info = mkv_info[(mkv_info['ticker'].str[0].isin(['0', '3', '6']))].set_index(
                'ticker')[['marketValue', 'negMarketValue']]
            style_exposure_df = self._load_style_exposure(p_date)

            idx = set(period_data.columns).intersection(set(bm_components['ticker'].unique())).intersection(
                set(mkv_info.index)).intersection(set(style_exposure_df.index))
            # 指数收益
            period_data = period_data.T.reindex(idx).T
            mkv_info = mkv_info.reindex(idx)
            bm_components = bm_components.merge(mkv_info, left_on='ticker', right_index=True).sort_values(
                by=['ticker', 'benchmark_id']).drop_duplicates(subset=['ticker'], keep='first')
            # tmp = bm_components
            bm_components = pd.pivot_table(
                bm_components, index='ticker', columns='benchmark_id', values='negMarketValue').fillna(0.) / 1e+9
            bm_components = (bm_components / bm_components.sum()).reindex(idx)
            index_ret = (1 + period_data).cumprod().dot(bm_components).pct_change().dropna()
            ret_list.append(index_ret)
            # 指数风格
            # style_exposure_df = style_exposure_df.reindex(idx)
            # index_style = bm_components.T.dot(style_exposure_df.astype(float)).T
            #
            # style_df = index_style.loc[style_name]
            # style_df.index = style_df.index.map(factor_map_dict)
            # benchmark_id_map = {"000300": "沪深300", "000905": "中证500", "000852": "中证1000", "000985": "剩余小票"}
            # style_df = style_df.rename(columns=benchmark_id_map)
            # style_dict[p_date] = style_df
            #
            # ind_df = index_style[10:]
            # ind_df.index = [reverse_ind[x] for x in ind_df.index]
            # ind_df = ind_df.rename(columns=benchmark_id_map)
            # industry_dict[p_date] = ind_df
            # # 风格拆解： 风格 + 行业
            # sql_script = "SELECT * FROM st_ashare.r_st_barra_factor_return where " \
            #              "TRADE_DATE > '{}' and TRADE_DATE <= {}".format(p_date, t_date)
            # res = hbs.db_data_query('alluser', sql_script, page_size=5000)
            # factor_return = pd.DataFrame(res['data'])
            # factor_return = pd.pivot_table(
            #     factor_return, index='trade_date', columns='factor_name', values='factor_ret').sort_index()
            # factor_return = (1 + factor_return).prod() - 1
            # factor_return.index = factor_return.index.str.lower()
            # index_style.loc["country"] = 1.
            #
            # idx = set(factor_return.index).intersection(set(index_style.index))
            #
            # f_ret = index_style.reindex(idx).mul(np.array(factor_return.reindex(idx)).reshape(-1, 1))
            # f_ret.loc['spec'] = (1 + index_ret).prod() - 1 - f_ret.sum()
            #
            # ret_attr[t_date] = f_ret

            # mkv_des = tmp.groupby('benchmark_id')['marketValue'].describe()

        ret_df = pd.concat(ret_list).sort_index()
        ret_df.loc[self.start_date] = 0.
        ret_df = ret_df.sort_index()

        # 风格归因的累计
        attr_list = []
        for date in sorted(ret_attr.keys()):
            tmp = ret_attr[date].copy()
            tmp['factor'] = tmp.index
            tmp['trade_date'] = date
            tmp.reset_index(drop=True, inplace=True)
            attr_list.append(tmp)

        attr_df = pd.concat(attr_list)

        # 沪深300的拆解
        sub_attr = []
        for col in ['000300', '000905', '000852', '000985']:
            sub_df = pd.pivot_table(attr_df, index='trade_date', columns='factor', values=col).sort_index()
            index_return = sub_df.sum(axis=1)
            kt = np.log(1 + index_return) / index_return
            r = (1 + index_return).prod() - 1
            k = np.log(1 + r) / r
            cum_attr = sub_df.T.multiply(kt / k).sum(axis=1).to_frame(col)
            sub_attr.append(cum_attr)

        sub_attr = pd.concat(sub_attr, axis=1)
        sub_attr_style = sub_attr.loc[style_name]
        sub_attr_style.index = sub_attr_style.index.map(factor_map_dict)
        ind_name = [x for x in sub_attr.index.tolist() if x not in style_name]
        ind_name = [x for x in ind_name if x not in ['spec', 'country']]
        sub_attr_style.loc['行业'] = sub_attr.loc[ind_name].sum()
        sub_attr_style.loc['国家因子'] = sub_attr.loc['country']
        sub_attr_style.loc['特质性收益'] = sub_attr.loc['spec']

        sub_attr_ind = sub_attr.loc[ind_name]
        sub_attr_ind.index = [reverse_ind[x] for x in sub_attr_ind.index]

        return ret_df


if __name__ == '__main__':
    # CapIndex('20150101', '20221118').calculate_cap_index()
    CapIndex('20211231', '20221130').calculate_cap_index()