import datetime
import requests
from requests import HTTPError
import math

from openweatherclass.geodataclass import GeoDataClass
from openweatherclass.historydataclass import HistoricDataClass
from openweatherclass.weatherdataclass import WeatherDataClass
from openweatherclass.condition_codes import condition_codes


class OpenWeatherClass:

    def __init__(self, api_key, zipcode, units='metric'):
        self.API_KEY = api_key
        self.zipcode = zipcode
        self.units = units
        self.weather_data = WeatherDataClass
        self.geo_data = GeoDataClass
        self.historic_data = HistoricDataClass
        self.today_historic_data = HistoricDataClass
        self.condition_codes = condition_codes
        self.lat = 0
        self.lon = 0
        self.get_coordinates()
        self.get_weather()

    def get_coordinates(self):
        zip_request = None
        payload = {
            'zip': f"{self.zipcode}",
            'appid': self.API_KEY,
        }
        try:
            zip_request = requests.get(url='https://api.openweathermap.org/geo/1.0/zip', params=payload)
            zip_request.raise_for_status()
        except HTTPError:
            print("Error Fetching Data...")
        self.geo_data = zip_request.json()
        self.lat = self.geo_data['lat']
        self.lon = self.geo_data['lon']

    def get_weather(self):
        weather_request = None
        payload = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": self.API_KEY,
            "units": self.units
        }
        try:
            weather_request = requests.get(url='https://api.openweathermap.org/data/2.5/onecall', params=payload)
            weather_request.raise_for_status()
        except HTTPError:
            print("Error Fetching Data...")
        self.weather_data = weather_request.json()

    def update_weather(self):
        self.get_weather()

    def get_historic_weather(self, day):
        weather_request = None
        dt = math.floor((datetime.datetime.today() - datetime.timedelta(days=day)).timestamp())
        payload = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": self.API_KEY,
            "units": self.units,
            "dt": dt
        }
        try:
            weather_request = requests.get(url='https://api.openweathermap.org/data/2.5/onecall/timemachine',
                                           params=payload)
            weather_request.raise_for_status()
        except HTTPError:
            print("Error Fetching Data...")
        self.historic_data = weather_request.json()

    def get_today_history(self):
        weather_request = None
        dt = math.floor((datetime.datetime.today() - datetime.timedelta(days=1)).timestamp())
        payload = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": self.API_KEY,
            "units": self.units,
            "dt": dt
        }
        try:
            weather_request = requests.get(url='https://api.openweathermap.org/data/2.5/onecall/timemachine',
                                           params=payload)
            weather_request.raise_for_status()
        except HTTPError:
            print("Error Fetching Data...")
        self.today_historic_data = weather_request.json()

    def check_condition(self, code):
        for codes in self.condition_codes:
            try:
                if codes['code'] == code:
                    return codes['description']
            except IndexError:
                print("Not Found.")
