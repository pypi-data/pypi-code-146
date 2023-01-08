from typing import Any, Union
import base64
import json

import requests
from requests import Response
from bs4 import BeautifulSoup
from Crypto.PublicKey.RSA import import_key
from Crypto.Cipher import PKCS1_OAEP
from pydpn._utils.api_service import ApiService
from pydpn._api import *


class DeeperNetwork:
    def __init__(
        self,
        username,
        password,
        hostIp: str = "http://34.34.34.34",
        proxy: Union[str, dict] = "",
    ) -> None:

        self.username: str = username
        self.password: str = password
        self.hostIp: str = hostIp

        # check for proxy settings
        if proxy:
            # convert to requests proxy schema
            if isinstance(proxy, str):
                self.proxy: dict = {
                    "http": f"http://{proxy}",
                    "https": f"https://{proxy}",
                }
            elif isinstance(self.proxy, dict):
                self.proxy: dict = proxy
        else:
            self.proxy: dict = None

        self.login()
        self.lastPostResp = {}

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.logout()

    def login(self, username: str = "", password: str = "") -> bool:
        """login to deeper device

        Args:
            username (str, optional): username. Defaults to "".
            password (str, optional): password. Defaults to "".

        Raises:
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: login success
        """

        # option for changing username and password after init
        if username:
            self.username = username

        if password:
            self.password = password

        # create requests session
        self.session = requests.Session()
        self.session.proxies.update(self.proxy)

        # load a public key from deeper device
        pubKey = self._load_public_key()
        if pubKey is None:
            raise ValueError("No Public Key found in js scrips provided by host")

        # encrypt the passwort with public key
        encPassword = PKCS1_OAEP.new(import_key(pubKey, passphrase=None)).encrypt(
            bytes(self.password, encoding="UTF-8")
        )
        data = {
            "username": self.username,
            "password": base64.b64encode(encPassword).decode("utf-8"),
        }
        url = f"{self.hostIp}/api/admin/login"

        # send login with post request to host
        # self.session = requests.Session()
        resp = self.session.post(url, data=data, proxies=self.proxy)

        # analyse host response
        if "application/json" in resp.headers["Content-Type"]:
            respData = json.loads(resp.text)
            respDataKeys = respData.keys()
            if "success" in respDataKeys:
                if respData["success"]:
                    if "token" in respDataKeys:
                        self.loginToken = respData["token"]
                        self.session.headers.update(
                            {"Authorization": respData["token"]}
                        )
                        return True

                    else:
                        raise ValueError("Token not transfered from host")

            elif "wrongPassword" in respDataKeys:
                raise ValueError("Password incorrect")

            elif "wrongUsername" in respDataKeys:
                raise ValueError("Username incorrect")

    def logout(self):
        url = f"{self.hostIp}/system?sessionError=sessionTimeout"
        self.session.headers.update({"Connection": "close"})
        resp = self.session.get(url)
        resp.close()

    @property
    def sharing_config(self):
        return SharingConfig(self)

    @property
    def dashboard(self):
        return Dashboard(self)

    @property
    def system(self):
        return System(self)

    @property
    def mode(self):
        return Mode(self)

    @property
    def tunnel(self):
        return Tunnel(self)

    @property
    def routing(self):
        return Routing(self)

    def reset(self):

        self.__init__(self.username, self.password)

    def quit(self):
        print("close")

    def _load_public_key(self) -> str:
        """method is loading all java script files provided by host
           and is searching for a public key (RSA)

        Returns:
            str: public key
        """

        soup = BeautifulSoup(self.session.get(self.hostIp).text, features="lxml")
        beginPublicKey = "-----BEGIN PUBLIC KEY-----"
        endPublicKey = "-----END PUBLIC KEY-----"
        for script in soup.find_all("script"):
            if script.attrs:
                if "src" in script.attrs.keys():
                    jsUrl = self.hostIp + script.attrs["src"]
                    resp = self.session.get(jsUrl, proxies=self.proxy)
                    if all(
                        [
                            beginPublicKey in resp.text,
                            endPublicKey in resp.text,
                        ]
                    ):
                        pubKeyText = resp.text.split(beginPublicKey)[1].split(
                            endPublicKey
                        )[0]
                        return (
                            beginPublicKey
                            + pubKeyText.replace("\\n", "\n")
                            + endPublicKey
                        )

    def _api_get(self, refUrl: str, apiRoute: str) -> Response:
        self.session.headers.update({"Referer": refUrl})
        url = f"{self.hostIp}/api/{apiRoute}"
        return self.session.get(url)

    def _api_post(self, refUrl: str, apiRoute: str, data) -> Response:
        self.session.headers.update({"Referer": refUrl})
        url = f"{self.hostIp}/api/{apiRoute}"
        resp = self.session.post(url, json=data)
        return resp

    def _api_call(self, service: dict) -> Any:

        service = ApiService(**service)
        if service.requestMethod == "GET":
            resp = self._api_get(service.refUrl, service.apiRoute)

        elif service.requestMethod == "POST":
            resp = self._api_post(service.refUrl, service.apiRoute, service.postData)

        if resp.status_code == 200:
            # if service.setValue:
            #     return json.loads(resp.text)
            # else:
            data = json.loads(resp.text)

            if service.responseType is dict:
                for key in data:
                    data[key] = service.responseContent[key](data[key])
                    if service.returnType in [int, float, str]:
                        return data[key]

                if service.returnType not in [
                    dict,
                    list,
                    float,
                    int,
                    str,
                    bool,
                ]:
                    resp = service.returnType()
                    for key in data:
                        setattr(resp, key, data[key])

                    return resp

                if service.returnType is bool:
                    for key in data:
                        return bool(data[key])

            if service.responseType is dict:
                for key in service.responseContent:
                    if key in data:

                        retVal = data[key]

                    else:
                        retVal = None

                    if key in service.responseAlias:
                        # setattr(self, service.responseAlias[key], retVal)
                        pass
                    else:
                        setattr(self, key, retVal)

                    retData = {}
                    for key in service.responseAlias:
                        retData.update({})

            elif service.responseType is list:
                if service.returnType not in [dict, list, float, int, str]:
                    resp = service.returnType()
                    for el, desc in zip(data, service.responseContent):
                        setattr(resp, desc[0], desc[1](el))

                    return resp

        return data
