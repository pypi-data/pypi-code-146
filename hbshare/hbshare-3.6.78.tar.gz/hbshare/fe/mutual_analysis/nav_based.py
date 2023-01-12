import datetime
import pandas as pd
import numpy as np
from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from hbshare.fe.XZ import db_engine
from hbshare.fe.XZ import functionality
from sklearn.linear_model import LinearRegression as LR
from scipy.optimize import shgo, minimize
import statsmodels.api as sm


localdb=db_engine.PrvFunDB().engine
hbdb=db_engine.HBDB()
util=functionality.Untils()

def get_daily_indexnav(index_list,start_date=None,end_date=None):

    index_con = util.list_sql_condition(index_list)

    if (start_date is not None):
        date_con1 = " and jyrq>='{0}'".format(start_date)
    else:
        date_con1 = ''

    if (end_date is not None):
        date_con2 = " and jyrq<='{0}'".format(end_date)
    else:
        date_con2 = ''

    sql = "select zqdm,jyrq,spjg from st_market.t_st_zs_hqql where zqdm in ({0}) {1} {2}  " \
        .format(index_con, date_con1, date_con2)
    navdf = hbdb.db2df(sql, db='alluser')

    return navdf

def get_daily_jjnav(jjdm_list,start_date=None,end_date=None):
    jjdm_con = util.list_sql_condition(jjdm_list)

    if (start_date is not None):
        date_con1 = " and jzrq>='{0}'".format(start_date)
    else:
        date_con1 = ''

    if (end_date is not None):
        date_con2 = " and jzrq<='{0}'".format(end_date)
    else:
        date_con2 = ''

    sql = "select jjdm,jzrq,jjjz from st_fund.t_st_gm_jjjz where jjdm in ({0}) {1} {2}  " \
        .format(jjdm_con, date_con1, date_con2)
    navdf = hbdb.db2df(sql, db='funduser')

    return navdf

def get_monthly_jjnav(jjdm_list,start_date=None,end_date=None):

    jjdm_con = util.list_sql_condition(jjdm_list)

    if(start_date is not None):
        date_con1=" and tjyf>='{0}'".format(start_date[0:6])
    else:
        date_con1=''

    if(end_date is not None):
        date_con2 = " and tjyf<='{0}'".format(end_date[0:6])
    else:
        date_con2=''

    #get the nav ret  for given jjdm and time zone(already times 100)
    sql="select jjdm,tjyf,rqzh,hb1y from st_fund.t_st_gm_yhb where jjdm in ({0}) and hb1y!=99999 {1} {2} "\
        .format(jjdm_con,date_con1,date_con2)
    navdf=hbdb.db2df(sql, db='funduser')

    max_yearmonth=navdf['tjyf'].max()
    min_yearmonth=navdf['tjyf'].min()

    return navdf,max_yearmonth,min_yearmonth

def get_yearly_jjnav(jjdm_list,start_date=None,end_date=None):

    jjdm_con = util.list_sql_condition(jjdm_list)

    if(start_date is not None):
        date_con1=" and tjnf>='{0}'".format(start_date[0:4])
    else:
        date_con1=''

    if(end_date is not None):
        date_con2 = " and tjnf<='{0}'".format(end_date[0:4])
    else:
        date_con2=''

    #get the nav ret  for given jjdm and time zone(already times 100)
    sql="select jjdm,tjnf,rqzh,hb1n from st_fund.t_st_gm_nhb where jjdm in ({0}) and hb1n!=99999 {1} {2} "\
        .format(jjdm_con,date_con1,date_con2)
    navdf=hbdb.db2df(sql, db='funduser')

    max_yearmonth=navdf['tjnf'].max()
    min_yearmonth=navdf['tjnf'].min()

    return navdf,max_yearmonth,min_yearmonth

def get_daily_jjret(jjdm_list,start_date=None,end_date=None):

    jjdm_con=util.list_sql_condition(jjdm_list)

    if(start_date is not None):
        date_con1=" and jzrq>='{0}'".format(start_date)
    else:
        date_con1=''

    if(end_date is not None):
        date_con2 = " and jzrq<='{0}'".format(end_date)
    else:
        date_con2=''

    sql="select jjdm,jzrq,hbdr from st_fund.t_st_gm_rhb where jjdm in ({0}) and hbdr!=99999 and hbdr!=0 {1} {2}  "\
        .format(jjdm_con,date_con1,date_con2)
    navdf=hbdb.db2df(sql, db='funduser')

    return navdf

def get_weekly_jjnav(jjdm_list,start_date=None,end_date=None):

    jjdm_con=util.list_sql_condition(jjdm_list)

    if(start_date is not None):
        date_con1=" and tjrq>='{0}'".format(start_date)
    else:
        date_con1=''

    if(end_date is not None):
        date_con2 = " and tjrq<='{0}'".format(end_date)
    else:
        date_con2=''

    sql="select jjdm,tjrq,hb1z from st_fund.t_st_gm_zhb where jjdm in ({0}) and hb1z!=99999 and hb1z!=0 {1} {2}  "\
        .format(jjdm_con,date_con1,date_con2)
    navdf=hbdb.db2df(sql, db='funduser')

    return navdf

def get_monthly_index_ret(zqdm,start_date=None,end_date=None):

    if(start_date is not None):
        date_con1=" and tjyf>='{0}'".format(start_date[0:6])
    else:
        date_con1=''

    if(end_date is not None):
        date_con2 = " and tjyf<='{0}'".format(end_date[0:6])
    else:
        date_con2=''

    sql="select zqdm,tjyf,rqzh,hb1y from st_market.t_st_zs_yhb where zqdm='{0}' and abs(hb1y)!=99999 {1} {2}"\
        .format(zqdm,date_con1,date_con2)

    benchmark_ret=hbdb.db2df(sql, db='alluser')

    return  benchmark_ret

def get_yearly_index_ret(zqdm,start_date=None,end_date=None):

    if(start_date is not None):
        date_con1=" and tjnf>='{0}'".format(start_date[0:4])
    else:
        date_con1=''

    if(end_date is not None):
        date_con2 = " and tjnf<='{0}'".format(end_date[0:4])
    else:
        date_con2=''

    sql="select zqdm,tjnf,rqzh,hb1n from st_market.t_st_zs_nhb where zqdm='{0}' and abs(hb1n)!=99999 {1} {2}"\
        .format(zqdm,date_con1,date_con2)

    benchmark_ret=hbdb.db2df(sql, db='alluser')

    return  benchmark_ret

def get_weekly_index_ret(zqdm,start_date=None,end_date=None):

    if(start_date is not None):
        date_con1=" and tjrq>='{0}'".format(start_date)
    else:
        date_con1=''

    if(end_date is not None):
        date_con2 = " and tjrq<='{0}'".format(end_date)
    else:
        date_con2=''

    sql="select zqdm,tjrq,hb1z from st_market.t_st_zs_zhb where zqdm='{0}' and abs(hb1z)!=99999 {1} {2}"\
        .format(zqdm,date_con1,date_con2)

    benchmark_ret=hbdb.db2df(sql, db='alluser')

    return  benchmark_ret

def bhar(arr):
        return 100*(np.power(np.cumprod((arr+100)/100).tolist()[-1],1/len(arr))-1)

def ols_withcons_for_group(arr):
    y_col=arr.columns[0]
    x_col=arr.columns.tolist()
    x_col.remove(y_col)

    # result=util.my_general_linear_model_func(arr[x_col].values,
    #                                          arr[y_col].values)
    # # print(result['x'].sum())
    # # print(result['success'])
    # return result['x'].tolist()

    result = util.my_general_linear_model_func(arr[x_col].values,
                                             arr[y_col].values)
    return result

def ols_for_group(arr):

    y_col=arr.columns[0]
    x_col=arr.columns.tolist()
    x_col.remove(y_col)

    result=sm.OLS(arr[y_col].values, arr[x_col].values).fit()

    return result.params.tolist()

def ols_for_rolling(arr):

    y_col=arr.columns[0]
    x_col=arr.columns.tolist()
    x_col.remove(y_col)

    result=sm.OLS(arr[y_col].values, arr[x_col].values).fit()

    return result.params.tolist()

def get_barra_daily_ret(start_date=None,end_date=None):
    #barra return daily return
    sql='select factor_ret,factor_name,trade_date from st_ashare.r_st_barra_factor_return'
    test=hbdb.db2df(sql,db='alluser')
    factor_name_list=test['factor_name'].unique().tolist()
    factor_ret_df=pd.DataFrame()
    date_list=test['trade_date'].unique().tolist()
    date_list.sort()
    factor_ret_df['date']=date_list
    for factor in factor_name_list:
        factor_ret_df=pd.merge(factor_ret_df,test[test['factor_name']==factor][['factor_ret','trade_date']],
                               how='left',left_on='date',right_on='trade_date').drop('trade_date',axis=1)
        factor_ret_df.rename(columns={'factor_ret':factor},inplace=True)

    return factor_ret_df

def get_styleindex_ret(index_list,start_date=None,end_date=None):

    if(start_date is not None):
        start_date="and jyrq>='{}'".format(start_date)
    else:
        start_date=""

    if(end_date is not None):
        end_date="and jyrq<='{}'".format(end_date)
    else:
        end_date=""

    # style daily return
    style_ret=pd.DataFrame()
    for zqdm in index_list:

        #sql = "select spjg,zqmc,jyrq from st_market.t_st_zs_hqql where zqdm='{}' ".format(zqdm)
        sql= "select zqdm,jyrq,hbdr from st_market.t_st_zs_rhb where zqdm='{0}' and hbdr!=0 {1} {2} "\
            .format(zqdm,start_date,end_date)
        test = hbdb.db2df(sql=sql, db='alluser')
        #test['ret'] = test['spjg'].pct_change()
        test[zqdm]=test['hbdr']
        test.set_index('jyrq',inplace=True)
        style_ret=pd.concat([style_ret,test[zqdm]],axis=1)

    return style_ret

def get_barra_ret(col_list):

    theme_map = dict(zip(['Bank', 'RealEstate', 'Health', 'Transportation', 'Mining', 'NonFerMetal',
                               'HouseApp', 'LeiService', 'MachiEquip', 'BuildDeco', 'CommeTrade',
                               'CONMAT', 'Auto', 'Textile', 'FoodBever', 'Electronics',
                               'Computer', 'LightIndus', 'Utilities', 'Telecom', 'AgriForest',
                               'CHEM', 'Media', 'IronSteel', 'NonBankFinan', 'ELECEQP', 'AERODEF',
                               'Conglomerates'],
                              ['大金融', '大金融', '消费', '制造', '周期', '周期',
                               '周期', '消费', '制造', '周期', '消费',
                               '消费', '制造', '消费', '消费', 'TMT',
                               'TMT', '制造', '制造', 'TMT', '消费',
                               '周期', 'TMT', '周期', '大金融', '制造', '无',
                               '无']))
    col_con=util.list_sql_condition(col_list)

    sql="""select factor_ret,factor_name,trade_date from st_ashare.r_st_barra_factor_return where factor_name in 
    ({0}) and trade_date>='20171231'
       """.format(col_con)
    df=hbdb.db2df(sql,db='alluser')
    if(col_list==list(theme_map.keys())):
        df['factor_name']=[theme_map[x] for x in df['factor_name'] ]
    df = df.groupby(['trade_date', 'factor_name']).mean().unstack()*100
    df.columns = df.columns.get_level_values(1)
    df.drop('无',axis=1,inplace=True)

    return  df

def get_jj_daily_ret(jjdm_list):

    tempdf = get_daily_jjret(jjdm_list)
    jj_ret = pd.DataFrame()
    if(len(tempdf)>0):
        jj_ret['date'] = tempdf.sort_values('jzrq')['jzrq']
        for jjdm in tempdf['jjdm'].unique():
            jj_ret=pd.merge(jj_ret,tempdf[tempdf['jjdm']==jjdm][['hbdr','jzrq']],
                            how='left',left_on='date',right_on='jzrq').drop('jzrq',axis=1)
            jj_ret.rename(columns={'hbdr':jjdm},inplace=True)


        jj_ret.set_index('date',drop=True,inplace=True)
    else:
        jj_ret=[]

    return jj_ret

def style_exp_foroutsideuser():


    for zqdm in ['399372', '399373', '399374', '399375', '399376', '399377', 'CBA00301']:

        sql="select spjg,jyrq from st_market.t_st_zs_hq where jyrq>='20100105' and zqdm='{}'"\
            .format(zqdm)
        temdf=hbdb.db2df(sql,db='alluser').rename(columns={'spjg':zqdm})
        if(zqdm=='399372'):
            style_index_ret=temdf.copy()
        else:
            style_index_ret=pd.merge(style_index_ret,temdf,how='left',on='jyrq')

    style_index_ret.set_index('jyrq',inplace=True)


    priv_pool=pd.read_excel(r"C:\Users\xuhuai.zhe\Downloads\私募跟踪池.xlsx")
    jjjc_con=util.list_sql_condition(priv_pool['基金简称'].values.tolist())
    pri_basis=hbdb.db2df("select jjdm,jjjc from st_hedge.t_st_jjxx where jjjc in ({})"
                         .format(jjjc_con),db='highuser')
    pri_basis.drop_duplicates('jjjc',keep='first',inplace=True)
    jjdm_list=pri_basis['jjdm'].values.tolist()

    output = []
    for jjdm in jjdm_list:
        #S64497

        jj_ret=hbdb.db2df("select hbdr,jzrq,fqdwjz from st_hedge.t_st_rhb where jjdm='{}' and hbdr!=0".format(jjdm)
                          ,db='highuser').rename(columns={'hbdr':jjdm})
        jj_ret['jzrq']=jj_ret['jzrq'].astype(int)
        jj_ret.set_index('jzrq',inplace=True)

        olsdf=pd.merge(jj_ret,style_index_ret,how='left',left_index=True,right_index=True).fillna(0)
        olsdf[['399372', '399373', '399374', '399375','399376', '399377', 'CBA00301']]=\
            olsdf[['399372', '399373', '399374', '399375','399376', '399377', 'CBA00301']].pct_change()*100

        olsdf['399374'] = (olsdf['399374'] + olsdf['399376']) / 2
        olsdf['399375'] = (olsdf['399375'] + olsdf['399377']) / 2
        olsdf.drop(['399376','399377'],axis=1,inplace=True)
        olsdf = olsdf[olsdf['399372'] < 9999]

        laster_half_year=olsdf.index[olsdf.index>=int((datetime.datetime.strptime(str(jj_ret.index[-1]),
                                                     '%Y%m%d')-datetime.timedelta(days=183)).strftime('%Y%m%d'))][0]
        last_year=olsdf.index[olsdf.index>=int((datetime.datetime.strptime(str(jj_ret.index[-1]),
                                                     '%Y%m%d')-datetime.timedelta(days=365)).strftime('%Y%m%d'))][0]
        last_oneandhalfyear=olsdf.index[olsdf.index>=int((datetime.datetime.strptime(str(jj_ret.index[-1]),
                                                     '%Y%m%d')-datetime.timedelta(days=365+182)).strftime('%Y%m%d'))][0]


        result1=util.my_general_linear_model_func(olsdf.loc[int(laster_half_year):][['399372', '399373', '399374', '399375','CBA00301']].values
                                                 , olsdf.loc[int(laster_half_year):][jjdm].values)
        result2=util.my_general_linear_model_func(olsdf.loc[int(last_year):][['399372', '399373', '399374', '399375','CBA00301']].values
                                                 , olsdf.loc[int(last_year):][jjdm].values)
        result3=util.my_general_linear_model_func(olsdf.loc[int(last_oneandhalfyear):][['399372', '399373', '399374', '399375','CBA00301']].values
                                                 , olsdf.loc[int(last_oneandhalfyear):][jjdm].values)
        result=list((np.array(result1)+np.array(result2)+np.array(result3))/3)
        result.append(jjdm)

        output.append(result)

    outdf=pd.DataFrame(data=output,columns=['大盘成长','大盘价值','中小成长','中小盘价值','中债','jjdm'])
    outdf=pd.merge(outdf,pri_basis,how='left',on='jjdm')
    outdf.to_csv('prv_core_ols.csv')



    # style_index_ret = get_styleindex_ret(['399372', '399373', '399374', '399375', '399376', '399377', 'CBA00301'],
    #                                      start_date='20100105')
    # style_index_ret['399374'] = (style_index_ret['399374'] + style_index_ret['399376']) / 2
    # style_index_ret['399375'] = (style_index_ret['399375'] + style_index_ret['399377']) / 2
    # style_index_ret=style_index_ret[['399372', '399373', '399374', '399375','CBA00301']]
    #
    # sql="select * from core_pool_history where asofdate='{}'".format('202203')
    # mutual_pool=pd.read_sql(sql,con=localdb).rename(columns={'基金代码':'jjdm',
    #                                                   '基金名称':'jjjc',
    #                                                   '基金经理':'manager'})
    # jjdm_list=mutual_pool['jjdm'].unique().tolist()
    #
    # output=[]
    #
    # for jjdm in jjdm_list:
    #     # get jj nav ret
    #     jj_ret = get_jj_daily_ret([jjdm])
    #     laster_half_year=util._shift_date( (datetime.datetime.strptime(str(jj_ret.index[-1]),
    #                                                  '%Y%m%d')-datetime.timedelta(days=183)).strftime('%Y%m%d'))
    #     last_year=util._shift_date( (datetime.datetime.strptime(str(jj_ret.index[-1]),
    #                                                  '%Y%m%d')-datetime.timedelta(days=365)).strftime('%Y%m%d'))
    #     last_oneandhalfyear=util._shift_date((datetime.datetime.strptime(str(jj_ret.index[-1]),
    #                                                  '%Y%m%d')-datetime.timedelta(days=365+182)).strftime('%Y%m%d'))
    #
    #     olsdf=pd.merge(jj_ret,style_index_ret,how='left',left_index=True,right_index=True).fillna(0)
    #
    #
    #     result1=util.my_general_linear_model_func(olsdf.loc[int(laster_half_year):][['399372', '399373', '399374', '399375','CBA00301']].values
    #                                              , olsdf.loc[int(laster_half_year):][jjdm].values)
    #     result2=util.my_general_linear_model_func(olsdf.loc[int(last_year):][['399372', '399373', '399374', '399375','CBA00301']].values
    #                                              , olsdf.loc[int(last_year):][jjdm].values)
    #     result3=util.my_general_linear_model_func(olsdf.loc[int(last_oneandhalfyear):][['399372', '399373', '399374', '399375','CBA00301']].values
    #                                              , olsdf.loc[int(last_oneandhalfyear):][jjdm].values)
    #     result=list((np.array(result1)+np.array(result2)*0.5+np.array(result3)*0.25)/1.75)
    #     result.append(jjdm)
    #
    #     output.append(result)
    #
    # outdf=pd.DataFrame(data=output,columns=['大盘成长','大盘价值','中小成长','中小盘价值','中债','jjdm'])
    # outdf=pd.merge(outdf,mutual_pool,how='left',on='jjdm')
    # outdf.to_csv('mutual_core_ols.csv')

def style_exp_simpleols_foroutsideuser_prv():

    #prv part
    for zqdm in ['399372', '399373', '399374', '399375', '399376', '399377', 'CBA00301']:

        sql="select spjg,jyrq from st_market.t_st_zs_hq where jyrq>='20100105' and zqdm='{}'"\
            .format(zqdm)
        temdf=hbdb.db2df(sql,db='alluser').rename(columns={'spjg':zqdm})
        if(zqdm=='399372'):
            style_index_ret=temdf.copy()
        else:
            style_index_ret=pd.merge(style_index_ret,temdf,how='left',on='jyrq')

    style_index_ret.set_index('jyrq',inplace=True)


    priv_pool=pd.read_excel(r"E:\GitFolder\docs\净值标签\全部私募打标结果20220718.xlsx",sheet_name='数据')
    jjjc_con=util.list_sql_condition(priv_pool['基金简称'].values.tolist())
    pri_basis=hbdb.db2df("select jjdm,jjjc from st_hedge.t_st_jjxx where jjjc in ({})"
                         .format(jjjc_con),db='highuser')
    pri_basis.drop_duplicates('jjjc',keep='first',inplace=True)

    today=datetime.datetime.today().strftime('%Y%m%d')

    jjdm_list=hbdb.db2df("select jjdm from st_hedge.t_st_jjxx where cpfl='4' and jjzt='0' and jjfl='1' and clrq<='{}' "
                         .format(str(int(today[0:4])-2)+today[4:]),db='highuser') ['jjdm'].values.tolist()
    jjdm_list=list(set(jjdm_list+pri_basis['jjdm'].unique().tolist()))
    jjdm_list_core=pri_basis['jjdm'].unique().tolist()

    result1=[]
    result2 = []
    result3 = []

    result4=[]
    result5 = []
    result6 = []

    for jjdm in jjdm_list:

        # try:
        print(jjdm)
        jj_ret=hbdb.db2df("select hbdr,jzrq,fqdwjz from st_hedge.t_st_rhb where jjdm='{}' and hbdr!=0".format(jjdm)
                          ,db='highuser').rename(columns={'hbdr':jjdm})
        if((len(jj_ret)==0 or jj_ret['jzrq'].min()>=str(int(today[0:4])-2)+today[4:] or jj_ret['jzrq'].max()<=str(int(today)-6000) )
                or (jjdm not in jjdm_list_core) ):
            continue
        jj_ret['jzrq']=jj_ret['jzrq'].astype(int)
        jj_ret.set_index('jzrq',inplace=True)

        olsdf=pd.merge(jj_ret,style_index_ret,how='left',left_index=True,right_index=True).fillna(0)
        if(len(olsdf)<=12):
            continue
        olsdf[['399372', '399373', '399374', '399375','399376', '399377', 'CBA00301']]=\
            olsdf[['399372', '399373', '399374', '399375','399376', '399377', 'CBA00301']].pct_change()*100

        olsdf['399374'] = (olsdf['399374'] + olsdf['399376']) / 2
        olsdf['399375'] = (olsdf['399375'] + olsdf['399377']) / 2
        olsdf.drop(['399376','399377'],axis=1,inplace=True)
        olsdf = olsdf[olsdf['399372'] < 9999]

        laster_half_year=olsdf.index[olsdf.index>=int((datetime.datetime.strptime(str(jj_ret.index[-1]),
                                                     '%Y%m%d')-datetime.timedelta(days=183)).strftime('%Y%m%d'))][0]
        last_year=olsdf.index[olsdf.index>=int((datetime.datetime.strptime(str(jj_ret.index[-1]),
                                                     '%Y%m%d')-datetime.timedelta(days=365)).strftime('%Y%m%d'))][0]
        last_oneandhalfyear=olsdf.index[olsdf.index>=int((datetime.datetime.strptime(str(jj_ret.index[-1]),
                                                     '%Y%m%d')-datetime.timedelta(days=365+182)).strftime('%Y%m%d'))][0]
        para = sm.OLS(olsdf.loc[int(laster_half_year):][jjdm].values,
                      olsdf.loc[int(laster_half_year):][
                          ['399372', '399373', '399374', '399375', 'CBA00301']].values).fit().params.tolist()
        result1.append(para+[jjdm])
        result4.append([para[0] + para[1], para[2] + para[3], para[0] + para[2],
                        para[1] + para[3], para[0] + para[1] - para[2] + para[3], para[0] + para[2] - para[1] + para[3],
                        jjdm])

        para = sm.OLS(olsdf.loc[int(last_year):][jjdm].values,
                      olsdf.loc[int(last_year):][
                          ['399372', '399373', '399374', '399375', 'CBA00301']].values).fit().params.tolist()
        result2.append(para+[jjdm])
        result5.append([para[0] + para[1], para[2] + para[3], para[0] + para[2],
                        para[1] + para[3], para[0] + para[1] - para[2] + para[3], para[0] + para[2] - para[1] + para[3],
                        jjdm])

        para = sm.OLS(olsdf.loc[int(last_oneandhalfyear):][jjdm].values,
                      olsdf.loc[int(last_oneandhalfyear):][
                          ['399372', '399373', '399374', '399375', 'CBA00301']].values).fit().params.tolist()
        result3.append(para+[jjdm])
        result6.append([para[0] + para[1], para[2] + para[3], para[0] + para[2],
                        para[1] + para[3], para[0] + para[1] - para[2] + para[3], para[0] + para[2] - para[1] + para[3],
                        jjdm])

        # except Exception as e:
        #     print(jjdm)
        #     print(e)



    result4=pd.DataFrame(data=result4,columns=['大盘','中小盘','成长','价值','大-中小','成长-价值','jjdm'])
    result5 = pd.DataFrame(data=result5, columns=['大盘','中小盘','成长','价值','大-中小','成长-价值','jjdm'])
    result6 = pd.DataFrame(data=result6, columns=['大盘','中小盘','成长','价值','大-中小','成长-价值','jjdm'])

    result1=pd.DataFrame(data=result1,columns=['大盘成长','大盘价值','中小盘成长','中小盘价值','中债','jjdm'])
    result2 = pd.DataFrame(data=result2, columns=['大盘成长','大盘价值','中小盘成长','中小盘价值','中债','jjdm'])
    result3 = pd.DataFrame(data=result3, columns=['大盘成长','大盘价值','中小盘成长','中小盘价值','中债','jjdm'])


    col_list = ['大盘成长', '大盘价值', '中小盘成长', '中小盘价值', '中债']
    result1[col_list]=result1[col_list].rank(method='min') / len(result1)
    result2[col_list]= result2[col_list].rank(method='min') / len(result2)
    result3[col_list] = result3[col_list].rank(method='min') / len(result3)



    output=result1.copy()
    output[col_list]=(result1[col_list]+result2[col_list]
                      +result3[col_list])/3
    outdf=pd.merge(pri_basis,output,how='left',on='jjdm')
    outdf.to_excel('prv_core_ols_1.xlsx')
    output.to_excel('prv_core_ols_11.xlsx')


    col_list2 = ['大盘', '中小盘', '成长', '价值', '大-中小', '成长-价值']
    result4[col_list2]=result4[col_list2].rank(method='min') / len(result4)
    result5[col_list2]= result5[col_list2].rank(method='min') / len(result5)
    result6[col_list2] = result6[col_list2].rank(method='min') / len(result6)
    output=result4.copy()
    output[col_list2]=(result4[col_list2]+result5[col_list2]
                      +result6[col_list2])/3
    outdf=pd.merge(pri_basis,output,how='left',on='jjdm')
    outdf.to_excel('prv_core_ols_2.xlsx')
    output.to_excel('prv_core_ols_22.xlsx')

def style_exp_simpleols_foroutsideuser_mu():



    style_index_ret = get_styleindex_ret(['399372', '399373', '399374', '399375', '399376', '399377', 'CBA00301'],
                                         start_date='20100105')
    style_index_ret['399374'] = (style_index_ret['399374'] + style_index_ret['399376']) / 2
    style_index_ret['399375'] = (style_index_ret['399375'] + style_index_ret['399377']) / 2
    style_index_ret=style_index_ret[['399372', '399373', '399374', '399375','CBA00301']]

    sql="select * from core_pool_history where asofdate='{}'".format('202203')
    mutual_pool=pd.read_sql(sql,con=localdb).rename(columns={'基金代码':'jjdm',
                                                      '基金名称':'jjjc',
                                                      '基金经理':'manager'})
    jjdm_list=util.get_potient_mutual_stock_funds('20220630')


    result1=[]
    result2 = []
    result3 = []

    result4=[]
    result5 = []
    result6 = []

    for jjdm in jjdm_list:
        # # get jj nav ret
        # try:
        jj_ret = get_jj_daily_ret([jjdm])

        olsdf=pd.merge(jj_ret,style_index_ret,how='left',left_index=True,right_index=True).fillna(0)

        laster_half_year = olsdf.index[olsdf.index >= int((datetime.datetime.strptime(str(jj_ret.index[-1]),
                                                                                      '%Y%m%d') - datetime.timedelta(
            days=183)).strftime('%Y%m%d'))][0]
        last_year = olsdf.index[olsdf.index >= int((datetime.datetime.strptime(str(jj_ret.index[-1]),
                                                                               '%Y%m%d') - datetime.timedelta(
            days=365)).strftime('%Y%m%d'))][0]
        last_oneandhalfyear = olsdf.index[olsdf.index >= int((datetime.datetime.strptime(str(jj_ret.index[-1]),
                                                                                         '%Y%m%d')-datetime.timedelta(days=365+182)).strftime('%Y%m%d'))][0]
        para = sm.OLS(olsdf.loc[int(laster_half_year):][jjdm].values,
                      olsdf.loc[int(laster_half_year):][
                          ['399372', '399373', '399374', '399375', 'CBA00301']].values).fit().params.tolist()
        result1.append(para + [jjdm])
        result4.append([para[0] + para[1], para[2] + para[3], para[0] + para[2],
                        para[1] + para[3], para[0] + para[1] - para[2] + para[3],
                        para[0] + para[2] - para[1] + para[3],
                        jjdm])

        para = sm.OLS(olsdf.loc[int(last_year):][jjdm].values,
                      olsdf.loc[int(last_year):][
                          ['399372', '399373', '399374', '399375', 'CBA00301']].values).fit().params.tolist()
        result2.append(para + [jjdm])
        result5.append([para[0] + para[1], para[2] + para[3], para[0] + para[2],
                        para[1] + para[3], para[0] + para[1] - para[2] + para[3],
                        para[0] + para[2] - para[1] + para[3],
                        jjdm])

        para = sm.OLS(olsdf.loc[int(last_oneandhalfyear):][jjdm].values,
                      olsdf.loc[int(last_oneandhalfyear):][
                          ['399372', '399373', '399374', '399375', 'CBA00301']].values).fit().params.tolist()
        result3.append(para + [jjdm])
        result6.append([para[0] + para[1], para[2] + para[3], para[0] + para[2],
                        para[1] + para[3], para[0] + para[1] - para[2] + para[3],
                        para[0] + para[2] - para[1] + para[3],
                        jjdm])

        #
        # except Exception as e:
        #     print(jjdm)
        #     print(e)


    result4=pd.DataFrame(data=result4,columns=['大盘','中小盘','成长','价值','大-中小','成长-价值','jjdm'])
    result5 = pd.DataFrame(data=result5, columns=['大盘','中小盘','成长','价值','大-中小','成长-价值','jjdm'])
    result6 = pd.DataFrame(data=result6, columns=['大盘','中小盘','成长','价值','大-中小','成长-价值','jjdm'])

    result1=pd.DataFrame(data=result1,columns=['大盘成长','大盘价值','中小盘成长','中小盘价值','中债','jjdm'])
    result2 = pd.DataFrame(data=result2, columns=['大盘成长','大盘价值','中小盘成长','中小盘价值','中债','jjdm'])
    result3 = pd.DataFrame(data=result3, columns=['大盘成长','大盘价值','中小盘成长','中小盘价值','中债','jjdm'])


    col_list = ['大盘成长', '大盘价值', '中小盘成长', '中小盘价值', '中债']
    result1[col_list]=result1[col_list].rank(method='min') / len(result1)
    result2[col_list]= result2[col_list].rank(method='min') / len(result2)
    result3[col_list] = result3[col_list].rank(method='min') / len(result3)



    output=result1.copy()
    output[col_list]=(result1[col_list]+result2[col_list]
                      +result3[col_list])/3
    #outdf=pd.merge(mutual_pool,output,how='left',on='jjdm')
    #outdf.to_excel('mu_core_ols_1.xlsx')
    output.to_excel('mu_core_ols_1.xlsx')


    col_list2 = ['大盘', '中小盘', '成长', '价值', '大-中小', '成长-价值']
    result4[col_list2]=result4[col_list2].rank(method='min') / len(result4)
    result5[col_list2]= result5[col_list2].rank(method='min') / len(result5)
    result6[col_list2] = result6[col_list2].rank(method='min') / len(result6)
    output=result4.copy()
    output[col_list2]=(result4[col_list2]+result5[col_list2]
                      +result6[col_list2])/3

    output.to_excel('mu_core_ols_2all.xlsx')
    # outdf=pd.merge(mutual_pool,output,how='left',on='jjdm')
    # outdf.to_excel('mu_core_ols_2.xlsx')

def rolling_rank(array):
    s = pd.Series(array)
    return s.rank(ascending=True).iloc[-1] / len(array)

def rolling_cumprod(array):
    s = pd.Series(array)
    return s.cumprod()[-1]

class Scenario_return:
    @staticmethod
    def get_histroy_scenario_ret():
        benchmark_ret=get_monthly_index_ret('000002')
        benchmark_ret['med']=99999
        benchmark_ret['scenario'] = ''
        for i in range(1,len(benchmark_ret)):
            benchmark_ret.loc[i,'med']=benchmark_ret.loc[0:i-1]['hb1y'].median()
            if(benchmark_ret.loc[i,'med']>=benchmark_ret.loc[i,'hb1y']):
                benchmark_ret.loc[i, 'scenario']='opt'
            else:
                benchmark_ret.loc[i, 'scenario'] = 'pes'

        return  benchmark_ret[['scenario','hb1y','tjyf','rqzh']]

    @staticmethod
    def pessimistic_ret(jjdm,benchmark_ret,start_date):

        navdf,max_yearmonth,min_yearmonth=get_monthly_jjnav([jjdm]
                                                            ,start_date=str(int(start_date[0:4])-2)+start_date[4:])

        navdf=pd.merge(navdf,benchmark_ret,how='left',on='tjyf')

        navdf['ext_ret']=navdf['hb1y_x']-navdf['hb1y_y']
        navdf.rename(columns={'rqzh_y':'rqzh'},inplace=True)

        #last 12 month average month return by calculating last 12 month cul ret and turn it into month return

        temp=navdf[navdf['scenario']=='pes']['ext_ret'].rolling(12).apply(bhar)
        temp=temp.to_frame('pes_ext_ret')
        navdf=pd.merge(navdf,temp,how='left',left_index=True, right_index=True)

        temp=navdf[navdf['scenario']=='opt']['ext_ret'].rolling(12).apply(bhar)
        temp=temp.to_frame('opt_ext_ret')
        navdf=pd.merge(navdf,temp,how='left',left_index=True, right_index=True)

        navdf['ext_ret'] = navdf['ext_ret'].rolling(12).apply(bhar)


        last_pes_ret=np.nan
        last_opt_ret=np.nan

        for i in range(0,len(navdf)):
            if(navdf.loc[i]['pes_ext_ret']==navdf.loc[i]['pes_ext_ret']):
                last_pes_ret=navdf.loc[i]['pes_ext_ret']

            else:
                navdf.loc[i,'pes_ext_ret']=last_pes_ret

            if(navdf.loc[i]['opt_ext_ret']==navdf.loc[i]['opt_ext_ret']):
                last_opt_ret=navdf.loc[i]['opt_ext_ret']

            else:
                navdf.loc[i,'opt_ext_ret']=last_opt_ret

        navdf=navdf[navdf['ext_ret'].notnull()]

        # for col in['ext_ret','pes_ext_ret','opt_ext_ret']:
        #     navdf[col] = (navdf[col]/100).astype(float).map("{:.2%}".format)

        return navdf[['jjdm','tjyf','rqzh','ext_ret','pes_ext_ret','opt_ext_ret']]

    @staticmethod
    def factorlize_ret(factor_name,fre='M'):

        sql="select * from scenario_ret where tjyf>'201512'"
        raw_df=pd.read_sql(sql,con=localdb)

        raw_df.rename(columns={'rqzh':'date'},inplace=True)
        raw_df=raw_df[raw_df[factor_name].notnull()]


        if(fre=='Q'):
            raw_df = raw_df[(raw_df['tjyf'].astype(str).str[4:6] == '03') | (raw_df['tjyf'].astype(str).str[4:6] == '06') | (
                        raw_df['tjyf'].astype(str).str[4:6] == '09') | (raw_df['tjyf'].astype(str).str[4:6] == '12')]
        elif(fre=='HA'):
            raw_df = raw_df[(raw_df['tjyf'].astype(str).str[4:6] == '06') | (raw_df['tjyf'].astype(str).str[4:6] == '12')]


        return raw_df

class Style_exp:


    def __init__(self,asofdate,fre='Q',start_date=None,end_date=None):


        self.jjdm_list=util.get_mutual_stock_funds(asofdate)

        self.write_style_exp2DB(self.jjdm_list, fre, start_date, end_date)

        #self.write_theme_exp2DB(self.jjdm_list, fre, start_date, end_date)

    @staticmethod
    def write_style_exp2DB(jjdm_list,fre,start_date=None,end_date=None):

        value_col = ['399370', '399371']
        size_col=['399314','399315','399316']
        bond_col=['CBA00301']

        #get value index ret :
        style_index_ret=get_styleindex_ret(value_col+size_col+bond_col)

        if(fre=='M'):
            def timezone_transform(olsdf):
                olsdf['yearmonth'] = [str(x)[0:6] for x in olsdf.index]
                return olsdf
        elif(fre=='Q'):
            def timezone_transform(olsdf):
                olsdf['yearmonth'] = ''
                olsdf.loc[olsdf.index.astype(str).str[4:6]<='03','yearmonth']='Q1'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '06')&(olsdf.index.astype(str).str[4:6] > '03'), 'yearmonth'] = 'Q2'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '09')&(olsdf.index.astype(str).str[4:6] > '06'), 'yearmonth'] = 'Q3'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '12')&(olsdf.index.astype(str).str[4:6] > '09'), 'yearmonth'] = 'Q4'
                olsdf['yearmonth']=olsdf.index.astype(str).str[0:4]+olsdf['yearmonth']

                return olsdf

        value_exp_df = pd.DataFrame()
        size_exp_df = pd.DataFrame()

        for jjdm in jjdm_list:
            print('{} start'.format(jjdm))
            #get jj nav ret
            jj_ret=get_jj_daily_ret([jjdm])
            if(len(jj_ret)==0):
                continue
            olsdf = pd.merge(jj_ret, style_index_ret, how='inner', left_index=True, right_index=True)

            olsdf=timezone_transform(olsdf)


            tempdf=olsdf[olsdf[[jjdm]+value_col+bond_col].notnull().sum(axis=1)==(len(value_col)+2)]
            tempdf=tempdf.groupby('yearmonth')[[jjdm]+value_col+bond_col].apply(ols_for_group).to_frame('exp')
            i=0
            for col in value_col+bond_col:
                tempdf[col]=[x[i] for x in tempdf['exp']]
                i+=1
            tempdf.drop('exp',inplace=True,axis=1)
            tempdf['jjdm']=jjdm
            value_exp_df=pd.concat([value_exp_df,tempdf],axis=0)


            tempdf=olsdf[olsdf[[jjdm]+size_col+bond_col].notnull().sum(axis=1)==(len(size_col)+2)]
            tempdf=tempdf.groupby('yearmonth')[[jjdm]+size_col+bond_col].apply(ols_for_group).to_frame('exp')
            i=0
            for col in size_col+bond_col:
                tempdf[col]=[x[i] for x in tempdf['exp']]
                i+=1
            tempdf.drop('exp',inplace=True,axis=1)
            tempdf['jjdm'] = jjdm
            size_exp_df=pd.concat([size_exp_df,tempdf],axis=0)

            print('jj {} Done'.format(jjdm))

        value_exp_df=value_exp_df.reset_index().rename(columns={'yearmonth':'date'})
        size_exp_df=size_exp_df.reset_index().rename(columns={'yearmonth':'date'})

        value_exp_df['fre']=fre
        size_exp_df['fre']=fre

        sql="delete from nav_value_exposure where fre='{}'".format(fre)
        localdb.execute(sql)
        value_exp_df.to_sql('nav_value_exposure',index=False,if_exists='append',con=localdb)


        sql="delete from nav_size_exposure where fre='{}'".format(fre)
        localdb.execute(sql)
        size_exp_df.to_sql('nav_size_exposure', index=False, if_exists='append',con=localdb)

    @staticmethod
    def write_theme_exp2DB(jjdm_list,fre,start_date=None,end_date=None):

        industry_con=['Bank', 'RealEstate', 'Health', 'Transportation', 'Mining', 'NonFerMetal',
        'HouseApp', 'LeiService', 'MachiEquip', 'BuildDeco', 'CommeTrade',
        'CONMAT', 'Auto', 'Textile', 'FoodBever', 'Electronics',
        'Computer', 'LightIndus', 'Utilities', 'Telecom', 'AgriForest',
        'CHEM', 'Media', 'IronSteel', 'NonBankFinan', 'ELECEQP', 'AERODEF',
        'Conglomerates']

        bond_col=['CBA00301']

        #get value index ret :
        #style_index_ret=get_styleindex_ret(bond_col)
        style_index_ret=get_barra_ret(industry_con)
        style_index_ret.index=style_index_ret.index.astype(int)
        style_index_ret=pd.merge(style_index_ret,get_styleindex_ret(bond_col),
                                 how='inner',left_index=True,right_index=True)

        if(fre=='M'):
            def timezone_transform(olsdf):
                olsdf['yearmonth'] = [str(x)[0:6] for x in olsdf.index]
                return olsdf
        elif(fre=='Q'):
            def timezone_transform(olsdf):
                olsdf['yearmonth'] = ''
                olsdf.loc[olsdf.index.astype(str).str[4:6]<='03','yearmonth']='Q1'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '06')&(olsdf.index.astype(str).str[4:6] > '03'), 'yearmonth'] = 'Q2'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '09')&(olsdf.index.astype(str).str[4:6] > '06'), 'yearmonth'] = 'Q3'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '12')&(olsdf.index.astype(str).str[4:6] > '09'), 'yearmonth'] = 'Q4'
                olsdf['yearmonth']=olsdf.index.astype(str).str[0:4]+olsdf['yearmonth']

                return olsdf

        industry_exp_df = pd.DataFrame()

        for jjdm in jjdm_list:

            #get jj nav ret
            jj_ret=get_jj_daily_ret([jjdm])

            olsdf = pd.merge(jj_ret, style_index_ret, how='inner', left_index=True, right_index=True)

            olsdf=timezone_transform(olsdf)

            theme_col=['大金融','周期','制造', '消费', 'TMT']

            tempdf=olsdf[olsdf[[jjdm]+theme_col+bond_col].notnull().sum(axis=1)==(len(theme_col)+2)]
            tempdf=tempdf.groupby('yearmonth')[[jjdm]+theme_col+bond_col].apply(ols_withcons_for_group).to_frame('exp')
            i=0
            for col in theme_col+bond_col:
                tempdf[col]=[x[i] for x in tempdf['exp']]
                i+=1
            tempdf.drop('exp',inplace=True,axis=1)
            tempdf['jjdm']=jjdm
            industry_exp_df=pd.concat([industry_exp_df,tempdf],axis=0)

            print('jj {} Done'.format(jjdm))

        industry_exp_df=industry_exp_df.reset_index().rename(columns={'yearmonth':'date'})

        industry_exp_df['fre']=fre

        industry_exp_df.to_sql('nav_theme_exposure',index=False,if_exists='append',con=localdb)

class Style_analysis:

    def __init__(self,jjdm_list,fre,asofdate=datetime.datetime.today().strftime('%Y%m%d'),time_length=3):

        self.value_col = ['399370', '399371']
        self.size_col=['399314','399315','399316']
        self.bond_col=['CBA00301']
        self.theme_col=['大金融','周期','制造', '消费', 'TMT']
        self.jjdm_list=jjdm_list

        self.index_map=dict(zip(self.value_col+self.size_col,['成长','价值','大盘','中盘','小盘']))

        self.theme_map=dict(zip(self.theme_col,self.theme_col))

        start_year=str(int(asofdate[0:4])-time_length)

        if(fre=='M'):
            start_date=start_year+asofdate[4:6]
        else:
            if(asofdate[4:6]<='03'):
                Q=1
            elif(asofdate[4:6]>'03' and asofdate[4:6]<='06'):
                Q=2
            elif(asofdate[4:6]>'06' and asofdate[4:6]<='09'):
                Q=3
            elif(asofdate[4:6]>'09' and asofdate[4:6]<='12'):
                Q=4
            start_date=start_year+"Q"+str(Q)

        self.val_date=self.get_jj_valuation_date(jjdm_list,asofdate)
        self.fre=fre
        self.asofdate=asofdate
        self.start_date=start_date

    @staticmethod
    def get_jj_valuation_date(jjdm_list,asofdate):

        jjdm_con=util.list_sql_condition(jjdm_list)
        #read jjjl info
        sql="select jjdm,ryxm,rydm,rzrq from st_fund.t_st_gm_jjjl where ryzt='-1' and jjdm in ({0}) "\
            .format(jjdm_con)
        jj_val_date=hbdb.db2df(sql,db='funduser')

        #for jj with multi managers,take the one with longer staying in this jj
        jj_val_date=jj_val_date.sort_values('rzrq')
        jj_val_date.drop_duplicates('jjdm', keep='first', inplace=True)

        #remove jj with manager managing no longer than 1.5years
        # last_oneandhalfyear = (datetime.datetime.strptime(asofdate, '%Y%m%d')
        #                        -datetime.timedelta(days=560)).strftime('%Y%m%d')
        # jj_val_date['rzrq']=jj_val_date['rzrq'].astype(str)
        # jj_val_date=jj_val_date[jj_val_date['rzrq']<=last_oneandhalfyear]


        return  jj_val_date[['jjdm','rzrq','rydm']]

    @staticmethod
    def read_jj_style_exp(jjdm_list,type,fre,start_date):

        jjdm_con=util.list_sql_condition(jjdm_list)
        sql="select * from nav_{0}_exposure where jjdm in ({1}) and fre='{2}' and date>='{3}'"\
            .format(type,jjdm_con,fre,start_date)
        expdf=pd.read_sql(sql,con=localdb)

        return  expdf

    @staticmethod
    def cal_style_shift_ratio(df,style_col):

        # calculate the total change in styles

        df['shift_ratio'] = df[style_col].diff().abs().sum(axis=1)

        # df['change'] = df[style_col].diff().abs().sum(axis=1)
        # # calculate the average style exp between two dates
        # df['avg_exp'] = df[style_col].sum(axis=1).rolling(2).mean()
        # # calculate shift ratio
        # df['shift_ratio'] = df['change'] / df['avg_exp']

        return df['shift_ratio'].values

    @staticmethod
    def standardliza_by_rank(style_df,style_col,bond_col):

        style_df[[x+'_abs' for x in style_col]]=style_df[style_col]
        style_df[style_col] = style_df.groupby('date').rank(method='min')[style_col]

        style_df = pd.merge(style_df,
                            style_df.groupby('date').count()['jjdm'].to_frame('count'),
                            left_on='date', right_index=True)
        for col in style_col + bond_col:
            style_df[col] = style_df[col] / style_df['count']

        return  style_df

    @staticmethod
    def standardlize_by_robust(style_df,style_col):
        from sklearn.preprocessing import RobustScaler
        rs = RobustScaler()
        style_df[style_col] = rs.fit_transform(style_df[style_col].values)

        return  style_df

    def get_style_property(self,style_df,style_col,type,method=''):

        # style_df = style_df.drop_duplicates()
        style_map = self.index_map

        if(type=='size'):

            def centralization(df):
                centralization = np.mean((df.max(axis=1) * 2 + tempdf.median(axis=1)) / 3)
                return centralization
        else:
            def centralization(df):
                centralization = np.mean(df.max(axis=1))
                return centralization


        #standradlize the exp by either robustscaler or by ranking for each date
        if(method=='robust'):
            style_df = self.standardlize_by_robust(style_df, style_col)
        elif(method=='rank'):
            style_df=self.standardliza_by_rank(style_df,style_col,self.bond_col)


        asofdate=style_df['date'].max()

        style_property_df=pd.DataFrame()

        temp=style_df.groupby('jjdm').min()['date']
        new_jjdm_list=temp[temp<=self.start_date].index.tolist()

        new_jjdm_list.sort()

        style_property_df['jjdm']=new_jjdm_list

        for jjdm in new_jjdm_list:

            #check if manager changed during the time zone
            tempdf=style_df[style_df['jjdm']==jjdm]
            if(len(self.val_date[self.val_date['jjdm']==jjdm]['rzrq'])>0):
                manager_change=str(str(self.val_date[self.val_date['jjdm']==jjdm]['rzrq'].values[0])[0:6]<=self.start_date)
            else:
                manager_change='False'

            tempdf2 = tempdf.copy()
            total_weight = tempdf2[style_col].sum(axis=1)
            for col in style_col:
                tempdf2[col] = tempdf2[col].values / total_weight


            tempdf['shift_ratio'] = self.cal_style_shift_ratio(tempdf2, style_col)
            # tempdf['shift_ratio']=self.cal_style_shift_ratio(tempdf,style_col)/tempdf[self.bond_col].std()[0]


            # centralization=(tempdf[style_col].std(axis=1)/tempdf[style_col].mean(axis=1)).mean()
            #centralization = (tempdf[style_col].std(axis=1)).mean()
            centralization_lv=centralization(tempdf2[style_col])


            style_property_df.loc[style_property_df['jjdm'] == jjdm,
                                  'shift_ratio'] = tempdf['shift_ratio'].mean()
            style_property_df.loc[style_property_df['jjdm'] == jjdm,
                                  'centralization'] = centralization_lv

            for col in style_col:
                style_property_df.loc[style_property_df['jjdm'] == jjdm,
                                      style_map[col] + '_mean'] = tempdf[col].mean()
                # get the absolute exp
                style_property_df.loc[style_property_df['jjdm'] == jjdm,
                                      style_map[col] + '_abs_mean'] = tempdf[col+'_abs'].mean()


            style_property_df.loc[style_property_df['jjdm'] == jjdm,
                                  'manager_change'] = manager_change
        #get the style rank%
        # rank_col=style_property_df.columns.tolist()
        # rank_col.remove('jjdm')
        rank_col=['shift_ratio','centralization']
        style_property_df[[x+'_rank' for x in rank_col]]=style_property_df[rank_col].rank(method='min')/len(style_property_df)

        style_property_df['asofdate']=asofdate

        return style_property_df

    def save_style_property2localdb(self):

        # sql="select distinct asofdate from nav_style_property_value where fre='{0}' and by_manager='{1}' "\
        #     .format(self.fre,'True')
        # asofdate_list=pd.read_sql(sql,con=localdb)['asofdate'].values.tolist()
        #
        # if(self.asofdate in asofdate_list):
        #     sql="delete from nav_style_property_value where asofdate='{0}' and fre-'{1}' and by_manager='{2}'"\
        #         .format(self.asofdate,self.fre,'True'+str(self.consistant_date))
        #     localdb.excute(sql)


        # value_df=self.get_style_property(self.read_jj_style_exp(self.jjdm_list,
        #                                 'value',self.fre,self.start_date)
        #                                  ,self.value_col,'value',method='')
        # value_df['fre']=self.fre
        # value_df.to_sql('new_nav_style_property_value',index=False,con=localdb,if_exists='append')
        #
        # size_df=self.get_style_property(self.read_jj_style_exp(self.jjdm_list,
        #                                 'size',self.fre,self.start_date)
        #                                  ,self.size_col,'size',method='')
        # size_df['fre'] = self.fre
        # size_df.to_sql('new_nav_style_property_size',index=False,con=localdb,if_exists='append')


        value_df=self.get_style_property(self.read_jj_style_exp(self.jjdm_list,
                                        'value',self.fre,self.start_date)
                                         ,self.value_col,'value',method='rank')
        value_df['fre']=self.fre

        #check if data alreay exist :
        sql="delete from nav_style_property_value where asofdate='{0}' and fre='{1}'"\
            .format(value_df['asofdate'][0],self.fre)
        localdb.execute(sql)

        value_df.to_sql('nav_style_property_value',index=False,con=localdb,if_exists='append')

        size_df=self.get_style_property(self.read_jj_style_exp(self.jjdm_list,
                                        'size',self.fre,self.start_date)
                                         ,self.size_col,'size',method='rank')
        size_df['fre'] = self.fre

        #check if data alreay exist :
        sql="delete from nav_style_property_size where asofdate='{0}' and fre='{1}'"\
            .format(size_df['asofdate'][0],self.fre)
        localdb.execute(sql)

        size_df.to_sql('nav_style_property_size',index=False,con=localdb,if_exists='append')


        # industry_df=self.get_style_property(self.read_jj_style_exp(self.jjdm_list,
        #                                 'theme',self.fre,self.start_date)
        #                                  ,self.theme_col,'theme')
        # industry_df['fre']=self.fre
        # industry_df.to_sql('nav_style_property_theme',index=False,con=localdb,if_exists='append')


    #below if function for futher style shift analysis


    def style_change_detect_engine(self,q_df,diff1,diff2,q_list,col_list,t1,t2):

        style_change=[]

        for col in col_list:

            potential_date=diff2[diff2[col]<=-1*t1].index.to_list()
            last_added_date=q_list[-1]
            for date in potential_date:
                if(diff1.loc[q_df.index[q_df.index<=date][-3]][col]<=-1*t2):
                    added_date=q_df.index[q_df.index<=date][-3]
                elif(diff1.loc[q_df.index[q_df.index<=date][-2]][col]<=-1*t2):
                    added_date=q_df.index[q_df.index<=date][-2]
                elif(diff1.loc[q_df.index[q_df.index<=date][-1]][col]<=-1*t2):
                    added_date = q_df.index[q_df.index <= date][-1]
                else:
                    added_date = q_df.index[q_df.index <= date][-3]

                if((q_list.index(added_date)-q_list.index(last_added_date)<=2
                        and q_list.index(added_date)-q_list.index(last_added_date)>0) or added_date==q_list[-1]):
                    continue
                else:
                    style_change.append(added_date + "@" + col)
                    last_added_date = added_date

            potential_date = diff2[diff2[col] >= t1].index.to_list()
            last_added_date = q_list[-1]
            for date in potential_date:
                if (diff1.loc[q_df.index[q_df.index <= date][-3]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-3]
                elif (diff1.loc[q_df.index[q_df.index <= date][-2]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-2]
                elif (diff1.loc[q_df.index[q_df.index <= date][-1]][col] >= t2):
                    added_date = q_df.index[q_df.index <= date][-1]
                else:
                    added_date = q_df.index[q_df.index <= date][-3]

                if (q_list.index(added_date) - q_list.index(last_added_date) <= 2
                        and q_list.index(added_date) - q_list.index(last_added_date) > 0):
                    continue
                else:
                    style_change.append(added_date + "@" + col)
                    last_added_date = added_date

        return style_change

    def style_change_detect_engine2(self, q_df, diff1, col_list, t1, t2):

        style_change=[]
        t3=t2/2

        for col in col_list:

            tempdf=pd.merge(q_df[col],diff1[col],how='left',on='date')
            tempdf['style']=''
            style_num=0
            tempdf['style'].iloc[0:2] = style_num

            for i in range(2,len(tempdf)-1):
                if(tempdf[col+'_y'].iloc[i]>t1 and tempdf[col+'_y'].iloc[i+1]>-1*t3 ):
                    style_num+=1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif(tempdf[col+'_x'].iloc[i]-tempdf[tempdf['style']==style_num][col+'_x'][0]>t1 and
                     tempdf[col+'_y'].iloc[i]>t2 and tempdf[col+'_y'].iloc[i+1]>-1*t3):
                    style_num += 1
                    added_date=tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif(tempdf[col+'_y'].iloc[i]<-1*t1 and tempdf[col+'_y'].iloc[i+1]<t3 ):
                    style_num += 1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)
                elif (tempdf[col + '_x'].iloc[i] - tempdf[tempdf['style'] == style_num][col + '_x'][0] < -1*t1 and
                      tempdf[col + '_y'].iloc[i] < -1*t2 and tempdf[col + '_y'].iloc[i + 1] <  t3):
                    style_num += 1
                    added_date = tempdf.index[i]
                    style_change.append(added_date + "@" + col)

                tempdf['style'].iloc[i] = style_num

        return style_change

    def style_change_detect(self,df,q_list,col_list,t1,t2):

        q_list.sort()
        q_df = df.loc[q_list]
        diff1=q_df.diff(1)
        # diff2=q_df.rolling(3).mean().diff(2)
        # diff4 = q_df.rolling(3).mean().diff(4)

        # style_change_short=self.style_change_detect_engine(q_df,diff1,diff2,q_list,col_list,t1,t2)
        # style_change_long=self.style_change_detect_engine(q_df,diff1,diff4,q_list,col_list,t1,t2)
        # style_change=style_change_short+style_change_long

        style_change = self.style_change_detect_engine2(q_df, diff1, col_list, t1, t2)

        return list(set(style_change)),np.array(q_list)

    def shifting_expression(self,change_ret,name,jjdm,style='Total'):

        change_winning_pro_hld = sum(change_ret[3]) / len(change_ret)
        change_winning_pro_nextq=sum(change_ret[2]) / len(change_ret)
        left_ratio = sum(change_ret[0]) / len(change_ret)
        left_ratio_deep = sum(change_ret[1]) / len(change_ret)
        # right_ratio = 1-left_ratio
        # right_ratio_deep = 1 - left_ratio_deep
        one_q_ret = change_ret[4].mean()
        hid_q_ret = change_ret[5].mean()

        return  np.array([style.split('_')[0],len(change_ret),change_winning_pro_hld,change_winning_pro_nextq
                             ,one_q_ret,hid_q_ret,left_ratio,left_ratio_deep])

    def style_change_ret(self,df,q_list,col_list,t1,t2,factor_ret):

        style_change,q_list = self.style_change_detect(df,q_list,col_list,t1,t2)
        change_count = len(style_change)
        style_changedf=pd.DataFrame()
        style_changedf['date']=[x.split('@')[0] for x in style_change]
        style_changedf['style']=[x.split('@')[1] for x in style_change]
        style_changedf.sort_values('date',inplace=True,ascending=False)
        style_chang_extret=dict(zip(style_change,style_change))


        # def get_factor_return(q_list, first_change_date, style):
        #
        #     # get value index ret :
        #     sql="select zqdm,jyrq,spjg from st_market.t_st_zs_hqql where zqdm='{0}' and jyrq>='{1}' and jyrq<='{2}'"\
        #         .format(style, q_list[q_list < first_change_date][-2]+'01', q_list[-1]+'31')
        #
        #     fac_ret_df=hbdb.db2df(sql,db='alluser')
        #     fac_ret_df['jyrq']=fac_ret_df['jyrq'].astype(str)
        #
        #     fac_ret_df['ym']=fac_ret_df['jyrq'].str[0:6]
        #     tempdf=fac_ret_df.drop_duplicates('ym', keep='last')[['jyrq','ym']]
        #     fac_ret_df=pd.merge(fac_ret_df,tempdf,how='left',on='jyrq').fillna('').drop('ym_x',axis=1)
        #
        #     # fac_ret_df['jyrq'] = fac_ret_df['ym']
        #     fac_ret_df.set_index('ym_y', drop=True, inplace=True)
        #
        #     fac_ret_df['price'] = fac_ret_df['spjg']
        #
        #     return fac_ret_df

        def q_ret(fac_ret_df,q0,q1,time_length=1):
            res=np.power(fac_ret_df.loc[q1]['price']/fac_ret_df.loc[q0]['price'],1/time_length)-1
            return  res


        if(change_count>0):
            for style in style_changedf['style']:

                changedf=style_changedf[style_changedf['style']==style]
                changedf=changedf.sort_values('date')
                first_change_date=changedf['date'].values[0]
                fac_ret_df=factor_ret[(factor_ret['zqdm'] == style) & (
                            factor_ret['jyrq'] >= q_list[q_list < first_change_date][-2] + '01') & (
                                       factor_ret['jyrq'] <= q_list[-1] + '31')]
                # fac_ret_df=get_factor_return(q_list,first_change_date,style)


                for i in range(len(changedf)):
                    date=changedf.iloc[i]['date']

                    observer_term=np.append(q_list[q_list<date][-2:],q_list[(q_list>=date)][0:2])

                    new_exp=df[style].loc[observer_term[2]]
                    old_exp=df[style].loc[observer_term[1]]

                    q0=observer_term[0]
                    q1=observer_term[1]
                    old_ret=q_ret(fac_ret_df,q0,q1)
                    #if_left_deep = fac_ret_df['price'].loc[q0:q1].mean() > fac_ret_df['price'].loc[q1]
                    if_left_deep =( (fac_ret_df['price'].loc[(fac_ret_df['jyrq']>=q0+'31')
                                                             &(fac_ret_df['jyrq']<=q1+'31')].mean()
                                     > fac_ret_df['price'].loc[q0:q1]).sum()\
                                   /len(fac_ret_df['price'].loc[q0:q1])>=0.5 )

                    q0=observer_term[1]
                    q1=observer_term[2]
                    current_ret=q_ret(fac_ret_df,q0,q1)
                    if_left=( (fac_ret_df['price'].loc[(fac_ret_df['jyrq']>=q0+'31')
                                                             &(fac_ret_df['jyrq']<=q1+'31')].mean()
                                     > fac_ret_df['price'].loc[q0:q1]).sum()\
                                   /len(fac_ret_df['price'].loc[q0:q1])>=0.5 )

                    q0=observer_term[2]
                    q1=observer_term[3]
                    next_ret=q_ret(fac_ret_df,q0,q1)


                    if (i != len(changedf) - 1):
                        q1 = changedf.iloc[i + 1]['date']
                        # q2 = q1
                    else:
                        q1 = q_list[-1]
                        # q2=fac_ret_df.index[-1]

                    change_date=date
                    time_length = q_list.tolist().index(q1) - q_list.tolist().index(change_date)
                    holding_ret=q_ret(fac_ret_df,q0,q1,time_length=time_length)

                    if_win_next=(new_exp>old_exp)&(next_ret>current_ret)
                    if_win_hld=(new_exp>old_exp)&(holding_ret>current_ret)

                    shift_retur_next= (new_exp-old_exp)*(next_ret-current_ret)
                    shift_retur_hld = (new_exp - old_exp) * (holding_ret - current_ret)

                    style_chang_extret[date+"@"+style]=[if_left,if_left_deep,if_win_next,if_win_hld,shift_retur_next,shift_retur_hld]

        return style_chang_extret

    def style_shifting_analysis(self,df,q_list,col_list,t1,t2,name,jjdm,factor_ret):

        # col_list=[x+"_exp_adj" for x in col]
        change_ret=self.style_change_ret(df,q_list,col_list,t1=t1,t2=t2,factor_ret=factor_ret)
        change_ret = pd.DataFrame.from_dict(change_ret).T
        change_ret['style'] = list([x.split('@')[1] for x in change_ret.index])
        change_ret['date'] = list([x.split('@')[0] for x in change_ret.index])

        data=[]

        if(len(change_ret)>0):
            data.append(self.shifting_expression(change_ret,name,jjdm))
            for style in change_ret['style'].unique():
                tempdf=change_ret[change_ret['style']==style]
                data.append(self.shifting_expression(tempdf,name,jjdm,style))

        shift_df = pd.DataFrame(data=data,columns=['风格类型','切换次数','胜率（直到下次切换）','胜率（下季度）',
                                                   '下季平均收益','持有平均收益','左侧比率','深度左侧比例'])
        # for col in ['胜率（直到下次切换）','胜率（下季度）','下季平均收益','持有平均收益','左侧比率','深度左侧比例']:
        #     shift_df[col] = shift_df[col].astype(float).map("{:.2%}".format)

        return  shift_df

    @staticmethod
    def read_style_exp(style,fre,start_date,end_date=None):

        if(end_date is not None):
            end_date="and date<='{}'".format(end_date)
        else:
            end_date=""

        sql=" SELECT * from nav_{0}_exposure where fre='{1}' and date>='{2}' {3} "\
            .format(style,fre,start_date,end_date)
        style_exp=pd.read_sql(sql,con=localdb)

        if(fre=='Q'):
            quarter2month=dict(zip(['Q1','Q2','Q3','Q4'],['03','06','09','12']))
            style_exp['date']=[x[0:4]+quarter2month[x[4:]] for x in style_exp['date']]



        return  style_exp

    def style_shift_analysis(self):

        #read style exp
        value_exp=self.read_style_exp('value',self.fre,self.start_date)
        size_exp = self.read_style_exp('size', self.fre,self.start_date)

        #standarlize style exp
        value_exp=self.standardliza_by_rank(value_exp,self.value_col,self.bond_col)
        size_exp = self.standardliza_by_rank(size_exp, self.size_col, self.bond_col)

        #shift the exp from rank(entire jj pool) to rank between exp col
        total_w=value_exp[self.value_col].sum(axis=1)
        for col in self.value_col:
            value_exp[col]=value_exp[col]/total_w

        total_w=size_exp[self.size_col].sum(axis=1)
        for col in self.size_col:
            size_exp[col]=size_exp[col]/total_w


        value_exp.set_index('date',inplace=True,drop=True)
        size_exp.set_index('date', inplace=True, drop=True)

        collect_df_size=pd.DataFrame()
        collect_df_value = pd.DataFrame()

        def get_factor_return(style_list,start_date,end_date):

            style=util.list_sql_condition(style_list)

            # get value index ret :
            sql="select zqdm,jyrq,spjg from st_market.t_st_zs_hqql where zqdm in({0}) and jyrq>='{1}' and jyrq<='{2}'"\
                .format(style, start_date+'01',end_date+'31')

            fac_ret_df=hbdb.db2df(sql,db='alluser')
            fac_ret_df['jyrq']=fac_ret_df['jyrq'].astype(str)

            fac_ret_df['ym']=fac_ret_df['jyrq'].str[0:6]
            tempdf=fac_ret_df.drop_duplicates('ym', keep='last')[['jyrq','ym']]
            fac_ret_df=pd.merge(fac_ret_df,tempdf,how='left',on='jyrq').fillna('').drop('ym_x',axis=1)

            # fac_ret_df['jyrq'] = fac_ret_df['ym']
            fac_ret_df.set_index('ym_y', drop=True, inplace=True)

            fac_ret_df['price'] = fac_ret_df['spjg']

            return fac_ret_df

        value_factor_ret=get_factor_return(self.value_col+self.size_col,start_date=value_exp.index[0],end_date=value_exp.index[-1])

        for jjdm in self.jjdm_list:

            print("{} start ".format(jjdm))

            try:

                tempdf =  value_exp[value_exp['jjdm'] == jjdm]

                q_list = tempdf.index.unique().tolist()
                q_list.sort()

                style_shift_df=pd.merge(pd.Series(['Total'] + self.value_col).to_frame('风格类型'),
                self.style_shifting_analysis(
                    tempdf[self.value_col],
                    q_list, self.value_col,
                    t1=0.35 , t2=0.35*0.75 , name='value', jjdm=jjdm,factor_ret=value_factor_ret),how='left',on=['风格类型'])

                style_shift_df = style_shift_df.T
                style_shift_df.columns = style_shift_df.loc['风格类型']
                style_shift_df.drop('风格类型', axis=0, inplace=True)
                style_shift_df['jjdm'] = jjdm
                style_shift_df.reset_index(drop=False, inplace=True)

                collect_df_value = pd.concat([collect_df_value, style_shift_df], axis=0)

                tempdf = size_exp[size_exp['jjdm'] == jjdm]

                q_list = tempdf.index.unique().tolist()
                q_list.sort()

                style_shift_df=pd.merge(pd.Series(['Total'] + self.size_col).to_frame('风格类型'),
                self.style_shifting_analysis(
                    tempdf[self.size_col],
                    q_list, self.size_col,
                    t1=0.2 , t2=0.2*0.75 , name='value', jjdm=jjdm,factor_ret=value_factor_ret),how='left',on=['风格类型'])

                style_shift_df = style_shift_df.T
                style_shift_df.columns = style_shift_df.loc['风格类型']
                style_shift_df.drop('风格类型', axis=0, inplace=True)
                style_shift_df['jjdm'] = jjdm
                style_shift_df.reset_index(drop=False, inplace=True)

                collect_df_size = pd.concat([collect_df_size, style_shift_df], axis=0)


            except Exception as e:
                print(jjdm)
                print(e)


        collect_df_value[['Total']+self.value_col] = collect_df_value[['Total']+self.value_col].astype(
            float)
        collect_df_size[['Total']+self.size_col] = collect_df_size[['Total']+self.size_col].astype(
            float)


        for collect_df in [collect_df_value,collect_df_size]:

            collect_df.rename(columns=self.index_map, inplace=True)

            col_name_list=collect_df.columns.to_list()
            col_name_list.remove('index')
            col_name_list.remove('jjdm')

            collect_df[[x+'_rank' for
                        x in col_name_list
                        ]]=collect_df.groupby('index').rank(method='min')[col_name_list]\
                           /collect_df.groupby('index').count()[col_name_list].loc['切换次数']

            collect_df.rename(columns={'index': '项目名'}, inplace=True)


            collect_df['asofdate']=value_exp.index.max()

            collect_df['fre']=self.fre


            if(len(collect_df.columns)==10):
                # check if already exist
                sql="delete from nav_shift_property_value where asofdate='{0}' and fre='{1}'"\
                    .format(value_exp.index.max(),self.fre)
                localdb.execute(sql)
                collect_df.to_sql('nav_shift_property_value',index=False,if_exists='append',con=localdb)
            else:
                # check if already exist
                sql="delete from nav_shift_property_size where asofdate='{0}' and fre='{1}'"\
                    .format(value_exp.index.max(),self.fre)
                localdb.execute(sql)
                collect_df.to_sql('nav_shift_property_size', index=False, if_exists='append', con=localdb)

        print('Done')

class Fund_ret_analysis:

    def __init__(self,asofdate):
        self.jjdm_list=util.get_potient_mutual_stock_funds(asofdate)

    @staticmethod
    def calculate_bias(indexdf,tickerdf,ret_col):

        joint_df=pd.merge(tickerdf,indexdf,left_index=True,right_index=True)
        available_jjdm_list=tickerdf.groupby('jjdm').count()[tickerdf.groupby('jjdm').count()['rqzh']>=3].index.tolist()
        joint_df=joint_df[joint_df['jjdm'].isin(available_jjdm_list)]
        joint_df['diff']=(joint_df[ret_col+'_x']-joint_df[ret_col+'_y']).abs()

        result=joint_df.groupby('jjdm').mean()['diff'].to_frame('mean')

        joint_df=pd.merge(joint_df,result,how='left',left_on='jjdm',right_index=True)
        #in order to relax the influence of mean on std, change diff to diff-mean
        joint_df['diff_adj']=joint_df['diff']-joint_df['mean']

        result['std']=joint_df.groupby('jjdm').std()['diff_adj']
        result.reset_index(inplace=True,drop=False)

        return result

    def save_index_difference2db(self,asofdate,time_length=3):

        start_date=str(int(asofdate[0:4])-time_length)+asofdate[4:]

        # jj_ret_weekly=get_weekly_jjnav(self.jjdm_list,start_date=start_date,end_date=asofdate)
        # index_ret_weekly=get_weekly_index_ret('885001',start_date=start_date,end_date=asofdate)
        # jj_ret_weekly.set_index('tjrq',inplace=True,drop=True)
        # index_ret_weekly.set_index('tjrq',inplace=True,drop=True)

        jj_ret_monthly,max_yearmonth,min_yearmonth=get_monthly_jjnav(self.jjdm_list,start_date=start_date,end_date=asofdate)
        index_ret_monthly=get_monthly_index_ret('885001',start_date=start_date,end_date=asofdate)
        jj_ret_monthly.set_index('tjyf',inplace=True,drop=True)
        index_ret_monthly.set_index('tjyf',inplace=True,drop=True)

        jj_ret_yearly,max_yearmonth,min_yearmonth=get_yearly_jjnav(self.jjdm_list,start_date=start_date,end_date=asofdate)
        index_ret_yearly=get_yearly_index_ret('885001',start_date=start_date,end_date=asofdate)
        jj_ret_yearly.set_index('tjnf',inplace=True,drop=True)
        index_ret_yearly.set_index('tjnf',inplace=True,drop=True)

        # bias_weekly=self.calculate_bias(index_ret_weekly,jj_ret_weekly,'hb1z')
        bias_monthly=self.calculate_bias(index_ret_monthly, jj_ret_monthly, 'hb1y')
        bias_yearly=self.calculate_bias(index_ret_yearly, jj_ret_yearly, 'hb1n')

        for col in ['mean','std']:
            # bias_weekly[col+'_rank']=bias_weekly[col].abs().rank(method='min')/len(bias_weekly)
            bias_monthly[col + '_rank'] = bias_monthly[col].abs().rank(method='min') / len(bias_monthly)
            bias_yearly[col + '_rank'] = bias_yearly[col].abs().rank(method='min') / len(bias_yearly)

        # bias_weekly.set_index('jjdm',inplace=True,drop=True)
        bias_monthly.set_index('jjdm',inplace=True,drop=True)
        bias_yearly.set_index('jjdm',inplace=True,drop=True)

        # bias_weekly.columns=[x+"_weekly" for x in bias_weekly.columns]
        bias_monthly.columns = [x + "_monthly" for x in bias_monthly.columns]
        bias_yearly.columns = [x + "_yearly" for x in bias_yearly.columns]

        # output_df=pd.merge(bias_monthly,bias_weekly,how='inner',left_index=True,right_index=True)
        output_df=pd.merge(bias_monthly,bias_yearly,how='left',left_index=True,right_index=True)
        output_df['asofdate']=str(jj_ret_monthly.index.max())
        output_df.reset_index(inplace=True,drop=False)

        #check if data already exist
        sql="delete from nav_ret_bias where asofdate='{0}'".format(str(jj_ret_monthly.index.max()))
        localdb.execute(sql)

        output_df.to_sql('nav_ret_bias',con=localdb,index=False,if_exists='append')

        print('Done')

class Manager_volume_hsl_analysis:

    def __init__(self,jjdm_list,asofdate=datetime.datetime.today().strftime('%Y%m%d')):

        self.jjjl_df, \
        self.jjvol_df, \
        self.jjhsl_df=self.get_basic_info(jjdm_list,asofdate)


        #trying to make analysis on fund volumne,hls and ret, trying calculate the correlation between the volume and ret
        #the method is no persuvise and is therefore given up
        # date_list = list(set(self.jjvol_df['jsrq'].astype(str).unique().tolist()+self.jjhsl_df['date'].unique().tolist()))
        # date_list.sort()
        # self.ret_rank=self.get_ret_rank(date_list,jjdm_list)
        #result1=self.volume_with_ret_analysis(self.jjjl_df, self.jjvol_df, self.ret_rank)
        #self.hsl_analysis(self.jjjl_df,self.jjhsl_df)

        self.save_hsl_and_volume2db(self.jjvol_df, self.jjhsl_df)


    @staticmethod
    def get_basic_info(jjdm_list,asofdate):

        start_date=str(int(asofdate[0:4])-10)+asofdate[4:]

        jjdm_con=util.list_sql_condition(jjdm_list)

        sql="select jjdm,ryxm,ryzt,rzrq,lrrq from st_fund.t_st_gm_jjjl where jjdm in ({0}) and ryzw='基金经理' and rzrq>='{1}' "\
            .format(jjdm_con,start_date)
        jjjl_df=hbdb.db2df(sql,db='funduser')

        sql = "select jjdm,jsrq,jjjzc from st_fund.t_st_gm_zcpz where jjdm in ({0}) and jsrq>='{1}'"\
            .format(jjdm_con,start_date)
        jjvol_df = hbdb.db2df(sql, db='funduser')

        sql="select * from factor_hsl where jjdm in ({0}) and date>='{1}'"\
            .format(jjdm_con,start_date)
        jjhsl_df=pd.read_sql(sql,con=localdb)

        return  jjjl_df,jjvol_df,jjhsl_df

    @staticmethod
    def get_ret_rank(date_list,jjdm_list):

        jjdm_con = util.list_sql_condition(jjdm_list)
        date_con = util.list_sql_condition(date_list)

        sql="""select jjdm,JZRQ,pmnpyj,slnpyj,pmnpej,slnpej 
        from st_fund.t_st_gm_rqjhbpm 
        where jjdm in ({0}) and zblb=2101 and JZRQ in ({1}) and pmnpej!=99999"""\
            .format(jjdm_con,date_con)

        ret_rank_month=hbdb.db2df(sql,db='funduser')

        sql="""select jjdm,JZRQ,pmnpyj,slnpyj,pmnpej,slnpej 
        from st_fund.t_st_gm_rqjhbpm 
        where jjdm in ({0}) and zblb=2103 and JZRQ in ({1}) and pmnpej!=99999"""\
            .format(jjdm_con,date_con)

        ret_rank_quarter=hbdb.db2df(sql,db='funduser')

        ret_rank=pd.merge(ret_rank_month,ret_rank_quarter,how='inner',on=['jjdm','JZRQ'])

        ret_rank['yj_m']=ret_rank['pmnpyj_x']/ret_rank['slnpyj_x']
        ret_rank['yj_q'] = ret_rank['pmnpyj_y'] / ret_rank['slnpyj_y']
        ret_rank['ej_m'] = ret_rank['pmnpej_x'] / ret_rank['slnpej_x']
        ret_rank['ej_q'] = ret_rank['pmnpej_y'] / ret_rank['slnpej_y']

        # ret_rank.rename(columns={'pmnpyj_x':'pmnpyj_m','slnpyj_x':'slnpyj_m'
        #     ,'pmnpyj_y':'pmnpyj_q','slnpyj_y':'slnpyj_q','pmnpej_x':'pmnpej_m','slnpej_x':'slnpej_m',
        #                          'pmnpej_y':'pmnpej_q','slnpej_y':'slnpej_q'},inplace=True)

        return ret_rank[['jjdm','JZRQ','yj_m','yj_q','ej_m','ej_q']]

    @staticmethod
    def volume_with_ret_analysis(jjjl_df,jjvol_df,ret_rank):

        data_df=pd.merge(jjvol_df,ret_rank,how='inner',left_on=['jjdm','jsrq'],right_on=['jjdm','JZRQ'])

        fin_df=pd.DataFrame()
        manager_list=[]
        jjdm_list=[]
        ej_m_cor=[]
        ej_q_cor=[]

        for manager in jjjl_df['ryxm'].unique():
            tempdf=jjjl_df[jjjl_df['ryxm']==manager]

            for jjdm in tempdf['jjdm'].unique():
                tempdf3=tempdf[tempdf['jjdm']==jjdm]
                tempdf2=pd.DataFrame()
                for i in range(len(tempdf3)):

                    tempdf2=pd.concat([tempdf2,data_df[(data_df['jjdm'] == tempdf3.iloc[i]['jjdm'])
                                       &(data_df['JZRQ']>=tempdf3.iloc[i]['rzrq'])
                                       &(data_df['JZRQ']<=tempdf3.iloc[i]['lrrq'])]])


                cor=tempdf2[['jjjzc', 'yj_m', 'yj_q', 'ej_m', 'ej_q']].corr()['jjjzc'].loc[['ej_m','ej_q']]
                jjdm_list.append(jjdm)
                manager_list.append(manager)
                ej_q_cor.append(cor['ej_q'])
                ej_m_cor.append(cor['ej_m'])

        fin_df['manager']=manager_list
        fin_df['jjdm'] = jjdm_list
        fin_df['ej_m_cor'] = ej_m_cor
        fin_df['ej_q_cor'] = ej_q_cor

        return  fin_df

    @staticmethod
    def hsl_analysis(jjhsl_df, jjvol_df):

        print('')

    @staticmethod
    def save_hsl_and_volume2db(jjvol_df,jjhsl_df):

        jjvol_df['jsrq']=jjvol_df['jsrq'].astype(str)
        jjhsl_df.drop('count',axis=1,inplace=True)
        joint_df=pd.merge(jjvol_df,jjhsl_df,how='inner',left_on=['jjdm','jsrq'],right_on=['jjdm','date'])

        joint_df['jjjzc_vs_hsl']=joint_df['jjjzc']/joint_df['hsl']/1000000
        joint_df=pd.concat([joint_df,joint_df.groupby('date').rank(method='min')['jjjzc_vs_hsl'].to_frame('rank')],axis=1)
        joint_df=pd.merge(joint_df,
                          joint_df.groupby('date', as_index=False).count()[['date', 'jjdm']].rename(columns={'jjdm':'count'}),
                          how='left',on='date')
        joint_df['rank']=joint_df['rank']/joint_df['count']
        joint_df['asofdate']=joint_df['date'].max()

        #check if data already exist
        # sql="delete from nav_hsl_vs_volume where asofdate='{0}'".format(joint_df['date'].max())
        # localdb.execute(sql)

        joint_df[['jjdm','date','rank','jjjzc','hsl','asofdate']].to_sql('nav_hsl_vs_volume',index=False,if_exists='append',con=localdb)

        # tempdf_s=joint_df[joint_df['rank']<=0.25]
        # tempdf_s['type']='volume_small&hsl_big'
        # tempdf_b=joint_df[joint_df['rank']>=0.75]
        # tempdf_b['type'] = 'volume_big&hsl_small'
        #
        # result=pd.concat([tempdf_s,tempdf_b],axis=0)
        #
        # return  result

class Theme_analysis():
    def __init__(self, jjdm_list, fre, asofdate=datetime.datetime.today().strftime('%Y%m%d'), time_length=3):
        # 时间区间
        start_year = str(int(asofdate[0:4]) - time_length)
        if fre == 'M':
            start_date = start_year + asofdate[4:6]
        else:
            if asofdate[4:6] <= '03':
                Q = 1
            elif asofdate[4:6] > '03' and asofdate[4:6] <= '06':
                Q = 2
            elif asofdate[4:6] > '06' and asofdate[4:6] <= '09':
                Q = 3
            elif asofdate[4:6] > '09' and asofdate[4:6] <= '12':
                Q = 4
            start_date = start_year + "Q" + str(Q)
        self.start_date = start_date
        self.fre = fre
        self.asofdate = asofdate
        self.val_date = self.get_jj_valuation_date(jjdm_list, asofdate)
        self.jjdm_list = jjdm_list

        # 指数代码及数据
        # todo：采用2014版申万一级行业分类，采掘行业数据停更问题
        # industry_info = HBDB().read_industry_info()
        # industry_info = industry_info[(industry_info['hyhfbz'] == '2') & (industry_info['fljb'] == '1') & (industry_info['sfyx'] == '1')]
        self.industry_col = ['801010','801030','801040','801050','801080','801110',
                              '801120','801130','801140','801150','801160','801170',
                              '801180','801200','801210','801230','801710','801720',
                              '801730','801740','801750','801760','801770','801780',
                              '801790','801880','801890','801950','801960','801970','801980']
        self.bond_col = ['CBA00301']
        self.index_data = HBDB().read_index_daily_k_given_date_and_indexs(start_year + '0101', self.industry_col + self.bond_col)
        # self.index_data.to_hdf('E:/GitFolder/hbshare/fe/xwq/data/index_data.hdf', key='table', mode='w')
        # self.index_data = pd.read_hdf('E:/GitFolder/hbshare/fe/xwq/data/index_data.hdf', key='table')
        self.index_data = self.index_data.rename(columns={'zqdm': 'INDEX_SYMBOL', 'zqmc': 'INDEX_NAME', 'jyrq': 'TRADE_DATE', 'spjg': 'CLOSE_INDEX', 'ltsz': 'NEG_MARKET_VALUE'})
        self.index_data = self.index_data[['INDEX_SYMBOL', 'INDEX_NAME', 'TRADE_DATE', 'CLOSE_INDEX', 'NEG_MARKET_VALUE']]
        self.index_map = self.index_data[['INDEX_SYMBOL', 'INDEX_NAME']].set_index('INDEX_SYMBOL')['INDEX_NAME'].to_dict()

        # 主题行业对应关系
        self.theme_col = ['大金融', '消费', 'TMT', '周期', '制造']
        self.theme_industry = dict(zip(self.theme_col,
                             [['银行','非银金融','房地产'],
                              ['食品饮料','家用电器','医药生物','社会服务','农林牧渔','商贸零售','美容护理'],
                              ['通信','计算机','电子','传媒','国防军工'],
                              ['钢铁','有色金属','建筑装饰','建筑材料','基础化工','石油石化','煤炭','环保','公用事业'],
                              ['交通运输','机械设备','汽车','纺织服饰','轻工制造','电力设备']
                              ]
                             ))

        # self.theme_industry = {
        #     '大金融': ['银行', '非银金融', '房地产'],
        #     '消费': ['家用电器', '食品饮料', '医药生物', '休闲服务', '农林牧渔', '商业贸易', '纺织服装'],
        #     'TMT': ['电子', '计算机', '传媒', '通信'],
        #     '周期': ['钢铁', '采掘', '有色金属', '化工', '建筑装饰', '建筑材料'],
        #     '制造': ['公用事业', '交通运输', '机械设备', '汽车', '电气设备', '轻工制造'],
        # }
        # self.theme_col = list(self.theme_industry.keys())

        # 基金净值
        # self.fund_nav = HBDB().read_fund_nav_given_date_and_codes(start_year + '0101', self.jjdm_list)
        # self.fund_nav.to_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/fund_nav.hdf', key='table', mode='w')
        # self.fund_nav = pd.read_hdf('D:/Git/hbshare/hbshare/fe/xwq/data/fund_nav.hdf', key='table')
        # self.fund_nav = self.fund_nav.rename(columns={'jjdm': 'FUND_CODE', 'jzrq': 'TRADE_DATE', 'jjjz': 'NAV', 'ljjz': 'CUM_NAV'})
        # self.fund_nav = self.fund_nav[['FUND_CODE', 'TRADE_DATE', 'NAV', 'CUM_NAV']]
        # self.fund_nav_adj = HBDB().read_fund_nav_adj_given_date_and_codes(start_year + '0101', self.jjdm_list)
        # self.fund_nav_adj.to_hdf('E:/GitFolder/hbshare/fe/xwq/data/fund_nav_adj.hdf', key='table', mode='w')
        self.fund_nav_adj = pd.read_hdf('E:/GitFolder/hbshare/fe/xwq/data/fund_nav_adj.hdf', key='table')
        self.fund_nav_adj = self.fund_nav_adj.rename(columns={'jjdm': 'FUND_CODE', 'jzrq': 'TRADE_DATE', 'fqdwjz': 'ADJ_NAV', 'hbdr': 'RET', 'hbfh': 'CUM_DIV_RET', 'hbcl': 'SOFAR_RET'})
        self.fund_nav_adj = self.fund_nav_adj[['FUND_CODE', 'TRADE_DATE', 'ADJ_NAV', 'RET', 'CUM_DIV_RET', 'SOFAR_RET']]

    def ols_for_group(self, arr):
        y_col = arr.columns[0]
        x_col = arr.columns.tolist()
        x_col.remove(y_col)
        X = arr[x_col].values
        Y = arr[y_col].values

        X = (X - X.mean()) / X.std(ddof=1)

        model = LR(fit_intercept=True)
        model.fit(X, Y)
        return model.coef_.tolist()

    def ols_for_group_with_cons(self, arr):
        y_col = arr.columns[0]
        x_col = arr.columns.tolist()
        x_col.remove(y_col)
        X = arr[x_col].values
        Y = arr[y_col].values

        X = (X - X.mean()) / X.std(ddof=1)

        def func(A):
            ls = 0.5 * (Y - np.dot(X, A)) ** 2
            result = np.sum(ls)
            return result

        def g1(A):
            return np.sum(A)

        def g2(A):
            return 1 - np.sum(A)

        constraints = [{'type': 'ineq', 'fun': g1},
                       {'type': 'eq', 'fun': g2}]
        bounds = [(0, 1)] * np.shape(X)[1]
        w = np.zeros(np.shape(X)[1])
        res = minimize(func, w,
                       bounds=bounds,
                       constraints=constraints,
                       method='SLSQP')
        # constraints = ({'type': 'ineq', 'fun': g1},
        #                {'type': 'eq', 'fun': g2})
        # bounds = [(0, 1)] * np.shape(X)[1]
        # res = shgo(func,
        #            bounds=bounds,
        #            constraints=constraints)
        return res.x.tolist()

    @staticmethod
    def read_jj_style_exp(jjdm_list, type, fre, start_date):
        jjdm_con = util.list_sql_condition(jjdm_list)
        sql = "select * from nav_{0}_exposure where jjdm in ({1}) and fre='{2}' and date>='{3}'".format(type, jjdm_con, fre, start_date)
        expdf = pd.read_sql(sql, con=localdb)
        return expdf

    @staticmethod
    def cal_style_shift_ratio(df, style_col):
        df = df.copy()
        # calculate the total change in styles
        df['change'] = df[style_col].diff().abs().sum(axis=1)
        # calculate the average style exp between two dates
        df['avg_exp'] = df[style_col].sum(axis=1).rolling(2).mean()
        # calculate shift ratio
        df['shift_ratio'] = df['change'] / df['avg_exp']
        return df['shift_ratio'].values

    @staticmethod
    def cal_style_centralization_level(df, style_col, num1=1, num2=2):
        df = df.set_index('date')[style_col]
        outputdf = pd.DataFrame(index=df.index,columns=['c_level'])
        for i in range(len(df)):
            outputdf.iloc[i]['c_level']=(df.iloc[i].sort_values()[-1*num1:].sum()+df.iloc[i].sort_values()[-1*num2:].sum())/2/df.iloc[i].sum()
        return outputdf.mean()[0]

    @staticmethod
    def get_jj_valuation_date(jjdm_list, asofdate):
        jjdm_con = util.list_sql_condition(jjdm_list)
        # read jjjl info
        sql = "select jjdm,ryxm,rydm,rzrq from st_fund.t_st_gm_jjjl where ryzt='-1' and jjdm in ({0})".format(jjdm_con)
        jj_val_date = hbdb.db2df(sql, db='funduser')
        # for jj with multi managers,take the one with longer staying in this jj
        # jj_val_date = jj_val_date.sort_values('rzrq')
        # jj_val_date.drop_duplicates('jjdm', keep='first', inplace=True)
        jj_val_date = jj_val_date.sort_values(['jjdm', 'rzrq']).drop_duplicates('jjdm', keep='first')
        # remove jj with manager managing no longer than 1.5years
        # last_oneandhalfyear = (datetime.datetime.strptime(asofdate, '%Y%m%d')
        #                        -datetime.timedelta(days=560)).strftime('%Y%m%d')
        # jj_val_date['rzrq']=jj_val_date['rzrq'].astype(str)
        # jj_val_date=jj_val_date[jj_val_date['rzrq']<=last_oneandhalfyear]
        return jj_val_date[['jjdm', 'rzrq', 'rydm']]

    def fit_theme_index(self, theme_industry, index_data):
        theme_ret_dic = {}
        for theme in theme_industry.keys():
            print('dealing {}...'.format(theme))
            theme_index_data = index_data[index_data['INDEX_NAME'].isin(theme_industry[theme])]
            theme_index_price = theme_index_data.pivot(index='TRADE_DATE', columns='INDEX_NAME', values='CLOSE_INDEX').sort_index().fillna(method='ffill')
            theme_index_ret = theme_index_price.pct_change()
            theme_index_nmv = theme_index_data.pivot(index='TRADE_DATE', columns='INDEX_NAME', values='NEG_MARKET_VALUE').sort_index().fillna(method='ffill')
            theme_index_weight = theme_index_nmv.apply(lambda x: x / x.sum(), axis=1)
            theme_ret = (theme_index_ret * theme_index_weight).sum(axis=1)
            theme_ret_dic[theme] = theme_ret
            print('finish dealing {}!'.format(theme))
        theme_ret = pd.DataFrame.from_dict(theme_ret_dic)

        return theme_ret

    def get_theme_exposure(self, index_data, nav):
        theme_ret = self.fit_theme_index(self.theme_industry, index_data)
        bond_price = index_data[index_data['INDEX_SYMBOL'].isin(self.bond_col)]
        bond_price = bond_price.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX').sort_index().fillna(method='ffill')
        bond_ret = bond_price.pct_change()
        theme_ret = pd.concat([theme_ret, bond_ret], axis=1).fillna(0.0)

        if self.fre == 'M':
            def timezone_transform(olsdf):
                olsdf['yearmonth'] = [str(x)[0:6] for x in olsdf.index]
                return olsdf
        else:
            def timezone_transform(olsdf):
                olsdf['yearmonth'] = ''
                olsdf.loc[olsdf.index.astype(str).str[4:6] <= '03', 'yearmonth'] = 'Q1'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '06') & (olsdf.index.astype(str).str[4:6] > '03'), 'yearmonth'] = 'Q2'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '09') & (olsdf.index.astype(str).str[4:6] > '06'), 'yearmonth'] = 'Q3'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '12') & (olsdf.index.astype(str).str[4:6] > '09'), 'yearmonth'] = 'Q4'
                olsdf['yearmonth'] = olsdf.index.astype(str).str[0:4] + olsdf['yearmonth']
                return olsdf

        theme_exp_df = pd.DataFrame()
        for idx, jjdm in enumerate(self.jjdm_list):
            jj_ret = nav[nav['FUND_CODE'] == jjdm][['TRADE_DATE', 'RET']].set_index('TRADE_DATE').rename(columns={'RET': jjdm})
            olsdf = pd.merge(jj_ret, theme_ret, how='inner', left_index=True, right_index=True)
            olsdf = timezone_transform(olsdf)
            tempdf = olsdf[olsdf[[jjdm] + self.theme_col + self.bond_col].notnull().sum(axis=1) == (len(self.theme_col) + 2)]
            tempdf = tempdf.groupby('yearmonth')[[jjdm] + self.theme_col + self.bond_col].apply(self.ols_for_group_with_cons).to_frame('exp')
            for i, col in enumerate(self.theme_col + self.bond_col):
                tempdf[col] = [exp[i] for exp in tempdf['exp']]
            tempdf.drop('exp', inplace=True, axis=1)
            tempdf['jjdm'] = jjdm
            theme_exp_df = pd.concat([theme_exp_df, tempdf], axis=0)
            print('[{}/{}:{}] Done!'.format(idx, len(self.jjdm_list), jjdm))
        theme_exp_df = theme_exp_df.reset_index().rename(columns={'yearmonth': 'date'})
        theme_exp_df['fre'] = self.fre
        theme_exp_df.to_sql('nav_theme_exposure', index=False, if_exists='append', con=localdb)
        return

    def get_theme_property(self, style_df, style_col, method='rank'):
        if self.fre == 'M':
            def timezone_transform(olsdf):
                olsdf['yearmonth'] = [str(x)[0:6] for x in olsdf.index]
                return olsdf
        else:
            def timezone_transform(olsdf):
                olsdf['yearmonth'] = ''
                olsdf.loc[olsdf.index.astype(str).str[4:6] <= '03', 'yearmonth'] = 'Q1'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '06') & (olsdf.index.astype(str).str[4:6] > '03'), 'yearmonth'] = 'Q2'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '09') & (olsdf.index.astype(str).str[4:6] > '06'), 'yearmonth'] = 'Q3'
                olsdf.loc[(olsdf.index.astype(str).str[4:6] <= '12') & (olsdf.index.astype(str).str[4:6] > '09'), 'yearmonth'] = 'Q4'
                olsdf['yearmonth'] = olsdf.index.astype(str).str[0:4] + olsdf['yearmonth']
                return olsdf
        self.val_date = timezone_transform(self.val_date.set_index('rzrq'))

        if (method == 'robust'):
            from sklearn.preprocessing import RobustScaler
            rs = RobustScaler()
            style_df[style_col] = rs.fit_transform(style_df[style_col].values)
        else:
            style_df[style_col] = style_df.groupby('date').rank(method='min')[style_col]
            style_df = pd.merge(style_df, style_df.groupby('date').count()['jjdm'].to_frame('count'), left_on='date', right_index=True)
            for col in style_col:
                style_df[col] = style_df[col] / style_df['count']
        asofdate = style_df['date'].max()
        style_property_df = pd.DataFrame()
        temp = style_df.groupby('jjdm').min()['date']
        new_jjdm_list = temp[temp <= self.start_date].index.tolist()
        new_jjdm_list.sort()
        style_property_df['jjdm'] = new_jjdm_list
        for idx, jjdm in enumerate(new_jjdm_list):
            # check if manager changed during the time zone
            tempdf = style_df[style_df['jjdm'] == jjdm]
            manager_change = str(str(self.val_date[self.val_date['jjdm'] == jjdm]['yearmonth'].values[0])[0:6] > self.start_date) if len(self.val_date[self.val_date['jjdm'] == jjdm]) > 0 else ''
            tempdf['shift_ratio'] = self.cal_style_shift_ratio(tempdf, style_col)
            centralization = self.cal_style_centralization_level(tempdf, style_col, 1, 2)
            # centralization = (tempdf[style_col].std(axis=1) / tempdf[style_col].mean(axis=1)).mean()
            style_property_df.loc[style_property_df['jjdm'] == jjdm, 'shift_ratio'] = tempdf['shift_ratio'].mean()
            style_property_df.loc[style_property_df['jjdm'] == jjdm, 'centralization'] = centralization
            for col in style_col:
                style_property_df.loc[style_property_df['jjdm'] == jjdm, col + '_mean'] = tempdf[col].mean()
            style_property_df.loc[style_property_df['jjdm'] == jjdm, 'manager_change'] = manager_change
            print('[{}/{}:{}] Done!'.format(idx, len(new_jjdm_list), jjdm))
        rank_col = ['shift_ratio', 'centralization'] + [col + '_mean' for col in style_col]
        style_property_df[[x + '_rank' for x in rank_col]] = style_property_df[rank_col].rank(method='min') / len(style_property_df)
        style_property_df['asofdate'] = asofdate
        return style_property_df


    def save_theme_property2localdb(self):
        self.get_theme_exposure(self.index_data, self.fund_nav_adj)

        # sql = "select distinct asofdate from nav_style_property_value where fre='{0}' and by_manager='{1}' " \
        #     .format(self.fre, 'True')
        # asofdate_list = pd.read_sql(sql, con=localdb)['asofdate'].values.tolist()
        #
        # if (self.asofdate in asofdate_list):
        #     sql = "delete from nav_style_property_value where asofdate='{0}' and fre-'{1}' and by_manager='{2}'" \
        #         .format(self.asofdate, self.fre, 'True' + str(self.consistant_date))
        #     localdb.excute(sql)

        value_df = self.get_theme_property(self.read_jj_style_exp(self.jjdm_list, 'theme', self.fre, self.start_date), self.theme_col, method='rank')
        value_df['fre'] = self.fre
        value_df.to_sql('nav_style_property_theme', index=False, con=localdb, if_exists='append')
        return

class Fund_return_analysis:


    @staticmethod
    def hurst_index(asofdate,if_prv=False):
        import hurst
        hurst_index_df=pd.DataFrame()

        if(if_prv):
            jjdm_list = ['']
        else:
            jjdm_list = util.get_mutual_stock_funds(asofdate)

        # jjdm_list=pd.read_sql("select * from core_pool_history where asofdate='202203'",
        #                               con=localdb)['基金代码'].tolist()
        #jjdm_list=['001892']

        #get jj nav
        jj_nav=get_daily_jjnav(jjdm_list,start_date=str((int(asofdate[0:4])-3))+asofdate[4:]
                               ,end_date=asofdate)

        # get jj log ret
        jj_nav['log_ret']=np.log(jj_nav.groupby('jjdm').pct_change()['jjjz'] + 1)
        #
        jjdm_h=[]
        jjdm_c=[]

        for jjdm in jjdm_list:

            print(jjdm)

            y_list = []
            x_list = []
            c_list = []


            tempdf=jj_nav[jj_nav['jjdm']==jjdm]
            tempdf=tempdf.iloc[1:]
            if(len(tempdf)<=250):
                jjdm_h.append(0.5)
                jjdm_c.append(0)
                continue

            result=hurst.compute_Hc(tempdf['log_ret'].values,simplified=False,kind ='change',min_window=7,max_window=250)
            # for tree_length in [7,30,90,125,250]:
            #
            #     tree_num=int(np.floor(len(tempdf)/tree_length))
            #
            #     ra_sa_list=[]
            #
            #     for i in range(tree_num):
            #         tempdfa=tempdf[i*tree_length:(i+1)*tree_length]
            #         xka_list=[]
            #         ea=tempdfa['log_ret'].mean()
            #         for j in range(len(tempdfa)):
            #             xka_list.append((tempdfa['log_ret'].iloc[0:j]-ea).sum())
            #
            #         ra=max(xka_list)-min(xka_list)
            #         sa=tempdfa['log_ret'].std()
            #         ra_sa_list.append(ra/sa)
            #
            #     rsn=pd.Series(ra_sa_list).mean()
            #     y_list.append(np.log10(rsn))
            #     x_list.append(np.log10(tree_num))
            #     c_list.append(0)
            #
            # ols_df=pd.DataFrame()
            # ols_df['y']=y_list
            # ols_df['x'] = x_list
            # ols_df['c'] = c_list
            # result = util.my_general_linear_model_func2(ols_df[['x','c']].values,ols_df['y'].values,
            #                                             lb=[0,0],ub=[1,np.log10(9999)])
            jjdm_h.append(result[0])
            jjdm_c.append(result[1])

        hurst_index_df['jjdm']=jjdm_list
        hurst_index_df['H']=jjdm_h
        hurst_index_df['C']=jjdm_c
        hurst_index_df['asofdate']=asofdate

        sql="delete from nav_hurst_index where asofdate='{0}'".format(asofdate)
        localdb.execute(sql,con=localdb)

        hurst_index_df.to_sql('nav_hurst_index',con=localdb,if_exists='append',index=False)

    @staticmethod
    def return_rank_analysis(asofdate,if_prv=False):

        if(if_prv):
            jjdm_list = ['']
        else:
            jjdm_list = util.get_mutual_stock_funds(asofdate)


        jj_nav=get_daily_jjnav(jjdm_list,start_date=str((int(asofdate[0:4])-3))+asofdate[4:]
                               ,end_date=asofdate)
        # get jj log ret
        jj_nav['log_ret']=np.log(jj_nav.groupby('jjdm').pct_change()['jjjz'] + 1)

        # get index nav
        index_nav=get_daily_indexnav(['885001'],start_date=str((int(asofdate[0:4])-3))+asofdate[4:]
                               ,end_date=asofdate)
        #get index log ret
        index_nav['log_ret'] = np.log(index_nav['spjg'].pct_change() + 1)

        #calculate the latest year Momentum
        moment=pd.merge(jj_nav[jj_nav['jzrq']>=int(str((int(asofdate[0:4])-1))+asofdate[4:])]
                        ,index_nav[index_nav['jyrq']>=int(str((int(asofdate[0:4])-1))+asofdate[4:])][['jyrq','log_ret']],how='left',left_on='jzrq',right_on='jyrq')
        moment['ext_ret']=moment['log_ret_x']-moment['log_ret_y']
        moment=moment.groupby('jjdm')['ext_ret'].sum().to_frame('moment')
        moment['moment_rank']=moment['moment'].rank(method='min')/len(moment)


        #sharp ratio
        sql="select jjdm,nhzbnp from st_fund.t_st_gm_zqjxpbl where tjrq>='{1}' and tjrq<='{2}' and zblb='2203' and jjdm in ({0}) and zbnp !=99999"\
            .format(util.list_sql_condition(jjdm_list),asofdate[0:4]+('0'+str(int(asofdate[4:6])-1))[-2:]+asofdate[6:],asofdate)
        other_ret_ratio=hbdb.db2df(sql,db='funduser')\
            .drop_duplicates(['jjdm'],keep='last').rename(columns={'nhzbnp':'sharp_ratio'})
        other_ret_ratio['sharp_ratio_rank']= other_ret_ratio['sharp_ratio'].rank(method='min')/len(other_ret_ratio)

        #downwards ratio
        sql="select jjdm,nhzbnp from st_fund.t_st_gm_zqjxxfx where tjrq>='{1}' and tjrq<='{2}' and zblb='2203' and jjdm in ({0}) and zbnp !=99999"\
            .format(util.list_sql_condition(jjdm_list),asofdate[0:4]+('0'+str(int(asofdate[4:6])-1))[-2:]+asofdate[6:],asofdate)
        other_ret_ratio=pd.merge(other_ret_ratio, hbdb.db2df(sql,db='funduser')\
            .drop_duplicates(['jjdm'],keep='last').rename(columns={'nhzbnp':'downwards_ratio'}),how='left',on='jjdm')
        other_ret_ratio['downwards_ratio_rank']= other_ret_ratio['downwards_ratio'].rank(method='min')/len(other_ret_ratio)
        #sortino  ratio
        sql="select jjdm,nhzbnp from st_fund.t_st_gm_zqjstn where tjrq>='{1}' and tjrq<='{2}' and zblb='2203' and jjdm in ({0}) and zbnp !=99999"\
            .format(util.list_sql_condition(jjdm_list),asofdate[0:4]+('0'+str(int(asofdate[4:6])-1))[-2:]+asofdate[6:],asofdate)
        other_ret_ratio=pd.merge(other_ret_ratio, hbdb.db2df(sql,db='funduser')\
            .drop_duplicates(['jjdm'],keep='last').rename(columns={'nhzbnp':'sortino_ratio'}),how='left',on='jjdm')
        other_ret_ratio['sortino_ratio_rank'] = other_ret_ratio['sortino_ratio'].rank(method='min') / len(
            other_ret_ratio)

        #max draw back
        sql="select jjdm,zbnp from st_fund.t_st_gm_rqjzdhc where jzrq>='{1}' and jzrq<='{2}' and zblb='2203' and jjdm in ({0}) and zbnp !=99999"\
            .format(util.list_sql_condition(jjdm_list),asofdate[0:4]+('0'+str(int(asofdate[4:6])-1))[-2:]+asofdate[6:],asofdate)
        other_ret_ratio=pd.merge(other_ret_ratio, hbdb.db2df(sql,db='funduser')\
            .drop_duplicates(['jjdm'],keep='last').rename(columns={'zbnp':'max_drawback'}),how='left',on='jjdm')
        other_ret_ratio['max_drawback_rank'] = other_ret_ratio['max_drawback'].rank(method='min') / len(
            other_ret_ratio)

        #calmark
        sql="select jjdm,zbnp from st_fund.t_st_gm_rqjkmbl where jzrq>='{1}' and jzrq<='{2}' and zblb='2203' and jjdm in ({0}) and zbnp !=99999"\
            .format(util.list_sql_condition(jjdm_list),asofdate[0:4]+('0'+str(int(asofdate[4:6])-1))[-2:]+asofdate[6:],asofdate)
        other_ret_ratio=pd.merge(other_ret_ratio, hbdb.db2df(sql,db='funduser')\
            .drop_duplicates(['jjdm'],keep='last').rename(columns={'zbnp':'calmark_ratio'}),how='left',on='jjdm')
        other_ret_ratio['calmark_ratio_rank'] = other_ret_ratio['calmark_ratio'].rank(method='min') / len(
            other_ret_ratio)

        #Treynor ratio
        sql="select jjdm,zbnp from st_fund.t_st_gm_zqjtlnbl where tjrq>='{1}' and tjrq<='{2}' and zblb='2203' and jjdm in ({0}) and zbnp !=99999"\
            .format(util.list_sql_condition(jjdm_list),asofdate[0:4]+('0'+str(int(asofdate[4:6])-1))[-2:]+asofdate[6:],asofdate)
        other_ret_ratio=pd.merge(other_ret_ratio, hbdb.db2df(sql,db='funduser')\
            .drop_duplicates(['jjdm'],keep='last').rename(columns={'zbnp':'treynor_ratio'}),how='left',on='jjdm')
        other_ret_ratio['treynor_ratio_rank'] = other_ret_ratio['treynor_ratio'].rank(method='min') / len(
            other_ret_ratio)

        last_3years_indexret=np.power( (1+np.log(index_nav['spjg'].iloc[-1]/index_nav['spjg'].iloc[0])),1/3)-1
        last_6month_date=index_nav.iloc[int(len(index_nav)/6*5)]['jyrq']
        last_6month_index_ret=np.power(1+ np.log(index_nav['spjg'].iloc[-1]/index_nav['spjg'].iloc[int(len(index_nav)/6*5)]),2)-1

        jj_nav.reset_index(drop=True,inplace=True)


        jj_nav['3years_extret']=np.power(np.log(jj_nav[(jj_nav['jzrq']==index_nav['jyrq'].min())
                                           |(jj_nav['jzrq']==index_nav['jyrq'].max())]
                                    .groupby('jjdm').pct_change()['jjjz']+1)+1,1/3)-1-last_3years_indexret
        jj_nav['6month_extret']=np.power(np.log(jj_nav[(jj_nav['jzrq']==last_6month_date)
                                           |(jj_nav['jzrq']==index_nav['jyrq'].max())]
                                    .groupby('jjdm').pct_change()['jjjz']+1)+1,2)-1-last_6month_index_ret

        jj_nav['ret_regress']=jj_nav['3years_extret']-jj_nav['6month_extret']
        jj_nav['ret_regress']=jj_nav['ret_regress'].rank(method='min')/len(jj_nav[jj_nav['ret_regress'].notnull()])
        regress_rank = jj_nav[jj_nav['ret_regress'].notnull()][['jjdm', 'ret_regress']]

        jj_nav['month']=jj_nav['jzrq'].astype(str).str[4:6]
        jj_nav['ym']=jj_nav['jzrq'].astype(str).str[0:6]


        #get the monthly nav performance
        jj_nav_rank_month=jj_nav.drop_duplicates(['jjdm', 'ym'], keep='last')
        jj_nav_rank_month['log_ret']=np.log(jj_nav_rank_month.groupby('jjdm')['jjjz'].pct_change()+1)

        jj_nav_rank_month=pd.merge(jj_nav_rank_month,
                                   jj_nav_rank_month.groupby('jzrq').count()['jjdm'].to_frame('count'),on='jzrq',how='inner')
        jj_nav_rank_month['log_ret_rank']=jj_nav_rank_month.groupby('jzrq').rank(method='min')['log_ret']/jj_nav_rank_month['count']
        outputdf=pd.merge(jj_nav_rank_month.groupby('jjdm').mean()['log_ret_rank'].to_frame('month_rank_mean'),
                 jj_nav_rank_month.groupby('jjdm').std()['log_ret_rank'].to_frame('month_rank_std'),how='left',on='jjdm')
        outputdf['month_rank_std']=outputdf['month_rank_std'].rank(method='min')/len(outputdf)

        # get the quarterly nav performance
        jj_nav_rank_quarter=jj_nav[(jj_nav['month']=='03')|(jj_nav['month']=='06')|(jj_nav['month']=='09')|(jj_nav['month']=='12')].drop_duplicates(['jjdm', 'ym'], keep='last')
        jj_nav_rank_quarter['log_ret']=np.log(jj_nav_rank_quarter.groupby('jjdm')['jjjz'].pct_change()+1)

        jj_nav_rank_quarter=pd.merge(jj_nav_rank_quarter,
                                   jj_nav_rank_quarter.groupby('jzrq').count()['jjdm'].to_frame('count'),on='jzrq',how='inner')
        jj_nav_rank_quarter['log_ret_rank']=jj_nav_rank_quarter.groupby('jzrq').rank(method='min')['log_ret']/jj_nav_rank_quarter['count']
        outputdf=pd.merge(outputdf,pd.merge(jj_nav_rank_quarter.groupby('jjdm').mean()['log_ret_rank'].to_frame('quarter_rank_mean'),
                 jj_nav_rank_quarter.groupby('jjdm').std()['log_ret_rank'].to_frame('quarter_rank_std'),how='left',on='jjdm'),how='inner',on='jjdm')

        outputdf['quarter_rank_std']=outputdf['quarter_rank_std'].rank(method='min')/len(outputdf)


        # get the half_yearly nav performance
        jj_nav_rank_hy=jj_nav[(jj_nav['month']=='06')|(jj_nav['month']=='12')].drop_duplicates(['jjdm', 'ym'], keep='last')
        jj_nav_rank_hy['log_ret']=np.log(jj_nav_rank_hy.groupby('jjdm')['jjjz'].pct_change()+1)

        jj_nav_rank_hy=pd.merge(jj_nav_rank_hy,
                                   jj_nav_rank_hy.groupby('jzrq').count()['jjdm'].to_frame('count'),on='jzrq',how='inner')
        jj_nav_rank_hy['log_ret_rank']=jj_nav_rank_hy.groupby('jzrq').rank(method='min')['log_ret']/jj_nav_rank_hy['count']
        outputdf=pd.merge(outputdf,pd.merge(jj_nav_rank_hy.groupby('jjdm').mean()['log_ret_rank'].to_frame('hy_rank_mean'),
                 jj_nav_rank_hy.groupby('jjdm').std()['log_ret_rank'].to_frame('hy_rank_std'),how='left',on='jjdm'),how='inner',on='jjdm')

        outputdf['hy_rank_std']=outputdf['hy_rank_std'].rank(method='min')/len(outputdf)

        # get the yearly nav performance
        jj_nav['year']=jj_nav['jzrq'].astype(str).str[0:4]
        jj_nav_rank_yearly=pd.merge(jj_nav.groupby(['jjdm','year']).max()['jzrq'].reset_index().rename(columns={'jzrq':'year_end'}),
                                     jj_nav.groupby(['jjdm','year']).min()['jzrq'].reset_index().rename(columns={'jzrq':'year_start'}),how='inner',
                                                                                                                                         on=['jjdm','year'])
        jj_nav_rank_yearly=pd.merge(jj_nav_rank_yearly,
                                     jj_nav.groupby(['jjdm','year']).count()['ym'].to_frame('count').reset_index(),
                                     how='inner',on=['jjdm','year'])
        jj_nav_rank_yearly=pd.merge(jj_nav_rank_yearly,jj_nav[['jjdm','jzrq','jjjz']],
                                    how='left',left_on=['jjdm','year_end'],right_on=['jjdm','jzrq']).drop('jzrq',axis=1)
        jj_nav_rank_yearly=pd.merge(jj_nav_rank_yearly,jj_nav[['jjdm','jzrq','jjjz']],
                                    how='left',left_on=['jjdm','year_start'],right_on=['jjdm','jzrq']).drop('jzrq',axis=1)

        jj_nav_rank_yearly['log_ret']=np.power(np.log(jj_nav_rank_yearly['jjjz_x']/jj_nav_rank_yearly['jjjz_y'])+1,250/jj_nav_rank_yearly['count'])-1

        jj_nav_rank_yearly=pd.merge(jj_nav_rank_yearly,
                                    jj_nav_rank_yearly.groupby('year').count()['jjdm'].to_frame('jjdm_count'),how='left',
                                    on='year')
        jj_nav_rank_yearly['log_ret_rank']=jj_nav_rank_yearly.groupby('year').rank(method='min')['log_ret']/jj_nav_rank_yearly['jjdm_count']
        outputdf=pd.merge(outputdf,pd.merge(jj_nav_rank_yearly.groupby('jjdm').mean()['log_ret_rank'].to_frame('yearly_rank_mean'),
                 jj_nav_rank_yearly.groupby('jjdm').std()['log_ret_rank'].to_frame('yearly_rank_std'),how='left',on='jjdm'),how='inner',on='jjdm')

        outputdf['yearly_rank_std']=outputdf['yearly_rank_std'].rank(method='min')/len(outputdf)
        outputdf=pd.merge(outputdf,regress_rank,on='jjdm',how='left')

        outputdf['业绩预期回归强度'] = '不明显'
        outputdf.loc[outputdf['ret_regress']<0.3,'业绩预期回归强度']='负向'
        outputdf.loc[outputdf['ret_regress'] < 0.1, '业绩预期回归强度'] = '强负向'
        outputdf.loc[outputdf['ret_regress'] > 0.6, '业绩预期回归强度'] = '正向'
        outputdf.loc[outputdf['ret_regress'] > 0.9, '业绩预期回归强度'] = '强正向'

        outputdf['长期相对业绩表现'] = '普通'
        outputdf.loc[outputdf['yearly_rank_mean'] < 0.4, '长期相对业绩表现'] = '较弱'
        outputdf.loc[outputdf['yearly_rank_mean'] > 0.6, '长期相对业绩表现'] = '较好'
        outputdf.loc[outputdf['yearly_rank_mean'] > 0.8, '长期相对业绩表现'] = '优秀'

        outputdf['相对业绩稳定性'] = '普通'
        outputdf.loc[outputdf['yearly_rank_std'] < 0.4, '相对业绩稳定性'] = '较弱'
        outputdf.loc[outputdf['yearly_rank_std'] > 0.6, '相对业绩稳定性'] = '较好'
        outputdf.loc[outputdf['yearly_rank_std'] > 0.8, '相对业绩稳定性'] = '优秀'

        outputdf=pd.merge(outputdf,other_ret_ratio,how='left',on='jjdm')
        outputdf = pd.merge(outputdf, moment, how='left', on='jjdm')

        outputdf['asofdate']=asofdate

        sql="delete from nav_jj_ret_analysis where asofdate='{0}'".format(asofdate)
        localdb.execute(sql,con=localdb)
        outputdf.to_sql('nav_jj_ret_analysis',con=localdb,if_exists='append',index=False)

class Timing_trade:

    def __init__(self):

        new_col_name = ['农林牧渔', '基础化工', '钢铁', '有色金属', '电子', '家用电器', '食品饮料',
                             '纺织服饰', '轻工制造', '医药生物', '公用事业', '交通运输', '房地产', '商贸零售',
                             '社会服务', '综合', '建筑材料', '建筑装饰', '电力设备', '国防军工', '计算机', '传媒',
                             '通信', '银行', '非银金融', '汽车', '机械设备', '煤炭', '石油石化', '环保', '美容护理']

        self.industry_index_1=['801003','801010','801030','801040','801050','801080','801110',
                              '801120','801130','801140','801150','801160','801170',
                              '801180','801200','801210','801230','801710','801720',
                              '801730','801740','801750','801760','801770','801780',
                              '801790','801880','801890','801950','801960','801970','801980']

        self.style_index=['399370','399371','399311']
        self.size_index = ['399314', '399315','399316','399311']
        self.index_code_map=dict(zip(self.industry_index_1,new_col_name))

        self.local_pedata=self.getlocal_index_weekly_pe()


    @staticmethod
    def get_index_price(index_list,start_date,end_date):

        sql="select zqdm,jyrq,spjg from st_market.t_st_zs_hq where zqdm in ({0}) and jyrq>='{1}' and jyrq<='{2}'"\
            .format(util.list_sql_condition(index_list),start_date,end_date)

        index_info=hbdb.db2df(sql,db='alluser')
        index_info['jyrq']=index_info['jyrq'].astype(str)

        return index_info

    @staticmethod
    def getlocal_index_weekly_pe():

        pe_data=pd.read_excel(r"D:\users\W4382909080\export\指数行情序列_行业&风格.xlsx")
        pe_data['时间']=pe_data['时间'].astype(str).str.replace('-','')


        return  pe_data

    @staticmethod
    def price2ret(style_data,col_list,bmk_col,thresheld=0.25):



        style_data['year']=style_data.index.str[0:4]
        style_data['ym'] = style_data.index.str[0:6]
        style_data['month'] = style_data.index.str[4:6]

        for col in col_list+[bmk_col]:
            style_data[col]=style_data[col]/style_data[col].iloc[0]

        style_data_monthret =pd.concat([style_data.iloc[[0]],
                                        style_data.drop_duplicates('ym',keep='last')],axis=0)[col_list+[bmk_col,'ym']]
        style_data_quarterret =pd.concat([style_data.iloc[[0]],
                                          style_data[style_data['month'].isin(['03','06','09','12'])].drop_duplicates('ym',keep='last')]
                                         ,axis=0)[col_list+[bmk_col,'ym']]
        style_data_halfyearret =pd.concat([style_data.iloc[[0]],
                                          style_data[style_data['month'].isin(['06','12'])].drop_duplicates('ym',keep='last')]
                                         ,axis=0)[col_list+[bmk_col,'ym']]
        style_data_yearret =pd.concat([style_data.iloc[[0]]
                                             ,style_data.drop_duplicates('year',keep='last')]
                                         ,axis=0)[col_list+[bmk_col,'year']]

        for col in col_list+[bmk_col]:
            style_data_monthret[col]=style_data_monthret[col].pct_change()
            style_data_quarterret[col]=style_data_quarterret[col].pct_change()
            style_data_halfyearret[col]=style_data_halfyearret[col].pct_change()
            style_data_yearret[col]=style_data_yearret[col].pct_change()

        style_data_monthret=pd.merge(style_data_monthret.iloc[1:]
                                     ,style_data.groupby('ym').mean()[[x+'PE' for x in col_list+[bmk_col]]+['PE_Diff_'+x for x in col_list]]
                                     ,how='left',on='ym')
        style_data_quarterret=pd.merge(style_data_quarterret.iloc[1:]
                                     ,style_data.groupby('ym').mean()[[x+'PE' for x in col_list+[bmk_col]]+['PE_Diff_'+x for x in col_list]]
                                     ,how='left',on='ym')
        style_data_halfyearret=pd.merge(style_data_halfyearret.iloc[1:]
                                     ,style_data.groupby('ym').mean()[[x+'PE' for x in col_list+[bmk_col]]+['PE_Diff_'+x for x in col_list]]
                                     ,how='left',on='ym')
        style_data_yearret=pd.merge(style_data_yearret.iloc[1:]
                                     ,style_data.groupby('year').mean()[[x+'PE' for x in col_list+[bmk_col]]+['PE_Diff_'+x for x in col_list]]
                                     ,how='left',on='year')

        for col in col_list:
            style_data_monthret[col]=style_data_monthret[col]-style_data_monthret[bmk_col]
            style_data_quarterret[col] = style_data_quarterret[col] - style_data_quarterret[bmk_col]
            style_data_halfyearret[col] = style_data_halfyearret[col] - style_data_halfyearret[bmk_col]
            style_data_yearret[col] = style_data_yearret[col] - style_data_yearret[bmk_col]

        for col in col_list+[x+'PE' for x in col_list+[bmk_col]]+['PE_Diff_'+x for x in col_list]:
            style_data_monthret[col+'_rank'] = style_data_monthret[col].rolling(len(style_data_monthret)-1,1).apply(rolling_rank)
            style_data_quarterret[col+'_rank'] = style_data_quarterret[col].rolling(len(style_data_quarterret)-1,1).apply(rolling_rank)
            style_data_halfyearret[col+'_rank'] = style_data_halfyearret[col].rolling(len(style_data_halfyearret)-1,1).apply(rolling_rank)
            style_data_yearret[col+'_rank'] = style_data_yearret[col].rolling(len(style_data_yearret)-1,1).apply(rolling_rank)

        for col in col_list:
            style_data_monthret.loc[style_data_monthret[col]>=0, col+'表现'] = 0.5
            style_data_monthret.loc[style_data_monthret[col] <= 0, col+'表现'] = -0.5
            style_data_monthret.loc[(style_data_monthret[col+'_rank'] >= (1-thresheld)), col+'表现'] = 1
            style_data_monthret.loc[(style_data_monthret[col+'_rank'] <= thresheld), col+'表现'] = -1

            style_data_quarterret.loc[style_data_quarterret[col]>=0, col+'表现'] = 0.5
            style_data_quarterret.loc[style_data_quarterret[col] <= 0, col+'表现'] = -0.5
            style_data_quarterret.loc[(style_data_quarterret[col+'_rank'] >= (1-thresheld)), col+'表现'] = 1
            style_data_quarterret.loc[(style_data_quarterret[col+'_rank'] <= thresheld), col+'表现'] = -1

            style_data_halfyearret.loc[style_data_halfyearret[col]>=0, col+'表现'] = 0.5
            style_data_halfyearret.loc[style_data_halfyearret[col] <= 0, col+'表现'] = -0.5
            style_data_halfyearret.loc[(style_data_halfyearret[col+'_rank'] >= (1-thresheld)), col+'表现'] = 1
            style_data_halfyearret.loc[(style_data_halfyearret[col+'_rank'] <= thresheld), col+'表现'] = -1

            style_data_yearret.loc[style_data_yearret[col]>=0, col+'表现'] = 0.5
            style_data_yearret.loc[style_data_yearret[col] <= 0, col+'表现'] = -0.5
            style_data_yearret.loc[(style_data_yearret[col+'_rank'] >= (1-thresheld)), col+'表现'] = 1
            style_data_yearret.loc[(style_data_yearret[col+'_rank'] <= thresheld), col+'表现'] = -1

            style_data_monthret['超额']=style_data_monthret[col_list[0]]-style_data_monthret[col_list[1]]
            style_data_quarterret['超额']=style_data_quarterret[col_list[0]]-style_data_quarterret[col_list[1]]
            style_data_halfyearret['超额']=style_data_halfyearret[col_list[0]]-style_data_halfyearret[col_list[1]]
            style_data_yearret['超额']=style_data_yearret[col_list[0]]-style_data_yearret[col_list[1]]


        return  style_data_monthret,style_data_quarterret,style_data_halfyearret,style_data_yearret

    @staticmethod
    def get_index_stock(if_style=True):

        if(if_style):
            index_history=pd.read_sql("select * from style_index_history where asofdate<='202206'"
                                      ,con=localdb).rename(columns={'asofdate':'ym'})
        else:
            index_history=pd.read_sql("select * from size_index_history where asofdate<='202206'"
                                      ,con=localdb).rename(columns={'asofdate':'ym'})

        #make up the index history for each month
        for year in index_history['ym'].str[0:4].unique():

            tempdf=index_history[index_history['ym']==str(year)+'03']
            tempdf['ym']=str(year)+'04'
            index_history=pd.concat([index_history,tempdf],axis=0)
            tempdf['ym']=str(year)+'05'
            index_history=pd.concat([index_history,tempdf],axis=0)

            tempdf=index_history[index_history['ym']==str(year)+'06']
            tempdf['ym']=str(year)+'07'
            index_history=pd.concat([index_history,tempdf],axis=0)
            tempdf['ym']=str(year)+'08'
            index_history=pd.concat([index_history,tempdf],axis=0)

            tempdf=index_history[index_history['ym']==str(year)+'09']
            tempdf['ym']=str(year)+'10'
            index_history=pd.concat([index_history,tempdf],axis=0)
            tempdf['ym']=str(year)+'11'
            index_history=pd.concat([index_history,tempdf],axis=0)

        index_history=index_history.sort_values('ym')

        sql = "SELECT JYRQ,SFYM FROM funddb.JYRL WHERE JYRQ >= {0} and JYRQ<={1} and SFJJ=0 ".format(
            index_history['ym'].min()+'01', index_history['ym'].max()+'31')
        calander = hbdb.db2df(sql, db='readonly').drop('ROW_ID', axis=1).sort_values('JYRQ')
        calander['ym']=calander['JYRQ'].str[0:6]

        index_history=pd.merge(index_history
                               ,calander[calander['SFYM']=='1'].drop('SFYM',axis=1),how='left',on='ym')
        index_history=index_history[index_history['ym']>='201301']

        price_df=[]

        for ym in index_history['ym'].unique().tolist():
            # print(ym)
            tempdf=index_history[index_history['ym']==ym]

            sql = """select b.SecuCode,a.BackwardPrice,a.TradingDay,a.ClosePrice 
            from hsjy_gg.SecuMain b left join hsjy_gg.QT_PerformanceData a on a.InnerCode=b.InnerCode 
            where b.SecuCode in ({0}) and a.TradingDay>=to_date('{1}','yyyymmdd') and a.TradingDay<=to_date('{2}','yyyymmdd')  """\
                .format(util.list_sql_condition(tempdf['代码'].tolist())
                        ,calander.iloc[calander['JYRQ'].tolist().index(tempdf['JYRQ'].iloc[0])-19]['JYRQ'],tempdf['JYRQ'].iloc[0])
            df = hbdb.db2df(sql, db='readonly').drop('ROW_ID',axis=1)
            df=pd.merge(df,df.groupby('SECUCODE').mean()['CLOSEPRICE'].to_frame('avg')
                        ,how='left',on='SECUCODE')
            df['flag']=0
            df.loc[df['CLOSEPRICE']>df['avg'],'flag']=1

            price_df.append(df[['SECUCODE','TRADINGDAY','flag']])

        price_df=pd.concat(price_df,axis=0)
        price_df['TRADINGDAY']=(price_df['TRADINGDAY'].str.replace('-','')).str[0:8]

        index_history=pd.merge(index_history,price_df,how='left'
                               ,left_on=['JYRQ','代码'],right_on=['TRADINGDAY','SECUCODE'])

        index_history=(index_history.groupby(['JYRQ', 'type']).mean()['flag']).reset_index()
        index_history['JYRQ']=index_history['JYRQ'].str[0:6]
        index_history=index_history.pivot_table('flag', 'JYRQ', 'type')

        if (if_style):
            index_history=(index_history['成长']-index_history['价值']).to_frame('强势股占比')
        else:
            index_history = (index_history['大盘'] -index_history['小盘']).to_frame('强势股占比')

        return index_history

    @staticmethod
    def timing_analysis(col_list,weight_col,pe_col,df_list,cluster_data=False):


        if(cluster_data):
            i=0
            outputdf = []
            for df1 in df_list[0:-1]:

                print(['月度','季度','半年度','年度'][i])
                i+=1

                for col in col_list:
                    df=df1.copy()
                    print(col)


                    # plot.plotly_line_multi_yaxis(
                    #     df[['PE_Diff', '国证成长']].reset_index().rename(columns={'时间': '日期'}), 'pe_diff'
                    #     , y2_col=['国证成长'])
                    # plot.plotly_line_multi_yaxis(
                    #     df[['PE_Rank_Diff', '国证成长']].reset_index().rename(columns={'时间': '日期'}), 'pe_diff'
                    #     , y2_col=['国证成长'])


                    for lag in [1,2,3]:
                        print('the corr for lag {}'.format(lag))
                        df[col + '_' + str(lag)] = df[col].iloc[lag:].tolist() + [np.nan] * lag

                    df=df[df[weight_col].notnull()]
                    df[weight_col+'_lag_1'] = [np.nan] + df[weight_col].iloc[0:-1].tolist()
                    df[weight_col+'_lag_2'] = [np.nan] * 2 + df[weight_col].iloc[0:-2].tolist()
                    # df.loc[ (
                    # (df['成长'] > df['成长_lag_2']) & (df['成长'] > df['成长_lag_1'])), 'inc_flag'] = 1
                    # df.loc[ (
                    # (df['成长'] < df['成长_lag_2']) & (df['成长'] < df['成长_lag_1'])), 'inc_flag'] = -1
                    df.loc[(df[weight_col] - df[weight_col+'_lag_2'] >= 0.08) | (
                    (df[weight_col] > df[weight_col+'_lag_2']) & (df[weight_col] > df[weight_col+'_lag_1'])), 'inc_flag'] = 1
                    df.loc[(df[weight_col] - df[weight_col+'_lag_2'] <= -0.08) | (
                    (df[weight_col] < df[weight_col+'_lag_2']) & (df[weight_col] < df[weight_col+'_lag_1'])), 'inc_flag'] = -1
                    outputdf.append(df.groupby('inc_flag').describe()[[col+'_1', col+'_2', col+'_3']].T)
                    #
                    # df=df[df['大盘'].notnull()]
                    # df['大盘_lag_1'] = [np.nan] + df['大盘'].iloc[0:-1].tolist()
                    # df['大盘_lag_2'] = [np.nan] * 2 + df['大盘'].iloc[0:-2].tolist()
                    # df.loc[(df['大盘'] - df['大盘_lag_2'] >= 0.07) | (
                    # (df['大盘'] > df['大盘_lag_2']) & (df['大盘'] > df['大盘_lag_1'])), 'inc_flag'] = 1
                    # df.loc[(df['大盘'] - df['大盘_lag_2'] <= -0.07) | (
                    # (df['大盘'] < df['大盘_lag_2']) & (df['大盘'] < df['大盘_lag_1'])), 'inc_flag'] = -1
                    # outputdf.append(df.groupby('inc_flag').describe()[['巨潮大盘_1', '巨潮大盘_2', '巨潮大盘_3']].T)

                    #
                    # df['stats'] = df[col+'表现'].rolling(2).sum().abs()
                    # print(df.groupby('stats').count()[bmk_col] / (len(df)-1))

            pd.concat(outputdf,axis=0).to_excel('885001weightfacor.xlsx')

        weekly_data=df_list[-1].iloc[52:]
        outputdf=[]
        for col in col_list:

            print('全局相关性')
            tempdf1=weekly_data[[col,col+'4',col+'12',col+'24'
                    ,col+'48',col+'96',col+'144',pe_col+'PE_rank','PE_Diff_{}_rank'
                                 .format(pe_col)]].corr()[[pe_col+'PE_rank','PE_Diff_{}_rank'.format(pe_col)]]
            print(tempdf1)
            outputdf.append(tempdf1)

            for threshold in [0.1,0.15,0.2,0.25]:
                print(threshold)
                print('极值相关性')
                tempdf1=weekly_data[(weekly_data[pe_col+'PE_rank']>=(1-threshold))|(weekly_data[pe_col+'PE_rank']<=threshold)][[col,col+'4',col+'12',col+'24'
                        ,col+'48',col+'96',col+'144',pe_col+'PE_rank','PE_Diff_{}_rank'
                                     .format(pe_col)]].corr()[[pe_col+'PE_rank','PE_Diff_{}_rank'.format(pe_col)]]
                print(tempdf1)
                outputdf.append(tempdf1)

                tempdf1=weekly_data[(weekly_data['PE_Diff_{}_rank'.format(pe_col)] >= (1 - threshold)) | (
                            weekly_data['PE_Diff_{}_rank'.format(pe_col)] <= threshold)][
                    [col, col + '4', col + '12', col + '24'
                        , col + '48', col + '96', col + '144', pe_col + 'PE_rank', 'PE_Diff_{}_rank'
                         .format(pe_col)]].corr()[[pe_col + 'PE_rank', 'PE_Diff_{}_rank'.format(pe_col)]]
                print(tempdf1)
                outputdf.append(tempdf1)

                print('PErank极值时超额收益分布')
                tempdf1=weekly_data[(weekly_data[pe_col + 'PE_rank'] >= (1 - threshold))][[col,col+'4',col+'12',col+'24'
                        ,col+'48',col+'96',col+'144']].describe()
                tempdf2=weekly_data[(weekly_data[pe_col + 'PE_rank'] <=  threshold)][[col,col+'4',col+'12',col+'24'
                        ,col+'48',col+'96',col+'144']].describe()
                # print(tempdf1)
                # outputdf.append(tempdf1)
                # print(tempdf2)
                # outputdf.append(tempdf2)
                print(tempdf1-tempdf2)
                outputdf.append(tempdf1-tempdf2)

                print('PE Diff rank 极值时超额收益分布')
                tempdf1=weekly_data[(weekly_data['PE_Diff_{}_rank'.format(pe_col)] >= (1 - threshold))][[col,col+'4',col+'12',col+'24'
                        ,col+'48',col+'96',col+'144']].describe()
                tempdf2=weekly_data[(weekly_data['PE_Diff_{}_rank'.format(pe_col)] <=  threshold)][[col,col+'4',col+'12',col+'24'
                        ,col+'48',col+'96',col+'144']].describe()
                # print(tempdf1)
                # outputdf.append(tempdf1)
                # print(tempdf2)
                # outputdf.append(tempdf2)
                print(tempdf1-tempdf2)
                outputdf.append(tempdf1-tempdf2)

        outputdf=pd.concat(outputdf,axis=1)
        outputdf.to_excel('reserve_test.xlsx')

    @staticmethod
    def strong_style_analysis(df,col_list,if_style=True):

        outputdf=[]

        if(if_style):
            df['强势表现'] = df['国证成长'] - df['国证价值']
        else:
            df['强势表现'] = df['巨潮大盘'] - df['巨潮小盘']

        for col in col_list:
            col='强势表现'
            for lag in [1, 2, 3]:
                df[col + '_' + str(lag)] = df[col].iloc[lag:].tolist() + [np.nan] * lag

            df=df[df['强势股占比'].notnull()]
            outputdf.append(df[['强势股占比',col,col+'_1',col+'_2',col+'_3']].corr()['强势股占比'])
            # print(
            # df[['强势股占比',col,col+'_1',col+'_2',col+'_3']].corr()['强势股占比']
            # )

            outputdf.append(df[df['强势股占比']>0].describe()[[col+'_1',col+'_2',col+'_3']])
            outputdf.append(df[df['强势股占比']>=0.09].describe()[[col+'_1',col+'_2',col+'_3']])
            # print(df[df['强势股占比']>=0].describe()[[col+'_1',col+'_2',col+'_3']])
            # print(df[df['强势股占比']>=0.09].describe()[[col+'_1',col+'_2',col+'_3']])
            outputdf=pd.concat(outputdf,axis=0)
            outputdf.to_excel('强势股{}.xlsx'.format(col_list[0]))

    def style_timing(self,start_date,end_date,threshold):

        plot=functionality.Plot(1200,600)

        style_data=self.get_index_price(self.style_index,start_date,end_date)
        size_data = self.get_index_price(self.size_index, start_date, end_date)

        style_data=style_data.pivot_table('spjg','jyrq','zqdm')
        size_data = size_data.pivot_table('spjg', 'jyrq', 'zqdm')


        style_data=pd.merge(style_data,
                            self.local_pedata[['时间','国证价值PE','国证成长PE','国证1000PE']],
                            how='inner',left_index=True,right_on='时间').rename(columns={'399311':'国证1000',
                                                                                       '399370':'国证成长',
                                                                           '399371':'国证价值'}).set_index('时间')
        for col in ['国证价值','国证成长']:
            style_data['PE_Diff_'+col]=style_data[col+'PE']-style_data['国证1000PE']

        style_data_monthret,style_data_quarterret,style_data_halfyearret,style_data_yearret=\
            self.price2ret(style_data, ['国证成长','国证价值'],'国证1000',threshold)

        # for col in ['国证价值', '国证成长','国证1000']:
        #     style_data[col]=style_data[col].pct_change(1)+1
        #     for lag in [4,12,24,48,96,144]:
        #         style_data[col+str(lag)]=style_data[col].rolling(lag).apply(rolling_cumprod).tolist()[lag:]+[np.nan]*(lag)
        #
        # style_data['超额' ]=style_data['国证成长']-style_data['国证价值']
        # for lag in [4,12,24,48,96,144]:
        #     style_data['超额'+str(lag)]=style_data['国证成长'+str(lag)]-style_data['国证价值'+str(lag)]
        #
        # for col in ['国证价值','国证成长']:
        #     style_data[col+'PE_rank']=style_data[col+'PE'].rolling(len(style_data),1).apply(rolling_rank)
        #     style_data['PE_Diff_' + col+'_rank']=style_data['PE_Diff_' + col].rolling(len(style_data),1).apply(rolling_rank)
        #     style_data[col]=style_data[col]-style_data['国证1000']
        #     for lag in [4,12,24,48,96,144]:
        #         style_data[col+str(lag)]=style_data[col+str(lag)]-style_data['国证1000'+str(lag)]

        # sql="SELECT * from 885001_hbs_style_exp where jsrq<='20211231'"
        # df885=pd.read_sql(sql,con=localdb)
        # df885.drop_duplicates(['jsrq','style_type','jjdm'],inplace=True)
        # df885['month']=df885['jsrq'].str[4:6]
        # df885=df885[df885['month'].isin(['06','12'])]
        # df885=pd.merge(df885,df885.groupby(['jjdm','jsrq']).sum()['zjbl'].reset_index(),how='left',on=['jjdm','jsrq'])
        # df885['zgbl']=df885['zjbl_x']/df885['zjbl_y']
        # df885=df885.groupby(['jsrq','style_type']).mean()['zgbl'].reset_index().pivot_table('zgbl','jsrq','style_type')
        # plot.plotly_line_style(df885,'885001风格占比时序')
        # df885['ym']=df885.index.astype(str).str[0:6]


        index_his=self.get_index_stock(True)

        # style_data_monthret=pd.merge(style_data_monthret[['国证价值', '国证成长','ym']]
        #                                 ,index_his,how='left',left_on='ym',right_on='JYRQ')
        # self.strong_style_analysis(style_data_monthret, ['国证成长'])

        style_data_quarterret=pd.merge(style_data_quarterret[['国证价值', '国证成长','ym']]
                                        ,index_his,how='left',left_on='ym',right_on='JYRQ')
        self.strong_style_analysis(style_data_quarterret, ['国证成长'])

        # style_data_halfyearret=pd.merge(style_data_halfyearret[['国证价值', '国证成长','超额','ym']]
        #                                 ,df885,how='left',on='ym')
        # style_data_quarterret=pd.merge(style_data_quarterret[['国证价值', '国证成长','超额','ym']]
        #                                 ,df885,how='left',on='ym')
        # style_data_monthret=pd.merge(style_data_monthret[['国证价值', '国证成长','超额','ym']]
        #                                 ,df885,how='left',on='ym')


        # self.timing_analysis(['超额','国证成长'],'成长','国证成长'
        #                      ,[style_data_monthret,style_data_quarterret, style_data_halfyearret,style_data]
        #                      ,cluster_data=False)


        #
        # sql="SELECT * from 885001_hbs_size_exp where jsrq<='20211231'"
        # df885=pd.read_sql(sql,con=localdb)
        # df885.drop_duplicates(['jsrq','size_type','jjdm'],inplace=True)
        # df885['month']=df885['jsrq'].str[4:6]
        # df885=df885[df885['month'].isin(['06','12'])]
        # df885=pd.merge(df885,df885.groupby(['jjdm','jsrq']).sum()['zjbl'].reset_index(),how='left',on=['jjdm','jsrq'])
        # df885['zgbl']=df885['zjbl_x']/df885['zjbl_y']
        # df885=df885.groupby(['jsrq','size_type']).mean()['zgbl'].reset_index().pivot_table('zgbl','jsrq','size_type')
        # df885['ym'] = df885.index.astype(str).str[0:6]
        #
        # size_data=pd.merge(size_data,
        #                     self.local_pedata[['时间','巨潮大盘PE','巨潮中盘PE' ,'巨潮小盘PE','国证1000PE']],
        #                     how='inner',left_index=True,right_on='时间').rename(columns={'399311':'国证1000',
        #                                                                                '399314':'巨潮大盘',
        #                                                                                '399315':'巨潮中盘',
        #                                                                                '399316':'巨潮小盘'}).set_index('时间')
        # for col in ['巨潮大盘','巨潮中盘','巨潮小盘']:
        #     size_data['PE_Diff_'+col]=size_data[col+'PE']-size_data['国证1000PE']
        #
        # size_data_monthret,size_data_quarterret,size_data_halfyearret,size_data_yearret=\
        #     self.price2ret(size_data, ['巨潮大盘','巨潮小盘'],'国证1000',threshold)
        #
        # for col in ['巨潮大盘','巨潮中盘','巨潮小盘','国证1000']:
        #     size_data[col]=size_data[col].pct_change(1)+1
        #     for lag in [4,12,24,48,96,144]:
        #         size_data[col+str(lag)]=size_data[col].rolling(lag).apply(rolling_cumprod).tolist()[lag:]+[np.nan]*(lag)
        #
        # size_data['超额' ]=size_data['巨潮大盘']-size_data['巨潮小盘']
        # for lag in [4,12,24,48,96,144]:
        #     size_data['超额'+str(lag)]=size_data['巨潮大盘'+str(lag)]-size_data['巨潮小盘'+str(lag)]
        #
        # for col in ['巨潮大盘','巨潮中盘','巨潮小盘']:
        #     size_data[col+'PE_rank']=size_data[col+'PE'].rolling(len(size_data),1).apply(rolling_rank)
        #     size_data['PE_Diff_' + col+'_rank']=size_data['PE_Diff_' + col].rolling(len(size_data),1).apply(rolling_rank)
        #     size_data[col]=size_data[col]-size_data['国证1000']
        #     for lag in [4,12,24,48,96,144]:
        #         size_data[col+str(lag)]=size_data[col+str(lag)]-size_data['国证1000'+str(lag)]
        #
        #
        # size_data_halfyearret=pd.merge(size_data_halfyearret[['巨潮小盘', '巨潮大盘','超额','ym']]
        #                                 ,df885,how='left',on='ym')
        # size_data_quarterret=pd.merge(size_data_quarterret[['巨潮小盘', '巨潮大盘','超额','ym']]
        #                                 ,df885,how='left',on='ym')
        # size_data_monthret=pd.merge(size_data_monthret[['巨潮小盘', '巨潮大盘','超额','ym']]
        #                                 ,df885,how='left',on='ym')
        #
        # self.timing_analysis(['超额','巨潮大盘'],'大盘','巨潮大盘'
        #                      ,[size_data_monthret,size_data_quarterret,size_data_halfyearret, size_data],cluster_data=False)


        # index_his=self.get_index_stock(False)
        #
        # size_data_monthret=pd.merge(size_data_monthret[['巨潮大盘', '巨潮小盘','ym']]
        #                                 ,index_his,how='left',left_on='ym',right_on='JYRQ')
        # self.strong_style_analysis(size_data_monthret, ['巨潮大盘'],False)
        #
        # size_data_quarterret=pd.merge(size_data_quarterret[['巨潮大盘', '巨潮小盘','ym']]
        #                                 ,index_his,how='left',left_on='ym',right_on='JYRQ')
        # self.strong_style_analysis(size_data_quarterret, ['巨潮大盘'],False)


        print('')

def temp_analysis_for_jr():
    #temperary work

    jj_nav_a=pd.read_excel(r"E:\GitFolder\docs\私募股多持仓分析\(周频）余小波-惠理时期代表产品净值走势.xlsx",
                         sheet_name='同策略余总过往A股基金（费后）')
    jj_nav_h = pd.read_excel(r"E:\GitFolder\docs\私募股多持仓分析\(周频）余小波-惠理时期代表产品净值走势.xlsx",
                           sheet_name='同策略余总过往港股基金（费后）')
    jj_nav_a['month_end'] = jj_nav_a['日期'].astype(str).str[5:7].astype(int).diff(-1).fillna(0)
    jj_nav_h['month_end'] = jj_nav_h['日期'].astype(str).str[5:7].astype(int).diff(-1).fillna(0)
    jj_nav_a['year_end'] = jj_nav_a['日期'].astype(str).str[0:4].astype(int).diff(-1).fillna(0)
    jj_nav_h['year_end'] = jj_nav_h['日期'].astype(str).str[0:4].astype(int).diff(-1).fillna(0)

    jj_nav_a.loc[jj_nav_a['日期']<'2018-08-01','glf']=0.01
    jj_nav_a.loc[jj_nav_a['日期'] >= '2018-08-01', 'glf'] = 0.008
    jj_nav_h.loc[jj_nav_a['日期']<'2018-08-01','glf']=0.008
    jj_nav_h.loc[jj_nav_a['日期'] >= '2018-08-01', 'glf'] = 0.005

    jj_nav_a.loc[jj_nav_a['日期']<'2018-08-01','jybc']=0.15
    jj_nav_a.loc[jj_nav_a['日期'] >= '2018-08-01', 'jybc'] = 0.13
    jj_nav_h['jybc']=0.15

    def nav_afterfee2nav_beforefee(jj_nav_a,x0):

        for i in range(1,len(jj_nav_a)):
            if(jj_nav_a.loc[i]['year_end']!=0):
                if(jj_nav_a.loc[i]['净值']>x0):
                    factor=1-jj_nav_a.loc[i]['glf']-jj_nav_a.loc[i]['jybc']/jj_nav_a.loc[i]['净值']
                    jj_nav_a.loc[i,'净值']= (jj_nav_a.loc[i]['净值']-jj_nav_a.loc[i]['jybc'])/factor
                else:
                    jj_nav_a.loc[i, '净值'] = jj_nav_a.loc[i]['净值'] / (1 - jj_nav_a.loc[i]['glf'])
                x0=jj_nav_a.loc[i,'净值']
                if(jj_nav_a.loc[i]['month_end']!=0):
                    jj_nav_a.loc[i,'净值']=jj_nav_a.loc[i]['净值']/(1-jj_nav_a.loc[i]['glf'])

        return  jj_nav_a

    jj_nav_a=nav_afterfee2nav_beforefee(jj_nav_a,1.1748)
    jj_nav_h=nav_afterfee2nav_beforefee(jj_nav_h.loc[2:].reset_index(drop=True),10.018500)

    jj_nav_a['日期']=jj_nav_a['日期'].astype(str).str.replace('-','')
    jj_nav_h['日期'] = jj_nav_h['日期'].astype(str).str.replace('-', '')

    # standardlize the nav
    jj_nav_a['净值']=jj_nav_a['净值']/1.1748
    jj_nav_h['净值'] = jj_nav_h['净值'] / 10.018500

    jj_nav=pd.merge(jj_nav_a[['日期','净值','month_end', 'year_end']],jj_nav_h[['日期','净值']],how='outer',on='日期')
    jj_nav=jj_nav.sort_values('日期')
    #get priviate fund nav
    compare_jjdm_list=['SJT512','H03985','S66391','SE6168']
    jj_ret = hbdb.db2df("select jjdm,hbdr,jzrq,fqdwjz from st_hedge.t_st_rhb where jjdm in ({})"
                        .format(util.list_sql_condition(compare_jjdm_list)), db='highuser')
    initial_value = (jj_ret.drop_duplicates(['jjdm'], keep='first').set_index('jjdm'))['fqdwjz']
    jj_ret=jj_ret.pivot_table('fqdwjz', 'jzrq', 'jjdm')
    #standardlize the nav
    for jjdm in compare_jjdm_list:
        jj_ret[jjdm]=jj_ret[jjdm]/initial_value.loc[jjdm]


    #get mutual fund nav
    compare_jjdm_list2=['006624','005267','000577','005775','001583']
    jj_ret2 = hbdb.db2df("select jjdm,jzrq,fqdwjz from st_fund.t_st_gm_rhb where jjdm in ({})"
                        .format(util.list_sql_condition(compare_jjdm_list2)), db='funduser')
    jj_ret2['jzrq']=jj_ret2['jzrq'].astype(str)
    initial_value = (jj_ret2.drop_duplicates(['jjdm'], keep='first').set_index('jjdm'))['fqdwjz']
    jj_ret2=jj_ret2.pivot_table('fqdwjz', 'jzrq', 'jjdm')

    #standardlize the nav
    for jjdm in compare_jjdm_list2:
        jj_ret2[jjdm]=jj_ret2[jjdm]/initial_value.loc[jjdm]

    #get index nav

    sql = "select zqdm,jyrq,spjg from st_market.t_st_zs_hqql where zqdm in ('399371','000905') and jyrq>='{0}' and jyrq<='{1}'"\
        .format(jj_nav['日期'].min(),jj_nav['日期'].max())
    index_nav = hbdb.db2df(sql, db='alluser')
    index_nav['jyrq']=index_nav['jyrq'].astype(str)
    index_nav=index_nav.pivot_table('spjg','jyrq','zqdm')
    # standardlize the nav
    index_nav['000905']=index_nav['000905']/index_nav['000905'].iloc[0]
    index_nav['399371'] = index_nav['399371'] / index_nav['399371'].iloc[0]


    jj_nav=pd.merge(jj_nav,jj_ret,how='left',left_on='日期',right_on='jzrq')
    jj_nav = pd.merge(jj_nav, jj_ret2, how='left', left_on='日期',right_on='jzrq')
    jj_nav = pd.merge(jj_nav, index_nav, how='left', left_on='日期', right_on='jyrq')

    jj_nav.set_index('日期',inplace=True)

    jjdm_list=['净值_x', '净值_y']+compare_jjdm_list+compare_jjdm_list2+['399371','000905']

    corr_df=pd.DataFrame(index=['净值_x','净值_y'],columns=['净值_y']+compare_jjdm_list+compare_jjdm_list2+['399371','000905'])

    corr_df.loc['净值_x', '净值_y'] = \
        (np.log(jj_nav[(jj_nav['净值_y'].notnull()) & (jj_nav['净值_x'].notnull())][['净值_x', '净值_y']].pct_change() + 1).corr())[
            '净值_y']['净值_x']
    corr_df.loc['净值_y', '净值_y'] = 1

    for jjdm in compare_jjdm_list+compare_jjdm_list2+['399371','000905']:
        corr_df.loc['净值_x',jjdm]=\
            (np.log(jj_nav[(jj_nav[jjdm].notnull())&(jj_nav['净值_x'].notnull())][['净值_x',jjdm]].pct_change()+1).corr())[jjdm]['净值_x']
        corr_df.loc['净值_y', jjdm] = \
        (np.log(jj_nav[jj_nav[jjdm].notnull()&(jj_nav['净值_y'].notnull())][['净值_y', jjdm]].pct_change() + 1).corr())[jjdm]['净值_y']


    #return analysis


    #get trade_date calander
    sql_script = "SELECT JYRQ,SFZM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {} and SFJJ=0 ".format(
        jj_nav.index.min(), jj_nav.index.max())
    calander = hbdb.db2df(sql_script, db='readonly').drop('ROW_ID',axis=1)

    jj_nav['year'] = jj_nav.index.str[0:4]
    # annual ret
    annual_ret = np.log(jj_nav[(jj_nav['year_end'] != 0) &
                               (jj_nav['year_end'].notnull())][jjdm_list].pct_change() + 1).fillna(0)
    # make the return yearly return for jj shown for the first time
    for jj in jjdm_list:
        first_shown=jj_nav[jj_nav[jj].notnull()].iloc[0:1]
        if(first_shown['year_end'].values[0]==0):
            adjust_data=jj_nav.drop_duplicates('year',
                                               keep='last')[jj_nav.drop_duplicates('year',
                                                                                   keep='last')['year']==first_shown['year'].iloc[0]][jj]
            time_diff=(datetime.datetime.strptime(adjust_data.index[0], '%Y%m%d')-datetime.datetime.strptime(first_shown.index[0], '%Y%m%d')).days

            new_ret=np.log( np.power(adjust_data.values[0]/first_shown[jj].values[0]
                             ,365/time_diff))
            annual_ret.loc[adjust_data.index[0],jj]=new_ret


    #quarter_ret
    jj_nav['month'] = jj_nav.index.str[4:6]
    quarter_ret=jj_nav[(jj_nav['month'] == '12')|
                       (jj_nav['month'] == '09')|
                       (jj_nav['month'] == '06')|
                       (jj_nav['month'] == '03')]
    quarter_ret=np.log(quarter_ret[(quarter_ret['month_end'] != 0)
           & (quarter_ret['month_end'].notnull())][jjdm_list].pct_change()+1).fillna(0)
    #month_ret
    monthly_ret=np.log(jj_nav[(jj_nav['month_end']!=0)
                              &(jj_nav['month_end'].notnull())][jjdm_list].pct_change()+1).fillna(0)

    #weekly ret
    jj_nav=pd.merge(jj_nav,calander,how='left',left_on='日期',right_on='JYRQ')
    jj_nav=jj_nav[jj_nav['SFZM']=='1']
    jj_nav=jj_nav.set_index('JYRQ').drop(['SFZM','month_end','year_end','month'],axis=1)
    weekly_ret=np.log(jj_nav[jjdm_list].pct_change()+1).fillna(0)

    #ratio value
    weekly_ret['year']=weekly_ret.index.str[0:4]

    max_draw_df=pd.DataFrame(columns=weekly_ret['year'].unique().tolist()[1:],index=jjdm_list)

    ret_ratio=weekly_ret.groupby('year').mean() * 52
    ret_vol = weekly_ret.groupby('year').std() * np.sqrt(52)
    ret_shart=pd.DataFrame(data=annual_ret.values/ret_vol.iloc[:-1].values,
                           columns=jjdm_list,index=ret_vol.index[:-1])

    for year in weekly_ret['year'].unique().tolist()[1:]:

        # max draw back
        temp_nav=jj_nav[jj_nav['year']==year]
        last_max_nav = pd.DataFrame(index=jjdm_list)
        last_max_nav['max'] =temp_nav.loc[temp_nav.index[0]].loc[jjdm_list].values
        last_max_nav['max_drawback'] = 0
        for index in temp_nav.index[1:]:
            last_max_nav['new_nav']=temp_nav.loc[index].loc[jjdm_list].values
            last_max_nav['new_drawback'] = np.log( (last_max_nav['new_nav']/last_max_nav['max']).astype(float))
            last_max_nav['max'] = last_max_nav[['max','new_nav']].max(axis=1)
            last_max_nav['max_drawback']=last_max_nav[['max_drawback','new_drawback']].min(axis=1)

        max_draw_df[year]=last_max_nav['max_drawback'].values


    name_map=dict(zip(jjdm_list,['静瑞A','静瑞H','仁桥','旭松','厚山','文多','中泰玉衡','嘉实价值','安信价值','中加转型动力'
        ,'安信新常态','巨潮价值','中证500']))

    ret_shart.to_excel('sharp_ratio.xlsx')

def jj_alpha_beta_analysis(jjdm_list):

    from hbshare.fe.common.util import regressions
    from itertools import combinations

    plot=functionality.Plot(1200,600)
    #get the jj_nav from DB

    sql="select jjdm,jzrq,fqdwjz from st_fund.t_st_gm_rhb where jjdm in ({})"\
        .format(util.list_sql_condition(jjdm_list))
    jj_nav=hbdb.db2df(sql,db='funduser')
    jj_nav['jzrq']=jj_nav['jzrq'].astype(str)

    start_date=jj_nav.groupby('jjdm')['jzrq'].min().max()
    end_date=jj_nav.groupby('jjdm')['jzrq'].max().min()
    jj_nav=jj_nav.pivot_table('fqdwjz','jzrq','jjdm')
    jj_nav=jj_nav.loc[start_date:end_date]
    jj_nav = jj_nav.pct_change(1)
    #read the barra factor return from DB
    sql="select * from st_ashare.r_st_barra_factor_return where trade_date>='{0}' and trade_date<='{1}'"\
        .format(start_date,end_date)

    barra_ret=hbdb.db2df(sql,db='alluser').pivot_table('factor_ret','trade_date','factor_name')
    risk_col=barra_ret.columns.tolist()
    barra_col=['beta', 'btop', 'country', 'earnyield', 'growth'
        , 'leverage', 'liquidity', 'momentum', 'resvol', 'size', 'sizenl']
    ols_df=pd.merge(jj_nav.iloc[1:],barra_ret
                    ,how='left',left_index=True,right_index=True)
    ols_df=ols_df[ols_df['momentum'].notnull()]

    new_jjdm_list=[]
    alpha_list=[]
    r_squre_list=[]

    for c in combinations(barra_col,6):
        for jjdm in jjdm_list:
            reg=regressions.Regression(ols_df[list(c)],ols_df[jjdm],0,1)
            result=reg.solve()
            para=result['solution_with_alpha']
            alpha=para['alpha']
            r_sq=result['r_square']

            new_jjdm_list.append(jjdm)
            alpha_list.append(alpha)
            r_squre_list.append(r_sq)

    plot_df=pd.DataFrame()
    plot_df['jjdm']=new_jjdm_list
    plot_df['alpha']=alpha_list
    plot_df['r_sq']=r_squre_list
    plot_df=plot_df.sort_values(['jjdm', 'r_sq'])
    name_map=dict(zip(['001410','005968','270028','377240'],
                      ['信澳新能源产业股票','创金合信工业周期股票','广发制造业精选混合','上投摩根新兴动力混合']))
    for jjdm in jjdm_list:

        plot.plotly_markers(plot_df[plot_df['jjdm']==jjdm][['alpha','r_sq']].set_index('r_sq'),name_map[jjdm])

class Fund_performance_research:


    def __init__(self,start_date,end_date,asofdate='20211231',benchmark_list=None):

        if(benchmark_list is None):
            self.benchmark_list=util.get_stock_funds_pool(asofdate)
        else:
            self.benchmark_list=benchmark_list

        self.start_date=start_date
        self.end_date=end_date


    @staticmethod
    def get_fund_size(jjdm_list,start_date,end_date):

        sql="select jjdm,jsrq,jjzzc from st_fund.t_st_gm_zcpz where jjdm in ({0}) and jsrq>='{1}' and jsrq<='{2}' "\
            .format(util.list_sql_condition(jjdm_list),start_date,end_date)

        fund_size_info=hbdb.db2df(sql,db='funduser')

        return  fund_size_info

    @staticmethod
    def manager_and_fund(ext_con=None):

        if(ext_con is None):
            ext_con='1=1'

        sql="select jjdm,ryxm,rydm,ryzt,rzrq,lrrq from st_fund.t_st_gm_jjjl where ryzw='基金经理' and {} "\
            .format(ext_con)
        manager_info=hbdb.db2df(sql,db='funduser')

        return  manager_info

    @staticmethod
    def get_benchmeark_monthly_ret(jjdm_list,start_date,end_date):

        sql = "select jjdm,tjyf,rqzh,hb1y from st_fund.t_st_gm_yhb where jjdm in ({0}) and rq1y!=99999 {1} {2} " \
            .format(util.list_sql_condition(jjdm_list)
                    , "and rqzh>='{}'".format(start_date)
                    , "and rqzh<='{}'".format(end_date))
        montly_ret=hbdb.db2df(sql,db='funduser')


        # sql = "select jjdm,tjjd,rqzh,hb1j from st_fund.t_st_gm_jhb where jjdm in ({0}) and hb1j!=99999 {1} {2} " \
        #     .format(util.list_sql_condition(jjdm_list)
        #             , "and rqzh>='{}'".format(start_date)
        #             , "and rqzh<='{}'".format(end_date))
        # quarterly_ret=hbdb.db2df(sql,db='funduser')
        #
        #
        # sql = "select jjdm,tjnf,rqzh,hb1n from st_fund.t_st_gm_nhb where jjdm in ({0}) and hb1n!=99999 {1} {2} " \
        #     .format(util.list_sql_condition(jjdm_list)
        #             , "and rqzh>='{}'".format(start_date)
        #             , "and rqzh<='{}'".format(end_date))
        # yearly_ret=hbdb.db2df(sql,db='funduser')


        return  montly_ret

    @staticmethod
    def get_manager_product_monthly_ret(manager_info,benchmark_list):

        jjdm_list = manager_info['jjdm'].unique().tolist()

        jjdm_list = list(set(jjdm_list).difference(set(benchmark_list)))

        start_date = str(manager_info['rzrq'].min())
        end_date = str(manager_info['lrrq'].max())

        sql = "select jjdm,tjyf,rqzh,hb1y from st_fund.t_st_gm_yhb where jjdm in ({0}) and rq1y!=99999 {1} {2} " \
            .format(util.list_sql_condition(jjdm_list)
                    , "and rqzh>='{}'".format(start_date)
                    , "and rqzh<='{}'".format(end_date))
        montly_ret = hbdb.db2df(sql, db='funduser')


        return montly_ret

    @staticmethod
    def get_index_monthly_ret(start_date,end_date):

        sql = "select zqdm,tjyf,rqzh,hb1y from st_market.t_st_zs_yhb where zqdm in ({0}) and abs(hb1y)!=99999 {1} {2}" \
            .format(util.list_sql_condition(['399370','399371','399401','399314','399311'])
                    , "and rqzh>='{}'".format(start_date)
                    ,"and rqzh<='{}'".format(end_date) )

        index_ret = hbdb.db2df(sql, db='alluser')

        index_ret['hb1y']=index_ret['hb1y']/100


        name_map=dict(zip(['399370','399371','399401','399314','399311']
                          ,['成长','价值','中小盘','大盘','国证1000']))

        index_ret=index_ret.pivot_table('hb1y', 'tjyf', 'zqdm').rename(columns=name_map).reset_index(drop=False)


        return index_ret

    def difference_between_product(self,ext_con):

        manager_info=self.manager_and_fund(ext_con)

        montly_ret=pd.concat([self.benchmark_ret
                                ,self.get_manager_product_monthly_ret(manager_info
                                ,self.benchmark_list)]
                             ,axis=0).sort_values(['jjdm','tjyf']).reset_index(drop=True)

        jjdm_list = manager_info['jjdm'].unique().tolist()

        monthly_result=pd.DataFrame()
        yearly_result=pd.DataFrame()

        benchmark_ret=self.get_benchmeark_monthly_ret(self.benchmark_list
                                                           ,self.start_date
                                                           ,self.end_date)

        monthly_his=pd.DataFrame(data=benchmark_ret['tjyf'].unique().tolist()
                                 ,columns=['tjyf'])
        yearly_his=pd.DataFrame(data=benchmark_ret['tjyf'].astype(str).str[0:4].unique().tolist()
                                 ,columns=['tjnf'])

        index_ret=self.get_index_monthly_ret(self.start_date,self.end_date)
        index_list=['成长','价值','中小盘','大盘','国证1000']
        index_ret[index_list]=index_ret[index_list]+1
        index_ret['tjnf'] = index_ret['tjyf'].astype(str).str[0:4]
        index_ret[index_list] = index_ret.groupby('tjnf').cumprod(axis=0)[
            index_list]
        index_year = index_ret.drop_duplicates('tjnf'
                                               , keep='last').reset_index(drop=True).drop('tjyf'
                                                                                          , axis=1)
        index_year[index_list] = index_year[index_list] - 1

        for jjdm in jjdm_list:

            date_range=manager_info[manager_info['jjdm']==jjdm][['rzrq','lrrq']]
            benchmark=montly_ret[(montly_ret['rqzh']>=date_range.values[0][0])&(montly_ret['rqzh']<=date_range.values[0][1])]


            benchmark['hb1y']=benchmark['hb1y']/100+1
            benchmark['month_rank']=benchmark.groupby('tjyf').rank(method='min')['hb1y']
            benchmark=pd.merge(benchmark
                               ,benchmark.groupby('tjyf').count()['jjdm'].to_frame('count'),on='tjyf')
            benchmark['month_rank']=benchmark['month_rank']/benchmark['count']

            #get yearly cum return
            benchmark['tjnf']=benchmark['tjyf'].astype(str).str[0:4]

            benchmark['cum_ret_byyear']=benchmark.groupby(['jjdm', 'tjnf'])['hb1y'].cumprod(axis=0)

            benchmark=benchmark.sort_values(['jjdm','tjyf']).reset_index(drop=True)

            benchmark_year=benchmark.drop_duplicates(['jjdm','tjnf']
                                                     ,keep='last').reset_index(drop=True).drop(['month_rank','count','hb1y']
                                                                                               ,axis=1)


            benchmark_year=pd.merge(benchmark_year
                                    ,benchmark.groupby(['jjdm', 'tjnf']).count()['tjyf'].to_frame('month_count')
                                    ,how='left',on=['jjdm','tjnf'])

            #get the annually return
            benchmark_year['cum_ret_byyear']=np.power(benchmark_year['cum_ret_byyear'],12/benchmark_year['month_count'])-1


            benchmark_year['year_rank']=benchmark_year.groupby('tjyf').rank(method='min')['cum_ret_byyear']
            benchmark_year=pd.merge(benchmark_year
                               ,benchmark_year.groupby('tjyf').count()['jjdm'].to_frame('count'),on='tjyf')
            benchmark_year['year_rank']=benchmark_year['year_rank']/benchmark_year['count']


            monthly_result=pd.concat([monthly_result
                                         ,benchmark[benchmark['jjdm']==jjdm].describe()['month_rank'].to_frame(jjdm)]
                                     ,axis=1)

            monthly_his = pd.merge(monthly_his,benchmark[benchmark['jjdm'] == jjdm][['month_rank', 'tjyf']].rename(
                columns={'month_rank': jjdm}),how='left',on='tjyf')

            yearly_result=pd.concat([yearly_result
                                         ,benchmark_year[benchmark_year['jjdm']==jjdm].describe()['year_rank'].to_frame(jjdm)]
                                     ,axis=1)

            yearly_his = pd.merge(yearly_his,benchmark_year[benchmark_year['jjdm'] == jjdm][['year_rank', 'tjnf']].rename(
                columns={'year_rank': jjdm}),how='left',on='tjnf')


        jjjc=hbdb.db2df("select jjdm,jjjc from st_fund.t_st_gm_jjxx where jjdm in ({})"
                        .format(util.list_sql_condition(jjdm_list)),db='funduser')

        jjjc_map=dict(zip(jjjc['jjdm'].tolist(),jjjc['jjjc'].tolist()))

        monthly_his=pd.merge(monthly_his,index_ret,how='left',on='tjyf')
        yearly_his=pd.merge(yearly_his,index_year,how='left',on='tjnf')

        return  monthly_result.rename(columns=jjjc_map)\
            ,monthly_his.rename(columns=jjjc_map)\
            ,yearly_result.rename(columns=jjjc_map)\
            ,yearly_his.rename(columns=jjjc_map)

    @staticmethod
    def define_scenario(monthly_his,yearly_his,index_list):

        interest_list=yearly_his.columns.tolist()
        interest_list=list(set(interest_list).difference(set(index_list)))
        interest_list.remove('tjnf')

        year_thresheld=0.1
        yearly_his['风格场景']='均衡'
        yearly_his.loc[yearly_his['成长']-yearly_his['价值']>year_thresheld,'风格场景']='成长占优'
        yearly_his.loc[yearly_his['价值']-yearly_his['成长']>year_thresheld,'风格场景']='价值占优'

        yearly_his['规模场景']='均衡'
        yearly_his.loc[yearly_his['大盘']-yearly_his['中小盘']>year_thresheld,'规模场景']='大盘占优'
        yearly_his.loc[yearly_his['中小盘']-yearly_his['大盘']>year_thresheld,'规模场景']='中小盘占优'

        yearly_his['市场场景']='均衡'
        yearly_his.loc[yearly_his['国证1000']>yearly_his['国证1000'].quantile(0.6),'市场场景']='景气'
        yearly_his.loc[yearly_his['国证1000']<yearly_his['国证1000'].quantile(0.4),'市场场景']='衰退'


        style_comparison=pd.merge(yearly_his[yearly_his['风格场景']=='成长占优'].groupby(['规模场景','市场场景']).mean()[interest_list]
                                  ,yearly_his[yearly_his['风格场景']=='价值占优'].groupby(['规模场景','市场场景']).mean()[interest_list]
                                  ,how='outer',left_index=True,right_index=True)
        size_comparison=pd.merge(yearly_his[yearly_his['规模场景']=='大盘占优'].groupby(['风格场景','市场场景']).mean()[interest_list]
                                  ,yearly_his[yearly_his['规模场景']=='中小盘占优'].groupby(['风格场景','市场场景']).mean()[interest_list]
                                  ,how='outer',left_index=True,right_index=True)
        market_comparison=pd.merge(yearly_his[yearly_his['市场场景']=='景气'].groupby(['规模场景','风格场景']).mean()[interest_list]
                                  ,yearly_his[yearly_his['市场场景']=='衰退'].groupby(['规模场景','风格场景']).mean()[interest_list]
                                  ,how='outer',left_index=True,right_index=True)


        for col in interest_list:
            style_comparison[col+'_成长-价值']=style_comparison[col+'_x']-style_comparison[col+'_y']
            size_comparison[col+'_大盘-中小盘']=size_comparison[col+'_x']-size_comparison[col+'_y']
            market_comparison[col+'_景气-衰退']=market_comparison[col+'_x']-market_comparison[col+'_y']

        for df in [style_comparison,size_comparison,market_comparison]:
            df.loc[('均值','-'),:] = df.mean(axis=0)
            df.fillna(0,inplace=True)
            for col in df.columns:
                df[col]= df[col].astype(float).map("{:.2%}".format)

        style_comparison=style_comparison[style_comparison.columns.sort_values()]
        orginal_col=style_comparison.columns.tolist()
        new_col=[x.replace('_x','_成长占优') for x in orginal_col]
        new_col = [x.replace('_y', '_价值占优') for x in new_col]
        style_comparison.columns=new_col

        size_comparison = size_comparison[size_comparison.columns.sort_values()]
        orginal_col = size_comparison.columns.tolist()
        new_col=[x.replace('_x','_大盘占优') for x in orginal_col]
        new_col = [x.replace('_y', '_中小盘占优') for x in new_col]
        size_comparison.columns=new_col

        market_comparison = market_comparison[market_comparison.columns.sort_values()]
        orginal_col = market_comparison.columns.tolist()
        new_col=[x.replace('_x','_景气') for x in orginal_col]
        new_col = [x.replace('_y', '_衰退') for x in new_col]
        market_comparison.columns=new_col

        style_comparison_year=style_comparison.copy().reset_index(drop=False)
        size_comparison_year = size_comparison.copy().reset_index(drop=False)
        market_comparison_year = market_comparison.copy().reset_index(drop=False)

        #month_thresheld=np.power((1+year_thresheld),1/12)-1
        month_thresheld=0.01
        monthly_his['风格场景']='均衡'
        monthly_his.loc[monthly_his['成长']-monthly_his['价值']>month_thresheld,'风格场景']='成长占优'
        monthly_his.loc[monthly_his['价值']-monthly_his['成长']>month_thresheld,'风格场景']='价值占优'

        monthly_his['规模场景']='均衡'
        monthly_his.loc[monthly_his['大盘']-monthly_his['中小盘']>month_thresheld,'规模场景']='大盘占优'
        monthly_his.loc[monthly_his['中小盘']-monthly_his['大盘']>month_thresheld,'规模场景']='中小盘占优'

        monthly_his['市场场景']='均衡'
        monthly_his.loc[monthly_his['国证1000']>monthly_his['国证1000'].quantile(0.6),'市场场景']='景气'
        monthly_his.loc[monthly_his['国证1000']<monthly_his['国证1000'].quantile(0.4),'市场场景']='衰退'



        style_comparison=pd.merge(monthly_his[monthly_his['风格场景']=='成长占优'].groupby(['规模场景','市场场景']).mean()[interest_list]
                                  ,monthly_his[monthly_his['风格场景']=='价值占优'].groupby(['规模场景','市场场景']).mean()[interest_list]
                                  ,how='outer',left_index=True,right_index=True)
        size_comparison=pd.merge(monthly_his[monthly_his['规模场景']=='大盘占优'].groupby(['风格场景','市场场景']).mean()[interest_list]
                                  ,monthly_his[monthly_his['规模场景']=='中小盘占优'].groupby(['风格场景','市场场景']).mean()[interest_list]
                                  ,how='outer',left_index=True,right_index=True)
        market_comparison=pd.merge(monthly_his[monthly_his['市场场景']=='景气'].groupby(['规模场景','风格场景']).mean()[interest_list]
                                  ,monthly_his[monthly_his['市场场景']=='衰退'].groupby(['规模场景','风格场景']).mean()[interest_list]
                                  ,how='outer',left_index=True,right_index=True)

        for col in interest_list:
            style_comparison[col+'_成长-价值']=style_comparison[col+'_x']-style_comparison[col+'_y']
            size_comparison[col+'_大盘-中小盘']=size_comparison[col+'_x']-size_comparison[col+'_y']
            market_comparison[col+'_景气-衰退']=market_comparison[col+'_x']-market_comparison[col+'_y']

        for df in [style_comparison,size_comparison,market_comparison]:
            df.loc[('均值','-'),:] = df.mean(axis=0)
            df.fillna(0,inplace=True)
            for col in df.columns:
                df[col]= df[col].astype(float).map("{:.2%}".format)

        style_comparison=style_comparison[style_comparison.columns.sort_values()]
        orginal_col=style_comparison.columns.tolist()
        new_col=[x.replace('_x','_成长占优') for x in orginal_col]
        new_col = [x.replace('_y', '_价值占优') for x in new_col]
        style_comparison.columns=new_col

        size_comparison = size_comparison[size_comparison.columns.sort_values()]
        orginal_col = size_comparison.columns.tolist()
        new_col=[x.replace('_x','_大盘占优') for x in orginal_col]
        new_col = [x.replace('_y', '_中小盘占优') for x in new_col]
        size_comparison.columns=new_col

        market_comparison = market_comparison[market_comparison.columns.sort_values()]
        orginal_col = market_comparison.columns.tolist()
        new_col=[x.replace('_x','_景气') for x in orginal_col]
        new_col = [x.replace('_y', '_衰退') for x in new_col]
        market_comparison.columns=new_col

        style_comparison_month=style_comparison.copy().reset_index(drop=False)
        size_comparison_month = size_comparison.copy().reset_index(drop=False)
        market_comparison_month = market_comparison.copy().reset_index(drop=False)


        return [style_comparison_month,size_comparison_month,market_comparison_month\
            ,style_comparison_year,size_comparison_year,market_comparison_year]

    @staticmethod
    def get_max_draw_back(df):

        nav_df=df.copy()
        total_len=len(nav_df)
        result=pd.DataFrame(index=nav_df.columns.tolist(),columns=['最大回撤','发生日期'])


        for col in nav_df.columns.tolist():

            nav_df[col+'_db']=(nav_df[col]/nav_df[col].rolling(total_len,1).max())-1
            max_drawback=nav_df[col+'_db'].min()
            result.loc[col,'最大回撤']=np.abs(max_drawback)
            result.loc[col, '发生日期']=nav_df[nav_df[col+'_db']==max_drawback].index[0]

        return result

    @staticmethod
    def get_downside_risk(ret_df):

        total_len=len(ret_df)
        result=pd.DataFrame(index=ret_df.columns.tolist(),columns=['下行波动率'])

        for col in ret_df.columns.tolist():
            mean=ret_df[col].mean()
            downsiderisk=np.sqrt( (np.power([ np.min([x,0]) for x in  ret_df[col]-mean],2)).sum()/total_len)
            result.loc[col,'下行波动率']=downsiderisk

        return  result

    def calculate_ret_stats(self,weekly_ret):
        std = weekly_ret.std(axis=0) * np.sqrt(12)
        downsiderisk = self.get_downside_risk(weekly_ret) * np.sqrt(12)
        return std,downsiderisk

    def calculate_nav_stats(self,weekly_nav):
        time_delta = (datetime.datetime.strptime(str(weekly_nav.index[-1]) + '01'
                                                 , '%Y%m%d') - datetime.datetime.strptime(
            str(weekly_nav.index[0]) + '01'
            , '%Y%m%d')).days / 365

        annual_ret = np.power(weekly_nav.iloc[-1], 1 / time_delta) - 1
        max_drawback = self.get_max_draw_back(weekly_nav)

        return annual_ret,max_drawback

    @staticmethod
    def combinethestats(annual_ret,std,downsiderisk,max_drawback):

        pool_stats = pd.merge(annual_ret.to_frame('年化收益')
                              , std.to_frame('年化波动率'), how='inner', left_index=True, right_index=True)
        pool_stats = pd.merge(pool_stats
                              , downsiderisk, how='inner', left_index=True, right_index=True)
        pool_stats = pd.merge(pool_stats
                              , max_drawback, how='inner', left_index=True, right_index=True)
        pool_stats['夏普比率'] = pool_stats['年化收益'] / pool_stats['年化波动率']
        pool_stats['索提诺比率'] = pool_stats['年化收益'] / pool_stats['下行波动率']
        pool_stats['卡尔玛比率'] = pool_stats['年化收益'] / pool_stats['最大回撤']

        return pool_stats

    def fund_pool_stats(self,pool_list,if_mutual=True):

        #get 上证指数周收益
        sql="select hb1y,tjyf from st_market.t_st_zs_yhb where zqdm='000001' and tjyf>='{0}' and tjyf<='{1}' and hb1y!=99999"\
            .format(self.start_date,self.end_date)
        bmk_ret=hbdb.db2df(sql,db='alluser').set_index('tjyf').rename(columns={'hb1y':'上证指数'})
        bmk_ret=bmk_ret/100


        if(if_mutual):

            sql="""
            select a.jjdm,a.hb1y ,a.tjyf,b.ejfl from st_fund.t_st_gm_yhb a 
            left join st_fund.t_st_gm_jjxx b  on a.jjdm=b.jjdm  
            where a.jjdm in ({0}) and a.tjyf>='{1}' and a.tjyf<='{2}' and a.hb1y<=300 and a.hb1y>=-300 
            """.format(util.list_sql_condition(pool_list),self.start_date,self.end_date)
            weekly_ret_detail = hbdb.db2df(sql, db='funduser')
            weekly_ret_detail=pd.merge(weekly_ret_detail,
                                       weekly_ret_detail.groupby('tjyf').quantile(0.8)['hb1y'].to_frame('80')
                                       ,how='inner',on='tjyf')
            weekly_ret_detail=pd.merge(weekly_ret_detail,
                                       weekly_ret_detail.groupby('tjyf').quantile(0.2)['hb1y'].to_frame('20')
                                       ,how='inner',on='tjyf')
            weekly_ret_detail=weekly_ret_detail[(weekly_ret_detail['hb1y']<weekly_ret_detail['80'])
                                                &(weekly_ret_detail['hb1y']>weekly_ret_detail['20'])]

            weekly_ret=(weekly_ret_detail.groupby('tjyf').mean()['hb1y']).to_frame('pool')

            desc = weekly_ret_detail.groupby('tjyf').describe()
            desc=desc['hb1y'][['75%','25%','50%']]/100
            desc['75%']=desc['75%']-desc['50%']
            desc['25%']=desc['25%']-desc['50%']

            sql="select zqdm,hb1y,tjyf from st_market.t_st_zs_yhb where zqdm in ('885000','885061','885001') and tjyf>='{0}' and tjyf<={1}"\
                .format(self.start_date,self.end_date)
            weekly_ret_byejfl=hbdb.db2df(sql,db='alluser').pivot_table('hb1y','tjyf','zqdm')


            weekly_ret=pd.merge(weekly_ret,weekly_ret_byejfl,how='inner',on='tjyf')
            weekly_ret.columns=['金工公募偏股型基金指数','万得偏股混合型指数']
            weekly_ret=weekly_ret/100

            weekly_ret=pd.merge(weekly_ret,bmk_ret,how='left',left_index=True,right_index=True)

            std, downsiderisk=self.calculate_ret_stats(weekly_ret)

            weekly_nav=(weekly_ret+1).cumprod()

            annual_ret, max_drawback=self.calculate_nav_stats(weekly_nav)

            pool_stats=self.combinethestats(annual_ret,std,downsiderisk,max_drawback)

        else:

            sql=""" select avg(hb1y) as hb1y,tjyf,ejfl from ( select a.hb1y ,a.tjyf,b.ejfl from st_hedge.t_st_sm_yhb a 
            left join st_hedge.t_st_jjxx b  on a.jjdm=b.jjdm  
            where a.jjdm in ({0}) and a.tjyf>='{1}' and a.tjyf<='{2}' and a.hb1y<=300 and a.hb1y>=-300) c group by tjyf,ejfl
            """.format(util.list_sql_condition(pool_list),self.start_date,self.end_date)
            weekly_ret=hbdb.db2df(sql,db='highuser').pivot_table('hb1y','tjyf','ejfl')
            weekly_ret=weekly_ret[(weekly_ret['1001'].notnull()) & (weekly_ret['1002'].notnull())]

            weekly_ret.columns = ['股票多头私募基金','股票量化私募基金']
            weekly_ret = weekly_ret / 100
            std = weekly_ret.std(axis=0) * np.sqrt(12)
            downsiderisk = self.get_downside_risk(weekly_ret) * np.sqrt(12)

            weekly_nav = (weekly_ret + 1).cumprod()

            time_delta = (datetime.datetime.strptime(str(weekly_nav.index[-1])+'01'
                                                     , '%Y%m%d') - datetime.datetime.strptime(str(weekly_nav.index[0])+'01'
                                                                                              , '%Y%m%d')).days / 365

            annual_ret = np.power(weekly_nav.iloc[-1], 1 / time_delta) - 1
            max_drawback = (self.get_max_draw_back(weekly_nav))

            pool_stats = pd.merge(annual_ret.to_frame('年化收益')
                                  , std.to_frame('年化波动率'), how='inner', left_index=True, right_index=True)
            pool_stats = pd.merge(pool_stats
                                  , downsiderisk, how='inner', left_index=True, right_index=True)
            pool_stats = pd.merge(pool_stats
                                  , max_drawback, how='inner', left_index=True, right_index=True)
            pool_stats['夏普比率'] = pool_stats['年化收益'] / pool_stats['年化波动率']
            pool_stats['索提诺比率'] = pool_stats['年化收益'] / pool_stats['下行波动率']
            pool_stats['卡尔玛比率'] = pool_stats['年化收益'] / pool_stats['最大回撤']



        return  pool_stats,weekly_nav[ pool_stats.index.tolist()],desc

if __name__ == '__main__':

    # jjdm_list=hbdb.db2df("select jjdm,jjjc,glrm,ejfl from st_hedge.t_st_jjxx where clrq<='20180830' and ejfl in ('1001','1002') and zzrq is null  "
    #                      ,db='highuser')
    #
    #
    # year_ret=hbdb.db2df("select jjdm,tjnf as 统计年份,hb1n as 年收益 from st_hedge.t_st_sm_nhb_ls where tjnf in ('2019','2020','2021') and jjdm in ({}) and hblb=1 and hb1n!=99999"
    #                     .format(util.list_sql_condition(jjdm_list['jjdm'].tolist())),db='highuser').pivot_table('年收益','jjdm','统计年份')
    #
    # sql="select jjdm,hb1y,tjyf from st_hedge.t_st_sm_yhb where jjdm in ({}) and tjyf>='202201' and tjyf<='202206' and hb1y!=99999 "\
    #     .format(util.list_sql_condition(year_ret.index.tolist()))
    # toyear_ret=hbdb.db2df(sql,db='highuser')
    # toyear_ret['hb1y']=toyear_ret['hb1y']/100+1
    # toyear_ret['202206']=(toyear_ret.groupby('jjdm').cumprod()-1)*100
    # toyear_ret=toyear_ret.drop_duplicates('jjdm',keep='last').drop(['tjyf','hb1y'],axis=1)
    #
    # year_ret=pd.merge(year_ret,toyear_ret,how='left',on='jjdm')
    # year_ret['total_ret']=((year_ret[2019]/100+1)*\
    #                       (year_ret[2020]/100+1)*\
    #                       (year_ret[2021]/100+1)*\
    #                       (year_ret['202206']/100+1)-1)*100
    # year_ret = pd.merge(year_ret, jjdm_list, how='left', on='jjdm')
    #
    # company_info=hbdb.db2df("select jgdm,jgmc from st_main.t_st_gg_jgxx where jgdm in ({})"
    #                         .format(util.list_sql_condition(year_ret['glrm'].unique().tolist()))
    #                         ,db='alluser')
    # final_df = pd.merge(year_ret, company_info, how='left', left_on='glrm',right_on='jgdm')
    # final_df=final_df[final_df['total_ret'].notnull()].drop(['glrm','jgdm'],axis=1)
    # final_df=final_df.sort_values('total_ret',ascending=False)[500:1000]
    # final_df.to_excel('私募股多收益统计.xlsx',index=False)
    # print('')


    #fund return analysis
    #calculate the ret bais for mutual funds
    # for asofdate in ['20151231','20160630','20161231','20170630','20171231','20180630'
    #         ,'20181231','20190630','20191231'
    #         ,'20200630','20201231','20210630','20211231','20220630']:
    #     fa=Fund_ret_analysis(asofdate=asofdate)
    #     fa.save_index_difference2db(asofdate=asofdate,time_length=7)

    # fpr=Fund_performance_research(asofdate='20220630',start_date='201301',end_date='202206')
    # plot = functionality.Plot(1200, 600)

    #get prv index diviation from DB
    # for index in ['1001']:
    #
    #     sql="""select jjdm,hb1y,pmbfw,tjyf from st_hedge.t_st_sm_zsyb
    #     where tjyf>='201301' and tjyf<='202206' and jjfl='{}' and pmbfw>=75 and pmbfw<=76 """.format(index)
    #     desc=hbdb.db2df(sql,db='highuser')
    #
    #
    #     desc=desc.sort_values('pmbfw')
    #     desc=desc.drop_duplicates('tjyf',keep='first')
    #     desc=desc.sort_values('tjyf')
    #     desc_prv=desc.copy()
    #     desc_prv[index+'_25%']=(desc['hb1y']/100).values
    #
    #     sql="""select jjdm,hb1y,pmbfw,tjyf from st_hedge.t_st_sm_zsyb
    #     where tjyf>='201301' and tjyf<='202206' and jjfl='{}' and pmbfw>=50 and pmbfw<=51 """.format(index)
    #     desc=hbdb.db2df(sql,db='highuser')
    #     desc=desc.sort_values('pmbfw')
    #     desc=desc.drop_duplicates('tjyf',keep='first')
    #     desc = desc.sort_values('tjyf')
    #     desc_prv[index+'_50%'] = (desc['hb1y'] / 100).values
    #
    #
    #     sql="""select jjdm,hb1y,pmbfw,tjyf from st_hedge.t_st_sm_zsyb
    #     where tjyf>='201301' and tjyf<='202206' and jjfl='{}' and pmbfw>=25 and pmbfw<=26 """.format(index)
    #     desc=hbdb.db2df(sql,db='highuser')
    #     desc=desc.sort_values('pmbfw')
    #     desc=desc.drop_duplicates('tjyf',keep='first')
    #     desc = desc.sort_values('tjyf')
    #     desc_prv[index+'_75%'] = (desc['hb1y'] / 100).values
    #
    #     desc_prv=desc_prv.set_index('tjyf')
    #     desc_prv[index+'75分位数与中位数偏离']=desc_prv[index+'_75%']-desc_prv[index+'_50%']
    #     desc_prv[index+'25分位数与中位数偏离']=desc_prv[index+'_25%']-desc_prv[index+'_50%']
    #     desc_prv.columns=[x.replace(index,'私募股多') for x in desc_prv.columns]
    #     # plot.plotly_line_style(desc_prv[[index+'_75%',index+'_25%']],index+'个基偏离')

    #read pool data from local file
    # quant_pool_in=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-08\私募量化基金池 - 202207.xlsx"
    #                          ,sheet_name='量化池列表')[['入池时间','基金代码','二级策略']]
    # quant_pool_out=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-08\私募量化基金池 - 202207.xlsx"
    #                          ,sheet_name='出池记录')[['入池时间','基金代码','出池时间','二级策略']]
    # quant_pool=pd.concat([quant_pool_out,quant_pool_in],axis=0)
    # quant_pool=quant_pool[(quant_pool['二级策略'].isin(['500指数增强','1000指数增强','300指数增强']))]
    # quant_pool['入池时间']=quant_pool['入池时间'].astype(str).str.replace('-','').str[0:6]
    # quant_pool['出池时间'] = quant_pool['出池时间'].astype(str).str.replace('-', '').str[0:6]
    # quant_pool.drop_duplicates('基金代码', inplace=True)
    #
    # prv_pool_in=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-08\私募股多池202207.xlsx"
    #                        ,sheet_name='主观池列表')[['入池时间','基金代码','一级策略']]
    # prv_pool_out=pd.read_excel(r"C:\Users\xuhuai.zhe\Documents\WXWork\1688858146292774\Cache\File\2022-08\私募股多池202207.xlsx"
    #                        ,sheet_name='一般推荐(出池) ')[['入池时间','基金代码','出池时间','一级策略']]
    # prv_pool_out=prv_pool_out[(prv_pool_out['入池时间'].notnull())&
    #                           (prv_pool_out['出池时间'].notnull())]
    # prv_pool_out=prv_pool_out[prv_pool_out['一级策略']=='股票型']
    # prv_pool = pd.concat([prv_pool_out, prv_pool_in], axis=0).sort_values('入池时间')
    # prv_pool['入池时间']=prv_pool['入池时间'].astype(str).str.replace('-','').str[0:6]
    # prv_pool['出池时间'] = prv_pool['出池时间'].astype(str).str.replace('-', '').str[0:6]
    # prv_pool.drop_duplicates('基金代码',inplace=True)
    #
    #
    # sql="select jjdm,hb1y,tjyf from st_hedge.t_st_sm_yhb where jjdm in ({}) and tjyf>='201901' and tjyf<='202206' and hb1y!=99999"\
    #     .format(util.list_sql_condition(prv_pool['基金代码'].tolist()))
    # prv_pool_nav=hbdb.db2df(sql,db='highuser')
    # prv_pool_nav=pd.merge(prv_pool_nav,prv_pool,how='left'
    #                       ,left_on='jjdm',right_on='基金代码')
    # prv_pool_nav=prv_pool_nav[(prv_pool_nav['入池时间']<prv_pool_nav['tjyf'])
    #                           &(prv_pool_nav['出池时间']>=prv_pool_nav['tjyf'])]
    # prv_pool_nav=prv_pool_nav.groupby('tjyf').mean()['hb1y'].to_frame('私募股多池')/100
    #
    # #
    # sql="select jjdm,hb1y,tjyf from st_hedge.t_st_sm_yhb where jjdm in ({}) and tjyf>='202111' and tjyf<='202208' and hb1y!=99999"\
    #     .format(util.list_sql_condition(quant_pool['基金代码'].tolist()))
    # quant_pool_nav=hbdb.db2df(sql,db='highuser')
    # quant_pool_nav=pd.merge(quant_pool_nav,quant_pool,how='left'
    #                       ,left_on='jjdm',right_on='基金代码')
    # quant_pool_nav=quant_pool_nav[(quant_pool_nav['入池时间']<quant_pool_nav['tjyf'])
    #                           &(quant_pool_nav['出池时间']>=quant_pool_nav['tjyf'])]
    # quant_pool_nav=quant_pool_nav.groupby(['二级策略','tjyf']).mean()['hb1y'].to_frame('量化池')/100



    #
    #
    # #get product info from DB
    # sql="select cpdm,hb1y,tjyf from st_portfolio.t_st_zh_clzhyhb where cpdm in ('tzzhczx','tzzhjjx') and tjyf>='201301' and tjyf<='202206' and hb1y!=99999"
    # jj_nav_mu=hbdb.db2df(sql,db='portfoliouser').pivot_table('hb1y','tjyf','cpdm')
    # jj_nav_mu.columns=['牛基宝成长型','牛基宝进取型']
    # jj_nav_mu.index=jj_nav_mu.index.astype(str)
    # prv_fof_list=['S29494','SGG703']
    # sql="select jjdm,hb1y,tjyf from st_hedge.t_st_sm_yhb where jjdm in ('S29494','SGG703') and tjyf>='201301' and tjyf<='202206' and hb1y!=99999"
    # jj_nav_prv=hbdb.db2df(sql,db='highuser').pivot_table('hb1y','tjyf','jjdm')
    # jj_nav_prv.columns=['新方程星动力S7','新方程量化中小盘精选']
    #
    #
    # jj_nav=pd.merge(jj_nav_mu,jj_nav_prv,how='inner',left_index=True,right_index=True)
    # jj_nav=jj_nav[jj_nav.isnull().sum(axis=1) == 0]/100
    #
    #
    # jj_nav=pd.merge(jj_nav,prv_pool_nav,how='inner',left_index=True,right_index=True)
    # jj_nav = pd.merge(jj_nav, quant_pool_nav, how='inner', left_index=True, right_index=True)
    #
    # #get self_defined mutual stock index
    # pool_stats_mu,weekly_nav_mu,desc=fpr.fund_pool_stats(pool_list=util.get_stock_funds_pool(asofQ='20220630'
    #                                                                         ,time_length=7,still_exist=False))
    #
    #
    # sql="select zsdm,tjyf,jjsl,hb1y,spjg from st_hedge.t_st_sm_hmzs where zsdm in ('HB1001','HB1002') and tjyf>=201301 and tjyf<=202206 and hb1y!=99999"
    # prv_ret=hbdb.db2df(sql,db='highuser').pivot_table('hb1y','tjyf','zsdm')
    # prv_ret=prv_ret/100
    # weekly_nav_prv=((prv_ret+1).cumprod())[['HB1001']]
    # weekly_nav_prv.rename(columns={'HB1001':'好买私募股多指数','HB1002':'好买量化多头'},inplace=True)
    #
    # prv_ret.columns=['好买私募股多指数','好买量化多头指数']
    # std,downsiderisk=fpr.calculate_ret_stats(prv_ret)
    # annual_ret, max_drawback = fpr.calculate_nav_stats(weekly_nav_prv)
    # pool_stats = fpr.combinethestats(annual_ret, std, downsiderisk, max_drawback)

    #
    # pool_stats=pd.concat([pool_stats_mu,pool_stats]
    #                      ,axis=0)
    #
    # weekly_nav_mu.index = weekly_nav_mu.index.astype(str)
    # weekly_nav=pd.merge(weekly_nav_mu,weekly_nav_prv
    #                     ,how='inner',left_index=True,right_index=True)
    # weekly_nav['year'] = weekly_nav.index.str[0:4]
    # year_ret=weekly_nav.drop_duplicates('year', keep='last')
    # weekly_nav.drop('year',axis=1,inplace=True)
    #
    # tempdata=year_ret.iloc[0][['金工公募偏股型基金指数','万得偏股混合型指数','上证指数','好买私募股多指数']].values-1
    # year_ret=year_ret[['金工公募偏股型基金指数','万得偏股混合型指数','上证指数','好买私募股多指数']].pct_change()
    # year_ret.loc[year_ret.index[0]]=tempdata
    # year_ret['year'] = year_ret.index.str[0:4]
    #
    # mubetaprv=year_ret[year_ret['金工公募偏股型基金指数']
    #                    >year_ret['好买私募股多指数']][['金工公募偏股型基金指数','好买私募股多指数','上证指数','year']]
    # prvbetamu=year_ret[year_ret['金工公募偏股型基金指数']
    #                    <year_ret['好买私募股多指数']][['金工公募偏股型基金指数','好买私募股多指数','上证指数','year']]
    #
    # for col in ['金工公募偏股型基金指数','上证指数','好买私募股多指数']:
    #     mubetaprv[col]= mubetaprv[col].map("{:.2%}".format)
    #     prvbetamu[col]= prvbetamu[col].map("{:.2%}".format)
    #
    # plot.plotly_table(mubetaprv, 600, '')
    # plot.plotly_table(prvbetamu, 600, '')
    #
    #
    # jj_nav=pd.merge(jj_nav,prv_ret,how='inner',left_index=True,right_index=True)
    # weekly_ret = weekly_nav_mu.pct_change()
    #
    #
    # jj_nav=pd.merge(jj_nav,weekly_ret[['金工公募偏股型基金指数']],how='inner',left_index=True,right_index=True)
    # std,downsiderisk=fpr.calculate_ret_stats(jj_nav)
    # jj_nav=(jj_nav+1).cumprod()
    # annual_ret, max_drawback=fpr.calculate_nav_stats(jj_nav)
    # jj_stats = fpr.combinethestats(annual_ret, std, downsiderisk, max_drawback)
    #
    #
    # for col in ['年化收益', '年化波动率', '下行波动率', '最大回撤']:
    #     pool_stats[col]= pool_stats[col].map("{:.2%}".format)
    #     jj_stats[col] = jj_stats[col].map("{:.2%}".format)
    # for col in ['夏普比率', '索提诺比率', '卡尔玛比率']:
    #     pool_stats[col]= pool_stats[col].map("{:.2}".format)
    #     jj_stats[col] = jj_stats[col].map("{:.2}".format)
    #
    # plot=functionality.Plot(1200,600)
    # plot.plotly_line_style(weekly_nav,'内部指数净值走势')
    # plot.plotly_line_style(jj_nav[['牛基宝进取型','牛基宝成长型','金工公募偏股型基金指数','好买私募股多指数','好买量化多头指数']]
    #                        , '公募产品业绩走势')
    # plot.plotly_line_style(jj_nav[['新方程星动力S7','新方程量化中小盘精选','量化池','私募股多池','好买量化多头指数','金工公募偏股型基金指数','好买私募股多指数']]
    #                        , '私募产品与池业绩走势')
    # plot.plotly_table(pool_stats.reset_index().sort_values('年化收益',ascending=False),1200,'')
    # plot.plotly_table(jj_stats.loc[['牛基宝进取型','牛基宝成长型','金工公募偏股型基金指数','好买私募股多指数','好买量化多头指数']].reset_index().sort_values('年化收益',ascending=False),1200,'')
    # plot.plotly_table(jj_stats.loc[['新方程星动力S7','新方程量化中小盘精选','量化池','私募股多池','好买量化多头指数','金工公募偏股型基金指数','好买私募股多指数']].reset_index().sort_values('年化收益',ascending=False),1200,'')
    #
    # desc.index=desc.index.astype(str)
    # desc=pd.merge(desc.rename(columns={'75%':'公募偏股基金75分位数相对中位数偏离'
    #     ,'25%':'公募偏股基金25分位数相对中位数偏离'})
    #               ,desc_prv,how='inner',left_index=True,right_index=True)
    #
    # plot.plotly_line_style(desc[['私募股多75分位数与中位数偏离','公募偏股基金75分位数相对中位数偏离'
    #     ,'私募股多25分位数与中位数偏离','公募偏股基金25分位数相对中位数偏离']], '指数内个基月收益偏离')
    # desc=desc[['公募偏股基金75分位数相对中位数偏离','公募偏股基金25分位数相对中位数偏离',
    #     '私募股多75分位数与中位数偏离','私募股多25分位数与中位数偏离']].describe()
    # for col in ['公募偏股基金75分位数相对中位数偏离','公募偏股基金25分位数相对中位数偏离',
    #     '私募股多75分位数与中位数偏离','私募股多25分位数与中位数偏离']:
    #     desc[col]=desc[col].map("{:.2%}".format)
    # plot.plotly_table(desc.iloc[1:],1000,'')



    # tt=Timing_trade()
    # tt.style_timing('20120101','20220630',0.15)
    #
    #
    # jjdm_list=['000739','001476','001856','001975','002340','005241','006624','007449','008901','011251'
    #         ,'161606','450004','519126','519133']
    # jjret=get_daily_jjret(jjdm_list,start_date='20210930',end_date='20222830')
    #
    # weight_list= [0.1065,0,0.1052,0.1064,0.1121,0,0.1094,0,0,0,0.1113,0.1179,0.1077,0.1117]
    # weight_list2=[0.111111111111111,0.05,0.1111,0.111111111111111,0.111111111111111,0.111,0.06,0,0,0.1123,0,0.111111111111111,0,0.111111111111111]
    # #weight_list2=[0.15,0.135522885900964,0,0.149999999999999,0.0948139924093508,0.0794888864178141,0.0362468967220349,0.020162885970587,0.000389419317164471,0.0644011130693203,0.15,0.118973920192762]
    #
    # for i in range(len(jjdm_list)):
    #     jjret.loc[jjret['jjdm']==jjdm_list[i],'org_w']=weight_list[i]
    #     jjret.loc[jjret['jjdm'] == jjdm_list[i], 'new_w'] = weight_list2[i]
    # #
    # jjret['hbdr_org']=jjret['hbdr']*jjret['org_w']
    # jjret['hbdr_new'] = jjret['hbdr'] * jjret['new_w']
    # jjret=jjret.groupby('jzrq').sum()[['hbdr_org', 'hbdr_new']]
    # jjret = jjret.iloc[0:-2]
    # #
    # #
    # index_list=['399370','399371','399314','399315','399316','885001','CBA00301']
    #
    # index_ret=get_daily_indexnav(index_list,start_date='20210930',end_date='20220830')
    # index_ret=index_ret.pivot_table('spjg','jyrq','zqdm')
    # for col in index_list:
    #     jjret[col]= (index_ret[col].pct_change() * 100).tolist()
    #
    #
    # ols_result=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    # col_list=['g_885','v_885','b_885','m_885','s_885'
    #     ,'g_n','v_n','b_n','m_n','s_n'
    #     ,'g_o','v_o','b_o','m_o','s_o']
    # jjret=jjret.iloc[1:]
    #
    # time_lap=20
    # ols_df= pd.DataFrame(index=jjret.index[time_lap:],columns=col_list)
    #
    # for i in range(time_lap,len(jjret)):
    #     j=0
    #     for y in ['885001','hbdr_new','hbdr_org']:
    #         result = sm.OLS(jjret.iloc[i-time_lap:i][y].values
    #                         , jjret.iloc[i-time_lap:i][['399370','399371','CBA00301']].values).fit().params.tolist()
    #         ols_result[j*5].append(result[0])
    #         ols_result[j*5+1].append(result[1])
    #
    #         result = sm.OLS(jjret.iloc[i-time_lap:i][y].values
    #                         , jjret.iloc[i-time_lap:i][['399314','399315','399316','CBA00301']].values).fit().params.tolist()
    #         ols_result[j*5+2].append(result[0])
    #         ols_result[j*5+3].append(result[1])
    #         ols_result[j*5+4].append(result[2])
    #
    #         j+=1
    #
    # for i in range(len(col_list)):
    #     ols_df[col_list[i]]=ols_result[i]
    #
    # ols_df.to_excel('ols_result_{}_new.xlsx'.format(time_lap))






    # plot = functionality.Plot(1200, 600)
    #
    # sql = "SELECT * from 885001_hbs_style_exp where jsrq<='20211231'"
    # df885 = pd.read_sql(sql, con=localdb)
    # df885.drop_duplicates(['jsrq', 'style_type', 'jjdm'], inplace=True)
    # df885['month'] = df885['jsrq'].str[4:6]
    # df885 = df885[df885['month'].isin(['06', '12'])]
    # df885 = pd.merge(df885, df885.groupby(['jjdm', 'jsrq']).sum()['zjbl'].reset_index(), how='left',
    #                  on=['jjdm', 'jsrq'])
    # df885['zgbl'] = df885['zjbl_x'] / df885['zjbl_y']
    # df885 = df885.groupby(['jsrq', 'style_type']).mean()['zgbl'].reset_index().pivot_table('zgbl', 'jsrq', 'style_type')
    # plot.plotly_line_style(df885, '885001风格占比时序')
    #
    # sql = "SELECT * from 885001_key_hbs_style_exp where jsrq<='20211231'"
    # df886 = pd.read_sql(sql, con=localdb)
    # df886.drop_duplicates(['jsrq', 'style_type', 'jjdm'], inplace=True)
    # df886['month'] = df886['jsrq'].str[4:6]
    # df886 = df886[df886['month'].isin(['06', '12'])]
    # df886 = pd.merge(df886, df886.groupby(['jjdm', 'jsrq']).sum()['zjbl'].reset_index(), how='left',
    #                  on=['jjdm', 'jsrq'])
    # df886['zgbl'] = df886['zjbl_x'] / df886['zjbl_y']
    # df886 = df886.groupby(['jsrq', 'style_type']).mean()['zgbl'].reset_index().pivot_table('zgbl', 'jsrq', 'style_type')
    #
    # df_gh=pd.merge(df885,df886,how='inner',on='jsrq')
    #
    # df_gh['diff'] =(df_gh['成长_x']-df_gh['成长_y']).abs()
    # df_gh['xret']=df_gh['成长_x'].diff(1)
    # df_gh['yret'] = df_gh['成长_y'].diff(1)
    # df_gh['diffret'] =(df_gh['xret']-df_gh['yret']).abs()
    #
    #
    # plot.plotly_line_style(df885, '885001风格占比时序')



    # #
    # tt=Timing_trade()
    # tt.style_timing('20120101','20220630',0.15)


    # fp=Fund_performance_research(start_date='20150101',end_date='20220713')
    # monthly_result,monthly_his,\
    # yearly_result,yearly_his=fp.difference_between_product("rydm='30319776'")
    #
    # remove_list=yearly_result.columns[yearly_result.loc['count']<5].tolist()
    # yearly_his.drop(remove_list,axis=1,inplace=True)
    # monthly_his.drop(remove_list, axis=1, inplace=True)
    # interest_list=yearly_result.columns[yearly_result.loc['count']>=5].tolist()
    #
    # year_stats=yearly_his[interest_list].describe()
    # for col in year_stats.columns:
    #     year_stats[col]=year_stats[col].astype(float).map("{:.2%}".format)
    #
    #
    # scenario_list=\
    #     fp.define_scenario(monthly_his,yearly_his,fp.index_list)
    #
    # plot = functionality.Plot(1500,400)
    # title_list=['成长-价值（月）','大盘-中小盘（月）','景气-衰退（月）'
    #     ,'成长-价值（年）','大盘-中小盘（年）','景气-衰退（年）']
    #
    # plot.plotly_table(year_stats.reset_index(),1000,'')
    #
    # for i in range(6):
    #     plot.plotly_table(scenario_list[i],3000,title_list[i])
    #
    # plot1=functionality.Plot(1200,600)
    # plot1.plotly_line_multi_yaxis(yearly_his[interest_list+['成长','价值','tjnf']].rename(columns={'tjnf':'日期'})
    #                              ,'年度业绩时序',['成长','价值'])
    # plot2 = functionality.Plot(2400, 600)
    # monthly_his['tjyf'] = monthly_his['tjyf'].astype(str)
    # plot2.plotly_line_multi_yaxis(monthly_his[interest_list+['成长','价值','tjyf']].rename(columns={'tjyf':'日期'})
    #                              ,'月度业绩时序',['成长','价值'])
    #
    # plot1.plotly_line_multi_yaxis(yearly_his[interest_list+['中小盘','大盘','tjnf']].rename(columns={'tjnf':'日期'})
    #                              ,'年度业绩时序',['中小盘','大盘'])
    # plot2.plotly_line_multi_yaxis(monthly_his[interest_list+['中小盘','大盘','tjyf']].rename(columns={'tjyf':'日期'})
    #                              ,'月度业绩时序',['中小盘','大盘'])
    #
    # plot1.plotly_line_multi_yaxis(yearly_his[interest_list + ['国证1000', 'tjnf']].rename(columns={'tjnf': '日期'})
    #                               , '年度业绩时序', ['国证1000'])
    # plot2.plotly_line_multi_yaxis(monthly_his[interest_list + ['国证1000', 'tjyf']].rename(columns={'tjyf': '日期'})
    #                               , '月度业绩时序', ['国证1000'])

    print('')

    #fra=Fund_return_analysis()
    #fra.hurst_index('20220331')
    #fra.return_rank_analysis('20220331')

    # #pri_basis=hbdb.db2df("select jjdm,jjjc from st_hedge.t_st_jjxx where clbz='1' and cpfl='4' and jjzt='0' and jjfl='1' and clrq<='20200506'"
    #                      ,db='highuser')


    #style_exp_simpleols_foroutsideuser_mu()
    style_exp_simpleols_foroutsideuser_prv()

    # df1=pd.read_excel(r"C:\Users\xuhuai.zhe\Downloads\股多-估值表-20220428.xlsx")
    # jjdm_con=util.list_sql_condition(df1['基金代码'].values.tolist())
    # df2=hbdb.db2df("select jjdm,weight,trade_date from st_hedge.r_st_sm_subjective_fund_holding where jjdm in ({0})"
    #                .format(jjdm_con),db='highuser')
    # df2['flag'] = 0
    # df2.loc[df2['weight'] == 99999, 'flag'] = 1
    # df2=df2.groupby(['jjdm','trade_date']).sum().reset_index()
    # df2['trade_date']=df2['trade_date'].astype(str)+','
    # df2=pd.merge(df2.groupby('jjdm')['flag'].mean().reset_index(),
    #              df2.groupby('jjdm')['trade_date'].sum().reset_index(),how='inner',on='jjdm')
    # df2.loc[df2['flag']==1,'flag']='解析失败'
    # df2.loc[df2['flag']==0,'flag']='解析成功'
    #
    # df=pd.merge(df1,df2,how='left',left_on='基金代码',right_on='jjdm').drop('jjdm',axis=1)
    # df.to_excel('对比结果新.xlsx')
    # print('')

    #calculate the return for different scenarios
    # sr = Scenario_return()
    # stock_jjdm_list=util.get_mutual_stock_funds('20211231')
    # stock_jjdm_list.sort()
    # benchmark_ret = sr.get_histroy_scenario_ret()
    # saved_df=pd.DataFrame()
    # for jjdm in stock_jjdm_list:
    #     scenario_ret=sr.pessimistic_ret(jjdm,benchmark_ret,'20120101')
    #     saved_df=pd.concat([saved_df,scenario_ret],axis=0)
    #
    # insert_date_list=saved_df['rqzh'].unique().tolist()
    # localdb.execute("delete from scenario_ret where rqzh in ({})".format(util.list_sql_condition(insert_date_list)))
    # saved_df.to_sql('scenario_ret',index=False,con=localdb,if_exists='append')

    #barra return daily return
    #factor_ret_df=get_barra_daily_ret()

    #write style exp into local db
    # se = Style_exp('20211231','M')
    # se = Style_exp('20211231', 'Q')

    #style exp analysis
    #

    # sql="select * from value_exposure where jjdm='002849' "
    # test=pd.read_sql(sql,con=localdb)[['399370','399371','CBA00301','date']]
    # test.set_index('date',inplace=True)
    # plot=functionality.Plot(2000,1000)
    # plot.plotly_line_style(test,'asdf')
    #

    # #style property calculation
    # jjdm_list=util.get_mutual_stock_funds('20211231')
    # sa=Style_analysis(jjdm_list,fre='M',time_length=3)
    # sa.style_shift_analysis()
    # sa=Style_analysis(jjdm_list,fre='Q',time_length=3)
    # sa.style_shift_analysis()


    # sa.save_style_property2localdb()
    # #
    # jjdm_list = util.get_mutual_stock_funds('20211231')
    # sa=Style_analysis(jjdm_list,asofdate='20220310',fre='M',time_length=3)
    # sa.save_style_property2localdb()
    # sa=Style_analysis(jjdm_list,asofdate='20220310',fre='Q',time_length=3)
    # sa.save_style_property2localdb()


    #manager hsl and volume estimate

    # jjdm_list=util.get_mutual_stock_funds('20211231')
    # ma = Manager_volume_hsl_analysis(jjdm_list)




    # for fre in ['Q']:
    #     jjdm_list = util.get_mutual_stock_funds('20211231')
    #     ta = Theme_analysis(jjdm_list, fre=fre, time_length=3)
    #     ta.save_theme_property2localdb()

    # jjdm_list = ['000577', '000729', '001410', '001667', '001856', '002340', '005233', '005267', '005827', '005968', '006624', '163415', '450004', '450009', '519126', '519133', '700003']
    # sql = "select * from nav_style_property_theme"
    # df = pd.read_sql(sql, con=localdb)
    # df = df[df['jjdm'].isin(jjdm_list)].sort_values(['jjdm', 'fre'])
    # df.to_excel('C:/Users/wenqian.xu/Desktop/test/test.xlsx')

