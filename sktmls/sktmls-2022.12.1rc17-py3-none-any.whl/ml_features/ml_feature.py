from dateutil import parser
from enum import Enum
from typing import List

from sktmls import MLSClient, MLSENV, MLSRuntimeENV, DoesNotExist


class MLFeature:
    class Type(Enum):
        """
        AutoML 피쳐 타입입니다.

        - CATEGORY: 카테고리형
        - NUMBER: 수치형
        """

        CATEGORY = "category"
        NUMBER = "number"

    class Status(Enum):
        """
        AutoML 피쳐 상태입니다.

        - CREATED: 생성됨
        - IN_SERVICE: 서비스 중
        - DEPRECATED: 더 이상 지원하지 않음
        """

        CREATED = "created"
        IN_SERVICE = "in_service"
        DEPRECATED = "deprecated"

    def __init__(self, **kwargs):
        """
        AutoML 피쳐 클래스.

        ## Attributes

        - id: (int) 피쳐 ID
        - name: (str) 이름
        - source: (str) 원천 경로
        - type: (`sktmls.ml_features.MLFeature.Type`) 타입
        - status: (`sktmls.ml_features.MLFeature.Status`) 서비스 상태
        - title: (str) 타이틀
        - description: (str) 설명
        - group: (str) 피쳐 그룹
        - created_at: (datetime.datetime) 생성 시각
        - updated_at: (datetime.datetime) 갱신 시각
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.source = kwargs.get("source")
        self.type = MLFeature.Type(kwargs.get("type"))
        self.status = MLFeature.Status(kwargs.get("status"))
        self.title = kwargs.get("title")
        self.description = kwargs.get("description")
        self.group = kwargs.get("group")

        try:
            self.created_at = parser.parse(kwargs.get("created_at"))
        except TypeError:
            self.created_at = None

        try:
            self.updated_at = parser.parse(kwargs.get("updated_at"))
        except TypeError:
            self.updated_at = None

    def __str__(self) -> str:
        return f"{self.source}.{self.name}"

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class MLFeatureGroup:
    def __init__(self, **kwargs):
        """
        AutoML 피쳐 그룹 클래스.

        ## Attributes

        - id: (int) 피쳐 그룹 ID
        - name: (str) 피쳐 그룹 이름
        - description: (str) 피쳐 그룸 설명
        - ml_features: (list(`sktmls.ml_features.MLFeature`)) 피쳐 그룹에 등록된 피쳐 리스트
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.description = kwargs.get("source")
        self.ml_features = [MLFeature(**feature) for feature in kwargs.get("ml_features", [])]

    def __str__(self):
        return self.name


class MLFeatureGroupClient(MLSClient):
    def __init__(
        self,
        env: MLSENV = None,
        runtime_env: MLSRuntimeENV = None,
        username: str = None,
        password: str = None,
    ):
        """
        AutoML 피쳐 그룹 관련 기능을 제공하는 클라이언트 클래스입니다.

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
        `sktmls.ml_features.MLFeatureGroupClient`

        ## Example

        ```python
        client = MLFeatureGroupClient(env=MLSENV.STG, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def list_feature_groups(self) -> List[MLFeatureGroup]:
        """
        AutoML 피쳐 그룹 리스트를 가져옵니다.

        ## Returns
        list(`sktmls.ml_features.ml_feature.MLFeatureGroup`)

        ## Example
        ```
        feature_groups = client.list_feature_groups()
        ```
        """
        response = self._request(method="GET", url="api/v1/ml_feature_groups")
        return [MLFeatureGroup(**fg) for fg in response.results]


class MLFeatureClient(MLSClient):
    def __init__(
        self,
        env: MLSENV = None,
        runtime_env: MLSRuntimeENV = None,
        username: str = None,
        password: str = None,
    ):
        """
        AutoML 피쳐 관련 기능을 제공하는 클라이언트 클래스입니다.

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
        `sktmls.ml_features.MLFeatureClient`

        ## Example

        ```python
        client = MLFeatureClient(env=MLSENV.STG, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def create_feature(
        self,
        name: str,
        source: str,
        type: MLFeature.Type,
        title: str = None,
        description: str = None,
    ) -> MLFeature:
        """
        새로운 AutoML 피쳐를 생성합니다.

        ## Args

        - name: (str) 이름
        - source: (str) 원천 경로
        - type: (`sktmls.ml_features.MLFeature.Type`) 타입
        - title: (optional) (str) 타이틀
        - description: (optional) (str) 설명

        ## Returns
        `sktmls.ml_features.MLFeature`
        """
        data = {
            "name": name,
            "source": source,
            "type": type.value,
        }
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description

        resp = self._request(method="POST", url="api/v1/ml_features", data=data).results

        return MLFeature(**resp)

    def update_feature(
        self,
        ml_feature: MLFeature,
        title: str = None,
        description: str = None,
        status: MLFeature.Status = None,
    ) -> MLFeature:
        """
        AutoML 피쳐를 수정합니다.

        ## Args
        - title: (optional) (str) 타이틀
        - description: (optional) (str) 설명
        - status: (`sktmls.ml_features.MLFeature.Status`) 서비스 상태

        ## Returns
        `sktmls.ml_features.MLFeature`
        """
        assert type(ml_feature) == MLFeature
        assert status in MLFeature.Status

        data = {"status": status.value}

        if title:
            data["title"] = title
        if description:
            data["description"] = description

        resp = self._request(method="PUT", url=f"api/v1/ml_features/{ml_feature.id}", data=data).results

        ml_feature.reset(**resp)

        return ml_feature

    def list_features(self, **kwargs) -> List[MLFeature]:
        """
        AutoML 피쳐의 리스트를 가져옵니다.

        ## Args

        - kwargs: (optional) (dict) 쿼리 조건
            - id: (int) 피쳐 ID
            - name: (str) 이름
            - source: (str) 원천 경로
            - type: (`sktmls.ml_features.MLFeature.Type`) 타입
            - status: (`sktmls.ml_features.MLFeature.Status`) 서비스 상태
            - title: (str) 타이틀
            - description: (str) 설명
            - query: (str) 검색 문자
            - page: (int) 페이지 번호

        ## Returns
        list(`sktmls.ml_features.MLFeature`)

        ## Example
        ```
        ml_features = client.list_features()
        ```
        """
        response = self._request(method="GET", url="api/v1/ml_features", params=kwargs).results

        return [MLFeature(**ml_feature) for ml_feature in response]

    def get_feature(self, id: int = None, name: str = None, source: str = None) -> MLFeature:
        """
        AutoML 피쳐를 가져옵니다.

        ## Args
        id 또는 name, source 조합 중 하나만 입력 가능합니다.

        - id: (int) 피쳐 ID
        - name: (str) 이름
        - source: (str) 원천 경로

        ## Returns

        `sktmls.ml_features.MLFeature`
        - id: (int) 피쳐 ID
        - name: (str) 이름
        - source: (str) 원천 경로
        - type: (`sktmls.ml_features.MLFeature.Type`) 타입
        - status: (`sktmls.ml_features.MLFeature.Status`) 서비스 상태
        - title: (str) 타이틀
        - description: (str) 설명
        - created_at: (datetime.datetime) 생성 시각
        - updated_at: (datetime.datetime) 갱신 시각

        ## Example
        ```
        ml_feature = client.get_feature(id=1)
        ```
        """
        assert id or name, "`id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다."
        assert not (id and name), "`id` 또는 `name` 은 동시에 사용될 수 없습니다."
        assert source if name else True, "`name` 은 반드시 `source` 와 함께 사용되어야 합니다."

        ml_features = self.list_features(id=id, name=name, source=source)

        if len(ml_features) == 0:
            raise DoesNotExist()

        return ml_features[0]

    def delete_feature(self, ml_feature: MLFeature):
        """
        AutoML 피쳐를 삭제합니다.

        ## Args

        - ml_feature: (`sktmls.ml_features.MLFeature`) AutoML 피쳐 객체

        ## Returns
        `sktmls.MLSResponse`

        ## Example

        ```
        client.delete_feature(ml_feature)
        ```
        """

        assert type(ml_feature) == MLFeature

        return self._request(method="DELETE", url=f"api/v1/ml_features/{ml_feature.id}")
