from dateutil import parser
from enum import Enum
from string import Template
from typing import Any, Dict, List

from sktmls import MLSClient, MLSENV, MLSRuntimeENV

SPARK_QUERY_FOR_LABLE_DATA = Template(
    """
SELECT sha2(source.svc_mgmt_num, 256) AS svc_mgmt_num, source.period AS period
FROM (
    ${source_query}
) AS source
"""
)


class ProblemType(Enum):
    """
    AutoML 데이터셋의 문제 타입입니다.

    - SCORE: 스코어 기반 고객 타겟팅
    - CLASSIFICATION: 분류
    - REGRESSION: 회귀
    """

    SCORE = "score"
    CLASSIFICATION = "classification"
    REGRESSION = "regression"


class DatasetError(Exception):
    def __init__(self, *args, **kwargs):
        """
        AutoML 데이터셋 에러.
        """
        super().__init__(*args, **kwargs)


class FeatureStoreConf:
    def __init__(self, enabled: bool, feature_group_id_list: List[int] = None, n_label_ratio: float = 1.0):
        """
        AutoML 데이터셋의 피쳐 스토어 설정입니다.

        ## Args

        - enabled: (bool) 피쳐 스토어 사용 유무
        - feature_group_id_list: (optional) (list(int)) 사용하고자 하는 피쳐 그룹의 ID 리스트
        - n_label_ratio: (optional) (float) N 레이블 샘플링 비율 (스코어 기반 고객 타겟팅 문제만 지원, 기본값: 1.0)

        ## Example

        ```python
        config = FeatureStoreConf(enabled=True, feature_group_id_list=[1, 2, 3], n_label_ratio=1.5)
        ```
        """
        self.enabled = enabled
        self.feature_group_id_list = feature_group_id_list
        self.n_label_ratio = n_label_ratio

    def __str__(self) -> str:
        return str(self.__dict__)


class LabelDataConf:
    def __init__(self, source_type: str, source_path: str, reverse: bool = False):
        """
        AutoML 데이터셋의 레이블 데이터 설정입니다.

        ## Args

        - source_type: (str) 레이블 데이터 타입 (`file` | `table`).
        - source_path: (str) 레이블 데이터의 이름 또는 테이블 경로.
          - file: 파일 이름 (ex. test.csv)
          - table: BigQuery 테이블의 경로 (ex. sktaic-datahub.x1234567.test)

        ## Example

        ```python
        config = LabelDataConf(source_type="table", source_path="sktaic-datahub.x1234567.test")
        ```
        """
        if not reverse:
            assert source_type in [
                "file",
                "table",
            ], "source_type 은(는) ['file', 'table'] 중 하나여야 합니다."

            assert type(source_path) == str, "source_path 은(는) str 타입이어야 합니다."

        self.source_type = source_type
        self.source_path = source_path

    def __str__(self) -> str:
        return str(self.__dict__)


class Dataset:
    def __init__(self, **kwargs):
        """
        AutoML 학습 데이터셋 클래스.

        ## Attributes

        - id: (int) 데이터셋 ID
        - name: (str) 데이터셋 이름
        - status: (str) 데이터셋 상태
        - problem_type: (`sktmls.datasets.ProblemType`) 문제 타입
        - feature_store_conf: (`sktmls.datasets.FeatureStoreConf`) 피쳐 스토어 설정값
        - label_data_conf: (`sktmls.datasets.LabelDataConf`) 레이블 데이터 설정값
        - created_at: (datetime.datetime) 데이터셋 생성 시점
        - updated_at: (datetime.datetime) 데이터셋 생성 완료 또는 갱신 시점
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.status = kwargs.get("status")
        self.problem_type = ProblemType(kwargs.get("data_type"))
        self._setup_conf = kwargs.get("setup_conf", {})

        base_feature_conf = self._setup_conf.get("base_feature_conf", {})
        self.feature_store_conf = FeatureStoreConf(
            enabled=base_feature_conf.get("enabled"),
            feature_group_id_list=base_feature_conf.get("feature_group_id_list"),
            n_label_ratio=base_feature_conf.get("n_label_ratio"),
        )

        label_data_conf = self._setup_conf.get("label_data_conf", {})
        self.label_data_conf = LabelDataConf(
            source_type=label_data_conf.get("source_type"),
            source_path=label_data_conf.get("source_path"),
            reverse=True,
        )

        try:
            self.created_at = parser.parse(kwargs.get("created_at"))
        except TypeError:
            self.created_at = None

        try:
            self.updated_at = parser.parse(kwargs.get("updated_at"))
        except TypeError:
            self.updated_at = None

    def __str__(self) -> str:
        return self.name

    def get_error(self) -> str:
        """
        데이터셋 생성 시 에러 발생 원인을 조회한다. (데이터셋 생성 실패 시에만 값 존재)

        ## Returns
        str
        """
        return self._setup_conf.get("error")


class DatasetClient(MLSClient):
    def __init__(
        self, env: MLSENV = None, runtime_env: MLSRuntimeENV = None, username: str = None, password: str = None
    ):
        """
        AutoML 데이터셋 관련 기능을 제공하는 클라이언트 클래스입니다.

        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.EDD`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)
        - username: (str) MLS 계정명 (기본값: $MLS_USERNAME)
        - password: (str) MLS 계정 비밀번호 (기본값: $MLS_PASSWORD)

        ## Returns
        `sktmls.datasets.DatasetClient`

        ## Example

        ```python
        client = DatasetClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def create_dataset(
        self, name: str, problem_type: ProblemType, feature_store_conf: FeatureStoreConf, label_data_conf: LabelDataConf
    ) -> Dataset:
        """
        새 AutoML 데이터셋을 생성합니다.

        ## Args

        - name: (str) 데이터셋 이름
        - problem_type: (`sktmls.datasets.ProblemType`) 문제 타입
        - feature_store_conf: (`sktmls.datasets.FeatureStoreConf`) 피쳐 스토어 설정
        - label_data_conf: (`sktmls.datasets.LabelDataConf`) 레이블 데이터 설정

        ## Returns
        `sktmls.datasets.Dataset`

        ## Example

        ```python
        client = DatasetClient()
        dataset = client.create_dataset(
            name="my_dataset",
            problem_type=ProblemType.SCORE,
            feature_store_conf=FeatureStoreConf(enabled=True, feature_group_id_list=[1, 2, 3], n_label_ratio=1.5),
            label_data_conf=LabelDataConf(source_type="ye", source_path="my_test_table"),
        )
        ```
        """
        data = {
            "name": name,
            "type": problem_type.value,
            "base_feature_conf": feature_store_conf.__dict__,
            "label_data_conf": label_data_conf.__dict__,
        }

        response = self._request(method="POST", url="api/v1/datasets", data=data)
        return Dataset(**response.results)

    def list_datasets(self, **kwargs) -> List[Dataset]:
        """
        AutoML 데이터셋 리스트를 가져옵니다.

        ## Args

        - kwargs: (optional) (dict) 쿼리 조건
            - id: (int) 데이터셋 ID
            - name: (str) 데이터셋 이름
            - query: (str) 검색 문자
            - page: (int) 페이지 번호

        ## Returns
        list(`sktmls.datasets.Dataset`)
        """
        response = self._request(method="GET", url="api/v1/datasets", params=kwargs)
        return [Dataset(**dataset) for dataset in response.results]

    def get_dataset(self, name: str = None, id: int = None) -> Dataset:
        """
        해당하는 AutoML 데이텨셋을 가져옵니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) 데이터셋 ID
        - name: (str) 데이터셋 이름

        ## Returns
        `sktmls.datasets.Dataset`
        """
        assert id is not None or name, "One of id or name must be provided"

        datasets = self.list_datasets(name=name, id=id)

        if len(datasets) == 0:
            raise DatasetError("Dataset does not exists")

        return datasets[0]

    def delete_dataset(self, name: str = None, id: int = None) -> None:
        """
        해당하는 AutoML 데이터셋을 삭제합니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) 데이터셋 ID
        - name: (str) 데이터셋 이름

        """
        dataset = self.get_dataset(name=name, id=id)
        self._request(method="DELETE", url=f"api/v1/datasets/{dataset.id}")

    def list_features(self, name: str = None, id: int = None) -> List[Dict[str, Any]]:
        """
        AutoML 데이터셋에 추가된 피쳐 리스트를 조회합니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) 데이터셋 ID
        - name: (str) 데이터셋 이름
        """
        dataset = self.get_dataset(name=name, id=id)
        response = self._request(method="GET", url=f"api/v1/datasets/{dataset.id}/columns")
        return response.results.get("columns", [])

    def update_column_specs(self, name: str = None, id: int = None, column_specs=None) -> None:
        """
        데이터셋의 컬럼 스펙을 업데이트 합니다.

        ## Args: `id` 또는 `name` 중 한 개 이상의 값이 반드시 전달되어야 합니다.

        - id: (int) 데이터셋 ID
        - name: (str) 데이터셋 이름
        - column_spec: (dict) 컬럼 스펙 (ex. {"feature_name": {"include": False}})
          - include: (bool) 학습 포함 여부
          - type_code: (str) 컬럼 타입 ("FLOAT64" | "CATEGORY")
        """
        assert type(column_specs) == dict, "'column_specs' must be a dict type"

        dataset = self.get_dataset(name=name, id=id)
        self._request("PUT", f"/api/v1/datasets/{dataset.id}/columnspecs", {"edit_columns": column_specs})
