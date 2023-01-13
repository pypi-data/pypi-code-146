import hbshare as hbs
import pandas as pd
from datetime import datetime
from hbshare.quant.CChen.func import generate_table
import pymysql

pymysql.install_as_MySQLdb()


list_sql_l = '''
    (
    code varchar(10) not null,
    name  varchar(100),
    manager  varchar(100),
    type  varchar(100),
    leverage  int,
    after_fee  int,
    fof  int,
    sales  int,
    first_date  date,
    latest_date  date,
    class  varchar(100),
    benchmark  varchar(100),
    stopped  int,
    primary key (id)
    )
    '''

fund_nw_sql_l = '''
    (
    t_date  date not null,
    nav  float null,
    source  varchar(100) null,
    primary key (t_date)
    )
    '''

funds_table_sql_l = '''
    (
    id bigint not null AUTO_INCREMENT,
    code  varchar(100),
    name  varchar(100),
    t_date  date not null,
    dwjz  float null,
    ljjz  float null,
    nav  float null,
    source  varchar(100) null,
    create_time  datetime,
    primary key (id)
    )
    '''


def update_fund_list_db(funds, db_path, sql_info):

    table = 'fund_list'

    generate_table(
        database='work',
        table=table,
        generate_sql=list_sql_l,
        sql_ip=sql_info['ip'],
        sql_user=sql_info['user'],
        sql_pass=sql_info['pass']
    )
    print(table + ' generated')

    fund_list = pd.DataFrame()
    fund_list = fund_list.append(funds, sort=False).reset_index(drop=True)

    existing_fund = pd.read_sql_query(
        'select * from ' + table, db_path
    )

    for f in range(len(fund_list)):
        print(fund_list['name'][f])
        if fund_list['code'][f] in existing_fund['code'].tolist():
            print(u'\t已存在')
        else:
            fund_list[f: f + 1].to_sql(table, db_path, if_exists='append', index=False)
            print(u'\t录入')


def update_fund_list_db2(db_path, sql_info, data_table='fund_data'):
    # 更新基金净值头尾日期
    table = 'fund_list'

    existing_fund = pd.read_sql_query(
        'select * from ' + table, db_path
    )

    conn = pymysql.connect(
        host=sql_info['ip'], port=3306, database='work',
        user=sql_info['user'], password=sql_info['pass'], charset='utf8'
    )
    cs1 = conn.cursor()

    for f in range(len(existing_fund)):
        print(existing_fund['name'][f])
        fund_data = pd.read_sql_query(
            'select * from ' + data_table
            + ' where code="' + existing_fund['code'][f].upper() + '" order by t_date',
            db_path
        )
        if len(fund_data) == 0:
            print('\tNo data')
            continue
        fund_date_start = fund_data['t_date'][0]
        fund_date_end = fund_data['t_date'][len(fund_data) - 1]

        query = 'update ' + table + ' set first_date=' + datetime.strftime(fund_date_start, '%Y%m%d') \
                + ', latest_date=' + datetime.strftime(fund_date_end, '%Y%m%d') \
                + ' where code="' + existing_fund['code'][f] + '"'

        cs1.execute(query)
        conn.commit()
        print(u'\t初始净值日期更新为：' + datetime.strftime(fund_date_start, '%Y-%m-%d'))
        print(u'\t最新净值日期更新为：' + datetime.strftime(fund_date_end, '%Y-%m-%d'))

    cs1.close()
    conn.close()


# 从hbshare读取基金信息
def update_fund_nav_db4(
        db_path,
        sql_info,
        table='fund_data',
        list_table='fund_list',
        start_date=datetime(1990, 1, 1).date(),
        token=''
):
    generate_table(
        database='work',
        table=table,
        generate_sql=funds_table_sql_l,
        sql_ip=sql_info['ip'],
        sql_user=sql_info['user'],
        sql_pass=sql_info['pass']
    )
    print(table + ' generated')

    fund_list = pd.read_sql_query(
        'select * from ' + list_table, db_path
    )
    for i in range(len(fund_list)):
        code = fund_list['code'][i]
        name = fund_list['name'][i]
        print(code + ' ' + name)

        data_exists = pd.read_sql_query(
            'select `code`, `name`, `t_date`, `nav`, `dwjz`, `ljjz` from ' + table
            + ' where `code`="' + code + '" order by t_date desc',
            db_path
        )

        try:
            data_new = hbs.get_simu_nav_by_code(
                code=code, start_date=start_date.strftime('%Y%m%d'), size=999
            )[0]
        except:
            print('Error')
            data_new = pd.DataFrame()

        # data_daily = hbs.commonQuery(
        #     'FB_RJZ', jjdm=code, access_token=token, fields=['netValueDate', 'netValue', 'fqdwjz', 'ljjz']
        # ).rename(
        #     columns={
        #         'netValueDate': 'jzrq',
        #         'netValue': 'jjjz',
        #     }
        # )
        # if len(data_daily) > 0:
        #     a = 1
        # data_new = data_new.append(data_daily).drop_duplicates(subset=['jzrq'])

        if len(data_new) == 0:
            print('\tNo new data')
        else:
            data_new = data_new.rename(
                columns={
                    'jjjz': 'dwjz',
                    'ljjz': 'ljjz',
                    'fqdwjz': 'nav'
                }
            )
            data_new['t_date'] = pd.to_datetime(data_new['jzrq'].astype(str)).dt.date
            data_new['code'] = code
            data_new['name'] = name
            data_new = data_new[['code', 'name', 't_date', 'nav', 'dwjz', 'ljjz']]
            data_new = data_exists.append(data_new).append(data_exists)
            data_new = data_new.drop_duplicates(['t_date'], keep=False).sort_values(by='t_date').reset_index(drop=True)
            print(data_new)
            data_new['create_time'] = datetime.now()
            data_new['source'] = 'hbdb'
            data_new.to_sql(table, db_path, if_exists='append', index=False)


def update_fund_nav_out(data, db_path, table='fund_data'):
    fund_list = pd.read_sql_query(
        'select * from fund_list', db_path
    )
    funds = data.columns.tolist()
    funds.remove('t_date')
    for i in funds:
        print(i)
        code = fund_list[fund_list['name'] == i]['code'].tolist()[0]
        nav = data[['t_date', i]].rename(columns={i: 'nav'})

        existing_fund_data = pd.read_sql_query(
            'select * from ' + table + ' where code="' + code + '" order by t_date', db_path
        )
        nav['code'] = code
        nav['name'] = i
        df = existing_fund_data.append(nav[nav['nav'] >= 0].reset_index(drop=True), sort=False)
        df_new = df.drop_duplicates(['t_date'], keep=False).reset_index(drop=True)
        df_new = df_new.append(existing_fund_data).append(existing_fund_data)
        df_new = df_new.drop_duplicates(['t_date'], keep=False).reset_index(drop=True)
        if len(df_new) == 0:
            print('\tNo new data')
            continue
        else:
            print(df_new)
            df_new['create_time'] = datetime.now()
            df_new['source'] = 'out'
        df_new.to_sql(table, db_path, if_exists='append', index=False)


