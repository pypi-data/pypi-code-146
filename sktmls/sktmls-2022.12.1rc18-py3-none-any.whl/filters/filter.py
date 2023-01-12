from typing import List, Dict

from dateutil import parser

from sktmls import MLSClient, MLSENV, MLSRuntimeENV, MLSResponse, MLSClientError

MLS_FILTERS_API_URL = "/api/v1/filters"


class Filter:
    """
    MLS 필터 클래스입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) 필터 고유 ID
            - name: (str) 필터 이름
            - conditions: (list(dict)) 필터 조건 리스트
            - created_at: (datetime) 생성일시
            - updated_at: (datetime) 수정일시

        ## Returns
        `sktmls.filters.Filter`
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")

        if kwargs.get("body"):
            self.conditions = kwargs.get("body", {}).get("conditions", None)
        elif kwargs.get("conditions"):
            self.conditions = kwargs.get("conditions", None)

        if kwargs.get("created_at"):
            self.created_at = parser.parse(kwargs.get("created_at"))
        if kwargs.get("updated_at"):
            self.updated_at = parser.parse(kwargs.get("updated_at"))

    def get(self):
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            if k == "body":
                setattr(self, "conditions", v.get("conditions", None))
            else:
                setattr(self, k, v)


class FilterClient(MLSClient):
    """
    MLS 필터 관련 기능들을 제공하는 클라이언트입니다.
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
        `sktmls.filters.FilterClient`

        ## Example

        ```python
        filter_client = FilterClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """

        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def create_filter(self, name: str, conditions: List[Dict]) -> Filter:
        """
        필터를 생성합니다.

        ## Args

        - name: (str) 필터 이름
        - conditions: (list(dict)) 필터 조건 리스트
            - key: 프로파일 키
            - operator: 연산자 (`==`|`!=`|`<=`|`>=`|`<`|`>`|`contains`)
            - value: 비교할 값

        ## Returns
        `sktmls.filters.Filter`

        - id: (int) 필터 고유 ID
        - name: (str) 필터 이름
        - conditions: (list(dict)) 필터 조건 리스트
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        filter = filter_client.create_filter(
            name="hello",
            conditions=[
                {"key": "age", "operator": "<", "value": "19"},
                {"key": "gender", "operator": "==", "value": "F"},
            ]
        )
        ```
        """

        data = {
            "name": name,
            "body": {"conditions": conditions},
        }

        return Filter(**self._request(method="POST", url=MLS_FILTERS_API_URL, data=data).results)

    def list_filters(self, **kwargs) -> List[Filter]:
        """
        필터 리스트를 가져옵니다. (필터 조건 제외)

        ## Args

        - kwargs: (optional) (dict) 쿼리 조건
            - id: (int) 필터 고유 ID
            - name: (str) 필터 이름
            - query: (str) 검색 문자
            - page: (int) 페이지 번호

        ## Returns
        list(`sktmls.filters.Filter`)

        - id: (int) 필터 고유 ID
        - name: (str) 필터 이름
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        filters = filter_client.list_filters()
        ```
        """

        response = self._request(method="GET", url=f"{MLS_FILTERS_API_URL}", params=kwargs).results

        return [Filter(**filter) for filter in response]

    def get_filter(self, type: str = None, id: int = None, name: str = None) -> Filter:
        """
        필터 정보를 가져옵니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (optional) (int) 필터 고유 ID
        - name: (optional) (str) 필터 이름

        ## Returns
        `sktmls.filters.Filter`

        - id: (int) 필터 고유 ID
        - name: (str) 필터 이름
        - conditions: (list(dict)) 필터 조건 리스트
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        filter_by_id = filter_client.get_filter(id=3)
        filter_by_name = filter_client.get_filter(name="hello")
        ```
        """
        assert id or name, "`id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        filters = self.list_filters(type=type, id=id, name=name)
        if len(filters) == 0:
            raise MLSClientError(code=404, msg="필터가 없습니다.")
        elif len(filters) > 1:
            raise MLSClientError(code=409, msg="필터가 여러개 존재합니다.")
        return Filter(**self._request(method="GET", url=f"{MLS_FILTERS_API_URL}/{filters[0].id}").results)

    def update_filter(self, filter: Filter, name: str = None, conditions: List[Dict] = None) -> Filter:
        """
        필터 정보를 수정합니다.

        ## Args

        - filter: (`sktmls.filters.Filter`) 필터 객체
        - name: (str) 필터 이름
        - conditions: (list(dict)) 필터 조건 리스트
            - key: 프로파일 키
            - operator: 연산자 (`==`|`!=`|`<=`|`>=`|`<`|`>`|`contains`)
            - value: 비교할 값

        ## Returns
        `sktmls.filters.Filter`

        - id: (int) 필터 고유 ID
        - name: (str) 필터 이름
        - conditions: (list(dict)) 필터 조건 리스트
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        filter = filter_clinet.get_filter(name="hello")
        filter = filter_client.update_filter(
            filter=filter,
            name="bye",
            conditions=[
                {"key": "age", "operator": "<", "value": "50"},,
                {"key": "gender", "operator": "==", "value": "M"},
            ]
        )
        ```
        """
        assert type(filter) == Filter

        data = {"name": filter.get().get("name"), "body": {"conditions": filter.get().get("conditions")}}
        if name:
            data["name"] = name
        if conditions:
            data["body"] = {"conditions": conditions}

        filter.reset(**self._request(method="PUT", url=f"{MLS_FILTERS_API_URL}/{filter.id}", data=data).results)
        return filter

    def delete_filter(self, filter: Filter) -> MLSResponse:
        """
        필터 삭제합니다.

        ## Args

        - filter: (`sktmls.filters.Filter`) 필터 객체

        ## Returns
        `sktmls.MLSResponse`

        ## Example

        ```python
        filter_client.delete_filter(filter)
        ```
        """

        assert type(filter) == Filter

        return self._request(method="DELETE", url=f"{MLS_FILTERS_API_URL}/{filter.id}")
