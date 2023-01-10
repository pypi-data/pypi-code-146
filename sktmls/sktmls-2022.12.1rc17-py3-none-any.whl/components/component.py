from typing import List

from dateutil import parser

from sktmls import MLSClient, MLSENV, MLSRuntimeENV, MLSResponse, MLSClientError

MLS_COMPONENTS_API_URL = "/api/v1/components"


class Component:
    """
    MLS 컴포넌트 클래스입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) 컴포넌트 고유 ID
            - name: (str) 컴포넌트 이름
            - info: (str) 컴포넌트 정보
            - is_latest: (bool) 최신여부
            - user: (str) 컴포넌트 생성 계정명
            - created_at: (datetime) 생성일시
            - updated_at: (datetime) 수정일시

        ## Returns
        `sktmls.components.Component`
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.info = kwargs.get("info")
        self.is_latest = kwargs.get("is_latest")
        self.user = kwargs.get("user")
        if kwargs.get("created_at"):
            self.created_at = parser.parse(kwargs.get("created_at"))
        if kwargs.get("updated_at"):
            self.updated_at = parser.parse(kwargs.get("updated_at"))

    def get(self):
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class ComponentClient(MLSClient):
    """
    MLS 컴포넌트 관련 기능들을 제공하는 클라이언트입니다.
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
        `sktmls.components.ComponentClient`

        ## Example

        ```python
        component_client = ComponentClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """

        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def create_component(self, name: str, info: str, is_latest: bool) -> Component:
        """
        컴포넌트를 생성합니다.

        ## Args

        - name: (str) 컴포넌트 이름
        - info: (str) 컴포넌트 정보
        - is_latest: (bool) 최신여부

        ## Returns
        `sktmls.components.Component`

        - id: (int) 컴포넌트 고유 ID
        - name: (str) 컴포넌트 이름
        - info: (str) 컴포넌트 정보
        - is_latest: (bool) 최신여부
        - user: (str) 컴포넌트 생성 계정명
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        component = component_client.create_component(
            name="my_component",
            info="my_info",
            is_latest=True,
        )
        ```
        """

        data = {"name": name, "info": info, "is_latest": is_latest}

        return Component(**self._request(method="POST", url=MLS_COMPONENTS_API_URL, data=data).results)

    def list_components(self, **kwargs) -> List[Component]:
        """
        컴포넌트 리스트를 가져옵니다.

        ## Args

        - kwargs: (optional) (dict) 컴포넌트 조건
            - id: (int) 컴포넌트 고유 ID
            - name: (str) 컴포넌트 이름
            - is_latest: (bool) 최신여부
            - query: (str) 검색 문자
            - page: (int) 페이지 번호

        ## Returns
        list(`sktmls.components.Component`)

        - id: (int) 컴포넌트 고유 ID
        - name: (str) 컴포넌트 이름
        - info: (str) 컴포넌트 정보
        - is_latest: (bool) 최신여부
        - user: (str) 컴포넌트 생성 계정명
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        components = component_client.list_components()
        ```
        """

        response = self._request(method="GET", url=f"{MLS_COMPONENTS_API_URL}", params=kwargs).results

        return [Component(**component) for component in response]

    def get_component(self, id: int = None, name: str = None, info: str = None, is_latest: bool = True) -> Component:
        """
        컴포넌트 정보를 가져옵니다. 여러개가 존재하는 경우 `is_latest`가 True인 최신의 컴포넌트를 반환합니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (optional) (int) 컴포넌트 고유 ID
        - name: (optional) (str) 컴포넌트 이름
        - is_latest: (optional) (bool) 최신여부 (기본값 : `True`)

        ## Returns
        `sktmls.components.Component`

        - id: (int) 컴포넌트 고유 ID
        - name: (str) 컴포넌트 이름
        - info: (str) 컴포넌트 정보
        - is_latest: (bool) 최신여부
        - user: (str) 컴포넌트 생성 계정명
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        component_by_id = component_client.get_component(
            id=3
        )
        component_by_name = component_client.get_component(
            name="my_component",
            is_latest=True
        )
        ```
        """
        assert id or name or info, "`id` 또는 `name` 또는 `info` 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        components = self.list_components(id=id, name=name, info=info, is_latest=is_latest)
        if len(components) == 0:
            raise MLSClientError(code=404, msg="컴포넌트가 없습니다.")
        elif len(components) > 1:
            raise MLSClientError(code=409, msg="컴포넌트가 여러개 존재합니다.")

        return Component(**self._request(method="GET", url=f"{MLS_COMPONENTS_API_URL}/{components[0].id}").results)

    def update_component(self, component: Component, is_latest: bool) -> Component:
        """
        컴포넌트 정보 중 `is_latest`를 수정합니다.

        ## Args

        - component: (`sktmls.components.Component`) 컴포넌트 객체
        - is_latest: (bool) 최신여부

        ## Returns
        `sktmls.components.Component`

        - id: (int) 컴포넌트 고유 ID
        - name: (str) 컴포넌트 이름
        - info: (str) 컴포넌트 정보
        - is_latest: (bool) 최신여부
        - user: (str) 컴포넌트 생성 계정명
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        component = component_client.get_component(name="hello")
        component = component_client.update_component(
            component=component,
            is_latest=True,
        )
        ```
        """
        assert type(component) == Component

        data = {
            "name": component.get().get("name"),
            "info": component.get().get("info"),
            "is_latest": is_latest,
        }

        component.reset(
            **self._request(method="PUT", url=f"{MLS_COMPONENTS_API_URL}/{component.id}", data=data).results
        )
        return component

    def delete_component(self, component: Component) -> MLSResponse:
        """
        컴포넌트 삭제합니다.

        ## Args

        - component: (`sktmls.components.Component`) 컴포넌트 객체

        ## Returns
        `sktmls.MLSResponse`

        ## Example

        ```python
        component_client.delete_component(component)
        ```
        """

        assert type(component) == Component

        return self._request(method="DELETE", url=f"{MLS_COMPONENTS_API_URL}/{component.id}")
