import asyncio
import importlib.util
import re
from abc import ABCMeta, abstractmethod
from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict, List, Union

import autogluon.tabular.version
import catboost
import lightgbm
import torch
import xgboost

from sktmls import ModelRegistry, MLSENV, MLSRuntimeENV


class MLSModelError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class MLSModel(metaclass=ABCMeta):
    """
    MLS 모델 레지스트리에 등록되는 최상위 클래스입니다.
    """

    def __init__(self, model_name: str, model_version: str):
        assert type(model_name) == str
        assert type(model_version) == str

        if not bool(re.search("^[A-Za-z0-9_]+_model$", model_name)):
            raise MLSModelError(
                "model_name should follow naming rule. MUST be in alphabet, number, underscore and endwiths '_model'"
            )

        if not bool(re.search("^[A-Za-z0-9_]+$", model_version)):
            raise MLSModelError("model_name should follow naming rule. MUST be in alphabet, number, underscore")

        self.models = None
        self.model_name = model_name
        self.model_version = model_version
        self.model_lib = None
        self.model_lib_version = None
        self.features = None

    def save(self, env: MLSENV = None, runtime_env: MLSRuntimeENV = None, force: bool = False) -> None:
        """
        모델 바이너리(model.joblib)와 정보(model.json)를 MLS 모델 레지스트리에 등록합니다.

        `sktmls.ModelRegistry.save`와 동일하게 동작합니다.

        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.EDD`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)
        - force: (bool) 이미 모델 레지스트리에 등록된 경우 덮어 쓸 것인지 여부 (기본값: `False`)
        """
        model_registry = ModelRegistry(env=env, runtime_env=runtime_env)
        model_registry.save(self, force=force)

    @abstractmethod
    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        pass

    async def predict_async(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        return await asyncio.get_event_loop().run_in_executor(None, partial(self.predict, x=x, **kwargs))


class MLSLightGBMModel(MLSModel):
    """
    MLS 모델 레지스트리에 등록되는 단일 LightGBM 기반 상위 클래스입니다.
    """

    def __init__(self, model, model_name: str, model_version: str, features: List[str] = None):
        super().__init__(model_name, model_version)
        self.models = [model]
        self.model_lib = "lightgbm"
        self.model_lib_version = lightgbm.__version__

        if features:
            self.features = features
        else:
            raise MLSModelError("`features`가 없습니다.")


class MLSXGBoostModel(MLSModel):
    """
    MLS 모델 레지스트리에 등록되는 단일 XGBoost 기반 상위 클래스입니다.
    """

    def __init__(self, model, model_name: str, model_version: str, features: List[str]):
        super().__init__(model_name, model_version)
        self.models = [model]
        self.model_lib = "xgboost"
        self.model_lib_version = xgboost.__version__

        if features:
            self.features = features
        else:
            raise MLSModelError("`features`가 없습니다.")


class MLSCatBoostModel(MLSModel):
    """
    MLS 모델 레지스트리에 등록되는 단일 CatBoost 기반 상위 클래스입니다.
    """

    def __init__(self, model, model_name: str, model_version: str, features: List[str]):
        super().__init__(model_name, model_version)
        self.models = [model]
        self.model_lib = "catboost"
        self.model_lib_version = catboost.__version__

        if features:
            self.features = features
        else:
            raise MLSModelError("`features`가 없습니다.")


class MLSRuleModel(MLSModel):
    """
    MLS 모델 레지스트리에 등록되는 Rule 기반 상위 클래스입니다.
    """

    def __init__(self, model_name: str, model_version: str, features: List[str]):
        super().__init__(model_name, model_version)
        self.model_lib = "rule"
        self.model_lib_version = "N/A"

        if features:
            self.features = features
        else:
            raise MLSModelError("`features`가 없습니다.")


class MLSGenericModel(MLSModel):
    """
    MLS 모델 레지스트리에 등록되는 제네릭 모델 기반 상위 클래스입니다.
    """

    def __init__(
        self,
        models,
        model_name: str,
        model_version: str,
        features: List[str],
        custom_predict_async: Union[str, Callable] = None,
    ):
        assert type(models) == list, "`models`는 list 타입이어야 합니다."

        super().__init__(model_name, model_version)
        self.models = models
        self.model_lib = "etc"
        self.model_lib_version = "N/A"

        if not custom_predict_async:
            self.custom_predict_async = None
        elif isinstance(custom_predict_async, str):
            self.load_custom_predict_async(custom_predict_async)
        else:
            self.custom_predict_async = custom_predict_async

        if features:
            self.features = features
        else:
            raise MLSModelError("`features`가 없습니다.")

    def set_model_lib(self, model_lib: str):
        """
        모델이 사용한 라이브러리 정보를 세팅하기 위한 함수입니다.
        """
        self.model_lib = model_lib
        if model_lib == "lightgbm":
            self.model_lib_version = lightgbm.__version__
        elif model_lib == "catboost":
            self.model_lib_version = catboost.__version__
        elif model_lib == "xgboost":
            self.model_lib_version = xgboost.__version__
        elif model_lib == "pytorch":
            self.model_lib_version = torch.__version__
        elif model_lib == "autogluon":
            self.model_lib_version == autogluon.tabular.version.__version__
        elif model_lib == "etc" or model_lib == "rule":
            self.model_lib_version == "N/A"

    def load_custom_predict_async(self, file_path: str = None) -> Callable:
        file_path = file_path or Path.home().joinpath("models").joinpath(
            self.model_name, self.model_version, "predict_async.py"
        )
        try:
            spec = importlib.util.spec_from_file_location(f"{self.model_name}/{self.model_version}", file_path)
            m = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(m)
            self.custom_predict_async = m.predict_async
        except (FileNotFoundError, AttributeError):
            self.custom_predict_async = None

    def predict(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        return {"items": []}

    async def predict_async(self, x: List[Any], **kwargs) -> Dict[str, Any]:
        if hasattr(self, "custom_predict_async") and self.custom_predict_async is not None:
            return await self.custom_predict_async(x, **kwargs)
        return await asyncio.get_event_loop().run_in_executor(None, partial(self.predict, x=x, **kwargs))


class MLSPyTorchModel(MLSModel):
    """
    MLS 모델 레지스트리에 등록되는 단일 PyTorch 기반 상위 클래스입니다.
    """

    def __init__(self, model, model_name: str, model_version: str, features: List[str]):
        assert isinstance(model, torch.jit.ScriptModule), "`model`은 `torch.jit.ScriptMoudle` 타입이어야 합니다"
        assert torch.__version__.split("+")[0] == "1.8.1", "`torch`버전은 1.8.1 이어야 합니다."

        super().__init__(model_name, model_version)
        self.models = [model]
        self.model_lib = "pytorch"
        self.model_lib_version = torch.__version__

        if features:
            self.features = features
        else:
            raise MLSModelError("`features`가 없습니다.")
