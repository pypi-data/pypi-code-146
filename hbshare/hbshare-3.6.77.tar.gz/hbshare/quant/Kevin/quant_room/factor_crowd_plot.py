"""
风格拥挤度跟踪模块
"""
import pandas as pd
import hbshare as hbs
from datetime import datetime
from sqlalchemy import create_engine
from hbshare.quant.Kevin.rm_associated.config import engine_params
import pyecharts.options as opts
from pyecharts.charts import Line, Bar
from pyecharts.globals import ThemeType


class FactorCrowd:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._load_data()

    def _load_data(self):
        engine = create_engine(engine_params)
        # crowd ratio
        sql_script = "SELECT * FROM crowd_ratio where trade_date >= {} and trade_date <= {}".format(
            self.start_date, self.end_date)
        crowd_ratio = pd.read_sql(sql_script, engine)
        crowd_ratio['trade_date'] = crowd_ratio['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        crowd_ratio['mean_ratio'] = crowd_ratio[['mean_to', 'stock_vol', 'beta']].mean(axis=1)
        crowd_ratio.loc[crowd_ratio['factor_name'] == "growth", 'mean_ratio'] = crowd_ratio['beta']
        self.crowd_ratio = pd.pivot_table(
            crowd_ratio, index='trade_date', columns='factor_name', values='mean_ratio').sort_index()
        # ls return
        sql_script = "SELECT * FROM ls_return where trade_date >= {} and trade_date <= {}".format(
            self.start_date, self.end_date)
        ls_return = pd.read_sql(sql_script, engine)
        ls_return['trade_date'] = ls_return['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
        self.factor_return = pd.pivot_table(
            ls_return, index='trade_date', columns='factor_name', values='ls_return').sort_index()

    def run(self, factor_name, standardize=True):
        crowd_ratio = self.crowd_ratio.copy()
        if standardize:
            crowd_ratio = (crowd_ratio - crowd_ratio.mean()) / crowd_ratio.std()
        factor_return = self.factor_return.copy()

        if factor_name in crowd_ratio.columns:
            df = crowd_ratio[[factor_name]].merge(
                factor_return[[factor_name]], left_index=True, right_index=True, suffixes=('_crowd', '_ret'))
            df[factor_name + '_nav'] = (1 + df[factor_name + '_ret']).cumprod()
            df = df.round(3)
            # plot
            bar = (
                Bar(init_opts=opts.InitOpts(width='1200px', height='600px'))
                .add_xaxis(
                    xaxis_data=df.index.tolist())
                .extend_axis(
                    yaxis=opts.AxisOpts(
                        type_="value",
                        # name="多空净值",
                        axistick_opts=opts.AxisTickOpts(is_show=True),
                        splitline_opts=opts.SplitLineOpts(is_show=False))
                )
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="风格拥挤度"),
                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                    legend_opts=opts.LegendOpts(pos_top='5%'),
                    yaxis_opts=opts.AxisOpts(
                        type_="value",
                        # name="拥挤度",
                        axistick_opts=opts.AxisTickOpts(is_show=True),
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    ),
                    xaxis_opts=opts.AxisOpts(
                        type_="category",
                        # axislabel_opts={"interval": "0", "rotate": 90},
                        axistick_opts=opts.AxisTickOpts(is_show=True)),
                    datazoom_opts=[
                        opts.DataZoomOpts(range_start=0, range_end=100),
                        opts.DataZoomOpts(type_="inside")]
                ).add_yaxis(
                    series_name="风格拥挤度(左轴)",
                    y_axis=df[factor_name + '_crowd'].tolist(),
                    label_opts=opts.LabelOpts(is_show=False),
                    itemstyle_opts=opts.ItemStyleOpts(opacity=0.3),
                    # bar_width="50%",
                    z=0
                )
            )

            line = (
                Line()
                .add_xaxis(
                    xaxis_data=df.index.tolist())
                .add_yaxis(
                    series_name="风格多空净值(右轴)",
                    is_smooth=True,
                    y_axis=df[factor_name + '_nav'].tolist(),
                    is_symbol_show=False,
                    linestyle_opts=opts.LineStyleOpts(width=2),
                    label_opts=opts.LabelOpts(is_show=False),
                    yaxis_index=1
                )
            )

            bar.overlap(line)

            bar.render('D:\\123.html')

        elif factor_name in ["factor_compare", "ret_compare"]:
            if factor_name == "factor_compare":
                df = crowd_ratio[['btop', 'growth']]
                label_name1, label_name2 = "成长拥挤度(左轴)", "价值拥挤度(右轴)"
                title_text = "成长 vs 价值（拥挤度）"
                if standardize:
                    df = (df - df.mean()) / df.std()
            else:
                df = (1 + factor_return).cumprod()[['btop', 'growth']]
                label_name1, label_name2 = "成长多空净值(左轴)", "价值多空净值(右轴)"
                title_text = "成长 vs 价值（收益）"

            df = df.round(3)

            line = (
                Line(init_opts=opts.InitOpts(width='1200px', height='600px'))
                .add_xaxis(
                    xaxis_data=df.index.tolist())
                .extend_axis(
                    yaxis=opts.AxisOpts(
                        type_="value",
                        axistick_opts=opts.AxisTickOpts(is_show=True),
                        splitline_opts=opts.SplitLineOpts(is_show=False))
                ).set_global_opts(
                    title_opts=opts.TitleOpts(title=title_text),
                    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
                    legend_opts=opts.LegendOpts(pos_top='5%'),
                    yaxis_opts=opts.AxisOpts(
                        type_="value",
                        axistick_opts=opts.AxisTickOpts(is_show=True),
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                    ),
                    xaxis_opts=opts.AxisOpts(
                        type_="category",
                        axistick_opts=opts.AxisTickOpts(is_show=True)),
                    datazoom_opts=[
                        opts.DataZoomOpts(range_start=0, range_end=100),
                        opts.DataZoomOpts(type_="inside")]
                ).add_yaxis(
                    series_name=label_name1,
                    is_smooth=True,
                    y_axis=df['growth'].tolist(),
                    is_symbol_show=False,
                    linestyle_opts=opts.LineStyleOpts(width=2),
                    label_opts=opts.LabelOpts(is_show=False),
                    z=0)
            )

            line_sub = (
                Line()
                .add_xaxis(
                    xaxis_data=df.index.tolist())
                .add_yaxis(
                    series_name=label_name2,
                    is_smooth=True,
                    y_axis=df['btop'].tolist(),
                    is_symbol_show=False,
                    linestyle_opts=opts.LineStyleOpts(width=2),
                    label_opts=opts.LabelOpts(is_show=False),
                    yaxis_index=1
                )
            )

            line.overlap(line_sub)

            line.render("D:\\123.html")


if __name__ == '__main__':
    FactorCrowd("20101015", "20221014").run('ret_compare', standardize=False)