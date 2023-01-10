import re
import sys

from dateutil import parser
from typing import Any, Dict, Union

from sktmls import MLSClient, MLSENV, MLSRuntimeENV
from sktmls.datasets import DatasetClient, ProblemType
from sktmls.models import AutoMLModel


class AutoMLPredictionError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ScoreExportOption:
    def __init__(self, sort: bool, target_limit: int = None):
        """
        스코어 출력 옵션 값입니다(스코어 기반 고객 타겟팅 문제만 지원).

        ## Args

        - sort: (bool) 결과 정렬 여부
        - target_limit: (int) 총 출력 개수 (sort = True 인 경우 필수)

        ## Returns
        `sktmls.models.automl.ScoreExportOption`

        ## Example

        ```python
        score_export_option = ScoreExportOption(sort=True, target_limit=1000000)
        ```
        """
        assert type(sort) == bool, "sort 은(는) bool 타입이어야 합니다."
        assert type(target_limit) == int if target_limit is not None else True, "target_limit 은(는) int 타입이어야 합니다."
        assert target_limit is not None if sort else True, "sort = True 인 경우 target_limit 은 반드시 전달되어야 합니다."
        assert target_limit <= 10000000 if sort else True, "target_limit 값은 10,000,000 이하여야 합니다."
        self.sort = sort
        self.target_limit = target_limit

    def value(self) -> Dict[str, Any]:
        return {"sort": self.sort, "target_limit": self.target_limit} if self.sort else {"sort": self.sort}


class CustomFeatureSourceConfig:
    def __init__(self, source_type: str, source_path: str):
        """
        예측 시 추가로 사용할 사용자 데이터 설정입니다(사용자 피쳐를 추가로 적용한 모델의 경우 필수).

        ## Args

        - source_type: (str) 데이터 타입 (`csv (deprecated)` | `edd2 (deprecated)` | `ye(deprecated)` | `file` | `table`).
        - source_path: (str) 데이터의 이름 또는 테이블 경로.
          - file: 파일 이름 (ex. test.csv)
          - table: BigQuery 테이블의 경로 (ex. sktaic-datahub.x1234567.test)

        ## Example

        ```python
        config = LabelDataConf(source_type="table", source_path="sktaic-datahub.x1234567.test")
        ```
        """
        assert source_type in [
            "csv",
            "edd2",
            "ye",
            "file",
            "table",
        ], "source_type 은(는) ['csv', 'edd2', 'ye', 'file', 'table'] 중 하나여야 합니다."

        if source_type in ["csv"]:
            print(
                "[Warn] CustomFeatureSourceConfig: 'csv' 타입은 deprecate 되었습니다. 'file' 타입을 사용해주세요.",
                file=sys.stderr,
            )
            source_type = "file"

        if source_type in ["edd2", "ye"]:
            print(
                "[Warn] CustomFeatureSourceConfig: 'edd2', 'ye' 타입은 deprecate 되었습니다. 'table' 타입을 사용해주세요.",
                file=sys.stderr,
            )
            source_type = "table"

        assert type(source_path) == str, "source_path 은(는) str 타입이어야 합니다."
        self.source_type = source_type
        self.source_path = source_path


class ExportChannelConfig:
    def __init__(self, channel: str):
        self.channel = channel


class EmailChannelConfig(ExportChannelConfig):
    param_name = "email_channel_config"

    def __init__(self, email: str):
        """
        이메일로 예측 결과를 전송하기 위한 설정 값입니다.

        ## Args

        - email: (str) 전송받을 이메일 경로 (@sktelecom.com 또는 @sk.com 도메인만 지원)

        ## Returns
        `sktmls.models.automl.EmailChannelConfig`

        ## Example

        ```python
        config = EmailChannelConfig("test@sktelecom.com")
        ```
        """
        super().__init__("EMAIL")
        assert type(email) == str, "email 은(는) str 타입이어야 합니다."
        self.email = email


class TOSChannelConfig(ExportChannelConfig):
    param_name = "tos_channel_config"

    def __init__(self, employee_num: str, target_group_name: str):
        """
        TOS로 예측 결과를 전송하기 위한 설정 값입니다.

        ## Args

        - employee_num: (str) 사번 (TOS 계정)
        - target_group_name: (str) 원하는 대상군 명

        ## Returns
        `sktmls.models.automl.TOSChannelConfig`

        ## Example

        ```python
        config = TOSChannelConfig("test@sktelecom.com")
        ```
        """
        super().__init__("TOS")
        assert type(employee_num) == str, "employee_num 은(는) str 타입이어야 합니다."
        assert type(target_group_name) == str, "target_group_name 은(는) str 타입이어야 합니다."
        self.employee_num = employee_num
        self.target_group_name = target_group_name


class EDDChannelConfig(ExportChannelConfig):
    param_name = "edd_channel_config"

    def __init__(self, username: str, database: str, table: str):
        """
        EDD로 예측 결과를 전송하기 위한 설정 값입니다.

        ## Args

        - username: (str) EDD 계정 (ex. g1234567)
        - database: (str) 데이터베이스 이름
        - table: (str) 테이블 이름

        ## Returns
        `sktmls.models.automl.EDDChannelConfig`

        ## Example

        ```python
        config = EDDChannelConfig("g1234567", "test_db", "test_table")
        ```
        """
        super().__init__("EDD")
        assert type(username) == str, "username 은(는) str 타입이어야 합니다."
        assert type(database) == str, "database 은(는) str 타입이어야 합니다."
        assert type(table) == str, "table 은(는) str 타입이어야 합니다."
        assert re.match(r"^[a-z][0-9]{7}", username), "잘못된 형식의 EDD 계정입니다."
        assert re.match(r"^[A-Za-z0-9_]+$", database), "잘못된 형식의 데이터베이스 이름입니다."
        assert re.match(r"^[A-Za-z0-9_]+$", table), "잘못된 형식의 테이블 이름입니다."
        self.username = username
        self.database = database
        self.table = table


class YEChannelConfig(ExportChannelConfig):
    param_name = "ye_channel_config"

    def __init__(self, username: str, table: str):
        """
        YE로 예측 결과를 전송하기 위한 설정 값입니다.

        ## Args

        - username: (str) YE 계정 (ex. "x1234567") 또는 BigQuery 데이터셋 이름 ("test_dataset")
        - table: (str) 테이블 이름 (ex. "test_table")

        ## Returns
        `sktmls.models.automl.YEChannelConfig`

        ## Example

        ```python
        config = YEChannelConfig("x1234567", "test_table")
        ```
        """
        super().__init__("YE")
        assert type(username) == str, "username 은(는) str 타입이어야 합니다."
        assert type(table) == str, "table 은(는) str 타입이어야 합니다."
        assert re.match(r"^[A-Za-z0-9_]+$", username), "잘못된 형식의 YE 계정 (또는 BigQuery 데이터셋 이름) 입니다."
        assert re.match(r"^[A-Za-z0-9_]+$", table), "잘못된 형식의 테이블 이름입니다."
        self.username = username
        self.table = table


class AutoMLBatchPrediction:
    def __init__(self, **kwargs):
        """
        AutoML 배치 예측 작업 클래스입니다.

        ## Args

        - id: (int) 예측 작업 ID.
        - channel: (string) 전송 채널 (`EMAIL` | `TOS` | `EDD` | `YE`)
        - status: (string) 예측 진행 상태 (`RUNNING` | `DONE` | `ERROR_BATCH_PREDICT`)
        - created_at: (datetime) 예측 시작 시간
        - updated_at: (datetime) 예측 완료 시간

        ## Returns
        `sktmls.models.automl.AutoMLBatchPrediction`
        """
        self.id = kwargs.get("id")
        self.channel = kwargs.get("name")
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
        return str(self.id)


class AutoMLBatchPredictionClient(MLSClient):
    def __init__(
        self, env: MLSENV = None, runtime_env: MLSRuntimeENV = None, username: str = None, password: str = None
    ):
        """
        AutoML 배치 예측 관련 기능을 제공하는 클라이언트입니다.

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
        `sktmls.models.automl.AutoMLBatchPredictionClient`

        ## Example

        ```python
        client = AutoMLBatchPredictionClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        ```
        """
        super().__init__(env=env, runtime_env=runtime_env, username=username, password=password)

    def predict(
        self,
        model: AutoMLModel,
        export_channel_config: Union[EmailChannelConfig, TOSChannelConfig, EDDChannelConfig, YEChannelConfig],
        score_export_option: ScoreExportOption = None,
        period: str = None,
        custom_feature_source_config: CustomFeatureSourceConfig = None,
    ) -> AutoMLBatchPrediction:
        """
        배치 예측을 수행합니다.

        ## Args

        - model: (`sktmls.models.AutoMLModel`) 학습 모델
        - export_channel_config: (`sktmls.models.automl.ExportChannelConfig`) 예측 결과 전송 채널 설정
        - score_export_option: (`sktmls.models.automl.ScoreExportOption`) 스코어 전송 옵션 (스코어 기반 고객 타겟팅 문제의 경우 필수)
        - period: (str) 예측에 적용할 피쳐 스토어 기준연월 (형식: YYYYMM, 만약 입력하지 않을 경우 가장 최신의 기준연월을 적용)
        - custom_feature_source_config: (`sktmls.models.automl.CustomFeatureSourceConfig`) 예측에 적용할 커스텀 피쳐 데이터 파일 설정 (커스텀 피쳐를 사용한 모델의 경우 필수)

        ## Returns
        `sktmls.models.automl.AutoMLBatchPrediction`

        ## Example

        ```python
        client = AutoMLBatchPredictionClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")

        model = model_client.get_automl_model(id=72)
        export_channel_config = YEChannelConfig(username="x1234567", table="triple_a_test")
        score_export_option = ScoreExportOption(sort=True, target_limit=100)
        custom_feature_config = CustomFeatureSourceConfig("ye", "my_custom_feature_table")

        prediction = client.predict(
            model=model,
            export_channel_config=export_channel_config,
            score_export_option=score_export_option,
            custom_feature_source_config=custom_feature_config,
        )
        ```
        """
        assert type(model) == AutoMLModel, "model 은(는) AutoMLModel 타입이어야 합니다."
        assert type(export_channel_config) in [
            EmailChannelConfig,
            TOSChannelConfig,
            EDDChannelConfig,
            YEChannelConfig,
        ], "export_channel_config 은(는) [EmailChannelConfig, TOSChannelConfig, EDDChannelConfig, YEChannelConfig] 중 하나여야 합니다."
        assert (
            score_export_option is None or type(score_export_option) == ScoreExportOption
        ), "score_export_option 은(는) ScoreExportOption 타입이어야 합니다."
        assert period is None or type(period) == str, "period 은(는) str 타입이어야 합니다."

        dataset_client = DatasetClient(
            self._MLSClient__env, self._MLSClient__runtime_env, self._MLSClient__username, self._MLSClient__password
        )
        dataset = dataset_client.get_dataset(id=model.dataset_id)

        if dataset.problem_type == ProblemType.SCORE and not score_export_option:
            raise AutoMLPredictionError("스코어 기반 고객 타겟팅 문제의 경우 score_export_option 파라미터가 필수입니다.")

        export_config = export_channel_config.__dict__
        channel = export_channel_config.channel
        del export_config["channel"]

        data = {"channel": channel}
        data[export_channel_config.param_name] = export_config

        if score_export_option:
            data["score_export_option"] = score_export_option.value()

        if period:
            data["period"] = period

        if custom_feature_source_config:
            data["custom_feature_source_config"] = custom_feature_source_config.__dict__

        return AutoMLBatchPrediction(
            **self._request(method="POST", url=f"/api/v1/models/{model.id}/predictions", data=data).results
        )
