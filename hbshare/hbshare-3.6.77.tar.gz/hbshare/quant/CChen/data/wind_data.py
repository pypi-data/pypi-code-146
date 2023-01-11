import pandas as pd
from WindPy import w
import re
from hbshare.quant.CChen.func import generate_table
from datetime import timedelta, datetime
from time import sleep
from hbshare.quant.CChen.data.wind_cons import sql_l_futures, sql_l_bar, sql_l_stk, sql_l_edb


class WindApi(object):

    def __init__(self):
        self.api = w
        self.api.start()

    def get_com_fut_contracts(self, date):
        com = self.api.wset("sectorconstituent", "date=" + date.strftime('%Y-%m-%d') + ";sectorid=1000015512000000")
        com_df = pd.DataFrame(com.Data).T.rename(columns={0: 't_date', 1: 'wind_code', 2: 'sec_name'})
        com_df['t_date'] = pd.to_datetime(com_df['t_date']).dt.date
        return com_df

    def get_fin_fut_contracts(self, date):
        fin = self.api.wset("sectorconstituent", "date=" + date.strftime('%Y-%m-%d') + ";sectorid=a599010101000000")
        fin_df = pd.DataFrame(fin.Data).T.rename(columns={0: 't_date', 1: 'wind_code', 2: 'sec_name'})
        fin_df['t_date'] = pd.to_datetime(fin_df['t_date']).dt.date
        return fin_df

    def get_fut_data(self, date, com=True, fin=True):
        if com:
            com_contracts = self.get_com_fut_contracts(date=date)
        else:
            com_contracts = pd.DataFrame()

        if fin:
            fin_contracts = self.get_fin_fut_contracts(date=date)
        else:
            fin_contracts = pd.DataFrame()

        contracts = pd.concat([com_contracts, fin_contracts])

        contracts_str = str(contracts['wind_code'].tolist())
        contracts_str = contracts_str.replace('[', '').replace(']', '').replace('\'', '')

        properties = 'dlmonth, pre_close, pre_settle, open, high, low, close, settle, volume, amt, oi, oi_chg'

        data = self.api.wss(
            contracts_str,
            properties,
            'tradeDate=' + date.strftime('%Y%m%d')
        )

        data_df = pd.DataFrame(data.Data, index=data.Fields, columns=data.Codes).T
        data_df['t_date'] = date

        return data_df

    def to_sql_stk_index_fut(self, db_path, table, sql_info, end_date, database):
        generate_table(
            database=database,
            table=table,
            generate_sql=sql_l_futures,
            sql_ip=sql_info['ip'],
            sql_user=sql_info['user'],
            sql_pass=sql_info['pass'],
            table_comment='Wind期货连续合约行情'
        )
        print(table + ' generated')

        futures_list = pd.read_csv('wind_fut_list.csv')

        properties = "open, high, low, close, volume, amt, trade_hiscode, settle, oi, oiamount"

        for i in range(len(futures_list)):
            name = futures_list['name'][i]
            symbol = futures_list['code'][i]
            underlying = futures_list['underlying'][i]
            # product = nh_index_list['product'][i]

            print('Wind ' + name)

            data_exists = pd.read_sql_query(
                'select * from ' + table + ' where symbol="' + symbol.lower() + '" order by t_date', db_path
            )

            if len(data_exists) > 0:
                data_end_date = data_exists['t_date'].tolist()[-1]
                data_end_close = data_exists['close'].tolist()[-1]
                print(
                    '\tExisting ' + data_exists['t_date'].tolist()[0].strftime('%Y/%m/%d')
                    + ' - ' + data_exists['t_date'].tolist()[-1].strftime('%Y/%m/%d')
                )
                if data_end_date >= end_date.date():
                    print('\tData exists')
                    continue
                else:
                    start_date = (data_exists['t_date'].tolist()[-1] + timedelta(days=1))
            else:
                print('\tExisting None')
                start_date = datetime(1990, 1, 1)
                data_end_close = None

            print('\t' + str(i + 1) + '/' + str(len(futures_list)))
            data_raw = self.api.wsd(
                symbol,
                properties,
                start_date,
                end_date
            )
            underlying_raw = self.api.wsd(
                underlying,
                'close',
                start_date,
                end_date
            )
            if len(data_raw.Data[0]) == 0:
                print('\tNo new data')
                continue

            if data_raw.ErrorCode != 0:
                print(data_raw.ErrorCode)
                print('Wind Error')
                break

            data_new = pd.DataFrame(
                {
                    't_date': data_raw.Times,
                    'open': data_raw.Data[0],
                    'high': data_raw.Data[1],
                    'low': data_raw.Data[2],
                    'close': data_raw.Data[3],
                    'volume': data_raw.Data[4],
                    'amount': data_raw.Data[5],
                    'code': data_raw.Data[6],
                    'settle': data_raw.Data[7],
                    'oi': data_raw.Data[8],
                    'oi_amount': data_raw.Data[9]
                }
            )

            data_new = data_new[data_new['close'] > 0].reset_index(drop=True)
            data_new['symbol'] = symbol
            data_new['product'] = re.findall(r'^[a-zA-Z]+', symbol)[0]
            data_new['pre_close'] = data_new['close'].shift(1)
            data_new.loc[0, 'pre_close'] = data_end_close

            underlying_data = pd.DataFrame(
                {
                    't_date': underlying_raw.Times,
                    'underlying': underlying_raw.Data[0]
                }
            )

            data_new = data_new.merge(underlying_data, on=['t_date'])
            data_new['basis'] = data_new['underlying'] - data_new['close']

            contracts = data_new[['code']].drop_duplicates().reset_index(drop=True)
            contracts_info = w.wss(
                str(tuple(contracts['code'])).replace('(', '').replace(',)', '').replace('\'',''),
                'lasttrade_date'
            )
            contracts_info = pd.DataFrame(
                {
                    'code': contracts_info.Codes,
                    'delist_date': contracts_info.Data[0]
                }
            )
            data_new = data_new.merge(contracts_info, on=['code'])

            print('\tLoading ' + data_new['t_date'].tolist()[0].strftime('%Y/%m/%d')
                  + ' - ' + data_new['t_date'].tolist()[-1].strftime('%Y/%m/%d'))
            data_new.to_sql(table, db_path, if_exists='append', index=False)
            print('\tto sql')
            sleep(1)

    def to_sql_fut_index(self, db_path, table, sql_info, end_date, database, code_df, freq=''):
        generate_table(
            database=database,
            table=table,
            generate_sql=sql_l_bar,
            sql_ip=sql_info['ip'],
            sql_user=sql_info['user'],
            sql_pass=sql_info['pass'],
            table_comment='期货指数行情'
        )
        print(table + ' generated')

        properties = "open, high, low, close, volume, amt, oi, oiamount"
        for i in range(len(code_df)):
            # name = code_df['name'][i]
            # exchange = code_df['exchange'][i]
            code = code_df['code'][i]
            product = code_df['product'][i]

            print('Wind ' + code + ' ' + str(product))

            data_exists = pd.read_sql_query(
                'select * from ' + table + ' where code="' + code.lower() + '" order by t_date',
                db_path
            )

            if len(data_exists) > 0:
                data_end_date = data_exists['t_date'].tolist()[-1]
                data_end_close = data_exists['close'].tolist()[-1]
                print(
                    '\tExisting ' + data_exists['t_date'].tolist()[0].strftime('%Y/%m/%d')
                    + ' - ' + data_exists['t_date'].tolist()[-1].strftime('%Y/%m/%d')
                )
                if data_end_date >= end_date.date():
                    print('\tData exists')
                    continue
                else:
                    start_date = (data_exists['t_date'].tolist()[-1] + timedelta(days=1))
            else:
                print('\tExisting None')
                start_date = datetime(1990, 1, 1)
                data_end_close = None

            print('\t' + str(i + 1) + '/' + str(len(code_df)))

            if freq.lower() in ['w', 'week', 'fund_stats']:
                data_raw = self.api.wsd(
                    code,
                    properties,
                    start_date,
                    end_date,
                    options="Period=W"
                )
            elif freq.lower() in ['month', 'monthly']:
                data_raw = self.api.wsd(
                    code,
                    properties,
                    start_date,
                    end_date,
                    options="Period=M"
                )
            else:
                data_raw = self.api.wsd(
                    code,
                    properties,
                    start_date,
                    end_date
                )
            if len(data_raw.Data[0]) == 0:
                print('\tNo new data')
                continue

            if data_raw.ErrorCode != 0:
                print(data_raw.ErrorCode)
                print('Wind Error')
                break

            data_new = pd.DataFrame(
                {
                    't_date': data_raw.Times,
                    'open': data_raw.Data[0],
                    'high': data_raw.Data[1],
                    'low': data_raw.Data[2],
                    'close': data_raw.Data[3],
                    'volume': data_raw.Data[4],
                    'amount': data_raw.Data[5],
                    'oi': data_raw.Data[6],
                    'oi_amount': data_raw.Data[7],
                }
            )
            data_new = data_new[data_new['close'] > 0].reset_index(drop=True)
            data_new['code'] = code
            data_new['product'] = product
            # data_new['name'] = name
            # data_new['exchange'] = exchange
            data_new['pre_close'] = data_new['close'].shift(1)
            data_new.loc[0, 'pre_close'] = data_end_close

            data_new['chg'] = data_new['close'] - data_new['pre_close']
            data_new['pct_chg'] = data_new['chg'] / data_new['pre_close']

            # print(data_new)

            # data_new['t_date'] = pd.to_datetime(data_new['t_date']).dt.date
            print('\tLoading ' + data_new['t_date'].tolist()[0].strftime('%Y/%m/%d')
                  + ' - ' + data_new['t_date'].tolist()[-1].strftime('%Y/%m/%d'))
            data_new.to_sql(table, db_path, if_exists='append', index=False)
            print('\tto sql')
            sleep(1)

    def to_sql_a_shares(self, start_date, end_date, db_path, table, sql_info, database):
        used_amount_all = 0

        generate_table(
            database=database,
            table=table,
            generate_sql=sql_l_stk,
            sql_ip=sql_info['ip'],
            sql_user=sql_info['user'],
            sql_pass=sql_info['pass'],
            table_comment='A股日行情'
        )
        print(table + ' generated')

        fields = 'open,high,low,close,volume,amt,adjfactor,free_turn_n,trade_status,riskwarning,share_totaltradable'

        date_list = self.api.wsd('000001.SH', 'close', start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')).Times

        for s in date_list:
            print(s)

            data = self.api.wset("sectorconstituent", "date=" + s.strftime('%Y-%m-%d') + ";sectorid=a001010100000000")

            stocks_pool = data.Data[1]
            stocks_name = data.Data[2]

            name_df = pd.DataFrame(
                {
                    'code': stocks_pool,
                    'name': stocks_name
                }
            )

            data_local = pd.read_sql_query(
                'select * from ' + table + ' where t_date=' + s.strftime('%Y%m%d'), db_path
            )

            data_diff_local = list(set(stocks_pool).difference(set(data_local['code'])))

            stock_data_raw = self.api.wss(
                codes=str(data_diff_local).replace('[', '').replace(']', '').replace('\'', ''),
                fields=fields,
                options='tradeDate=' + s.strftime('%Y%m%d')
            )

            if stock_data_raw.ErrorCode != 0:
                print(stock_data_raw.ErrorCode)
                print('Wind Error')
                quit()

            used_amount = len(stock_data_raw.Data) * len(stock_data_raw.Codes)
            used_amount_all += used_amount
            stock_data = pd.DataFrame(
                {
                    't_date': s,
                    'code': stock_data_raw.Codes,
                    'open': stock_data_raw.Data[0],
                    'high': stock_data_raw.Data[1],
                    'low': stock_data_raw.Data[2],
                    'close': stock_data_raw.Data[3],
                    'volume': stock_data_raw.Data[4],
                    'amount': stock_data_raw.Data[5],
                    'adjFactor': stock_data_raw.Data[6],
                    'freeTurn': stock_data_raw.Data[7],
                    'tdState': stock_data_raw.Data[8],
                    'stState': stock_data_raw.Data[9],
                    'freeShare': stock_data_raw.Data[10]
                }, index=range(len(stock_data_raw.Codes))
            ).merge(name_df, on='code', how='left')

            stock_data.to_sql(table, db_path, if_exists='append', index=False)
            print(
                # s.strftime('%Y-%m-%d') +
                '\t ' + str(len(stock_data)) + ' stk done'
                + '\n\tused amount this time: ' + str(used_amount)
                + '\n\tused amount this all: ' + str(used_amount_all)
            )

    def get_edb_data(self, start_date, end_date, db_path, table, sql_info, database, indicators):
        generate_table(
            database=database,
            table=table,
            generate_sql=sql_l_edb,
            sql_ip=sql_info['ip'],
            sql_user=sql_info['user'],
            sql_pass=sql_info['pass'],
            table_comment='Wind EDB数据'
        )
        print(table + ' generated')
        start_date0 = start_date

        for i in range(len(indicators)):
            print(indicators['指标名称'][i])
            data_exists = pd.read_sql_query(
                'select * from ' + table
                + ' where code=\'' + indicators['指标ID'][i]
                + '\' order by t_date',
                db_path
            )

            if len(data_exists) > 0:
                data_end_date = data_exists['t_date'].tolist()[-1]
                print(
                    '\tExisting ' + data_exists['t_date'].tolist()[0].strftime('%Y/%m/%d')
                    + ' - ' + data_exists['t_date'].tolist()[-1].strftime('%Y/%m/%d')
                )
                if data_end_date >= end_date:
                    print('\t\tData exists')
                    continue
                else:
                    start_date = (data_exists['t_date'].tolist()[-1] + timedelta(days=1))
            else:
                print('\tExisting None')
                start_date = start_date0

            data_raw = self.api.edb(
                indicators['指标ID'][i],
                start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')
            )
            if data_raw.ErrorCode != 0:
                print('\tWind error: ' + str(data_raw.ErrorCode))
                continue

            df = pd.DataFrame(
                {
                    'code': data_raw.Codes[0],
                    't_date': data_raw.Times,
                    'close': data_raw.Data[0]
                }
            ).dropna()
            df = df[df['t_date'] >= start_date]
            if len(df) > 0:
                df.to_sql(table, db_path, if_exists='append', index=False)
                print(
                    '\t\t更新 '
                    + df['t_date'].tolist()[0].strftime('%Y-%m-%d') + ' - '
                    + df['t_date'].tolist()[-1].strftime('%Y-%m-%d')
                )
            else:
                print('\t\t 无更新')

        # print()