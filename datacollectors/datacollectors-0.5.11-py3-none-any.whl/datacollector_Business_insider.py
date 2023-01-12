import requests
from dateutil import parser


class Business_insider():
    @staticmethod
    def metals_prices(commodity, start_date, end_date):
        _data = Business_insider._data_loader(commodity, start_date, end_date)
        _data = [{'date': parser.parse(obs['Date']), 'value': obs['Close'], 'metal': commodity} for obs in _data]
        return _data

    @staticmethod
    def metals_prices_df(commodity, start_date, end_date):
        import pandas as pd
        _data = Business_insider.metals_prices(commodity, start_date, end_date)
        df = pd.DataFrame(_data)
        df = df.set_index('date')
        df = df.sort_index()
        return df

    @classmethod
    def _data_loader(cls, commodity, start_date, end_date):
        product_dict = cls._parms()
        url_base = f'https://markets.businessinsider.com/Ajax/Chart_GetChartData?instrumentType=Commodity'
        url_commodity = f'&tkData=300002,{product_dict[commodity]},0,333'
        url_date = f'&from={start_date.strftime("%Y%m%d")}&to={end_date.strftime("%Y%m%d")}'
        url = f'{url_base}{url_commodity}{url_date}'
        _indata = requests.get(url).json()
        return _indata

    @classmethod
    def _parms(cls):
        _parms_dict = {
            "Copper": 9,
            "Aluminium": 7,
            "Gold": 1,
            "Silver": 2,
        }
        return _parms_dict
