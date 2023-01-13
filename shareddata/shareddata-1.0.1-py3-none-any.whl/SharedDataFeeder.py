import pandas as pd
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time

from SharedData.Metadata import Metadata
from SharedData.Logger import Logger
from SharedData.SharedDataPeriod import SharedDataPeriod

class SharedDataFeeder():
    
    def __init__(self, sharedData, feeder):
        self.feeder = feeder
        self.sharedData = sharedData    
        self.database = sharedData.database        
        self.default_collections = None
        
        # DATA DICTIONARY
        # data[period][tag]
        self.data = {} 
    
        # DATASET        
        self.dataset_metadata = Metadata(\
            'DATASET/' + sharedData.database + '/' + feeder,\
            mode=sharedData.mode,\
            user=sharedData.user)
        
        self.dataset = self.dataset_metadata.static
        self.collections = pd.Index([])
        if len(self.dataset)>0:
            ucoll = self.dataset['collections'].unique()
            for coll in ucoll:
                c = coll.replace('\n','').split(',')
                self.collections = self.collections.union(c)

            uperiod = self.dataset['period'].unique()
            for period in uperiod:
                self.data[period] = SharedDataPeriod(self, period)
                ustartdate = self.dataset.set_index('period')['startDate'].unique()
                for startdate in ustartdate:
                    self.data[period].getContinousTimeIndex(startdate)    
    
    def __setitem__(self, period, value):
        self.data[period] = value
                
    def __getitem__(self, period):
        if not period in self.data.keys():
            if (period=='D1') | (period=='M15') | (period=='M1'):
                self.data[period] = SharedDataPeriod(self, period)
            else:
                Logger.log.error('Period '+period+ ' not supported!')
                raise ValueError('Period '+period+ ' not supported!')
        return self.data[period]

    def load(self, period='D1', tags=None):
            
        if not self.default_collections is None:
            for c in self.default_collections.replace('\n','').split(','):
                self.sharedData.getMetadata(c)    

        for c in self.collections:
            self.sharedData.getMetadata(c)
        
        if tags is None:            
            idx = self.dataset['period'] == period
            tags = self.dataset['tag'][idx].values
        
        n_workers = len(tags)
        if n_workers>0:
            with ThreadPoolExecutor(n_workers) as exe:
                futures = [exe.submit(self.load_tag, period, tag) for tag in tags]                
                data = [future.result() for future in futures]
         
    def load_tag(self,period,tag):        
        return self[period][tag]
 
    def save(self,  period='D1', tags=None, startDate=None):

        if not self.default_collections is None:
            for c in self.default_collections.replace('\n','').split(','):
                self.sharedData.getMetadata(c)    

        for c in self.collections:
            self.sharedData.getMetadata(c)

        if tags is None:
            tags = self[period].tags.keys()
            
        n_workers = len(tags)
        if n_workers>0:
            with ThreadPoolExecutor(n_workers) as exe:
                futures = [exe.submit(self.save_tag, period, tag, startDate) for tag in tags]
                data = [future.result() for future in futures]

    def save_tag(self, period, tag, startDate=None):
        if startDate is None:
            self[period].tags[tag].Write()
        else:
            self[period].tags[tag].Write(startDate=startDate)
       
    def dataset_scan(self,period='D1'):
        ds = self.dataset_metadata.static.reset_index().set_index('tag')
        d1 = self[period]
        tags = d1.dataset.index
        for tag in tags:
            ds.loc[tag,'last_valid_index'] = d1[tag].last_valid_index()
            ds.loc[tag,'index_count'] = d1[tag].shape[0]
            ds.loc[tag,'columns_count'] = d1[tag].shape[1]
            ds.loc[tag,'notnull_sum'] = d1[tag].notnull().sum().sum()   
            ds.loc[tag,'notnull_index'] = d1[tag].dropna(how='all',axis=0).shape[0]
            ds.loc[tag,'notnull_columns'] = d1[tag].dropna(how='all',axis=1).shape[1]
            ds.loc[tag,'density_ratio'] = ds.loc[tag,'notnull_sum']/(d1[tag].shape[0]*d1[tag].shape[1])
            ds.loc[tag,'density_ratio_index'] = ds.loc[tag,'notnull_index']/d1[tag].shape[0]
            ds.loc[tag,'density_ratio_columns'] = ds.loc[tag,'notnull_columns']/d1[tag].shape[1]
            ds.loc[tag,'create_map'] = d1.tags[tag].create_map
            ds.loc[tag,'init_time'] = d1.tags[tag].init_time
            ds.loc[tag,'last_update'] = d1.tags[tag].last_update
            ds.loc[tag,'first_update'] = d1.tags[tag].first_update            
            ds.loc[tag,'data_size'] = ds.loc[tag,'notnull_sum']*8/1000000
            ds.loc[tag,'memory_size'] = d1[tag].memory_usage(deep=True).sum()/1000000
            ds.loc[tag,'download_time'] = d1.tags[tag].download_time
            ds.loc[tag,'download_speed'] = np.nan
            if not pd.isnull(ds.loc[tag,'download_time']):
                ds.loc[tag,'download_speed'] = ds.loc[tag,'data_size']*1000000/d1.tags[tag].download_time
        self.dataset_metadata.static = ds.reset_index()
        return ds.reset_index()
