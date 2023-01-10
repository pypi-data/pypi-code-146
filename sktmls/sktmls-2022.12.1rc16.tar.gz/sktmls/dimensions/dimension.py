from typing import List

from dateutil import parser

from sktmls import MLSClient, MLSENV, MLSRuntimeENV, MLSResponse, MLSClientError

MLS_DIMENSIONS_API_URL = "/api/v1/dimensions"


class Dimension:
    """
    MLS 디멘전 클래스입니다.
    """

    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) 디멘전 고유 ID
            - name: (str) 디멘전 이름
            - dimension_type: (str) 디멘전 타입 (`user`|`item`)
            - data_type: (str) 디멘전 데이터 타입 (`string`|`number`)
            - default: (str) 디멘전 기본 값
            - period: (str) 디멘전 생성 주기 (`daily`|`monthly`)
            - description: (str) 디멘전 설명
            - task_id: (str) 디멘전 생성 Airflow Task ID
            - tag: (str) 디멘전 태그
            - is_derivative: (bool) 디멘전 파생변수 여부
            - is_enabled: (bool) 디멘전 서비스 여부
            - created_at: (datetime) 생성일시
            - updated_at: (datetime) 수정일시

        ## Returns
        `sktmls.dimensions.Dimension`
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.dimension_type = kwargs.get("dimension_type")
        self.data_type = kwargs.get("data_type")
        self.default = kwargs.get("default")
        self.period = kwargs.get("period")
        self.description = kwargs.get("description")
        self.task_id = kwargs.get("task_id")
        self.tag = kwargs.get("tag")

        self.is_derivative = kwargs.get("is_derivative")
        self.is_enabled = kwargs.get("is_enabled")
        try:
            self.created_at = parser.parse(kwargs.get("created_at"))
        except TypeError:
            self.created_at = None
        try:
            self.updated_at = parser.parse(kwargs.get("updated_at"))
        except TypeError:
            self.updated_at = None

    def get(self):
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class DimensionClient(MLSClient):
    """
    MLS 디멘전 관련 기능들을 제공하는 클라이언트입니다.
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
        `sktmls.dimensions.DimensionClient`

        ## Example

        ```python
        dimension_client = DimensionClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """

        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def create_dimension(
        self,
        name: str,
        dimension_type: str,
        data_type: str,
        default: str,
        period: str,
        description: str = None,
        task_id: str = None,
        tag: str = None,
        is_derivative: bool = None,
        is_enabled: bool = None,
    ) -> Dimension:
        """
        디멘전을 생성합니다.

        ## Args

        - name: (str) 디멘전 이름
        - dimension_type: (str) 디멘전 타입 (`user`|`item`)
        - data_type: (str) 디멘전 데이터 타입 (`string`|`number`|`array`|`json`)
        - default: (str) 디멘전 기본 값
        - period: (str) 디멘전 생성 주기 (`daily`|`monthly`)
        - description: (optional) (str) 디멘전 설명
        - task_id: (optional) (str) 디멘전 생성 Airflow Task ID
        - tag: (optional) (str) 디멘전 태그
        - is_derivative: (optional) (bool) 디멘전 파생변수 여부 (기본값: False)
        - is_enabled: (optional) (bool) 디멘전 서비스 여부 (기본값: True)

        ## Returns
        `sktmls.dimensions.Dimension`

        - id: (int) 디멘전 고유 ID
        - name: (str) 디멘전 이름
        - dimension_type: (str) 디멘전 타입 (`user`|`item`)
        - data_type: (str) 디멘전 데이터 타입 (`string`|`number`|`array`|`json`)
        - description: (str) 디멘전 설명
        - default: (str) 디멘전 기본 값
        - task_id: (str) 디멘전 생성 Airflow Task ID
        - period: (str) 디멘전 생성 주기 (`daily`|`monthly`)
        - tag: (str) 디멘전 태그
        - is_derivative: (bool) 디멘전 파생변수 여부
        - is_enabled: (bool) 디멘전 서비스 여부
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        dimension = dimension_client.create_dimension(
            name="hello",
            dimension_type="user",
            data_type="string",
            default="1",
            period="daily"
        )
        ```
        """
        assert dimension_type in ["user", "item"]
        assert data_type in ["string", "number", "array", "json"]
        assert period in ["daily", "monthly"]

        data = {
            "name": name,
            "dimension_type": dimension_type,
            "data_type": data_type,
            "default": default,
            "period": period,
        }
        if description:
            data["description"] = description
        if task_id:
            data["task_id"] = task_id
        if tag:
            data["tag"] = tag
        if is_derivative is not None:
            data["is_derivative"] = is_derivative
        if is_enabled is not None:
            data["is_enabled"] = is_enabled

        return Dimension(**self._request(method="POST", url=MLS_DIMENSIONS_API_URL, data=data).results)

    def update_dimension(
        self,
        dimension: Dimension,
        name: str = None,
        dimension_type: str = None,
        data_type: str = None,
        default: str = None,
        period: str = None,
        description: str = None,
        task_id: str = None,
        tag: str = None,
        is_derivative: bool = None,
        is_enabled: bool = None,
    ) -> Dimension:
        """
        디멘전 정보를 수정합니다.

        ## Args

        - dimension: (`sktmls.dimensions.Dimension`) 디멘전 객체
        - name: (optional) (str) 디멘전 이름
        - dimension_type: (optional) (str) 디멘전 타입 (`user`|`item`)
        - data_type: (optional) (str) 디멘전 데이터 타입 (`string`|`number`|`array`|`json`)
        - default: (optional) (str) 디멘전 기본 값
        - period: (optional) (str) 디멘전 생성 주기 (`daily`|`monthly`)
        - description: (optional) (str) 디멘전 설명
        - task_id: (optional) (str) 디멘전 생성 Airflow Task ID
        - tag: (optional) (str) 디멘전 태그
        - is_derivative: (optional) (bool) 디멘전 파생변수 여부
        - is_enabled: (optional) (bool) 디멘전 서비스 여부

        ## Returns
        `sktmls.dimensions.Dimension`

        - id: (int) 디멘전 고유 ID
        - name: (str) 디멘전 이름
        - dimension_type: (str) 디멘전 타입 (`user`|`item`)
        - data_type: (str) 디멘전 데이터 타입 (`string`|`number`|`array`|`json`)
        - default: (str) 디멘전 기본 값
        - period: (str) 디멘전 생성 주기 (`daily`|`monthly`)
        - description: (str) 디멘전 설명
        - task_id: (str) 디멘전 생성 Airflow Task ID
        - tag: (optional) (str) 디멘전 태그
        - is_derivative: (bool) 디멘전 파생변수 여부
        - is_enabled: (bool) 디멘전 서비스 여부
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        dimension = dimension_client.update_dimension(
            dimension=dimension,
            name="bye",
            default="2",
            period="monthly"
        )
        ```
        """
        assert type(dimension) == Dimension

        data = {
            "name": dimension.name,
            "dimension_type": dimension.dimension_type,
            "data_type": dimension.data_type,
            "default": dimension.default,
            "period": dimension.period,
        }
        if dimension.description is not None:
            data["description"] = dimension.description
        if dimension.task_id is not None:
            data["task_id"] = dimension.task_id
        if dimension.tag is not None:
            data["tag"] = dimension.tag
        if dimension.is_derivative is not None:
            data["is_derivative"] = dimension.is_derivative
        if dimension.is_enabled is not None:
            data["is_enabled"] = dimension.is_enabled

        if name:
            data["name"] = name
        if dimension_type:
            assert dimension_type in ["user", "item"]
            data["dimension_type"] = dimension_type
        if data_type:
            assert data_type in ["string", "number", "array", "json"]
            data["data_type"] = data_type
        if default:
            data["default"] = default
        if period:
            assert period in ["daily", "monthly"]
            data["period"] = period
        if description is not None:
            data["description"] = description
        if task_id is not None:
            data["task_id"] = task_id
        if tag is not None:
            data["tag"] = tag
        if is_derivative is not None:
            data["is_derivative"] = is_derivative
        if is_enabled is not None:
            data["is_enabled"] = is_enabled

        dimension.reset(
            **self._request(method="PUT", url=f"{MLS_DIMENSIONS_API_URL}/{dimension.id}", data=data).results
        )

        return dimension

    def get_dimension(self, dimension_type: str, id: int = None, name: str = None) -> Dimension:
        """
        디멘전 정보를 가져옵니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - dimension_type: (str) 디멘전 타입 (`user`|`item`)
        - id: (optional) (int) 디멘전 고유 ID
        - name: (optional) (str) 디멘전 이름


        ## Returns
        `sktmls.dimensions.Dimension`

        - id: (int) 디멘전 고유 ID
        - name: (str) 디멘전 이름
        - dimension_type: (str) 디멘전 타입 (`user`|`item`)
        - data_type: (str) 디멘전 데이터 타입 (`string`|`number`|`array`|`json`)
        - default: (str) 디멘전 기본 값
        - period: (str) 디멘전 생성 주기 (`daily`|`monthly`)
        - description: (str) 디멘전 설명
        - task_id: (str) 디멘전 생성 Airflow Task ID
        - tag: (str) 디멘전 태그
        - is_derivative: (bool) 디멘전 파생변수 여부
        - is_enabled: (bool) 디멘전 서비스 여부
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        dimension = dimension_client.get_dimension(
            dimension_type="user",
            name="hello"
        )
        ```
        """
        assert id or name, "`id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다."

        dimensions = self.list_dimensions(dimension_type=dimension_type, id=id, name=name)
        if len(dimensions) == 0:
            raise MLSClientError(code=404, msg="디멘전이 없습니다.")
        elif len(dimensions) > 1:
            raise MLSClientError(code=409, msg="디멘전이 여러개 존재합니다.")
        return dimensions[0]

    def list_dimensions(self, dimension_type: str, **kwargs) -> List[Dimension]:
        """
        디멘전 리스트를 가져옵니다.

        ## Args

        - dimension_type: (str) 디멘전 타입 (`user`|`item`)
        - kwargs: (optional) (dict) 쿼리 조건
            - id: (int) 디멘전 고유 ID
            - name: (str) 디멘전 이름
            - data_type: (str) 디멘전 데이터 타입 (`string`|`number`|`array`|`json`)
            - period: (str) 디멘전 생성 주기 (`daily`|`monthly`)
            - task_id: (str) 디멘전 생성 Airflow Task ID
            - tag: (str) 디멘전 태그
            - is_derivative: (bool) 파생 변수 여부
            - is_enabled: (bool) 디멘전 서비스 여부
            - query: (str) 검색 문자
            - page: (int) 페이지 번호


        ## Returns
        list(`sktmls.dimensions.Dimension`)

        - id: (int) 디멘전 고유 ID
        - name: (str) 디멘전 이름
        - dimension_type: (str) 디멘전 타입 (`user`|`item`)
        - data_type: (str) 디멘전 데이터 타입 (`string`|`number`|`array`|`json`)
        - default: (str) 디멘전 기본 값
        - period: (str) 디멘전 생성 주기 (`daily`|`monthly`)
        - description: (str) 디멘전 설명
        - task_id: (str) 디멘전 생성 Airflow Task ID
        - tag: (str) 디멘전 태그
        - is_derivative: (bool) 디멘전 파생변수 여부
        - is_enabled: (bool) 디멘전 서비스 여부
        - created_at: (datetime) 생성일시
        - updated_at: (datetime) 수정일시

        ## Example

        ```python
        dimensions = dimension_client.list_dimensions(
            dimension_type="user"
        )

        derivative_dimensions = dimension_client.list_dimensions(
            dimension_type="user",
            is_derivative=True
        )

        string_dimensions = dimension_client.list_dimensions(
            dimension_type="user",
            data_type="string"
        )
        ```
        """

        response = self._request(
            method="GET", url=f"{MLS_DIMENSIONS_API_URL}?type={dimension_type}", params=kwargs
        ).results

        return [Dimension(**dimension) for dimension in response]

    def delete_dimension(self, dimension: Dimension) -> MLSResponse:
        """
        디멘전을 삭제합니다.

        ## Args

        - dimension: (`sktmls.dimensions.Dimension`) 디멘전 객체

        ## Returns
        `sktmls.MLSResponse`

        ## Example

        ```python
        dimension_client.delete_dimension(dimension)
        ```
        """

        assert type(dimension) == Dimension

        return self._request(method="DELETE", url=f"{MLS_DIMENSIONS_API_URL}/{dimension.id}")
