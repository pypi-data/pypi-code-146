import requests
import pandas as pd
from io import StringIO
from piwikapi.analytics import PiwikAnalytics

#%%
class PiwikRaumoLive():
    def __init__(self, config, start, stop):
        self.api_url = config.URL
        self.api_token = config.TOKEN
        self.STOP = stop
        self.START = start

    def build(self, idsite):
        self.pa = PiwikAnalytics()
        self.pa.set_api_url(self.api_url)
        self.pa.set_parameter('token_auth', self.api_token)
        self.pa.set_id_site(idsite) 
        self.pa.set_parameter('segment', 'dimension1==live')
        self.pa.set_filter_limit(-1)
        self.pa.set_period('day')
        self.pa.set_date('{},{}'.format(self.START,self.STOP))

    def query_as_csv(self):
        self.pa.set_format('CSV')
        query = self.pa.get_query_string()

        resp = requests.get(query)
        csv = StringIO(resp.text)
        df = pd.read_csv(csv,sep=',')
        df.index = pd.to_datetime(df['date'])

        return df

    def return_query(self):
        self.pa.set_format('CSV')
        query = self.pa.get_query_string()

        return query

    def convert_relative_to_numeric(self, df):
        df = df.str.replace(',','.')
        df = df.str.removesuffix('%')
        df = df.str.strip()
        return pd.to_numeric(df)/100

    def query_events_eventname(self, label, idsite):
        self.build(idsite)
        self.pa.set_method('Events.getName')
        self.pa.set_parameter('label', label)

        return self.query_as_csv()

    def query_events_eventname_combi(self, label, label2, idsite):
        self.build(idsite)
        self.pa.set_method('Events.getName')
        self.pa.set_parameter('label', label2)
        self.pa.set_parameter('label', label)

        return self.query_as_csv()

    def query_visits(self, idsite):
        self.build(idsite)
        self.pa.set_method('API.get')

        return self.query_as_csv()

    def query_conversions(self, idsite):
        self.build(idsite)
        self.pa.set_method('Goals.get')

        df = self.query_as_csv()
        df['conversion_rate'] = self.convert_relative_to_numeric(df['conversion_rate'])

        return df