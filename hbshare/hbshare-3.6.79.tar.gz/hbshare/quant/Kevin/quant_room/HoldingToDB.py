"""
私募基金估值表持仓入库
"""
import os
import pandas as pd
from hbshare.quant.Kevin.asset_allocation.macro_index.util import create_table, delete_duplicate_records, WriteToDB


class HoldingExtractor:
    def __init__(self, data_path, table_name, fund_name, is_increment=1):
        self.data_path = data_path
        self.table_name = table_name
        self.fund_name = fund_name
        self.is_increment = is_increment

    def _load_portfolio_weight(self):
        filenames = os.listdir(self.data_path)
        filenames = [x for x in filenames if x.split('.')[-1] in ['xls', 'xlsx']]

        portfolio_weight_list = []
        for name in filenames:
            date = name.split('_')[-2]
            # 国君 & 海通
            if self.fund_name in ['因诺聚配中证500指数增强', '凡二中证500增强9号1期', '赫富500指数增强一号', '赫富1000指数增强一号',
                                  '宽德金选中证500指数增强6号', 'TEST', '量锐62号', '启林广进中证1000指数增强',
                                  '白鹭精选量化鲲鹏十号', '伯兄建康', '伯兄熙宁', '世纪前沿指数增强2号',
                                  '云起量化指数增强1号', '罗维盈安凌云增强2号', '朋锦永宁', '宽德中证1000指数增强8号',
                                  '稳博金选中证500指数增强6号', '稳博广博中证1000']:
                context = "市值占净值%"
                if self.fund_name in ['伯兄建康', '伯兄熙宁']:
                    hd = 2
                    context = "市值占净值(%)"
                elif self.fund_name in ['世纪前沿指数增强2号']:
                    hd = 2 if date >= '20210630' else 0
                    context = "市值占净值(%)"
                else:
                    hd = 3
                data = pd.read_excel(
                    os.path.join(self.data_path, name), sheet_name=0, header=hd).dropna(subset=['科目代码'])
                sh = data[data['科目代码'].str.startswith('11020101')]
                sz = data[data['科目代码'].str.startswith('11023101')]
                cyb = data[data['科目代码'].str.startswith('11024101')]
                kcb = data[data['科目代码'].str.startswith('1102C101')]
                df = pd.concat([sh, sz, cyb, kcb], axis=0).dropna()
                df['ticker'] = df['科目代码'].apply(lambda x: x[-6:])
                df.rename(columns={"科目名称": "sec_name", context: "weight"}, inplace=True)
                if self.fund_name in ['凡二中证500增强9号1期', '量锐62号', '罗维盈安凌云增强2号'] and \
                        type(df['weight'].tolist()[0]) == str:
                    df['weight'] = df['weight'].str.strip('%').astype(float)
            # 招商
            elif self.fund_name in ['星阔广厦1号中证500指数增强', '星阔上林1号', '星阔山海6号',
                                    '量客卓宇六号', '乾象中证500指数增强1号', '水木博雅500指增',
                                    '概率1000指增1号', '概率500指增2号', '稳博中性稳稳系列1号', '稳博中性稳稳系列2号',
                                    '稳博1000指数增强1号', '蒙玺量化对冲钧衡3号', '天戈500指增', '宽德九臻',
                                    '顽岩中证500指数增强1号', '托特中证500指数增强2号', '卓识500指数增强一号', '卓识辰熙',
                                    '世纪前沿指数增强24号', '世纪前沿量化优选一号', '本利达利磐八号', '锋滔指数增强2号',
                                    '知行通达500指增', '伯兄永隆', '华钧真观1期']:
                header = 6 if self.fund_name in ['星阔上林1号', '水木博雅500指增', '乾象中证500指数增强1号',
                                                 '稳博中性稳稳系列1号', '稳博中性稳稳系列2号',
                                                 '本利达利磐八号', '锋滔指数增强2号', '知行通达500指增', '华钧真观1期'] else 7
                data = pd.read_excel(
                    os.path.join(self.data_path, name), sheet_name=0, header=header).dropna(subset=['科目代码'])
                sh = data[data['科目代码'].str.endswith('SH')]
                sz = data[data['科目代码'].str.endswith('SZ')]
                df = pd.concat([sh, sz], axis=0)
                # add
                df = df[df['科目代码'].str.startswith('1')]
                df['ticker'] = df['科目代码'].apply(lambda x: x.split(' ')[0][-6:])
                df.rename(columns={"科目名称": "sec_name", "市值占比": "weight"}, inplace=True)
                if self.fund_name in ["乾象中证500指数增强1号", "天戈500指增"]:
                    # 处理一下分红
                    ratio = data[data['科目代码'] == '资产净值']['市值占比'].values[0] / \
                            data[data['科目代码'] == '资产合计']['市值占比'].values[0]
                    df['weight'] *= ratio
                if self.fund_name == '蒙玺量化对冲钧衡3号':
                    df['weight'] = df['weight'] / df['weight'].sum()
                df['weight'] *= 100.
            # 海通但有信用账户
            elif self.fund_name in ['朋锦金石炽阳']:
                data = pd.read_excel(
                    os.path.join(self.data_path, name), sheet_name=0, header=3).dropna(subset=['科目代码'])
                sh1 = data[data['科目代码'].str.startswith('11020101')]
                sh2 = data[data['科目代码'].str.startswith('11021101')]
                sz1 = data[data['科目代码'].str.startswith('11023101')]
                sz2 = data[data['科目代码'].str.startswith('11023201')]
                cyb1 = data[data['科目代码'].str.startswith('11024101')]
                cyb2 = data[data['科目代码'].str.startswith('11021501')]
                kcb1 = data[data['科目代码'].str.startswith('1102C101')]
                kcb2 = data[data['科目代码'].str.startswith('1102D201')]
                df = pd.concat([sh1, sh2, sz1, sz2, cyb1, cyb2, kcb1, kcb2], axis=0).dropna()
                df['ticker'] = df['科目代码'].apply(lambda x: x[-6:])
                df.rename(columns={"科目名称": "sec_name", "市值占净值%": "weight"}, inplace=True)
                df['weight'] = 100. * df['weight'] / df['weight'].sum()
            # 国君但有信用账户
            elif self.fund_name in ['思勰中证500指数增强1号']:
                data = pd.read_excel(
                    os.path.join(self.data_path, name), sheet_name=0, header=3).dropna(subset=['科目代码'])
                del data['估值增值']
                sh1 = data[data['科目代码'].str.startswith('11020101')]
                sh2 = data[data['科目代码'].str.startswith('11021101')]
                sz1 = data[data['科目代码'].str.startswith('11023101')]
                sz2 = data[data['科目代码'].str.startswith('11021201')]
                cyb1 = data[data['科目代码'].str.startswith('11024101')]
                cyb2 = data[data['科目代码'].str.startswith('11021501')]
                kcb1 = data[data['科目代码'].str.startswith('1102C101')]
                kcb2 = data[data['科目代码'].str.startswith('1102D201')]
                df = pd.concat([sh1, sh2, sz1, sz2, cyb1, cyb2, kcb1, kcb2], axis=0).dropna()
                df['ticker'] = df['科目代码'].apply(lambda x: x[-6:])
                df.rename(columns={"科目名称": "sec_name", "市值占净值%": "weight"}, inplace=True)
            else:
                date = None
                df = pd.DataFrame()

            df['trade_date'] = date
            portfolio_weight_list.append(df[['trade_date', 'ticker', 'sec_name', 'weight']])

        portfolio_weight_df = pd.concat(portfolio_weight_list)
        portfolio_weight_df = portfolio_weight_df.groupby(
            ['trade_date', 'ticker', 'sec_name'])['weight'].sum().reset_index()
        portfolio_weight_df['fund_name'] = self.fund_name
        portfolio_weight_df = portfolio_weight_df[portfolio_weight_df['ticker'].str[0].isin(('3', '0', '6'))]  # 剔除货基

        print(portfolio_weight_df.groupby('trade_date')['weight'].sum().sort_index())

        return portfolio_weight_df

    def writeToDB(self):
        if self.is_increment == 1:
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
                fund_name varchar(20))
            """.format(self.table_name)
            create_table(self.table_name, sql_script)
            data = self._load_portfolio_weight()
            WriteToDB().write_to_db(data, self.table_name)


if __name__ == '__main__':
    HoldingExtractor(data_path='D:\\估值表基地\\概率500指增2号', table_name="private_fund_holding",
                     fund_name="概率500指增2号").writeToDB()
