import os
from typing import Any, Dict, List

import aiohttp
import requests

from sktmls import MLSENV, MLSRuntimeENV, MLSResponse
from sktmls.config import Config


class MLSProfileAPIClient:
    """
    MLS 프로파일 API를 호출할 수 있는 클라이언트입니다.

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
        `sktmls.apis.MLSProfileAPIClient`

        ## Example

        ```python
        profile_api_client = MLSProfileAPIClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE)
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

    def get_user_profile(self, profile_id: str, user_id: str, keys: List[str] = None) -> Dict[str, Any]:
        """
        MLS User Profile API를 호출합니다.

        ## Args

        - profile_id: (str) 호출할 프로파일 ID
        - user_id: (str) 해시된 유저 고유 ID (해시된 서비스관리번호)
        - keys: (optional) (list(str)) 조회할 키 리스트 (기본값: None, 기본값 전달시 모든 키 조회)

        ## Returns
        dict

        ## Example

        ```python
        user_profile_dict = profile_api_client.get_user_profile(
            profile_id="default",
            user_id=hashlib.sha256("1234567890".encode()).hexdigest(),
            keys=["age", "gender"]
        )
        ```
        """
        return self._get_profile(api_type="user", profile_id=profile_id, target_id=user_id, keys=keys)

    async def get_user_profile_async(self, profile_id: str, user_id: str, keys: List[str] = None) -> Dict[str, Any]:
        """
        MLS User Profile API를 비동기로 호출합니다.

        ## Args

        - profile_id: (str) 호출할 프로파일 ID
        - user_id: (str) 해시된 유저 고유 ID (해시된 서비스관리번호)
        - keys: (optional) (list(str)) 조회할 키 리스트 (기본값: None, 기본값 전달시 모든 키 조회)

        ## Returns
        dict

        ## Example

        ```python
        user_profile_dict = await profile_api_client.get_user_profile_async(
            profile_id="default",
            user_id=hashlib.sha256("1234567890".encode()).hexdigest(),
            keys=["age", "gender"]
        )
        ```
        """
        return await self._get_profile_async(api_type="user", profile_id=profile_id, target_id=user_id, keys=keys)

    def get_item_profile(self, profile_id: str, item_id: str, keys: List[str] = None) -> Dict[str, Any]:
        """
        MLS Item Profile API를 호출합니다.

        ## Args

        - profile_id: (str) 호출할 프로파일 ID
        - item_id: (str) 아이템 고유 ID
        - keys: (optional) (list(str)) 조회할 키 리스트 (기본값: None, 기본값 전달시 모든 키 조회)

        ## Returns
        dict

        ## Example

        ```python
        item_profile_dict = profile_api_client.get_item_profile(
            profile_id="device",
            item_id="item001",
            keys=["price", "resolution"]
        )
        ```
        """

        return self._get_profile(api_type="item", profile_id=profile_id, target_id=item_id, keys=keys)

    async def get_item_profile_async(self, profile_id: str, item_id: str, keys: List[str] = None) -> Dict[str, Any]:
        """
        MLS Item Profile API를 비동기로 호출합니다.

        ## Args

        - profile_id: (str) 호출할 프로파일 ID
        - item_id: (str) 아이템 고유 ID
        - keys: (optional) (list(str)) 조회할 키 리스트 (기본값: None, 기본값 전달시 모든 키 조회)

        ## Returns
        dict

        ## Example

        ```python
        item_profile_dict = await profile_api_client.get_item_profile_async(
            profile_id="device",
            item_id="item001",
            keys=["price", "resolution"]
        )
        ```
        """

        return await self._get_profile_async(api_type="item", profile_id=profile_id, target_id=item_id, keys=keys)

    def get_profile(self, profile_id: str, id: str, keys: List[str] = None) -> Dict[str, Any]:
        """
        MLS 통합 Profile API를 호출합니다.

        ## Args

        - profile_id: (str) 호출할 프로파일 ID
        - id: (str) 조회할 ID

        ## Returns
        dict

        ## Example

        ```python
        profile_dict = profile_api_client.get_profile(
            profile_id="default",
            target_id="001",
            keys=["age", "gender"]
        )
        ```
        """
        headers = {}
        params = {"id": id}
        if keys is not None:
            assert isinstance(keys, list), "`keys` 리스트가 유효하지 않습니다."
            params["f"] = keys

        if self.__runtime_env == MLSRuntimeENV.MMS:
            client_id = "mls-mms"
        else:
            client_id = self.__client_id
            headers["apikey"] = self.__apikey
            params["mode"] = "test"

        response = MLSResponse(
            requests.get(
                url=f"{self.config.MLS_PROFILE_API_URL[self.__env.value]}/v1/{client_id}/profiles/{profile_id}",
                headers=headers,
                params=params,
            )
        )
        return response.results

    async def get_profile_async(self, profile_id: str, id: str, keys: List[str] = None) -> Dict[str, Any]:
        """
        MLS 통합 Profile API를 비동기로 호출합니다.

        ## Args

        - profile_id: (str) 호출할 프로파일 ID
        - id: (str) 조회할 ID

        ## Returns
        dict

        ## Example

        ```python
        profile_dict = await profile_api_client.get_profile_async(
            profile_id="default",
            target_id="001",
            keys=["age", "gender"]
        )
        ```
        """
        headers = {}
        params = {"id": id}
        if keys is not None:
            assert isinstance(keys, list), "`keys` 리스트가 유효하지 않습니다."
            params["f"] = keys

        if self.__runtime_env == MLSRuntimeENV.MMS:
            client_id = "mls-mms"
        else:
            client_id = self.__client_id
            headers["apikey"] = self.__apikey
            params["mode"] = "test"

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=f"{self.config.MLS_PROFILE_API_URL[self.__env.value]}/v1/{client_id}/profiles/{profile_id}",
                headers=headers,
                params=params,
            ) as response:
                return MLSResponse(status=response.status, body=await response.json()).results

    def _get_profile(self, api_type: str, profile_id: str, target_id: str, keys: List[str] = None) -> Dict[str, Any]:
        params = {}
        headers = {}
        if keys is not None:
            assert isinstance(keys, list), "`keys` 리스트가 유효하지 않습니다."
            params["f"] = keys

        if self.__runtime_env == MLSRuntimeENV.MMS:
            client_id = "mls-mms"
        else:
            client_id = self.__client_id
            headers["apikey"] = self.__apikey
            params["mode"] = "test"

        api_type += "s"
        response = MLSResponse(
            requests.get(
                url=f"{self.config.MLS_PROFILE_API_URL[self.__env.value]}/v1/{client_id}/profiles/{profile_id}/{api_type}/{target_id}",
                headers=headers,
                params=params,
            )
        )
        return response.results

    async def _get_profile_async(
        self, api_type: str, profile_id: str, target_id: str, keys: List[str] = None
    ) -> Dict[str, Any]:
        params = {}
        headers = {}
        if keys is not None:
            assert isinstance(keys, list), "`keys` 리스트가 유효하지 않습니다."
            params["f"] = keys

        if self.__runtime_env == MLSRuntimeENV.MMS:
            client_id = "mls-mms"
        else:
            client_id = self.__client_id
            headers["apikey"] = self.__apikey
            params["mode"] = "test"

        api_type += "s"
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=f"{self.config.MLS_PROFILE_API_URL[self.__env.value]}/v1/{client_id}/profiles/{profile_id}/{api_type}/{target_id}",
                headers=headers,
                params=params,
            ) as response:
                return MLSResponse(status=response.status, body=await response.json()).results
