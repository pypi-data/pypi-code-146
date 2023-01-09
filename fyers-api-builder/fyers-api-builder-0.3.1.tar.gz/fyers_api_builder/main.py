import os
from datetime import datetime
from urllib.parse import parse_qs, urlparse

import requests

from fyers_api_builder.libs.get_history_data import GetHistoryData
from fyers_api_builder.libs.get_live_data import GetLiveData

current_directory = os.path.dirname(os.path.realpath(__file__))

data_path = os.path.join(current_directory, "data")
data_file = datetime.now().strftime("%Y-%m-%d")
fyers_access_token_path = os.path.join(data_path, data_file)

log_path = os.path.join(current_directory, "logs")


class FyersApiConfig:
    def __init__(self, config):
        self.username = config["username"]
        self.password = config["password"]
        self.pin = config["pin"]
        self.client_id = config["client_id"]
        self.secret_key = config["secret_key"]
        self.redirect_uri = config["redirect_uri"]


class FyersApiBuilder:
    def __init__(self, config, accessToken, fyersModel, ws):
        self.__set_config(config)
        self.__set_fyers_api(accessToken, fyersModel, ws)
        self.__generate_folders_if_not_exists()
        self.__initialize()

    def __set_config(self, config):
        self.__config = FyersApiConfig(config)

    def __set_fyers_api(self, accessToken, fyersModel, ws):
        self.__accessToken = accessToken
        self.__fyersModel = fyersModel
        self.__ws = ws

    def __generate_folders_if_not_exists(self):
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        if not os.path.exists(log_path):
            os.makedirs(log_path)

    def __set_initial_values(self, token):
        self.access_token = token
        self.client = self.__fyersModel.FyersModel(
            client_id=self.__config.client_id, token=token, log_path=log_path
        )

        self.ws_access_token = f"{self.__config.client_id}:{self.access_token}"
        self.ws_client = self.__ws.FyersSocket(
            access_token=self.ws_access_token, run_background=False, log_path=log_path
        )

    def subscribe(self, symbol=None, data_type=None, custom_message=None):
        self.ws_client.websocket_data = custom_message
        self.ws_client.subscribe(symbol=symbol, data_type=data_type)
        self.ws_client.keep_running()

    def unsubscribe(self, symbol=None):
        self.ws_client.unsubscribe(symbol=symbol)

    def get_history_data(
        self,
        symbol=None,
        resolution="1",
        fetch_from_epoch=None,
        fetch_to_epoch=None,
    ):
        getHistoryData = GetHistoryData(
            self.client, symbol, resolution, fetch_from_epoch, fetch_to_epoch
        )

        return getHistoryData.run()

    def get_live_data(
        self,
        symbol=None,
        resolution="1",
        fetch_from_epoch=None,
        fetch_to_epoch=None,
    ):
        getLiveData = GetLiveData(
            self.client, symbol, resolution, fetch_from_epoch, fetch_to_epoch
        )

        return getLiveData.run()

    def __initialize(self):
        try:
            token = self.__read_file()
            self.__set_initial_values(token)
        except FileNotFoundError:
            token = self.__setup()
            self.__set_initial_values(token)

    def __read_file(self):
        with open(f"{fyers_access_token_path}", "r") as f:
            token = f.read()
        return token

    def __write_file(self, token):
        with open(f"{fyers_access_token_path}", "w") as f:
            f.write(token)

    def __setup(self):
        s = requests.Session()

        data1 = f'{{"fy_id":"{self.__config.username}","password":"{self.__config.password}","app_id":"2","imei":"","recaptcha_token":""}}'
        r1 = s.post("https://api.fyers.in/vagator/v1/login", data=data1)
        assert r1.status_code == 200, f"Error in r1:\n {r1.json()}"

        request_key = r1.json()["request_key"]
        data2 = f'{{"request_key":"{request_key}","identity_type":"pin","identifier":"{self.__config.pin}","recaptcha_token":""}}'
        r2 = s.post("https://api.fyers.in/vagator/v1/verify_pin", data=data2)
        assert r2.status_code == 200, f"Error in r2:\n {r2.json()}"

        headers = {
            "authorization": f"Bearer {r2.json()['data']['access_token']}",
            "content-type": "application/json; charset=UTF-8",
        }
        data3 = f'{{"fyers_id":"{self.__config.username}","app_id":"{self.__config.client_id[:-4]}","redirect_uri":"{self.__config.redirect_uri}","appType":"100","code_challenge":"","state":"abcdefg","scope":"","nonce":"","response_type":"code","create_cookie":true}}'
        r3 = s.post("https://api.fyers.in/api/v2/token", headers=headers, data=data3)
        assert r3.status_code == 308, f"Error in r3:\n {r3.json()}"

        parsed = urlparse(r3.json()["Url"])
        auth_code = parse_qs(parsed.query)["auth_code"][0]

        session = self.__accessToken.SessionModel(
            client_id=self.__config.client_id,
            secret_key=self.__config.secret_key,
            redirect_uri=self.__config.redirect_uri,
            response_type="code",
            grant_type="authorization_code",
        )
        session.set_token(auth_code)
        response = session.generate_token()
        token = response["access_token"]
        self.__write_file(token)

        return token
