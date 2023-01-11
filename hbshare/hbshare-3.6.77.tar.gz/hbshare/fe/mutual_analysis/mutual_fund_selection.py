import pandas as pd
from hbshare.fe.XZ import db_engine
from hbshare.fe.XZ import functionality
from hbshare.fe.mutual_analysis import  holdind_based as hb
import numpy as np
from hbshare.fe.Machine_learning import classifier
import  datetime
import  joblib



util=functionality.Untils()
hbdb=db_engine.HBDB()
localdb=db_engine.PrvFunDB().engine


def get_pic_from_localdb(jjdm,asofdate='20220831',if_percentage=True,show_num=None):


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_value_p_hbs where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_value_p_hbs where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    value_p_hbs=pd.read_sql(sql,con=localdb)

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_size_p_hbs where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_size_p_hbs where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    size_p_hbs=pd.read_sql(sql,con=localdb).drop('规模偏好',axis=1)


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_industry_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    ind_max_date=latest_date
    sql="SELECT * from jjpic_industry_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    industry_p=pd.read_sql(sql,con=localdb)

    float_col_list=industry_p.columns.tolist()
    float_col_list.remove('jjdm')
    float_col_list.remove('asofdate')
    float_col_list.remove('前五大行业')
    float_col_list.remove('二级行业前20大')
    float_col_list.remove('三级行业前20大')
    float_col_list.remove('基金简称')
    float_col_list.remove('一级行业类型')
    float_col_list.remove('二级行业类型')
    float_col_list.remove('三级行业类型')


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_theme_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_theme_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    theme_p=pd.read_sql(sql,con=localdb)


    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_industry_sp where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_industry_sp where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    industry_sp=pd.read_sql(sql,con=localdb)
    ind_sp_float_col_list=industry_sp.columns.tolist()
    ind_sp_float_col_list.remove('jjdm')
    ind_sp_float_col_list.remove('asofdate')
    ind_sp_float_col_list.remove('项目名')

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_theme_sp where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_theme_sp where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    theme_sp=pd.read_sql(sql,con=localdb)
    theme_sp_float_col_list = theme_sp.columns.tolist()
    theme_sp_float_col_list.remove('jjdm')
    theme_sp_float_col_list.remove('asofdate')
    theme_sp_float_col_list.remove('项目名')

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_stock_p where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_stock_p where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    stock_p=pd.read_sql(sql,con=localdb)
    float_col=stock_p.columns.tolist()
    float_col.remove('jjdm')
    float_col.remove('asofdate')
    float_col.remove('持股数量')
    float_col.remove('PE')
    float_col.remove('PB')
    float_col.remove('ROE')
    float_col.remove('股息率')
    float_col.remove('PE_中位数')
    float_col.remove('PB_中位数')
    float_col.remove('ROE_中位数')
    float_col.remove('股息率_中位数')
    float_col.remove('基金简称')
    float_col.remove('个股风格A')
    float_col.remove('个股风格B')
    float_col.remove('是否有尾仓(针对高个股集中基金)')

    latest_date=pd.read_sql(
        "select max(asofdate) as asofdate from jjpic_stock_tp where asofdate<='{}'"
            .format(asofdate),con=localdb)['asofdate'][0]
    sql="SELECT * from jjpic_stock_tp where {0} and asofdate='{1}' "\
        .format(jjdm,latest_date)
    stock_tp=pd.read_sql(sql,con=localdb)
    tp_float_col=stock_tp.columns.tolist()
    tp_float_col.remove('jjdm')
    tp_float_col.remove('平均持有时间(出重仓前)')
    tp_float_col.remove('平均持有时间(出持仓前)')
    tp_float_col.remove('asofdate')
    tp_float_col.remove('基金简称')
    tp_float_col.remove('左侧标签')
    tp_float_col.remove('新股次新股偏好')

    #update the industry label by ticker shift ratio
    industry_p = pd.merge(industry_p, stock_tp[['jjdm', '换手率_rank']],how='left',on='jjdm')
    industry_p.loc[(industry_p['一级行业类型']=='博弈')
                   &(industry_p['换手率_rank']<0.5),'一级行业类型']='博弈(被动)'
    industry_p.loc[(industry_p['一级行业类型']=='轮动')
                   &(industry_p['换手率_rank']<0.5),'一级行业类型']='轮动(被动)'
    industry_p.drop('换手率_rank',axis=1,inplace=True)

    # latest_date=pd.read_sql(
    #     "select max(asofdate) as asofdate from nav_jj_ret_analysis where  asofdate<='{}'"
    #         .format(asofdate),con=localdb)['asofdate'][0]
    # sql="SELECT * from nav_jj_ret_analysis where {0} and asofdate='{1}' "\
    #     .format(jjdm,latest_date)
    # jj_performance=pd.read_sql(sql,con=localdb).fillna(0)
    #
    # latest_date=pd.read_sql(
    #     "select max(asofdate) as asofdate from nav_hurst_index where  asofdate<='{}'"
    #         .format(asofdate),con=localdb)['asofdate'][0]
    # sql="SELECT * from nav_hurst_index where {0} and asofdate='{1}' "\
    #     .format(jjdm,latest_date)
    # hurst=pd.read_sql(sql,con=localdb)
    # hurst['业绩特征'] = '随机'
    # hurst.loc[hurst['H'] <= 0.35,'业绩特征']='趋势反转'
    # hurst.loc[hurst['H'] >= 0.65,'业绩特征']='趋势保持'
    #
    # jj_performance=pd.merge(jj_performance,hurst[['jjdm','业绩特征']],how='left',on='jjdm')

    # jj_performance=jj_performance[['jjdm','业绩预期回归强度', '长期相对业绩表现', '相对业绩稳定性','业绩特征','month_rank_mean', 'month_rank_std', 'quarter_rank_mean',
    #    'quarter_rank_std', 'hy_rank_mean', 'hy_rank_std', 'yearly_rank_mean',
    #    'yearly_rank_std', 'ret_regress',
    #    'sharp_ratio', 'sharp_ratio_rank', 'downwards_ratio',
    #    'downwards_ratio_rank', 'sortino_ratio', 'sortino_ratio_rank',
    #    'max_drawback', 'max_drawback_rank', 'calmark_ratio',
    #    'calmark_ratio_rank', 'treynor_ratio', 'treynor_ratio_rank','moment','moment_rank',
    #    'asofdate']]
    # performance_float_col=jj_performance.columns.tolist()
    # performance_float_col.remove('jjdm')
    # performance_float_col.remove('业绩预期回归强度')
    # performance_float_col.remove('长期相对业绩表现')
    # performance_float_col.remove('相对业绩稳定性')
    # performance_float_col.remove('asofdate')
    # performance_float_col.remove('业绩特征')


    if (if_percentage):
        for col in float_col_list:
            industry_p[col] = industry_p[col].map("{:.2%}".format)
        for col in ind_sp_float_col_list[0:int(len(ind_sp_float_col_list) / 2)]:
            industry_sp[col] = \
                industry_sp[col].astype(float).map("{:.2%}".format)
        for col in ind_sp_float_col_list[int(len(ind_sp_float_col_list) / 2):]:
            industry_sp.loc[industry_sp['项目名'] != '切换次数', col] = \
                industry_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
        for col in theme_sp_float_col_list[0:int(len(theme_sp_float_col_list) / 2)]:
            theme_sp[col] = \
                theme_sp[col].astype(float).map("{:.2%}".format)
        for col in theme_sp_float_col_list[int(len(theme_sp_float_col_list) / 2):]:
            theme_sp.loc[theme_sp['项目名'] != '切换次数', col] = \
                theme_sp.iloc[1:][col].astype(float).map("{:.2%}".format)
        for col in ['主题集中度', '主题换手率', '大金融', '消费', 'TMT', '周期',
       '制造']:
            theme_p[col]=theme_p[col].map("{:.2%}".format)


        for col in ['集中度(持仓)', '换手率(持仓)', '成长绝对暴露(持仓)', '价值绝对暴露(持仓)', '集中度排名(持仓)',
           '换手率排名(持仓)', '成长暴露排名(持仓)', '价值暴露排名(持仓)']:
            value_p_hbs[col]=value_p_hbs[col].map("{:.2%}".format)
        for col in ['集中度(持仓)', '换手率(持仓)', '大盘绝对暴露(持仓)', '中盘绝对暴露(持仓)', '小盘绝对暴露(持仓)',
           '集中度排名(持仓)', '换手率排名(持仓)', '大盘暴露排名(持仓)', '中盘暴露排名(持仓)', '小盘暴露排名(持仓)']:
            size_p_hbs[col]=size_p_hbs[col].map("{:.2%}".format)


        for col in float_col:
            stock_p[col]= stock_p[col].map("{:.2%}".format)
        for col in tp_float_col:
            stock_tp[col] = stock_tp[col].map("{:.2%}".format)

        # for col in performance_float_col:
        #     jj_performance[col] = jj_performance[col].map("{:.2%}".format)

    return value_p_hbs,size_p_hbs,\
           industry_p,industry_sp,theme_p,theme_sp,stock_p,\
           stock_tp

def get_fund_features(asofdate,asofdate2,jjdm_list):


    if(jjdm_list is not None):
        jjdm_con="jjdm in ({})".format(util.list_sql_condition(jjdm_list))
    else:
        jjdm_con='1=1'

    value_p_hbs,size_p_hbs,  \
    industry_p, industry_sp, theme_p, theme_sp, stock_p, stock_tp= \
        get_pic_from_localdb(jjdm_con, asofdate=asofdate,if_percentage=False)

    jj_features=pd.merge(value_p_hbs.drop(['风格偏好','成长绝对暴露(持仓)',
                                           '价值绝对暴露(持仓)','成长暴露排名(持仓)', '价值暴露排名(持仓)'],axis=1)
                         ,size_p_hbs.drop(['asofdate','基金简称','大盘绝对暴露(持仓)','中盘绝对暴露(持仓)',
                                           '小盘绝对暴露(持仓)', '大盘暴露排名(持仓)','中盘暴露排名(持仓)', '小盘暴露排名(持仓)'],axis=1)
                         ,how='inner',on='jjdm')

    jj_features=pd.merge(jj_features,industry_p.drop(['asofdate','基金简称','前五大行业','二级行业前20大','三级行业前20大'],axis=1)
                         ,how='inner',on='jjdm')
    jj_features=pd.merge(jj_features,
                         industry_sp[['项目名','Total_rank','jjdm']].pivot_table('Total_rank','jjdm','项目名')
                         ,how='left',on='jjdm')
    jj_features=pd.merge(jj_features,theme_p.drop(['asofdate','基金简称','大金融','消费','TMT','周期','制造'],axis=1)
                         ,how='inner',on='jjdm')
    jj_features=pd.merge(jj_features,stock_p.drop(['asofdate','基金简称'],axis=1)
                         ,how='inner',on='jjdm')
    jj_features=pd.merge(jj_features,stock_tp.drop(['asofdate','基金简称'],axis=1)
                         ,how='inner',on='jjdm')

    objective_col=jj_features.dtypes[jj_features.dtypes=='O'].index.tolist()

    objective_col.remove('jjdm')
    objective_col.remove('基金简称')
    objective_col.remove('asofdate')
    dummpy_data=pd.get_dummies(jj_features[objective_col])

    jj_features=pd.concat([jj_features.drop(objective_col,axis=1),dummpy_data],axis=1)


    if(asofdate2[4:6]=='12'):
        return_date=str(int(asofdate2[0:4])+1)+'0930'
        # return_date = str(int(asofdate2[0:4]) + 2) + '0330'
        start_date=str(int(asofdate2[0:4])+1)+'0331'
    else:
        return_date =str(int(asofdate2[0:4])+1) + '0331'
        # return_date = str(int(asofdate2[0:4]) + 1) + '0930'
        start_date = asofdate2[0:4] + '0930'

    sql="select jjdm,zbnp from st_fund.t_st_gm_rqjhb where jjdm in ({0}) and zblb='2106' and jzrq>='{1}' and jzrq<='{2}'"\
        .format(util.list_sql_condition(jjdm_list),return_date[0:6]+'15',return_date[0:6]+'31')
    jj_half_year_ret=hbdb.db2df(sql,db='funduser').drop_duplicates('jjdm',keep='last')

    # sql="select jjdm,hb1n from st_fund.t_st_gm_nhb where tjnf={0} and jjdm in ({1})"\
    #     .format(str(int(asofdate[0:4])+1),util.list_sql_condition(jjdm_list))
    # jj_year_ret=hbdb.db2df(sql,db='funduser')

    ratio=0.9

    jj_features=jj_features[((jj_features['一级行业集中度']>0.8)
                            &(jj_features['一级行业换手率'])<0.2)]

    jj_features=pd.merge(jj_features,jj_half_year_ret,how='left',on='jjdm')
    jj_features['zbnp']=jj_features['zbnp'].rank(method='min')/len(jj_features)
    jj_features['flag']=1
    jj_features.loc[jj_features['zbnp']>=ratio,'flag']=0

    # jj_features=jj_features[((jj_features['zbnp']>ratio)|(jj_features['zbnp']<1-ratio))
    #                         |(jj_features['asofdate']=='20210630')]

    jj_features.drop('zbnp',axis=1,inplace=True)


    sql="select jjdm,zbnp,zblb from st_fund.t_st_gm_zqjxxbl where tjrq>={0} and tjrq<={1} and jjdm in ({2}) and zblb in ('2201','2202','2203','2106','2103','2101') and zbnp!=99999"\
        .format(start_date[0:6]+'01',start_date[0:6]+'31',util.list_sql_condition(jj_features['jjdm'].unique().tolist()))
    info_ratio=hbdb.db2df(sql,db='funduser').drop_duplicates(['jjdm','zblb'],keep='last').pivot_table('zbnp','jjdm','zblb')

    float_col=jj_features.dtypes[jj_features.dtypes!='O'].index.tolist()
    jj_features[float_col]=jj_features[float_col].fillna(0)

    jj_features=pd.merge(jj_features,info_ratio,how='left',on='jjdm')


    return jj_features


if __name__ == '__main__':

    jj_features=[]
    for asofdate in ['20181228','20190628','20191231'
        , '20200630',  '20201231'
        , '20210630']:
        print(asofdate)
        jjdm_list=util.get_bmk_funds_list(asofdate)

        jj_features.append(get_fund_features(asofdate=(datetime.datetime.strptime(asofdate, '%Y%m%d')
                                     +datetime.timedelta(days=120)).strftime('%Y%m%d'),asofdate2=asofdate, jjdm_list=jjdm_list))

    jj_features=pd.concat(jj_features,axis=0)
    jj_features.to_excel('mchl_data.xlsx',index=False)
    print('20210630')
    test_ratio=len(jj_features[jj_features['asofdate']<='20201231'])-1
    model, f1_score=\
        classifier.model_built_up(jj_features.drop(['jjdm','基金简称','asofdate'],axis=1).fillna(0),'flag','randomforest',[],test_ratio)

    # model, f1_score = \
    #     classifier.model_built_up(jj_features.drop(['jjdm', '基金简称', 'asofdate'], axis=1).fillna(0), 'flag', 'xgboost',
    #                               [], test_ratio)
    # joblib.dump(model,'xgboost_20210630.pkl')

    # feature_imp = pd.DataFrame(data=model.feature_importances_,
    #                            index=jj_features.drop(['jjdm', '基金简称', 'asofdate', 'flag'], axis=1).columns)
    # print(feature_imp.sort_values(0, ascending=False).iloc[0:10])
    #
    # #
    # print('20201231')
    # jj_features=jj_features[jj_features['asofdate']<='20201231']
    # test_ratio = len(jj_features[jj_features['asofdate'] <= '20200630']) - 1
    # model, f1_score = \
    #     classifier.model_built_up(jj_features.drop(['jjdm', '基金简称', 'asofdate'], axis=1).fillna(0), 'flag',
    #                               'xgboost', [], test_ratio)
    # joblib.dump(model,'xgboost_20201231.pkl')
    # feature_imp = pd.DataFrame(data=model.feature_importances_,
    #                            index=jj_features.drop(['jjdm', '基金简称', 'asofdate', 'flag'], axis=1).columns)
    # print(feature_imp.sort_values(0, ascending=False).iloc[0:10])
    # #
    # print('20200630')
    # jj_features=jj_features[jj_features['asofdate']<='20200630']
    # test_ratio = len(jj_features[jj_features['asofdate'] <= '20191231']) - 1
    # model, f1_score = \
    #     classifier.model_built_up(jj_features.drop(['jjdm', '基金简称', 'asofdate'], axis=1).fillna(0), 'flag',
    #                               'xgboost', [], test_ratio)
    # joblib.dump(model, 'xgboost_20200630.pkl')
    # feature_imp = pd.DataFrame(data=model.feature_importances_,
    #                            index=jj_features.drop(['jjdm', '基金简称', 'asofdate', 'flag'], axis=1).columns)
    # print(feature_imp.sort_values(0, ascending=False).iloc[0:10])
    # #
    # print('20191231')
    # jj_features=jj_features[jj_features['asofdate']<='20191231']
    # test_ratio = len(jj_features[jj_features['asofdate'] <= '20190628']) - 1
    # model, f1_score = \
    #     classifier.model_built_up(jj_features.drop(['jjdm', '基金简称', 'asofdate'], axis=1).fillna(0), 'flag',
    #                               'xgboost', [], test_ratio)
    # joblib.dump(model, 'xgboost_20191231.pkl')
    # feature_imp = pd.DataFrame(data=model.feature_importances_,
    #                            index=jj_features.drop(['jjdm', '基金简称', 'asofdate', 'flag'], axis=1).columns)
    # print(feature_imp.sort_values(0, ascending=False).iloc[0:10])

    # #
    # jj_features=pd.read_excel('mchl_data.xlsx')
    # asofdate = '20211231'
    # jjdm_list = util.get_bmk_funds_list(asofdate)
    # test = get_fund_features(asofdate=(datetime.datetime.strptime(asofdate, '%Y%m%d')
    #                                  +datetime.timedelta(days=120)).strftime('%Y%m%d'),asofdate2=asofdate, jjdm_list=jjdm_list)
    # test = pd.concat([jj_features.iloc[[-1]], test], axis=0)
    # #
    # voting_result=[]
    # fi_summary=pd.DataFrame(columns=['index'])
    # for asofdate in ['20191231'
    #     , '20200630',  '20201231'
    #     , '20210630']:
    #     #to make sure the columns is the same
    #     print(asofdate)
    #     model=joblib.load('xgboost_{}.pkl'.format(asofdate))
    #     feature_imp = pd.DataFrame(data=model.feature_importances_,
    #                                index=jj_features.drop(['jjdm', '基金简称', 'asofdate', 'flag'], axis=1).columns)
    #     fi_summary=\
    #         pd.merge(fi_summary, feature_imp.reset_index().rename(columns={0:asofdate}), how='outer', on='index')
    #
    #     result = model.predict(test.drop(['jjdm', '基金简称', 'asofdate', 'flag'], axis=1).fillna(0))
    #     test['pred']=result
    #     test.loc[test['pred']<0.5,'pred']=0
    #     test.loc[test['pred'] > 0.5, 'pred'] = 1
    #     print('{}'.format(len(test[(test['pred']==0)&(test['flag']==0)])/len(test[test['pred']==0])))
    #
    #
    #     voting_result.append(test[test['pred']<0.5]['jjdm'])
    #     test.drop('pred',axis=1,inplace=True)
    #
    # fi_summary.set_index('index',inplace=True)
    #
    # print('')


