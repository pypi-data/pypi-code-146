"""
alpha收益弹性的计算模块
"""
import numpy as np
import pandas as pd
import os
import hbshare as hbs
from datetime import datetime
from hbshare.quant.Kevin.quant_room.MyUtil.data_loader import get_trading_day_list
from Arbitrage_backtest import cal_annual_return


class AlphaElasticity:
    def __init__(self, data_path, end_date, start_date='20161230'):
        self.data_path = data_path
        self.end_date = end_date
        self.start_date = start_date

    def run(self):
        data_with_header = pd.read_excel(
            os.path.join(self.data_path, r"指增-{}.xlsx".format(self.end_date)), sheet_name='原始净值')
        data = pd.read_excel(
            os.path.join(self.data_path, "指增-{}.xlsx".format(self.end_date)), sheet_name='原始净值', header=1)
        data['t_date'] = data['t_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        data.index = data['t_date']
        cols = data_with_header.columns.tolist()

        # fix start date

        trading_day_list = get_trading_day_list(self.start_date, self.end_date, frequency="week")

        data_param = []
        type_list = [x for x in cols if not x.startswith('Unnamed')]
        for i in range(len(type_list) - 1):
            if type_list[i] in ['量价（500）', '机器学习', '基本面']:
                s_index, e_index = cols.index(type_list[i]), cols.index(type_list[i + 1])
                data_slice = data[data.columns[s_index: e_index]]
                data_slice = data_slice[data_slice.index >= self.start_date].reindex(trading_day_list)
                data_param.append(data_slice)
            else:
                pass

        nav_df = pd.concat(data_param, axis=1).dropna(how='all', axis=0).sort_index()

        # 卓识的先手动入
        nav_zs = pd.read_excel("D:\\卓识伟业净值\\卓识伟业_20221028.xlsx", sheet_name=0)[
            ['日期', '复权净值归一']].dropna()
        nav_zs['日期'] = nav_zs['日期'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        nav_zs.rename(columns={"日期": "TRADEDATE", "复权净值归一": "卓识伟业"}, inplace=True)
        nav_zs = nav_zs.set_index('TRADEDATE')['卓识伟业']
        del nav_df['卓识伟业']
        nav_df = nav_df.merge(nav_zs, left_index=True, right_index=True, how='left')

        sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format('000905', self.start_date, self.end_date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script, page_size=5000)['data'])
        index_df = data.set_index('TRADEDATE').reindex(trading_day_list)[['TCLOSE']]
        index_df.rename(columns={"TCLOSE": "benchmark"}, inplace=True)

        assert (nav_df.shape[0] == index_df.shape[0])

        # 微调
        nav_df.loc[: '20211231', '白鹭精选量化鲲鹏十号'] = np.NAN

        excess_return = nav_df.pct_change().sub(index_df.pct_change()['benchmark'].squeeze(), axis=0)
        mean_excess = excess_return.mean(axis=1).dropna().to_frame('mean_excess')

        threshold = 0.002
        mean_excess.loc[mean_excess['mean_excess'] > threshold, 'alpha_env'] = "up"
        mean_excess.loc[mean_excess['mean_excess'] <= -threshold, 'alpha_env'] = "down"
        mean_excess['alpha_env'] = mean_excess['alpha_env'].fillna('shake')
        mean_excess = mean_excess[mean_excess['alpha_env'] != 'shake']

        df = pd.merge(excess_return[1:], mean_excess, left_index=True, right_index=True)

        ret_list = []
        for col in df.columns[:-1]:
            tmp = df[[col, 'alpha_env']].dropna()
            counts = df['alpha_env'].value_counts()
            if (counts.loc['up'] <= 5) or (counts.loc['down'] <= 5):
                continue

            res = tmp.groupby('alpha_env').apply(cal_annual_return)
            ret_list.append(res)

        ret_df = pd.concat(ret_list, axis=1).T.sort_values(by='up')

        include_list = [
            '启林中证500指数增强1号',
            '诚奇中证500增强精选1期',
            '九坤日享中证500指数增强1号',
            '天演中证500指数增强',
            '星阔广厦1号中证500指数增强',
            '明汯价值成长1期3号',
            '世纪前沿指数增强2号',
            '九章幻方中证500量化进取1号',
            '黑翼中证500指数增强1号',
            '衍复指增三号',
            '卓识伟业',

            '量锐7号',
            '赫富500指数增强一号',
            '量派500增强8号A',
            '凡二英火5号',
            '希格斯水手2号',
            '伯兄建康',
            '因诺聚配中证500指数增强',
            '乾象中证500指数增强1号B',
            '宽德金选中证500指数增强6号',
            '概率500指增1号',
            '白鹭精选量化鲲鹏十号',
            '顽岩中证500指数增强1号'
        ]

        # df = pd.merge(excess_return[include_list], mean_excess, left_index=True, right_index=True).dropna()
        # res = df.groupby('alpha_env').apply(cal_annual_return).T.reindex(include_list)

        res = (ret_df.rank() / ret_df.shape[0]).loc[include_list]

        return res


if __name__ == '__main__':
    AlphaElasticity("D:\\量化产品跟踪\\指数增强", '20221028').run()