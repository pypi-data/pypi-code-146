import random
import string
from typing import List

from sktmls import MLSClient, MLSENV, MLSRuntimeENV, MLSResponse, MLSClientError

MLS_CLIENTS_API_URL = "/api/v1/clients"


class Client:
    """
    MLS 클라이언트 클래스입니다. `Client`는 MLS 연동에 필요한 클라이언트 정보를 가지는 클래스이며 `sktmls.MLSClient`와는 별개의 개념입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) 클라이언트 고유 ID
            - name: (str) 클라이언트 이름
            - apikey: (str) API Key
            - user: (str) 클라이언트 소유 계정명

        ## Returns
        `sktmls.clients.Client`
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.apikey = kwargs.get("apikey")
        self.user = kwargs.get("user")

    def get(self):
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ClientClient(MLSClient):
    """
    MLS 클라이언트 관련 기능들을 제공하는 클라이언트입니다.
    """

    def __init__(
        self,
        env: MLSENV = None,
        runtime_env: MLSRuntimeENV = None,
        username: str = None,
        password: str = None,
    ):
        """
        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.EDD`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)
        - username: (str) MLS 계정명 (기본값: $MLS_USERNAME)
        - password: (str) MLS 계정 비밀번호 (기본값: $MLS_PASSWORD)

        아래의 환경 변수가 정의된 경우 해당 파라미터를 생략 가능합니다.

        - $MLS_ENV: env
        - $MLS_RUNTIME_ENV: runtime_env
        - $MLS_USERNAME: username
        - $MLS_PASSWORD: password

        ## Returns
        `sktmls.clients.ClientClient`

        ## Example

        ```python
        client_client = ClientClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def create_client(self, name: str, apikey: str = None) -> Client:
        """
        클라이언트를 생성합니다.

        ## Args

        - name: (str) 클라이언트 이름
        - apikey: (optional) (str) 길이 40의 API Key. 전달되지 않을 경우 자동 생성

        ## Returns
        `sktmls.clients.Client`

        - id: (int) 클라이언트 고유 ID
        - name: (str) 클라이언트 이름
        - apikey: (str) API Key
        - user: (str) 클라이언트 소유 계정명

        ## Example

        ```python
        client = client_client.create_client(name="my_mls_client")
        ```
        """
        if apikey is not None:
            assert len(apikey) == 40, "apikey의 길이는 반드시 40이어야 합니다."
        else:
            apikey = "".join(random.choices(string.ascii_uppercase + string.digits, k=40))

        data = {"name": name, "apikey": apikey}

        return Client(**self._request(method="POST", url=MLS_CLIENTS_API_URL, data=data).results)

    def list_clients(self, **kwargs) -> List[Client]:
        """
        클라이언트 리스트를 가져옵니다.

        ## Args

        - kwargs: (optional) (dict) 쿼리 조건
            - id: (int) 클라이언트 고유 ID
            - name: (str) 클라이언트 이름
            - query: (str) 검색 문자
            - page: (int) 페이지 번호

        ## Returns
        list(`sktmls.clients.Client`)

        - id: (int) 클라이언트 고유 ID
        - name: (str) 클라이언트 이름
        - apikey: (str) API Key
        - user: (str) 클라이언트 소유 계정명

        ## Example

        ```python
        all_my_clients = client_client.list_clients()
        ```
        """
        response = self._request(method="GET", url=f"{MLS_CLIENTS_API_URL}", params=kwargs).results
        return [Client(**client) for client in response]

    def get_client(self, id: int = None, name: str = None) -> Client:
        """
        클라이언트 정보를 가져옵니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) 클라이언트 고유 ID
        - name: (str) 클라이언트 이름

        ## Returns
        `sktmls.clients.Client`

        - id: (int) 클라이언트 고유 ID
        - name: (str) 클라이언트 이름
        - apikey: (str) API Key
        - user: (str) 클라이언트 소유 계정명

        ## Example

        ```python
        client_by_id = client_client.get_client(id=3)
        client_by_name = client_client.get_client(name="my_client")
        ```
        """
        assert id or name, "`id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        clients = self.list_clients(id=id, name=name)
        if len(clients) != 1:
            raise MLSClientError(code=404, msg="클라이언트가 없거나 여러개 존재합니다.")
        return clients[0]

    def delete_client(self, client: Client) -> MLSResponse:
        """
        클라이언트를 삭제합니다.

        ## Args

        - client: (`sktmls.clients.Client`) 클라이언트 객체

        ## Returns
        `sktmls.MLSResponse`

        ## Example

        ```python
        client_client.delete_client(my_client)
        ```
        """
        assert type(client) == Client

        return self._request(method="DELETE", url=f"{MLS_CLIENTS_API_URL}/{client.id}")
