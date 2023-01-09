'''
reinan br <slimchatuba@gmail.com>
31/12/2021 15:46
Lib: noawclg (light version from noaawc) v0.0.1b0
=================================================================
Why it work use the GPLv3 LICENSE?
-----------------------------------------------------------------
    this project use the license GPLv3  because i have a hate 
    for the other projects that 're privates in the social network's
    that use the 'open data' from noaa in the your closed source,
    and i see it, i getted it init that make the ant way
    from this method, and making the condiction that who use it
    project on your personal project, open your project, or win
    a process.

=================================================================
what's for it project?
-----------------------------------------------------------------
    This project is for a best development in works with 
    climate prediction and getting it data from the 
    opendata in noaa site on type netcdf.

=================================================================
it's a base from the noaawc lib
-----------------------------------------------------------------
    This will are the base from a lib very more big from it's,
    your name will call as 'nooawc', and because from need
    mpl_toolkits.basemap, your work will are possible only
    the anaconda.
'''

__version__ = '0.0.3'
__author__ = 'Reinan Br'


# importing the need lib's
#import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from datetime import datetime
# import requests as rq
# from bs4 import beautifulsoup as soup

import matplotlib.pyplot as plt
plt.style.use('seaborn')
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent='Mozilla/5.0 (Linux; U; Android 4.4.2; zh-cn; GT-I9500 Build/KOT49H) AppleWebKit/537.36(KHTML, like Gecko)Version/4.0 MQQBrowser/5.0 QQ-URL-Manager Mobile Safari/537.36')



date_now = datetime.now
date_base_param = date_now().strftime('%Y/%m/%d')


print(xr.__version__)

def fmt(dt): return dt

# function for get data from noaa dataOpen 
# Tḧis function is the base from the all work
# because its getting the data from noaa
class get_noaa_data:
    __version__ = __version__
    __author__ = __author__
    
    def __init__(self,date:str=None,hour:str='00',gfs:str='0p25',url_data:str=None):
        '''
            params:
                date: str
                    input a date in mode day/moth/year
                    ex: 08/01/2022
        '''
        
        if not date:
            date=date_base_param
        self.date = date
        date = datetime.strptime(date,'%d/%m/%Y')
        date = date.strftime('%Y%m%d')
        print(date)
        
        self.gfs = gfs
        self.url_data = url_data
        self.hour = hour
        
        date_input=date
        date=date.split('/')
        date=''.join(date)
        #print(date)
        # url base from the data noaa in GFS 0.25 or GFS 1.00
        #url_cdf=f'https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs{date}/gfs_0p25_{hour}z'
        url_cdf=f'https://nomads.ncep.noaa.gov/dods/gfs_{gfs}/gfs{date}/gfs_{gfs}_{hour}z'#'https://nomads.ncep.noaa.gov/dods/gfs_0p25/gfs20230103/gfs_0p25_00z'
       
        
        if url_data:
            print('hmm, url_data, its a urgency?..')
            url_cdf=url_data
    
        #self.date = date
        self.gfs = gfs
        self.url_data = url_data
        self.hour = hour
        print(f'url_data: {url_cdf}')
        # reading the data required in the param's
        file = xr.open_dataset(url_cdf)
        
        self.file_noaa = file
        
    
    def __getitem__(self,key:str):
        data_get = self.file_noaa.variables[key]
        return data_get
    
    # getting the list data present in the data noaa GFS 0.25
    def get_noaa_keys(self):
        '''
        '''

        keys = self.file_noaa.variables.keys()
        keys_about = {}
        for key in keys:
            about_key = self.file_noaa.variables[key].attrs['long_name'] 
            keys_about[key]=about_key
        
        return keys_about


    def get_data_from_point(self,point:tuple):
        '''
        '''
        new_data = get_noaa_data(hour=self.hour,date=self.date,gfs=self.gfs,url_data=self.url_data)
        #data = self.file.variables
        
        lat,lon = point[0],360+(point[1]) if point[1]<0 else point[1]
        print(f"never print it!! just get the your need data's. ")
        data_point = new_data.file_noaa.sel(lon=lon,lat=lat,method='nearest')
        # data_point = {'time':data_point.variables['time'],'data':data_point.variables[data_key]}
        
        return data_point
    
    
    def get_data_from_place(self,place:str):
        location = geolocator.geocode(place)
        point = (location.latitude, location.longitude)
        print(point)

        data_point = self.get_data_from_point(point=point)

        return data_point
    
    

    def plot_data_from_place(self,place:str,title=f'plot'
                             ,path_file:str='plot_temp.png',dpi:int=600,
                             by='by @gpftc_ifsertão',key_noaa='tmp80m',fmt_data=fmt,
                             max_label:str='max',med_label='med',min_label='min',
                             xlabel='date',ylabel='',show=True,cla=True):
        if cla:
            plt.cla()
            plt.clf()
        data_point = self.get_data_from_place(place)
        temp = fmt_data(data_point[key_noaa])
        print('getted data..')
        temp = temp.to_pandas()

        m_temp = temp.rolling(8).mean()
        max_temp = temp.rolling(8).max()
        min_temp = temp.rolling(8).min()

        ax2 = max_temp.plot(label=max_label)
        ax1 = m_temp.plot(label=med_label)
        ax3 = min_temp.plot(label=min_label)

        plt.title(title,fontweight='bold')
        plt.legend()
        #plt.annotate('by @gpftc_ifsertâo',xy=(temp.index[10],20))
        plt.text(0.14, 0.07, by, fontsize=10, fontweight='bold', transform=plt.gcf().transFigure)
        about_key=self.get_noaa_keys()[key_noaa]
        key_about = f'{key_noaa}:\n {about_key}'
        plt.text(0.65, 0.07, key_about, fontsize=8, transform=plt.gcf().transFigure)

        plt.xlabel(xlabel)
        plt.ylabel(ylabel)

        plt.tight_layout()
        plt.savefig(path_file,dpi=dpi)
        if show:
            plt.show()
            
        return plt



