"""
Alpha标的表现统计
"""
import os
import pandas as pd
import hbshare as hbs
import datetime
import plotly
from plotly.offline import plot as plot_ly
import plotly.graph_objs as go

plotly.offline.init_notebook_mode(connected=True)


alpha_dict = {
    "hs300": {
        "明汯稳健增长2期1号": "SK5676",
        "幻方300指数增强欣享一号": "SNL044",
        "星阔春山一号": "SQF231"
    },
    "zz500": {
        "启林": "SGY379",
        "诚奇": "SLS817",
        "幻方": "SEC185",
        "九坤": "ST9804",
        "明汯": "SEE194",
        "天演": "P20830",
        "星阔": "SNU706",
        "卓识": "SGA015",
        "衍复": "SJH866",
        "黑翼": "SEM323",
        "世纪前沿": "SGP682",
        "乾象": "P48470",
        "宽德": "SJF555",
        "因诺": "SGX346",
        "伯兄": "SQT564",
        "概率": "SQT076",
        "赫富": "SEP463",
        "量锐": "SGR954",
        "量派": "SNJ513",
        "茂源": "SJM016",
        "希格斯": "SLE315",
        "白鹭": "SQB109",
        "朋锦仲阳": "SGN254",
        "衍合": "SLG867",
        "弈倍": "SY0096"},
    "zz1000": {
        "启林": "SSU078",
        "明汯": "SGG585",
        "凡二": "SSC067",
        "衍复": "SJM688",
        "概率": "SQQ803",
        "星阔": "SQF225"
    },
    "all_market": {
        "明汯": "SSL078",
        "天演": "P22984",
        "诚奇": "SSU249",
        "星阔": "SSE288"
    },
    "market_neutral": {
        "明汯中性7号1期": "SEL756",
        "天演广全": "SLC213",
        "诚奇睿盈对冲尊享1号": "SNR622",
        "赫富对冲四号": "SEW735",
        "星阔云起1号": "SNU704",
        "茂源巴舍里耶2期": "SCV226",
        "伯兄卢比孔": "SL3246",
        "概率一号": "SNM976"
    },
    "cb": {"悬铃C号": "SEK201",
           "百奕传家一号": "SJS027",
           "艾方可转债1号": "SCK025",
           "安值福慧量化1号": "SCP765"}
}


class AlphaPerformance:
    def __init__(self, start_date, pre_date, end_date, fund_info_dict):
        self.start_date = start_date
        self.pre_date = pre_date
        self.end_date = end_date
        self.fund_info_dict = fund_info_dict
        self._load_data()

    def _load_calendar(self):
        sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            self.start_date, self.end_date)
        res = hbs.db_data_query('readonly', sql_script, page_size=5000)
        df = pd.DataFrame(res['data']).rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                     "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

        self.calendar_df = df[['calendarDate', 'isOpen', 'isWeekEnd', 'isMonthEnd']]

        trading_day_list = df[df['isWeekEnd'] == 1]['calendarDate'].tolist()

        return trading_day_list

    def _load_data(self):
        nav_series_dict = dict()

        for strategy_type, id_dict in self.fund_info_dict.items():
            nav_list = []
            for fund_name, fund_id in id_dict.items():
                sql_script = "SELECT a.jjdm fund_id, b.jzrq TRADEDATE, b.fqdwjz as ADJ_NAV from " \
                             "st_hedge.t_st_jjxx a, st_hedge.t_st_rhb b where a.cpfl = '4' and a.jjdm = b.jjdm " \
                             "and a.jjzt not in ('3') " \
                             "and a.jjdm = '{}' and b.jzrq >= {} and b.jzrq <= {} " \
                             "order by b.jzrq".format(fund_id, self.start_date, self.end_date)
                res = hbs.db_data_query("highuser", sql_script, page_size=5000)
                data = pd.DataFrame(res['data']).set_index('TRADEDATE')['ADJ_NAV']
                data.name = fund_name
                nav_list.append(data)

            nav_df = pd.concat(nav_list, axis=1)
            nav_series_dict[strategy_type] = nav_df.sort_index()

        self.nav_series_dict = nav_series_dict

    @staticmethod
    def _load_benchmark(benchmark_id, start_date, end_date):
        sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format(benchmark_id, start_date, end_date)
        res = hbs.db_data_query('readonly', sql_script)
        data = pd.DataFrame(res['data']).rename(columns={"TCLOSE": "benchmark"}).set_index('TRADEDATE')[['benchmark']]

        return data

    @staticmethod
    def plotly_line(df, title_text, sava_path, figsize=(1200, 500)):
        fig_width, fig_height = figsize
        data = []
        for col in df.columns:
            trace = go.Scatter(
                x=df.index.tolist(),
                y=df[col],
                name=col,
                mode="lines"
            )
            data.append(trace)

        # date_list = df.index.tolist()
        # tick_vals = [i for i in range(0, len(df), 4)]
        # tick_text = [date_list[i] for i in range(0, len(df), 4)]

        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height,
            yaxis=dict(tickfont=dict(size=12), showgrid=True),
            # xaxis=dict(showgrid=True, tickvals=tick_vals, ticktext=tick_text),
            xaxis=dict(showgrid=True),
            template='plotly_white'
        )
        fig = go.Figure(data=data, layout=layout)

        plot_ly(fig, filename=sava_path, auto_open=False)

    def get_construct_result(self):
        trading_day_list = self._load_calendar()

        nan_excel = pd.DataFrame()
        file = os.path.join("D:\\量化产品跟踪\\代销及FOF标的", r"AlphaPerf_{}.xlsx".format(self.end_date))
        nan_excel.to_excel(file)
        writer = pd.ExcelWriter(file)

        # 300指增
        # nav_df = self.nav_series_dict['hs300'].reindex(trading_day_list).dropna(how='all')
        # return_df = nav_df.fillna(method='ffill').pct_change().fillna(0.)
        # benchmark_series = self._load_benchmark('000300', self.start_date, self.end_date).reindex(
        #     trading_day_list).pct_change().fillna(0.)
        # return_df = return_df.sub(benchmark_series['benchmark'], axis=0)
        # 500指增
        nav_df = self.nav_series_dict['zz500'].reindex(trading_day_list).dropna(how='all')
        # 月末日期
        tmp = pd.DataFrame({"trade_date": nav_df.index})
        tmp['month'] = tmp['trade_date'].apply(lambda x: datetime.datetime.strptime(x, '%Y%m%d').month)
        tmp['next_month'] = tmp['month'].shift(-1).fillna(0.).astype(int)
        tmp = tmp[tmp['month'] != tmp['next_month']]
        month_end = tmp['trade_date'].tolist()

        benchmark_series = self._load_benchmark('000905', self.start_date, self.end_date).reindex(
            trading_day_list).pct_change().fillna(0.)
        return_df = nav_df.fillna(method='ffill').pct_change().fillna(0.)
        return_df = return_df.sub(benchmark_series['benchmark'], axis=0)
        # 月度超额收益
        month_excess = (1 + return_df).cumprod().reindex(month_end).pct_change().dropna().sort_index().T
        month_excess.columns = [x[:6] for x in month_excess.columns]
        month_excess.to_excel(writer, sheet_name="500指增月度超额")
        # 当月超额
        week_excess = return_df[return_df.index > self.pre_date].sort_index().T
        week_excess.to_excel(writer, sheet_name="500指增当月周度超额")

        # 1000指增
        nav_df = self.nav_series_dict['zz1000'].reindex(trading_day_list).dropna(how='all')
        benchmark_series = self._load_benchmark('000852', self.start_date, self.end_date).reindex(
            trading_day_list).pct_change().fillna(0.)
        return_df = nav_df.fillna(method='ffill').pct_change().fillna(0.)
        return_df = return_df.sub(benchmark_series['benchmark'], axis=0)
        # 月度超额收益
        month_excess = (1 + return_df).cumprod().reindex(month_end).pct_change().dropna().sort_index().T
        month_excess.columns = [x[:6] for x in month_excess.columns]
        month_excess.to_excel(writer, sheet_name="1000指增月度超额")
        # 当月超额
        week_excess = return_df[return_df.index > self.pre_date].sort_index().T
        week_excess.to_excel(writer, sheet_name="1000指增当月周度超额")

        # 全市场选股
        nav_df = self.nav_series_dict['all_market'].reindex(trading_day_list).dropna(how='all')
        benchmark_series = self._load_benchmark('000985', self.start_date, self.end_date).reindex(
            trading_day_list).pct_change().fillna(0.)
        return_df = nav_df.fillna(method='ffill').pct_change().fillna(0.)
        return_df = return_df.sub(benchmark_series['benchmark'], axis=0)
        return_df = return_df[return_df.index >= '20211231']  # 全市场从22年开始看
        # 月度超额收益
        month_excess = (1 + return_df).cumprod().reindex(month_end).pct_change().dropna().sort_index().T
        month_excess.columns = [x[:6] for x in month_excess.columns]
        month_excess.to_excel(writer, sheet_name="全市场选股月度超额")
        # 当月超额
        week_excess = return_df[return_df.index > self.pre_date].sort_index().T
        week_excess.to_excel(writer, sheet_name="全市场选股当月周度超额")

        # 市场中性
        # nav_df = self.nav_series_dict['market_neutral'].reindex(trading_day_list).dropna(how='all')
        # return_df = nav_df.fillna(method='ffill').pct_change().fillna(0.)
        # adj_nav_df = (1 + return_df).cumprod()
        # self.plotly_line(
        #     adj_nav_df, "市场中性产品走势图", "D:\\量化产品跟踪\\代销及FOF标的\\市场中性走势.html", figsize=(1200, 600))
        # 可转债
        # nav_df = self.nav_series_dict['cb'].reindex(trading_day_list).dropna(how='all')
        # return_df = nav_df.fillna(method='ffill').pct_change().fillna(0.)
        # adj_nav_df = (1 + return_df).cumprod()
        # self.plotly_line(adj_nav_df, "可转债套利产品走势图", "D:\\量化产品跟踪\\代销及FOF标的\\可转债走势.html",
        #                  figsize=(1200, 600))

        writer.save()


if __name__ == '__main__':
    AlphaPerformance('20210520', '20220429', '20220527', alpha_dict).get_construct_result()