import numpy as np
from hbshare.quant.CChen.fund_stats.perf import performance_analysis, performance_specific_ret
from hbshare.quant.CChen.data.data import load_funds_data, load_funds_alpha
import pandas as pd
from hbshare.quant.CChen.db_const import sql_write_path_work
from datetime import timedelta
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import riskfolio as rp

register_matplotlib_converters()
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['KaiTi']

pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.width', 5500)


class FOFBacktest(object):

    investable_date = None
    db_path = sql_write_path_work['work']
    # cal_path = sql_write_path_work['daily']

    result = None
    fof_result = None

    trade_dict = {
        1: [
            1,
            # 4,
            7,
            # 10
        ],
        2: [2, 5, 8, 11],
        3: [3, 6, 9, 12],
    }

    def __init__(
            self,
            start_date,
            end_date,
            targets,
            date_key='t_date',
            alpha=False,
            data=None,
            trade_m=1
    ):
        self.start_date = start_date
        self.end_date = end_date
        self.targets = targets
        self.target_weight = None
        self.tm = trade_m

        self.funds = pd.read_sql_query(
            'select * from fund_list where `name` in' + str(tuple(self.targets['name'].tolist())).replace(',)', ')'),
            self.db_path
        )

        if data is None:
            self.data = load_funds_data(
                fund_list=self.funds,
                first_date=start_date - timedelta(days=365 * 2),
                end_date=end_date,
                freq='w',
                db_path=self.db_path,
                # cal_db_path=self.cal_path,
                drop_1=True,
            )[[date_key] + self.targets['name'].tolist()]
        else:
            self.data = data

        if alpha:
            self.data_alpha = load_funds_alpha(
                fund_list=self.funds,
                first_date=start_date - timedelta(days=365 * 2),
                end_date=end_date,
                freq='w',
                db_path=self.db_path,
                # cal_db_path=self.cal_path
            )['eav']

        self.calendar = self.data[date_key].tolist()
        self.data = self.data.set_index(self.data[date_key]).ffill()
        self.data = self.data[self.targets['name'].tolist()]
        self.data_return = self.data.pct_change()

        self.fund_pos_df = pd.DataFrame()
        self.fund_value_df = pd.DataFrame()
        self.fund_contribution_df = pd.DataFrame()
        self.equity = pd.DataFrame()

        self.money = 1

    def current_targets(self, date):
        fund_pool = self.targets['name'].tolist().copy()
        fund_targets = self.data.loc[date, fund_pool]
        return fund_targets

    def consider_investable_date(self, date, fund_pool):
        # 考虑入池时间
        if self.investable_date is not None:
            for f in self.investable_date:
                if date < self.investable_date[f]['入池时间'].date():
                    if f in fund_pool:
                        fund_pool.remove(f)
        return fund_pool

    def compute_initial_weights(self, date, fund_targets):
        pass

    def compute_weights(self, date, fund_targets):
        pass

    def compute_contribution(self, date):
        date_lag = self.calendar[self.calendar.index(date) - 1]
        funds_return = self.current_targets(date=date) - self.current_targets(date=date_lag)
        fund_contribution = funds_return * self.fund_pos_df.loc[date_lag]
        self.fund_contribution_df = pd.concat(
            [
                self.fund_contribution_df,
                pd.DataFrame(fund_contribution).T.rename({0: date})
            ],
            sort=True
        )

    def trade_status(self, current_date):
        # 判定是否交易

        if_trade = (
                current_date.month in self.trade_dict[self.tm]
                and current_date.month != self.calendar[self.calendar.index(current_date) - 1].month
        )
        return if_trade

    def run(self, no_adjust_untill_new=False, trade_lag=False):
        start_index = sum(np.array(self.calendar) < self.start_date)
        fund_pos = None
        self.equity = pd.DataFrame(
            {
                '现金': 0
            }, index=[self.calendar[start_index - 1]]
        )

        for i in range(start_index, len(self.calendar)):
            current_date = self.calendar[i]
            # print(current_date)
            fund_targets = self.current_targets(date=current_date)

            if i == start_index:
                # 起点建仓
                fund_pos = self.compute_initial_weights(date=current_date, fund_targets=fund_targets)
                fund_value = fund_pos.mul(fund_targets)
                self.fund_contribution_df = fund_value.copy()
                self.fund_contribution_df.iloc[:, :] = np.nan

            else:
                fund_pos = fund_pos.rename({self.data.index[i - 1]: self.data.index[i]})
                fund_value = fund_pos * fund_targets

                # 计算当期分产品贡献
                self.compute_contribution(date=current_date)

            self.fund_value_df = pd.concat([self.fund_value_df, fund_value], sort=True)
            if self.equity.loc[self.calendar[i - 1], '现金'] > 0:
                # 上一期总资产
                fund_pos = pos_future
                self.equity.loc[current_date, '现金'] = 0
            else:
                self.equity.loc[current_date, '现金'] = self.equity.loc[self.calendar[i - 1], '现金']

            # 交易
            if i > start_index and i != len(self.calendar) - 1:
                if self.trade_status(current_date=current_date):
                    if no_adjust_untill_new:
                        if int((~np.isnan(fund_value.values)).sum()) != len(fund_targets[fund_targets > 0]):
                            fund_pos = self.compute_weights(date=current_date, fund_targets=fund_targets)
                    else:
                        fund_pos = self.compute_weights(date=current_date, fund_targets=fund_targets)

                    if trade_lag:
                        # 考虑申购赎回间隔
                        position_before_trade = self.fund_pos_df.loc[
                            [self.calendar[i - 1]],
                            (self.fund_pos_df.loc[[self.calendar[i - 1]]] > 0).loc[self.calendar[i - 1]]
                            + (fund_pos.loc[[self.calendar[i]]] > 0).loc[self.calendar[i]]
                        ].fillna(0)  # 赎回前标的仓位
                        position_after_trade = fund_pos.loc[
                            [self.calendar[i]],
                            (self.fund_pos_df.loc[[self.calendar[i - 1]]] > 0).loc[self.calendar[i - 1]]
                            + (fund_pos.loc[[self.calendar[i]]] > 0).loc[self.calendar[i]]
                        ].fillna(0)  # 赎回后标的仓位
                        position_trade = position_before_trade.append(position_after_trade)
                        fund_pos = pd.DataFrame(position_trade.min(axis=0)).rename(columns={0: current_date}).loc[
                            (position_trade.loc[[self.calendar[i]]] > 0).loc[self.calendar[i]]
                        ].T  # 实际赎回操作后的仓位
                        fund_v = fund_pos * fund_targets
                        fund_v = fund_v[fund_v > 0]
                        # 计算目标持仓分产品持仓市值
                        # fund_value_trade = fund_pos.copy()
                        # fund_value_trade.loc[:, :] = self.fund_value_df.loc[current_date].sum() / len(fund_pos.columns)
                        fund_value_trade = position_after_trade * fund_targets
                        value_diff = fund_value_trade - fund_v[fund_value_trade.columns.tolist()].fillna(0)
                        # 下期持仓，涉及未来净值
                        pos_future = (
                                value_diff / self.current_targets(date=self.calendar[i + 1])[
                                    fund_value_trade.columns.tolist()
                                ] + fund_pos
                        ).set_index([[self.calendar[i + 1]]])
                        self.equity.loc[current_date, '现金'] = (
                                self.fund_value_df.loc[current_date].sum() - (fund_pos * fund_targets).sum(1)[0]
                        )

            self.fund_pos_df = pd.concat([self.fund_pos_df, fund_pos], sort=True)

            # if i == len(self.calendar) - 1:
            #     self.compute_contribution(date=current_date)

        if self.equity['现金'].max() > 0:
            self.fund_value_df['现金'] = self.equity['现金'][:-1].tolist()
        self.fof_result = pd.DataFrame(self.fund_value_df.sum(axis=1)).reset_index().rename(
            columns={'index': 't_date', 0: '组合'}
        )
        self.fof_result['动态回撤'] = (
                                        self.fof_result['组合'] - self.fof_result['组合'].cummax()
                                ) / self.fof_result['组合'].cummax()
        result1, _, _ = performance_analysis(
            data_df=self.fof_result[['t_date', '组合']],
            start_date=self.start_date,
            end_date=self.end_date,
            ret_num_per_year=52
        )
        result2 = performance_specific_ret(data_df=self.fof_result[['t_date', '组合']]).reset_index(drop=True)
        self.result = result1.append(result2.loc[6:, :])

    def summary(self, fig=True, title=''):
        pd.options.display.float_format = '{:.2f}'.format
        print(self.result[['index', '组合']].set_index('index'))
        print()
        pd.options.display.float_format = '{:.2%}'.format
        print(
            pd.DataFrame(
                self.fund_contribution_df.sum() / self.money
            ).sort_values(by=0, ascending=False).rename(columns={0: '贡献'})
        )
        # for i in self.fund_contribution_df.columns:
        #     print(i + ' 贡献：\n\t%.2f%%' % round(self.fund_contribution_df[i].sum() * 100 / self.money, 2))

        if fig:
            fig = plt.figure(figsize=(18, 8))
            ax1 = fig.add_subplot(1, 2, 1)
            ax1.plot(self.fof_result['t_date'], self.fof_result['组合'])
            plt.title(title)
            ax11 = ax1.twinx()
            ax11.fill_between(
                self.fof_result['t_date'],
                self.fof_result['动态回撤'],
                color='gray',
                alpha=0.3
            )

            ax2 = fig.add_subplot(1, 2, 2)
            plot_str = ''
            for i in self.fund_contribution_df.columns:
                plot_str += 'self.fund_value_df[\'' + i + '\'].fillna(0).tolist(), '
            eval(
                'ax2.stackplot(self.fund_value_df.index, '
                + plot_str
                + 'labels=list(self.fund_contribution_df.columns))'
            )

            # ax2.stackplot(
            #     fund_value_df.index, np.vstack(fund_value_df.fillna(0).values.T.tolist()),
            #     # labels=list(fund_name)
            # )

            plt.legend(loc=(0.95, 0.05))
            plt.show()

    def to_excel(self, name):
        # self.result.to_excel('bt统计.xlsx')
        # self.fund_pos_df.to_excel('bt权重.xlsx')
        # self.fund_value_df.to_excel('bt价值.xlsx')
        # self.data.to_excel('bt数据.xlsx')
        # self.fund_contribution_df.to_excel('bt贡献.xlsx')

        writer = pd.ExcelWriter(name + '.xlsx')
        self.result.to_excel(writer, sheet_name='统计')
        self.fund_pos_df.to_excel(writer, sheet_name='权重')
        self.fund_value_df.to_excel(writer, sheet_name='价值')
        self.data.to_excel(writer, sheet_name='数据')
        self.fund_contribution_df.to_excel(writer, sheet_name='贡献')
        writer.save()


def exposure_ts(nav_data, factor_data, freq, step='Forward'):
    exposure = pd.DataFrame()
    for i in range(freq + 1, len(nav_data) + 1):
        loadings = rp.loadings_matrix(
            X=factor_data.pct_change().iloc[i - freq: i, :],
            Y=nav_data.pct_change().iloc[i - freq: i, :],
            stepwise=step
        )
        loadings['t_date'] = nav_data.index[i - 1]
        exposure = exposure.append(loadings)
    return exposure







