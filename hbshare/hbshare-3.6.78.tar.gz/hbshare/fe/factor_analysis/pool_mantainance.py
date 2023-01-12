import numpy as np
import pandas as pd
from hbshare.fe.XZ import db_engine as dbeng
from hbshare.fe.XZ import functionality


util=functionality.Untils()
hbdb=dbeng.HBDB()
localdb = dbeng.PrvFunDB().engine

def save_mutual_core_pool2locabdb(asofdate):

    data=pd.read_excel(r"C:\Users\xuhuai.zhe\Desktop\核心池列表-20220629_风格.xlsx")

    data=data[['基金代码','基金名称']]
    data['基金经理']=''
    data['asofdate']=asofdate

    data['基金代码']=data['基金代码'].astype(str).str[0:6]

    data.to_sql('core_pool_history',
                con=localdb,index=False,if_exists='append')

def save_wenjian_pool2locabdb(asofdate,factor_name):

    pool_size = 10

    raw_df=pd.read_sql("select * from factor_year_rank_quantile",
                       con=localdb)


    localdb.execute("delete from conservative_pool_{1}_history where asofdate='{0}'".format(asofdate,factor_name.split('%')[0]))

    raw_df=raw_df[(raw_df['date']==asofdate)&(raw_df['count']==17)].sort_values(factor_name
                                               ,ascending=False)[0:pool_size][['jjdm',factor_name]]
    raw_df['asofdate']=asofdate

    raw_df.to_sql('conservative_pool_{0}_history'.format(factor_name.split('%')[0]),con=localdb,index=False,if_exists='append')

def save_wenjian_pool2locabdb(asofdate,factor_name):

    pool_size = 10

    raw_df=pd.read_sql("select * from factor_year_rank_quantile",
                       con=localdb)


    localdb.execute("delete from conservative_pool_{1}_history where asofdate='{0}'".format(asofdate,factor_name.split('%')[0]))

    raw_df=raw_df[(raw_df['date']==asofdate)&(raw_df['count']==17)].sort_values(factor_name
                                               ,ascending=False)[0:pool_size][['jjdm',factor_name]]
    raw_df['asofdate']=asofdate

    raw_df.to_sql('conservative_pool_{0}_history'.format(factor_name.split('%')[0]),con=localdb,index=False,if_exists='append')

def save_momentum_pool2locabdb(asofdate):

    pool_size = 20
    factor_name='year_logret'
    fre='Q'
    raw_df=pd.read_sql("select * from factor_year_ret where  {0} is not null "
                       .format(factor_name)
                       ,con=localdb)


    localdb.execute("delete from momentum_pool_history where asofdate='{}'".format(asofdate))

    raw_df=raw_df[(raw_df['date']==asofdate)].sort_values(factor_name
                                               ,ascending=False)[0:pool_size][['jjdm',factor_name]]
    raw_df['asofdate']=asofdate

    raw_df.to_sql('momentum_pool_history',con=localdb,index=False,if_exists='append')

def save_info_ratio_pool2locabdb(asofdate):

    pool_size = 50
    factor_name='info_ratio'
    fre='Q'
    raw_df=pd.read_sql("select * from factor_infor_ratio where zblb='2101'",
                       con=localdb)


    localdb.execute("delete from info_ratio_pool_history where asofdate='{}'".format(asofdate))

    raw_df=raw_df[(raw_df['date']==int(asofdate))].sort_values(factor_name
                                               ,ascending=False)[0:pool_size][['jjdm',factor_name]]
    raw_df['asofdate']=asofdate

    raw_df.to_sql('info_ratio_pool_history',con=localdb,index=False,if_exists='append')

if __name__ == '__main__':


    # save_info_ratio_pool2locabdb('20211227')
    # save_info_ratio_pool2locabdb('20220328')
    # save_info_ratio_pool2locabdb('20220627')

    #save_momentum_pool2locabdb('20220630')
    #
    # save_wenjian_pool2locabdb('20220630','25%')
    # save_wenjian_pool2locabdb('20220331','25%')
    # save_wenjian_pool2locabdb('20211231','25%')
    #
    # save_wenjian_pool2locabdb('20220630','10%')
    # save_wenjian_pool2locabdb('20220331','10%')
    # save_wenjian_pool2locabdb('20211231','10%')

    #save_mutual_core_pool2locabdb('202206')

    last_2years = '20191231'


    #ind cons
    sql="SELECT jjdm,max(`占持仓比例(时序均值)`)as max_w from jjpic_industry_detail_1 GROUP BY jjdm "
    d1=pd.read_sql(sql,con=localdb)

    old_jjdm_list=d1['jjdm'].unique().tolist()

    ticker_con = "'" + "','".join(old_jjdm_list) + "'"

    sql = "select jjdm,min(gptzzjb) from st_fund.t_st_gm_zcpz where jsrq<='{0}' and jsrq>={1} and jjdm in ({2}) group by jjdm" \
        .format('20211231', '20200630', ticker_con)

    tempdf = hbdb.db2df(sql, db='funduser')
    old_jjdm_list = tempdf[tempdf['min(gptzzjb)'] >= 60]['jjdm'].tolist()


    d1=d1[d1['max_w']<=0.6]

    sql="SELECT * from jjpic_theme_p"
    d2=pd.read_sql(sql,con=localdb)
    d2['max_w'] = d2[['大金融', '消费', 'TMT', '周期', '制造']].max(axis=1)
    d2 = d2[d2['max_w'] <= 0.7]

    #size cons
    sql="select jjdm,jjjzc from st_fund.t_st_gm_zcpz where jsrq='20211231' and jjdm in ({})"\
        .format(util.list_sql_condition(old_jjdm_list))

    d3=hbdb.db2df(sql,db='funduser')
    d3=d3[(d3['jjjzc']<=50000000000)]

    #manager length
    sql="select jjdm,rydm from st_fund.t_st_gm_jjjl where jjdm in ({}) and ryzw='基金经理' and lrrq>='20211231'"\
        .format(util.list_sql_condition(old_jjdm_list))
    d4=hbdb.db2df(sql,db='funduser')
    sql="select distinct(rydm) from st_fund.t_st_gm_jjjl where rydm in ({0}) and rzrq<='20161231' "\
        .format(util.list_sql_condition(d4['rydm'].astype(str).unique().tolist()))
    d44=hbdb.db2df(sql,db='funduser')
    d44['flag']=1
    d4=pd.merge(d4,d44,how='left',on='rydm')
    d4=d4[d4['flag'].notnull()]


    d=pd.merge(d1,d2,how='inner',on='jjdm')
    d=pd.merge(d,d3,how='inner',on='jjdm')
    d=pd.merge(d,d4,how='inner',on='jjdm')
    new_jjdm_list=d['jjdm'].unique().tolist()

    plot=functionality.Plot(600,600)
    sql="SELECT avg(`成长绝对暴露(持仓)`) as `成长持仓占比`, avg(`价值绝对暴露(持仓)`) as `价值持仓占比` from jjpic_value_p_hbs  "
    pool_value_pic=pd.read_sql(sql,con=localdb)
    plot.plotly_pie(pool_value_pic.T.rename(columns={0:'weight'}),'成长价值占比',save_local_file=True)

    sql="SELECT `成长绝对暴露(持仓)` as `成长持仓占比`, `价值绝对暴露(持仓)` as `价值持仓占比` from jjpic_value_p_hbs  "
    pool_value_pic=pd.read_sql(sql,con=localdb)
    plot.plotly_hist(pool_value_pic[['成长持仓占比']],'成长持仓占比',save_local_file=True)
    plot.plotly_hist(pool_value_pic[['价值持仓占比']],'价值持仓占比',save_local_file=True)


    sql="SELECT avg(`大盘绝对暴露(持仓)`) as `大盘持仓占比`, avg(`中盘绝对暴露(持仓)`) as `中盘持仓占比`,avg(`小盘绝对暴露(持仓)`) as `小盘持仓占比` from jjpic_size_p_hbs  "
    pool_value_pic=pd.read_sql(sql,con=localdb)
    plot.plotly_pie(pool_value_pic.T.rename(columns={0:'weight'}),'规模占比分布',save_local_file=True)

    sql="SELECT `大盘绝对暴露(持仓)` as `大盘持仓占比`, (`中盘绝对暴露(持仓)`+`小盘绝对暴露(持仓)`) as `中小盘持仓占比` from jjpic_size_p_hbs  "
    pool_value_pic=pd.read_sql(sql,con=localdb)
    plot.plotly_hist(pool_value_pic[['大盘持仓占比']],'大盘持仓占比',save_local_file=True)
    plot.plotly_hist(pool_value_pic[['中小盘持仓占比']],'中小盘持仓占比',save_local_file=True)


    sql="SELECT avg(`大金融`) as `大金融`, avg(`消费`) as `消费`,avg(TMT) as TMT,avg(`制造`) as `制造`,avg(`周期`) as `周期`  from jjpic_theme_p   "
    pool_theme_pic=pd.read_sql(sql,con=localdb)
    plot.plotly_pie(pool_theme_pic.T.rename(columns={0:'weight'}),'主题占比分布',save_local_file=True)

    edf=pd.read_excel(r"E:\GitFolder\hbshare\fe\mutual_analysis\均衡池_20211231.xlsx")
    edf2=pd.read_excel(r"E:\GitFolder\hbshare\fe\mutual_analysis\均衡池_20220331.xlsx")
    #
    # sql="select avg(hb1y) as bmk_old,tjyf from st_fund.t_st_gm_yhb where jjdm in ({}) and tjyf>='201612' and tjyf<='202206' and hb1y!=99999 group by tjyf"\
    #     .format(util.list_sql_condition(old_jjdm_list))
    # ret1=hbdb.db2df(sql,db='funduser')

    sql="select avg(hb1y) as bmk ,tjyf from st_fund.t_st_gm_yhb where jjdm in ({}) and tjyf>='201812' and tjyf<='202206' and hb1y!=99999 group by tjyf"\
        .format(util.list_sql_condition(new_jjdm_list))
    ret2=hbdb.db2df(sql,db='funduser')

    sql="select hb1y as 偏股混指数 ,tjyf from st_market.t_st_zs_yhb where zqdm='885001' and  tjyf>'202112' and tjyf<='202206'"
    ret=hbdb.db2df(sql,db='alluser')

    sql = "select avg(hb1y) as eq_ret ,tjyf from st_fund.t_st_gm_yhb where jjdm in ({}) and tjyf>'202112' and tjyf<='202203' and hb1y!=99999 group by tjyf" \
        .format(util.list_sql_condition(edf['jjdm'].tolist()))
    ret2 = hbdb.db2df(sql, db='funduser')
    sql = "select avg(hb1y) as eq_ret ,tjyf from st_fund.t_st_gm_yhb where jjdm in ({}) and tjyf>'202203' and tjyf<='202206' and hb1y!=99999 group by tjyf" \
        .format(util.list_sql_condition(edf2['jjdm'].tolist()))
    ret3 = hbdb.db2df(sql, db='funduser')

    ret2=pd.concat([ret2,ret3],axis=0)

    ret = pd.merge(ret, ret2, how='left', on='tjyf')
    ret['tjyf']=ret['tjyf'].astype(str)
    ret.set_index('tjyf',inplace=True)
    ret=ret/100+1
    for col in ret:

        ret[col]=ret[col].cumprod()

    plot.plotly_line_style(ret,'业绩走势比较',save_local_file=True)

    print('Done')