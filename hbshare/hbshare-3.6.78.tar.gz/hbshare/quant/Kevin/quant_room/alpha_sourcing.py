"""
alpha标的sourcing
"""
import hbshare as hbs
import pandas as pd
import numpy as np
from tqdm import tqdm
import Levenshtein
from hbshare.quant.Kevin.quant_room.MyUtil.data_loader import get_fund_nav_from_sql, get_trading_day_list
from Arbitrage_backtest import cal_annual_return, cal_annual_volatility, cal_sharpe_ratio, cal_max_drawdown
import jieba
import jieba.posseg as pseg
import numpy as np
from sklearn.cluster import KMeans
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import Birch
import matplotlib.pyplot as plt

plt.style.use('seaborn')


## 统计数量
# sql_script = "SELECT count(*) FROM st_hedge.t_st_jjxx"
# data = pd.DataFrame(hbs.db_data_query('highuser', sql_script)['data'])
# print(data)


class AlphaSourcing:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def _get_fund_info(self):
        sql_script = \
            "SELECT clrq, jjdm, jjmc, jjjc FROM st_hedge.t_st_jjxx where cpfl = '4' and ejfl = '1002' and jjzt = '0'"
        data = pd.DataFrame(hbs.db_data_query('highuser', sql_script, page_size=50000)['data'])
        # 剔除300
        data = data[~data['jjmc'].str.contains('300')]
        # 剔除1000
        data = data[~data['jjmc'].str.contains('1000')]
        # 剔除中性
        data = data[~data['jjmc'].str.contains('对冲')]
        data = data[~data['jjmc'].str.contains('中性')]
        # 成立满一年
        data = data[data['clrq'] < self.start_date]

        fund_dict = data.set_index('jjmc')['jjdm'].to_dict()

        return fund_dict

    @staticmethod
    def _get_fund_nav_from_sql(start_date, end_date, fund_dict):
        """
        获取db的私募基金净值数据
        """
        nav_series_list = []
        for name, fund_id in tqdm(fund_dict.items()):
            sql_script = "SELECT a.jjdm fund_id, b.jzrq TRADEDATE, b.fqdwjz as ADJ_NAV from " \
                         "st_hedge.t_st_jjxx a, st_hedge.t_st_rhb b where a.cpfl = '4' and a.jjdm = b.jjdm " \
                         "and a.jjzt not in ('3') " \
                         "and a.jjdm = '{}' and b.jzrq >= {} and b.jzrq <= {} " \
                         "order by b.jzrq".format(fund_id, start_date, end_date)
            res = hbs.db_data_query("highuser", sql_script, page_size=5000)
            if len(res['data']) != 0:
                data = pd.DataFrame(res['data']).set_index('TRADEDATE')['ADJ_NAV']
                data.name = name
                nav_series_list.append(data)
            else:
                pass
        df = pd.concat(nav_series_list, axis=1).sort_index()

        return df

    @staticmethod
    def lev_metric(x, y):
        distance = Levenshtein.distance(x, y)
        return 1 - distance / (len(x) + len(y))

    def run(self):
        fund_dict = self._get_fund_info()
        nav_df = self._get_fund_nav_from_sql(self.start_date, self.end_date, fund_dict)
        trading_day_list = get_trading_day_list(self.start_date, self.end_date, frequency="week")
        trading_day_list = [x for x in trading_day_list if x != "20210930"]
        nav_df = nav_df.reindex(trading_day_list)
        # 数据缺失剔除
        count_df = nav_df.isnull().sum()
        selected_list = count_df[count_df <= 3].index.tolist()
        nav_df = nav_df[selected_list]
        # 均值填充
        return_df = nav_df.pct_change(limit=1)
        return_df.iloc[0] = 0.
        return_df = return_df.T
        return_df = return_df.fillna(return_df.mean()).T
        nav_df = (1 + return_df).cumprod()
        # 跟踪误差校验：10%为界
        sql_script = "SELECT JYRQ as TRADEDATE, ZQDM, SPJG as TCLOSE from funddb.ZSJY WHERE" \
                     " ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format("000905", self.start_date, self.end_date)
        res = hbs.db_data_query('readonly', sql_script, page_size=5000)
        data = pd.DataFrame(res['data'])
        benchmark_series = data.set_index('TRADEDATE')['TCLOSE'].reindex(trading_day_list)
        return_df = nav_df.pct_change().dropna().sub(benchmark_series.pct_change().dropna(), axis=0).sort_index()
        annual_vol = return_df.std() * np.sqrt(52)
        vol_list = annual_vol[annual_vol < 0.15].index.tolist()  # 以幻方为界
        return_df = return_df[vol_list]
        excess_df = (1 + return_df).cumprod()
        # 剔除区间内超额的标的
        period_excess = excess_df.iloc[-1] / excess_df.iloc[0] - 1
        selected_list = period_excess[period_excess >= 0.05].index.tolist()
        excess_df = excess_df[selected_list]
        "========================================================================================================"
        # 文本聚类
        stop_words = ['私募', '基金', '证券', '投资', '集合', '资金', '计划', '号', '期', '\n']+[str(i) for i in range(1, 500)]
        jieba.add_word("中证500")
        jieba.add_word("500指数")
        title_list = excess_df.columns.tolist()
        corpus = [" ".join([w for w in jieba.lcut(str(x)) if w not in stop_words]) for x in title_list]
        # title_dict = {idx: title for idx, title in enumerate(title_list)}
        #将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
        vectorizer = CountVectorizer()
        #该类会统计每个词语的tf-idf权值
        transformer = TfidfTransformer()
        #第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
        tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
        #获取词袋模型中的所有词语
        # word = vectorizer.get_feature_names()
        #将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
        weight = tfidf.toarray()

        print('start cluster Birch -------------------')
        cluster = Birch(threshold=0.3, n_clusters=None)
        cluster.fit_predict(weight)

        # cluster_dict = {}
        # # cluster_dict key为Birch聚类后的每个类，value为 title对应的index
        # for index, value in enumerate(cluster.labels_):
        #     if value not in cluster_dict:
        #         cluster_dict[value] = [index]
        #     else:
        #         cluster_dict[value].append(index)
        # print(cluster_dict)

        label_df = pd.DataFrame({"fund_name": title_list, "label": cluster.labels_}).sort_values(by='label')
        distinct_list = label_df.drop_duplicates(subset='label', keep='first')['fund_name'].tolist()
        distinct_return_df = return_df[distinct_list]

        "==================================================================================================="
        dis_nav_df = (1 + distinct_return_df).cumprod()

        # 净值指标
        performance_df = pd.DataFrame(
            index=distinct_return_df.columns, columns=['超额年化收益', '超额年化波动', '最大回撤', 'Sharpe', '区间收益9-2', '今年以来超额'])
        performance_df.loc[:, '超额年化收益'] = distinct_return_df.apply(cal_annual_return, axis=0)
        performance_df.loc[:, '超额年化波动'] = distinct_return_df.apply(cal_annual_volatility, axis=0)
        performance_df.loc[:, '最大回撤'] = dis_nav_df.apply(cal_max_drawdown, axis=0)
        performance_df.loc[:, 'Sharpe'] = distinct_return_df.apply(lambda x: cal_sharpe_ratio(x, 0.015), axis=0)
        performance_df.loc[:, '区间收益9-2'] = dis_nav_df.loc["20220211"] / dis_nav_df.loc["20210903"] - 1
        performance_df.loc[:, '今年以来超额'] = dis_nav_df.iloc[-1] / dis_nav_df.loc["20211231"] - 1

        # 超额稳定性聚类
        kmeans = KMeans(n_clusters=2)
        df = performance_df[['最大回撤', 'Sharpe', '区间收益9-2']]
        result = kmeans.fit(df)
        df['label'] = result.labels_

        # cluster_center = pd.DataFrame(columns=['最大回撤', 'Sharpe', '区间收益9-2'], data=result.cluster_centers_)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection="3d")
        ax.scatter(df[df['label'] == 1]['最大回撤'],
                   df[df['label'] == 1]['区间收益9-2'],
                   df[df['label'] == 1]['Sharpe'], c='r')
        ax.scatter(df[df['label'] == 0]['最大回撤'],
                   df[df['label'] == 0]['区间收益9-2'],
                   df[df['label'] == 0]['Sharpe'], c='g')
        ax.set_xlabel('max_drawdown')
        ax.set_ylabel('9-2_period_ret')
        ax.set_zlabel('Sharpe')

        stable_list = df[df['label'] == 1].index.tolist()
        unstable_list = df[df['label'] == 0].index.tolist()
        (1 + distinct_return_df[stable_list].mean(axis=1)).cumprod().to_clipboard()
        (1 + distinct_return_df[unstable_list].mean(axis=1)).cumprod().to_clipboard()


if __name__ == '__main__':
    s_date = '20210827'
    e_date = '20220916'

    AlphaSourcing(s_date, e_date).run()