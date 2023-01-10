import os
import re
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from datupapi.configure.config import Config
from pandas.tseries.offsets import MonthEnd

class Stocks(Config):

        def __init__(self, config_file, logfile, log_path, *args, **kwargs):
            Config.__init__(self, config_file=config_file, logfile=logfile)
            self.log_path = log_path

        # SALES HISTORY-----------------------------------------------------------------------
        def extract_sales_history (self,df_prep, df_invopt,date_cols,location=True):  
            """
            Returns a data frame that incorporates the DemandHistory column into the inventory data frame.

            : param df_prep: Dataframe prepared for Forecast
            : param df_invopt: Inventory's Dataframe with the columns Item, Location(Optional)
            : param date_cols: Column name of date from df_prep
            : param location: Boolean to enable the use of Location in the Inventory's dataframe
            : return df_extract: Dataframe with addition the column Sales History in the Inventory's Dataframe

            >>> df_extract = extract_sales_history (df_prep,df_invopt,date_cols='timestamp', location=self.use_location)
            >>> df_extract =
                                                Item    Location  DemandHistory
                                    idx0          85      905        200
                                    idx1          102     487        100
            """      
            try:
                df_prep_history = df_prep[df_prep[date_cols]== df_prep[date_cols].max()]
                if location:
                    dict_names = {'item_id':'Item',
                                    'location':'Location',
                                    'demand':'DemandHistory'}
                    df_prep_history.rename(columns=dict_names,inplace=True)

                    df_prep_history['Item'] = df_prep_history['Item'].astype(str)
                    df_prep_history['Location'] = df_prep_history['Location'].astype(str)
                    df_invopt['Item'] = df_invopt['Item'].astype(str)
                    df_invopt['Location'] = df_invopt['Location'].astype(str)

                    df_extract = pd.merge(df_invopt,df_prep_history[['Item','Location','DemandHistory']],on=['Item','Location'],how='left')
                else:
                    dict_names =  {'item_id':'Item',
                                    'demand':'DemandHistory'}
                    df_prep_history.rename(columns=dict_names,inplace=True)

                    df_prep_history['Item'] = df_prep_history['Item'].astype(str)
                    df_invopt['Item'] = df_invopt['Item'].astype(str)

                    df_extract = pd.merge(df_invopt,df_prep_history[['Item','DemandHistory']],on=['Item'],how='left')

            except KeyError as err:
                self.logger.exception(f'No column found. Please check columns names: {err}')
                print(f'No column found. Please check columns names')
                raise
            return df_extract

        #FORECAST-----------------------------------------------------------------------

        def extract_forecast(self,df_fcst,df_invopt,date_cols,frequency_,months_,location,column_forecast='ForecastCollab',weeks_=4,join_='left'):      
            """
            Returns a data frame that incorporates the SuggestedForecast column into the inventory data frame.

            : param df_fcst: Forecast's Dataframe 
            : param df_invopt: Inventory's Dataframe with the columns Item, Location(Optional), DemandHistory
            : param date_cols: Column name of date from df_fcst
            : param frequency_: Target frequency to the dataset
            : param months_: Number of months
            : param location: Boolean to enable the use of Location in the Inventory's dataframe
            : param column_forecast: name of the column where the desired forecast is located 
            : param join_: type of join with forecast 

            >>> df_extract = extract_forecast (df_prep,df_fcst,df_invopt,date_cols='Date', location=self.use_location, frequency_= self.dataset_frequency,join_='left')
            >>> df_extract =
                                                Item    Location  DemandHistory   SuggestedForecast
                                    idx0          85      905         23              200
                                    idx1          102     487         95              100
            """ 
            try:
                if frequency_ == 'M':
                    df_fcst_sug = df_fcst[df_fcst[date_cols]>= (df_fcst[date_cols].max() - relativedelta(months=months_))]
                    if location:
                        df_fcst_sug = df_fcst_sug.groupby(['Item', 'Location'], as_index=False)\
                                                                        .agg({column_forecast: sum})\
                                                                        .reset_index(drop=True)
                        df_invopt['Item'] = df_invopt['Item'].astype(str)
                        df_invopt['Location'] = df_invopt['Location'].astype(str)
                        df_fcst_sug['Item'] = df_fcst_sug['Item'].astype(str)
                        df_fcst_sug['Location'] = df_fcst_sug['Location'].astype(str)
                        df_extract = pd.merge(df_invopt,df_fcst_sug[['Item','Location',column_forecast]],on=['Item','Location'],how=join_)
                    else:
                        df_invopt['Item'] = df_invopt['Item'].astype(str)
                        df_fcst_sug['Item'] = df_fcst_sug['Item'].astype(str)
                        df_extract = pd.merge(df_invopt,df_fcst_sug[['Item',column_forecast]],on=['Item'],how=join_)
                
                elif frequency_ == 'W':
                    df_fcst_sug = df_fcst[df_fcst[date_cols]>= (df_fcst[date_cols].max() - relativedelta(weeks=weeks_))]
                    if location:
                        df_fcst_sug = df_fcst_sug.groupby(['Item', 'Location'], as_index=False)\
                                                                        .agg({column_forecast: sum})\
                                                                        .reset_index(drop=True)
                        df_invopt['Item'] = df_invopt['Item'].astype(str)
                        df_invopt['Location'] = df_invopt['Location'].astype(str)
                        df_fcst_sug['Item'] = df_fcst_sug['Item'].astype(str)
                        df_fcst_sug['Location'] = df_fcst_sug['Location'].astype(str)
                        df_extract = pd.merge(df_invopt,df_fcst_sug[['Item','Location',column_forecast]],on=['Item','Location'],how=join_)
                    else:
                        df_fcst_sug = df_fcst_sug.groupby(['Item'], as_index=False)\
                                              .agg({column_forecast: sum})\
                                              .reset_index(drop=True)
                        df_invopt['Item'] = df_invopt['Item'].astype(str)
                        df_fcst_sug['Item'] = df_fcst_sug['Item'].astype(str)
                        df_extract = pd.merge(df_invopt,df_fcst_sug[['Item',column_forecast]],on=['Item'],how=join_)

            except KeyError as err:
                self.logger.exception(f'No column found. Please check columns names: {err}')
                print(f'No column found. Please check columns names')
                raise
            return df_extract


        #DEFINE PERIODS-----------------------------------------------------------------------

        def define_periods(self,df_ ,df_current ,period, DayOfWeek, DaysOfWeek, DayOfMonth, DaysOfMonth,pmonth, df_Prep, df_inv, column_forecast, location, frequency_ , join_,columns_group):
            """
            : param df_:  Forecast Dataframe  Filtered
            : param df_current: Current Forecast
            : param period: Period of reorder
            : param DayOfWeek: current day of the week
            : param DaysOfWeek: total days of the week
            : param DayOfMonth: current day of the month
            : param DaysOfMonth: total days of the month
            : param pmonth: flag for february
            : param df_Prep: Qprep
            : param df_inv: Qsales, pervious dataframe
            : param column_forecast: name of the column where the desired forecast is located 
            : param location: Boolean to enable the use of Location in the Inventory's dataframe
            : param frequency_: Target frequency to the dataset
            : param join_: type of join with forecast 
            : param columns_group: final set of columns 

            """ 
            try: 
                if location == False:
                    
                    if frequency_ == 'W':      
                        
                        if not df_.empty:
                            itemslist_=list(df_['Item'].unique())
                            df_current=df_current[df_current['Item'].isin(itemslist_)]
                            # LESS THAN A PERIOD-----------------------------------------------------
                            if period == 0:
                                    df_ = df_[(df_['Date']>df_Prep['timestamp'].max())&
                                                            (df_['Date']<= (df_Prep['timestamp'].max()+relativedelta(weeks=1)))]
                                    df_=df_.iloc[:,:18]
                                    df_=df_.drop_duplicates()
                                    df_extract_forecast = self.extract_forecast(df_, df_inv, column_forecast=column_forecast, location=location,frequency_= frequency_ ,
                                                            date_cols = 'Date',months_= 1,weeks_= 1,join_=join_).fillna(0) 
                                    df_final = df_extract_forecast.groupby(columns_group, as_index=False).agg({column_forecast:sum})
                                    df_final[column_forecast]=df_final[column_forecast] *(1-DayOfWeek/DaysOfWeek)              

                            if period != 0:
                                df_ = df_[(df_['Date']>(df_Prep['timestamp'].max()+relativedelta(weeks=1)))&
                                    (df_['Date']<= (df_Prep['timestamp'].max()+relativedelta(weeks=(period+1))))]
                                df_a=df_.iloc[:,:18].copy()
                                df_a=df_a.drop_duplicates()
                                df_extract_forecast = self.extract_forecast(df_a, df_inv, column_forecast=column_forecast, location=location,frequency_= frequency_ ,
                                                                    date_cols = 'Date',months_= (period+1) ,weeks_= (period+1),join_=join_).fillna(0) 
                                df_extract_forecast = df_extract_forecast.groupby(columns_group, as_index=False).agg({column_forecast:sum}) 
                                df_extract_forecast.rename(columns={column_forecast:'Next'},inplace=True)
                            
                                df_b=df_[['Item','Coverage','Periods']].drop_duplicates() 
                                df_final= pd.merge(df_extract_forecast,df_b,on=['Item'],how='left')
                                df_final= pd.merge(df_final,df_current,on=['Item'],how='left')
                                df_final[column_forecast]=df_final['Current'] + df_final['Next']*((df_final['Coverage']-DaysOfWeek+DayOfWeek)/(df_final['Periods']*DaysOfWeek))
                                df_final = df_final.groupby(columns_group, as_index=False).agg({column_forecast:max})    

                        if df_.empty:
                            columns=list(df_inv.columns)
                            columns.append(column_forecast)
                            df_final = pd.DataFrame(columns = columns)
                    
                    if frequency_ == 'M':      
                        
                        if not df_.empty:
                            itemslist_=list(df_['Item'].unique())
                            df_current=df_current[df_current['Item'].isin(itemslist_)]
                            # LESS THAN A PERIOD-----------------------------------------------------
                            if period == 0:
                                df_ = df_[(df_['Date']>df_Prep['timestamp'].max())&
                                                (df_['Date']<= (df_Prep['timestamp'].max()+relativedelta(months=1)+MonthEnd(pmonth)))] 
                                df_=df_.iloc[:,:18]
                                df_=df_.drop_duplicates()
                                df_extract_forecast = self.extract_forecast(df_, df_inv, column_forecast=column_forecast, location=location,frequency_= frequency_ ,
                                                                        date_cols = 'Date',months_= 1,weeks_= 4,join_=join_).fillna(0) 
                                df_final = df_extract_forecast.groupby(columns_group, as_index=False).agg({column_forecast:sum})  
                                df_final [column_forecast]=df_final [column_forecast]*(1-DayOfMonth/DaysOfMonth)            

                            if period != 0:                          
                                df_ = df_[(df_['Date']>(df_Prep['timestamp'].max()+relativedelta(months=1)+MonthEnd(pmonth)))&
                                                (df_['Date']<= (df_Prep['timestamp'].max()+relativedelta(months=(period+1))+MonthEnd(pmonth)))] 
                                df_a=df_.iloc[:,:18].copy()
                                df_a=df_a.drop_duplicates()
                                df_extract_forecast = self.extract_forecast(df_a, df_inv, column_forecast=column_forecast, location=location,frequency_= frequency_ ,
                                                                    date_cols = 'Date',months_= (period+1),weeks_= ((period+1)*4),join_=join_).fillna(0) 
                                df_extract_forecast = df_extract_forecast.groupby(columns_group, as_index=False).agg({column_forecast:sum}) 
                                df_extract_forecast.rename(columns={column_forecast:'Next'},inplace=True)
                            
                                df_b=df_[['Item','Coverage','Periods']].drop_duplicates() 
                                df_final= pd.merge(df_extract_forecast,df_b,on=['Item'],how='left')
                                df_final= pd.merge(df_final,df_current,on=['Item'],how='left')
                                df_final[column_forecast]=df_final['Current'] + df_final['Next']*((df_final['Coverage']-DaysOfMonth+DayOfMonth)/(df_final['Periods']*DaysOfMonth))
                                df_final = df_final.groupby(columns_group, as_index=False).agg({column_forecast:max})    

                        if df_.empty:
                            columns=list(df_inv.columns)
                            columns.append(column_forecast)
                            df_final = pd.DataFrame(columns = columns)

                if location == True :
                    
                    if frequency_ == 'W':      
                    
                        if not df_.empty:
                            itemslist_=list(df_['Item'].unique())
                            df_current=df_current[df_current['Item'].isin(itemslist_)]
                            # LESS THAN A PERIOD-----------------------------------------------------
                            if period == 0:
                                df_ = df_[(df_['Date']>df_Prep['timestamp'].max())&
                                                        (df_['Date']<= (df_Prep['timestamp'].max()+relativedelta(weeks=1)))]
                                df_=df_.iloc[:,:19]
                                df_=df_.drop_duplicates()
                                df_extract_forecast = self.extract_forecast(df_, df_inv, column_forecast=column_forecast, location=location,frequency_= frequency_ ,
                                                        date_cols = 'Date',months_= 1,weeks_= 1,join_=join_).fillna(0) 
                                df_final = df_extract_forecast.groupby(columns_group, as_index=False).agg({column_forecast:sum})
                                df_final[column_forecast]=df_final[column_forecast] *(1-DayOfWeek/DaysOfWeek)              

                            if period != 0:
                                df_ = df_[(df_['Date']>(df_Prep['timestamp'].max()+relativedelta(weeks=1)))&
                                    (df_['Date']<= (df_Prep['timestamp'].max()+relativedelta(weeks=(period+1))))]
                                df_a=df_.iloc[:,:19].copy()
                                df_a=df_a.drop_duplicates()
                                df_extract_forecast = self.extract_forecast(df_a, df_inv, column_forecast=column_forecast, location=location,frequency_= frequency_ ,
                                                                      date_cols = 'Date',months_= (period+1) ,weeks_= (period+1),join_=join_).fillna(0) 
                                df_extract_forecast = df_extract_forecast.groupby(columns_group, as_index=False).agg({column_forecast:sum}) 
                                df_extract_forecast.rename(columns={column_forecast:'Next'},inplace=True)
                            
                                df_b=df_[['Item','Location','Coverage','Periods']].drop_duplicates() 
                                df_final= pd.merge(df_extract_forecast,df_b,on=['Item','Location'],how='left')
                                df_final= pd.merge(df_final,df_current,on=['Item','Location'],how='left')
                                df_final[column_forecast]=df_final['Current'] + df_final['Next']*((df_final['Coverage']-DaysOfWeek+DayOfWeek)/(df_final['Periods']*DaysOfWeek))
                                df_final = df_final.groupby(columns_group, as_index=False).agg({column_forecast:max})    

                        if df_.empty:
                            columns=list(df_inv.columns)
                            columns.append(column_forecast)
                            df_final = pd.DataFrame(columns = columns)
                    
                    if frequency_ == 'M':      
                        
                        if not df_.empty:
                            itemslist_=list(df_['Item'].unique())
                            df_current=df_current[df_current['Item'].isin(itemslist_)]
                            # LESS THAN A PERIOD-----------------------------------------------------
                            if period == 0:
                                df_ = df_[(df_['Date']>df_Prep['timestamp'].max())&
                                                (df_['Date']<= (df_Prep['timestamp'].max()+relativedelta(months=1)+MonthEnd(pmonth)))] 
                                df_=df_.iloc[:,:19]
                                df_=df_.drop_duplicates()
                                df_extract_forecast = self.extract_forecast(df_, df_inv, column_forecast=column_forecast, location=location,frequency_= frequency_ ,
                                                                        date_cols = 'Date',months_= 1,weeks_= 4,join_=join_).fillna(0) 
                                df_final = df_extract_forecast.groupby(columns_group, as_index=False).agg({column_forecast:sum})  
                                df_final [column_forecast]=df_final [column_forecast]*(1-DayOfMonth/DaysOfMonth)            

                            if period != 0:                          
                                df_ = df_[(df_['Date']>(df_Prep['timestamp'].max()+relativedelta(months=1)+MonthEnd(pmonth)))&
                                                (df_['Date']<= (df_Prep['timestamp'].max()+relativedelta(months=(period+1))+MonthEnd(pmonth)))] 
                                df_a=df_.iloc[:,:19].copy()
                                df_a=df_a.drop_duplicates()
                                df_extract_forecast = self.extract_forecast(df_a, df_inv, column_forecast=column_forecast, location=location,frequency_= frequency_ ,
                                                                      date_cols = 'Date',months_= (period+1),weeks_= ((period+1)*4),join_=join_).fillna(0) 
                                df_extract_forecast = df_extract_forecast.groupby(columns_group, as_index=False).agg({column_forecast:sum}) 
                                df_extract_forecast.rename(columns={column_forecast:'Next'},inplace=True)
                            
                                df_b=df_[['Item','Location','Coverage','Periods']].drop_duplicates() 
                                df_final= pd.merge(df_extract_forecast,df_b,on=['Item','Location'],how='left')
                                df_final= pd.merge(df_final,df_current,on=['Item','Location'],how='left')
                                df_final[column_forecast]=df_final['Current'] + df_final['Next']*((df_final['Coverage']-DaysOfMonth+DayOfMonth)/(df_final['Periods']*DaysOfMonth))
                                df_final = df_final.groupby(columns_group, as_index=False).agg({column_forecast:max})    

                        if df_.empty:
                            columns=list(df_inv.columns)
                            columns.append(column_forecast)
                            df_final = pd.DataFrame(columns = columns)

            except KeyError as err:
                self.logger.exception(f'No column found. Please check columns names: {err}')
                print(f'No column found. Please check columns names')
                raise
            return df_final    


        # GET FORECAST -----------------------------------------------------------------------
        def suggested_forecast(self,df_LeadTimes ,df_Forecast,df_Prep,df_inv,column_forecast,frequency_,location,actualdate,join_='left'):
            """
            Returns a data frame that incorporates the SuggestedForecast column into the inventory data frame, taking into account delivery times 

            : param df_LeadTimes: LeadTime's Dataframe
            : param df_Forecast: Forecast's Dataframe 
            : param df_Prep: Dataframe prepared for Forecast
            : param df_inv: Inventory's Dataframe with the columns Item, Location(Optional), DemandHistory
            : param column_forecast: name of the column where the desired forecast is located 
            : param frequency_: Target frequency to the dataset
            : param location: Boolean to enable the use of Location in the Inventory's dataframe
            : param actualdate: current day   
            : param join_: type of join with forecast   
            
            
            >>> df_forecats = suggested_forecast(df_LeadTimes=df_lead_time, 
                                                            df_Forecast=df_fcst,
                                                            df_Prep=df_prep,
                                                            df_inv=df_inv,
                                                            column_forecast='SuggestedForecast',
                                                            frequency_ = 'W',
                                                            location = True/False,
                                                            actualdate=timestamp,
                                                            join_='left')
            >>> suggested_forecast =
                                                Item    Location  DemandHistory   SuggestedForecast
                                    idx0          85      905         23              200
                                    idx1          102     487         95              100
            """ 
            try:                 
                  
                d1 = pd.Period(pd.to_datetime(str('28'+'-02-'+actualdate[0:4]), format="%d-%m-%Y"),freq='M').end_time.date()
                d2 = str('29'+'-02-'+actualdate[0:4])

                if (df_Prep['timestamp'].max()).date() == d1:
                    pmonth=1
                    finfebrero='28'
                elif str((df_Prep['timestamp'].max()).date()) == d2:
                    pmonth=1
                    finfebrero='29'
                else:
                    pmonth=0
                    finfebrero='28'

                lastdayDict={'1':'31', '2': finfebrero, '3':'31', '4':'30', '5':'31', '6':'30', '7':'31', '8':'31', '9':'30', '10':'31', '11':'30', '12':'31'}
                DayOfMonth= int(actualdate[6:8])
                Month=str(int(actualdate[4:6]))
                DaysOfMonth = int(lastdayDict[Month])
                DayOfWeek = int(datetime.datetime.today().weekday())+1 
                DaysOfWeek =7 

                columns_group=list(df_inv.columns)

                if location == False:
                    
                    df_lead_cruce= df_LeadTimes.copy()
                    df_lead_cruce=df_lead_cruce.groupby(['Item'], as_index=False).agg({'Coverage':'mean','AvgLeadTime':'mean'}).reset_index(drop=True)
                    df_lead_cruce=df_lead_cruce[['Item','Coverage','AvgLeadTime']].drop_duplicates()
                    df_lead_cruce['Coverage']=df_lead_cruce[['Coverage','AvgLeadTime']].apply(lambda x : x['Coverage'] if (x['Coverage']>=x['AvgLeadTime']) else x['AvgLeadTime'], axis=1)
                    df_lead_cruce=df_lead_cruce[['Item','Coverage']].drop_duplicates() 

                    df_fcst_cruce = df_Forecast.copy()
                    df_final_fcst = pd.merge(df_fcst_cruce,df_lead_cruce,on=['Item'],how='left')  

                    if frequency_ == 'M':
                        df_final_fcst.loc[df_final_fcst['Coverage'].isnull(),'Coverage'] = 29
                        df_final_fcst['Periods'] = (df_final_fcst['Coverage']+DayOfMonth-1)//DaysOfMonth

                        #CURRENT PERIOD --------------------------------------------------------------
                        df_fcst_current = df_final_fcst[(df_final_fcst['Date']>df_Prep['timestamp'].max())&
                            (df_final_fcst['Date']<= (df_Prep['timestamp'].max()+relativedelta(months=1)+MonthEnd(pmonth)))] 
                        df_fcst_current=df_fcst_current.iloc[:,:18]
                        df_fcst_current=df_fcst_current.drop_duplicates()
                        df_extract_fcst_current = self.extract_forecast(df_fcst_current, df_inv, column_forecast=column_forecast, location=location,frequency_= frequency_ ,
                                                            date_cols = 'Date',months_= 1,weeks_= 4,join_=join_).fillna(0) 
                        df_extract_fcst_current = df_extract_fcst_current.groupby(columns_group, as_index=False).agg({column_forecast:sum})           
                        df_extract_fcst_current[column_forecast]=df_extract_fcst_current[column_forecast]*(1-DayOfMonth/DaysOfMonth)
                        df_extract_fcst_current.rename(columns={column_forecast:'Current'},inplace=True)
                        df_extract_fcst_current=df_extract_fcst_current[['Item','Current']]

                        columns=list(df_inv.columns)
                        columns.append(column_forecast)
                        df_fcst_final = pd.DataFrame(columns = columns)

                        df_fcst_={}
                        df_final_={}

                        for period in range((int(df_final_fcst['Periods'].max()))+1):
                            df_fcst_[period] = df_final_fcst[df_final_fcst["Periods"] == period]
                            df_final_[period] = self.define_periods(df_fcst_[period],df_extract_fcst_current,period, DayOfWeek, DaysOfWeek, DayOfMonth, DaysOfMonth,pmonth, df_Prep, df_inv, column_forecast, location, frequency_ , join_,columns_group)
                            df_fcst_final = pd.concat([df_fcst_final,df_final_[period]],ignore_index=True) 
                    
                    if frequency_ == 'W':
                        df_final_fcst.loc[df_final_fcst['Coverage'].isnull(),'Coverage'] = 6
                        df_final_fcst['Periods'] = (df_final_fcst['Coverage']+DayOfWeek)//DaysOfWeek

                        #CURRENT PERIOD --------------------------------------------------------------
                        df_fcst_current = df_final_fcst[(df_final_fcst['Date']>df_Prep['timestamp'].max())&
                                    (df_final_fcst['Date']<= (df_Prep['timestamp'].max()+relativedelta(weeks=1)))]
                        df_fcst_current=df_fcst_current.iloc[:,:18]
                        df_fcst_current=df_fcst_current.drop_duplicates()
                        df_extract_fcst_current = self.extract_forecast(df_fcst_current, df_inv, column_forecast=column_forecast, location=location,frequency_= frequency_ ,
                                                            date_cols = 'Date',months_= 1,weeks_= 1,join_=join_).fillna(0) 
                        df_extract_fcst_current = df_extract_fcst_current.groupby(columns_group, as_index=False).agg({column_forecast:sum})
                        df_extract_fcst_current[column_forecast]=df_extract_fcst_current[column_forecast] *(1-DayOfWeek/DaysOfWeek)
                        df_extract_fcst_current.rename(columns={column_forecast:'Current'},inplace=True)
                        df_extract_fcst_current=df_extract_fcst_current[['Item','Current']]

                        columns=list(df_inv.columns)
                        columns.append(column_forecast)
                        df_fcst_final = pd.DataFrame(columns = columns)
                        
                        df_fcst_={}
                        df_final_={}

                        for period in range((int(df_final_fcst['Periods'].max()))+1):
                            df_fcst_[period] = df_final_fcst[df_final_fcst["Periods"] == period]
                            df_final_[period] = self.define_periods(df_fcst_[period],df_extract_fcst_current,period, DayOfWeek, DaysOfWeek, DayOfMonth, DaysOfMonth,pmonth, df_Prep, df_inv, column_forecast, location, frequency_ , join_,columns_group)
                            df_fcst_final = pd.concat([df_fcst_final,df_final_[period]],ignore_index=True)       
                        
                    # Forecast -----------------------------------------------------------------  
                    df_fcst_final = df_fcst_final.groupby(columns_group, as_index=False).agg({column_forecast:max}) 
                
                if location == True:

                    df_lead_cruce= df_LeadTimes.copy()
                    df_lead_cruce=df_lead_cruce.groupby(['Item','Location'], as_index=False).agg({'Coverage':'mean','AvgLeadTime':'mean'}).reset_index(drop=True)
                    df_lead_cruce=df_lead_cruce[['Item','Location','Coverage','AvgLeadTime']].drop_duplicates()
                    df_lead_cruce['Coverage']=df_lead_cruce[['Coverage','AvgLeadTime']].apply(lambda x : x['Coverage'] if (x['Coverage']>=x['AvgLeadTime']) else x['AvgLeadTime'], axis=1)
                    df_lead_cruce=df_lead_cruce[['Item','Location','Coverage']].drop_duplicates()
                    
                    df_fcst_cruce = df_Forecast.copy()
                    df_fcst_cruce['Location']=df_fcst_cruce['Location'].astype(str)
                    df_final_fcst = pd.merge(df_fcst_cruce,df_lead_cruce,on=['Item','Location'],how='left')  

                    if frequency_ == 'M':
                        df_final_fcst.loc[df_final_fcst['Coverage'].isnull(),'Coverage'] = 29
                        df_final_fcst['Periods'] = (df_final_fcst['Coverage']+DayOfMonth-1)//DaysOfMonth

                        #CURRENT PERIOD --------------------------------------------------------------
                        df_fcst_current = df_final_fcst[(df_final_fcst['Date']>df_Prep['timestamp'].max())&
                            (df_final_fcst['Date']<= (df_Prep['timestamp'].max()+relativedelta(months=1)+MonthEnd(pmonth)))] 
                        df_fcst_current=df_fcst_current.iloc[:,:19]
                        df_fcst_current=df_fcst_current.drop_duplicates()
                        df_extract_fcst_current = self.extract_forecast(df_fcst_current, df_inv, column_forecast=column_forecast, location=location,frequency_= frequency_ ,
                                                            date_cols = 'Date',months_= 1,weeks_= 4,join_=join_).fillna(0) 
                        df_extract_fcst_current = df_extract_fcst_current.groupby(columns_group, as_index=False).agg({column_forecast:sum})           
                        df_extract_fcst_current[column_forecast]=df_extract_fcst_current[column_forecast]*(1-DayOfMonth/DaysOfMonth)
                        df_extract_fcst_current.rename(columns={column_forecast:'Current'},inplace=True)
                        df_extract_fcst_current=df_extract_fcst_current[['Item','Location','Current']]

                        columns=list(df_inv.columns)
                        columns.append(column_forecast)
                        df_fcst_final = pd.DataFrame(columns = columns)

                        df_fcst_={}
                        df_final_={}

                        for period in range((int(df_final_fcst['Periods'].max()))+1):
                            df_fcst_[period] = df_final_fcst[df_final_fcst["Periods"] == period]
                            df_final_[period] = self.define_periods(df_fcst_[period],df_extract_fcst_current,period, DayOfWeek, DaysOfWeek, DayOfMonth, DaysOfMonth,pmonth, df_Prep, df_inv, column_forecast, location, frequency_ , join_,columns_group)
                            df_fcst_final = pd.concat([df_fcst_final,df_final_[period]],ignore_index=True) 
                    
                    if frequency_ == 'W':
                        df_final_fcst.loc[df_final_fcst['Coverage'].isnull(),'Coverage'] = 6
                        df_final_fcst['Periods'] = (df_final_fcst['Coverage']+DayOfWeek)//DaysOfWeek

                        #CURRENT PERIOD --------------------------------------------------------------
                        df_fcst_current = df_final_fcst[(df_final_fcst['Date']>df_Prep['timestamp'].max())&
                                    (df_final_fcst['Date']<= (df_Prep['timestamp'].max()+relativedelta(weeks=1)))]
                        df_fcst_current=df_fcst_current.iloc[:,:19]
                        df_fcst_current=df_fcst_current.drop_duplicates()
                        df_extract_fcst_current = self.extract_forecast(df_fcst_current, df_inv, column_forecast=column_forecast, location=location,frequency_= frequency_ ,
                                                            date_cols = 'Date',months_= 1,weeks_= 1,join_=join_).fillna(0) 
                        df_extract_fcst_current = df_extract_fcst_current.groupby(columns_group, as_index=False).agg({column_forecast:sum})
                        df_extract_fcst_current[column_forecast]=df_extract_fcst_current[column_forecast] *(1-DayOfWeek/DaysOfWeek)
                        df_extract_fcst_current.rename(columns={column_forecast:'Current'},inplace=True)
                        df_extract_fcst_current=df_extract_fcst_current[['Item','Location','Current']]

                        columns=list(df_inv.columns)
                        columns.append(column_forecast)
                        df_fcst_final = pd.DataFrame(columns = columns)

                        df_fcst_={}
                        df_final_={}

                        for period in range((int(df_final_fcst['Periods'].max()))+1):
                            df_fcst_[period] = df_final_fcst[df_final_fcst["Periods"] == period]
                            df_final_[period] = self.define_periods(df_fcst_[period],df_extract_fcst_current,period, DayOfWeek, DaysOfWeek, DayOfMonth, DaysOfMonth,pmonth, df_Prep, df_inv, column_forecast, location, frequency_ , join_,columns_group)
                            df_fcst_final = pd.concat([df_fcst_final,df_final_[period]],ignore_index=True) 

                    # Forecast -----------------------------------------------------------------  
                    df_fcst_final = df_fcst_final.groupby(columns_group, as_index=False).agg({column_forecast:max}) 
            
            except KeyError as err:
                self.logger.exception(f'No column found. Please check columns names: {err}')
                print(f'No column found. Please check columns names')
                raise
            return df_fcst_final


        # AVERAGE DAILY -----------------------------------------------------------------

        def extract_avg_daily(self, df_Prep ,df_Forecast, df_invopt, forecast_=False,location=False,column_forecast='SuggestedForecast',frequency_='M',months_=4,weeks_= 16): 
            """
            Returns a data frame that incorporates the AvgDailyUsage column into the inventory data frame.

            : param df_Prep: Dataframe prepared for Forecast
            : param df_Forecast: Forecast's Dataframe 
            : param df_invopt: Inventory's Dataframe with the columns Item, Location(Optional), Inventory, Transit
            : param forecast_: Boolean to allow the use of the Suggested Forecast to calculate the average
            : param location: Boolean to enable the use of Location in the Inventory's dataframe
            : param column_forecast: name of the column where the desired forecast is located 
            : param frequency_: Target frequency to the dataset
            : param months_: Target Number months 
            : param weeks_: Target Number weeks 

            >>> df_extract = extract_avg_daily(df_Prep = df_prep,
                                              df_Forecast = df_fcst,
                                              df_invopt = df_avg, 
                                              forecast_=False,
                                              location = True,
                                              column_forecast='SuggestedForecast',
                                              months_ = 4 ,
                                              frequency_ = 'M')
            >>> df_extract =
                                                Item    Location   Inventory   Transit     AvgDailyUsage
                                    idx0          85      905         23            0             20
                                    idx1          102     487         95            0             10
            """

            try:            
                if forecast_ == True:
                  
                      if frequency_ == 'M':
                      
                            df_avg = df_Forecast[(df_Forecast['Date'] >= df_Prep['timestamp'].max()) & 
                                                (df_Forecast['Date'] < (df_Prep['timestamp'].max() + relativedelta(months=months_) + MonthEnd(0)))]
                            
                            if location:

                                df_avg = df_avg[['Date','Item','Location','Target',column_forecast]]
                                df_avg['AvgDailyUsage'] = df_avg.apply(lambda x: x[column_forecast] if (x['Target']==0) else x['Target'], axis=1 )
                                
                                df_avg = df_avg.groupby(['Item','Location'], as_index=False).agg({'AvgDailyUsage': sum}).reset_index(drop=True)
                                df_avg['AvgDailyUsage'] = df_avg['AvgDailyUsage']/(30*months_)
                                df_avg['Item'] = df_avg['Item'].astype(str)
                                df_avg['Location'] = df_avg['Location'].astype(str)
                                df_invopt['Item'] = df_invopt['Item'].astype(str)
                                df_invopt['Location'] = df_invopt['Location'].astype(str)
                                
                                df_extract = pd.merge(df_invopt,df_avg[['Item','Location','AvgDailyUsage']],on=['Item','Location'],how='left')
                              
                            else:
                                df_avg = df_avg[['Date','Item','Target',column_forecast]]
                                df_avg['AvgDailyUsage'] = df_avg.apply(lambda x: x[column_forecast] if (x['Target']==0) else x['Target'], axis=1 )

                                df_avg = df_avg.groupby(['Item'], as_index=False).agg({'AvgDailyUsage': sum}).reset_index(drop=True)
                                df_avg['AvgDailyUsage'] = df_avg['AvgDailyUsage']/(30*months_)
                                df_avg['Item'] = df_avg['Item'].astype(str)
                                df_invopt['Item'] = df_invopt['Item'].astype(str)
                                
                                df_extract = pd.merge(df_invopt,df_avg[['Item','AvgDailyUsage']],on=['Item'],how='left')
                      
                      if frequency_ == 'W':
                      
                            df_avg = df_Forecast[(df_Forecast['Date'] >= df_Prep['timestamp'].max()) & 
                                                (df_Forecast['Date'] < (df_Prep['timestamp'].max() + relativedelta(weeks=weeks_)))]
                            
                            if location:

                                df_avg = df_avg[['Date','Item','Location','Target',column_forecast]]
                                df_avg['AvgDailyUsage'] = df_avg.apply(lambda x: x[column_forecast] if (x['Target']==0) else x['Target'], axis=1 )
                                
                                df_avg = df_avg.groupby(['Item','Location'], as_index=False).agg({'AvgDailyUsage': sum}).reset_index(drop=True)
                                df_avg['AvgDailyUsage'] = df_avg['AvgDailyUsage']/(7*weeks_)
                                df_avg['Item'] = df_avg['Item'].astype(str)
                                df_avg['Location'] = df_avg['Location'].astype(str)
                                df_invopt['Item'] = df_invopt['Item'].astype(str)
                                df_invopt['Location'] = df_invopt['Location'].astype(str)
                                
                                df_extract = pd.merge(df_invopt,df_avg[['Item','Location','AvgDailyUsage']],on=['Item','Location'],how='left')
                              
                            else:
                                df_avg = df_avg[['Date','Item','Target',column_forecast]]
                                df_avg['AvgDailyUsage'] = df_avg.apply(lambda x: x[column_forecast] if (x['Target']==0) else x['Target'], axis=1 )

                                df_avg = df_avg.groupby(['Item'], as_index=False).agg({'AvgDailyUsage': sum}).reset_index(drop=True)
                                df_avg['AvgDailyUsage'] = df_avg['AvgDailyUsage']/(7*weeks_)
                                df_avg['Item'] = df_avg['Item'].astype(str)
                                df_invopt['Item'] = df_invopt['Item'].astype(str)
                                
                                df_extract = pd.merge(df_invopt,df_avg[['Item','AvgDailyUsage']],on=['Item'],how='left')

                if forecast_ == False:
                  
                      if frequency_ == 'M':
                      
                            df_avg = df_Forecast[(df_Forecast['Date'] <= df_Prep['timestamp'].max()) & 
                                                (df_Forecast['Date'] > (df_Prep['timestamp'].max() - relativedelta(months=months_) + MonthEnd(0)))]
                            
                            if location:

                                df_avg = df_avg[['Date','Item','Location','Target',column_forecast]]
                                df_avg['AvgDailyUsage'] = df_avg['Target'].copy()
                                
                                df_avg = df_avg.groupby(['Item','Location'], as_index=False).agg({'AvgDailyUsage': sum}).reset_index(drop=True)
                                df_avg['AvgDailyUsage'] = df_avg['AvgDailyUsage']/(30*months_)
                                df_avg['Item'] = df_avg['Item'].astype(str)
                                df_avg['Location'] = df_avg['Location'].astype(str)
                                df_invopt['Item'] = df_invopt['Item'].astype(str)
                                df_invopt['Location'] = df_invopt['Location'].astype(str)
                                
                                df_extract = pd.merge(df_invopt,df_avg[['Item','Location','AvgDailyUsage']],on=['Item','Location'],how='left')
                              
                            else:
                                df_avg = df_avg[['Date','Item','Target',column_forecast]]
                                df_avg['AvgDailyUsage'] = df_avg['Target'].copy()

                                df_avg = df_avg.groupby(['Item'], as_index=False).agg({'AvgDailyUsage': sum}).reset_index(drop=True)
                                df_avg['AvgDailyUsage'] = df_avg['AvgDailyUsage']/(30*months_)
                                df_avg['Item'] = df_avg['Item'].astype(str)
                                df_invopt['Item'] = df_invopt['Item'].astype(str)
                                
                                df_extract = pd.merge(df_invopt,df_avg[['Item','AvgDailyUsage']],on=['Item'],how='left')
                      
                      if frequency_ == 'W':
                      
                            df_avg = df_Forecast[(df_Forecast['Date'] <= df_Prep['timestamp'].max()) & 
                                                (df_Forecast['Date'] > (df_Prep['timestamp'].max() - relativedelta(weeks=weeks_)))]
                            
                            if location:

                                df_avg = df_avg[['Date','Item','Location','Target',column_forecast]]
                                df_avg['AvgDailyUsage'] = df_avg['Target'].copy()
                                
                                df_avg = df_avg.groupby(['Item','Location'], as_index=False).agg({'AvgDailyUsage': sum}).reset_index(drop=True)
                                df_avg['AvgDailyUsage'] = df_avg['AvgDailyUsage']/(7*weeks_)
                                df_avg['Item'] = df_avg['Item'].astype(str)
                                df_avg['Location'] = df_avg['Location'].astype(str)
                                df_invopt['Item'] = df_invopt['Item'].astype(str)
                                df_invopt['Location'] = df_invopt['Location'].astype(str)
                                
                                df_extract = pd.merge(df_invopt,df_avg[['Item','Location','AvgDailyUsage']],on=['Item','Location'],how='left')
                              
                            else:
                                df_avg = df_avg[['Date','Item','Target',column_forecast]]
                                df_avg['AvgDailyUsage'] = df_avg['Target'].copy()

                                df_avg = df_avg.groupby(['Item'], as_index=False).agg({'AvgDailyUsage': sum}).reset_index(drop=True)
                                df_avg['AvgDailyUsage'] = df_avg['AvgDailyUsage']/(7*weeks_)
                                df_avg['Item'] = df_avg['Item'].astype(str)
                                df_invopt['Item'] = df_invopt['Item'].astype(str)
                                
                                df_extract = pd.merge(df_invopt,df_avg[['Item','AvgDailyUsage']],on=['Item'],how='left')

                df_extract['AvgDailyUsage'] = round(df_extract['AvgDailyUsage'],3)
                df_extract.loc[(df_extract['AvgDailyUsage']<0),'AvgDailyUsage'] = 0
            
            except KeyError as err:
                self.logger.exception(f'No column found. Please check columns names: {err}')
                print(f'No column found. Please check columns names')
                raise
            return df_extract


        # MAX SALES ----------------------------------------------------------------

        def extract_max_daily(self, df_Prep ,df_Forecast, df_invopt, forecast_=False,location=False,column_forecast='SuggestedForecast',frequency_='M',months_=4,weeks_= 16): 
            """
            Returns a data frame that incorporates the MaxDailyUsage column into the inventory data frame.

            : param df_Prep: Dataframe prepared for Forecast
            : param df_Forecast: Forecast's Dataframe 
            : param df_invopt: Inventory's Dataframe with the columns Item, Location(Optional), Inventory, Transit
            : param forecast_: Boolean to allow the use of the Suggested Forecast to calculate the max
            : param location: Boolean to enable the use of Location in the Inventory's dataframe
            : param column_forecast: name of the column where the desired forecast is located 
            : param frequency_: Target frequency to the dataset
            : param months_: Target Number months 
            : param weeks_: Target Number weeks 

            >>> df_extract = extract_max_daily(df_Prep = df_prep,
                                              df_Forecast = df_fcst,
                                              df_invopt = df_avg, 
                                              forecast_=False,
                                              location = True,
                                              column_forecast='SuggestedForecast',
                                              months_ = 4 ,
                                              frequency_ = 'M')
            >>> df_extract =
                                                Item    Location   Inventory   Transit     MaxDailyUsage
                                    idx0          85      905         23            0             20
                                    idx1          102     487         95            0             10
            """
            
            try:

              if forecast_ == True:
                
                    if frequency_ == 'M':
                    
                          df_avg = df_Forecast[(df_Forecast['Date'] >= df_Prep['timestamp'].max()) & 
                                              (df_Forecast['Date'] < (df_Prep['timestamp'].max() + relativedelta(months=months_) + MonthEnd(0)))]
                          
                          if location:

                              df_avg = df_avg[['Date','Item','Location','Target',column_forecast]]
                              df_avg['MaxDailyUsage'] = df_avg.apply(lambda x: x[column_forecast] if (x['Target']==0) else x['Target'], axis=1 )
                              
                              df_avg = df_avg.groupby(['Item','Location'], as_index=False).agg({'MaxDailyUsage': np.std}).reset_index(drop=True)
                              df_avg['MaxDailyUsage'] = (2*df_avg['MaxDailyUsage'])/(30*months_)
                              df_avg['Item'] = df_avg['Item'].astype(str)
                              df_avg['Location'] = df_avg['Location'].astype(str)
                              df_invopt['Item'] = df_invopt['Item'].astype(str)
                              df_invopt['Location'] = df_invopt['Location'].astype(str)
                              
                              df_extract = pd.merge(df_invopt,df_avg[['Item','Location','MaxDailyUsage']],on=['Item','Location'],how='left')
                            
                          else:
                              df_avg = df_avg[['Date','Item','Target',column_forecast]]
                              df_avg['MaxDailyUsage'] = df_avg.apply(lambda x: x[column_forecast] if (x['Target']==0) else x['Target'], axis=1 )

                              df_avg = df_avg.groupby(['Item'], as_index=False).agg({'MaxDailyUsage': np.std}).reset_index(drop=True)
                              df_avg['MaxDailyUsage'] = (2*df_avg['MaxDailyUsage'])/(30*months_)
                              df_avg['Item'] = df_avg['Item'].astype(str)
                              df_invopt['Item'] = df_invopt['Item'].astype(str)
                              
                              df_extract = pd.merge(df_invopt,df_avg[['Item','MaxDailyUsage']],on=['Item'],how='left')
                    
                    if frequency_ == 'W':
                    
                          df_avg = df_Forecast[(df_Forecast['Date'] >= df_Prep['timestamp'].max()) & 
                                              (df_Forecast['Date'] < (df_Prep['timestamp'].max() + relativedelta(weeks=weeks_)))]
                          
                          if location:

                              df_avg = df_avg[['Date','Item','Location','Target',column_forecast]]
                              df_avg['MaxDailyUsage'] = df_avg.apply(lambda x: x[column_forecast] if (x['Target']==0) else x['Target'], axis=1 )
                              
                              df_avg = df_avg.groupby(['Item','Location'], as_index=False).agg({'MaxDailyUsage': np.std}).reset_index(drop=True)
                              df_avg['MaxDailyUsage'] = (2*df_avg['MaxDailyUsage'])/(7*weeks_)
                              df_avg['Item'] = df_avg['Item'].astype(str)
                              df_avg['Location'] = df_avg['Location'].astype(str)
                              df_invopt['Item'] = df_invopt['Item'].astype(str)
                              df_invopt['Location'] = df_invopt['Location'].astype(str)
                              
                              df_extract = pd.merge(df_invopt,df_avg[['Item','Location','MaxDailyUsage']],on=['Item','Location'],how='left')
                            
                          else:
                              df_avg = df_avg[['Date','Item','Target',column_forecast]]
                              df_avg['MaxDailyUsage'] = df_avg.apply(lambda x: x[column_forecast] if (x['Target']==0) else x['Target'], axis=1 )

                              df_avg = df_avg.groupby(['Item'], as_index=False).agg({'MaxDailyUsage': np.std}).reset_index(drop=True)
                              df_avg['MaxDailyUsage'] = (2*df_avg['MaxDailyUsage'])/(7*weeks_)
                              df_avg['Item'] = df_avg['Item'].astype(str)
                              df_invopt['Item'] = df_invopt['Item'].astype(str)
                              
                              df_extract = pd.merge(df_invopt,df_avg[['Item','MaxDailyUsage']],on=['Item'],how='left')

              if forecast_ == False:
                
                    if frequency_ == 'M':
                    
                          df_avg = df_Forecast[(df_Forecast['Date'] <= df_Prep['timestamp'].max()) & 
                                              (df_Forecast['Date'] > (df_Prep['timestamp'].max() - relativedelta(months=months_) + MonthEnd(0)))]
                          
                          if location:

                              df_avg = df_avg[['Date','Item','Location','Target',column_forecast]]
                              df_avg['MaxDailyUsage'] = df_avg['Target'].copy()
                              
                              df_avg = df_avg.groupby(['Item','Location'], as_index=False).agg({'MaxDailyUsage': np.std}).reset_index(drop=True)
                              df_avg['MaxDailyUsage'] = (2*df_avg['MaxDailyUsage'])/(30*months_)
                              df_avg['Item'] = df_avg['Item'].astype(str)
                              df_avg['Location'] = df_avg['Location'].astype(str)
                              df_invopt['Item'] = df_invopt['Item'].astype(str)
                              df_invopt['Location'] = df_invopt['Location'].astype(str)
                              
                              df_extract = pd.merge(df_invopt,df_avg[['Item','Location','MaxDailyUsage']],on=['Item','Location'],how='left')
                            
                          else:
                              df_avg = df_avg[['Date','Item','Target',column_forecast]]
                              df_avg['MaxDailyUsage'] = df_avg['Target'].copy()

                              df_avg = df_avg.groupby(['Item'], as_index=False).agg({'MaxDailyUsage': np.std}).reset_index(drop=True)
                              df_avg['MaxDailyUsage'] = (2*df_avg['MaxDailyUsage'])/(30*months_)
                              df_avg['Item'] = df_avg['Item'].astype(str)
                              df_invopt['Item'] = df_invopt['Item'].astype(str)
                              
                              df_extract = pd.merge(df_invopt,df_avg[['Item','MaxDailyUsage']],on=['Item'],how='left')
                    
                    if frequency_ == 'W':
                    
                          df_avg = df_Forecast[(df_Forecast['Date'] <= df_Prep['timestamp'].max()) & 
                                              (df_Forecast['Date'] > (df_Prep['timestamp'].max() - relativedelta(weeks=weeks_)))]
                          
                          if location:

                              df_avg = df_avg[['Date','Item','Location','Target',column_forecast]]
                              df_avg['MaxDailyUsage'] = df_avg['Target'].copy()
                              
                              df_avg = df_avg.groupby(['Item','Location'], as_index=False).agg({'MaxDailyUsage': np.std}).reset_index(drop=True)
                              df_avg['MaxDailyUsage'] = (2*df_avg['MaxDailyUsage'])/(7*weeks_)
                              df_avg['Item'] = df_avg['Item'].astype(str)
                              df_avg['Location'] = df_avg['Location'].astype(str)
                              df_invopt['Item'] = df_invopt['Item'].astype(str)
                              df_invopt['Location'] = df_invopt['Location'].astype(str)
                              
                              df_extract = pd.merge(df_invopt,df_avg[['Item','Location','MaxDailyUsage']],on=['Item','Location'],how='left')
                            
                          else:
                              df_avg = df_avg[['Date','Item','Target',column_forecast]]
                              df_avg['MaxDailyUsage'] = df_avg['Target'].copy()

                              df_avg = df_avg.groupby(['Item'], as_index=False).agg({'MaxDailyUsage': np.std}).reset_index(drop=True)
                              df_avg['MaxDailyUsage'] = (2*df_avg['MaxDailyUsage'])/(7*weeks_)
                              df_avg['Item'] = df_avg['Item'].astype(str)
                              df_invopt['Item'] = df_invopt['Item'].astype(str)
                              
                              df_extract = pd.merge(df_invopt,df_avg[['Item','MaxDailyUsage']],on=['Item'],how='left')

              df_extract['MaxDailyUsage'] = round(df_extract['MaxDailyUsage'],3)
              df_extract['MaxDailyUsage'] = df_extract['AvgDailyUsage'] + df_extract['MaxDailyUsage']
              df_extract.loc[(df_extract['MaxDailyUsage']<0),'MaxDailyUsage'] = 0
          
            except KeyError as err:
                self.logger.exception(f'No column found. Please check columns names: {err}')
                print(f'No column found. Please check columns names')
                raise
            return df_extract


        #INDICADORES -----------------------------------------------------------

        def functions_inventory(self, df_inv,min_inv=False,div_purfac=False,ref_secstock=False, exhivitions=False):
            """
                Return a dataframe with all the indicators 
            
                : param df_inv: Inventory's Dataframe with the columns Item, Location(Optional), Inventory, Transit, DemandHistory  SuggestedForecast AvgDailyUsage MaxDailyUsage           
                : param min_inv: Boolean to allow the minimum amount of inventory in location
                : param div_purfac: Boolean to allow data divided by purchase days 
                : param ref_secstock: Boolean to allow Security Stock Ref 
                : param exhivitions: Boolean to allow Exhivitions

                >>> df_inv = functions_inventory(df_inv,min_inv=False,div_purfac=False,ref_secstock=False,exhivitions=False)  

            """
            try:
                df=df_inv.copy()
                
                df['InventoryTransit'] = df['Inventory'] + df['Transit']
                
                df['InventoryTransitForecast'] = df['InventoryTransit'] - df['SuggestedForecast']
                
                df['LeadTimeDemand'] = df['SuggestedForecast']
                
                if ((ref_secstock==False) & (exhivitions==False)):
                    df['SecurityStock'] = ((df['MaxDailyUsage']*df['MaxLeadTime']) - (df['AvgDailyUsage']*df['AvgLeadTime']))
                
                if ((ref_secstock==True) & (exhivitions==False)):
                    df['SecurityStock'] = df['SecurityStockDaysRef'] * df['AvgDailyUsage']
                
                if ((ref_secstock==False) & (exhivitions==True)):
                    df['SecurityStock'] = (((df['MaxDailyUsage']*df['MaxLeadTime']) - (df['AvgDailyUsage']*df['AvgLeadTime']))) + df['Exhivitions']
                
                if ((ref_secstock==True) & (exhivitions==True)):
                    df['SecurityStock'] = (df['SecurityStockDaysRef'] * df['AvgDailyUsage']) + df['Exhivitions']                  
                
                df['SecurityStock'] = df['SecurityStock'].fillna(0)
                df['SecurityStock'] = df['SecurityStock'].map(lambda x: 0 if x < 1 else x)
                
                df['SecurityStockDays'] = (df['SecurityStock']) / (df['AvgDailyUsage'])
                df['SecurityStockDays'] = df['SecurityStockDays'].fillna(0)
                df['SecurityStockDays'] = df['SecurityStockDays'].map(lambda x: 0 if x < 0 else x)
                df['SecurityStockDays'] = df['SecurityStockDays'].astype(str).str.replace('-inf', '0').str.replace('inf', '0').str.replace('nan', '0')
                df['SecurityStockDays'] = df['SecurityStockDays'].astype(float)
                
                df['ReorderPoint'] = (df['LeadTimeDemand']  + df['SecurityStock'])
                df['ReorderPoint'] = df['ReorderPoint'].map(lambda x: 0 if x < 0 else x)
                
                df['ReorderPointDays'] = df['ReorderPoint'] / (df['AvgDailyUsage'])
                df['ReorderPointDays'] = df['ReorderPointDays'].fillna(0)
                df['ReorderPointDays'] = df['ReorderPointDays'].astype(str).str.replace('-inf', '0').str.replace('inf', '0').str.replace('nan', '0')
                df['ReorderPointDays'] = df['ReorderPointDays'].astype(float)
                    
                df['ReorderStatus']=df[['InventoryTransit','ReorderPoint']].apply(lambda x: 'Order' if (x['InventoryTransit'] < x['ReorderPoint']) else 'Hold', axis=1)
                df['ReorderStatus']=df[['InventoryTransit','ReorderPoint','ReorderStatus']].apply(lambda x: 'Hold' if (((x['ReorderPoint'] - x['InventoryTransit']) <1 ) & ((x['ReorderPoint'] - x['InventoryTransit']) >0 ) & (x['ReorderStatus']=='Order')) else x['ReorderStatus'], axis=1)
                        
                if min_inv == False:
                    df['RQty'] = (df['ReorderPoint'] - df['InventoryTransit'] ).abs()
                    df['ReorderQty'] = df[['ReorderStatus','RQty']].apply(lambda x: x['RQty'] if (x['ReorderStatus']=='Order') else 0 , axis=1 )
                    df['ReorderQty'] = df[['ReorderQty','ReorderStatus']].apply(lambda x: (0 if (x['ReorderQty'] < 1) else x['ReorderQty']) if(x['ReorderStatus']=='Order') else x['ReorderQty'], axis=1)
                    
                if min_inv == True:
                    df['RQty'] = (df['ReorderPoint'] - df['InventoryTransit'] ).abs()
                    df['ReorderQty'] = df[['ReorderStatus','RQty','DemandHistory']].apply(lambda x: x['RQty'] if (x['ReorderStatus']=='Order') else x['DemandHistory'] , axis=1 )
                    df['ReorderQty'] = df[['ReorderQty','ReorderStatus']].apply(lambda x: (0 if (x['ReorderQty'] < 1) else x['ReorderQty']), axis=1)
                    
                df['MinQty'] = (df['BackSuggestedForecast'] + df['SecurityStock']- df['InventoryTransit']).abs()   
                df['MaxQty'] = (df['NextSuggestedForecast'] + df['SecurityStock']- df['InventoryTransit'] ).abs()
                
                df['MinReorderQty'] = df[['ReorderStatus','MinQty','MaxQty']].apply(lambda x: (x['MinQty'] if (x['MinQty']<x['MaxQty']) else x['MaxQty']) if (x['ReorderStatus']=='Order') else 0 , axis=1 )
                df['MinReorderQty'] = df[['MinReorderQty','ReorderStatus']].apply(lambda x: (0 if (x['MinReorderQty'] < 1) else x['MinReorderQty']) if(x['ReorderStatus']=='Order') else x['MinReorderQty'], axis=1)
                
                df['MaxReorderQty'] = df[['ReorderStatus','MinQty','MaxQty']].apply(lambda x: (x['MinQty'] if (x['MinQty']>x['MaxQty']) else x['MaxQty']) if (x['ReorderStatus']=='Order') else 0 , axis=1 )
                df['MaxReorderQty'] = df[['MaxReorderQty','ReorderStatus']].apply(lambda x: (0 if (x['MaxReorderQty'] < 1 )else x['MaxReorderQty']) if(x['ReorderStatus']=='Order') else x['MaxReorderQty'], axis=1)
                
                df['RQtyTwoPeriods'] = (df['SuggestedForecast_2p'] + df['SecurityStock']- df['InventoryTransit']).abs() 
                df['ReorderQtyTwoPeriods'] = df[['ReorderStatus','RQtyTwoPeriods']].apply(lambda x: x['RQtyTwoPeriods'] if (x['ReorderStatus']=='Order') else 0 , axis=1 )
                df['ReorderQtyTwoPeriods'] = df[['ReorderQtyTwoPeriods','ReorderStatus']].apply(lambda x: (0 if (x['ReorderQtyTwoPeriods'] < 1) else x['ReorderQtyTwoPeriods']) if(x['ReorderStatus']=='Order') else x['ReorderQtyTwoPeriods'], axis=1)
                
                df['RQtyThreePeriods'] = (df['SuggestedForecast_3p'] + df['SecurityStock']- df['InventoryTransit']).abs() 
                df['ReorderQtyThreePeriods'] = df[['ReorderStatus','RQtyThreePeriods']].apply(lambda x: x['RQtyThreePeriods'] if (x['ReorderStatus']=='Order') else 0 , axis=1 )
                df['ReorderQtyThreePeriods'] = df[['ReorderQtyThreePeriods','ReorderStatus']].apply(lambda x: (0 if (x['ReorderQtyThreePeriods'] < 1) else x['ReorderQtyThreePeriods']) if(x['ReorderStatus']=='Order') else x['ReorderQtyThreePeriods'], axis=1)
                
                df.drop(columns=['RQty','MinQty','MaxQty','RQtyTwoPeriods','RQtyThreePeriods'],inplace=True)                             
                
                df['StockoutDays']=(df['Inventory']-df['SecurityStock'])/df['AvgDailyUsage']
                df['StockoutDays'] = df['StockoutDays'].fillna(0)
                df['StockoutDays'] = df['StockoutDays'].map(lambda x: 0 if x < 0 else x)
                df['StockoutDays'] = df['StockoutDays'].astype(str).str.replace('-inf', '0').str.replace('inf', '0').str.replace('nan', '0')
                df['StockoutDays'] = df['StockoutDays'].astype(float)

                df['InvTransStockoutDays']=(df['InventoryTransit']-df['SecurityStock'])/df['AvgDailyUsage']
                df['InvTransStockoutDays'] = df['InvTransStockoutDays'].fillna(0)
                df['InvTransStockoutDays'] = df['InvTransStockoutDays'].map(lambda x: 0 if x < 0 else x)
                df['InvTransStockoutDays'] = df['InvTransStockoutDays'].astype(str).str.replace('-inf', '0').str.replace('inf', '0').str.replace('nan', '0')
                df['InvTransStockoutDays'] = df['InvTransStockoutDays'].astype(float)
                
                df['ForecastStockoutDays']=(df['InventoryTransitForecast']-df['SecurityStock'])/df['AvgDailyUsage']
                df['ForecastStockoutDays'] = df['ForecastStockoutDays'].fillna(0)
                df['ForecastStockoutDays'] = df['ForecastStockoutDays'].map(lambda x: 0 if x < 0 else x)
                df['ForecastStockoutDays'] = df['ForecastStockoutDays'].astype(str).str.replace('-inf', '0').str.replace('inf', '0').str.replace('nan', '0')
                df['ForecastStockoutDays'] = df['ForecastStockoutDays'].astype(float)
                
                if div_purfac == False:
                    df['ReorderQty'] = ((df['ReorderQty']/df['PurchaseFactor']).apply(np.ceil))*df['PurchaseFactor']
                    df['MinReorderQty'] = ((df['MinReorderQty']/df['PurchaseFactor']).apply(np.ceil))*df['PurchaseFactor']
                    df['MaxReorderQty'] = ((df['MaxReorderQty']/df['PurchaseFactor']).apply(np.ceil))*df['PurchaseFactor']
                    df['ReorderQtyTwoPeriods'] = ((df['ReorderQtyTwoPeriods']/df['PurchaseFactor']).apply(np.ceil))*df['PurchaseFactor']
                    df['ReorderQtyThreePeriods'] = ((df['ReorderQtyThreePeriods']/df['PurchaseFactor']).apply(np.ceil))*df['PurchaseFactor']   

                    df['ReorderQtyFactor']=round(df['ReorderQty']/df['PurchaseFactor'])
                    df['ReorderQtyTwoPeriodsFactor']=round(df['ReorderQtyTwoPeriods']/df['PurchaseFactor'])
                    df['ReorderQtyThreePeriodsFactor']=round(df['ReorderQtyThreePeriods']/df['PurchaseFactor'])
                    
                if div_purfac == True:
                    df['ReorderQtyFactor']=df['ReorderQty']   
                    df['ReorderQtyTwoPeriodsFactor']=df['ReorderQtyTwoPeriods']
                    df['ReorderQtyThreePeriodsFactor']=df['ReorderQtyThreePeriods']   

                if 'UnitCost' not in df.columns:
                    df.loc[:,'UnitCost'] = 0           

                if 'TotalCost' not in df.columns:        
                    df.loc[:,'TotalCost'] = df['UnitCost']*df['ReorderQty']
                
            except KeyError as err:
                self.logger.exception(f'No column found. Please check columns names: {err}')
                print(f'No column found. Please check columns names')
                raise         
            return df        

        #FORMAT-------------------------------------------------
        def clean_and_format(self,df_invopt):
            """
            Return a dataframe with the correct format       
            : param df: Inventory's Dataframe 
                
            >>> df = clean_and_format(df)
            """           
            try:
                df=df_invopt.copy()
                indicators=['Item','ItemDescription','Location','LocationDescription','Inventory','Transit', 'Transfer','Committed',
                            'InventoryTransit','InventoryTransitForecast','StockoutDays','InvTransStockoutDays',
                            'DemandHistory','SuggestedForecast','NextSuggestedForecast','BackSuggestedForecast',
                            'SuggestedForecast_2p','SuggestedForecast_3p','ForecastStockoutDays',
                            'Ranking','AvgDailyUsage','MaxDailyUsage','AvgLeadTime','MaxLeadTime','LeadTimeDemand',
                            'SecurityStock','SecurityStockDays',
                            'ReorderPoint','ReorderPointDays','ReorderFreq','Coverage',
                            'ReorderStatus','ReorderQty','MinReorderQty','MaxReorderQty','ReorderQtyTwoPeriods','ReorderQtyThreePeriods',
                            'PurchaseFactor','ReorderQtyFactor','ReorderQtyTwoPeriodsFactor','ReorderQtyThreePeriodsFactor',
                            'Provider','ProviderDescription','UM','MinOrderQty','MaxOrderQty','DeliveryFactor','PurchaseOrderUnit','PalletFactor',
                            'SecurityStockDaysRef', 'Exhivitions',
                            'UnitCost','TotalCost','LastCost','Customer','Country',
                            'ProductType','Weight','Dimension','Color','Origen','Gama', 
                            'Marca','MateriaPrima','JefeProducto','JefeProductoDescription','GrupoCompra','Familia',
                            'Seccion','Categoria', 'Linea','Canal','InventoryUnit','Comments']

                for val,name in enumerate(indicators):
                    if name not in df.columns:
                        df[name] = "N/A"

                cols1 = ['Inventory', 'ReorderFreq','Coverage', 'Transit', 'Committed', 'Transfer',          
                    'DemandHistory','SuggestedForecast','NextSuggestedForecast','BackSuggestedForecast',
                    'SuggestedForecast_2p','SuggestedForecast_3p',
                    'InventoryTransit', 'InventoryTransitForecast','SecurityStock', 'SecurityStockDays','SecurityStockDaysRef', 'Exhivitions',
                    'ReorderPoint','ReorderPointDays',
                    'ReorderQty', 'MinReorderQty', 'MaxReorderQty',
                    'ReorderQtyTwoPeriods','ReorderQtyThreePeriods',
                    'ReorderQtyFactor','ReorderQtyTwoPeriodsFactor','ReorderQtyThreePeriodsFactor',
                    'StockoutDays', 'ForecastStockoutDays','InvTransStockoutDays']

                for a in cols1:
                    df[a] = df[a].astype(str).replace("N/A",'0')
                    df[a] = df[a].astype(float) 
                    df[a] = df[a].apply(np.ceil)
                    df[a] = df[a].astype(int) 

                cols =  df.select_dtypes(['float']).columns
                df[cols] =  df[cols].apply(lambda x: round(x, 3))
                
                df = df[indicators]
                df = df.drop_duplicates().reset_index(drop=True) 
                df = df.sort_values(by=['Ranking','Item']).drop_duplicates().reset_index(drop=True) 

            except KeyError as err:
                self.logger.exception(f'No column found. Please check columns names: {err}')
                print(f'No column found. Please check columns names')
                raise
            return df 


        # TBL INVENTORY -------------------------------------------------
        def functions_tblinv(self, df_inv):
            """
                Return a dataframe with all the indicators             
                : param df_inv: Inventory's Dataframe with the columns      
                >>> df_inv = functions_tblinv(df_inv)  
            """
            try:
                df=df_inv.copy()                
                df.loc[:,'InventoryTransit'] = df['Inventory'] + df['Transit']
                df.loc[:,'StockoutDays']=( df['Inventory']- df['SecurityStock'])/ df['AvgDailyUsage']
                df.loc[:,'StockoutDays'] = df['StockoutDays'].fillna(0)
                df.loc[:,'StockoutDays'] = df['StockoutDays'].map(lambda x: 0 if x < 0 else x)
                df.loc[:,'StockoutDays'] = df['StockoutDays'].astype(str).str.replace('-inf', '0').str.replace('inf', '0').str.replace('nan', '0')
                df.loc[:,'StockoutDays'] = df['StockoutDays'].astype(float)

                df.loc[:,'InvTransStockoutDays'] = ( df['Inventory'] + df['Transit']- df['SecurityStock'])/ df['AvgDailyUsage']
                df.loc[:,'InvTransStockoutDays'] = df['InvTransStockoutDays'].fillna(0)
                df.loc[:,'InvTransStockoutDays'] = df['InvTransStockoutDays'].map(lambda x: 0 if x < 0 else x)
                df.loc[:,'InvTransStockoutDays'] = df['InvTransStockoutDays'].astype(str).str.replace('-inf', '0').str.replace('inf', '0').str.replace('nan', '0')
                df.loc[:,'InvTransStockoutDays'] = df['InvTransStockoutDays'].astype(float)
                
            except KeyError as err:
                self.logger.exception(f'No column found. Please check columns names: {err}')
                print(f'No column found. Please check columns names')
                raise         
            return df  

        def format_tblinv(self,df_invopt):
            """
            Return a dataframe with the correct format       
            : param df: Inventory's Dataframe 
              
            >>> df = format_tblinv(df)
            """           
            try:
                df=df_invopt.copy()
                df=df.fillna(0) 
                indicators=['Item','ItemDescription',	'Location',	'Country',
                            'Inventory',	'Transit',	'TransitDate',	 'TransitAdditional',	 'Committed',
                            'UM',	'InventoryTransit',	'StockoutDays',	'InvTransStockoutDays',	'Ranking',
                            'Provider',	'ProductType',	'Customer',	'JefeProducto','GrupoCompra',	'Seccion',
                            'Origen',	'Color',	'Marca','MateriaPrima','Gama']

                for val,name in enumerate(indicators):
                    if name not in df.columns:
                        df[name] = "N/A"

                cols1 = ['Inventory','Transit', 'Committed','InventoryTransit','StockoutDays','InvTransStockoutDays' ]

                for a in cols1:
                    df[a] = df[a].astype(str).replace("N/A",'0')
                    df[a] = df[a].astype(float) 
                    df[a] = df[a].apply(np.ceil)
                    df[a] = df[a].astype(int) 

                cols =  df.select_dtypes(['float']).columns
                df[cols] =  df[cols].apply(lambda x: round(x, 3))
                
                df = df[indicators]
                df = df.drop_duplicates().reset_index(drop=True)  

            except KeyError as err:
                self.logger.exception(f'No column found. Please check columns names: {err}')
                print(f'No column found. Please check columns names')
                raise
            return df 