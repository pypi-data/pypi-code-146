import os
from typing import Any, Dict, List

import aiohttp
import requests

from sktmls import MLSENV, MLSRuntimeENV, MLSResponse
from sktmls.config import Config


class MLSRecommendationAPIClient:
    """
    MLS 추천 API를 호출할 수 있는 클라이언트입니다.

    MMS를 제외한 환경에서는 테스트용 호출로 처리됩니다.

    EDD 환경은 지원하지 않습니다.
    """

    def __init__(
        self,
        env: MLSENV = None,
        runtime_env: MLSRuntimeENV = None,
        client_id: str = None,
        apikey: str = None,
    ):
        """
        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.MMS`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)
        - client_id: (optional) (str) 호출 클라이언트 (`tw`, `twd`, `netcrm` 등)
        - apikey: (optional) (str) 클라이언트의 API Key

        아래의 환경 변수가 정의된 경우 해당 파라미터를 생략 가능합니다.

        - $MLS_ENV: env
        - $AWS_ENV: env
        - $MLS_RUNTIME_ENV: runtime_env

        runtime_env가 `sktmls.MLSRuntimeENV.MMS`인 경우 `client_id`와 `apikey` 파라미터를 생략 가능합니다.

        ## Returns
        `sktmls.apis.MLSRecommendationAPIClient`

        ## Example

        ```python
        recommendation_api_client = MLSRecommendationAPIClient(client_id="tw", apikey="test_apikey",
        env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE)
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

        assert runtime_env != MLSRuntimeENV.EDD, "EDD 환경은 지원하지 않습니다."
        if runtime_env != MLSRuntimeENV.MMS:
            assert client_id and apikey, "`client_id`와 `apikey`가 전달되어야 합니다."
            self.__client_id = client_id
            self.__apikey = apikey
        else:
            self.__client_id = None
            self.__apikey = None

        self.config = Config(self.__runtime_env.value)

    def get_env(self) -> MLSENV:
        return self.__env

    def get_runtime_env(self) -> MLSRuntimeENV:
        return self.__runtime_env

    def request(self, version: str, user_id: str, channel_ids: List[str]) -> Dict[str, Any]:
        """
        MLS 추천 API v1/v2를 호출합니다.

        ## Args

        - version: (str) 호출할 추천 API 버전(`v1`|`v2`)
        - user_id: (str) 해시된 유저 고유 ID (해시된 서비스관리번호)
        - channel_ids: (list(str)) 조회할 채널 ID 리스트

        ## Returns
        dict

        ## Example

        ```python
        rec_dict = recommendation_api_client.request(
            version="v2",
            user_id=hashlib.sha256("1234567890".encode()).hexdigest(),
            channel_ids=["test"]
        )
        ```
        """
        assert version in ["v1", "v2"], "현재 지원하는 버전은 `v1`, `v2`입니다"
        assert channel_ids, "`channel_ids` 리스트가 유효하지 않습니다."

        headers = {"User-Id-Want-Digest": "no"}
        params = {}
        if self.__runtime_env == MLSRuntimeENV.MMS:
            client_id = "mls-mms"
        else:
            client_id = self.__client_id
            headers["apikey"] = self.__apikey
            params["mode"] = "test"

        data = {"user_id": user_id, "channel_ids": channel_ids, "sale_org_id": "admin"}

        response = MLSResponse(
            requests.post(
                url=f"{self.config.MLS_RECOMMENDATION_API_URL[self.__env.value]}/{version}/{client_id}/items",
                headers=headers,
                params=params,
                json=data,
            )
        )
        return response.results

    async def request_async(self, version: str, user_id: str, channel_ids: List[str]) -> Dict[str, Any]:
        """
        MLS 추천 API v1/v2를 비동기 호출합니다.

        ## Args

        - version: (str) 호출할 추천 API 버전(`v1`|`v2`)
        - user_id: (str) 해시된 유저 고유 ID (해시된 서비스관리번호)
        - channel_ids: (list(str)) 조회할 채널 ID 리스트

        ## Returns
        dict

        ## Example

        ```python
        rec_dict = await recommendation_api_client.request_async(
            version="v2",
            user_id=hashlib.sha256("1234567890".encode()).hexdigest(),
            channel_ids=["test"]
        )
        ```
        """
        assert version in ["v1", "v2"], "현재 지원하는 버전은 `v1`, `v2`입니다"
        assert channel_ids, "`channel_ids` 리스트가 유효하지 않습니다."

        headers = {"User-Id-Want-Digest": "no"}
        params = {}
        if self.__runtime_env == MLSRuntimeENV.MMS:
            client_id = "mls-mms"
        else:
            client_id = self.__client_id
            headers["apikey"] = self.__apikey
            params["mode"] = "test"

        data = {"user_id": user_id, "channel_ids": channel_ids, "sale_org_id": "admin"}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{self.config.MLS_RECOMMENDATION_API_URL[self.__env.value]}/{version}/{client_id}/items",
                headers=headers,
                json=data,
                params=params,
            ) as response:
                return MLSResponse(status=response.status, body=await response.json()).results

    def predict(self, api_type: str, target_id: str, channel_ids: List[str], keys: List[Any] = []):
        """
        MLS 추천 API v3를 호출합니다.

        ## Args

        - api_type: (str) 식별자 타입 (`user`|`target`)
        - target_id: (str) 추천 타겟의 고유 식별자
        - channel_ids: (list(str)) 조회할 채널 ID 리스트
        - keys: (optional) (list) 추가 전달할 keys 리스트 (기본값: [])

        ## Returns
        dict

        ## Example

        ```python
        rec_dict = recommendation_api_client.predict(
            api_type="user",
            target_id=hashlib.sha256("1234567890".encode()).hexdigest(),
            channel_ids=["test"],
            keys=[],
        )
        ```
        """
        headers = {}
        params = {}
        if self.__runtime_env == MLSRuntimeENV.MMS:
            client_id = "mls-mms"
        else:
            client_id = self.__client_id
            headers["apikey"] = self.__apikey
            params["mode"] = "test"

        data = {"type": api_type, "id": target_id, "channel_ids": channel_ids, "keys": keys}

        response = MLSResponse(
            requests.post(
                url=f"{self.config.MLS_RECOMMENDATION_API_URL[self.__env.value]}/v3/{client_id}/predict",
                headers=headers,
                params=params,
                json=data,
            )
        )
        return response.results

    async def predict_async(self, api_type: str, target_id: str, channel_ids: List[str], keys: List[Any] = []):
        """
        MLS 추천 API v3를 비동기 호출합니다.

        ## Args

        - api_type: (str) 식별자 타입 (`user`|`target`)
        - target_id: (str) 추천 타겟의 고유 식별자
        - channel_ids: (list(str)) 조회할 채널 ID 리스트
        - keys: (optional) (list) 추가 전달할 keys 리스트 (기본값: [])

        ## Returns
        dict

        ## Example

        ```python
        rec_dict = await recommendation_api_client.predict_async(
            api_type="user",
            target_id=hashlib.sha256("1234567890".encode()).hexdigest(),
            channel_ids=["test"],
            keys=[],
        )
        ```
        """
        headers = {}
        params = {}
        if self.__runtime_env == MLSRuntimeENV.MMS:
            client_id = "mls-mms"
        else:
            client_id = self.__client_id
            headers["apikey"] = self.__apikey
            params["mode"] = "test"

        data = {"type": api_type, "id": target_id, "channel_ids": channel_ids, "keys": keys}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url=f"{self.config.MLS_RECOMMENDATION_API_URL[self.__env.value]}/v3/{client_id}/predict",
                headers=headers,
                json=data,
                params=params,
            ) as response:
                return MLSResponse(status=response.status, body=await response.json()).results
