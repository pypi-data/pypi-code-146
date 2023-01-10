import os
from typing import Any, Dict

import aiohttp
import requests

from sktmls import MLSENV, MLSRuntimeENV
from sktmls.config import Config


class MLSConversionTrackingAPIClient:
    """
    MLS Conversion Tracking API를 호출할 수 있는 클라이언트입니다.

    모든 호출은 테스트용 호출로 처리됩니다.

    MMS, EDD 환경은 지원하지 않습니다.
    """

    def __init__(
        self,
        client_id: str,
        apikey: str,
        env: MLSENV = None,
        runtime_env: MLSRuntimeENV = None,
    ):
        """
        ## Args

        - client_id: (str) 호출 클라이언트 (`tw`, `twd`, `netcrm` 등)
        - apikey: (str) 클라이언트의 API Key
        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)

        아래의 환경 변수가 정의된 경우 해당 파라미터를 생략 가능합니다.

        - $MLS_ENV: env
        - $AWS_ENV: env
        - $MLS_RUNTIME_ENV: runtime_env

        ## Returns
        `sktmls.apis.MLSConversionTrackingAPIClient`

        ## Example

        ```python
        conversion_tracking_api_client = MLSConversionTrackingAPIClient(client_id="tw", apikey="test_apikey", env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE)
        ```
        """
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

        assert runtime_env not in [MLSRuntimeENV.EDD, MLSRuntimeENV.MMS], "EDD, MMS 환경은 지원하지 않습니다."
        assert client_id and apikey, "`client_id`와 `apikey`가 전달되어야 합니다."
        self.__client_id = client_id
        self.__apikey = apikey

        self.config = Config(self.__runtime_env.value)

    def get_env(self) -> MLSENV:
        return self.__env

    def get_runtime_env(self) -> MLSRuntimeENV:
        return self.__runtime_env

    def request(
        self, user_id: str, channel_id: str, conversion_type: str, process_id: str, item_id: str
    ) -> Dict[str, Any]:
        """
        MLS Conversion Tracking API를 호출합니다.

        ## Args

        - user_id: (str) 추천 요청의 user ID (해시된 서비스관리번호)
        - channel_id: (str) 추천 요청 또는 응답의 channel ID
        - conversion_type: (str) 이벤트 타입(`impression`|`click`|`detail_view`|`like`|`dislike`)
        - process_id: (str) 추천 결과 응답의 process ID
        - item_id : (str) 추천 결과 응답의 item_id

        ## Returns
        dict

        ## Example

        ```python
        conversion_tracking_dict = conversion_tracking_api_client.request(
            user_id=hashlib.sha256("1234567890".encode()).hexdigest(),
            channel_id="sample_channel",
            conversion_type="impression",
            process_id="sample_process",
            item_id="sample_item",
        )
        ```
        """

        client_id = self.__client_id
        headers = {"apikey": self.__apikey, "User-Id-Want-Digest": "no"}
        params = {"mode": "test"}
        data = {
            "user_id": user_id,
            "channel_id": channel_id,
            "process_id": process_id,
            "item_id": item_id,
        }
        response = requests.post(
            url=f"{self.config.MLS_CONVERSION_TRACKING_API_URL[self.__env.value]}/v1/{client_id}/{conversion_type}",
            headers=headers,
            params=params,
            json=data,
        )

        return response.content.decode("utf-8")

    async def request_async(
        self, user_id: str, channel_id: str, conversion_type: str, process_id: str, item_id: str
    ) -> Dict[str, Any]:
        """
        MLS Conversion Tracking API를 비동기 호출합니다.

        ## Args

        - user_id: (str) 추천 요청의 user ID (해시된 서비스관리번호)
        - channel_id: (str) 추천 요청 또는 응답의 channel ID
        - conversion_type: (str) 이벤트 타입(`impression`|`click`|`detail_view`|`like`|`dislike`)
        - process_id: (str) 추천 결과 응답의 process ID
        - item_id : (str) 추천 결과 응답의 item_id

        ## Returns
        dict

        ## Example

        ```python
        conversion_tracking_dict = await conversion_tracking_api_client.request_async(
            user_id=hashlib.sha256("1234567890".encode()).hexdigest(),
            channel_id="sample_channel",
            conversion_type="impression",
            process_id="sample_process",
            item_id="sample_item",
        )
        ```
        """

        client_id = self.__client_id
        headers = {"apikey": self.__apikey, "User-Id-Want-Digest": "no"}
        params = {"mode": "test"}
        data = {
            "user_id": user_id,
            "channel_id": channel_id,
            "process_id": process_id,
            "item_id": item_id,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{self.config.MLS_CONVERSION_TRACKING_API_URL[self.__env.value]}/v1/{client_id}/{conversion_type}",
                headers=headers,
                params=params,
                json=data,
            ) as response:
                return await response.json()
