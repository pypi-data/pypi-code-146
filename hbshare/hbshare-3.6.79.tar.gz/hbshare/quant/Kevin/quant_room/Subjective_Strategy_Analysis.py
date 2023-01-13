"""
主观股多的估值表分析
"""
import os
import datetime
import pandas as pd
import numpy as np
import hbshare as hbs
from hbshare.quant.Kevin.asset_allocation.macro_index.util import create_table, delete_duplicate_records, WriteToDB
from hbshare.fe.common.util.config import industry_name, industry_cluster_dict_new as industry_cluster_dict
import plotly
import plotly.graph_objs as go
import pyecharts.options as opts
from pyecharts.charts import Bar, Timeline
import plotly.figure_factory as ff
from hbshare.db.simu import valuation
from hbshare.fe.XZ import  db_engine
from hbshare.fe.XZ.functionality import  Untils as util
import xlwt


# from plotly.offline import plot as plot_ly

# plotly.offline.init_notebook_mode(connected=True)

hbdb=db_engine.HBDB()
ams_color_lista = ['#C94649', '#EEB2B4', '#E1777A', '#D57C56', '#E39A79', '#DB8A66', '#E5B88C']
ams_color_listb = ['#8588B7', '#B4B6D1', '#55598D', '#628497', '#A9C6CB', '#866EA9', '#B79BC7']
ams_color_listc = ['#7D7D7E', '#CACACA', '#A7A7A8', '#606063', '#C4C4C4', '#99999B', '#B7B7B7']
# def plot_render(plot_dic, width=1200, height=600, **kwargs):
#     kwargs['output_type'] = 'div'
#     plot_str = plotly.offline.plot(plot_dic, **kwargs)
#     print('%%angular <div style="height: %ipx; width: %spx"> %s </div>' % (height, width, plot_str))

def plot_render(plot_dic, width=1200, height=600, **kwargs):
    data=plot_dic['data']
    layout=plot_dic['layout']
    fig = go.Figure(data=data, layout=layout)
    fig.show()

def save_pic2local(data,layout,name,annotations=None):
    fig = go.Figure(data=data, layout=layout)
    if(annotations is not None ):
        fig.update_layout(annotations=annotations)
    fig.write_image(name)

class HoldingExtractor:
    def __init__(self, table_name,fund_name,is_increment=1,data_path=None,fund_code=None,date_list=None):
        self.data_path = data_path
        self.table_name = table_name
        self.fund_name = fund_name
        self.is_increment = is_increment
        self.fund_code=fund_code
        self.date_list=date_list
        self.total_asset_dmlist=['资产类合计:','资产合计']
        self.net_asset_dmlist=['基金资产净值:','资产净值','资产资产净值:']
        self.debt_dmlist=['负债类合计:']
        self.ashare_dmlist=['11020101','1102.01.01.','1101010101']
        self.szshare_dmlist=['11023101','1102.33.01.','1101013101']
        self.cyb_dmlistt=['11024101','1101014101']
        self.kcb_dmlist=['1102C101','1101C101']
        self.jjtz_dmlist = ['110104', '1105']
        if(data_path is not None):
            self._load_portfolio_weight()

    @staticmethod
    def _shift_date(date):
        trade_dt = datetime.datetime.strptime(date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=30)).strftime('%Y%m%d')

        sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            pre_date, date)
        res = hbs.db_data_query('readonly', sql_script, page_size=5000)
        df = pd.DataFrame(res['data']).rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                     "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

        trading_day_list = df[df['isOpen'] == 1]['calendarDate'].tolist()

        return trading_day_list[-1]

    def valuation_data2DB(self,jjdm,date_list,fund_name):
        portfolio_weight_list = []
        for date in date_list:
            data=valuation.get_prod_valuation_by_jjdm_gzrq(jjdm,date)
            if(data.empty):
                print("data for {0} missed,continue...".format(date))
                continue
            date = self._shift_date(str(date))
            columns_map=dict(zip(['kmdm','sz','kmmc'],['科目代码','市值','科目名称']))

            data.rename(columns=columns_map,inplace=True)

            for dm in self.total_asset_dmlist:
                if(len(data[data['科目代码'] == dm])>0):
                    total_asset = float(data[data['科目代码'] ==dm]['市值'].values[0])
                    break

            net_asset=0
            for dm in self.net_asset_dmlist:
                if(len(data[data['科目代码'] == dm])>0):
                    net_asset = float(data[data['科目代码'] == dm]['市值'].values[0])
                    break

            if(net_asset==0):
                for dm in self.debt_dmlist:
                    if (len(data[data['科目代码'] == dm]) > 0):
                        debt = float(data[data['科目代码'] == dm]['市值'].values[0])
                        net_asset=total_asset-debt
                        break

            leverage = total_asset / net_asset
            # A股
            sh=pd.DataFrame()
            for dm in self.ashare_dmlist:
                if(len(data[data['科目代码'].str.startswith(dm)])>0):
                    sh = data[data['科目代码'].str.startswith(dm)]
                    break
            # sh = data[data['科目代码'].str.startswith('11020101')]
            sz=pd.DataFrame()
            for dm in self.szshare_dmlist:
                if(len(data[data['科目代码'].str.startswith(dm)])>0):
                    sz = data[data['科目代码'].str.startswith(dm)]
                    break
            cyb = pd.DataFrame()
            for dm in self.cyb_dmlistt:
                if (len(data[data['科目代码'].str.startswith(dm)]) > 0):
                    cyb = data[data['科目代码'].str.startswith(dm)]
                    break
            kcb = pd.DataFrame()
            for dm in self.kcb_dmlist:
                if (len(data[data['科目代码'].str.startswith(dm)]) > 0):
                    kcb = data[data['科目代码'].str.startswith(dm)]
                    break

            if(len(sh)==0 and len(sz)==0 and len(cyb)==0 and len(kcb)==0):
                print('No stock exist for {0} at {1}..'.format(fund_name,date))
                continue

            equity_a = pd.concat([sh, sz, cyb, kcb], axis=0)

            equity_a['len'] = equity_a['科目代码'].apply(lambda x: len(x))
            equity_a = equity_a[equity_a['len'] > 10]

            if("." not in equity_a['科目代码'].values[0]):
                equity_a['ticker'] = equity_a['科目代码'].apply(lambda x: x[-6:])
            else:
                equity_a['ticker'] = equity_a['科目代码'].apply(lambda x: x[-8:-2])

            equity_a['weight'] = equity_a['市值'].astype(float) / net_asset
            equity_a = equity_a.rename(columns={"科目名称": "sec_name"})[['ticker', 'sec_name', 'weight']]
            # 港股
            hk1 = data[data['科目代码'].str.startswith('11028101')]
            hk2 = data[(data['科目代码'].str.startswith('11028201')) | (data['科目代码'].str.startswith('11028301'))]
            equity_hk = pd.concat([hk1, hk2], axis=0).fillna('')
            equity_hk['len'] = equity_hk['科目代码'].apply(lambda x: len(x))
            equity_hk = equity_hk[equity_hk['len'] > 8]
            equity_hk['ticker'] = equity_hk['科目代码'].apply(lambda x: x[-6:])
            equity_hk['科目名称'] = equity_hk['科目名称'].apply(lambda x: x.strip())  # add
            equity_hk['weight'] = equity_hk['市值'].astype(float) / net_asset
            equity_hk = equity_hk.rename(columns={"科目名称": "sec_name"})[['ticker', 'sec_name', 'weight']]
            equity_hk = equity_hk.groupby(['sec_name', 'ticker'])['weight'].sum().reset_index()
            # 债券
            tmp = data[data['科目代码'] == '1103']
            if tmp.empty:
                bond_df = pd.DataFrame()
            else:
                bond_ratio = tmp['市值'].astype(float).values[0] / net_asset
                bond_df = pd.DataFrame(columns=['ticker', 'sec_name', 'weight'])
                bond_df.loc[0] = ['b00001', '债券投资', bond_ratio]
            # 基金
            for dm in self.jjtz_dmlist:
                if (len(data[data['科目代码']==dm]) > 0):
                    tmp = data[data['科目代码'] == dm]
                    break
            if tmp.empty:
                fund_df = pd.DataFrame()
            else:
                fund_ratio = tmp['市值'].astype(float).values[0] / net_asset
                fund_df = pd.DataFrame(columns=['ticker', 'sec_name', 'weight'])
                fund_df.loc[0] = ['f00001', '基金投资', fund_ratio]

            df = pd.concat([equity_a, equity_hk, bond_df, fund_df], axis=0)
            # 其他类
            cash_df = pd.DataFrame(columns=['ticker', 'sec_name', 'weight'])
            cash_df.loc[0] = ['c00001', '现金类投资', leverage - df['weight'].sum()]
            df = pd.concat([df, cash_df], axis=0)
            df['trade_date'] = date
            if(len(df[df['ticker'].str[0].isin(['0', '3', '6'])])>0):
                portfolio_weight_list.append(df)

        portfolio_weight_df = pd.concat(portfolio_weight_list)
        portfolio_weight_df['fund_name'] = fund_name

        return  portfolio_weight_df

    def _load_portfolio_weight(self):
        filenames = os.listdir(self.data_path)
        filenames = [x for x in filenames if x.split('.')[-1] in ['xls', 'xlsx']]

        portfolio_weight_list = []
        for file_name in filenames:
            if self.fund_name == '亘曦2号':
                date = file_name.split('.')[0].split('_')[-1][:-3].replace('-', '')
            elif self.fund_name in ['富乐一号', '仁布积极进取1号']:
                date = file_name.split('.')[0].split('_')[-2]
            else:
                date = file_name.split('.')[0].split('_')[-1]
            # shift_date
            date = self._shift_date(date)
            data = pd.read_excel(
                os.path.join(self.data_path, file_name), sheet_name=0, header=3).dropna(subset=['科目代码'])
            net_asset = data[data['科目代码'] == '基金资产净值:']['市值'].values[0]
            total_asset = data[data['科目代码'] == '资产类合计:']['市值'].values[0]
            leverage = total_asset / net_asset
            # A股
            sh = data[data['科目代码'].str.startswith('11020101')]
            sz = data[data['科目代码'].str.startswith('11023101')]
            cyb = data[data['科目代码'].str.startswith('11024101')]
            kcb = data[data['科目代码'].str.startswith('1102C101')]
            equity_a = pd.concat([sh, sz, cyb, kcb], axis=0)
            # sh1 = data[data['科目代码'].str.startswith('11021101')]
            # sz1 = data[data['科目代码'].str.startswith('11021201')]
            # cyb1 = data[data['科目代码'].str.startswith('11021501')]
            # kcb1 = data[data['科目代码'].str.startswith('1102D201')]
            # xsg = data[data['科目代码'].str.startswith('11028401')]
            # equity_cr = pd.concat([sh1, sz1, cyb1, kcb1, xsg], axis=0)
            # equity_a = pd.concat([equity_a, equity_cr], axis=0)
            equity_a['len'] = equity_a['科目代码'].apply(lambda x: len(x))
            equity_a = equity_a[equity_a['len'] > 8]
            equity_a['ticker'] = equity_a['科目代码'].apply(lambda x: x[-6:])
            equity_a['weight'] = equity_a['市值'] / net_asset
            equity_a = equity_a.rename(columns={"科目名称": "sec_name"})[['ticker', 'sec_name', 'weight']]
            # 港股
            hk1 = data[data['科目代码'].str.startswith('11028101')]
            hk2 = data[(data['科目代码'].str.startswith('11028201')) | (data['科目代码'].str.startswith('11028301'))]
            equity_hk = pd.concat([hk1, hk2], axis=0)
            equity_hk['len'] = equity_hk['科目代码'].apply(lambda x: len(x))
            equity_hk = equity_hk[equity_hk['len'] > 8]
            equity_hk['ticker'] = equity_hk['科目代码'].apply(lambda x: x[-6:])
            equity_hk['科目名称'] = equity_hk['科目名称'].apply(lambda x: x.strip())  # add
            equity_hk['weight'] = equity_hk['市值'] / net_asset
            equity_hk = equity_hk.rename(columns={"科目名称": "sec_name"})[['ticker', 'sec_name', 'weight']]
            equity_hk = equity_hk.groupby(['sec_name', 'ticker'])['weight'].sum().reset_index()
            # 债券
            tmp = data[data['科目代码'] == '1103']
            if tmp.empty:
                bond_df = pd.DataFrame()
            else:
                bond_ratio = tmp['市值'].values[0] / net_asset
                bond_df = pd.DataFrame(columns=['ticker', 'sec_name', 'weight'])
                bond_df.loc[0] = ['b00001', '债券投资', bond_ratio]
            # 基金
            tmp = data[data['科目代码'] == '1105']
            if tmp.empty:
                fund_df = pd.DataFrame()
            else:
                fund_ratio = tmp['市值'].values[0] / net_asset
                fund_df = pd.DataFrame(columns=['ticker', 'sec_name', 'weight'])
                fund_df.loc[0] = ['f00001', '基金投资', fund_ratio]

            df = pd.concat([equity_a, equity_hk, bond_df, fund_df], axis=0)
            # 其他类
            cash_df = pd.DataFrame(columns=['ticker', 'sec_name', 'weight'])
            cash_df.loc[0] = ['c00001', '现金类投资', leverage - df['weight'].sum()]
            df = pd.concat([df, cash_df], axis=0)
            df['trade_date'] = date
            portfolio_weight_list.append(df)

        portfolio_weight_df = pd.concat(portfolio_weight_list)
        portfolio_weight_df['fund_name'] = self.fund_name

        return portfolio_weight_df

    def Pre_test(self,fromdb=False):

        if (fromdb):
            data = self.valuation_data2DB(self.fund_code, self.date_list, self.fund_name)
        else:
            data = self._load_portfolio_weight()

        start_date=data['trade_date'].unique().tolist()[0]
        end_date=data['trade_date'].unique().tolist()[-1]

        HoldingAnalysor(self.fund_name, start_date=start_date, end_date=end_date,inputdf=data).get_construct_result()

    def writeToDB(self,fromdb=False):
        if self.is_increment == 1:
            if(fromdb):
                data=self.valuation_data2DB(self.fund_code,self.date_list,self.fund_name)
            else:
                data = self._load_portfolio_weight()
            trading_day_list = data['trade_date'].unique().tolist()
            sql_script = "delete from {} where trade_date in ({}) and fund_name = '{}'".format(
                self.table_name, ','.join(trading_day_list), self.fund_name)
            # delete first
            delete_duplicate_records(sql_script)
            # add new records

            WriteToDB().write_to_db(data, self.table_name)
        else:
            sql_script = """
                create table {}(
                id int auto_increment primary key,
                trade_date date not null,
                ticker varchar(10),
                sec_name varchar(20),
                weight decimal(5, 4),
                fund_name varchar(40))
            """.format(self.table_name)
            create_table(self.table_name, sql_script)
            data = self._load_portfolio_weight()
            WriteToDB().write_to_db(data, self.table_name)

class HoldingAnalysor:
    def __init__(self, fund_name, start_date, end_date, threshold=1,from_local_db=False,inputdf=None):
        self.fund_name = fund_name
        self.start_date = start_date
        self.end_date = end_date
        self.threshold = threshold
        self.theme_col = ['大金融', '消费', 'TMT', '周期', '制造']
        self.theme_map = dict(zip(self.theme_col,
                             [['银行','非银金融','房地产'],
                              ['食品饮料','家用电器','医药生物','社会服务','农林牧渔','商贸零售','美容护理'],
                              ['通信','计算机','电子','传媒','国防军工'],
                              ['钢铁','有色金属','建筑装饰','建筑材料','基础化工','石油石化','煤炭','环保','公用事业'],
                              ['交通运输','机械设备','汽车','纺织服饰','轻工制造','电力设备']
                              ]
                             ))
        self.index_code_map =pd.DataFrame()
        self.index_code_map['col_name']=['农林牧渔','基础化工','钢铁','有色金属','电子','家用电器','食品饮料',
                           '纺织服饰','轻工制造','医药生物','公用事业','交通运输','房地产','商贸零售',
                           '社会服务','综合','建筑材料','建筑装饰','电力设备','国防军工','计算机','传媒',
                           '通信','银行','非银金融','汽车','机械设备','煤炭','石油石化','环保','美容护理']
        self.index_code_map['index_name']=['801010','801030','801040','801050','801080','801110',
                              '801120','801130','801140','801150','801160','801170',
                              '801180','801200','801210','801230','801710','801720',
                              '801730','801740','801750','801760','801770','801780',
                              '801790','801880','801890','801950','801960','801970','801980']

        if(inputdf is None):
            self._load_data(from_local_db)
        else:self._load_data(from_local_db,inputdf)

    def _load_portfolio_weight(self,from_local_db):

        if(from_local_db):
            from hbshare.fe.XZ import  db_engine
            localdb=db_engine.PrvFunDB().engine
            sql="select * from prv_fund_holding where jjdm='{0}' and trade_date >= '{1}' and trade_date <= '{2}'"\
                .format(self.fund_name,self.start_date,self.end_date)
            holding_df=pd.read_sql(sql,con=localdb).drop_duplicates(['ticker', 'trade_date'],keep='last')
        else:
            sql="select * from st_hedge.r_st_sm_subjective_fund_holding where jjdm='{0}' and trade_date >= '{1}' and trade_date <= '{2}' "\
                .format(self.fund_name,self.start_date,self.end_date)
            holding_df=hbdb.db2df(sql,db='highuser')

        holding_df.loc[(holding_df['ticker'].str.contains('H'))
                       &(holding_df['ticker'].str[0]!='H'),'ticker']=['H'+x[0:4] for x in holding_df.loc[(holding_df['ticker'].str.contains('H'))
                       &(holding_df['ticker'].str[0]!='H')]['ticker']]

        holding_df['trade_date']=holding_df['trade_date'].astype(str)
        holding_df['ym'] = holding_df['trade_date'].str[0:6]
        holding_df=pd.merge(holding_df
                            ,holding_df.sort_values('trade_date').drop_duplicates('ym',keep='last')[['trade_date']]
                            ,how='inner',on='trade_date')
        return holding_df[['trade_date', 'ticker', 'sec_name', 'weight','dwcb','sl','value_increased']]

    @staticmethod
    def _load_shift_date(date):
        trade_dt = datetime.datetime.strptime(date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=100)).strftime('%Y%m%d')

        sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            pre_date, date)
        res = hbs.db_data_query('readonly', sql_script, page_size=5000)
        df = pd.DataFrame(res['data']).rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                     "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

        trading_day_list = df[df['isMonthEnd'] == 1]['calendarDate'].tolist()

        return trading_day_list[-1]

    @staticmethod
    def _load_benchmark_weight(benchmark_id, shift_date, date):
        sql_script = "SELECT * FROM hsjy_gg.SecuMain where SecuCategory = 4 and SecuCode = '{}'".format(benchmark_id)
        res = hbs.db_data_query('readonly', sql_script)
        index_info = pd.DataFrame(res['data'])
        inner_code = index_info.set_index('SECUCODE').loc[benchmark_id, 'INNERCODE']

        sql_script = "SELECT (select a.SecuCode from hsjy_gg.SecuMain a where a.InnerCode = b.InnerCode and " \
                     "rownum = 1) SecuCode, b.EndDate, b.Weight FROM hsjy_gg.LC_IndexComponentsWeight b WHERE " \
                     "b.IndexCode = '{}' and b.EndDate = to_date('{}', 'yyyymmdd')".format(inner_code, shift_date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
        weight_df = data.rename(
            columns={"SECUCODE": "ticker", "ENDDATE": "effDate", "WEIGHT": "weight"})
        weight_df['benchmark_id'] = benchmark_id
        weight_df['trade_date'] = date

        if(len(weight_df)==0):
            return  pd.DataFrame(columns=['trade_date', 'ticker', 'benchmark_id'])
        else:
            return weight_df[['trade_date', 'ticker', 'benchmark_id']]

    @staticmethod
    def _load_security_sector(equity_portfolio_weight,theme_cluster):

        sql="select a.zqdm,b.yjxymc,b.xxfbrq,b.ejxymc,b.sjxymc from st_ashare.t_st_ag_zqzb a left join st_ashare.t_st_ag_gshyhfb b on a.gsdm=b.gsdm where a.zqlb=1 and b.xyhfbz={0} and a.sszt=1 and a.zqdm in ({1}) "\
            .format(38,util.list_sql_condition(equity_portfolio_weight['ticker'].unique().tolist()))
        ind_map=hbdb.db2df(sql,db='alluser')
        ind_map.reset_index(drop=True,inplace=True)
        ind_map.sort_values(['zqdm','xxfbrq'],inplace=True)
        temp=ind_map['zqdm']
        temp.drop_duplicates(keep='last', inplace=True)
        ind_map=ind_map.loc[temp.index][['zqdm','yjxymc','ejxymc','sjxymc']]

        # ind_hld=pd.merge(equity_portfolio_weight,ind_map,how='left',left_on='ticker',right_on='zqdm')

        lista=[]
        listb=[]
        for theme in theme_cluster.keys():
            for col in theme_cluster[theme]:
                lista.append(col)
                listb.append(theme)
        ind2thememap=pd.DataFrame()
        ind2thememap['industry_name']=lista
        ind2thememap['theme']=listb

        ind_hld=pd.merge(ind_map,ind2thememap,left_on='yjxymc',right_on='industry_name',how='left')\
            .rename(columns={'zqdm':'ticker'})

        return ind_hld[['ticker','yjxymc', 'ejxymc', 'sjxymc','theme']]

    @staticmethod
    def _load_security_value(equity_portfolio_weight):
        ticker_list=equity_portfolio_weight['ticker'].unique().tolist()
        trading_day_list = sorted(equity_portfolio_weight['trade_date'].unique())
        value_data_list = []
        trunk_size=800
        for date in trading_day_list:
            # 主板
            date_data=[]
            for i in range(int(np.floor(len(ticker_list)/trunk_size)+1)):
                temp_ticker_list = ticker_list[i * trunk_size:(i + 1) * trunk_size]

                sql_script = "SELECT PE, PB, DividendRatio, TotalMV, SecuCode FROM " \
                             "(SELECT b.PE, b.PB, b.DividendRatio, b.TotalMV, a.SecuCode, " \
                             "row_number() over(partition by a.InnerCode order by a.InnerCode) rn FROM " \
                             "hsjy_gg.LC_DIndicesForValuation b join hsjy_gg.SecuMain a on a.InnerCode = b.InnerCode and " \
                             "a.SecuMarket in (83, 90) and a.SecuCategory = 1 WHERE " \
                             "b.TradingDay = to_date('{}', 'yyyymmdd') and a.SecuCode in ({})) " \
                             "WHERE rn = 1".format(date, ','.join("'{0}'".format(x) for x in temp_ticker_list))
                res = hbs.db_data_query('readonly', sql_script, page_size=5000)
                data_main = pd.DataFrame(res['data']).rename(columns={"PE": "PETTM"})
                # if(len(data_main)==0):

                start_date=str(int(date[0:4])-1)+date[4:6]+'01'
                end_date=date
                sql = """select b.SecuCode,a.OperProfitGrowRate3Y  as OperatingRevenueYOY,
                a.NPPCCGrowRate3Y as NetProfitGrowRate,a.ROETTM as ROE,a.EndDate from hsjy_gg.SecuMain b left join hsjy_gg.LC_MainIndexNew a on a.CompanyCode=b.CompanyCode 
                where b.SecuCode in ({0}) and a.EndDate>=to_date('{1}','yyyymmdd')  and a.EndDate<=to_date('{2}','yyyymmdd')  """.format(util.list_sql_condition(temp_ticker_list),
                                                                                           start_date,end_date)
                df1 =pd.DataFrame(hbs.db_data_query('readonly', sql, page_size=5000)['data'])
                if(len(df1)==0):
                    df1=pd.DataFrame(columns=['SECUCODE', 'ROE', 'NETPROFITGROWRATE', 'OPERATINGREVENUEYOY',
               'ENDDATE', 'ROW_ID'])
                df1=df1.drop('ROW_ID', axis=1)
                df1=df1.sort_values(['SECUCODE','ENDDATE']).drop_duplicates(['SECUCODE'],keep='last')
                data_main=pd.merge(data_main,df1.drop('ENDDATE',axis=1),how='left',on='SECUCODE')

                # 科创板
                sql_script = "SELECT PETTM, PB, DividendRatio, TotalMV, SecuCode FROM " \
                             "(SELECT b.PETTM, b.PB, b.DividendRatio, b.TotalMV, a.SecuCode, " \
                             "row_number() over(partition by a.InnerCode order by a.InnerCode) rn FROM " \
                             "hsjy_gg.LC_STIBDIndiForValue b join hsjy_gg.SecuMain a on a.InnerCode = b.InnerCode and " \
                             "a.SecuMarket in (83, 90) and a.SecuCategory = 1 WHERE " \
                             "b.TradingDay = to_date('{}', 'yyyymmdd') and a.SecuCode in ({})) " \
                             "WHERE rn = 1".format(date, ','.join("'{0}'".format(x) for x in temp_ticker_list))
                res = hbs.db_data_query('readonly', sql_script, page_size=5000)
                data_stib = pd.DataFrame(res['data'])

                if(len(data_stib)>0):
                    sql = """select b.CompanyCode,b.InnerCode,a.ROETTM as ROE,b.SecuCode,a.ORComGrowRateThreeY as OperatingRevenueYOY,a.NPPCCGrowRateThreeY as NetProfitGrowRate,a.EndDate 
                    from hsjy_gg.LC_STIBMainIndex a left join hsjy_gg.SecuMain b on a.CompanyCode=b.CompanyCode
                     where b.SecuCode in ({0}) and a.EndDate>=to_date('{1}','yyyymmdd')  and a.EndDate<=to_date('{2}','yyyymmdd') and a.IfAdjusted=2 and a.IfMerged=1""" \
                        .format(util.list_sql_condition(temp_ticker_list),
                                                                                                     start_date,end_date)

                    df1 =pd.DataFrame(hbs.db_data_query('readonly', sql, page_size=5000)['data']).drop('ROW_ID',axis=1)
                    df1=df1.sort_values(['SECUCODE','ENDDATE']).drop_duplicates(['SECUCODE'],keep='last')
                    data_stib = pd.merge(data_stib, df1.drop('ENDDATE', axis=1), how='left', on='SECUCODE')

                data = pd.concat([data_main, data_stib]).rename(columns={"SECUCODE": "ticker", "TOTALMV": "MarketValue"})
                data['MarketValue'] /= 1e+8
                del data['ROW_ID']
                data = data.dropna(subset=['ticker'])
                data['trade_date'] = date
                date_data.append(data)


            value_data_list.append(pd.concat(date_data,axis=0))

        security_value_df = pd.concat(value_data_list)

        equity_portfolio_weight=pd.merge(equity_portfolio_weight,security_value_df,how='left',on=['ticker','trade_date'])

        return equity_portfolio_weight

    @staticmethod
    def _load_security_price(equity_portfolio_weight):

        ticker_list=equity_portfolio_weight['ticker'].unique().tolist()
        date_list=equity_portfolio_weight['trade_date'].unique().tolist()

        trunk_size = 800
        price_df=[]
        for i in range(int(np.floor(len(ticker_list) / trunk_size) + 1)):
            temp_ticker_list = ticker_list[i * trunk_size:(i + 1) * trunk_size]
            sql = """
            select ZQDM,JYRQ,SPJG from FUNDDB.ZGJY where ZQDM in ({0}) and DRJJ is not null and JYRQ in ({1})
             """.format(util.list_sql_condition(temp_ticker_list),
                        util.list_sql_condition(date_list))

            price_df.append(hbdb.db2df(sql, db='readonly').drop('ROW_ID', axis=1))
        price_df=pd.concat(price_df,axis=0)
        equity_portfolio_weight=pd.merge(equity_portfolio_weight,price_df,
                                         how='left',left_on=['ticker','trade_date'],
                                         right_on=['ZQDM','JYRQ']).drop(['ZQDM','JYRQ'],
                                                                        axis=1).rename(columns={'SPJG':'close_price'})
        return  equity_portfolio_weight

    @staticmethod
    def _ticker_shift_ratio(equity_weight):
        date_list=equity_weight['trade_date'].sort_values().unique().tolist()

        shift_ratio_df=pd.DataFrame(columns=['trade_date','buy','sell','mv'])
        shift_ratio_df.loc[0]=[date_list[0],0,0,
                               (equity_weight[equity_weight['trade_date']==date_list[0]]['sl']
                                *equity_weight[equity_weight['trade_date']==date_list[0]]['close_price']).sum()]

        for i in range(1,len(date_list)):
            t0=date_list[i-1]
            t1=date_list[i]
            last_hld=equity_weight[equity_weight['trade_date']==t0].drop('trade_date',axis=1)
            current_hld = equity_weight[equity_weight['trade_date'] == t1].drop('trade_date',axis=1)

            difference=pd.merge(current_hld,last_hld,how='outer',on='ticker').fillna(0)
            difference['quantity_change']=difference['sl_x'] - difference['sl_y']
            buy=(difference[difference['quantity_change']>0]['sl_x'].astype(float)\
                *difference[difference['quantity_change']>0]['dwcb_x'].astype(float)-difference[difference['quantity_change']>0]['sl_y'].astype(float)\
                *difference[difference['quantity_change']>0]['dwcb_y'].astype(float)).sum()
            sell=(difference[difference['quantity_change']<0]['sl_x'].astype(float)\
                *difference[difference['quantity_change']<0]['close_price_x'].astype(float)-difference[difference['quantity_change']<0]['sl_y'].astype(float)\
                *difference[difference['quantity_change']<0]['close_price_y'].astype(float)).sum()

            shift_ratio_df.loc[i] = [t1,np.abs(buy),np.abs(sell),
                                     (current_hld['sl']*current_hld['close_price']).sum()]


        name_list=['one_period_hsl','two_period_hsl','','four_period_hsl']
        outputdf=pd.DataFrame()
        outputdf['trade_date']=shift_ratio_df['trade_date']
        for j in [0,1,3]:
            trade_quantity=shift_ratio_df.rolling(j+1).sum()[['buy','sell']].sum(axis=1)
            average_mv=shift_ratio_df.rolling(j+2).sum()['mv']/(j+2)
            outputdf[name_list[j]]=trade_quantity/average_mv

        if(len(outputdf)>1):
            time_delta=(datetime.datetime.strptime(outputdf['trade_date'].max(),"%Y%m%d")-\
                       datetime.datetime.strptime(outputdf['trade_date'].min(),"%Y%m%d")).days/365
            outputdf.loc[len(outputdf)]=['年化最小换手率',outputdf['one_period_hsl'].sum()/time_delta,'','']

        return  outputdf

    @staticmethod
    def ticker_contribution(ticker_list,inputdf,industry_index_ret):

        hld=inputdf.copy()
        hld=hld[hld['ticker'].isin(ticker_list)]
        date_list=hld['trade_date'].unique().tolist()
        date_list.sort()
        hld.set_index('trade_date',inplace=True)

        zqdm_list=hld['ticker'].unique().tolist()
        price_df=[]
        for m in range(int(np.ceil(len(zqdm_list)/500))):

            sql = """
            select ZQDM ,JYRQ ,SPJG from FUNDDB.ZGJY where  DRJJ is not null and JYRQ in ({0}) and ZQDM in ({1})
             """.format(util.list_sql_condition(date_list),
                        util.list_sql_condition(zqdm_list[m*500:(m+1)*500]))
            price_df.append(hbdb.db2df(sql, db='readonly').drop('ROW_ID', axis=1))
        price_df=pd.concat(price_df,axis=0)

        coutribution_df=pd.DataFrame()
        mimic_ind_ret=pd.DataFrame()

        if(len(date_list)>1):
            for i in range(1,len(date_list)):

                t0=date_list[i-1]
                t1=date_list[i]
                average_weight=pd.merge(hld[['ticker','weight']].loc[[t0]],hld[['ticker','weight']].loc[[t1]],
                                        how='outer',on='ticker').fillna(0)
                average_weight=pd.merge(average_weight,
                                        price_df[price_df['JYRQ']==t0][['ZQDM','SPJG']]
                                        ,how='left',left_on='ticker',right_on='ZQDM').drop('ZQDM',axis=1)
                average_weight=pd.merge(average_weight,
                                        price_df[price_df['JYRQ']==t1][['ZQDM','SPJG']]
                                        ,how='left',left_on='ticker',right_on='ZQDM').drop('ZQDM',axis=1)

                average_weight['avg_w']=average_weight[['weight_y','weight_x']].mean(axis=1)
                average_weight=pd.merge(average_weight,hld[['ticker','yjxymc']].drop_duplicates('ticker')
                                        ,how='left',on='ticker')
                average_weight=pd.merge(average_weight,
                                        average_weight.groupby('yjxymc').sum()['avg_w'].to_frame('ind_w')
                                        ,how='left',on='yjxymc')
                average_weight['adj_w']=average_weight['avg_w']/average_weight['ind_w']
                average_weight['adj_ret']=(average_weight['SPJG_y']/average_weight['SPJG_x']-1)\
                                               *average_weight['adj_w']


                average_weight['contribution']=(average_weight['SPJG_y']/average_weight['SPJG_x']-1)\
                                               *average_weight['avg_w']

                average_weight['trade_date']=t1

                mimic_ret=average_weight.groupby('yjxymc').sum()['adj_ret'].to_frame('mimic_ind_ret')
                mimic_ret['trade_date']=t1

                coutribution_df=pd.concat([coutribution_df,
                                           average_weight[['trade_date','ticker','contribution']]],axis=0)

                mimic_ind_ret=pd.concat([mimic_ind_ret,
                                           mimic_ret.reset_index(drop=False)],axis=0)

            mimic_ind_ret=pd.merge(mimic_ind_ret,industry_index_ret[['zqdm','ret','jyrq']]
                                   ,how='left',left_on=['yjxymc','trade_date'],right_on=['zqdm','jyrq'])
            industry_mimic_dict=dict()
            for ind in mimic_ind_ret['yjxymc'].unique():
                tempdf=mimic_ind_ret[mimic_ind_ret['yjxymc']==ind].set_index('jyrq')[['mimic_ind_ret','ret']]
                tempdf=tempdf+1
                tempdf=tempdf.cumprod()
                industry_mimic_dict[ind]=tempdf.rename(columns={'mimic_ind_ret':'模拟净值'
                    ,'ret':'行业指数'})

            coutribution_df=coutribution_df.groupby('ticker').sum().reset_index()

            coutribution_df=pd.merge(coutribution_df
                                     ,hld[['ticker','sec_name','yjxymc','ejxymc','sjxymc']].drop_duplicates('ticker'),how='left',on='ticker')


            coutribution_df['name_per']=coutribution_df['sec_name'].astype(str)+"("\
                                           +(coutribution_df['contribution']*100).astype(str).str[0:4]+"%),"

            ind_contribution_list=[]
            ind_contribution=coutribution_df.copy()
            for industry_lv in ['yjxymc','ejxymc','sjxymc']:
                tempdf=ind_contribution.groupby([industry_lv]).sum().reset_index()
                tempdf['industry_lv']=industry_lv

                ind_contribution.sort_values('contribution',ascending=False,inplace=True)
                tempdf2=ind_contribution[[industry_lv,'name_per']].groupby(
                                                 industry_lv).sum().reset_index().rename(columns={'name_per':'个股贡献'})
                tempdf=pd.merge(tempdf,tempdf2,how='left',on=industry_lv).rename(columns={industry_lv:'industry_name'})

                ind_contribution_list.append(tempdf)

            ind_contribution_list=pd.concat(ind_contribution_list,axis=0)
            return  ind_contribution_list,industry_mimic_dict
        else:
            return pd.DataFrame(columns=['','']),pd.DataFrame(columns=['',''])


    def _load_data(self,from_local_db,inputdf=None):

        if(inputdf is None):
            portfolio_weight_df = self._load_portfolio_weight(from_local_db)
        else:
            portfolio_weight_df=inputdf
        date_list = sorted(portfolio_weight_df['trade_date'].unique())
        benchmark_weight = []
        for date in date_list:
            shift_date = self._load_shift_date(date)
            weight_300 = self._load_benchmark_weight('000300', shift_date, date)
            weight_500 = self._load_benchmark_weight('000905', shift_date, date)
            weight_1000 = self._load_benchmark_weight('000852', shift_date, date)
            benchmark_weight.append(pd.concat([weight_300, weight_500, weight_1000]))

        benchmark_weight = pd.concat(benchmark_weight)
        portfolio_weight_df = pd.merge(portfolio_weight_df.fillna(0), benchmark_weight, on=['trade_date', 'ticker'],
                                       how='left').fillna('other')

        equity_portfolio_weight = portfolio_weight_df[portfolio_weight_df['ticker'].str[0].isin(['0', '3', '6'])].drop(['sec_name', 'dwcb','sl', 'value_increased','benchmark_id'],axis=1)
        equity_portfolio_weight=pd.merge(equity_portfolio_weight,
                                     self._load_security_sector(equity_portfolio_weight,self.theme_map),
                                     how='left',on='ticker')

        equity_portfolio_weight = self._load_security_value(equity_portfolio_weight)

        equity_portfolio_weight = self._load_security_price(equity_portfolio_weight)

        portfolio_weight_df=pd.merge(portfolio_weight_df,equity_portfolio_weight,
                                     how='left',on=['trade_date', 'ticker','weight'])

        industry_index_ret=self.get_industry_index_ret(equity_portfolio_weight['trade_date'].unique().tolist())

        #calculate the ticker contribution
        ticker_contribution,industry_mimic_dict=self.ticker_contribution(equity_portfolio_weight['ticker'].unique().tolist()
                                 ,portfolio_weight_df[['trade_date','ticker', 'sec_name', 'weight','yjxymc', 'ejxymc', 'sjxymc']],industry_index_ret)

        #calculate the ticker_shift_ratio
        jjhsl=self._ticker_shift_ratio(
            portfolio_weight_df[portfolio_weight_df['ticker'].str[0].isin(['0', '3', '6'])][['trade_date',
                                                                                             'ticker','sl','dwcb','close_price']])

        #get the value and size exp from local db
        sql="select * from hbs_prv_style_exp where jjdm='{}'".format(self.fund_name)
        value_exp=pd.read_sql(sql,con=localdb)
        sql="select * from hbs_prv_size_exp where jjdm='{}'".format(self.fund_name)
        size_exp=pd.read_sql(sql,con=localdb)

        #get jj pic from local db
        sql="SELECT * from  jjpic_prv_value_p_hbs where jjdm='{}' ".format(self.fund_name)
        style_pic=pd.read_sql(sql,con=localdb)
        sql="SELECT * from  jjpic_prv_size_p_hbs where jjdm='{}' ".format(self.fund_name)
        size_pic=pd.read_sql(sql,con=localdb)
        sql = "SELECT * from  jjpic_prv_industry_p where jjdm='{}' ".format(self.fund_name)
        industry_pic = pd.read_sql(sql, con=localdb)
        sql="SELECT * from jjpic_prv_industry_detail_1 where jjdm='{}'".format(self.fund_name)
        industry_detil_pic=pd.read_sql(sql,con=localdb)
        self.data_param = {"portfolio_weight": portfolio_weight_df,
                           "value_exp": value_exp,
                           "size_exp": size_exp,
                           "style_pic": style_pic,
                           'size_pic':size_pic,
                           "industry_pic": industry_pic,
                           'industry_detil_pic':industry_detil_pic,
                           'jjhsl':jjhsl,
                           'contribution':ticker_contribution,
                           'industry_index_ret':industry_index_ret,
                           'industry_mimic_dict':industry_mimic_dict
                           }

    @staticmethod
    def get_industry_index_ret(date_list):

        industry_list = ['801010', '801030', '801040', '801050', '801080', '801110',
                           '801120', '801130', '801140', '801150', '801160', '801170',
                           '801180', '801200', '801210', '801230', '801710', '801720',
                           '801730', '801740', '801750', '801760', '801770', '801780',
                           '801790', '801880', '801890', '801950', '801960', '801970', '801980']
        new_col_name = ['农林牧渔', '基础化工', '钢铁', '有色金属', '电子', '家用电器', '食品饮料',
                        '纺织服饰', '轻工制造', '医药生物', '公用事业', '交通运输', '房地产', '商贸零售',
                        '社会服务', '综合', '建筑材料', '建筑装饰', '电力设备', '国防军工', '计算机', '传媒',
                        '通信', '银行', '非银金融', '汽车', '机械设备', '煤炭', '石油石化', '环保', '美容护理']
        index_code_map = dict(zip(industry_list, new_col_name))

        sql = "select zqdm,jyrq,spjg from st_market.t_st_zs_hqql where zqdm in ({0}) and jyrq in ({1}) " \
            .format(util.list_sql_condition(industry_list),util.list_sql_condition(date_list))
        navdf = hbdb.db2df(sql, db='alluser')
        navdf['zqdm']=[index_code_map[x] for x in navdf['zqdm']]
        navdf['ret']=navdf.groupby('zqdm').pct_change()['spjg']
        navdf['jyrq']=navdf['jyrq'].astype(str)

        return navdf

    @staticmethod
    def get_mimic_ret(inputdf,navdf):

        date_list=inputdf.index.tolist()

        tempdf=inputdf.copy().stack().reset_index().sort_values(['yjxymc','trade_date'])
        tempdf['avg_w']=(tempdf.groupby('yjxymc').rolling(2).mean())[0].values

        tempdf=pd.merge(tempdf,navdf,how='left'
                        ,left_on=['trade_date','yjxymc'],right_on=['jyrq','zqdm'])
        tempdf['total_ret']=tempdf['avg_w']*tempdf['ret']
        tempdf=tempdf.groupby('trade_date').sum()['total_ret']+1
        tempdf=tempdf.to_frame('ret')
        tempdf['nav']=tempdf[['ret']].cumprod()


        #get product nav
        sql="select jzrq,ljjz from st_hedge.t_st_jjjz where jzrq>='{0}' and jzrq<='{1}' and jjdm='{2}'"\
            .format(date_list[0],date_list[-1],jjdm)
        fund_nav=hbdb.db2df(sql,db='highuser')

        #if no nav data found then make it to be 1
        if(len(fund_nav)==0):
            fund_nav=pd.DataFrame()
            fund_nav['jzrq']=tempdf.index.tolist()
            fund_nav['ljjz']=1


        tempdf=pd.merge(tempdf,fund_nav.set_index('jzrq'),how='outer',left_index=True,right_index=True)
        tempdf['nav']=tempdf['nav'].interpolate(mehtod='cubic')
        tempdf['ljjz']=tempdf['ljjz'].interpolate(mehtod='cubic')
        tempdf=tempdf[(tempdf['nav'].notnull())&(tempdf['ljjz'].notnull())]
        for col in ['nav','ljjz']:
            tempdf[col]=tempdf[col]/tempdf[col].iloc[0]

        return tempdf[['nav','ljjz']].rename(columns={'nav':'模拟净值','ljjz':'实际净值'})

    @staticmethod
    def _calculate_asset_allo_series(portfolio_weight):
        date_list = sorted(portfolio_weight['trade_date'].unique())
        equity_a_series = portfolio_weight[portfolio_weight['ticker'].str[0].isin(['0', '3', '6'])].groupby(
            'trade_date')['weight'].sum().reindex(date_list).fillna(0.).to_frame('A股')
        equity_hk_series = portfolio_weight[portfolio_weight['ticker'].str.startswith('H')].groupby(
            'trade_date')['weight'].sum().reindex(date_list).fillna(0.).to_frame('港股')
        bond_series = portfolio_weight[portfolio_weight['ticker'].str.startswith('b')].groupby(
            'trade_date')['weight'].sum().reindex(date_list).fillna(0.).to_frame('债券')
        fund_series = portfolio_weight[portfolio_weight['ticker'].str.startswith('f')].groupby(
            'trade_date')['weight'].sum().reindex(date_list).fillna(0.).to_frame('基金')
        index_deri_series = portfolio_weight[portfolio_weight['sec_name'].astype(str).str.startswith('IF')].groupby(
            'trade_date')['weight'].sum().reindex(date_list).fillna(0.).to_frame('股指期货')
        pri_fund_series = portfolio_weight[portfolio_weight['ticker'].str.startswith('l')].groupby(
            'trade_date')['weight'].sum().reindex(date_list).fillna(0.).to_frame('私募理财')
        rq_series = portfolio_weight[portfolio_weight['ticker'].str.startswith('r')].groupby(
            'trade_date')['weight'].sum().reindex(date_list).fillna(0.).to_frame('买入返售金融资产')
        cash_series = portfolio_weight[portfolio_weight['ticker'].str.startswith('c')].groupby(
            'trade_date')['weight'].sum().reindex(date_list).fillna(0.).to_frame('其他')
        asset_allo_series = pd.concat(
            [equity_a_series, equity_hk_series, bond_series, fund_series,index_deri_series,pri_fund_series, rq_series,cash_series], axis=1)
        # asset_allo_series['现金类'] = 1 - asset_allo_series.sum(axis=1)

        return asset_allo_series

    @staticmethod
    def _calculate_ind_allo_series(portfolio_weight):

        grouped_df = portfolio_weight.groupby(['trade_date', 'yjxymc'])['weight'].sum().reset_index()
        pivot_df = pd.pivot_table(
            grouped_df, index='trade_date', columns='yjxymc', values='weight').sort_index().fillna(0.)

        sector_df = pd.DataFrame(index=pivot_df.index, columns=industry_cluster_dict.keys())
        for key, value in industry_cluster_dict.items():
            value_include = [x for x in value if x in pivot_df.columns]
            sector_df[key] = pivot_df[value_include].sum(axis=1)

        return pivot_df, sector_df

    @staticmethod
    def _calculate_mkt_dis(portfolio_weight):
        df = portfolio_weight.dropna(subset=['MarketValue'])
        df.loc[df['MarketValue'] < 100, 'sign'] = 'S'
        df.loc[(df['MarketValue'] >= 100) & (df['MarketValue'] < 300), 'sign'] = 'M'
        df.loc[(df['MarketValue'] >= 300) & (df['MarketValue'] < 1000), 'sign'] = 'L'
        df.loc[df['MarketValue'] >= 1000, 'sign'] = 'XL'
        grouped_df = df.groupby(['trade_date', 'sign'])['weight'].sum().reset_index()
        pivot_df = pd.pivot_table(
            grouped_df, index='trade_date', columns='sign', values='weight').sort_index().fillna(0.)

        name_map=dict(zip(['XL', 'L', 'M', 'S'],["1000亿以上", "300-1000亿",  "100-300亿", "100亿以下"]))
        for col in pivot_df.columns:
            pivot_df.rename(columns={col:name_map[col]},inplace=True)
        # pivot_df = pivot_df[['XL', 'L', 'M', 'S']].rename(
        #     columns={"XL": "1000亿以上", "L": "300-1000亿", "M": "100-300亿", "S": "100亿以下"})

        return pivot_df

    @staticmethod
    def plotly_area(df, title_text, range_upper=100,lower_range=0, figsize=(1200, 600)):
        fig_width, fig_height = figsize
        cols = df.index.tolist()

        data = []

        if(len(cols)<21):
            a=int(np.floor(len(cols)/3))
            b=len(cols)%3

            color_list=ams_color_lista[0:a+int(b>=1)]+\
                       ams_color_listb[0:a+int(b>=2)]+\
                       ams_color_listc[0:a]


            color_count=0
            for col in cols:
                tmp = go.Scatter(
                    x=df.columns.tolist(),
                    y=df.loc[col].values,
                    name=col,
                    mode='lines',
                    line=dict(width=0.5),
                    fill='tonexty',
                    marker=dict(color=color_list[color_count]),
                    stackgroup='one')
                data.append(tmp)
                color_count+=1
        else:
            for col in cols:
                tmp = go.Scatter(
                    x=df.columns.tolist(),
                    y=df.loc[col].values,
                    name=col,
                    mode='lines',
                    text=col,
                    showlegend=True,
                    line=dict(width=0.5),
                    fill='tonexty',
                    #fill='tozeroy',
                    #marker=dict(color=color_list[color_count]),
                    stackgroup='one')

                data.append(tmp)

        layout = go.Layout(
            title=title_text,
            autosize=False,
            width=fig_width,
            height=fig_height,
            showlegend=True,
            xaxis=dict(type='category'),
            yaxis=dict(
                type='linear',
                range=[lower_range, range_upper],
                dtick=np.round(range_upper/6),
                ticksuffix='%'))

        return data, layout

    @staticmethod
    def plotly_area_and_bar(df, title_text, bar_col,range_upper=100,lower_range=0, figsize=(1200, 600)):
        fig_width, fig_height = figsize
        cols = df.index.tolist()
        for col in bar_col:
            cols.remove(col)

        data = []

        if(len(cols)<21):
            a=int(np.floor(len(cols)/3))
            b=len(cols)%3

            color_list=ams_color_lista[0:a+int(b>=1)]+\
                       ams_color_listb[0:a+int(b>=2)]+\
                       ams_color_listc[0:a]


            color_count=0
            for col in cols:
                tmp = go.Scatter(
                    x=df.columns.tolist(),
                    y=df.loc[col].values,
                    name=col,
                    mode='lines',
                    line=dict(width=0.5),
                    fill='tonexty',
                    xaxis = 'x',
                    yaxis = 'y1',
                    marker=dict(color=color_list[color_count]),
                    stackgroup='one')
                data.append(tmp)
                color_count+=1

            for col in bar_col:
                trace = go.Bar(
                    x=df.columns.tolist(),
                    y=df.loc[col].values,
                    name=col,
                    xaxis='x',
                    yaxis='y2',
                    marker=dict(color='#000000'),
                    width=[0.05 * len(df.columns)] * len(df.columns),
                )
                data.append(trace)
                color_count += 1
        else:
            for col in cols:
                tmp = go.Scatter(
                    x=df.columns.tolist(),
                    y=df.loc[col].values,
                    name=col,
                    mode='lines',
                    text=col,
                    showlegend=True,
                    line=dict(width=0.5),
                    fill='tonexty',
                    stackgroup='one')

                data.append(tmp)


        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height,
            yaxis=dict(
                type='linear',
                overlaying='y2',
                range=[lower_range, range_upper],
                dtick=np.round(range_upper/6),
                ticksuffix='%'),

            yaxis2=dict(
                # tickformat=',.2%',
                side='right',
                # anchor='x',
                showgrid=False,
                range=[lower_range, range_upper],
                dtick=np.round(range_upper / 6),
                ticksuffix='%'
                # rangemode='tozero',

            ),
            # xaxis=dict(type='category'),
            template='plotly_white'
        )


        return data, layout

    @staticmethod
    def plotly_line(df, title_text,tickformat=',.0%', figsize=(1200, 600)):
        fig_width, fig_height = figsize
        data = []

        cols= df.columns
        a=int(np.floor(len(cols)/3))
        b=len(cols)%3

        color_list=ams_color_lista[0:a+int(b>=1)]+\
                   ams_color_listb[0:a+int(b>=2)]+\
                   ams_color_listc[0:a]

        color_count=0
        for col in cols:
            trace = go.Scatter(
                x=df.index.tolist(),
                y=df[col],
                name=col,
                mode="lines+markers",
                marker=dict(color=color_list[color_count])
            )
            data.append(trace)
            color_count+=1

        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height,
            yaxis=dict(tickfont=dict(size=12), tickformat=tickformat, showgrid=True),
            xaxis=dict(showgrid=True),
            template='plotly_white'
        )

        return data, layout

    @staticmethod
    def plotly_line_and_bar(df_line,df2_bar, title_text, figsize=(1200, 600)):
        fig_width, fig_height = figsize
        data = []

        cols=df_line.columns.tolist()+df2_bar.columns.tolist()
        a=int(np.floor(len(cols)/3))
        b=len(cols)%3

        color_list=ams_color_lista[0:a+int(b>=1)]+\
                   ams_color_listb[0:a+int(b>=2)]+\
                   ams_color_listc[0:a]

        color_count=0

        for col in df_line.columns:
            trace = go.Scatter(
                x=df_line.index.tolist(),
                y=df_line[col],
                name=col,
                mode="lines+markers",
                xaxis = 'x',
                yaxis = 'y1',
                marker=dict(color="#EEB2B4"),
            )
            data.append(trace)
            color_count+=1


        for col in df2_bar.columns:
            trace = go.Bar(
                x=df2_bar.index.tolist(),
                y=df2_bar[col],
                name=col,
                xaxis='x',
                yaxis='y2',
                marker=dict(color='#000000'),
                width=0.01*len(df2_bar),
            )
            data.append(trace)
            color_count += 1

        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height,
            yaxis=dict(
                title='Price',
                overlaying='y2',
                anchor='x',
                showgrid=False
                # rangemode='tozero'
            ),

            yaxis2=dict(
                title='Quantity',
                # tickformat=',.2%',
                side='right',
                anchor='x',
                showgrid=False
                # rangemode='tozero',

            ),
            xaxis=dict(showgrid=False),
            template='plotly_white'
        )

        return data, layout

    @staticmethod
    def plotly_double_y_line(df, title_text, figsize=(1200, 600)):
        fig_width, fig_height = figsize

        a=int(np.floor(2/3))
        b=2%3

        color_list=ams_color_lista[0:a+int(b>=1)]+\
                   ams_color_listb[0:a+int(b>=2)]+\
                   ams_color_listc[0:a]


        trace0 = go.Scatter(
            x=df.index.tolist(), y=df[df.columns[0]], mode="lines+markers", name=df.columns[0] + '(左轴)',marker=dict(color=color_list[0]))
        trace1 = go.Scatter(
            x=df.index.tolist(), y=df[df.columns[1]], mode="lines+markers", name=df.columns[1] + '(右轴)', yaxis='y2',marker=dict(color=color_list[1]))

        data = [trace0, trace1]

        layout = go.Layout(
            title=dict(text=title_text),
            autosize=False, width=fig_width, height=fig_height,
            yaxis=dict(tickfont=dict(size=12), showgrid=False),
            yaxis2=dict(overlaying='y', side='right'),
            xaxis=dict(showgrid=True),
            template='plotly_white'
        )

        return data, layout

    @staticmethod
    def draw_timeline_bar(df, title_text, min_value=0, min_height=600):
        num = int(df.gt(min_value).sum(axis=1).max())
        tl = Timeline(init_opts=opts.InitOpts(width='1200px', height='{}px'.format(max(25 * num, min_height))))

        for i in df.index.tolist():
            tmp = df.loc[i].dropna()
            tmp = tmp[tmp >= min_value].sort_values()
            bar = (
                Bar()
                .add_xaxis(tmp.index.tolist())
                .add_yaxis(
                    "持仓权重",
                    (tmp * 100).round(2).values.tolist(),
                    itemstyle_opts=opts.ItemStyleOpts(color="#37a2da"),
                    label_opts=opts.LabelOpts(is_show=False))
                .reversal_axis()
                .set_global_opts(
                    title_opts=opts.TitleOpts("{} (时间点: {})".format(title_text, i)),
                    xaxis_opts=opts.AxisOpts(
                        axislabel_opts=opts.LabelOpts(formatter="{value} %"),
                        splitline_opts=opts.SplitLineOpts(is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=0.3)))
                )
            )
            tl.add(bar, "{}年{}月".format(i[:4], i[4:6]))

        return tl

    @staticmethod
    def plotly_table(portfolio_weight_df, threshold=1.0,return_data=False):
        df = portfolio_weight_df[portfolio_weight_df['ticker'].str[0].isin(['0', '3', '6', 'H'])]
        df['weight'] *= 100.
        df['content'] = df['sec_name'].astype(str) + '（' + df['weight'].round(1).map(str) + '%）'
        df = df[df['weight'] >= threshold]
        max_len = int(df['trade_date'].value_counts().max())
        table_data = pd.DataFrame(index=np.arange(max_len), columns=sorted(df['trade_date'].unique()))
        for col in table_data.columns:
            tmp = df[df['trade_date'] == col].sort_values(by='weight', ascending=False)
            table_data.loc[:len(tmp) - 1, col] = tmp['content'].tolist()

        table_data.dropna(how='any', axis=0, inplace=True)

        fig = ff.create_table(table_data)
        if(return_data):
            return table_data
        else:
            return fig, table_data.shape[1]

    @staticmethod
    def plotly_change_table(portfolio_weight_df, threshold=1.0,return_data=False):
        df = portfolio_weight_df[portfolio_weight_df['ticker'].str[0].isin(['0', '3', '6', 'H'])]
        df['weight'] = (100 * df['weight']).round(1)
        pivot_df = pd.pivot_table(df, index=['ticker', 'sec_name'], columns='trade_date', values='weight').sort_index()
        pivot_df['mean'] = pivot_df.mean(axis=1)
        pivot_df = pivot_df[pivot_df.mean(axis=1) > threshold].sort_values(by='mean', ascending=False)
        del pivot_df['mean']
        pivot_df.fillna('-', inplace=True)
        res_df = pivot_df.reset_index().rename(columns={"ticker": "股票代码", "sec_name": "股票简称"})

        fig = ff.create_table(res_df)
        if(return_data):
            return res_df
        else:
            return fig, res_df.shape[1]

    @staticmethod
    def get_construct_result(self, is_tl_show=False):
        portfolio_weight = self.data_param['portfolio_weight']
        benchmark_weight = self.data_param['benchmark_weight']
        security_sector_df = self.data_param['security_sector_df']
        security_value_df = self.data_param['security_value_df']
        # 资产配置时序
        asset_allo_series = self._calculate_asset_allo_series(portfolio_weight)
        # 行业配置时序
        industry_allo_df, sector_allo_df = self._calculate_ind_allo_series(portfolio_weight, security_sector_df)
        industry_cr = \
            pd.concat([industry_allo_df.apply(lambda x: x.nlargest(1).sum(), axis=1).to_frame('第一大行业'),
                       industry_allo_df.apply(lambda x: x.nlargest(3).sum(), axis=1).to_frame('前三大行业'),
                       industry_allo_df.apply(lambda x: x.nlargest(5).sum(), axis=1).to_frame('前五大行业')], axis=1)
        # 重仓持股
        equity_weight = portfolio_weight[~portfolio_weight['ticker'].str[0].isin(['b', 'f', 'c'])]
        equity_weight = pd.pivot_table(
            equity_weight, index='trade_date', columns='sec_name', values='weight').sort_index()
        tmp = equity_weight.fillna(0.)
        equity_cr = pd.concat([tmp.apply(lambda x: x.nlargest(3).sum(), axis=1).to_frame('cr3'),
                               tmp.apply(lambda x: x.nlargest(5).sum(), axis=1).to_frame('cr5'),
                               tmp.apply(lambda x: x.nlargest(10).sum(), axis=1).to_frame('cr10')], axis=1)
        # 平均PE/PB
        value_df = pd.merge(security_value_df, portfolio_weight, on=['trade_date', 'ticker']).dropna(
            subset=['PB', 'PETTM'])
        # 做一下剔除
        value_df = value_df[(value_df['PETTM'] <= 1000) & (value_df['PETTM'] >= -1000)]
        average_pe = value_df.groupby('trade_date').apply(
            lambda x: (x['weight'] * x['PETTM']).sum() / x['weight'].sum()).to_frame('平均市盈率')
        average_pb = value_df.groupby('trade_date').apply(
            lambda x: (x['weight'] * x['PB']).sum() / x['weight'].sum()).to_frame('平均市净率')
        average_pe_pb = pd.concat([average_pe, average_pb], axis=1)
        # 持仓宽基分布
        df = portfolio_weight[portfolio_weight['ticker'].str[0].isin(['0', '3', '6'])]
        df = pd.merge(df, benchmark_weight, on=['trade_date', 'ticker'], how='left').fillna('other')
        bm_dis = df.groupby(['trade_date', 'benchmark_id'])['weight'].sum().reset_index()
        bm_dis = pd.pivot_table(
            bm_dis, index='trade_date', columns='benchmark_id', values='weight').sort_index().fillna(0.)
        map_dict = {"000300": "沪深300", "000905": "中证500", "000852": "中证1000", "other": "1800以外"}
        bm_dis.columns = [map_dict[x] for x in bm_dis.columns]
        # bm_dis = bm_dis[['沪深300', '中证500', '中证1000', '1800以外']]
        # 持仓市值分布
        mkt_dis = self._calculate_mkt_dis(portfolio_weight, security_value_df)

        upper_range = np.ceil(asset_allo_series.sum(axis=1).max() / 0.2) * 20
        data, layout = self.plotly_area(100 * asset_allo_series.T, '资产配置走势', upper_range)
        plot_render({"data": data, "layout": layout}, width=1200, height=600)

        upper_range = np.ceil(industry_allo_df.sum(axis=1).max() / 0.2) * 20
        data, layout = self.plotly_area(100 * industry_allo_df.T, '行业配置走势', upper_range)
        plot_render({"data": data, "layout": layout}, width=1200, height=600)
        # fig = go.Figure(data=data, layout=layout)
        # plot_ly(fig, filename="D:\\主观股多估值表基地\\图表所在\\B-行业配置走势.html", auto_open=False)

        upper_range = np.ceil(sector_allo_df.sum(axis=1).max() / 0.2) * 20
        data, layout = self.plotly_area(100 * sector_allo_df.T, '板块配置走势', upper_range)
        plot_render({"data": data, "layout": layout}, width=1200, height=600)

        data, layout = self.plotly_line(industry_cr, '行业集中度走势')
        plot_render({"data": data, "layout": layout}, width=1200, height=600)

        if is_tl_show:
            tl_bar = self.draw_timeline_bar(industry_allo_df, "截面行业权重", min_value=0.02, min_height=350)
            html_content = tl_bar.render_embed()
            print("%html {}".format(html_content))
            # tl_bar.render('D:\\主观股多估值表基地\\图表所在\\D-持仓行业明细.html')

        fig, n = self.plotly_table(portfolio_weight)
        plot_render({"data": fig.data, "layout": fig.layout}, width=120*n, height=600)

        fig, n = self.plotly_change_table(portfolio_weight)
        plot_render({"data": fig.data, "layout": fig.layout}, width=80*n, height=600)

        data, layout = self.plotly_line(equity_cr, "持股集中度走势")
        plot_render({"data": data, "layout": layout}, width=1200, height=600)

        if is_tl_show:
            tl_bar = self.draw_timeline_bar(equity_weight, "截面持股权重", min_value=0.02)
            html_content = tl_bar.render_embed()
            print("%html {}".format(html_content))

        data, layout = self.plotly_double_y_line(average_pe_pb.round(1), "持股估值水平走势")
        plot_render({"data": data, "layout": layout}, width=1200, height=600)

        upper_range = np.ceil(bm_dis.sum(axis=1).max() / 0.2) * 20
        data, layout = self.plotly_area(100 * bm_dis.T, '宽基成分配置走势', upper_range)
        plot_render({"data": data, "layout": layout}, width=1200, height=600)

        upper_range = np.ceil(mkt_dis.sum(axis=1).max() / 0.2) * 20
        data, layout = self.plotly_area(100 * mkt_dis.T, '持股市值分布走势', upper_range)
        plot_render({"data": data, "layout": layout}, width=1200, height=600)

    @staticmethod
    def get_annotations(asset_allo_series):

        annotations=[]
        index_list = asset_allo_series.T.index.tolist()
        index_list.reverse()
        for asset in asset_allo_series.columns:
            # labeling the left_side of the plot
            max_value=asset_allo_series[asset].nlargest(1).values[0]
            if(max_value>0):
                x_index=asset_allo_series[asset].nlargest(1).index[0]
                x_position=asset_allo_series.index.tolist().index(x_index)/np.max([(len(asset_allo_series.index)-1),1])
                y_position=(asset_allo_series.T.loc[index_list]*100).loc[asset:][x_index].sum()-(asset_allo_series.T*100).loc[asset][x_index]+(asset_allo_series.T*100).loc[asset][x_index]/2
                if(x_position==0):
                    xanchor='left'
                elif(x_position==1):
                    xanchor='right'
                else:
                    xanchor='center'
                annotations.append(dict(xref='paper', x=x_position, y=y_position,
                                        xanchor=xanchor, yanchor='middle',
                                        text=asset,
                                        font=dict(family='Arial',
                                                  size=12),
                                        showarrow=False))

        return annotations

    @staticmethod
    def get_factor_return(start_date, end_date, style_list):

        style = util.list_sql_condition(style_list)
        sql = "select zqdm,jyrq,spjg from st_market.t_st_zs_hqql where zqdm in ({0}) and jyrq>='{1}' and  jyrq<='{2}'  " \
            .format(style, start_date, end_date)
        fac_ret_df = hbdb.db2df(sql, db='alluser')
        fac_ret_df['jyrq'] = fac_ret_df['jyrq'].astype(str)
        fac_ret_df.set_index('jyrq', drop=True, inplace=True)

        fac_ret_df['price'] = fac_ret_df['spjg']


        return fac_ret_df

    @staticmethod
    def get_ticker_price_fq(ticker_list,start_date,end_date):

        #get the stock price data
        sql = """
        select b.SecuCode as ZQDM,a.TradingDay as JYRQ,a.BackwardPrice as SPJG from hsjy_gg.SecuMain b left join hsjy_gg.QT_PerformanceData a on a.InnerCode=b.InnerCode where b.SecuCode in ({0})  and a.TradingDay>=to_date('{1}','yyyymmdd') and  a.TradingDay<=to_date('{2}','yyyymmdd')
         """.format(util.list_sql_condition(ticker_list),
                    start_date,end_date)
        price_df=hbdb.db2df(sql,db='readonly')

        sql = """
        select b.SecuCode as ZQDM,a.TradingDay as JYRQ,a.BackwardPrice as SPJG from hsjy_gg.SecuMain b left join hsjy_gg.LC_STIBPerformanceData a on a.InnerCode=b.InnerCode where b.SecuCode in ({0})  and a.TradingDay>=to_date('{1}','yyyymmdd') and  a.TradingDay<=to_date('{2}','yyyymmdd')
         """.format(util.list_sql_condition(ticker_list),
                    start_date,end_date)
        price_kcb_df = hbdb.db2df(sql, db='readonly')
        price_df=pd.concat([price_df,price_kcb_df],axis=0).drop('ROW_ID',axis=1)
        price_df.sort_values('JYRQ',inplace=True)
        price_df['JYRQ'] = price_df['JYRQ'].str[0:10].str.replace('-', '')

        return  price_df

    def get_hld_corr(self,equity_weight):

        corr_his=[]
        name_map=equity_weight.drop_duplicates(['ticker','sec_name']
                                               ,keep='last')[['ticker','sec_name']].rename(columns={'ticker':'ZQDM'}).reset_index(drop=True)
        # name_map=pd.DataFrame()
        # name_map['ZQDM']=equity_weight['ticker'].unique().tolist()
        # name_map['sec_name'] = equity_weight['sec_name'].unique().tolist()

        for date in equity_weight['trade_date'].unique():
            ticker_list=(equity_weight[equity_weight['trade_date'] == date].sort_values('weight'
                                                                                        ,ascending=False)).iloc[0:10][['ticker','yjxymc']]
            ind_list=self.index_code_map[self.index_code_map['col_name'].isin(ticker_list['yjxymc'].unique().tolist())]['index_name'].tolist()
            if(len(ind_list)==0):
                continue
            ticker_list=ticker_list['ticker']


            pricedf=self.get_ticker_price_fq(ticker_list,str(int(date[0:4])-1)+date[4:6]+'01',date)
            pricedf=pd.merge(pricedf,name_map,how='left',on='ZQDM')
            corr=pricedf.pivot_table('SPJG','JYRQ','sec_name').corr()
            corr = corr.reset_index().rename(columns={'sec_name': ''})
            corr['hld_date'] = date

            indexdf=self.get_factor_return(str(int(date[0:4])-1)+date[4:], date, ind_list)
            indexdf=pd.merge(indexdf.reset_index(),self.index_code_map,
                             how='left',left_on='zqdm',right_on='index_name')
            corr_ind = indexdf.pivot_table('price', 'jyrq', 'col_name').corr()
            corr_ind = corr_ind.reset_index().rename(columns={'col_name': ''})

            corr=pd.concat([corr,corr_ind],axis=1)

            corr_his.append(corr)

        return corr_his

    def save_construct_result2loacl(self,gsjc,jjjc,is_tl_show=False):
        import xlwings as xw

        asofdate=datetime.datetime.today().strftime('%Y%m%d')
        xls = xlwt.Workbook()
        for sheet in ['持仓分析（图）','行业画像','一级行业细节画像', '行业个股占比图','风格画像',
                      '前十大个股交易记录','前十大个股行业相关性', '基金换手率','重仓持股', '持仓时序','持仓贡献', '原始数据']:
            xls.add_sheet(sheet)

        authority=pd.read_excel(r"E:\GitFolder\docs\私募股多持仓分析\研究员对应表.xlsx")[['研究员','公司']]
        researcher_folder=authority[authority['公司']==gsjc]['研究员']
        if(len(researcher_folder)>0):
            researcher_folder=researcher_folder.values[0]
        else:
            researcher_folder='其他'

        template_folder = r"E:\GitFolder\docs\私募股多持仓分析\{2}\{3}_{0}_{1}.xls".format(self.fund_name,
                                                                                  asofdate,researcher_folder,jjjc)

        xls.save(template_folder)

        # template_folder = r"E:\GitFolder\docs\私募股多持仓分析\私募股多持仓分析_{0}_{1}.xls".format(self.fund_name,asofdate)
        app = xw.App(visible=False)
        wb = app.books.open(template_folder)
        # try:
        df_list=[]
        sheet_list=[]

        portfolio_weight = self.data_param['portfolio_weight']

        # 资产配置时序
        asset_allo_series = self._calculate_asset_allo_series(portfolio_weight)
        # 行业配置时序
        industry_allo_df, sector_allo_df = self._calculate_ind_allo_series(portfolio_weight)
        industry_cr = \
            pd.concat([industry_allo_df.apply(lambda x: x.nlargest(1).sum(), axis=1).to_frame('第一大行业'),
                       industry_allo_df.apply(lambda x: x.nlargest(3).sum(), axis=1).to_frame('前三大行业'),
                       industry_allo_df.apply(lambda x: x.nlargest(5).sum(), axis=1).to_frame('前五大行业')], axis=1)

        mimic_nav=self.get_mimic_ret(industry_allo_df,self.data_param['industry_index_ret'])


        # 重仓持股
        equity_weight = portfolio_weight[portfolio_weight['ticker'].str[0].isin(['0', '3', '6','H'])]
        equity_weight = pd.pivot_table(
            equity_weight, index='trade_date', columns='sec_name', values='weight').sort_index()
        tmp = equity_weight.fillna(0.)
        equity_cr = pd.concat([tmp.apply(lambda x: x.nlargest(3).sum(), axis=1).to_frame('cr3'),
                               tmp.apply(lambda x: x.nlargest(5).sum(), axis=1).to_frame('cr5'),
                               tmp.apply(lambda x: x.nlargest(10).sum(), axis=1).to_frame('cr10')], axis=1)
        # 平均PE/PB
        value_df = portfolio_weight.dropna(
            subset=['PB', 'PETTM'])
        # 做一下剔除
        value_df = value_df[(value_df['PETTM'] <= 1000) & (value_df['PETTM'] > 0)]
        average_pe = value_df.groupby('trade_date').apply(
            lambda x: (x['weight'] * x['PETTM']).sum() / x['weight'].sum()).to_frame('平均市盈率')
        average_pb = value_df.groupby('trade_date').apply(
            lambda x: (x['weight'] * x['PB']).sum() / x['weight'].sum()).to_frame('平均市净率')
        average_pe_pb = pd.concat([average_pe, average_pb], axis=1)
        # 持仓宽基分布
        df = portfolio_weight[portfolio_weight['ticker'].str[0].isin(['0', '3', '6'])]
        bm_dis = df.groupby(['trade_date', 'benchmark_id'])['weight'].sum().reset_index()
        bm_dis = pd.pivot_table(
            bm_dis, index='trade_date', columns='benchmark_id', values='weight').sort_index().fillna(0.)
        map_dict = {"000300": "沪深300", "000905": "中证500", "000852": "中证1000", "other": "1800以外"}
        bm_dis.columns = [map_dict[x] for x in bm_dis.columns]
        # bm_dis = bm_dis[['沪深300', '中证500', '中证1000', '1800以外']]
        # 持仓市值分布
        mkt_dis = self._calculate_mkt_dis(portfolio_weight)
        #基金净资产
        jjjzc =portfolio_weight[portfolio_weight['ticker']=='zc0001'][['trade_date','weight']].set_index('trade_date')

        #持仓相关性
        equity_weight = portfolio_weight[portfolio_weight['ticker'].str[0].isin(['0', '3', '6'])]
        corr_his=self.get_hld_corr(equity_weight)

        #新建临时文件夹存放图片
        newpath = r'E:\GitFolder\docs\私募股多持仓分析\pic_temp'

        upper_range = np.ceil(asset_allo_series.sum(axis=1).max() / 0.2) * 20
        data, layout = self.plotly_area_and_bar(100 * asset_allo_series.T, '资产配置走势',['股指期货'], upper_range,lower_range=asset_allo_series['股指期货'].min()*100)

        annotations=self.get_annotations(asset_allo_series.abs())

        save_pic2local(data,layout,newpath+r"\资产配置走势.png",annotations=annotations)
        ws = wb.sheets['持仓分析（图）']
        ws.clear()

        ws.pictures.add(newpath+r"\资产配置走势.png", left=ws.range('A1').left, top=ws.range('A1').top,
                        width=700, height=350)

        data, layout = self.plotly_line(jjjzc, "基金净资产走势",tickformat='.0')
        save_pic2local(data, layout, newpath + r"\基金净资产走势.png")
        ws.pictures.add(newpath+r"\基金净资产走势.png", left=ws.range('P1').left, top=ws.range('P1').top,
                        width=700, height=350)

        upper_range = np.ceil(sector_allo_df.sum(axis=1).max() / 0.2) * 20
        data, layout = self.plotly_area(100 * sector_allo_df.T, '板块配置走势', upper_range)
        save_pic2local(data, layout, newpath + r"\板块配置走势.png")
        ws.pictures.add(newpath+r"\板块配置走势.png", left=ws.range('A31').left, top=ws.range('A31').top,
                        width=700, height=350)

        data, layout = self.plotly_line(industry_cr, '行业集中度走势')
        save_pic2local(data, layout, newpath + r"\行业集中度走势.png")
        ws.pictures.add(newpath+r"\行业集中度走势.png", left=ws.range('P31').left, top=ws.range('P31').top,
                        width=700, height=350)

        if is_tl_show:
            tl_bar = self.draw_timeline_bar(industry_allo_df, "截面行业权重", min_value=0.02, min_height=350)
            html_content = tl_bar.render_embed()
            print("%html {}".format(html_content))
            # tl_bar.render('D:\\主观股多估值表基地\\图表所在\\D-持仓行业明细.html')

        top10_tickers=portfolio_weight[(portfolio_weight['ticker'].str[0].isin(['0','6','3']))
                                       &(portfolio_weight['ticker'].str.len()==6)].groupby('ticker').sum()['weight'].sort_values(ascending=False)[0:10].index.tolist()
        #get the stock price data
        trade_dt = datetime.datetime.strptime(portfolio_weight['trade_date'].min(), '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=30)).strftime('%Y%m%d')
        sql = """
        select b.SecuCode as ZQDM,a.TradingDay as JYRQ,a.BackwardPrice as SPJG from hsjy_gg.SecuMain b left join hsjy_gg.QT_PerformanceData a on a.InnerCode=b.InnerCode where b.SecuCode in ({0})  and a.TradingDay>=to_date('{1}','yyyymmdd') and  a.TradingDay<=to_date('{2}','yyyymmdd')
         """.format(util.list_sql_condition(top10_tickers),
                    pre_date,portfolio_weight['trade_date'].max())
        price_df=hbdb.db2df(sql,db='readonly')

        sql = """
        select b.SecuCode as ZQDM,a.TradingDay as JYRQ,a.BackwardPrice as SPJG from hsjy_gg.SecuMain b left join hsjy_gg.LC_STIBPerformanceData a on a.InnerCode=b.InnerCode where b.SecuCode in ({0})  and a.TradingDay>=to_date('{1}','yyyymmdd') and  a.TradingDay<=to_date('{2}','yyyymmdd')
         """.format(util.list_sql_condition(top10_tickers),
                    pre_date, portfolio_weight['trade_date'].max())
        price_kcb_df = hbdb.db2df(sql, db='readonly')
        price_df=pd.concat([price_df,price_kcb_df],axis=0).drop('ROW_ID',axis=1)
        price_df.sort_values('JYRQ',inplace=True)
        price_df['JYRQ'] = price_df['JYRQ'].str[0:10].str.replace('-', '')

        zcstock_df = self.plotly_table(portfolio_weight,return_data=True)
        df_list.append(zcstock_df)
        sheet_list.append('重仓持股')

        portfolio_weight_his= self.plotly_change_table(portfolio_weight,return_data=True)
        portfolio_weight_his['股票代码']=["'"+str(x) for x in portfolio_weight_his['股票代码']]
        df_list.append(portfolio_weight_his)
        sheet_list.append('持仓时序')
        portfolio_weight_his.to_excel('temp.xlsx')

        col_name_map=dict(zip(['SECUCODE_new','weight', 'sl', 'value_increased','benchmark_id',
                               'yjxymc', 'ejxymc', 'sjxymc', 'theme','MarketValue','DIVIDENDRATIO',
                               'NETPROFITGROWRATE','OPERATINGREVENUEYOY','trade_date','sec_name'],
                              ['股票代码','占净值比例', '持股数量', '估值增值','所属宽基指数',
                               '一级行业', '二级行业', '三级行业', '主题','市值','股息率','净利润增长率','主营收入增长率','交易日期','股票简称']))
        sql="select SecuCode,SecuMarket,InnerCode from hsjy_gg.SecuMain where  SecuCategory in (1,2)"
        stock_base_info=hbdb.db2df(sql,db='readonly').drop('ROW_ID',axis=1).fillna(90)
        stock_base_info.drop_duplicates(keep='last',inplace=True)
        stock_base_info['SECUCODE_new']=stock_base_info['SECUCODE']
        # stock_base_info.loc[stock_base_info['SECUCODE'].str[0]=='H',
        #                     'SECUCODE_new']=stock_base_info.loc[stock_base_info['SECUCODE'].str[0]=='H']['SECUCODE_new'].str[1:]+".HK"
        stock_base_info.loc[stock_base_info['SECUMARKET']==90,
                            'SECUCODE_new']=stock_base_info.loc[stock_base_info['SECUMARKET']==90]['SECUCODE_new']+".SZ"
        stock_base_info.loc[stock_base_info['SECUMARKET']==83,
                            'SECUCODE_new']=stock_base_info.loc[stock_base_info['SECUMARKET']==83]['SECUCODE_new']+".SH"

        portfolio_weight=pd.merge(portfolio_weight,stock_base_info,
                                  how='left',left_on='ticker',right_on='SECUCODE')\
            .drop(['SECUCODE','SECUMARKET'],axis=1)
        portfolio_weight.loc[portfolio_weight['ticker'].str[0]=='H',
                             'SECUCODE_new']="HK."+portfolio_weight.loc[portfolio_weight['ticker'].str[0]=='H']['ticker'].str[-4:]
        portfolio_weight.drop('ticker',axis=1,inplace=True)
        portfolio_weight.rename(columns=col_name_map,inplace=True)
        portfolio_weight['所属宽基指数']=[map_dict[x] for x in  portfolio_weight['所属宽基指数']]
        portfolio_weight.rename(columns={'dwcb':'单位成本'
            ,'close_price':'收盘价'},inplace=True)
        df_list.append(portfolio_weight[['交易日期', '股票代码','股票简称', '占净值比例', '持股数量','单位成本','收盘价',
                                         '估值增值',  '一级行业', '二级行业','三级行业', '主题','所属宽基指数',
                                         'PB', 'PETTM', '市值', '股息率', 'ROE', '净利润增长率', '主营收入增长率'
       ]])
        sheet_list.append('原始数据')


        df_list.append(self.data_param['industry_pic'])
        sheet_list.append('行业画像')

        df_list.append(self.data_param['industry_detil_pic'])
        sheet_list.append('一级行业细节画像')

        df_list.append(self.data_param['jjhsl'])
        sheet_list.append('基金换手率')

        df_list.append(self.data_param['contribution'])
        sheet_list.append('持仓贡献')


        data, layout =self.plotly_line(mimic_nav,'虚拟净值VS实际净值')
        save_pic2local(data,layout,newpath+r"\虚拟净值VS实际净值.png")

        data, layout = self.plotly_line(equity_cr, "持股集中度走势")
        save_pic2local(data, layout, newpath + r"\持股集中度走势.png")
        ws.pictures.add(newpath+r"\持股集中度走势.png", left=ws.range('A61').left, top=ws.range('A61').top,
                        width=700, height=350)

        if is_tl_show:
            tl_bar = self.draw_timeline_bar(equity_weight, "截面持股权重", min_value=0.02)
            html_content = tl_bar.render_embed()
            print("%html {}".format(html_content))

        data, layout = self.plotly_double_y_line(average_pe_pb.round(1), "持股估值水平走势")
        save_pic2local(data, layout, newpath + r"\持股估值水平走势.png")
        ws.pictures.add(newpath+r"\持股估值水平走势.png", left=ws.range('P61').left, top=ws.range('P61').top,
                        width=700, height=350)

        upper_range = np.ceil(bm_dis.sum(axis=1).max() / 0.2) * 20
        data, layout = self.plotly_area(100 * bm_dis.T, '宽基成分配置走势', upper_range)
        save_pic2local(data, layout, newpath + r"\宽基成分配置走势.png")
        ws.pictures.add(newpath+r"\宽基成分配置走势.png", left=ws.range('A91').left, top=ws.range('A91').top,
                        width=700, height=350)

        upper_range = np.ceil(mkt_dis.sum(axis=1).max() / 0.2) * 20
        data, layout = self.plotly_area(100 * mkt_dis.T, '持股市值分布走势', upper_range)
        save_pic2local(data, layout, newpath + r"\持股市值分布走势.png")
        ws.pictures.add(newpath+r"\持股市值分布走势.png", left=ws.range('P91').left, top=ws.range('P91').top,
                        width=700, height=350)

        ws.pictures.add(newpath+r"\虚拟净值VS实际净值.png", left=ws.range('A121').left, top=ws.range('A121').top,
                        width=700, height=350)

        ws = wb.sheets['风格画像']
        ws["A1"].options(pd.DataFrame, header=1, index=False, expand='table').value = self.data_param['style_pic']
        ws["A3"].options(pd.DataFrame, header=1, index=False, expand='table').value = self.data_param['size_pic']

        ws = wb.sheets['行业个股占比图']
        ws.clear()
        top5_industry=industry_allo_df.mean(axis=0).sort_values(ascending=False)[0:5].index.tolist()
        j=1
        for i in range(len(top5_industry)):
            industrys=top5_industry[i]
            top5_industry_tickers=portfolio_weight[portfolio_weight['一级行业']==industrys][['交易日期'
            ,'股票简称','占净值比例']].sort_values('交易日期')
            pivot_df = pd.pivot_table(
                top5_industry_tickers, index='交易日期', columns='股票简称', values='占净值比例').sort_index().fillna(0.)
            upper_range = np.ceil(pivot_df.sum(axis=1).max()*120)
            data, layout = self.plotly_area(100 * pivot_df.T, '{}个股配置'.format(industrys),
                                            upper_range)
            annotations = self.get_annotations(pivot_df)
            save_pic2local(data, layout, newpath + r"\{}个股配置.png".format(industrys),annotations=annotations)
            if(i%2==0):
                x_mark='A'
                if(i>1):
                    j = j + 30
            else:
                x_mark='P'
            ws.pictures.add(newpath+r"\{}个股配置.png".format(industrys), left=ws.range(x_mark+str(j)).left, top=ws.range(x_mark+str(j)).top,
                            width=700, height=350)

        ws = wb.sheets['前十大个股交易记录']
        ws.clear()
        j=1
        for i in range(len(top10_tickers)):
            ticker=top10_tickers[i]
            df_bar=portfolio_weight[portfolio_weight['股票代码'].str[0:6]==ticker].set_index('交易日期')
            df_line = price_df[(price_df['ZQDM'] == ticker)
                               &(price_df['JYRQ'] >= df_bar.index.min())][['JYRQ', 'SPJG']].set_index('JYRQ')
            sec_name=df_bar['股票简称'].unique()[0]
            df_bar=pd.merge(df_line,df_bar,
                            how='left',left_index=True,right_index=True).fillna(0)['持股数量'].to_frame('持股数量')
            # df_bar['index_count'] = df_bar.reset_index().index
            # for position in df_bar[df_bar['持股数量']!=0]['index_count']:
            #     df_bar.loc[(df_bar['index_count']<=position)&(df_bar['index_count']>=position-10),'持股数量']=\
            #         df_bar[df_bar['index_count']==position]['持股数量'].values[0]
            #figsize=(max(len(df_line)*2,700), max(len(df_line),350))
            data,layout=self.plotly_line_and_bar(df_line,df_bar['持股数量'].to_frame('持股数量'),
                                                 sec_name, figsize=(700, 350))
            save_pic2local(data, layout, newpath + r"\{}.png".format(sec_name.replace('*','')))

            # x_mark = 'A'
            if(i%2==0):
                x_mark='A'
                if(i>1):
                    j = j + 30
            else:
                x_mark='P'

            ws.pictures.add(newpath+r"\{}.png".format(sec_name.replace('*','')), left=ws.range(x_mark+str(j)).left, top=ws.range(x_mark+str(j)).top,
                            width=700, height=350)

        for i in range(len(sheet_list)):

            ws = wb.sheets[sheet_list[i]]
            ws.clear()

            ws["A1"].options(pd.DataFrame, header=1, index=False, expand='table').value = df_list[i]
            # print('{} done'.format(sheet_list[i]))

        ws = wb.sheets['行业画像']
        upper_range = np.ceil(industry_allo_df.sum(axis=1).max() / 0.2) * 20
        data, layout = self.plotly_area(100 * industry_allo_df.T, '行业配置走势', upper_range)
        annotations = self.get_annotations(industry_allo_df)
        save_pic2local(data, layout, newpath + r"\行业配置走势.png",annotations=annotations)
        ws.pictures.add(newpath+r"\行业配置走势.png", left=ws.range('A4').left, top=ws.range('A4').top,
                        width=700, height=350)

        industry_mimic_dict=self.data_param['industry_mimic_dict']
        row_num=1
        for col in industry_mimic_dict.keys():
            data, layout = self.plotly_line(industry_mimic_dict[col]
                                            ,'{}虚拟净值VS行业指数'.format(col))
            save_pic2local(data, layout, newpath + r"\{}虚拟净值VS行业指数.png".format(col))
            ws.pictures.add(newpath +  r"\{}虚拟净值VS行业指数.png".format(col), left=ws.range('A{}'.format(4+30*row_num)).left
                            , top=ws.range('A{}'.format(4+30*row_num)).top,
                            width=700, height=350)
            row_num+=1

        ws = wb.sheets['风格画像']
        if(len(self.data_param['value_exp'])>0):
            upper_range = np.ceil(self.data_param['value_exp'].pivot_table('zjbl','jsrq','style_type').fillna(0).sum(axis=1).max() / 0.2) * 20
            data, layout = self.plotly_area(100 * self.data_param['value_exp'].pivot_table('zjbl','jsrq','style_type').fillna(0).T,
                                            '风格暴露时序', upper_range)
            save_pic2local(data, layout, newpath + r"\风格暴露时序.png")
            ws.pictures.add(newpath+r"\风格暴露时序.png", left=ws.range('A6').left, top=ws.range('A6').top,
                            width=700, height=350)

        if(len(self.data_param['size_exp'])>0):
            upper_range = np.ceil(self.data_param['size_exp'].pivot_table('zjbl','jsrq','size_type').fillna(0).sum(axis=1).max() / 0.2) * 20
            data, layout = self.plotly_area(100 * self.data_param['size_exp'].pivot_table('zjbl','jsrq','size_type').fillna(0).T,
                                            '规模暴露时序', upper_range)
            save_pic2local(data, layout, newpath + r"\规模暴露时序.png")
            ws.pictures.add(newpath+r"\规模暴露时序.png", left=ws.range('P6').left, top=ws.range('P6').top,
                            width=700, height=350)

        ws = wb.sheets['前十大个股行业相关性']
        y_position=1
        for df in corr_his:
            length=len(df)
            ws["A{}".format(y_position)].options(pd.DataFrame, header=1, index=False, expand='table').value = df
            y_position+=length+2

        wb.save(template_folder)
        wb.close()
        app.quit()

        # except Exception as e :
        #     wb.close()
        #     app.quit()
        #     print("Error occure on {0} for {1}".format(self.fund_name,e))

class HoldingExtractor_DB:

    def __init__(self):

        self.total_asset_dmlist=['资产类合计:','资产合计']
        self.net_asset_dmlist=['基金资产净值:','资产净值','资产资产净值:']
        self.debt_dmlist=['负债类合计:']
        self.ashare_dmlist=['11020101','1102.01.01.','1101010101','1102.05.01','11021101','11021501']
        self.szshare_dmlist=['11023101','1102.33.01.','1101013101','1102.37.01','11023201','1102.31.01']
        self.cyb_dmlistt=['11024101','1101014101','1102.38.01','1102.34.01','1102.61.01']
        self.kcb_dmlist=['1102C101','1101C101','1102.88.01','1102.02.01','1102D201','1102.2A.01','1102.C1.01'
            ,'1102.C2.01']
        self.jjtz_dmlist = ['110104', '1105']
        self.hk_dmlist=['11028101','11028201','11028301','1102.81.01','1102.65.01','1102.66.01','1102.68.01']
        self.rqyw_list=['1202']
        self.qhzbj=['3102']
        self.qtlc=['1109','1108']

    @staticmethod
    def _shift_date(date):
        trade_dt = datetime.datetime.strptime(date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=30)).strftime('%Y%m%d')

        sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            pre_date, date)
        res = hbs.db_data_query('readonly', sql_script, page_size=5000)
        df = pd.DataFrame(res['data']).rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                     "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

        trading_day_list = df[df['isOpen'] == 1]['calendarDate'].tolist()

        return trading_day_list[-1]

    @staticmethod
    def to_month_date(date_list):

        date_frame=pd.DataFrame(data=date_list,columns=['date'])
        date_frame['date']=date_frame['date'].astype(str)
        date_frame = date_frame[date_frame['date'] >= '20141031']
        date_frame['yeatmonth']=[x[0:6] for x in date_frame['date']]
        date_frame=date_frame.drop_duplicates('yeatmonth', keep='last')['date'].to_list()

        return  date_frame

    def _load_portfolio_weight(self,jjdm,date_list,fund_name=None):

        #date_list=self.to_month_date(date_list)

        portfolio_weight_list = []
        error=''
        for date in date_list:

            try:

                data=valuation.get_prod_valuation_by_jjdm_gzrq(jjdm,date)
                data=data.drop_duplicates()
                if(data.empty):
                    print("data for {0} missed,continue...".format(date))
                    error+="data for {0} missed,continue...;".format(date)
                    continue
                date = self._shift_date(str(date))
                columns_map=dict(zip(['kmdm','sz','kmmc'],['科目代码','市值','科目名称']))

                data.rename(columns=columns_map,inplace=True)

                for dm in self.total_asset_dmlist:
                    if(len(data[data['科目代码'] == dm])>0):
                        total_asset = float(data[data['科目代码'] ==dm]['市值'].values[0])
                        # break

                net_asset=0
                for dm in self.net_asset_dmlist:
                    if(len(data[data['科目代码'] == dm])>0):
                        net_asset = float(data[data['科目代码'] == dm]['市值'].values[0])
                        break

                if(net_asset==0):
                    for dm in self.debt_dmlist:
                        if (len(data[data['科目代码'] == dm]) > 0):
                            debt = float(data[data['科目代码'] == dm]['市值'].values[0])
                            net_asset=total_asset-debt
                            break

                leverage = total_asset / net_asset
                # A股
                sh=pd.DataFrame()
                for dm in self.ashare_dmlist:
                    if(len(data[data['科目代码'].str.startswith(dm)])>0):
                        sh =pd.concat([sh,data[data['科目代码'].str.startswith(dm)]],axis=0)
                        # break
                sz=pd.DataFrame()
                for dm in self.szshare_dmlist:
                    if(len(data[data['科目代码'].str.startswith(dm)])>0):
                        sz = pd.concat([sz,data[data['科目代码'].str.startswith(dm)]],axis=0)
                        # break
                cyb = pd.DataFrame()
                for dm in self.cyb_dmlistt:
                    if (len(data[data['科目代码'].str.startswith(dm)]) > 0):
                        cyb = data[data['科目代码'].str.startswith(dm)]
                        # break
                kcb = pd.DataFrame()
                for dm in self.kcb_dmlist:
                    if (len(data[data['科目代码'].str.startswith(dm)]) > 0):
                        kcb = data[data['科目代码'].str.startswith(dm)]
                        # break

                if(len(sh)==0 and len(sz)==0 and len(cyb)==0 and len(kcb)==0):
                    print('No stock exist for {0} at {1}..'.format(jjdm,date))
                    error+='No stock exist for {0} at {1}..;'.format(jjdm,date)
                    continue

                equity_a = pd.concat([sh, sz, cyb, kcb], axis=0)

                equity_a['len'] = equity_a['科目代码'].apply(lambda x: len(x))
                equity_a = equity_a[equity_a['len'] > 10]
                if(len(equity_a)==0):
                    print('No stock details found in the data, date {} is skipped'.format(date))
                    error+='No stock details found in the data, date {} is skipped;'.format(date)
                    continue

                if("." not in equity_a['科目代码'].values[0]):
                    equity_a['ticker'] = equity_a['科目代码'].apply(lambda x: x[-6:])
                else:
                    equity_a['ticker'] = equity_a['科目代码'].apply(lambda x: x[-8:-2])

                equity_a['weight'] = equity_a['市值'].astype(float) / net_asset
                equity_a = equity_a.rename(columns={"科目名称": "sec_name","gzzz":"value_increased"})[['ticker', 'sec_name', 'weight','dwcb','sl','value_increased']]

                #deal with stocks brought from different acount
                equity_a=pd.merge(equity_a,equity_a.groupby('ticker').sum()['weight'].to_frame('tw')
                                  ,how='left',on='ticker')
                equity_a['dwcb']=equity_a['dwcb'].astype(float)*\
                                 equity_a['weight'].astype(float)/equity_a['tw'].astype(float)
                equity_a=equity_a.groupby(['ticker','sec_name']).sum().reset_index().drop('tw',axis=1)

                # 港股
                equity_hk = pd.DataFrame()
                for dm in self.hk_dmlist:
                    if(len(data[data['科目代码'].str.startswith(dm)])>0):
                        equity_hk =pd.concat([equity_hk,data[data['科目代码'].str.startswith(dm)]]
                                             ,axis=0).fillna('')
                        # break

                if(len(equity_hk)>0):
                    equity_hk['len'] = equity_hk['科目代码'].apply(lambda x: len(x))
                    equity_hk = equity_hk[equity_hk['len'] > 10]
                    equity_hk['ticker'] = equity_hk['科目代码'].apply(lambda x: x[-6:])
                    equity_hk['科目名称'] = equity_hk['科目名称'].apply(lambda x: x.strip())  # add
                    equity_hk['weight'] = equity_hk['市值'].astype(float) / net_asset
                    equity_hk = equity_hk.rename(columns={"科目名称": "sec_name","gzzz":"value_increased"})[['ticker', 'sec_name', 'weight','dwcb','sl','value_increased']]

                    #deal with stocks brought from different acount
                    for col in ['dwcb','weight']:
                        equity_hk.loc[equity_hk[col]=='',col]=0
                    equity_hk=pd.merge(equity_hk,equity_hk.groupby('ticker').sum()['weight'].to_frame('tw')
                                      ,how='left',on='ticker').fillna(0)
                    equity_hk['dwcb']=equity_hk['dwcb'].astype(float)*\
                                     equity_hk['weight'].astype(float)/equity_hk['tw'].astype(float)
                    equity_hk=equity_hk.groupby(['ticker','sec_name']).sum().reset_index().drop('tw',axis=1)
                # 债券
                tmp = data[data['科目代码'] == '1103']
                if tmp.empty:
                    bond_df = pd.DataFrame()
                else:
                    bond_ratio = tmp['市值'].astype(float).values[0] / net_asset
                    bond_df = pd.DataFrame(columns=['ticker', 'sec_name', 'weight'])
                    bond_df.loc[0] = ['b00001', '债券投资', bond_ratio]
                # 基金
                tmp=pd.DataFrame()
                for dm in self.jjtz_dmlist:
                    if (len(data[data['科目代码']==dm]) > 0):
                        tmp = data[data['科目代码'] == dm]
                        break
                if tmp.empty:
                    fund_df = pd.DataFrame()
                else:
                    fund_ratio = tmp['市值'].astype(float).values[0] / net_asset
                    fund_df = pd.DataFrame(columns=['ticker', 'sec_name', 'weight'])
                    fund_df.loc[0] = ['f00001', '基金投资', fund_ratio]
                #融券
                tmp=pd.DataFrame()
                for dm in self.rqyw_list:
                    if (len(data[data['科目代码']==dm]) > 0):
                        tmp = data[data['科目代码'] == dm]
                        break
                if tmp.empty:
                    rzrq_df = pd.DataFrame()
                else:
                    fund_ratio = tmp['市值'].astype(float).values[0] / net_asset
                    rzrq_df = pd.DataFrame(columns=['ticker', 'sec_name', 'weight'])
                    rzrq_df.loc[0] = ['r00001', '买入返售金融资产(融券)', fund_ratio]
                #股指期货
                tmp=pd.DataFrame()
                for dm in self.qhzbj:
                    if (len(data[(data['科目代码'].astype(str).str.contains(dm))
                                 &(data['科目名称'].astype(str).str.contains('IF')) ]) > 0):
                        # print('期货 Bingo at {}!'.format( date))
                        tmp = data[(data['科目代码'].astype(str).str.contains(dm))
                                 &(data['科目名称'].astype(str).str.contains('IF'))&(data['sl'].notnull()) ]
                        break
                if tmp.empty:
                    qhzbj_df = pd.DataFrame()
                else:
                    # tmp['科目代码']=tmp[]
                    tmp['weight']=tmp['市值'].astype(float).values / net_asset
                    qhzbj_df =tmp[['科目代码','科目名称','weight','dwcb','sl','gzzz']].rename(columns={'科目代码':'ticker',
                                                                            '科目名称':'sec_name','gzzz':'value_increased'})
                    #print('股指 Bingo! at {}'.format(date))

                #理财
                tmp=pd.DataFrame()
                for dm in self.qtlc:
                    if (len(data[data['科目代码']==dm]) > 0):
                        tmp = data[data['科目代码'] == dm]
                        break
                if tmp.empty:
                    lc_df = pd.DataFrame()
                else:
                    fund_ratio = tmp['市值'].astype(float).values[0] / net_asset
                    lc_df = pd.DataFrame(columns=['ticker', 'sec_name', 'weight'])
                    lc_df.loc[0] = ['l00001', '理财投资', fund_ratio]
                    # print('理财 Bingo at{}'.format(date))

                df = pd.concat([equity_a, equity_hk, bond_df, fund_df,rzrq_df,qhzbj_df,lc_df], axis=0)
                # 其他类
                cash_df = pd.DataFrame(columns=['ticker', 'sec_name', 'weight'])
                cash_df.loc[0] = ['c00001', '其他', leverage - df['weight'].abs().sum()]
                df = pd.concat([df, cash_df], axis=0)


                #净资产，总资产
                zc_df= pd.DataFrame(columns=['ticker', 'sec_name', 'weight'])
                zc_df.loc[0]=['zc0001', '净资产', net_asset]
                zc_df.loc[1] = ['zc0002', '总资产', total_asset]
                df = pd.concat([df, zc_df], axis=0)

                df['trade_date'] = date
                if(len(df[df['ticker'].str[0].isin(['0', '3', '6'])])>0):
                    portfolio_weight_list.append(df)

            except Exception as e:
                print(str(e)+"for jjdm:{0} at date :{1}".format(jjdm,date))
                error+=str(e)+"for jjdm:{0} at date :{1}".format(jjdm,date)
                continue

        if(len(portfolio_weight_list)>0):
            portfolio_weight_df = pd.concat(portfolio_weight_list)
        else:
            portfolio_weight_df = pd.concat([pd.DataFrame(columns=['ticker', 'sec_name','weight','trade_date'],
                                                          data=[['','',99999,date]])])

        portfolio_weight_df['jjdm'] = jjdm
        portfolio_weight_df['error_list']=error

        return  portfolio_weight_df

def get_new_joiner():

    sql="SELECT max(trade_date) as maxdate from st_hedge.r_st_sm_subjective_fund_holding"
    max_date=hbdb.db2df(sql,db='highuser')

    test=hbdb.db2df("SELECT jjdm,ticker,weight,trade_date from st_hedge.r_st_sm_subjective_fund_holding where trade_date>='20220101' and trade_date<='{}'"
                    .format(max_date)
                    ,db='highuser')

    outputdf=[]
    for jjdm in test['jjdm'].unique().tolist():
        print(jjdm)
        temp=test[test['jjdm']==jjdm].reset_index(drop=True)
        for i in range(len(temp)):
            temp.loc[i, 'flag'] = int(temp.loc[i]['ticker'] in temp.loc[:np.max([0,i-1])]['ticker'].tolist())
        outputdf.append(temp)

    outputdf=pd.concat(outputdf,axis=0)
    outputdf.to_excel('new_joiner.xlsx',index=False)

if __name__ == '__main__':

    from hbshare.fe.XZ import  db_engine
    localdb=db_engine.PrvFunDB().engine
    name = '新方程泰暘臻选1期'
    # name = '新方程望正精英鹏辉'
    # name = '新方程域秀智享5号'
    # name = '亘曦2号'
    # name = '富乐一号'
    #name = '仁布积极进取1号'

    name='新方程巨杉,无股票'
    name= '同犇消费5号，20200630 资产合计项是空的'
    name='睿洪二号'
    name='丰岭稳健成长1期'
    name='望正精英-鹏辉1号'
    name='丹羿精选3号，无股票'
    name='亘曦2号,没有估值表'


    #get the fre for jj with valuation table
    # sql_script = "SELECT jjdm,trade_date,ticker,weight from st_hedge.r_st_sm_subjective_fund_holding where weight!=99999"
    # data = hbdb.db2df(sql_script,db='highuser')
    # data=data.drop_duplicates(['jjdm','trade_date'],keep='first').sort_values(['jjdm','trade_date']).reset_index(drop=True)
    # data['time_diff']=data[['jjdm', 'trade_date']].groupby('jjdm').diff()
    # time_diff=data[['jjdm','time_diff']].groupby('jjdm').median()
    # last_trade_date=data[['jjdm','trade_date']].groupby('jjdm').max()
    # last_trade_date['distrance2today'] = last_trade_date['trade_date'].max()-last_trade_date['trade_date']
    # check_df=pd.merge(time_diff,last_trade_date,how='outer',on='jjdm')
    # check_df['if_updated'] = 'True'
    # check_df.loc[check_df['distrance2today'] / check_df['time_diff'] > 1.5, 'if_updated'] = 'False'
    # check_df.loc[ check_df['time_diff'].isnull(), 'if_updated'] = 'False'
    #
    # check_df.loc[(check_df['time_diff']>0)&(check_df['time_diff']<=14),'fre']='fund_stats'
    # check_df.loc[(check_df['time_diff'] > 20) & (check_df['time_diff'] <= 120), 'fre'] = 'monthly'
    # check_df.loc[(check_df['time_diff'] > 120) & (check_df['time_diff'] <= 400), 'fre'] = 'quarter'
    # check_df.loc[(check_df['time_diff'] > 800) & (check_df['time_diff'] <= 10000), 'fre'] = 'yearly'
    #
    # yjy=pd.read_excel(r"E:\GitFolder\docs\私募股多持仓分析\研究员对应表.xlsx")


    # #
    # sql_script = "SELECT distinct (jjdm) from st_hedge.r_st_sm_subjective_fund_holding where weight!=99999"
    # jjdm_list = hbdb.db2df(sql_script,db='highuser')['jjdm'].tolist()
    # jjdm_list=['S63505']
    # for select_jjdm in jjdm_list:
    #
    #     sql_script = "SELECT distinct trade_date from st_hedge.r_st_sm_subjective_fund_holding where jjdm = '{}' and weight!='99999'".format(select_jjdm)
    #     data = hbdb.db2df(sql_script,db='highuser')
    #     # data['ym']=data['trade_date'].astype(str).str[0:6]
    #
    #     # data.loc[data['trade_date'].astype(str).str[4:6].isin(['01','03','05','07','08','10','12'])
    #     # ,'trade_date']=data.loc[data['trade_date'].astype(str).str[4:6].isin(['01','03','05','07','08','10','12'])]['ym']+'31'
    #     #
    #     # data.loc[data['trade_date'].astype(str).str[4:6].isin([ '04', '06', '09', '11'])
    #     # , 'trade_date'] = \
    #     # data.loc[data['trade_date'].astype(str).str[4:6].isin(['04', '06', '09', '11'])]['ym'] + '30'
    #     #
    #     # data.loc[data['trade_date'].astype(str).str[4:6].isin(['02'])
    #     # , 'trade_date'] = \
    #     # data.loc[data['trade_date'].astype(str).str[4:6].isin(['02'])]['ym'] + '28'
    #
    #     data['trade_date']=data['trade_date'].astype(str)
    #     date_list = sorted(data['trade_date'].unique())
    #     print(select_jjdm)
    #
    #     sql = "select TRADINGDATE from hsjy_gg.QT_TradingDayNew where TradingDate>= to_date('20200409','yyyymmdd') and TradingDate<= to_date('20221028','yyyymmdd') and IFTRADINGDAY=1 "
    #     date_list=hbdb.db2df(sql, db='readonly')
    #     date_list['TRADINGDATE'] = date_list['TRADINGDATE'].astype(str).str[0:10].str.replace('-', '')
    #     date_list=date_list['TRADINGDATE'] .tolist()
    #     date_list=list(set(date_list))
    #     date_list.sort()
    #
    #     data=HoldingExtractor_DB()._load_portfolio_weight(jjdm=select_jjdm,date_list=date_list)
    #     sql="delete from prv_fund_holding where jjdm='{}'".format(select_jjdm)
    #     data.to_sql('prv_fund_holding',con=localdb,if_exists='append',index=False)


    #
    sql_script = "SELECT distinct (jjdm) as jjdm from st_hedge.r_st_sm_subjective_fund_holding where weight!=99999  "
    jjdm_list = hbdb.db2df(sql_script,db='highuser')['jjdm'].tolist()
    # sql_script = "SELECT distinct (jjdm) as jjdm from prv_fund_holding where weight!=99999"
    # jjdm_list =pd.read_sql(sql_script,con=localdb)['jjdm'].tolist()
    #jjdm_list=['S20950','S66391','S85909','SEX801','SX4289','SLA342']
    # jjdm_list=['SLT664']
    from_local_db=False

    for jjdm in jjdm_list[0:8]:
        print("{} start".format(jjdm))
        if(from_local_db):
            sql="select max(trade_date) as end_date,min(trade_date) as start_date from prv_fund_holding where jjdm='{0}' "\
                .format(jjdm)
            date_df =pd.read_sql(sql,con=localdb)
        else:
            sql="select max(trade_date) as end_date,min(trade_date) as start_date  from st_hedge.r_st_sm_subjective_fund_holding where jjdm='{0}' "\
                .format(jjdm)
            date_df=hbdb.db2df(sql,db='highuser')

        start_date=date_df['start_date'][0]
        end_date=date_df['end_date'][0]
        sql = "select b.jgjc,a.jjjc from st_hedge.t_st_jjxx a left join broadcast.t_st_gg_jgxx b on a.glrm=b.jgdm where a.jjdm='{0}'".format(
            jjdm)
        prv_info = hbdb.db2df(sql, db='highuser')
        HoldingAnalysor(jjdm, start_date=start_date
                        , end_date=end_date,from_local_db=from_local_db).save_construct_result2loacl(gsjc=prv_info['jgjc'][0],
                                                                                                    jjjc=prv_info['jjjc'][0])
        print('{} Done!'.format(jjdm))
