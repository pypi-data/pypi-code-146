from dateutil import parser
from enum import Enum


class MLModel:
    def __init__(self, **kwargs):
        """
        ## Args

        - kwargs
            - id: (int) ML모델 고유 ID
            - name: (str) ML모델 이름
            - version: (str) ML모델 버전
            - creator: (str) ML모델 생성 계정명
            - description: (str) ML모델 설명
            - table: (str) ML모델 테이블
            - model_data: (str) ML모델 물리적 위치
            - model_lib : (`mlops_sdk.models.MLModelLib`) 모델 라이브러리
            - model_lib_version : (str) 모델 라이브러리 버전
            - model_checkpoint : (str) 모델 체크포인트
            - product_name : (str) 데이터 프로덕트 이름
            - dataset_train : (str) 학습 데이터셋 ID
            - dataset_test : (str) 테스트 데이터셋 ID
            - eval_metric : (str) 평가 메트릭
            - eval_method : (str) 평가 방법
            - status: (`mlops_sdk.models.MLModelStatus`) ML모델 상태
            - created_at: (datetime) 생성일시
            - updated_at: (datetime) 수정일시

        ## Returns
        `mlops_sdk.models.MLModel`
        """
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.version = kwargs.get("version")
        self.description = kwargs.get("description")
        self.creator = kwargs.get("creator")
        self.table = kwargs.get("table")
        self.model_data = kwargs.get("model_data")
        self.model_lib = kwargs.get("model_lib")
        self.model_lib_version = kwargs.get("model_lib_version")
        self.model_checkpoint = kwargs.get("model_checkpoint")
        self.product_name = kwargs.get("product_name")
        self.dataset_train = kwargs.get("dataset_train")
        self.dataset_test = kwargs.get("dataset_test")
        self.eval_metric = kwargs.get("eval_metric")
        self.eval_method = kwargs.get("eval_method")
        self.status = kwargs.get("status")
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

    def get(self) -> dict:
        return self.__dict__

    def reset(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class MLModelStatus(Enum):
    IN_USE = "IN_USE"
    NOT_IN_USE = "NOT_IN_USE"
    AUTOML_TRAINING = "TRAINING"
    AUTOML_DONE = "DONE"
    AUTOML_FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


class MLModelLib(Enum):
    PYTORCH = "pytorch"
    TENSORFLOW = "tensorflow"
    SKLEARN = "sklearn"


class MLModelClient:
    def __init__():
        """
        ## Args

        ## Returns
        `mlops_sdk.models.MLModelClient`

        ## Example

        ```python
        ml_model_client = MLModelClient()
        ```
        """
        super().__init__()
