import requests


class ForecaAPI:
    api_base_url = "https://pfa.foreca.com"
    has_authenticated = False

    def __init__(self):
        self.location = None
        self.lang = "en"
        self.tz = "IR"
        self.client = requests.Session()

    def set_user_pass(self, username, password):
        self.username = username
        self.password = password

    def set_user_admin_password(self, password):
        self.admin_password = password

    def set_access_token(self, access_token):
        self.access_token = access_token
        self.client.headers.update(
            {'Authorization': 'Bearer ' + self.access_token})

    def get_access_token(self):
        return self.access_token

    def authenticate(self, expire_hours=1):
        if self.username is None or self.password is None:
            raise Exception("username and password are both required")
        url = f"{self.api_base_url}/authorize/token"
        body = {
            "user": self.username,
            "password": self.password,
            "expire_hours": expire_hours
        }

        response = self.client.post(url, json=body)
        if response.status_code == 200:
            data = response.json()
            self.has_authenticated = True
            self.access_token = data.get("access_token")
            self.client.headers.update(
                {'Authorization': 'Bearer ' + self.access_token})
            return True
        else:
            raise Exception(
                f"Could not authenticate with the provided credentials, with status_code = {response.status_code}")

    def set_lang(self, language):
        self.lang = language

    def set_tz(self, timzone_iana):
        self.tz = timzone_iana

    def set_location(self, lat=None, lon=None, location_id=None):
        if location_id is None:
            self.location = f"{lon},{lat}"
        else:
            self.location = location_id

    def fetch_keys(self):
        if self.username is None or self.password is None:
            raise Exception("username and password are both required")
        url = f"{self.api_base_url}/authorize/key"
        body = {
            "user": self.username,
            "password": self.password,
        }
        response = requests.post(url, json=body)
        return response.json()

    def month_usage(self, month):
        if month is None:
            raise Exception(
                "please provide the month with this format YYYY-MM")
        if self.username is None or self.password is None:
            raise Exception("username and admin password are both required")
        url = f"{self.api_base_url}/usage/month/"
        params = {
            "month": month
        }
        body = {
            "user": self.username,
            "password": self.admin_password,
        }
        response = requests.post(url, params=params, json=body)
        return response.json()
    
    
    def day_usage(self, day):
        if day is None:
            raise Exception(
                "please provide the day with this format YYYY-MM-DD")
        if self.username is None or self.password is None:
            raise Exception("username and admin password are both required")
        url = f"{self.api_base_url}/usage/day/"
        params = {
            "day": day
        }
        body = {
            "user": self.username,
            "password": self.admin_password,
        }
        response = requests.post(url, params=params, json=body)
        return response.json()
    
    
    def location_search(self, location_name):
        url = f"{self.api_base_url}/api/v1/location/search/"
        params = {
            "q": location_name,
            "lang": self.lang
        }
        response = self.client.post(url, params=params)
        return response.json()

    def location_info(self):

        url = f"{self.api_base_url}/api/v1/location/"
        params = {
            "location": self.location,
            "lang": self.lang
        }
        response = self.client.post(url, params=params)
        return response.json()

    def get_observation_weather_location(self,  stations=3, tempunit="C", winduint="m/s", rounding=1):
        url = f"{self.api_base_url}/api/v1/observation/latest/"
        params = {
            "location": self.location,
            "lang": self.lang,
            "tz": self.tz,
            "tempunit": tempunit,
            "winduint": winduint,
            "rounding": rounding
        }
        response = self.client.post(url, params=params)
        return response.json()

    def get_current_weather_location(self,  alt=None, tempunit="C", winduint="m/s", rounding=1):
        url = f"{self.api_base_url}/api/v1/current/"
        params = {
            "location": self.location,
            "lang": self.lang,
            "tz": self.tz,
            "alt": alt,
            "tempunit": tempunit,
            "winduint": winduint,
            "rounding": rounding
        }
        response = self.client.post(url, params=params)
        return response.json()

    def get_forecast_minutely(self,  periods=60):
        url = f"{self.api_base_url}/api/v1/forecast/minutely/"
        params = {
            "location": self.location,
            "lang": self.lang,
            "tz": self.tz,
            "periods": periods
        }

        response = self.client.post(url, params=params)
        return response.json()

    def get_forecast_15minutely(self,  alt=None, tempunit="C", winduint="m/s", periods=60, dataset="standard", rounding=1):
        url = f"{self.api_base_url}/api/v1/forecast/15minutely/"
        params = {
            "location": self.location,
            "lang": self.lang,
            "tz": self.tz,
            "periods": periods,
            "alt": alt,
            "tempunit": tempunit,
            "winduint": winduint,
            "rounding": rounding,
            "dataset": dataset
        }
        response = self.client.post(url, params=params)
        return response.json()

    def get_forecast_hourly(self,  alt=None, tempunit="C", winduint="m/s", periods=60, dataset="standard", rounding=1, history=1):
        url = f"{self.api_base_url}/api/v1/forecast/hourly/"
        params = {
            "location": self.location,
            "lang": self.lang,
            "tz": self.tz,
            "periods": periods,
            "alt": alt,
            "tempunit": tempunit,
            "winduint": winduint,
            "rounding": rounding,
            "dataset": dataset,
            "history": history
        }
        response = self.client.post(url, params=params)
        return response.json()

    def get_forecast_3hourly(self,  alt=None, tempunit="C", winduint="m/s", periods=16, dataset="standard", rounding=1, history=1):
        url = f"{self.api_base_url}/api/v1/forecast/3hourly/"
        params = {
            "location": self.location,
            "lang": self.lang,
            "tz": self.tz,
            "periods": periods,
            "alt": alt,
            "tempunit": tempunit,
            "winduint": winduint,
            "rounding": rounding,
            "dataset": dataset,
            "history": history
        }
        response = self.client.post(url, params=params)
        return response.json()

    def get_forecast_daily(self,  alt=None, tempunit="C", winduint="m/s", periods=7, dataset="standard", rounding=1, history=1):
        url = f"{self.api_base_url}/api/v1/forecast/daily/"
        params = {
            "location": self.location,
            "lang": self.lang,
            "periods": periods,
            "alt": alt,
            "tempunit": tempunit,
            "winduint": winduint,
            "rounding": rounding,
            "dataset": dataset,
            "history": history
        }
        response = self.client.post(url, params=params)
        return response.json()

    def get_air_quality_forecast_hourly(self, periods=24):
        url = f"{self.api_base_url}/api/v1/air-quality/forecast/hourly/"
        params = {
            "location": self.location,
            "lang": self.lang,
            "periods": periods,
            "tz": self.tz
        }
        response = self.client.post(url, params=params)
        return response.json()

    def get_air_quality_forecast_daily(self, periods=24):
        url = f"{self.api_base_url}/api/v1/air-quality/forecast/daily/"
        params = {
            "location": self.location,
            "lang": self.lang,
            "periods": periods,
            "tz": self.tz
        }
        response = self.client.post(url, params=params)
        return response.json()


