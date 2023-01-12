import numpy as np
import re
import pdfplumber
import pandas as pd
import os
from datetime import datetime
from hbshare.quant.CChen.sql_cons import gtja_gzb_col_sql
from hbshare.quant.CChen.func import generate_table


def str_2_num(x):
    return np.nan if x in ['', ' '] else float(x.replace(',', '')) if type(x) == str else x


def gzb_str_2_num(df):
    df[['数量', '单位成本', '市价', '估值增值', '成本', '市值', '成本占净值', '市值占净值']] = df[
        ['数量', '单位成本', '市价', '估值增值', '成本', '市值', '成本占净值', '市值占净值']
    ].applymap(str_2_num)
    return df


def gen_gzb_table(table, db, sql_info):
    generate_table(
        database=db,
        table=table,
        generate_sql=gtja_gzb_col_sql,
        sql_ip=sql_info['ip'],
        sql_user=sql_info['user'],
        sql_pass=sql_info['pass'],
        table_comment='基金估值表'
    )
    print(table + ' generated')


def ht_transfer(x):
    # 华泰估值表科目名称去除冗余字段
    if type(x) == str:
        r = re.findall(r'[A-Za-z]+', x)
        if len(r):
            return re.findall(r'[A-Za-z0-9]+', x)[0]
        else:
            return x
    else:
        return x


# 用于读取华泰估值表
def ht_gzb(file_path):
    data = pd.read_excel(file_path)
    name = data.iloc[1, 0].replace('华泰证券股份有限公司_', '').replace('_专用表', '')
    name = name.replace('私募证券投资基金', '').replace('私募投资基金', '').replace('私募基金', '')
    date = datetime.strptime(data.iloc[2, 0][-10:], '%Y-%m-%d').date()
    data = data.iloc[:, list(range(6)) + [7, 8, 9, 11, 12, 14, 15]]
    data.columns = data.iloc[3]
    data = data.iloc[6:].reset_index(drop=True)
    df = data.rename(
        columns={
            '成本占比': '成本占净值',
            '行情': '市价',
            '市值占比': '市值占净值',
        }
    ).drop(columns=['币种', '汇率'])
    df_col = df.columns.tolist()
    df['基金名称'] = name
    df['日期'] = date
    df['成本占净值'] = df['成本占净值'] * 100
    df['市值占净值'] = df['市值占净值'] * 100
    df = gzb_str_2_num(df)
    df['科目名称'] = df['科目名称'].apply(ht_transfer)
    return df[['日期', '基金名称'] + df_col]


# 华泰估值表录入数据库
def ht_gzb_to_db(table, fpath, db_path):
    data_exists = pd.read_sql_query('select `日期`, `基金名称` from ' + table, db_path)
    data_exists['label'] = data_exists['基金名称'] + data_exists['日期'].apply(lambda x: x.strftime('%Y%m%d'))
    data_exists = data_exists['label'].tolist()

    file_list = os.listdir(fpath)
    for f in file_list:
        file = fpath + '/' + f
        df = ht_gzb(file_path=file)
        name = df['基金名称'][0]
        date = df['日期'][0]

        if name + date.strftime('%Y%m%d') not in data_exists:
            df.to_sql(table, db_path, index=False, if_exists='append')
            data_exists.append(name + date.strftime('%Y%m%d'))
            print(f)
        else:
            print(name + ' ' + date.strftime('%Y%m%d') + ' exists')


# 用于读取国泰君安估值表
def gtja_gzb(file_path):
    if file_path[-3:].lower() == 'pdf':
        pdf = pdfplumber.open(file_path)

        df = pd.DataFrame()
        name = None
        date = None

        for i in pdf.pages:
            if i.page_number == 1:
                i_text = i.extract_text()
                date = datetime.strptime(i_text[i_text.index('估值日期'):][5:13], '%Y%m%d').date()
                name_index0 = i_text.index('国泰君安证券股份有限公司__')
                name_index1 = i_text.index('__专用表')
                name = i_text[
                         name_index0 + 14: name_index1
                         ].replace('私募证券投资基金', '').replace('私募投资基金', '').replace('私募基金', '')
            table_raw = i.extract_tables()
            table_df = pd.DataFrame(table_raw[0][1:], columns=table_raw[0][0])
            for c in table_df.columns:
                table_df = table_df.rename(columns={c: c.replace('\n', '')})
            df = pd.concat([df, table_df])
        # df.applymap(lambda x: x.replace('\n', '') if type(x) == str else x)
        df['科目名称'] = df['科目名称'].apply(lambda x: x.replace('\n', ''))
        df['科目代码'] = df['科目代码'].apply(lambda x: x.replace('\n', ''))
        df['停牌信息'] = df['停牌信息'].apply(lambda x: x.replace('\n', ''))

    else:
        df = pd.read_excel(file_path)
        name = df.iloc[0, 0].replace('国泰君安证券股份有限公司__', '').replace('国泰君安___', '').replace('___专用表', '')
        name = name.replace('私募证券投资基金', '').replace('私募投资基金', '').replace('私募基金', '')
        date = datetime.strptime(df.iloc[1, 0][-8:], '%Y%m%d').date()
        df.columns = df.iloc[2]
        df = df.iloc[3:].reset_index(drop=True)
    df = df.rename(
        columns={
            '成本占净值%': '成本占净值',
            '市值占净值%': '市值占净值'
        }
    )
    df_col = df.columns.tolist()
    df['基金名称'] = name
    df['日期'] = date
    df = gzb_str_2_num(df)
    return df[['日期', '基金名称'] + df_col].reset_index(drop=True)


# 国泰君安估值表录入数据库
def gtja_gzb_to_db(table, fpath, db_path):
    data_exists = pd.read_sql_query('select `日期`, `基金名称` from ' + table, db_path)
    data_exists['label'] = data_exists['基金名称'] + data_exists['日期'].apply(lambda x: x.strftime('%Y%m%d'))
    data_exists = data_exists['label'].tolist()

    file_list = os.listdir(fpath)
    for f in file_list:
        file = fpath + '/' + f
        df = gtja_gzb(file_path=file)
        name = df['基金名称'][0]
        date = df['日期'][0]

        if name + date.strftime('%Y%m%d') not in data_exists:
            df.to_sql(table, db_path, index=False, if_exists='append')
            data_exists.append(name + date.strftime('%Y%m%d'))
            print(f)
        else:
            print(name + ' ' + date.strftime('%Y%m%d') + ' exists')


# 用于读取招商估值表
def zs_gzb(file_path):
    data = pd.read_excel(file_path)
    name = data.iloc[1, 0].replace('招商证券_', '').replace('_专用表', '').replace('招商证券备机_', '').replace('招商证券股份有限公司_', '')
    name = name.replace('私募证券投资基金', '').replace('私募投资基金', '').replace('私募基金', '')
    date = datetime.strptime(data.iloc[2, 0][-10:], '%Y-%m-%d').date()
    data.columns = data.iloc[3]
    data = data.iloc[7:].reset_index(drop=True)
    df = data.rename(
        columns={
            '成本-本币': '成本',
            '成本占比': '成本占净值',
            '行情': '市价',
            '市值-本币': '市值',
            '市值占比': '市值占净值',
            '估值增值-本币': '估值增值'
        }
    )
    df_col = df.columns.tolist()
    df['基金名称'] = name
    df['日期'] = date
    df['成本占净值'] = df['成本占净值'] * 100
    df['市值占净值'] = df['市值占净值'] * 100
    df = gzb_str_2_num(df)
    return df[['日期', '基金名称'] + df_col]


# 招商估值表录入数据库
def zs_gzb_to_db(table, fpath, db_path):
    data_exists = pd.read_sql_query('select `日期`, `基金名称` from ' + table, db_path)
    data_exists['label'] = data_exists['基金名称'] + data_exists['日期'].apply(lambda x: x.strftime('%Y%m%d'))
    data_exists = data_exists['label'].tolist()

    file_list = os.listdir(fpath)
    for f in file_list:
        file = fpath + '/' + f
        df = zs_gzb(file_path=file)[
            [
                '日期', '基金名称',
                '科目代码', '科目名称',
                '数量', '单位成本', '成本', '成本占净值',
                '市价', '市值', '市值占净值', '估值增值', '停牌信息',
            ]
        ]
        name = df['基金名称'][0]
        date = df['日期'][0]

        if name + date.strftime('%Y%m%d') not in data_exists:
            df.to_sql(table, db_path, index=False, if_exists='append')
            data_exists.append(name + date.strftime('%Y%m%d'))
            print(f)
        else:
            print(name + ' ' + date.strftime('%Y%m%d') + ' exists')


# 用于读取申万宏源估值表
def swhy_gzb(file_path):
    data = pd.read_excel(file_path)
    name = data.iloc[0, 0].replace('申万宏源证券有限公司___', '').replace('___专用表', '')
    name = name.replace('私募证券投资基金', '').replace('私募投资基金', '').replace('私募基金', '')
    date = datetime.strptime(data.iloc[1, 0][-10:], '%Y-%m-%d').date()
    data.columns = data.iloc[2]
    data = data.iloc[3:].reset_index(drop=True)
    df = data.rename(
        columns={
            '成本占净值(%)': '成本占净值',
            '市值占净值(%)': '市值占净值'
        }
    )
    df_col = df.columns.tolist()
    df['基金名称'] = name
    df['日期'] = date
    df = gzb_str_2_num(df)
    return df[['日期', '基金名称'] + df_col]


# 申万宏源估值表录入数据库
def swhy_gzb_to_db(table, fpath, db_path):
    data_exists = pd.read_sql_query('select `日期`, `基金名称` from ' + table, db_path)
    data_exists['label'] = data_exists['基金名称'] + data_exists['日期'].apply(lambda x: x.strftime('%Y%m%d'))
    data_exists = data_exists['label'].tolist()

    file_list = os.listdir(fpath)
    for f in file_list:
        file = fpath + '/' + f
        df = swhy_gzb(file_path=file).iloc[:, :13]
        name = df['基金名称'][0]
        date = df['日期'][0]

        if name + date.strftime('%Y%m%d') not in data_exists:
            df.to_sql(table, db_path, index=False, if_exists='append')
            data_exists.append(name + date.strftime('%Y%m%d'))
            print(f)
        else:
            print(name + ' ' + date.strftime('%Y%m%d') + ' exists')


if __name__ == '__main__':
    fpath = 'E:\\documents\\调研\\管理人材料\\Z智龙\\估值表\\智赢一号\\SGY648_SAP智龙智赢一号私募证券投资基金_4级科目估值表_20220722.pdf'
    a = gtja_gzb(fpath)

