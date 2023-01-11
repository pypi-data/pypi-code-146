# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt
import requests, io
from .api import quantim

class portfolios(quantim):
    def __init__(self, username, password, secretpool, env="qa"):
        super().__init__(username, password, secretpool, env)

    def get_portfolios(self, ref_date=None, country=None, fields=None, port_names=None, clean=False):
        '''
        Query portfolios from database.

        Parameters:
        ----------
        ref_date : String
            Portfolios data in format %Y-%m-%d (default None)
        country : Array of Strings
            Country code [CO, CL, MX] (default None)
        fields : Array
            Array of fields (default None)
        port_names : Array
            Array of portfolios names (default None)
        clean : bool
            Indicator thar removes empty columns (default False)

        Returns:
        -------
        : pandas.DataFrame
        '''

        if (country is None or  len(country)==0) and port_names is None:
            raise ValueError('Either country or port_names must be different to None.')

        data = {'date':ref_date, 'country':country, 'fields':fields, 'port_names':port_names, 'clean':clean, 'res_url':True}
        ports_url = self.api_call('query_portfolios', method="post", data=data, verify=False)
        ports_data = requests.get(ports_url, verify=False)
        ports_df = pd.read_csv(io.StringIO(ports_data.content.decode('utf-8')))

        return ports_df

    def get_portfolios_views(self, ref_date=None, country=None, port_names=None, asset=None):
        '''
        Get portfolio views
        '''
        if country is None and port_names is None:
            raise ValueError('Either country or port_names must be different to None.')
        data = {'date':ref_date, 'country':country, 'port_names':port_names, 'asset':asset}
        resp = self.api_call('query_portfolios_views', method="post", data=data, verify=False)
        ports_df = pd.DataFrame(resp)

        return ports_df
