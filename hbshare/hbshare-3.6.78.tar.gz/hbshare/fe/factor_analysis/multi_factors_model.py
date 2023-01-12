import numpy as np
import pandas as pd
from hbshare.fe.XZ import db_engine as dbeng
from hbshare.fe.XZ import functionality
from sklearn import  preprocessing as pp



util=functionality.Untils()
hbdb=dbeng.HBDB()
fre_map={'M':'2101','Q':'2103','HA':'2106','A':'2201','2A':'2202','3A':'2203'}
localdb = dbeng.PrvFunDB().engine

class Multi_factor_model:

    def __init__(self,factor_list,fre):

        self.factor_list=factor_list
        self.fre=fre

        factor_df=pd.DataFrame()
        count=0
        for factor_name in factor_list:

            raw_factor_data = self.factor_loader(factor_name)

            raw_factor_data['month'] = raw_factor_data['date'].astype(str).str[4:6]
            raw_factor_data['year_month']=raw_factor_data['date'].astype(str).str[0:6]

            if (fre == 'Q'):
                raw_factor_data = raw_factor_data.loc[raw_factor_data['month'].isin(['03', '06', '09', '12'])]
            elif (fre == 'HA'):
                raw_factor_data = raw_factor_data.loc[raw_factor_data['month'].isin(['06', '12'])]
            elif (fre == 'A'):
                raw_factor_data = raw_factor_data.loc[raw_factor_data['month'].isin(['12'])]

            if (count == 0):
                factor_df = raw_factor_data.drop(['month'],axis=1).copy()
            else:
                factor_df = pd.merge(factor_df
                                     , raw_factor_data.drop(['date','month'],axis=1), how='inner', on=['jjdm', 'year_month'])
            count += 1

        self.raw_factor_data=factor_df.drop('year_month',axis=1)


    @staticmethod
    def factor_loader(factor_name):

        if('25%' in factor_name):

            rolling=factor_name.split('25%')[1]

            sql="SELECT * from factor{}_rank_quantile".format(rolling)
            factor_date=pd.read_sql(sql,con=localdb)[['jjdm','25%','date']].rename(columns={'25%':factor_name})

        elif (factor_name == 'year_logret'):

            sql="select jjdm,year_logret,date from factor_year_ret where year_logret is not null "
            factor_date=pd.read_sql(sql, con=localdb)

        elif (factor_name == 'jjzzc'):

            sql="select jjdm,jjzzc,date from factor_size  "
            factor_date=pd.read_sql(sql, con=localdb)

        elif ('info_ratio' in factor_name):

            rolling=factor_name.split('info_ratio')[1].split('_')[1]

            sql="select jjdm,info_ratio as {0},date from factor_infor_ratio where zblb={1} ".format(factor_name,rolling)
            factor_date=pd.read_sql(sql, con=localdb)
            factor_date['date']=factor_date['date'].astype(str)

        elif ('sortino' in factor_name):

            rolling=factor_name.split('sortino')[1].split('_')[1]

            sql="select jjdm,sortino as {0},date from factor_sortino where zblb={1} ".format(factor_name,rolling)
            factor_date=pd.read_sql(sql, con=localdb)
            factor_date['date']=factor_date['date'].astype(str)

        elif ('ext_ret' in factor_name):

            from hbshare.fe.mutual_analysis import nav_based as nbs

            sr = nbs.Scenario_return()
            factor_date = sr.factorlize_ret(factor_name)[['jjdm','date']+[factor_name]]
            factor_date['date']=factor_date['date'].astype(str)

        else:
            print('input factor name is not included in the model by now ')
            raise  Exception

        return  factor_date

    def factor_correlation_check(self):

        factor_df=self.raw_factor_data.copy()
        factor_df.drop('jjdm',axis=1,inplace=True)

        corr_res=factor_df.groupby('date').corr()

        return  corr_res.reset_index().groupby('level_1').mean()

    def get_the_combined_factors(self,method,factor_list=None,factor_symbol=None):

        if(factor_list is None):
            factor_list=self.factor_list

        factor_df = self.raw_factor_data[['jjdm', 'date'] + factor_list]
        factor_df[factor_list] = pp.scale(factor_df[factor_list])


        if(method=='avg'):
            if(factor_symbol is None):
                factor_df['new_factor']=factor_df[factor_list].mean(axis=1)
            else:
                for j in range(len(factor_list)):
                    factor_df[factor_list[j]]=factor_df[factor_list[j]]*factor_symbol[j]
                factor_df['new_factor'] = factor_df[factor_list].mean(axis=1)

        elif(method=='ir'):

            from hbshare.fe.factor_analysis import  single_factor_analysis as sfa
            factor_df['new_factor']=0
            factor_df['total_ir'] = 0


            for factor in factor_list:

                ic_history=sfa.single_factor_ic(factor_df[['jjdm','date']+[factor]],factor
                                           ,fre=self.fre,pool_size=20,fund_flag=True,grouping_flag=False)
                ic_history['std']=ic_history.rolling(120,4).std()['ic']
                ic_history['mean'] = ic_history.rolling(120,4).mean()['ic']
                ic_history['ir']=ic_history['mean']/ic_history['std']
                # ic_history['ir']=[np.max([x,0]) for x in ic_history['ir']]

                factor_df=pd.merge(factor_df
                                   ,ic_history[['date','ir']].rename(columns={'ir':factor+"_ir"}),how='left',on='date')

                factor_df['new_factor']=factor_df['new_factor']+factor_df[factor]*factor_df[factor+"_ir"]
                factor_df['total_ir'] = factor_df['total_ir'] + factor_df[factor + "_ir"].abs()

            factor_df['new_factor']=factor_df['new_factor']/factor_df['total_ir']
            factor_df=factor_df[(factor_df['total_ir'].notnull())|(factor_df['date']==factor_df['date'].max())]

        else:
            print('the input method is not suppoered ')
            raise  Exception


        return factor_df[['jjdm','date','new_factor']]


if __name__ == '__main__':


    mfm=Multi_factor_model(['25%_year','25%_half_year','year_logret'],fre='Q')
    #corr=mfm.factor_correlation_check()




    print('Done')