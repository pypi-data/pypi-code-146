import aiohttp
import base64
import json
import os
import requests
from typing import Any, Dict

from sktmls import MLSENV, MLSRuntimeENV
from sktmls.config import Config


class MLSClientError(Exception):
    def __init__(self, code: int, msg: str):
        super().__init__(msg)
        self.code = code
        self.msg = msg


class DoesNotExist(MLSClientError):
    def __init__(self, msg="결과가 존재하지 않습니다"):
        super().__init__(404, msg)


class MLSResponse:
    def __init__(self, response: requests.models.Response = None, status: int = None, body: Dict[str, Any] = None):
        if response is not None and status is None and body is None:
            data = json.loads(response.content.decode("utf-8"))
            self.status = response.status_code
        else:
            data = body
            self.status = status
        self.code = data.get("code")
        self.error = data.get("error")
        self.results = data.get("results")

        if self.error:
            raise MLSClientError(code=self.code, msg=self.error)


class MLSClient:
    def __init__(
        self,
        env: MLSENV = None,
        runtime_env: MLSRuntimeENV.LOCAL = None,
        username: str = None,
        password: str = None,
    ):
        if env:
            assert env in MLSENV.list_items(), "유효하지 않은 MLS 환경입니다."
            self.__env = env
        elif os.environ.get("MLS_ENV"):
            self.__env = MLSENV[os.environ["MLS_ENV"]]
        elif os.environ.get("AWS_ENV"):
            self.__env = MLSENV[os.environ["AWS_ENV"]]
        else:
            self.__env = MLSENV.STG

        if runtime_env:
            assert runtime_env in MLSRuntimeENV.list_items(), "유효하지 않은 런타임 환경입니다."
            self.__runtime_env = runtime_env
        elif os.environ.get("MLS_RUNTINE_ENV"):
            self.__runtime_env = MLSRuntimeENV[os.environ["MLS_RUNTINE_ENV"]]
        else:
            __HOSTNAME = os.environ.get("HOSTNAME", "").lower()
            if __HOSTNAME.startswith("bdp-dmi"):
                self.__runtime_env = MLSRuntimeENV.YE
            elif __HOSTNAME.startswith("vm-skt"):
                self.__runtime_env = MLSRuntimeENV.EDD
            else:
                self.__runtime_env = MLSRuntimeENV.LOCAL

        self.config = Config(self.__runtime_env.value)

        if runtime_env != MLSRuntimeENV.MMS:
            if username:
                assert type(username) == str, "`username`의 타입이 str이 아닙니다."
                self.__username = username
            elif os.environ.get("MLS_USERNAME"):
                self.__username = os.environ["MLS_USERNAME"]
            else:
                raise MLSClientError(code=400, msg="`username`이 전달되지 않았습니다. 파라미터 또는 $MLS_USERNAME 환경 변수를 확인해주세요.")

            if password:
                assert type(password) == str, "`password`의 타입이 str이 아닙니다."
                self.__password = password
            elif os.environ.get("MLS_PASSWORD"):
                self.__password = os.environ["MLS_PASSWORD"]
            else:
                raise MLSClientError(code=400, msg="`password`가 전달되지 않았습니다. 파라미터 또는 $MLS_PASSWORD 환경 변수를 확인해주세요.")

            self.__api_token = base64.b64encode(f"{self.__username}:{self.__password}".encode()).decode("utf-8")
        else:
            self.__api_token = "None"

    def get_env(self) -> MLSENV:
        return self.__env

    def get_runtime_env(self) -> MLSRuntimeENV:
        return self.__runtime_env

    def get_username(self) -> str:
        return self.__username

    def _request(self, method: str, url: str, data: Any = None, params=None) -> MLSResponse:
        response = requests.request(
            method=method,
            url=f"{self.config.MLS_AB_API_URL[self.__env.value]}{'' if url.startswith('/') else '/'}{url}",
            headers={"Authorization": f"Basic {self.__api_token}"},
            json=data,
            params=params,
        )

        return MLSResponse(response)

    async def _request_async(self, method: str, url: str, data: Any = None, params=None) -> MLSResponse:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=f"{self.config.MLS_AB_API_URL[self.__env.value]}{'' if url.startswith('/') else '/'}{url}",
                headers={"Authorization": f"Basic {self.__api_token}"},
                json=data,
                params=params,
            ) as response:
                return MLSResponse(status=response.status, body=await response.json())
