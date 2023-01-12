import time

from typing import List
from sktmls import MLSENV, MLSRuntimeENV
from sktmls.models import MLModelClient, AutoMLModel
from sktmls.experiments import Bucket, ExperimentClient


class AutoMLHelper:
    """
    AutoML모델 Helper 클래스 입니다.
    """

    def __init__(
        self, env: MLSENV = None, runtime_env: MLSRuntimeENV = None, username: str = None, password: str = None
    ):
        self.__experiment_client = ExperimentClient(env, runtime_env, username, password)
        self.__model_client = MLModelClient(env, runtime_env, username, password)

    def upgrade_deployment(
        self, prev_model: AutoMLModel, next_model: AutoMLModel, copy_handler: bool = True, stop_prev_model: bool = True
    ) -> List[Bucket]:
        """
        기존 모델 (`prev_model`) 을 신규 모델 (`next_model`) 으로 대체하는 작업을 지원하는 함수입니다. 기존 모델이 연결되어 있는 모든 버킷들에 신규 모델을 적용합니다.

        신규 모델이 동작중이 아닌 경우, 자동으로 동작 중 상태로 업데이트합니다.

        ## Args

        - prev_model: (`sktmls.models.AutoMLModel`) 기존 모델
        - next_model: (`sktmls.models.AutoMLModel`) 신규 모델
        - copy_handler: (optional) (bool) `prev_model`의 핸들러 코드 복제 여부 (`False` 일 경우, 미리 Handler 가 등록되어 있어야 함, Default: `True`)
        - stop_prev_model: (optional) (bool) 업그레이드 완료 후 `prev_model` 의 모델 서버를 중단할지 여부 (Default: `True`)

        ## Example

        ```python
        prev_model = model_client.get_automl_model(name=model_name, version=prev_model_version)
        next_model = model_client.get_automl_model(name=model_name, version=next_model_version)

        automl_helper.upgrade_deployment(prev_model=prev_model, next_model=next_model)
        ```
        """

        def _wait_cache_update():
            time.sleep(60)

        if not self.__model_client.get_automl_model_server_handler(next_model):
            if copy_handler:
                prev_handler = self.__model_client.get_automl_model_server_handler(prev_model)
                if prev_handler:
                    self.__model_client.update_automl_model_server_handler(next_model, prev_handler)
                else:
                    raise Exception(
                        f"'prev_model'에 예측 결과 처리 로직이 등록되어 있지 않습니다 ({prev_model.name} {prev_model.version})."
                    )

            else:
                raise Exception(f"예측 결과 처리 로직이 등록되지 않은 모델입니다 ({next_model.name} {next_model.version}).")

        ams_status = self.__model_client.get_automl_model_server_status(model=next_model)

        start_model = False

        if ams_status in ["STOPPING"]:
            raise Exception(
                f"'{ams_status}' 상태의 모델을 사용할 수 없습니다. 잠시 후 다시 시도해주세요 ({next_model.name} {next_model.version})."
            )
        elif ams_status in ["STOPPED", "FAILED", "UNKNOWN"]:
            self.__model_client.start_automl_model_server(model=next_model)
            time.sleep(60)
            ams_status = self.__model_client.get_automl_model_server_status(model=next_model)
            start_model = True

        wait_tic = 0

        while ams_status == "STARTING" and wait_tic <= 120:
            time.sleep(10)
            wait_tic += 1
            ams_status = self.__model_client.get_automl_model_server_status(model=next_model)

        if ams_status in ["STARTING", "STOPPED"]:
            raise Exception(f"AutoML 모델 동작 Timeout 발생 ({next_model.name} {next_model.version}).")

        elif ams_status in ["FAILED", "UNKNOWN"]:
            raise Exception(f"AutoML 모델 동작 실패: {ams_status} ({next_model.name} {next_model.version}).")

        if start_model:
            _wait_cache_update()

        buckets = self.__experiment_client.migrate_bucket(
            prev_model=prev_model,
            next_prediction_type="automl",
            next_model=next_model,
        )

        if stop_prev_model:
            self.__model_client.stop_automl_model_server(model=prev_model)

        return buckets
