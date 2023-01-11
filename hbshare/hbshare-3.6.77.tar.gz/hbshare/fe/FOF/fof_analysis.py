import datetime
import pandas as pd
import numpy as np
from hbshare.fe.XZ import db_engine
from hbshare.fe.XZ import functionality
from scipy import interpolate
import  os

util=functionality.Untils()
hbdb=db_engine.HBDB()
plot=functionality.Plot(1000,600)
localdb=db_engine.PrvFunDB().engine


def rolling_rank(array):
    s = pd.Series(array)
    return s.rank(ascending=True).iloc[-1] / len(array)

def monotonic(L):
        return all(x > y for x, y in zip(L, L[1:])) or all(x < y for x, y in zip(L, L[1:]))

def find_weight_change_point(weight_history,col_list,index_list,monotonic_lenght=20):

    weight_target_df = []

    def trade_stat(q_line_date, weight_history):

        tempdf = pd.DataFrame()

        if (len(q_line_date) > 0):
            q_line_date = \
                [weight_history['日期'].iloc[0]] \
                + q_line_date['日期'].tolist() \
                + [weight_history['日期'].iloc[-1]]

            sql = """select zqdm,jyrq,spjg from st_market.t_st_zs_hqql 
            where jyrq in ({0}) and zqdm in ({1})""" \
                .format(util.list_sql_condition(q_line_date),util.list_sql_condition(index_list))

            mu_index_ret = hbdb.db2df(sql, db='alluser').pivot_table('spjg', 'jyrq', 'zqdm')
            mu_index_ret.index = mu_index_ret.index.astype(str)

            for i in range(len(q_line_date) - 1):
                remove_data = int(monotonic_lenght / 2)

                tempdf.loc[q_line_date[i] + " to " + q_line_date[i + 1], '权重均值'] = \
                    weight_history[(weight_history['日期'] >= q_line_date[i])
                                   & (weight_history['日期'] <= q_line_date[i + 1])][col][remove_data:-remove_data].mean()
                tempdf.loc[q_line_date[i] + " to " + q_line_date[i + 1], '权重中值'] = \
                    weight_history[(weight_history['日期'] >= q_line_date[i])
                                   & (weight_history['日期'] <= q_line_date[i + 1])][col][
                    remove_data:-remove_data].median()
                tempdf.loc[q_line_date[i] + " to " + q_line_date[i + 1], '偏离均值'] = \
                    weight_history[(weight_history['日期'] >= q_line_date[i])
                                   & (weight_history['日期'] <= q_line_date[i + 1])][col + "_30div"][
                    remove_data:-remove_data].mean()
                tempdf.loc[q_line_date[i] + " to " + q_line_date[i + 1], '偏离最大'] = \
                    weight_history[(weight_history['日期'] >= q_line_date[i])
                                   & (weight_history['日期'] <= q_line_date[i + 1])][col + "_30div"][
                    remove_data:-remove_data].max()

                if(q_line_date[i] in mu_index_ret.index and q_line_date[i+1] in mu_index_ret.index ):

                    for index_name in index_list:
                        tempdf.loc[q_line_date[i] + " to " + q_line_date[i + 1], index_name] = \
                            (mu_index_ret.loc[q_line_date[i + 1]][index_name] /
                             mu_index_ret.loc[q_line_date[i]][index_name] - 1)


        else:

            tempdf.loc['全期', '权重均值'] = weight_history[col].mean()
            tempdf.loc['全期', '权重中值'] = weight_history[col].median()

            tempdf.loc['全期', '偏离均值'] = weight_history[col + "_30div"][30:-30].mean()
            tempdf.loc['全期', '偏离最大'] = weight_history[col + "_30div"][30:-30].max()

        return tempdf

    for col in col_list:

        weight_history[col + "_30MA"] = weight_history[col].rolling(30).mean()
        weight_history[col + "_30div"] = abs(weight_history[col] - weight_history[col + "_30MA"])
        weight_history[col + 'Ndays_monotonic'] =\
            weight_history[col + "_30div"].rolling(monotonic_lenght).apply(
            monotonic)
        weight_history[col + 'Ndays_monotonic_T-1'] = \
            [np.nan] + weight_history[col + 'Ndays_monotonic'][0:-1].tolist()
        weight_history.loc[(weight_history[col + 'Ndays_monotonic'] == 1) & (
                weight_history[col + 'Ndays_monotonic_T-1'] == 0), col + '_q_line'] = True

        weight_history[col + '_q_line'] = weight_history[col + '_q_line'].iloc[monotonic_lenght:].tolist() + [
            np.nan] * monotonic_lenght

        q_line_date = weight_history[weight_history[col + '_q_line'] == True]

        tempdf = trade_stat(q_line_date, weight_history)
        less_than1_diff = tempdf[tempdf['权重中值'].diff().abs() <= 0.02].index
        while len(less_than1_diff) > 0:
            for date_line in less_than1_diff:
                q_line_date = q_line_date[q_line_date['日期'] != date_line[0:8]]
            tempdf = trade_stat(q_line_date, weight_history)
            less_than1_diff = tempdf[tempdf['权重中值'].diff().abs() <= 0.02].index

        tempdf = tempdf.reset_index(drop=False).rename(columns={'index': '持续日期'})
        tempdf.index = len(tempdf) * [col]
        weight_target_df.append(tempdf)

    weight_target_df = pd.concat(weight_target_df, axis=0)

    return  weight_target_df

class FOF_analysis:

    def __init__(self,dir,end_date):

        raw_df=pd.read_excel(dir,sheet_name='数据')
        # remove '未定义',keep 审核通过 take
        raw_df = raw_df[(raw_df['审核状态'] == '审核通过') & (raw_df['投资类型'] != '未定义')]
        raw_df = raw_df[(raw_df['投资类型'] == '认购') |
                        (raw_df['投资类型'] == '申购')|
                        (raw_df['投资类型'] == '赎回')|
                        (raw_df['投资类型'] == '份额转入')|
                        (raw_df['投资类型'] == '份额转出')]

        raw_df['交易日期'] = raw_df['交易日期'].astype(str).str.replace('-', '')
        raw_df = raw_df[raw_df['交易日期'] <= end_date]
        raw_df['交易日期']=[x[0:8] for x in raw_df['交易日期']]
        raw_df['投资基金代码'] = [ str(x).replace('.OF','') for x in raw_df['投资基金代码']]
        raw_df['投资基金代码'] = [("000000"+str(x))[-6:] for x in raw_df['投资基金代码']]

        #add the nav price for mutual fund



        self.trading_flow=raw_df
        self.prv_jjflmap= dict(zip(['c','d','b','Z','1','2','3','4','5','7','8','0'], ['其他','多策略','多空仓型','组合型','股票型'
                                    ,'债券型','货币型','宏观策略','市场中性','套利型','管理期货','其他']))
        self.prv_ejflmap =dict(zip(['Z001','Z002','c005','c006','c007','1001','1002','2001','2002','2003','2004','8003','8004','8005','8006','0'
                     ],['MOM','FOF','其他策略','期权策略','其他衍生品','主观多头','量化多头','纯债策略','强债策略','转债策略','债券其他','量化趋势','量化套利','管理期货复合','主观CTA','其他'
                     ]))
        self.mu_jjflmap= dict(zip(['1', '2', '3','0','7','9'], ['股票型', '债券型', '混合型','其他','货币型','QDII']))
        self.mu_ejflmap =dict(zip(['13', '14', '15', '16', '21', '22', '23', '24', '25', '26', '27', '28', '34', '35', '36', '37',
                     '38',
                     '41', '42','0','91'
                     ],['普通股票型', '股票型', '增强指数型', '被动指数型', '被动指数型债券', '短期纯债型', '混合债券型一级', '混合债券型二级', '增强指数型债券', '债券型',
                     '中长期纯债型',
                     '可转换债券型', '平衡混合型', '灵活配置型', '混合型', '偏股混合型', '偏债混合型', '股票多空', '商品型','其他','股票型QDII'
                     ]))

        self.index_enhance_manual_map=dict(zip(['SJH866'],['500zz']))

    @staticmethod
    def get_fund_lable(trading_detail):

        # merge mu fund style label
        max_date = \
            pd.read_sql("select max(asofdate) as max_date from jjpic_value_p_hbs ", con=localdb)['max_date'].iloc[0]
        sql = "SELECT jjdm,`风格偏好`,`风格类型`,`成长绝对暴露(持仓)`,`价值绝对暴露(持仓)` from jjpic_value_p_hbs where asofdate='{0}' and jjdm in ({1})" \
            .format(max_date, util.list_sql_condition(trading_detail['jjdm'].unique().tolist()))
        mu_style_lable = pd.read_sql(sql, con=localdb)

        # get the A share label for C share fund
        miss_mu_jjdm = set(trading_detail[(trading_detail['cpfl'] == '2')
                                          & (trading_detail['ejfl'].isin(['13', '35', '37']))][
                               'jjdm']).difference(set(mu_style_lable['jjdm']))

        if(len(miss_mu_jjdm)>0):
            # get fund name
            sql = "select jjdm,jjjc from st_fund.t_st_gm_jjxx where jjdm in ({})" \
                .format(util.list_sql_condition(list(miss_mu_jjdm)))
            fund_name = hbdb.db2df(sql, db='funduser')
            fund_name['jjjc'] = [x.replace('C', 'A') for x in fund_name['jjjc'].tolist()]
            fund_name = pd.merge(fund_name, hbdb.db2df(sql="select jjdm,jjjc from st_fund.t_st_gm_jjxx where jjjc in ({}) "
                                                       .format(util.list_sql_condition(fund_name['jjjc'].tolist())),
                                                       db='funduser')
                                 , how='left', on='jjjc')
            name_map = dict(zip(fund_name['jjdm_x'].tolist(), fund_name['jjdm_y'].tolist()))
            trading_detail.loc[trading_detail['jjdm'].isin(fund_name['jjdm_x'].tolist())
            , 'jjdm'] = [name_map[x] for x in
                         trading_detail[trading_detail['jjdm'].isin(fund_name['jjdm_x'].tolist())]['jjdm'].tolist()]

            sql = "SELECT jjdm,`风格偏好`,`风格类型`,`成长绝对暴露(持仓)`,`价值绝对暴露(持仓)` from jjpic_value_p_hbs where asofdate='{0}' and jjdm in ({1})" \
                .format(max_date, util.list_sql_condition(trading_detail['jjdm'].unique().tolist()))
            mu_style_lable = pd.read_sql(sql, con=localdb)

        mu_style_lable.loc[(mu_style_lable['风格偏好'] == '均衡')
                           & (mu_style_lable['价值绝对暴露(持仓)'] > mu_style_lable['成长绝对暴露(持仓)'])
                           & (mu_style_lable['风格类型'] == '配置')
        , '风格偏好'] = '价值'

        trading_detail = pd.merge(trading_detail, mu_style_lable[['jjdm', '风格偏好']]
                                  , how='left', on='jjdm')
        sql = "SELECT jjdm,`规模偏好` from jjpic_size_p_hbs where asofdate='{0}' and jjdm in ({1})" \
            .format(max_date, util.list_sql_condition(trading_detail['jjdm'].unique().tolist()))
        mu_size_lable = pd.read_sql(sql, con=localdb)
        trading_detail = pd.merge(trading_detail, mu_size_lable[['jjdm', '规模偏好']]
                                  , how='left', on='jjdm')

        missed_mu_jjdm = trading_detail[(trading_detail['风格偏好'].isnull())
                                        & (trading_detail['cpfl'] == '2')
                                        & (trading_detail['ejfl'] != '38')][['jjdm', 'jjjc']]
        missed_prv_jjdm = trading_detail[(trading_detail['风格偏好'].isnull())
                                         & (trading_detail['cpfl'] == '4')
                                         ][['jjdm', 'jjjc']]

        file_list = pd.DataFrame(data=os.listdir(r"E:\GitFolder\docs\净值标签"), columns=['name'])

        nav_mu_label = pd.read_excel(r"E:\GitFolder\docs\净值标签\{}"
                                     .format(file_list[file_list['name'].str.startswith('公募基于净值标签')].iloc[-1]['name']))[
            ['jjdm', '规模标签', '风格标签']]

        nav_mu_label['jjdm'] = [("000000" + str(x))[-6:] for x in nav_mu_label['jjdm']]
        missed_mu_jjdm = pd.merge(missed_mu_jjdm, nav_mu_label, how='left', on='jjdm').drop_duplicates(
            'jjdm').set_index('jjdm')

        for jjdm in missed_mu_jjdm.index.tolist():
            trading_detail.loc[trading_detail['jjdm'] == jjdm, '风格偏好'] = missed_mu_jjdm.loc[jjdm]['风格标签']
            trading_detail.loc[trading_detail['jjdm'] == jjdm, '规模偏好'] = missed_mu_jjdm.loc[jjdm]['规模标签']

        nav_prv_label = pd.read_excel(r"E:\GitFolder\docs\净值标签\{}"
            .format(
            file_list[file_list['name'].str.startswith('全部私募打标结果')].iloc[-1]['name']))[['jjdm', '基金简称', '大小盘', '成长价值']]
        missed_prv_jjdm = pd.merge(missed_prv_jjdm, nav_prv_label, how='left', on='jjdm')
        nav_prv_label['company'] = nav_prv_label['基金简称'].str[0:2]
        missed_prv_jjdm['company'] = missed_prv_jjdm['jjjc'].str[0:2]
        nav_prv_label = nav_prv_label.groupby(['company', '大小盘', '成长价值']).count()['jjdm'].reset_index().sort_values(
            ['company', 'jjdm']).drop_duplicates('company', keep='last').drop('jjdm', axis=1)
        missed_prv_jjdm = pd.merge(missed_prv_jjdm, nav_prv_label, how='left', on='company')
        missed_prv_jjdm.loc[missed_prv_jjdm['大小盘_x'].isnull(), '大小盘_x'] = \
            missed_prv_jjdm[missed_prv_jjdm['大小盘_x'].isnull()]['大小盘_y']
        missed_prv_jjdm.loc[missed_prv_jjdm['成长价值_x'].isnull(), '成长价值_x'] = \
            missed_prv_jjdm[missed_prv_jjdm['成长价值_x'].isnull()]['成长价值_y']
        missed_prv_jjdm = missed_prv_jjdm.rename(columns={'大小盘_x': '大小盘'
            , '成长价值_x': '成长价值'}).drop(['大小盘_y',
                                       '成长价值_y'], axis=1).drop_duplicates('jjdm').set_index('jjdm')

        for jjdm in missed_prv_jjdm.index.tolist():
            trading_detail.loc[trading_detail['jjdm'] == jjdm, '风格偏好'] = missed_prv_jjdm.loc[jjdm]['成长价值']
            trading_detail.loc[trading_detail['jjdm'] == jjdm, '规模偏好'] = missed_prv_jjdm.loc[jjdm]['大小盘']

        return trading_detail

    def fromtrading2holding(self,end_date,start_date=None):

        if(start_date is None):
            start_date='0'

        # read trading details

        raw_df = self.trading_flow


        raw_df=pd.merge(raw_df.drop_duplicates(['产品名称','投资基金代码','交易日期','指令类型'])[['产品名称', '投资基金'
            , '投资基金代码', '指令类型', '投资类型', '交易日期', '确认净值','审核状态']]
                        ,raw_df.groupby(['产品名称','投资基金代码','交易日期','指令类型']).sum()[['认申购金额','赎回份额','赎回费']].reset_index()
                        ,how='inner',on=['产品名称','投资基金代码','交易日期','指令类型'])

        #combine the same action happend in one day


        for product in raw_df['产品名称'].unique():
            df = raw_df[raw_df['产品名称'] == product]
            df = df.sort_values('交易日期')
            nav_df = pd.read_excel(r"E:\FOF分析\{}\基金净值数据.xls".format(product))
            nav_df['日期'] = nav_df['日期'].astype(str).str.replace('-', '')
            nav_df = nav_df.sort_values('日期')
            nav_df=nav_df[nav_df['日期']<=end_date]
            date_list = nav_df['日期'].tolist()
            date_list = date_list + df['交易日期'].unique().tolist()
            date_list=list(set(date_list))
            date_list.sort()
            hold_df = []

            for i in range(len(date_list)):

                date = date_list[i]


                buy = df[((df['投资类型'] == '申购')|(df['投资类型'] == '认购')|(df['投资类型'] == '份额转入'))
                         & (df['交易日期'] == date)][['投资基金代码', '认申购金额', '确认净值']]
                sell = df[((df['投资类型'] == '赎回')|(df['投资类型'] == '份额转出'))
                          & (df['交易日期'] == date)][['投资基金代码', '赎回份额', '确认净值', '赎回费']]

                if (i == 0):
                    tempdf = pd.DataFrame(columns=['date', 'jjdm', 'quant', 'cbprice','buyprice', 'sellprice'])
                    tempdf['date'] = [date]
                else:
                    tempdf = hold_df[i - 1].copy()

                # buy
                if (len(buy) > 0):
                    buy['buy_quant'] = buy['认申购金额'] / buy['确认净值']

                    tempdf = pd.merge(tempdf, buy[['投资基金代码', 'buy_quant', '确认净值']]
                                      , how='outer', left_on='jjdm', right_on='投资基金代码')

                    tempdf.loc[tempdf['buy_quant'].notnull(), 'cbprice'] = ((tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'cbprice']*tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'quant']).fillna(0)+tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             '确认净值']*tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'buy_quant'])/\
                                                                           (tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'quant'].fillna(0)+tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'buy_quant'])

                    # tempdf.loc[tempdf['buy_quant'].notnull(), 'money_price'] = ((tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'cbprice']*tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'quant']*tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'money_price']).fillna(0)+tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          '确认净值']*tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'buy_quant']*nav_df[nav_df['日期']==date]['单位净值'].values[0])/\
                    #                                                        ((tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'cbprice']*tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'quant']).fillna(0)+tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          '确认净值']*tempdf.loc[tempdf['buy_quant'].notnull()][
                    #                                                          'buy_quant'])


                    tempdf['cbprice']=tempdf['cbprice'].astype(float)

                    tempdf.loc[tempdf['buy_quant'].notnull(), 'quant'] = tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'quant'].fillna(0) \
                                                                         + tempdf.loc[tempdf['buy_quant'].notnull()][
                                                                             'buy_quant']
                    tempdf.loc[tempdf['buy_quant'].notnull(), 'jjdm'] = tempdf.loc[tempdf['buy_quant'].notnull()][
                        '投资基金代码']
                    tempdf.loc[tempdf['buy_quant'].notnull(), 'buyprice'] = tempdf.loc[tempdf['buy_quant'].notnull()][
                        '确认净值']

                    tempdf.drop(['buy_quant', '投资基金代码', '确认净值'], axis=1, inplace=True)
                    tempdf = tempdf[tempdf['jjdm'].notnull()]
                # sell
                if (len(sell) > 0):
                    tempdf = pd.merge(tempdf, sell[['投资基金代码', '赎回份额', '确认净值']]
                                      , how='left', left_on='jjdm', right_on='投资基金代码')

                    tempdf.loc[tempdf['赎回份额'].notnull(), 'cbprice'] = ((tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             'cbprice']*tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             'quant']).fillna(0)-tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             '确认净值']*tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             '赎回份额'])/\
                                                                           (tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             'quant'].fillna(0)-tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                             '赎回份额'])




                    tempdf.loc[tempdf['赎回份额'].notnull(), 'quant'] = tempdf.loc[tempdf['赎回份额'].notnull()][
                                                                        'quant'].fillna(0) \
                                                                    - tempdf.loc[tempdf['赎回份额'].notnull()]['赎回份额']
                    #if left quant<100,make it 0
                    tempdf.loc[(tempdf['赎回份额'].notnull())&(tempdf['quant']<=100), 'quant']=0

                    tempdf.loc[tempdf['赎回份额'].notnull(), 'sellprice'] = tempdf.loc[tempdf['赎回份额'].notnull()]['确认净值']
                    tempdf.drop(['赎回份额', '投资基金代码', '确认净值'], axis=1, inplace=True)

                tempdf['date'] = date

                if(date==start_date ):
                    file_name_list =pd.DataFrame(data=os.listdir(r"E:\FOF分析\{0}\估值表\{1}"
                                                .format(product,start_date[0:6])),columns=['name'])
                    file_name_list['name_new'] = [x.replace("-", '') for x in file_name_list['name']]
                    fold_name = \
                    file_name_list[file_name_list['name_new'].str.contains(start_date)]['name'].iloc[0]
                    gzb = pd.read_excel(r"E:\FOF分析\{0}\估值表\{1}\{2}"
                                        .format(product, start_date[0:6], fold_name)).iloc[2:-3]
                    gzb.columns = gzb.iloc[0]
                    gzb = gzb[((gzb['科目代码'].astype(str).str.startswith('11090501'))
                               | (gzb['科目代码'].astype(str).str.startswith('11090201'))
                               | (gzb['科目代码'].astype(str).str.startswith('11050201'))
                               | (gzb['科目代码'].astype(str).str.startswith('11050301')) |
                               (gzb['科目代码'].astype(str).str.startswith('11090601')))
                              &
                              ((gzb['科目代码'].astype(str) != '11090201')
                               & (gzb['科目代码'].astype(str) != '11090501')
                               & (gzb['科目代码'].astype(str) != '11050201')
                               & (gzb['科目代码'].astype(str) != '11050301')
                               & (gzb['科目代码'].astype(str) != '11090601'))][['科目代码', '科目名称', '市价']]

                    gzb.loc[(gzb['科目代码'].str.startswith('11090201'))
                            & (~gzb['科目代码'].str.startswith('11090201S'))
                            & (~gzb['科目代码'].str.startswith('11090201P')), '科目代码'] = "S" + \
                                                                                    gzb[(gzb['科目代码'].str.startswith(
                                                                                        '11090201'))
                                                                                        & (~gzb['科目代码'].str.startswith(
                                                                                        '11090201S'))]['科目代码'].str[
                                                                                    -6:-1]
                    gzb.loc[(gzb['科目代码'].str.startswith('11090601'))
                            & (~gzb['科目代码'].str.startswith('11090601S'))
                            & (~gzb['科目代码'].str.startswith('11090601P')), '科目代码'] = "S" + \
                                                                                    gzb[(gzb['科目代码'].str.startswith(
                                                                                        '11090601'))
                                                                                        & (~gzb['科目代码'].str.startswith(
                                                                                        '11090601S'))]['科目代码'].str[
                                                                                    -6:-1]

                    gzb['科目代码']=gzb['科目代码'].str[-6:-1]
                    tempdf['科目代码']=tempdf['jjdm'].astype(str).str[-6:-1]
                    tempdf=pd.merge(tempdf,gzb,how='left',on='科目代码')
                    tempdf['cbprice']=tempdf['市价']
                    tempdf=tempdf[tempdf['市价'].notnull()]
                    tempdf.drop(['科目名称','市价','科目代码'],axis=1,inplace=True)
                    tempdf=tempdf[tempdf['quant']!=0]

                hold_df.append(tempdf)

            hold_df = pd.concat(hold_df, axis=0)
            hold_df = pd.merge(hold_df, nav_df[['日期', '资产净值', '资产份额', '单位净值','累计单位净值']]
                               , how='left', left_on='date', right_on='日期')
            hold_df['jjdm']=[("000000"+x)[-6:] for x in hold_df['jjdm'].astype(str).tolist()]
            jjdm_list = hold_df['jjdm'].unique().tolist()

            # get prv list and mutual list
            sql = "select jjdm,jjjc,cpfl,jjfl,ejfl from st_fund.t_st_gm_jjxx where jjdm in ({}) and cpfl='2'" \
                .format(util.list_sql_condition([("000000" + x)[-6:] for x in jjdm_list]))
            mutual_fund = hbdb.db2df(sql, db='funduser')

            sql = "select jjdm,jjjc,cpfl,jjfl,ejfl from st_hedge.t_st_jjxx where jjdm in ({}) and cpfl='4'" \
                .format(util.list_sql_condition(jjdm_list))
            prv_fund = hbdb.db2df(sql, db='highuser')
            #
            # sql="select jjdm,jjjc,cpfl,jjfl,ejfl from st_fixed.t_st_jjxx where jjdm in ({0}) "\
            #     .format(util.list_sql_condition(jjdm_list))
            # fix_fund=hbdb.db2df(sql, db='fixeduser')

            # read fund nav from DB

            # for prv fund
            if(len(prv_fund)>0):
                sql = "select jjdm,jzrq,jjjz from st_hedge.t_st_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'" \
                    .format(util.list_sql_condition(prv_fund['jjdm'].tolist()), date_list[0], date_list[-1])
                prv_nav = hbdb.db2df(sql, db='highuser')
            else:
                prv_nav=pd.DataFrame(columns=['jjdm','jzrq','jjjz'])

            prv_nav_new=[]

            for date in hold_df['date'].unique().tolist():
                tempdf=\
                    prv_nav[(prv_nav['jzrq']<=date)&(prv_nav['jjjz'].notnull())][['jjjz','jjdm']].drop_duplicates('jjdm',keep='last')
                tempdf['jzrq']=date
                prv_nav_new.append(tempdf)

            prv_nav=pd.concat(prv_nav_new,axis=0).reset_index(drop=True)

            # for mutual fund
            if(len(mutual_fund[mutual_fund['jjfl']!='7'])>0):
                sql = "select jjdm,jzrq,jjjz from st_fund.t_st_gm_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'" \
                    .format(util.list_sql_condition(mutual_fund['jjdm'].tolist()), date_list[0], date_list[-1])
                mutual_nav = hbdb.db2df(sql, db='funduser')
                mutual_nav['jzrq'] = mutual_nav['jzrq'].astype(str)
            else:
                mutual_nav=pd.DataFrame(columns=['jjdm','jzrq','jjjz'])

            mu_nav_new=[]

            for date in hold_df['date'].unique().tolist():
                tempdf=\
                    mutual_nav[(mutual_nav['jzrq']<=date)&(mutual_nav['jjjz'].notnull())][['jjjz','jjdm']].drop_duplicates('jjdm',keep='last')
                tempdf['jzrq']=date
                mu_nav_new.append(tempdf)

            mutual_nav=pd.concat(mu_nav_new,axis=0).reset_index(drop=True)


            hold_nan = hold_df[hold_df['jjdm'].isin(list((set(hold_df['jjdm'].unique()).difference(set(mutual_fund['jjdm'].tolist()))).difference(set(prv_fund['jjdm'].tolist()))))]

            hold_df_mu = pd.merge(hold_df[hold_df['jjdm'].isin(mutual_fund['jjdm'].tolist())], mutual_nav
                                  , how='left', left_on=['jjdm', 'date'], right_on=['jjdm', 'jzrq'])
            hold_df_mu=pd.merge(hold_df_mu,mutual_fund,how='left',on='jjdm')

            hold_df_prv = pd.merge(hold_df[hold_df['jjdm'].isin(prv_fund['jjdm'].tolist())], prv_nav
                                   , how='left', left_on=['jjdm', 'date'], right_on=['jjdm', 'jzrq'])
            hold_df_prv=pd.merge(hold_df_prv,prv_fund,how='left',on='jjdm')

            hold_df = pd.concat([hold_nan, hold_df_prv], axis=0)
            hold_df = pd.concat([hold_df, hold_df_mu], axis=0).sort_values('date').drop(['jzrq', '日期'], axis=1)

            hold_df=self.get_fund_lable(hold_df)


            #make sure that every fund has jjjz at the last day
            file_name_list = pd.DataFrame(data=os.listdir(r"E:\FOF分析\{0}\估值表\{1}"
                                                          .format(product, hold_df['date'].max()[0:6])),
                                          columns=['name'])
            file_name_list['name_new']=[x.replace("-",'') for x in file_name_list['name']]
            fold_name = file_name_list[file_name_list['name_new'].str.contains(hold_df['date'].max())]['name'].iloc[0]
            gzb = pd.read_excel(r"E:\FOF分析\{0}\估值表\{1}\{2}"
                                .format(product, hold_df['date'].max()[0:6], fold_name)).iloc[2:-3]
            gzb.columns = gzb.iloc[0]
            gzb = gzb[((gzb['科目代码'].astype(str).str.startswith('11090501'))
                       | (gzb['科目代码'].astype(str).str.startswith('11090201'))
                       |(gzb['科目代码'].astype(str).str.startswith('11050201'))
                       |(gzb['科目代码'].astype(str).str.startswith('11050301'))|
                       (gzb['科目代码'].astype(str).str.startswith('11090601')))
                      &
                      ((gzb['科目代码'].astype(str) != '11090201')
                       & (gzb['科目代码'].astype(str) != '11090501')
                       &(gzb['科目代码'].astype(str) != '11050201')
                       &(gzb['科目代码'].astype(str) != '11050301')
                       &(gzb['科目代码'].astype(str) != '11090601'))][['科目代码', '科目名称', '市价']]

            gzb.loc[(gzb['科目代码'].str.startswith('11090201'))
                    & (~gzb['科目代码'].str.startswith('11090201S'))
                    & (~gzb['科目代码'].str.startswith('11090201P')), '科目代码'] = "S" + \
                                                                            gzb[(gzb['科目代码'].str.startswith('11090201'))
                                                                                & (~gzb['科目代码'].str.startswith(
                                                                                '11090201S'))]['科目代码'].str[-6:-1]
            gzb.loc[(gzb['科目代码'].str.startswith('11090601'))
               & (~gzb['科目代码'].str.startswith('11090601S'))
               & (~gzb['科目代码'].str.startswith('11090601P')), '科目代码'] = "S" + \
                                                                            gzb[(gzb['科目代码'].str.startswith('11090601'))
               & (~gzb['科目代码'].str.startswith('11090601S'))]['科目代码'].str[-6:-1]

            gzb['科目代码'] = gzb['科目代码'].str[-6:]
            hold_df['科目代码'] = hold_df['jjdm'].astype(str).str[-6:]
            hold_df = pd.merge(hold_df, gzb, how='left', on='科目代码')
            hold_df.loc[hold_df['jjjz'].isnull(),'jjjz']=hold_df[hold_df['jjjz'].isnull()]['市价']
            hold_df.drop(['科目名称', '市价', '科目代码'], axis=1, inplace=True)

            hold_df.to_excel(r"E:\FOF分析\{}\基金持仓数据.xlsx".format(product), index=False)

            print(product + ' Done ')

    def valuation_table_analysis(self,product,end_date,start_date=None):

        if(start_date is None):
            start_date='0'

        month_list=os.listdir(r"E:\FOF分析\{0}\估值表"
                                    .format(product))

        solved_gzb=[]

        for month in month_list:
            file_name_list =pd.DataFrame(data=os.listdir(r"E:\FOF分析\{0}\估值表\{1}"
                                        .format(product,month)),columns=['name'])

            for name in file_name_list['name']:
                gzb = pd.read_excel(r"E:\FOF分析\{0}\估值表\{1}\{2}"
                                    .format(product, month, name)).iloc[2:-3]
                gzb.columns = gzb.iloc[0]
                gzb = gzb[((gzb['科目代码'].astype(str).str.startswith('11090501'))
                           | (gzb['科目代码'].astype(str).str.startswith('11090201'))
                           | (gzb['科目代码'].astype(str).str.startswith('11050201'))
                           | (gzb['科目代码'].astype(str).str.startswith('11050301')) |
                           (gzb['科目代码'].astype(str).str.startswith('11090601'))
                           |(gzb['科目代码'].astype(str)=='1203'))
                          &
                          ((gzb['科目代码'].astype(str) != '11090201')
                           & (gzb['科目代码'].astype(str) != '11090501')
                           & (gzb['科目代码'].astype(str) != '11050201')
                           & (gzb['科目代码'].astype(str) != '11050301')
                           & (gzb['科目代码'].astype(str) != '11090601'))][['科目代码', '科目名称','数量'
                    ,'单位成本','成本占净值%','市价','市值','市值占净值%','估值增值']]

                if('1203' not in gzb['科目代码'].tolist()):
                    gzb.loc[gzb.index[-1]+1]=['1203','应收股利']+[0]*7


                gzb['科目代码']=gzb['科目代码'].str[-6:]
                gzb['date']=name.split('.')[0][-8:]



                solved_gzb.append(gzb)

        hold_df=pd.concat(solved_gzb,axis=0)

        jjdm_map=dict(zip(['SSA052','1ZLZG3','1BYTZ2','1AAAA7','1BXZG2','1BLKS1','002316','SVN813','482002',
                           '001714','2QHGH1','450009','519133','005277','SGG127','1HYZG5','006699','006784','006131',
                           '1HFL32','2HFLH1','2JZTZ1','1JZTZ4','1LPTZ2','2LPTZ4','SJB208','1LSTZ9','3MXTZ1','1MXTZ8',
                           'SJF304','3MHTZ3','1MHTZC','1MHTZJ','SGG585','1MHTZB','1MHTZE','003474','005127','1QLTZ3',
                           '1QLTZ5','1QLT11','2RQZG1','3RPTZ2','SQR743','377240','1SGD12','006978','005488','1XMZC2',
                           'SGK791','1XMZC1','1XKTZA','1XKTZA','1XKTZ5','3XKTZ2','1YFT12','SJH866','SJH864','110026',
                           '001856','3ZHTZ1','005070','003363','003538','006567','1203']
                          ,['SSA052','SLP211','SNZ338','SQS281','STR792','SED697','002316','SVN813','482002','001714'
                              ,'SY0256','450009','519133','005277','SGG127','S83614','006699','006784','006131',
                            'SNX384','SLK497','SNE372','SJD015','SNP300','SQJ816','SJB208','SER492','SJA462','SGP290',
                            'SJF304','SR0001','SM8148','SLF242','SGG585','SEF092','SCY785','003474','005127','SGC224',
                            'SGY379','SNL641','SJZ021','SX5605','SQR743','377240','SGU946','006978','005488','SEU546',
                            'SGK791','SEZ550','SQW465','SSE288','SNV206','SSM840','SNP647','SJH866','SJH864','110026',
                            '001856','SQS592','005070','003363','003538','006567','1203']))
        hold_df['科目代码'] = [jjdm_map[x] for x in hold_df['科目代码']]
        jjdm_list=hold_df['科目代码'].unique()
        # get prv list and mutual list
        sql = "select jjdm,cpfl,jjfl,ejfl from st_fund.t_st_gm_jjxx where jjdm in ({}) and cpfl='2'" \
            .format(util.list_sql_condition(jjdm_list))
        mutual_fund = hbdb.db2df(sql, db='funduser')

        sql = "select jjdm,cpfl,jjfl,ejfl from st_hedge.t_st_jjxx where jjdm in ({}) and cpfl='4'" \
            .format(util.list_sql_condition(jjdm_list))
        prv_fund = hbdb.db2df(sql, db='highuser')

        fund_features=pd.concat([mutual_fund,prv_fund],axis=0)
        hold_df=pd.merge(hold_df,fund_features,how='left',
                         left_on='科目代码',right_on='jjdm').drop('jjdm',axis=1).rename(columns={'科目代码':'jjdm',
                                                                                             '科目名称':'jjjc',
                                                                                             '数量':'quant',
                                                                                             '单位成本':'cbprice',
                                                                                             '市价':'jjjz',
                                                                                             '市值':'mv',
                                                                                             '成本占净值%':'cb_w',
                                                                                             '市值占净值%':'weight',
                                                                                             '估值增值':'value_increased',})
        # hold_nan = hold_df[hold_df['jjdm'].isin(list((set(hold_df['jjdm'].unique()).difference(set(mutual_fund['jjdm'].tolist()))).difference(set(prv_fund['jjdm'].tolist()))))]
        #
        # hold_df_mu = pd.merge(hold_df[hold_df['jjdm'].isin(mutual_fund['jjdm'].tolist())], mutual_nav
        #                       , how='left', left_on=['jjdm', 'date'], right_on=['jjdm', 'jzrq'])
        # hold_df_mu=pd.merge(hold_df_mu,mutual_fund,how='left',on='jjdm')
        #
        # hold_df_prv = pd.merge(hold_df[hold_df['jjdm'].isin(prv_fund['jjdm'].tolist())], prv_nav
        #                        , how='left', left_on=['jjdm', 'date'], right_on=['jjdm', 'jzrq'])
        # hold_df_prv=pd.merge(hold_df_prv,prv_fund,how='left',on='jjdm')
        #
        # hold_df = pd.concat([hold_nan, hold_df_prv], axis=0)
        # hold_df = pd.concat([hold_df, hold_df_mu], axis=0).sort_values('date').drop(['jzrq', '日期'], axis=1)

        nav_df = pd.read_excel(r"E:\FOF分析\{}\基金净值数据.xls".format(product))
        nav_df['日期'] = nav_df['日期'].astype(str).str.replace('-', '')
        nav_df = nav_df.sort_values('日期')

        hold_df=pd.merge(hold_df,nav_df[['日期', '资产净值', '资产份额', '单位净值', '累计单位净值']]
                         ,how='left',left_on='date',right_on='日期').drop('日期',axis=1)


        hold_df=self.get_fund_lable(hold_df)

        hold_df.to_excel(r"E:\FOF分析\{}\基金持仓数据.xlsx".format(product), index=False)

        print(product + ' Done ')

    def fund_attribution_new(self,hold_df):

        hold_df['ejfl'] = hold_df['ejfl'].fillna(0).astype(str).str.replace("\.0", '')
        hold_df['jjfl'] = hold_df['jjfl'].fillna(0).astype(str).str.replace("\.0", '')


        for index in self.mu_jjflmap.keys():
            hold_df.loc[(hold_df['jjfl'] == index)
                        &(hold_df['cpfl'] == '公募基金'), 'jjfl'] = self.mu_jjflmap[index]
        for index in self.prv_jjflmap.keys():
            hold_df.loc[(hold_df['jjfl'] == index)
                        &(hold_df['cpfl'] == '私募基金'), 'jjfl'] = self.prv_jjflmap[index]

        for index in self.mu_ejflmap.keys():
            hold_df.loc[(hold_df['ejfl'] == index)
                        &(hold_df['cpfl'] == '公募基金'), 'ejfl'] = self.mu_ejflmap[index]
        for index in self.prv_ejflmap.keys():
            hold_df.loc[(hold_df['ejfl'] == index)
                        &(hold_df['cpfl'] == '私募基金'), 'ejfl'] = self.prv_ejflmap[index]

        trade_data=self.trading_flow

        cont=[]
        hold_df['ret'] = hold_df[['jjdm', 'jjjz']].groupby('jjdm').diff().fillna(0)
        for jjdm in hold_df['jjdm'].unique():

            tempdf=hold_df[hold_df['jjdm']==jjdm]

            tempdf['revenue']=tempdf['value_increased'].diff()
            tempdf['revenue_2'] = tempdf['mv'].diff()

            tempdf['quant_change']=tempdf['quant'].diff().fillna(0)

            tempdf_trade=trade_data[trade_data['投资基金代码'] == jjdm]
            tempdf_trade['交易日期'] = [datetime.datetime.strptime(x, '%Y%m%d') for x in tempdf_trade['交易日期']]

            buy=tempdf[tempdf['quant_change'] >0]['date']
            sell=tempdf[tempdf['quant_change'] <0]['date']
            for buydate in buy:
                day_delta = \
                    datetime.datetime.strptime(str(buydate), '%Y%m%d') - \
                    tempdf_trade[tempdf_trade['认申购金额'] > 0][
                    '交易日期'].to_frame('day_delta')
                day_delta['day_delta'] = [x.days for x in day_delta['day_delta']]
                if(((day_delta['day_delta']>=0)&(day_delta['day_delta']<=8)).sum()==0):
                    tempdf.loc[tempdf['date']==buydate,'revenue']=\
                        tempdf.loc[tempdf['date']==buydate]['revenue_2']

            for selldate in sell:
                day_delta = \
                    datetime.datetime.strptime(str(selldate), '%Y%m%d') - \
                    tempdf_trade[tempdf_trade['认申购金额'] < 0][
                    '交易日期'].to_frame('day_delta')
                day_delta['day_delta'] = [x.days for x in day_delta['day_delta']]
                if(((day_delta['day_delta']>=0)&(day_delta['day_delta']<=8)).sum==0):
                    tempdf.loc[tempdf['date']==selldate,'revenue']=\
                        tempdf.loc[tempdf['date']==selldate]['revenue_2']
                else:

                    tempdf_trade['date_delta']=\
                        [x.days for x in (datetime.datetime.strptime(str(selldate), '%Y%m%d')-tempdf_trade['交易日期'])]

                    tempdf.loc[tempdf['date']==selldate,'revenue']=\
                        tempdf.loc[tempdf['date']==selldate]['revenue_2']+\
                        tempdf_trade[tempdf_trade['date_delta']>0].sort_values('date_delta').iloc[0]['确认净值']*tempdf_trade[tempdf_trade['date_delta']>0].sort_values('date_delta').iloc[0]['赎回份额']-tempdf_trade[tempdf_trade['date_delta']>0].fillna(0).sort_values('date_delta').iloc[0]['赎回费']

            if(jjdm!='1203'):
                tempdf['contr'] = tempdf['revenue'] / tempdf['资产净值']
            else:
                tempdf['contr'] = tempdf['revenue_2'] / tempdf['资产净值']
            cont.append(tempdf[['jjdm','date','contr','revenue','revenue_2']])

        cont =pd.concat(cont,axis=0).sort_values('date')
        hold_df['weight']=hold_df['weight'].astype(str).str.replace('%', '').astype(float) / 100

        hold_df=pd.merge(hold_df,cont,how='left',on=['date','jjdm'])

        cont = hold_df[['date', 'jjdm','jjjc', 'contr', 'weight','ejfl','jjfl','cpfl','风格偏好','规模偏好','二级策略']]

        mimic_nav = (cont.groupby('date').sum()['contr'] + 1).cumprod().to_frame('mimic_ret')\
                    * hold_df['累计单位净值'].iloc[0]
        mimic_nav['mimic_ret'] = [np.nan] + mimic_nav['mimic_ret'].iloc[0:-1].tolist()
        cont=pd.merge(cont,mimic_nav,how='left',on=['date'])
        cont['contribute_ret']=cont['contr']*cont['mimic_ret']/hold_df['累计单位净值'].iloc[0]


        return hold_df,cont

    def fund_attribution(self,hold_df,holding_time,if_prv):

        total_time= \
            (datetime.datetime.strptime(str(hold_df['date'].iloc[-1]),"%Y%m%d")-\
            datetime.datetime.strptime(str(hold_df['date'].iloc[0]),"%Y%m%d")).days

        total_trade_days=len(hold_df['date'].unique())

        if(if_prv):
            # prv ret
            mu_df = hold_df[hold_df['cpfl'] == '私募基金']
            mu_df['ejfl'] = mu_df['ejfl'].fillna(0).astype(str).str.replace("\.0", '')
            mu_df['jjfl'] = mu_df['jjfl'].fillna(0).astype(str).str.replace("\.0", '')
            jjfl_map = self.prv_jjflmap
            for index in jjfl_map.keys():
                mu_df.loc[mu_df['jjfl'] == index, 'jjfl'] = jjfl_map[index]
            ejfl_map = self.prv_ejflmap
            for index in ejfl_map.keys():
                mu_df.loc[mu_df['ejfl'] == index, 'ejfl'] = ejfl_map[index]

            #get jj ret from start to end
            # sql="select jjdm,jjjz,jzrq from st_hedge.t_st_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'"\
            #     .format(util.list_sql_condition(mu_df['jjdm'].unique().tolist()),
            #             hold_df['date'].iloc[0],hold_df['date'].iloc[-1])
            # nav=hbdb.db2df(sql,db='highuser').sort_values('jzrq')
            # nav=pd.merge(nav.drop_duplicates('jjdm',keep='last')[['jjdm','jjjz']]
            #              ,nav.drop_duplicates('jjdm',keep='first')[['jjdm','jjjz']]
            #              ,how='left',on='jjdm')

        else:

            # mutual ret
            mu_df = hold_df[hold_df['cpfl'] == '公募基金']
            mu_df['ejfl'] = mu_df['ejfl'].fillna(0).astype(str).str.replace("\.0", '')
            mu_df['jjfl'] = mu_df['jjfl'].fillna(0).astype(str).str.replace("\.0", '')
            jjfl_map = self.mu_jjflmap
            for index in jjfl_map.keys():
                mu_df.loc[mu_df['jjfl'] == index, 'jjfl'] = jjfl_map[index]
            ejfl_map = self.mu_ejflmap
            for index in ejfl_map.keys():
                mu_df.loc[mu_df['ejfl'] == index, 'ejfl'] = ejfl_map[index]

            # sql="select jjdm,jjjz,jzrq from st_fund.t_st_gm_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'"\
            #     .format(util.list_sql_condition(mu_df['jjdm'].unique().tolist()),
            #             hold_df['date'].iloc[0],hold_df['date'].iloc[-1])
            # nav=hbdb.db2df(sql,db='funduser').sort_values('jzrq')
            # nav=pd.merge(nav.drop_duplicates('jjdm',keep='last')[['jjdm','jjjz']]
            #              ,nav.drop_duplicates('jjdm',keep='first')[['jjdm','jjjz']]
            #              ,how='left',on='jjdm')

        mu_df['资产净值']=mu_df['资产净值'].astype(str).str.replace(',','').astype(float)
        mu_df['累计份额'] = mu_df['资产净值'] / mu_df['累计单位净值']

        out_df=[]

        for jjdm in mu_df['jjdm'].unique().tolist():

            tempdf=mu_df[mu_df['jjdm']==jjdm]
            tempdf['share_changed']=tempdf['累计份额'].diff()

            tempdf=pd.merge(mu_df[['date']].drop_duplicates('date').sort_values('date')
                            ,tempdf,how='left',on='date')
            tempdf=tempdf[tempdf['jjdm'].notnull()]
            tempdf.reset_index(inplace=True)
            tempdf.loc[0,'first_buy_price']=tempdf.loc[0]['jjjz']
            tempdf['index_diff'] = tempdf['index'].diff()

            for i in range(1,len(tempdf)):

                if(tempdf.loc[i]['index_diff']==1):
                    tempdf.loc[i,'first_buy_price']=tempdf.loc[i-1]['first_buy_price']
                else:
                    tempdf.loc[i, 'first_buy_price'] = tempdf.loc[i]['jjjz']

            for group in tempdf['first_buy_price'].unique().tolist():

                tempdf2=tempdf[tempdf['first_buy_price']==group]
                holding_days=len(tempdf2)
                # tempdf2=tempdf2[(tempdf2['share_changed'].abs()>=500000)
                #                 |(tempdf2['date']==tempdf2['date'].iloc[0])
                #                 |(tempdf2['date']==tempdf2['date'].iloc[-1])]
                # tempdf2['revenue']=tempdf2['value_increased']
                # tempdf2['revenue']=(tempdf2['revenue'].fillna(0).diff()).iloc[1:].tolist()+[np.nan]
                tempdf2['revenue'] = tempdf2['value_increased']
                tempdf2['contribute_ret'] = tempdf2['revenue'] / (tempdf2['累计单位净值'].iloc[0]*tempdf2['累计份额'])

                out_df.append(tempdf2)

                # mu_df.loc[(mu_df['jjdm']==jjdm)&
                #           (mu_df['date']>=tempdf2['date'].min())&
                #           (mu_df['date']<=tempdf2['date'].max()),'revenue'] = tempdf2['revenue'].sum()
                #
                # mu_df.loc[(mu_df['jjdm']==jjdm)&
                #           (mu_df['date']>=tempdf2['date'].min())&
                #           (mu_df['date']<=tempdf2['date'].max()),'contribute_ret'] = tempdf2['contribute_ret'].sum()
                #
                # mu_df.loc[(mu_df['jjdm']==jjdm)&
                #           (mu_df['date']>=tempdf2['date'].min())&
                #           (mu_df['date']<=tempdf2['date'].max()),'holding_days'] = holding_days/total_trade_days
                #
                # mu_df.loc[(mu_df['jjdm']==jjdm)&
                #           (mu_df['date']>=tempdf2['date'].min())&
                #           (mu_df['date']<=tempdf2['date'].max()),'ret'] = \
                #     (tempdf2['jjjz']/tempdf2['first_buy_price']-1).iloc[-1]

        #mu_df.drop_duplicates(['jjdm', 'contribute_ret'])
        out_df=pd.concat(out_df,axis=0)
        return out_df

    @staticmethod
    def attribution_by_class(fund_attribution,index_type_map):

        cpfl_att =pd.merge(fund_attribution.groupby('cpfl').sum()[['contribute_ret']]
                           ,fund_attribution.groupby(['date','cpfl']).sum()[['weight']].reset_index().groupby('cpfl').mean()[['weight']],how='left',on='cpfl')
        known_tr = abs(cpfl_att['contribute_ret'].sum())
        plot.plotly_jjpic_bar(cpfl_att[['contribute_ret']] / known_tr, '公私募基金收益分布')
        cpfl_att['ret'] = cpfl_att['contribute_ret']/(cpfl_att['weight'])
        plot.plotly_jjpic_bar(cpfl_att[['ret']], '公私募基金收益率分布')

        attack_asset_jjfl = ['股票型', '混合型','多空仓型']
        CTA_asset_jjfl = ['管理期货','套利型']
        statrage_att = \
            fund_attribution[fund_attribution['jjfl'].isin(attack_asset_jjfl
                                                           + CTA_asset_jjfl)]

        statrage_att = pd.merge(statrage_att.groupby('jjfl').sum()[['contribute_ret']]
                            , statrage_att.groupby(['date', 'jjfl']).sum()[['weight']].reset_index().groupby(
                'jjfl').mean()[['weight']], how='left', on='jjfl')

        plot.plotly_jjpic_bar(statrage_att[['contribute_ret']] / abs(statrage_att['contribute_ret'].sum()), '超一级策略收益分布')
        statrage_att['ret'] = statrage_att['contribute_ret']/statrage_att['weight']
        plot.plotly_jjpic_bar(statrage_att[['ret']], '超一级策略收益率分布')

        stock_asset_jjfl = ['主观多头', '量化多头', '偏股混合型', '灵活配置型', '普通股票型']

        plot.plotly_jjpic_bar((fund_attribution[fund_attribution['ejfl'].isin(stock_asset_jjfl
                                                                   )].drop_duplicates('jjdm')).groupby('ejfl').count()['jjdm'].to_frame('持仓数量').sort_values('持仓数量',ascending=False)
                        , '进攻性资产数量分布')

        stock_att = fund_attribution[fund_attribution['ejfl'].isin(stock_asset_jjfl
                                                                   )]
        stock_att = pd.merge(stock_att.groupby('ejfl').sum()[['contribute_ret']]
                            , stock_att.groupby(['date', 'ejfl']).sum()[['weight']].reset_index().groupby(
                'ejfl').mean()[['weight']], how='left', on='ejfl')


        # plot.plotly_pie(stock_att[['weight']],'进攻性资产持仓占比分布')
        plot.plotly_jjpic_bar(stock_att[['contribute_ret']] / abs(stock_att['contribute_ret'].sum()), '进攻性资产收益分布')
        stock_att['ret'] = stock_att['contribute_ret']/stock_att['weight']
        plot.plotly_jjpic_bar(stock_att[['ret']], '进攻性资产收益率分布')

        index_enhance_att = fund_attribution[fund_attribution['二级策略'].astype(str).str.contains('指数增强')]

        if(len(index_enhance_att)>0):


            index_enhance_att=pd.merge(index_enhance_att.groupby('二级策略').sum()[['contribute_ret']]
                            , index_enhance_att.groupby(['date', '二级策略']).sum()[['weight']].reset_index().groupby(
                '二级策略').mean()[['weight']], how='left', on='二级策略')

            index_enhance_att['ret'] = index_enhance_att['contribute_ret']/index_enhance_att['weight']


        style_att = pd.merge(fund_attribution.groupby('风格偏好').sum()[['contribute_ret']]
                            , fund_attribution.groupby(['date', '风格偏好']).sum()[['weight']].reset_index().groupby(
                '风格偏好').mean()[['weight']], how='left', on='风格偏好')

        style_att['ret'] = style_att['contribute_ret'] / style_att['weight']
        plot.plotly_pie(style_att[['weight']],'成长价值风格持仓成本分布')
        plot.plotly_jjpic_bar(style_att[['contribute_ret']] / abs(style_att['contribute_ret'].sum()), '成长价值风格收益分布')


        fund_attribution.loc[fund_attribution['规模偏好'].astype(str).str.contains('大'),'规模偏好']='大'
        fund_attribution.loc[fund_attribution['规模偏好'].astype(str).str.contains('中'),'规模偏好']='中小'
        fund_attribution.loc[fund_attribution['规模偏好'].astype(str).str.contains('小'),'规模偏好']='中小'


        size_att = pd.merge(fund_attribution.groupby('规模偏好').sum()[['contribute_ret']]
                            , fund_attribution.groupby(['date', '规模偏好']).sum()[['weight']].reset_index().groupby(
                '规模偏好').mean()[['weight']], how='left', on='规模偏好')
        size_att['ret'] = size_att['contribute_ret'] / size_att['weight']
        plot.plotly_pie(size_att[['weight']],'市值风格持仓成本分布')
        plot.plotly_jjpic_bar(size_att[['contribute_ret']] / abs(size_att['contribute_ret'].sum()), '市值风格收益分布')

        attribution_by_class=[cpfl_att,statrage_att,stock_att,index_enhance_att,style_att,size_att]
        attribution_by_class = pd.concat(attribution_by_class, axis=0)


        return  attribution_by_class

    @staticmethod
    def generate_index_enhance_index(start_date,end_date):

        quant_pool_in = \
        pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-08\私募量化基金池 - 202207.xlsx"
                      , sheet_name='量化池列表')[['入池时间', '基金代码', '二级策略']]
        quant_pool_out = \
        pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-08\私募量化基金池 - 202207.xlsx"
                      , sheet_name='出池记录')[['入池时间', '基金代码', '出池时间', '二级策略']]
        quant_pool = pd.concat([quant_pool_out, quant_pool_in], axis=0)
        quant_pool = quant_pool[(quant_pool['二级策略'].isin(['500指数增强', '1000指数增强', '300指数增强']))]
        quant_pool['入池时间'] = quant_pool['入池时间'].astype(str).str.replace('-', '').str[0:6]
        quant_pool['出池时间'] = quant_pool['出池时间'].astype(str).str.replace('-', '').str[0:6]
        quant_pool.drop_duplicates('基金代码', inplace=True)

        sql = "select jjdm,hb1y,tjyf from st_hedge.t_st_sm_yhb where jjdm in ({0}) and tjyf>='{1}' and tjyf<='{2}' and hb1y!=99999" \
            .format(util.list_sql_condition(quant_pool['基金代码'].tolist())
                    ,start_date,end_date)
        quant_pool_nav = hbdb.db2df(sql, db='highuser')
        quant_pool_nav = pd.merge(quant_pool_nav, quant_pool, how='left'
                                  , left_on='jjdm', right_on='基金代码')
        quant_pool_nav = quant_pool_nav[(quant_pool_nav['入池时间'] < quant_pool_nav['tjyf'])
                                        & (quant_pool_nav['出池时间'] >= quant_pool_nav['tjyf'])]
        quant_pool_nav = quant_pool_nav.groupby(['二级策略', 'tjyf']).mean()['hb1y'].to_frame('量化池') / 100

        quant_pool_nav=quant_pool_nav.reset_index().pivot_table('量化池', 'tjyf', '二级策略')

        return (quant_pool_nav+1).cumprod()

    def get_bmk_return(self,start_date,end_date):


        # get market mutual index return

        sql = """select zqdm,jyrq,spjg from st_market.t_st_zs_hqql 
        where jyrq>='{0}' and jyrq<='{1}' and zqdm in ('885001','399370','399371','399314','399315','399316','881001','399311','CI0077','CBA00301')""" \
            .format(str(int(start_date[0:4])-3)+start_date[4:], end_date)

        mu_index_ret = hbdb.db2df(sql, db='alluser').pivot_table('spjg', 'jyrq', 'zqdm')

        mu_index_ret.rename(columns={
                                     '885001':'公募偏股',
                                     '399370':'国证成长',
                                     '399371':'国证价值',
                                     '399314':'国证大盘',
                                     '399315':'国证中盘',
                                     '399316':'国证小盘',},inplace=True)


        for col in mu_index_ret.columns:
            mu_index_ret[col]=mu_index_ret[col]/mu_index_ret[col].iloc[0]

        for col in ['国证大盘', '国证中盘', '国证小盘', '国证成长', '国证价值']:
            mu_index_ret[col+'_累计超额'] = mu_index_ret[col]-mu_index_ret['399311']

        for col in ['公募偏股']:
            mu_index_ret[col+'_累计超额'] = mu_index_ret[col]-mu_index_ret['881001']

        for col in ['国证大盘', '国证中盘', '国证小盘', '国证成长', '国证价值','公募偏股']:
            mu_index_ret[col+'_rank']=mu_index_ret[col+'_累计超额'].rolling(500,1).apply(rolling_rank)
            mu_index_ret.drop(col+'_累计超额',axis=1,inplace=True)


        sql = """select zsdm,jyrq,spjg from st_hedge.t_st_sm_zhmzs 
        where jyrq>='{0}' and jyrq<='{1}' and zsdm in ('HB0018','HB1001','HB1002')""" \
            .format(str(int(start_date[0:4])-3)+start_date[4:], end_date)

        howbuy_index_ret = hbdb.db2df(sql, db='highuser').pivot_table('spjg', 'jyrq', 'zsdm').fillna(1000)
        howbuy_index_ret.rename(columns={'HB0018':'CTA',
                                     'HB1001':'主观多头',
                                     'HB1002':'量化多头'},inplace=True)
        mu_index_ret.index=mu_index_ret.index.astype(str)
        for col in howbuy_index_ret.columns:
            howbuy_index_ret[col]=howbuy_index_ret[col]/howbuy_index_ret[col].iloc[0]

        howbuy_index_ret=pd.merge(howbuy_index_ret,mu_index_ret[['881001']],how='left',
                                  left_index=True,right_index=True)

        for col in howbuy_index_ret.columns:
            howbuy_index_ret[col]=howbuy_index_ret[col]/howbuy_index_ret[col].iloc[0]

        for col in ['CTA', '主观多头', '量化多头']:
            howbuy_index_ret[col+'_累计超额'] = howbuy_index_ret[col]-mu_index_ret['881001']

        for col in ['CTA', '主观多头', '量化多头']:
            howbuy_index_ret[col+'_rank']=howbuy_index_ret[col+'_累计超额'].rolling(100,1).apply(rolling_rank)
            howbuy_index_ret.drop(col+'_累计超额',axis=1,inplace=True)

        howbuy_index_ret.drop('881001', axis=1, inplace=True)
        howbuy_index_ret=howbuy_index_ret.loc[start_date:]

        mu_index_ret=mu_index_ret.loc[start_date:]


        index_enhance_index = \
            self.generate_index_enhance_index(str(int(start_date[0:4])-3)+start_date[4:6]
                                              , str(end_date)[0:6])
        for col in index_enhance_index.columns.tolist():
            index_enhance_index[col+'_rank']=index_enhance_index[col].rolling(24,1).apply(rolling_rank)

        index_enhance_index=index_enhance_index.loc[start_date:]


        return  howbuy_index_ret,mu_index_ret,index_enhance_index

    @staticmethod
    def brinson_wise_analysis(fund_attribution,trade_ret,howbuy_index_ret
                              , mu_index_ret, index_enhance_index):

        return_table_list=[]

        #calculate ideal asset weight by BLM assumption that all asset allocation submit to mean variance model

        prv_stock_ret= \
            (np.power((howbuy_index_ret['主观多头'].iloc[-1]/ howbuy_index_ret['主观多头'].iloc[0])
                     ,52/len(howbuy_index_ret))-1)

        mu_stock_ret= \
            (np.power((mu_index_ret['公募偏股'].iloc[-1]/ mu_index_ret['公募偏股'].iloc[0])
                     ,250/len(mu_index_ret))-1)

        prv_quant_ret= \
            (np.power((howbuy_index_ret['量化多头'].iloc[-1]/ howbuy_index_ret['量化多头'].iloc[0])
                     ,52/len(howbuy_index_ret))-1)

        if (prv_stock_ret < 0 or mu_stock_ret < 0 or prv_quant_ret < 0):

            min_ret=np.min([prv_stock_ret,mu_stock_ret,prv_quant_ret])
            prv_stock_ret=prv_stock_ret-min_ret+0.03
            mu_stock_ret = mu_stock_ret - min_ret+0.03
            prv_quant_ret = prv_quant_ret - min_ret+0.03


        prv_stock_sharp= \
            prv_stock_ret/\
            (howbuy_index_ret['主观多头'].pct_change().std()*np.sqrt(52))

        mu_stock_sharp= \
            mu_stock_ret/\
            (mu_index_ret['公募偏股'].pct_change().std()*np.sqrt(250))

        prv_quant_sharp= \
            prv_quant_ret/\
            (howbuy_index_ret['量化多头'].pct_change().std()*np.sqrt(52))


        total_sharp=prv_stock_sharp+mu_stock_sharp+prv_quant_sharp
        prv_stock_bmk_w=prv_stock_sharp/total_sharp
        mu_stock_bmk_w = mu_stock_sharp / total_sharp
        prv_quant_bmk_w = prv_quant_sharp / total_sharp


        #make all index monthly

        howbuy_index_ret['tjyf']= howbuy_index_ret.index.astype(str).str[0:6]
        mu_index_ret['tjyf']=mu_index_ret.index.astype(str).str[0:6]

        index_ret_monthly=pd.merge(howbuy_index_ret.drop_duplicates('tjyf',keep='last')[['CTA','主观多头','量化多头','tjyf']]
                                          ,howbuy_index_ret.drop_duplicates('tjyf',keep='first')[['CTA','主观多头','量化多头','tjyf']]
                                          ,how='left',on='tjyf')
        index_ret_monthly=pd.merge(index_ret_monthly,mu_index_ret.drop_duplicates('tjyf',keep='last')[['公募偏股','tjyf']]
                                          ,how='left',on='tjyf')
        index_ret_monthly=pd.merge(index_ret_monthly,mu_index_ret.drop_duplicates('tjyf',keep='first')[['公募偏股','tjyf']]
                                          ,how='left',on='tjyf')

        for index in ['CTA','主观多头','量化多头','公募偏股']:

            index_ret_monthly[index]=\
                index_ret_monthly[index+'_x']/index_ret_monthly[index+'_y']-1

        index_ret_monthly=index_ret_monthly[['tjyf','CTA','主观多头','量化多头','公募偏股']]


        # equit asset return reasoning


        equit_att = \
            (fund_attribution[fund_attribution['ejfl'].isin(['主观多头'
                                                               , '量化多头', '指数增强型', '偏股混合型',
                                                            '灵活配置型', '普通股票型'])].groupby(['date','ejfl']).sum()).reset_index()

        equit_att['ejfl']=[x.replace('指数增强型','量化多头') for x in equit_att['ejfl']]
        equit_att['ejfl'] = [x.replace('灵活配置型', '公募偏股') for x in equit_att['ejfl']]
        equit_att['ejfl'] = [x.replace('偏股混合型', '公募偏股') for x in equit_att['ejfl']]
        equit_att['ejfl'] = [x.replace('普通股票型', '公募偏股') for x in equit_att['ejfl']]
        equit_att['tjyf']=equit_att['date'].astype(str).str[0:6]
        equit_att=pd.merge(equit_att.groupby(['tjyf','ejfl']).sum()[['contribute_ret']]
                 ,equit_att.groupby(['tjyf','ejfl']).mean()[['weight']],how='left',on=['tjyf','ejfl'])

        equit_att['ret']=equit_att['contribute_ret']/equit_att['weight']
        equit_att=equit_att.reset_index()
        equit_att=pd.merge(equit_att,
                           equit_att.groupby('tjyf').sum()[['weight']].rename(columns={'weight':'total_weight'}),
                           how='left',on='tjyf')
        equit_att['weight'] = equit_att['weight'] / equit_att['total_weight']

        equit_att=pd.merge(equit_att.pivot_table('ret','tjyf','ejfl')
                 ,equit_att.pivot_table('weight','tjyf','ejfl')
                 ,how='left',on='tjyf')
        equit_att=pd.merge(equit_att,index_ret_monthly,how='left',on='tjyf')

        # arrange the bmk weight
        equit_att['主观多头bmk_w'] = prv_stock_bmk_w
        equit_att['量化股票bmk_w'] = prv_quant_bmk_w
        equit_att['公募偏股bmk_w'] = mu_stock_bmk_w


        # return allocation
        total_extra_ret=(equit_att[['主观多头_x', '公募偏股_x', '量化多头_x']].fillna(0).values * equit_att[['主观多头_y', '公募偏股_y', '量化多头_y']].fillna(0).values \
        -equit_att[['主观多头', '量化多头', '公募偏股']].values * equit_att[['主观多头bmk_w', '量化股票bmk_w', '公募偏股bmk_w']].values).sum(axis=1)
        allocation_extraret = ((equit_att[['主观多头_y', '公募偏股_y', '量化多头_y']].fillna(0).values-\
                              equit_att[['主观多头bmk_w', '量化股票bmk_w', '公募偏股bmk_w']].values)*equit_att[['主观多头', '量化多头', '公募偏股']].values).sum(axis=1)
        selection_extraret=pd.DataFrame(data=(equit_att[['主观多头bmk_w', '量化股票bmk_w', '公募偏股bmk_w']].values * (equit_att[['主观多头_x', '公募偏股_x', '量化多头_x']].values-
                                                                                          equit_att[['主观多头', '量化多头', '公募偏股']].values))).fillna(0).sum(axis=1)
        brinson_his=pd.DataFrame()
        brinson_his['date']=equit_att['tjyf'].tolist()
        brinson_his['总超额'] =total_extra_ret
        brinson_his['配置收益'] =allocation_extraret
        brinson_his['择基收益'] = selection_extraret.values.tolist()
        brinson_his['其他收益'] =brinson_his['总超额']-brinson_his['配置收益']-brinson_his['择基收益']
        brinson_his.set_index('date',inplace=True)
        brinson_his=brinson_his.cumsum()

        plot.plotly_line_style(brinson_his,'进攻性资产收益拆解')

        equit_att.to_excel('进攻性资产brinsion数据.xlsx',index=False)

        index_enhance_att = \
            (fund_attribution[fund_attribution['二级策略'].astype(str).str.contains('指数增强')].groupby(['date','二级策略']).sum()).reset_index()

        if(len(index_enhance_att)>0):

            index_enhance_index = index_enhance_index.pct_change()


            index_enhance_att['tjyf'] = index_enhance_att['date'].astype(str).str[0:6]
            index_enhance_att = pd.merge(index_enhance_att.groupby(['tjyf', '二级策略']).sum()[['contribute_ret']]
                                         , index_enhance_att.groupby(['tjyf', '二级策略']).mean()[['weight']], how='left',
                                         on=['tjyf', '二级策略'])

            index_enhance_att['ret'] = index_enhance_att['contribute_ret'] / index_enhance_att['weight']
            index_enhance_att = index_enhance_att.reset_index()
            index_enhance_att = pd.merge(index_enhance_att,
                                 index_enhance_att.groupby('tjyf').sum()[['weight']].rename(columns={'weight': 'total_weight'}),
                                 how='left', on='tjyf')
            index_enhance_att['weight'] = index_enhance_att['weight'] / index_enhance_att['total_weight']

            index_enhance_att = pd.merge(index_enhance_att.pivot_table('ret', 'tjyf', '二级策略')
                                 , index_enhance_att.pivot_table('weight', 'tjyf', '二级策略')
                                 , how='left', on='tjyf')
            index_enhance_att = pd.merge(index_enhance_att, index_enhance_index[['1000指数增强','500指数增强','300指数增强']],
                                         how='left', on='tjyf')
            index_enhance_att.reset_index(inplace=True)
            # arrange the bmk weight
            index_enhance_att['1000指数增强bmk_w'] = 0.1
            index_enhance_att['500指数增强bmk_w'] = 0.8
            index_enhance_att['300指数增强bmk_w'] = 0.1

            for asset in ['1000指数增强', '500指数增强', '300指数增强']:

                if(asset+'_x' not in index_enhance_att.columns):
                    index_enhance_att[asset+'_x']=np.nan
                    index_enhance_att[asset + '_y'] = np.nan

            # return allocation
            total_extra_ret = (index_enhance_att[['1000指数增强_x', '500指数增强_x', '300指数增强_x']].fillna(0).values * index_enhance_att[
                ['1000指数增强_y', '500指数增强_y', '300指数增强_y']].fillna(0).values \
                               - index_enhance_att[['1000指数增强', '500指数增强', '300指数增强']].values * index_enhance_att[
                                   ['1000指数增强bmk_w', '500指数增强bmk_w', '300指数增强bmk_w']].values).sum(axis=1)
            allocation_extraret = ((index_enhance_att[['1000指数增强_y', '500指数增强_y', '300指数增强_y']].fillna(0).values - \
                                    index_enhance_att[['1000指数增强bmk_w', '500指数增强bmk_w', '300指数增强bmk_w']].values) * index_enhance_att[
                                       ['1000指数增强', '500指数增强', '300指数增强']].values).sum(axis=1)
            selection_extraret = pd.DataFrame(data=(index_enhance_att[['1000指数增强bmk_w', '500指数增强bmk_w', '300指数增强bmk_w']].values * (
                        index_enhance_att[['1000指数增强_x', '500指数增强_x', '300指数增强_x']].values -
                        index_enhance_att[['1000指数增强', '500指数增强', '300指数增强']].values))).fillna(0).sum(axis=1)
            brinson_his = pd.DataFrame()
            brinson_his['date'] = index_enhance_att['tjyf'].tolist()
            brinson_his['总超额'] = total_extra_ret
            brinson_his['配置收益'] = allocation_extraret
            brinson_his['择基收益'] = selection_extraret.values.tolist()
            brinson_his['其他收益'] = brinson_his['总超额'] - brinson_his['配置收益'] - brinson_his['择基收益']
            brinson_his.set_index('date', inplace=True)
            brinson_his = brinson_his.cumsum()

            plot.plotly_line_style(brinson_his, '指数增强收益拆解')

            index_enhance_att.to_excel('指数增强资产brinsion数据.xlsx', index=False)


    @staticmethod
    def fund_lable_analysis(hold_df):

        hold_df['资产净值']=hold_df['资产净值'].astype(str).str.replace(',','').astype(float)


        def mutual_lable_analysis(hold_df):

            mu_lable=hold_df[(hold_df['cpfl']=='公募基金')
                             &(hold_df['ejfl'].isin([13,35,37]))][['date'
                ,'jjdm','jjjc','jjjz','quant','资产净值']]

            #read style lable from local db

            max_asofdate=pd.read_sql("select max(asofdate) as date from jjpic_value_p_hbs"
                                     ,con=localdb)['date'][0]
            sql="SELECT jjdm,`风格偏好`,`成长绝对暴露(持仓)`,`价值绝对暴露(持仓)` from jjpic_value_p_hbs where jjdm in ({0}) and  asofdate='{1}'"\
                .format(util.list_sql_condition(mu_lable['jjdm'].unique().tolist()),max_asofdate)
            value_pic=pd.read_sql(sql,con=localdb)

            sql="SELECT jjdm,`规模偏好`,`大盘绝对暴露(持仓)`,`中盘绝对暴露(持仓)`,`小盘绝对暴露(持仓)` from jjpic_size_p_hbs where jjdm in ({0}) and  asofdate='{1}'"\
                .format(util.list_sql_condition(mu_lable['jjdm'].unique().tolist()),max_asofdate)
            size_pic=pd.read_sql(sql,con=localdb)


            #read industry type lable from local db
            max_asofdate=pd.read_sql("select max(asofdate) as date from jjpic_industry_p"
                                     ,con=localdb)['date'][0]
            sql="SELECT jjdm,`一级行业类型` from jjpic_industry_p where jjdm in ({0}) and  asofdate='{1}'"\
                .format(util.list_sql_condition(mu_lable['jjdm'].unique().tolist()),max_asofdate)
            industry_pic=pd.read_sql(sql,con=localdb)

            mu_lable=pd.merge(mu_lable,value_pic,how='left',on='jjdm')
            mu_lable = pd.merge(mu_lable, size_pic, how='left', on='jjdm')
            mu_lable = pd.merge(mu_lable, industry_pic, how='left', on='jjdm')

            mu_lable['持仓权重']=mu_lable['quant']*mu_lable['jjjz']/mu_lable['资产净值']

            for col in ['成长绝对暴露(持仓)','价值绝对暴露(持仓)','大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)']:
                mu_lable[col]=mu_lable[col]*mu_lable['持仓权重']

            value_pic=mu_lable.groupby(['date',
                                        '风格偏好']).sum()[['持仓权重']].reset_index().pivot_table('持仓权重','date','风格偏好').fillna(0)

            value_pic2=mu_lable.groupby('date').sum()[['成长绝对暴露(持仓)','价值绝对暴露(持仓)']]
            size_pic = mu_lable.groupby(['date'
                                            , '规模偏好']).sum()[['持仓权重']].reset_index().pivot_table('持仓权重','date','规模偏好').fillna(0)

            size_pic2 = mu_lable.groupby('date').sum()[['大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)']]
            industry_pic = mu_lable.groupby(['date'
                                                , '一级行业类型']).sum()[['持仓权重']].reset_index().pivot_table('持仓权重','date','一级行业类型').fillna(0)


            return  value_pic,value_pic2,size_pic,size_pic2,industry_pic

        def prv_lable_analysis(hold_df):

            prv_lable = hold_df[(hold_df['cpfl'] == '私募基金')
                                & (hold_df['ejfl'].isin([1001]))][['date'
                , 'jjdm', 'jjjc', 'jjjz', 'quant', '资产净值']]

            file_name_list = os.listdir(r"E:\GitFolder\docs\净值标签")
            file_name_list.sort()
            fold_name = ''
            for name in file_name_list:
                if (name.startswith('全部私募打标结果')):
                    fold_name = name
                    break
            prv_pic = pd.read_excel(r"E:\GitFolder\docs\净值标签\{}".format(fold_name), sheet_name='数据')
            prv_lable = pd.merge(prv_lable, prv_pic[['jjdm', '大小盘', '成长价值']]
                                 , how='left', on='jjdm')
            return  prv_lable

        value_pic,value_pic2,size_pic,size_pic2,industry_pic=mutual_lable_analysis(hold_df)

        data, layout=plot.plotly_area(value_pic.T*100,'公募风格类型分布时序'
                                      ,range_upper=value_pic.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

        data, layout=plot.plotly_area(value_pic2.T*100,'公募持仓打穿后成长价值分布'
                                      ,range_upper=value_pic2.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

        data, layout=plot.plotly_area(size_pic.T*100, '公募市值类型分布时序'
                                      ,range_upper=size_pic.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

        data, layout=plot.plotly_area(size_pic2.T*100,'公募持仓打穿后大中小盘分布'
                                      ,range_upper=size_pic2.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

        data, layout=plot.plotly_area(industry_pic.T*100, '公募行业类型分布时序',
                                      range_upper=industry_pic.sum(axis=1).max()*110)
        plot.plot_render(data, layout)

    @staticmethod
    def calculate_holding_time(inputdf):

        hold_df=inputdf.copy()
        #take attack asset only
        #
        # hold_df=hold_df[(hold_df['jjdm'] != '000nan') &
        #         ((hold_df['jjfl'].astype(str).str.startswith('1'))
        #          | (hold_df['ejfl'].astype(str).str.startswith('35'))
        #          | (hold_df['ejfl'].astype(str).str.startswith('37'))
        #          |(hold_df['cpfl'].astype(str)=='私募基金'))]

        hold_df=hold_df[(hold_df['jjdm'] != '000nan')]


        jjdm_list=hold_df[hold_df['jjdm']!='000nan'].drop_duplicates(['jjdm'])[['jjdm','cpfl','ejfl']]
        for jjdm in jjdm_list['jjdm'].tolist():
            tempdf=hold_df[hold_df['jjdm']==jjdm]
            tempdf['last_day_quant']=[np.nan]+tempdf['quant'].iloc[0:-1].tolist()
            tempdf['last_day_quant']=tempdf['last_day_quant'].fillna(0)
            tempdf.loc[(tempdf['last_day_quant']<=1000)&
                       (tempdf['quant']>1000),'trade_signal']=1
            tempdf.loc[(tempdf['last_day_quant']>1000)&
                       (tempdf['quant']<=1000),'trade_signal']=-1


            # avg_jjjzc=tempdf['累计份额']


            tempdf2=tempdf[tempdf['trade_signal'].notnull()]
            if(len(tempdf2)>1):
                tempdf2['date']=[datetime.datetime.strptime(str(x),"%Y%m%d")  for x in tempdf2['date']]
                jjdm_list.loc[jjdm_list['jjdm']==jjdm,'holding_days']=tempdf2['date'].diff().mean().days
            else:
                jjdm_list.loc[jjdm_list['jjdm']==jjdm,'holding_days']=\
                    (datetime.datetime.strptime(str(tempdf['date'].iloc[-1]),"%Y%m%d")-datetime.datetime.strptime(str(tempdf['date'].iloc[0]),"%Y%m%d")).days
            # jjdm_list.loc[jjdm_list['jjdm'] == jjdm, '资产份额_adj']=avg_jjjzc

        avg_hld_days=jjdm_list['holding_days'].mean()
        mu_avg_hld_days=jjdm_list[jjdm_list['cpfl']=='公募基金']['holding_days'].mean()
        prv_avg_hld_days=jjdm_list[jjdm_list['cpfl']=='私募基金']['holding_days'].mean()

        outdf=pd.DataFrame(data=[[avg_hld_days,mu_avg_hld_days,prv_avg_hld_days]]
                           ,columns=['进攻性资产平均持有时间','私募平均持有时间','公募平均持有时间'])

        return outdf,jjdm_list

    @staticmethod
    def style_analysis(hold_df,cb_w=False):

        if(cb_w):
            style_df = hold_df.groupby(['date', '风格偏好']).sum()[['cb_w']].reset_index().rename(columns={'cb_w':'weight'})
        else:
            style_df=hold_df.groupby(['date', '风格偏好']).sum()[['weight']].reset_index()

        style_df=\
            pd.merge(style_df,style_df.groupby('date').sum()['weight'].to_frame('total_w'),how='left',on='date')
        style_df['weight']=style_df['weight']/style_df['total_w']
        style_df=style_df.pivot_table('weight','date',
                                      '风格偏好')

        data, layout=plot.plotly_area(style_df.T*100,'',range_upper=100)
        plot.plot_render(data, layout)

        style_df=style_df.reset_index(drop=False).rename(columns={'date': '日期'})
        style_df['日期']=style_df['日期'].astype(str)
        weight_col=style_df.columns.tolist()
        weight_col.remove('日期')
        style_summary=find_weight_change_point(style_df, weight_col,index_list=['399370','399371'])
        for col in ['权重均值', '权重中值', '偏离均值', '偏离最大']+['399370','399371']:
            style_summary[col]=style_summary[col].map("{:.2%}".format)
        plot.plotly_table(style_summary.reset_index(),1200,'')

        return  style_df

    def holding_analysis(self,dir,start_date=None):

        hold_df=pd.read_excel(dir)
        hold_df['资产份额']=hold_df['资产份额'].str.replace(',','').astype(float)
        hold_df['资产净值'] = hold_df['资产净值'].str.replace(',', '').astype(float)
        if(start_date is not None):
            hold_df=hold_df[hold_df['date']>=int(start_date)]


        #remove the money asset

        #read trade info



        #mark prv fix income fund as prv
        hold_df.loc[(hold_df['cpfl'].isnull()) & (hold_df['jjdm'] != '000nan'), 'cpfl'] = 4
        hold_df.loc[hold_df['cpfl']==4,'cpfl']='私募基金'
        hold_df.loc[hold_df['cpfl'] == 2, 'cpfl'] = '公募基金'

        quant_pool_in = \
        pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-08\私募量化基金池 - 202207.xlsx"
                      , sheet_name='量化池列表')[['入池时间', '基金代码', '二级策略']].drop_duplicates('基金代码')
        hold_df=pd.merge(hold_df,quant_pool_in[['基金代码','二级策略']]
                         ,how='left',left_on='jjdm',right_on='基金代码')

        hold_df,fund_attribution=self.fund_attribution_new(hold_df)

        # holding_time_table,holding_time_details=self.calculate_holding_time(hold_df)
        # plot.plotly_table(holding_time_table,1000,'')
        #
        # prv_attribution=self.fund_attribution(hold_df,holding_time_details,if_prv=True)
        # mutual_attribution=self.fund_attribution(hold_df,holding_time_details,if_prv=False)
        # fund_attribution=pd.concat([prv_attribution,mutual_attribution],axis=0).reset_index(drop=True)


        #annuallize ret

        # fund_attribution['contribute_ret']=np.power(fund_attribution['contribute_ret']+1,365/total_time)-1
        # fund_attribution['cb_w'] = np.power(fund_attribution['cb_w'] + 1, 365 / total_time) - 1


        #for tempary use : since we can not get the specific ret contribution, we can only add the trade ret on each asset based on it weight
        rel_ret=hold_df['累计单位净值'].iloc[-1]/hold_df['累计单位净值'].iloc[0]-1
        explained_ret=fund_attribution['contribute_ret'].sum()
        trade_ret=rel_ret-explained_ret


        style_weight_his=self.style_analysis(hold_df,cb_w=False)
        style_weight_his.to_excel(dir.replace('基金持仓数据','风格权重时序'))
        #self.style_analysis(hold_df, fund_attribution, cb_w=True)

        hold_df['ym']=hold_df['date'].astype(str).str[0:6]
        hold_df['month']=hold_df['date'].astype(str).str[4:6]

        first_st_his=(hold_df.groupby(['date','ejfl']).sum()[['weight']]*100).reset_index().pivot_table('weight','ejfl','date').fillna(0)
        data, layout=plot.plotly_area(first_st_his,'test')
        plot.plot_render(data, layout)

        hold_by_jj=\
            hold_df[(hold_df['date'].isin(hold_df.drop_duplicates('ym', keep='last')['date'].tolist()))
                &(hold_df['month'].isin(['03','06','09','12']))].pivot_table('weight','jjjc','date').fillna(0)
        for col in hold_by_jj.columns.tolist():
            hold_by_jj[col]=hold_by_jj[col].map("{:.2%}".format)
        hold_by_jj.to_excel(dir.replace('基金持仓数据','季度持仓by基金'))
        plot.plotly_table(hold_by_jj.reset_index(),200*len(hold_by_jj.columns),'')

        tempdf_hold=hold_df[(hold_df['date'].isin(hold_df.drop_duplicates('ym', keep='last')['date'].tolist()))
                &(hold_df['month'].isin(['03','06','09','12']))]
        tempdf_hold['name_weight']=tempdf_hold['jjjc']+"("+tempdf_hold['weight'].fillna(0).map("{:.2%}".format)+")"

        hold_by_date=[]
        for ym in tempdf_hold['ym'].unique():
            hold_by_date.append(pd.DataFrame(data=tempdf_hold[(tempdf_hold['ym']==ym)
                                                              &(tempdf_hold['weight']>0)].sort_values('weight',ascending=False)['name_weight'].tolist(),columns=[ym]))
        hold_by_date=pd.concat(hold_by_date,axis=1)
        hold_by_date.to_excel(dir.replace('基金持仓数据','季度持仓by日期'))
        plot.plotly_table(hold_by_date,200*len(hold_by_jj.columns),'')


        attribution_by_class=self.attribution_by_class(fund_attribution,self.index_enhance_manual_map)

        howbuy_index_ret, mu_index_ret, index_enhance_index=self.get_bmk_return(str(hold_df['date'].iloc[0])
                                                                                ,str(hold_df['date'].iloc[-1]))

        fund_attribution.to_excel(dir.replace('基金持仓数据','个基收益贡献'),index=False)
        attribution_by_class.to_excel(dir.replace('基金持仓数据','各级资产收益贡献'),index=False)

        self.brinson_wise_analysis(fund_attribution,trade_ret,howbuy_index_ret
                              , mu_index_ret, index_enhance_index)


        #self.fund_lable_analysis(hold_df)


    #trading analysis part


    def trade_date_preprocessing(self,weight_his_dir,hold_data_dir,start_date):

        #read stratage weight history data from local file

        stratage_weight_his=pd.read_excel(weight_his_dir)
        stratage_weight_his['日期']=stratage_weight_his['日期'].astype(str)
        stratage_weight_his=stratage_weight_his[stratage_weight_his['日期']>=start_date]
        stratage_weight_his.columns=[x.replace('(%)','占比') for x in stratage_weight_his.columns]
        stratage_weight_his['沪深300']=(stratage_weight_his['沪深300占比']+100)/100

        #get bmk index ret
        howbuy_index_ret,mu_index_ret,index_enhance_index=\
            self.get_bmk_return( stratage_weight_his['日期'].iloc[0]
                             ,stratage_weight_his['日期'].iloc[-1])
        mu_index_ret.index=mu_index_ret.index.astype(str)

        for col in howbuy_index_ret.columns:
            if('rank' not in col):
                howbuy_index_ret[col]=howbuy_index_ret[col]/howbuy_index_ret[col].iloc[0]
        for col in mu_index_ret.columns:
            if ('rank' not in col):
                mu_index_ret[col]=mu_index_ret[col]/mu_index_ret[col].iloc[0]


        #read fund class info and FOF nav info
        hold_df = pd.read_excel(hold_data_dir)[['jjdm','cpfl','jjfl','ejfl','风格偏好', '规模偏好']].drop_duplicates('jjdm',keep='last')
        hold_df.loc[hold_df['cpfl'].isnull(),'cpfl']=4
        fof_nav= pd.read_excel(hold_data_dir)[['date','资产净值','资产份额','单位净值']].drop_duplicates('date',keep='last')
        fof_nav['date']=fof_nav['date'].astype(str)
        for col in ['资产净值','资产份额','单位净值']:
            fof_nav[col]=\
                fof_nav[col].astype(str).str.replace(',','').astype(float)


        #read trading flow
        trading_detail=self.trading_flow[self.trading_flow['产品名称']==product]
        trading_detail=trading_detail[trading_detail['交易日期']>=start_date]
        trading_detail['投资基金代码']=trading_detail['投资基金代码'].astype(str)
        trading_detail=pd.merge(trading_detail,hold_df
                                ,how='left',left_on='投资基金代码',right_on='jjdm').drop('投资基金代码',axis=1)
        trading_detail=pd.merge(trading_detail,fof_nav
                                ,how='left',left_on='交易日期',right_on='date').drop('交易日期',axis=1)

        #remove money asset
        trading_detail=trading_detail[(trading_detail['jjfl']!=7)
                                      &(trading_detail['jjfl'].notnull())]

        #data cleaning
        trading_detail.loc[(trading_detail['cpfl'].isnull())
                           &(trading_detail['投资基金'].str.startswith('CTA')),'jjfl']='8'
        trading_detail.loc[(trading_detail['cpfl'].isnull())
                           &(trading_detail['投资基金'].str.startswith('CTA')),'cpfl']=4
        trading_detail['ejfl']=trading_detail['ejfl'].fillna(0).astype(str).str.replace("\.0", '')
        trading_detail['jjfl'] = trading_detail['jjfl'].fillna(0).astype(str).str.replace("\.0", '')
        trading_detail[['认申购金额','赎回份额','确认净值','单位净值']]=\
            trading_detail[['认申购金额','赎回份额','确认净值','单位净值']].astype(float)
        trading_detail['资产净值']=trading_detail['资产净值'].astype(str).str.replace(',', '').astype(float)
        trading_detail['资产份额']=trading_detail['资产份额'].astype(str).str.replace(',', '').astype(float)

        #rename the fund class name by chinese
        trading_detail.loc[trading_detail['cpfl']==4,'jjfl']\
            =[self.prv_jjflmap[x] for x in trading_detail[trading_detail['cpfl']==4]['jjfl']]
        trading_detail.loc[trading_detail['cpfl']==4,'ejfl']\
            =[self.prv_ejflmap[x] for x in trading_detail[trading_detail['cpfl']==4]['ejfl']]

        trading_detail.loc[trading_detail['cpfl']==2,'jjfl']\
            =[self.mu_jjflmap[x] for x in trading_detail[trading_detail['cpfl']==2]['jjfl']]
        trading_detail.loc[trading_detail['cpfl']==2,'ejfl']\
            =[self.mu_ejflmap[x] for x in trading_detail[trading_detail['cpfl']==2]['ejfl']]

        trading_detail.loc[trading_detail['投资类型']=='申购','change_w']\
            =trading_detail[trading_detail['投资类型']=='申购']['认申购金额']/\
             trading_detail[trading_detail['投资类型']=='申购']['资产净值']*100
        trading_detail.loc[trading_detail['投资类型']=='赎回','change_w']\
            =trading_detail[trading_detail['投资类型']=='赎回']['赎回份额']\
             /trading_detail[trading_detail['投资类型']=='赎回']['确认净值']/\
             trading_detail[trading_detail['投资类型']=='赎回']['资产净值']*-100

        hsl=self.calculate_hsl(trading_detail)
        plot.plotly_table(hsl,1000,'')

        #trading analysis
        #merge index ret data
        trading_data=pd.merge(stratage_weight_his[['日期','沪深300']]
                             ,howbuy_index_ret,how='left',left_on='日期',right_index=True)
        trading_data=pd.merge(trading_data
                             ,mu_index_ret,how='left',left_on='日期',right_index=True)
        trading_data['ym']=trading_data['日期'].str[0:6]
        trading_data=pd.merge(trading_data
                             ,index_enhance_index,how='left',left_on='ym',right_index=True)

        #using liner interpolation to make up missed data
        for indexname in howbuy_index_ret.columns.tolist()\
                         +index_enhance_index.columns.tolist()+mu_index_ret.columns.tolist():

            temp = trading_data[indexname].reset_index(drop=True)
            tempnotnull=temp[temp.notnull()]
            f = interpolate.interp1d(tempnotnull.index.values, tempnotnull.values, kind='cubic')
            ynew = f(temp.iloc[tempnotnull.index[0]:tempnotnull.index[-1]].index.values)
            temp.loc[tempnotnull.index[0]:tempnotnull.index[-1]-1]=ynew
            trading_data[indexname]=temp.values

        for col in [ 'CTA', '主观多头', '量化多头', '国证大盘', '国证中盘', '国证小盘',
       '国证成长', '国证价值', '公募偏股','1000指数增强','500指数增强','300指数增强']:
            if(col in ['CTA', '主观多头', '量化多头',  '公募偏股']):
                trading_data[col] = trading_data[col] - trading_data['881001']
            elif(col in ['国证大盘', '国证中盘', '国证小盘','国证成长', '国证价值']):
                trading_data[col]=trading_data[col]-trading_data['399311']
            else:
                trading_data[col] = trading_data[col]-trading_data['量化多头']
            trading_data["ma10"]=trading_data[col].rolling(10).mean()
            trading_data["ma60"] = trading_data[col].rolling(60).mean()
            trading_data.loc[trading_data['ma60']>=trading_data['ma10'],col+'trend']=-1
            trading_data.loc[trading_data['ma60'] <= trading_data['ma10'], col + 'trend'] = 1
            trading_data.drop(['ma10','ma60'],axis=1,inplace=True)

        #sum the weight_change for one fund at one day
        trading_detail=pd.merge(trading_detail
                                ,trading_detail.groupby(['date','jjdm']).sum('change_w')['change_w'].reset_index()
                                ,how='left'
                                ,on=['date','jjdm']).rename(columns={'change_w_y':'change_w'}).drop('change_w_x',axis=1)

        trading_detail=trading_detail.drop_duplicates(['date','jjdm'])


        #merge weight change by class
        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['jjfl'] == '管理期货'].groupby('date').sum()['change_w'].to_frame('CTA_weight_change')
                             ,how='left',left_on='日期',right_index=True)

        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['ejfl'] == '量化多头'].groupby('date').sum()['change_w'].to_frame('量化多头_weight_change')
                             ,how='left',left_on='日期',right_index=True)

        for type in ['300','500','1000']:
            trading_detail.loc[(trading_detail['jjdm'].str.contains(type))
                             &(trading_detail['ejfl']=='量化多头'),'sjfl']=type+'指增'
            trading_data = pd.merge(trading_data
                                    , trading_detail[trading_detail['sjfl']==type+'指增'].groupby(
                    'date').sum()['change_w'].to_frame(type+'指增_weight_change')
                                    , how='left', left_on='日期', right_index=True)

        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['ejfl'] == '主观多头'].groupby('date').sum()['change_w'].to_frame('主观多头_weight_change')
                             ,how='left',left_on='日期',right_index=True)

        trading_data=pd.merge(trading_data
                             ,trading_detail[trading_detail['ejfl'].isin(['偏股混合型','灵活配置型','普通股票型'])].groupby('date').sum()['change_w'].to_frame('公募偏股_weight_change')
                             ,how='left',left_on='日期',right_index=True)

        trading_data=pd.merge(trading_data
                             ,trading_detail[~trading_detail['jjfl'].isin(['混合型',
        '股票型','管理期货'])].groupby('date').sum()['change_w'].to_frame('其他_weight_change')
                             ,how='left',left_on='日期',right_index=True)

        fof_nav['FOF净申赎'] = fof_nav['资产份额'].diff(1) * fof_nav['单位净值']
        trading_data=pd.merge(trading_data,fof_nav[['date','资产份额','资产净值']]
                              ,how='left',left_on='日期',right_on='date').drop('date',axis=1).set_index('日期')



        return  trading_data,trading_detail,fof_nav

    @staticmethod
    def define_trading_type(trading_data):

        # lable negative trading
        #add two columns 资产净值T+14 and 资产净值T-14
        trading_data['资产份额T+14']=trading_data['资产份额'].iloc[14:].tolist() + 14 * [np.nan]
        trading_data['资产份额T-14'] = 14 * [np.nan]+trading_data['资产份额'].iloc[0:-14].tolist()
        trading_data['调仓类型']=''
        trading_data.loc[((trading_data['CTA_weight_change']>0)
                         |(trading_data['量化多头_weight_change']>0)
                         |(trading_data['主观多头_weight_change']>0)
                         |(trading_data['公募偏股_weight_change']>0)
                         |(trading_data['其他_weight_change']>0))
                         &((trading_data['资产份额T-14']<trading_data['资产份额'])
                           |(trading_data.index<=trading_data.index[60])),'调仓类型']='被动增仓'

        trading_data.loc[((trading_data['CTA_weight_change']<0)
                         |(trading_data['量化多头_weight_change']<0)
                         |(trading_data['主观多头_weight_change']<0)
                         |(trading_data['公募偏股_weight_change']<0)
                         |(trading_data['其他_weight_change']<0))
                         &((trading_data['资产份额T+14']<trading_data['资产份额'])|
                           (trading_data.index<=trading_data.index[60])),'调仓类型']='被动减仓'

        trading_data.loc[((trading_data['CTA_weight_change'].notnull())
                         |(trading_data['量化多头_weight_change'].notnull())
                         |(trading_data['主观多头_weight_change'].notnull())
                         |(trading_data['公募偏股_weight_change'].notnull())
                         |(trading_data['其他_weight_change'].notnull())
                         )
                         &(trading_data['调仓类型']==''),'调仓类型']='主动'


        return  trading_data

    @staticmethod
    def calculate_hsl(inputdf):

        positive_trade=inputdf.copy()
        positive_trade=positive_trade[positive_trade['change_w'].notnull()]
        positive_trade['change_w']=abs(positive_trade['change_w'])
        positive_trade['year']=positive_trade['date'].astype(str).str[0:4]
        hsl=(positive_trade.groupby('year').sum()['change_w']/100).to_frame('双边换手率').reset_index()
        print('avg hsl is '+str(hsl['双边换手率'].mean()))

        return hsl

    def fof_trading_analysis(self,weight_his_dir,hold_data_dir,start_date,product):


        #trade data pre processing
        trading_data,trading_detail,fof_nav=\
            self.trade_date_preprocessing(weight_his_dir,hold_data_dir,start_date)

        #temparory use
        first_class_asset_weight_his=pd.read_excel(weight_his_dir)
        first_class_asset_weight_his['公募偏股(%)']=\
            first_class_asset_weight_his['股票型(公募)(%)']+first_class_asset_weight_his['混合型(公募)(%)']
        first_class_asset_weight_his['日期']=first_class_asset_weight_his['日期'].astype(str)
        # temparory use

        #*******define trading type : positive or negative *******
        trading_data=self.define_trading_type(trading_data)

        negative_trade=trading_data[trading_data['调仓类型'].str.contains('被动')]
        negative_trade_summary=pd.DataFrame(index=negative_trade['调仓类型'].unique().tolist())
        for type in negative_trade['调仓类型'].unique().tolist():
            for asset in ['CTA','量化多头','主观多头','公募偏股','其他']:
                negative_trade_summary.loc[type,asset]= \
                    len(negative_trade[(negative_trade['调仓类型'] == type)
                                       & (negative_trade[asset + "_weight_change"].notnull())])

        #positive_trade=trading_data[(trading_data['调仓类型']=='主动')]
        positive_trade=trading_data[(trading_data['调仓类型']!='')]


        positive_trade=positive_trade.reset_index(drop=False)
        positive_trade_block=[]

        jjfl2stratage_map=dict(zip(['管理期货','股票型','混合型','其他','债券型','市场中性','套利型','多策略','QDII','货币型','多空仓型']
                                   ,['CTA','进攻性资产','进攻性资产','稳健性资产','稳健性资产','稳健性资产','稳健性资产','稳健性资产','进攻性资产','稳健性资产','CTA']))

        def define_trade_type(inputdf):


            block_detail=inputdf.copy()
            block_detail['操作类型']=[jjfl2stratage_map[x] for x in block_detail['jjfl']]

            style_detail=block_detail.groupby('风格偏好').sum()['change_w']
            size_detail = block_detail.groupby('规模偏好').sum()['change_w']
            ej_detail=block_detail.groupby('ejfl').sum()['change_w']
            weight_change=[np.nan]*12


            trade_type2=''
            trade_type3=''
            for style in style_detail.index.tolist():

                if(style_detail.loc[style]>0):
                    action='买'
                else:
                    action='卖'

                if(style=='价值'):
                    weight_change[8]=style_detail.loc[style]
                elif(style=='成长'):
                    weight_change[7] = style_detail.loc[style]

                trade_type2+=action+"%.2f%%" % abs(style_detail.loc[style])+style+","

            for style in size_detail.index.tolist():

                if (size_detail.loc[style] > 0):
                    action = '买'
                else:
                    action = '卖'

                if('大' in  style):
                    weight_change[9]=size_detail.loc[style]
                elif('中' in  style):
                    weight_change[10] = size_detail.loc[style]
                elif ('小' in  style):
                    weight_change[11] = size_detail.loc[style]

                trade_type3 += action + "%.2f%%" % abs(size_detail.loc[style])+style+","

            for ejfl in ej_detail.index.tolist():

                if('管理期货' in  ejfl):
                    weight_change[0]=ej_detail.loc[ejfl]
                elif('量化多头' in  ejfl  ):
                    weight_change[1] = ej_detail.loc[ejfl]
                elif ('300指增' in  ejfl):
                    weight_change[2] = ej_detail.loc[ejfl]
                elif ('500指增' in  ejfl):
                    weight_change[3] = ej_detail.loc[ejfl]
                elif ('1000指增' in  ejfl):
                    weight_change[4] = ej_detail.loc[ejfl]
                elif ('主观多头' in  ejfl):
                    weight_change[5] = ej_detail.loc[ejfl]
                elif ('偏股混合型' in  ejfl or '普通股票型' in  ejfl or '灵活配置型' in  ejfl ):
                    weight_change[6] = ej_detail.loc[ejfl]



            if(len(block_detail[block_detail['change_w']>0])>0
                    and len(block_detail[block_detail['change_w'] < 0])>0):

                block_detail['YTM'] = abs(block_detail['YTM'] * block_detail['change_w'])
                buy_ytm=block_detail[block_detail['change_w']>0].sum()['YTM']
                sell_ytm = block_detail[block_detail['change_w'] < 0].sum()['YTM']

                if (buy_ytm>sell_ytm ):
                    if_win = '胜'
                else:
                    if_win = '败'
            else:
                if_win=''

            if(len(block_detail['操作类型'].unique())>1):

                block_detail=block_detail.groupby('操作类型').sum()[['change_w']]
                trade_type = ''
            else:
                if(len(block_detail['ejfl'].unique())>1):
                    block_detail = block_detail.groupby('ejfl').sum()[['change_w']]
                    trade_type = ''

                else:
                    if(if_win!=''):
                        trade_type = '置换{}资产'.format(block_detail['ejfl'].unique()[0])
                    else:
                        if(block_detail['change_w'].sum()>0):
                            trade_type = '购买{}资产'.format("%.2f%%" %abs(block_detail['change_w'].sum())+block_detail['ejfl'].unique()[0])
                        else:
                            trade_type = '卖出{}资产'.format("%.2f%%" %abs(block_detail['change_w'].sum())+block_detail['ejfl'].unique()[0])


            if(trade_type==''):
                for index in block_detail.index.tolist():

                    if(block_detail.loc[index]['change_w']>0):
                        trade_dir='买'
                    else:
                        trade_dir='卖'
                    trade_type+=trade_dir+"%.2f%%" % block_detail.loc[index]['change_w']+index+";"

            return  trade_type,trade_type2,trade_type3,if_win,weight_change


        i=0
        while (i<len(positive_trade)):
            t0=datetime.datetime.strptime(positive_trade.iloc[i]['日期']
                                          , '%Y%m%d')
            t_14=(t0+datetime.timedelta(days=14)).strftime('%Y%m%d')
            tempdf=positive_trade[(positive_trade['日期']>=positive_trade.iloc[i]['日期'])
                           &(positive_trade['日期']<=t_14)]

            increase_asset=0
            decrease_asset=0
            for col in ['CTA','量化多头','主观多头','公募偏股','其他']:
                increase_asset+=len(tempdf[tempdf[col+'_weight_change']>0])
                decrease_asset+=len(tempdf[tempdf[col+'_weight_change']<0])
            if(len(tempdf)>1):
            # if(increase_asset>0 and decrease_asset>0):
                i = tempdf.index[-1] + 1
                t0 = datetime.datetime.strptime(positive_trade.iloc[i]['日期']
                                                , '%Y%m%d')
                if((t0-datetime.datetime.strptime(tempdf['日期'].max(),'%Y%m%d')).days<=7):
                    tempdf=pd.concat([tempdf,positive_trade[(
                            positive_trade['日期']==positive_trade.iloc[i]['日期'] )]],axis=0)
                    i = tempdf.index[-1] + 1

                positive_trade_block.append(tempdf)

            else:
                if(len(tempdf)==1):
                    positive_trade_block.append(tempdf)
                i += 1

        wc_name = ['CTA_weight_change', '量化多头_weight_change', '300指增_weight_change', '500指增_weight_change',
                   '1000指增_weight_change', '主观多头_weight_change', '公募偏股_weight_change', '国证成长_weight_change'
            , '国证价值_weight_change', '国证大盘_weight_change', '国证中盘_weight_change', '国证小盘_weight_change']
        for i in range(len(positive_trade_block)):
            block=positive_trade_block[i]
            block_detail=\
                trading_detail[trading_detail['date'].isin(block['日期'].unique())][['jjdm','cpfl','jjfl','ejfl','风格偏好', '规模偏好','date','change_w','投资基金']]


            sql = "select jjdm,jzrq,jjjz from st_fund.t_st_gm_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'" \
                .format(util.list_sql_condition(block_detail[block_detail['cpfl']==2]['jjdm'].tolist())
                        , block_detail['date'].iloc[0], fof_nav['date'].iloc[-1])
            mutual_nav = hbdb.db2df(sql, db='funduser')
            if(len(mutual_nav)>0):
                mutual_nav=mutual_nav.pivot_table('jjjz','jzrq','jjdm')
                for col in mutual_nav.columns:
                    block_detail.loc[block_detail['jjdm']==col,'YTM']=\
                        mutual_nav[mutual_nav[col].notnull()][col].iloc[-1]\
                        /mutual_nav[mutual_nav[col].notnull()][col].iloc[0]-1

            sql = "select jjdm,jzrq,jjjz from st_hedge.t_st_jjjz where jjdm in ({0}) and jzrq>='{1}' and jzrq<='{2}'" \
                .format(util.list_sql_condition(block_detail[block_detail['cpfl']==4]['jjdm'].tolist())
                        , block_detail['date'].iloc[0], fof_nav['date'].iloc[-1])
            prv_nav = hbdb.db2df(sql, db='highuser')
            if(len(prv_nav)>0):
                prv_nav=prv_nav.pivot_table('jjjz','jzrq','jjdm')
                for col in prv_nav.columns:
                    block_detail.loc[block_detail['jjdm']==col,'YTM']=\
                        prv_nav[prv_nav[col].notnull()][col].iloc[-1]\
                        /prv_nav[prv_nav[col].notnull()][col].iloc[0]-1

            block_detail['trade_group']=i+1

            trade_type,trade_type2,trade_type3,if_win,weight_change=\
                define_trade_type(block_detail)
            block_detail['资产操作类型']=trade_type
            block_detail['风格操作类型'] = trade_type2
            block_detail['市值风格操作类型'] = trade_type3
            block_detail['操作结果'] = if_win

            for j in range(12):
                block_detail[wc_name[j]]=weight_change[j]

            positive_trade_block[i]=block_detail

        positive_trade_block=pd.concat(positive_trade_block,axis=0)
        positive_trade_block['change_w']=positive_trade_block['change_w']/100
        for col in ['change_w','YTM']:
            positive_trade_block[col] = \
                positive_trade_block[col].map("{:.2%}".format)

        positive_trade_block=\
            positive_trade_block.sort_values(['trade_group', 'date'])[['trade_group', 'date', '投资基金', 'YTM', 'change_w'
            , 'jjfl', 'ejfl', '资产操作类型', '操作结果', '风格操作类型', '市值风格操作类型']+wc_name]
        silme_positive_trade=positive_trade_block.drop_duplicates('trade_group',keep='last')[['date'
            ,'资产操作类型', '风格操作类型', '市值风格操作类型']+wc_name].set_index('date')
        silme_trade_data=pd.merge(trading_data[['CTA', '主观多头', '量化多头', 'CTA_rank', '主观多头_rank', '量化多头_rank',
       '国证大盘', '国证中盘', '国证小盘', '国证成长', '国证价值', '881001','CBA00301', 'CI0077', '公募偏股', '国证大盘_rank',
       '国证中盘_rank', '国证小盘_rank', '国证成长_rank', '国证价值_rank',
       '公募偏股_rank', 'ym', '1000指数增强', '300指数增强', '500指数增强', '1000指数增强_rank',
       '300指数增强_rank', '500指数增强_rank', 'CTAtrend', '主观多头trend', '量化多头trend',
       '国证大盘trend', '国证中盘trend', '国证小盘trend', '国证成长trend', '国证价值trend',
       '公募偏股trend', '1000指数增强trend', '500指数增强trend', '300指数增强trend']],silme_positive_trade,how='left',left_index=True,right_index=True)


        silme_trade_summary=pd.DataFrame(index=wc_name,columns=['买入时点','卖出时点','买入左侧比例','卖出左侧比例'])
        for name in wc_name:
            if(sum(silme_trade_data[name].notnull())>0):
                short_name=name.split('_')[0]
                silme_trade_summary.loc[name,'买入时点']= \
                    sum(silme_trade_data[silme_trade_data[name] > 0][short_name + '_rank'] *
                        silme_trade_data[silme_trade_data[name] > 0][short_name + '_weight_change']) / \
                    silme_trade_data[silme_trade_data[name] > 0][short_name + '_weight_change'].sum()
                silme_trade_summary.loc[name,'卖出时点']= \
                    sum(silme_trade_data[silme_trade_data[name] < 0][short_name + '_rank'] *
                        silme_trade_data[silme_trade_data[name] < 0][short_name + '_weight_change']) / \
                    silme_trade_data[silme_trade_data[name] < 0][short_name + '_weight_change'].sum()

                silme_trade_summary.loc[name,'买入左侧比例']= \
                    sum((silme_trade_data[silme_trade_data[name] > 0][short_name + 'trend'] == -1) * (
                    silme_trade_data[silme_trade_data[name] > 0][short_name + '_weight_change'])) / (
                    silme_trade_data[silme_trade_data[name] > 0][short_name + '_weight_change']).sum()
                silme_trade_summary.loc[name,'卖出左侧比例']= \
                    sum((silme_trade_data[silme_trade_data[name] < 0][short_name + 'trend'] == 1) * (
                    silme_trade_data[silme_trade_data[name] < 0][short_name + '_weight_change'])) / (
                    silme_trade_data[silme_trade_data[name] < 0][short_name + '_weight_change']).sum()

        for col in silme_trade_summary:
            silme_trade_summary[col]=silme_trade_summary[col].map("{:.2%}".format)

        # plot.plotly_table(silme_trade_summary.reset_index(drop=False), 1000, '')
        # plot.plotly_table(negative_trade_summary.reset_index(drop=False), 1000, '')
        # plot.plotly_table(positive_trade_block[['trade_group', 'date', '投资基金', 'YTM', 'change_w'
        #     , 'jjfl', 'ejfl', '资产操作类型', '风格操作类型', '市值风格操作类型']],1500,'')
        positive_trade_block=pd.merge(positive_trade_block,trading_detail[['投资基金','风格偏好','规模偏好']].drop_duplicates('投资基金')
                                      ,how='left',on='投资基金').rename(columns={'trade_group':'交易组',
                                                                             'date':'交易日期',
                                                                             'change_w':'权重变动',
                                                                             'jjfl':'基金分类',
                                                                             'ejfl':'二级分类'})
        positive_trade_block[['交易组', '交易日期','资产操作类型',
                              '风格操作类型', '市值风格操作类型','投资基金',
                              '权重变动', '基金分类', '二级分类','风格偏好', '规模偏好']].to_excel(hold_data_dir.replace('基金持仓数据','交易细节'))
        silme_trade_summary.to_excel(hold_data_dir.replace('基金持仓数据', '资产配置交易细节'))

        first_class_asset_weight_his=pd.merge(first_class_asset_weight_his
                                              ,silme_trade_data[['CTA', '主观多头', '量化多头','公募偏股','881001','CBA00301', 'CI0077', '国证成长', '国证价值']]
                                              ,how='left',on='日期')
        first_class_asset_weight_his.to_excel(hold_data_dir.replace('基金持仓数据', '一级策略权重与指数'))



        data, layout=plot.plotly_line_and_bar(silme_trade_data[['CTA']]
                                                  ,silme_trade_data[['CTA_weight_change']]
                                              ,product+'CTA交易时序')
        plot.plot_render(data, layout)

        data, layout=plot.plotly_line_and_bar(silme_trade_data[['主观多头']]
                                                  ,silme_trade_data[['主观多头_weight_change']]
                                              ,product+'私募股多交易时序')
        plot.plot_render(data, layout)

        data, layout=plot.plotly_line_and_bar(silme_trade_data[['量化多头']]
                                                  ,silme_trade_data[['量化多头_weight_change']]
                                              ,product+'量化多头交易时序')
        plot.plot_render(data, layout)

        data, layout=plot.plotly_line_and_bar(silme_trade_data[['公募偏股']]
                                                  ,silme_trade_data[['公募偏股_weight_change']]
                                              ,product+'公募偏股交易时序')
        plot.plot_render(data, layout)

        data, layout=plot.plotly_line_and_bar(silme_trade_data[['国证成长']]
                                                  ,silme_trade_data[['国证成长_weight_change']]
                                              ,product+'国证成长交易时序')
        plot.plot_render(data, layout)
        data, layout=plot.plotly_line_and_bar(silme_trade_data[['国证价值']]
                                                  ,silme_trade_data[['国证价值_weight_change']]
                                              ,product+'国证价值交易时序')
        plot.plot_render(data, layout)
        data, layout=plot.plotly_line_and_bar(silme_trade_data[['国证大盘']]
                                                  ,silme_trade_data[['国证大盘_weight_change']]
                                              ,product+'国证大盘交易时序')
        plot.plot_render(data, layout)
        data, layout=plot.plotly_line_and_bar(silme_trade_data[['国证中盘']]
                                                  ,silme_trade_data[['国证中盘_weight_change']]
                                              ,product+'国证中盘交易时序')
        plot.plot_render(data, layout)
        data, layout=plot.plotly_line_and_bar(silme_trade_data[['国证小盘']]
                                                  ,silme_trade_data[['国证小盘_weight_change']]
                                              ,product+'国证小盘交易时序')
        plot.plot_render(data, layout)

class FOF_ams_data_analysis:


    def __init__(self,dir1,dir2,product_list):

        for product in product_list:

            self.year_ret_analysis(dir2.replace('@@',product))
            self.define_weight_target(dir1.replace('@@',product))

    @staticmethod
    def define_weight_target(dir,monotonic_lenght=20):

        weight_history=pd.read_excel(dir)
        weight_history.columns=[x.replace('(%)','') for x in weight_history.columns]
        weight_history['日期']=weight_history['日期'].astype(str)
        weight_history['total']=weight_history.sum(axis=1)

        equity_asset=['股票型(私募)', '股票型(公募)', '混合型(公募)']

        weight_history['进攻性资产仓位'] =\
            weight_history[equity_asset].sum(axis=1)

        for col in equity_asset:
            weight_history[col]=\
                weight_history[col]/weight_history['进攻性资产仓位']
        weight_history['进攻性资产仓位']=weight_history['进攻性资产仓位']/100

        weight_target_df=[]

        def trade_stat(q_line_date,weight_history):

            tempdf = pd.DataFrame()

            if(len(q_line_date)>0):
                q_line_date = \
                    [weight_history['日期'].iloc[0]]\
                    +q_line_date['日期'].tolist()\
                    +[weight_history['日期'].iloc[-1]]

                sql = """select zqdm,jyrq,spjg from st_market.t_st_zs_hqql 
                where jyrq in ({0}) and zqdm in ('881001','885001')""" \
                    .format(util.list_sql_condition(q_line_date))

                mu_index_ret = hbdb.db2df(sql, db='alluser').pivot_table('spjg', 'jyrq', 'zqdm')
                mu_index_ret.index = mu_index_ret.index.astype(str)


                for i in range(len(q_line_date)-1):

                    remove_data=int(monotonic_lenght/2)

                    tempdf.loc[q_line_date[i]+" to "+q_line_date[i+1],'权重均值']= \
                        weight_history[(weight_history['日期']>= q_line_date[i])
                                   &(weight_history['日期']<= q_line_date[i+1])][col][remove_data:-remove_data].mean()
                    tempdf.loc[q_line_date[i]+" to "+q_line_date[i+1],'权重中值']=\
                        weight_history[(weight_history['日期']>= q_line_date[i])
                                   &(weight_history['日期']<= q_line_date[i+1])][col][remove_data:-remove_data].median()
                    tempdf.loc[q_line_date[i]+" to "+q_line_date[i+1],'偏离均值']= \
                        weight_history[(weight_history['日期']>= q_line_date[i])
                                   &(weight_history['日期']<= q_line_date[i+1])][col+"_30div"][remove_data:-remove_data].mean()
                    tempdf.loc[q_line_date[i]+" to "+q_line_date[i+1],'偏离最大']= \
                        weight_history[(weight_history['日期']>= q_line_date[i])
                                   &(weight_history['日期']<= q_line_date[i+1])][col+"_30div"][remove_data:-remove_data].max()


                    tempdf.loc[q_line_date[i]+" to "+q_line_date[i+1],'全A涨幅']=\
                        (mu_index_ret.loc[q_line_date[i+1]]['881001']/
                         mu_index_ret.loc[q_line_date[i]]['881001']-1)
                    tempdf.loc[q_line_date[i]+" to "+q_line_date[i+1],'偏股混涨幅']=\
                        (mu_index_ret.loc[q_line_date[i+1]]['885001']/
                         mu_index_ret.loc[q_line_date[i]]['885001']-1)

            else:

                tempdf.loc['全期', '权重均值'] =weight_history[col].mean()
                tempdf.loc['全期', '权重中值'] = weight_history[col].median()

                tempdf.loc['全期', '偏离均值'] =weight_history[col + "_30div"][30:-30].mean()
                tempdf.loc['全期', '偏离最大'] =weight_history[col + "_30div"][30:-30].max()

            return  tempdf

        for col in ['进攻性资产仓位']+equity_asset:

            weight_history[col+"_30MA"]=weight_history[col].rolling(30).mean()
            weight_history[col+"_30div"]=abs(weight_history[col]-weight_history[col+"_30MA"])
            weight_history[col+'Ndays_monotonic']=weight_history[col+"_30div"].rolling(monotonic_lenght).apply(monotonic)
            weight_history[col + 'Ndays_monotonic_T-1']=\
                [np.nan]+weight_history[col+'Ndays_monotonic'][0:-1].tolist()
            weight_history.loc[(weight_history[col+'Ndays_monotonic'] == 1) & (
                        weight_history[col + 'Ndays_monotonic_T-1'] == 0), col+'_q_line'] = True

            weight_history[col+'_q_line']=weight_history[col+'_q_line'].iloc[monotonic_lenght:].tolist()+[np.nan]*monotonic_lenght


            q_line_date=weight_history[weight_history[col+'_q_line']==True]


            tempdf=trade_stat(q_line_date, weight_history)
            less_than1_diff=tempdf[tempdf['权重中值'].diff().abs()<=0.02].index
            while len(less_than1_diff)>0:
                for date_line in less_than1_diff:
                    q_line_date=q_line_date[q_line_date['日期']!=date_line[0:8]]
                tempdf = trade_stat(q_line_date, weight_history)
                less_than1_diff = tempdf[tempdf['权重中值'].diff().abs() <= 0.02].index

            tempdf = tempdf.reset_index(drop=False).rename(columns={'index': '持续日期'})
            tempdf.index = len(tempdf) * [col]
            weight_target_df.append(tempdf)

        weight_target_df=pd.concat(weight_target_df,axis=0)

        for col in ['权重均值','权重中值','偏离均值','偏离最大','全A涨幅','偏股混涨幅']:

            weight_target_df[col]=weight_target_df[col].map("{:.2%}".format)


        plot.plotly_table(weight_target_df.reset_index(),1200,'资产仓位中枢与变动')

    @staticmethod
    def year_ret_analysis(dir):
        nav_history=pd.read_excel(dir)[['日期','累计单位净值']]

        nav_history['日期']=nav_history['日期'].astype(str).str.replace('-','')
        nav_history=nav_history.sort_values('日期')
        nav_history['year']=nav_history['日期'].str[0:4]

        summary=pd.DataFrame(index=nav_history['year'].unique()
                             ,columns=['收益率','波动率'])
        for date in nav_history['year'].unique():
            summary.loc[date,'收益率']=\
                nav_history[nav_history['year']==date]['累计单位净值'].iloc[-1]\
                /nav_history[nav_history['year']==date]['累计单位净值'].iloc[0]-1
            summary.loc[date, '波动率']=\
                nav_history[nav_history['year']==date]['累计单位净值'].pct_change().std()*np.sqrt(250)

        for col in summary.columns:

            summary[col]=summary[col].map("{:.2%}".format)

        plot.plotly_table(summary.reset_index(drop=False),500,'')



        print('')



if __name__ == '__main__':


    # fada=FOF_ams_data_analysis("E:\FOF分析\@@\一级策略时序图.xlsx"
    #                            ,"E:\FOF分析\@@\基金净值数据.xls"
    #                            ,product_list=['新方程星动力S7号基金','新方程-北大价值精选FOF1号'])

    # data=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WeChat Files\wxid_xvk2piiub53y12\FileStorage\MsgAttach\9e20f478899dc29eb19741386f9343c8\File\2022-11\881304.WI-成分进出记录-20221123.xlsx")
    # data['日期']=[str(x).replace('-','') for x in data['日期']]
    # data=data.sort_values('日期')



    # sql="select jsrq,zqdm,zqmc,zjbl,zgbl from st_fund.t_st_gm_gpzh where jjdm='001714' and jsrq>='20160101'"
    # data=hbdb.db2df(sql,db='funduser')
    #
    # prv_hold = pd.read_excel(r"E:\GitFolder\docs\私募股多持仓分析\刘泽龙\新方程泓澄精选_S63505_20221122.xls"
    #                          , sheet_name='持仓时序')
    # prv_hold.drop_duplicates('股票简称', inplace=True)
    # mu_hold = pd.read_excel(r"E:\GitFolder\hbshare\fe\FOF\工银zjbl.xlsx")
    # 
    # date_list=mu_hold.columns.tolist()
    # prv_date_list=prv_hold.columns.tolist()[2:]
    # 
    # prv_hold = prv_hold.drop('股票代码',axis=1).set_index('股票简称').T
    # prv_hold=prv_hold.iloc[5:]
    # prv_hold.drop(prv_hold.sum(axis=0)[prv_hold.sum(axis=0) == 0].index.tolist(),axis=1,inplace=True)
    # prv_buy_time=pd.DataFrame(columns=prv_hold.columns.tolist())
    # for zq in prv_hold.columns.unique().tolist():
    #     prv_buy_time.loc['0',zq]=prv_hold[prv_hold[zq].notnull()].index[0]
    # 
    # prv_buy_time=prv_buy_time.T.rename(columns={'0': '泓澄买入时点'})
    # 
    # 
    # mu_hold = mu_hold.set_index('zqmc').T
    # mu_buy_time = pd.DataFrame(columns=mu_hold.columns.tolist())
    # for zq in mu_hold.columns.unique().tolist():
    #     mu_buy_time.loc['0', zq] = mu_hold[mu_hold[zq].notnull()].index[0]
    # 
    # mu_buy_time=mu_buy_time.T.rename(columns={'0': '工银买入时点'})
    # 
    # buy_time=pd.merge(mu_buy_time,prv_buy_time,how='inner',left_index=True,right_index=True)
    # buy_time['泓澄买入时点']=[datetime.datetime.strptime(str(x),
    #                                                '%Y%m%d') for x in buy_time['泓澄买入时点']]
    # buy_time['工银买入时点']=[datetime.datetime.strptime(str(x),
    #                                                '%Y%m%d') for x in buy_time['工银买入时点']]
    # buy_time['diff']=buy_time['泓澄买入时点']-buy_time['工银买入时点']
    # buy_time['diff']=[x.days for x in buy_time['diff']]
    # buy_time.to_excel('买入时点比较.xlsx')

    # #
    # summary_df=pd.DataFrame(index=['工银 交集占持仓数量比','泓澄_交集占持仓数量比','工银 交集占持仓数量比（过去三月）','泓澄_交集占持仓数量比（过去三月）'
    #     ,'工银_交集占股票比例','泓澄_交集占股票比例','工银_交集占股票比例（过去三月）','泓澄_交集占股票比例（过去三月）','当月交集持仓比例差别和'])
    #
    # summary_df_top10 = pd.DataFrame(index=['工银 交集占持仓数量比', '泓澄_交集占持仓数量比',
    #     '工银_交集占股票比例', '泓澄_交集占股票比例', '当月交集持仓比例差别和'])
    #
    # for i in range(1,len(date_list)):
    #
    #     mu_con_hold=mu_hold[mu_hold[date_list[i]].notnull()][['zqmc',date_list[i]]]
    #     mu_zqjc=mu_con_hold['zqmc'].tolist()
    #
    #     mu_con_hold_top10=mu_con_hold.sort_values(date_list[i], ascending=False)[0:10]
    #
    #     prv_con_hold=prv_hold[(prv_hold[prv_date_list[i * 3 + 2]].notnull())
    #     |(prv_hold[prv_date_list[i * 3 + 3]].notnull())
    #     |(prv_hold[prv_date_list[i * 3 + 4]].notnull())][['股票简称']
    #                                                                          +prv_date_list[i * 3 + 2:i * 3 + 5]]
    #     prv_con_hold[prv_date_list[i * 3 + 2:i * 3 + 5]].astype(float)
    #
    #
    #     prv_con_hold2=prv_hold[prv_hold[prv_date_list[i * 3 + 4]].notnull()][['股票简称']+[prv_date_list[i * 3 + 4]]]
    #     prv_con_hold_top10=prv_con_hold2.sort_values(prv_date_list[i * 3 + 4], ascending=False)[0:10]
    #
    #
    #     prv_zqjc=prv_con_hold['股票简称'].unique().tolist()
    #
    #     prv_zqjc2=prv_con_hold2['股票简称'].unique().tolist()
    #
    #     covered_zqjc=list(set(mu_zqjc).intersection(set(prv_zqjc)))
    #
    #     covered_zqjc2=list(set(mu_zqjc).intersection(set(prv_zqjc2)))
    #
    #     joint_holding=pd.merge(mu_con_hold,prv_con_hold2,how='inner',left_on='zqmc',right_on='股票简称').drop('zqmc',axis=1)
    #     joint_holding['diff']=joint_holding[joint_holding.columns[0]]-joint_holding[joint_holding.columns[2]]
    #
    #     value_list=[len(covered_zqjc2)/len(mu_zqjc),len(covered_zqjc2)/len(prv_zqjc2)
    #         ,len(covered_zqjc)/len(mu_zqjc),len(covered_zqjc)/len(prv_zqjc),
    #                 mu_con_hold[mu_con_hold['zqmc'].isin(covered_zqjc2)].sum().iloc[1] / mu_con_hold.sum().iloc[1],
    #                 prv_con_hold2[prv_con_hold2['股票简称'].isin(covered_zqjc2)].sum().iloc[1] / prv_con_hold2.sum().iloc[
    #                     1],
    #                 mu_con_hold[mu_con_hold['zqmc'].isin(covered_zqjc)].sum().iloc[1]/mu_con_hold.sum().iloc[1],
    #                 prv_con_hold[prv_con_hold['股票简称'].isin(covered_zqjc)].sum().iloc[1:].sum()/prv_con_hold.sum().iloc[1:].sum(),
    #                 joint_holding['diff'].abs().sum()]
    #
    #     summary_df[date_list[i]]=value_list
    #
    #     joint_holding_top10=pd.merge(mu_con_hold_top10,prv_con_hold_top10,
    #              how='inner',left_on='zqmc',right_on='股票简称').drop('zqmc',axis=1)
    #     joint_holding_top10['diff'] = joint_holding_top10[joint_holding_top10.columns[0]] - joint_holding_top10[joint_holding_top10.columns[2]]
    #
    #     top_10_joint=list(set(mu_con_hold_top10['zqmc']).intersection(set(prv_con_hold_top10['股票简称'])))
    #
    #     summary_df_top10[date_list[i]]=[len(top_10_joint)/len(mu_con_hold_top10),
    #                                     len(top_10_joint)/len(prv_con_hold_top10),
    #                                     mu_con_hold_top10[mu_con_hold_top10['zqmc'].isin(top_10_joint)].sum().iloc[1]/mu_con_hold_top10.sum().iloc[1],
    #                                     prv_con_hold_top10[prv_con_hold_top10['股票简称'].isin(top_10_joint)].sum().iloc[1]/prv_con_hold_top10.sum().iloc[1],
    #                                     joint_holding_top10['diff'].abs().sum()/100]
    #
    #
    # summary_df.to_excel('持仓对比总结.xlsx',index=True)
    # summary_df_top10.to_excel('top10持仓对比总结.xlsx',index=True)

    # jjdm_list=util.get_bmk_funds_list_20220824('20220630',)
    # sql="select jjdm,min(jzrq) from st_fund.t_st_gm_jjjz where jzrq>='20160331' and jjdm in ({}) group by jjdm "\
    #     .format(util.list_sql_condition(jjdm_list))
    # mu_nav_all=hbdb.db2df(sql,db='funduser')
    # jjdm_list = mu_nav_all[mu_nav_all['min(jzrq)'] <= 20160331]['jjdm'].tolist()
    #
    # sql="select jjdm,min(jzrq) from st_fund.t_st_gm_jjjz where jzrq>='20160331' and jjdm in ({}) group by jjdm "\
    #     .format(util.list_sql_condition(jjdm_list))
    # mu_nav_all=hbdb.db2df(sql,db='funduser')

    nav_compare = pd.read_excel(r"E:\GitFolder\hbshare\fe\FOF\nav_compare.xlsx")[['日期','泓澄净值日涨跌幅']]
    sql="select jjdm,jzrq,ljjz from st_fund.t_st_gm_jjjz where jzrq>='20160331' and jjdm in ({})"\
        .format(util.list_sql_condition(['001910','161005','000761','660006','519069']))
    mu_nav_all=hbdb.db2df(sql,db='funduser').pivot_table('ljjz','jzrq','jjdm').pct_change()

    # for i in range(6):
    #
    #     sql="select jjdm,jzrq,ljjz from st_fund.t_st_gm_jjjz where jzrq>='20160331' and jjdm in ({})"\
    #         .format(util.list_sql_condition(jjdm_list[200*i:200*(i+1)]))
    #     mu_nav_all=hbdb.db2df(sql,db='funduser').pivot_table('ljjz','jzrq','jjdm').pct_change()
    #
    #     mu_nav_all=pd.merge(mu_nav_all,nav_compare,
    #                         how='right',left_on='jzrq',right_on='日期').drop('日期',axis=1).corr()[['泓澄净值日涨跌幅']]
    #     mu_nav_all.to_excel('全公募相关性_{}.xlsx'.format(i))

    #mu_nav_all=pd.merge(mu_nav_all,nav_compare[])

    # nav_compare['ym']=nav_compare['日期'].astype(str).str[0:6]
    # nav_compare['year'] = nav_compare['日期'].astype(str).str[0:4]
    #
    # jzcor=nav_compare[['工银净值', '华安逆向策略混合', '华安安信消费', '泓澄净值',  '万得全A',
    #    '万得偏股混合型基金指数','万得金仓200']].corr()
    # retcor=nav_compare[['工银净值日涨跌幅', '华安逆向策略混合涨跌幅', '华安安信消费涨跌幅', '泓澄净值日涨跌幅',
    #    '万得全A涨跌幅', '万得偏股混合型基金指数涨跌幅', '万得金仓200日涨跌幅']].corr()
    #
    # pd.concat([jzcor,retcor],axis=1).to_excel('全期像关系.xlsx')
    #
    # yearjz_cor=[]
    # yearret_cor = []
    # for year in nav_compare['year'].unique().tolist():
    #     yearjz_cor.append(nav_compare[nav_compare['year']==year][['工银净值', '华安逆向策略混合', '华安安信消费', '泓澄净值',  '万得全A',
    #    '万得偏股混合型基金指数','万得金仓200']].corr())
    #     yearret_cor.append(nav_compare[nav_compare['year'] == year][['工银净值日涨跌幅', '华安逆向策略混合涨跌幅', '华安安信消费涨跌幅', '泓澄净值日涨跌幅',
    #    '万得全A涨跌幅', '万得偏股混合型基金指数涨跌幅', '万得金仓200日涨跌幅']].corr())
    #
    # for ym in nav_compare['ym'].unique().tolist():
    #     nav_compare[nav_compare['ym'] == ym][['工银净值', '泓澄净值', '万得金仓200', '万得金仓100', '万得金仓50', '万得金仓30']].corr()
    #     nav_compare[nav_compare['ym'] == ym][['工银净值日涨跌幅', '泓澄净值日涨跌幅', '万得金仓200日涨跌幅', '万得金仓100日涨跌幅', '万得金仓50日涨跌幅',
    #                                               '万得金仓30日涨跌幅']].corr()


    # sql="select jzrq,ljjz from st_fund.t_st_gm_jjjz where jjdm ='519002' and jzrq>='20160331' "
    # mu_nav=hbdb.db2df(sql,db='funduser')
    # mu_nav['jzrq'] = mu_nav['jzrq'].astype(str)
    #
    # prv2=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-11\泓澄16-18年净值(1).xlsx")[['估值日期','单位净值']]
    # prv_3=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-11\净值份额单位净值查询_7118_新方程泓澄精选证券投资基金_20190101_20221118(1).xls")[['日期','累计单位净值']]
    # prv2['日期'] = ["20" + x.split('/')[2] + x.split('/')[1] + x.split('/')[0] for x in prv2['估值日期']]
    # prv_3['日期'] = [str(x)[0:10].replace('-','') for x in prv_3['日期']]
    # prv_3.rename(columns={'累计单位净值':'单位净值'},inplace=True)
    # prv=pd.concat([prv2[prv2['日期']<'20190101'][['日期','单位净值']],prv_3],axis=0)
    #
    # nav_compare = pd.merge(mu_nav, prv, how='inner', left_on='jzrq',right_on='日期').drop('jzrq',axis=1)
    #
    # jincang_index=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WeChat Files\wxid_xvk2piiub53y12\FileStorage\MsgAttach\9e20f478899dc29eb19741386f9343c8\File\2022-11\金仓指数行情序列.xlsx")
    # jincang_index['日期']=[str(x)[0:10].replace('-','') for x in jincang_index['时间']]
    #
    # nav_compare = pd.merge(nav_compare, jincang_index, how='inner', on='日期').drop('时间', axis=1)
    # nav_compare.to_excel('净值比较.xlsx')




    # fa=FOF_analysis(dir=r"E:\FOF分析\交易流水.xlsx",end_date='20221031')
    #fa.valuation_table_analysis(product='新方程对冲精选H1号基金',start_date='20190506',end_date='20221031')
    #fa.fromtrading2holding(start_date='20190510',end_date='20221031')


    # '新方程大类配置稳健型私募证券投资基金','新方程星动力S7号基金','新方程-北大价值精选FOF1号'
    # for product in ['新方程对冲精选H1号基金']:
    #     #
    #     fa.holding_analysis(dir=r"E:\FOF分析\{}\基金持仓数据.xlsx".format(product),start_date='20190506')
        # fa.fof_trading_analysis(weight_his_dir=r"E:\FOF分析\{}\一级策略时序图.xlsx".format(product)
        #                         ,hold_data_dir=r"E:\FOF分析\{}\基金持仓数据.xlsx".format(product)
        #                         ,start_date='20190510',product=product)


