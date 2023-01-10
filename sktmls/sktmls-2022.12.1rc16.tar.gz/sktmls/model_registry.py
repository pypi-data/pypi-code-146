import json
import os
import shlex
import subprocess
from pathlib import Path
from shutil import copyfile
from typing import List, TYPE_CHECKING

import joblib
import torch

from sktmls import MLSENV, MLSRuntimeENV, MLSClientError
from sktmls.config import Config

if TYPE_CHECKING:
    from sktmls.models import MLSModel, MLModelClient, ManualModel

MLS_MODEL_DIR = Path.home().joinpath("models")
MODEL_BINARY_NAME = "model.joblib"
MODEL_META_NAME = "model.json"
PYTORCH_BINARY_NAME = "torch_model.pth"
BUCKET = "mls-model-registry"


class ModelRegistryError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ModelRegistry:
    """
    모델 레지스트리 클래스입니다.
    """

    def __init__(self, env: MLSENV = None, runtime_env: MLSRuntimeENV = None):
        """
        ## Args

        - env: (`sktmls.MLSENV`) 접근할 MLS 환경 (`sktmls.MLSENV.DEV`|`sktmls.MLSENV.STG`|`sktmls.MLSENV.PRD`) (기본값: `sktmls.MLSENV.STG`)
        - runtime_env: (`sktmls.MLSRuntimeENV`) 클라이언트가 실행되는 환경 (`sktmls.MLSRuntimeENV.YE`|`sktmls.MLSRuntimeENV.EDD`|`sktmls.MLSRuntimeENV.LOCAL`) (기본값: `sktmls.MLSRuntimeENV.LOCAL`)

        아래의 환경 변수가 정의된 경우 해당 파라미터를 생략 가능합니다.

        - $MLS_ENV: env
        - $AWS_ENV: env
        - $MLS_RUNTIME_ENV: runtime_env

        ## Returns
        `sktmls.ModelRegistry`

        ## Example

        ```python
        model_registry = ModelRegistry(env=MLSENV.STG, runtime_env=MLSRuntimeENV.LOCAL)
        ```
        """
        if env:
            assert env in MLSENV.list_items(), "Invalid environment."
            self.__env = env
        elif os.environ.get("MLS_ENV"):
            self.__env = MLSENV[os.environ["MLS_ENV"]]
        elif os.environ.get("AWS_ENV"):
            self.__env = MLSENV[os.environ["AWS_ENV"]]
        else:
            self.__env = MLSENV.STG

        if runtime_env:
            assert runtime_env in MLSRuntimeENV.list_items(), "Invalid environment."
            self.__runtime_env = runtime_env
        elif os.environ.get("MLS_RUNTINE_ENV"):
            self.__runtime_env = MLSRuntimeENV[os.environ["MLS_RUNTINE_ENV"]]
        else:
            __HOSTNAME = os.environ.get("HOSTNAME", "").lower()
            if __HOSTNAME.startswith("bdp-dmi"):
                self.__runtime_env = MLSRuntimeENV.YE
            elif __HOSTNAME.startswith("vm-skt"):
                self.__runtime_env = MLSRuntimeENV.EDD
            else:
                self.__runtime_env = MLSRuntimeENV.LOCAL

        self.config = Config(self.__runtime_env.value)

    def save(self, mls_model: "MLSModel", force: bool = False, custom_predict_async_path: str = None) -> None:
        """
        모델 바이너리(model.joblib)와 정보(model.json)를 MLS 모델 레지스트리에 등록합니다.

        `sktmls.models.MLSModel.save`와 동일하게 동작합니다.

        ## Args

        - mls_model: (`sktmls.models.MLSModel`) 모델 객체
        - force: (optional) (bool) 이미 모델 레지스트리에 등록된 경우 덮어 쓸 것인지 여부 (기본값: `False`)
        - custom_predict_async_path: (optional) (str) predict_async.py 파일 경로 (기본값: None)

        ## Example

        ```python
        model_registry = ModelRegistry(env=MLSENV.STG)
        model_registry.save(gbm_model)
        ```
        """
        model_path = MLS_MODEL_DIR.joinpath(mls_model.model_name, mls_model.model_version)
        model_binary_path = model_path.joinpath(MODEL_BINARY_NAME)
        model_meta_path = model_path.joinpath(MODEL_META_NAME)

        if self.config.MLS_RUNTIME_ENV != "LOCAL" and mls_model.model_lib == "autogluon":
            mls_model.set_mms_path()

        model_path.mkdir(parents=True, exist_ok=True)
        if mls_model.model_lib == "pytorch":
            models = mls_model.models

            pytorch_binary_path = model_path.joinpath(PYTORCH_BINARY_NAME)
            torch.jit.ScriptModule.save(mls_model.models[0], pytorch_binary_path)
            mls_model.models = None

            joblib.dump(mls_model, model_binary_path)
            mls_model.models = models
        elif hasattr(mls_model, "custom_predict_async"):
            custom_predict_async = mls_model.custom_predict_async
            mls_model.custom_predict_async = None
            joblib.dump(mls_model, model_binary_path)
            mls_model.custom_predict_async = custom_predict_async
        else:
            joblib.dump(mls_model, model_binary_path)

        with model_meta_path.open("w") as f:
            json.dump(
                {
                    "name": mls_model.model_name,
                    "version": mls_model.model_version,
                    "model_lib": mls_model.model_lib,
                    "model_lib_version": mls_model.model_lib_version,
                    "model_data": f"/models/{mls_model.model_name}/{mls_model.model_version}/{MODEL_BINARY_NAME}",
                    "features": mls_model.features,
                    "class": mls_model.__class__.__name__,
                    "metric": getattr(mls_model, "metric", None),
                    "performance": getattr(mls_model, "performance", None),
                    "feature_importance": getattr(mls_model, "feature_importance", None),
                    "model_info": getattr(mls_model, "model_info", None),
                },
                f,
            )

        if custom_predict_async_path:
            copyfile(custom_predict_async_path, str(model_path.joinpath("predict_async.py")))

        if self.config.MLS_RUNTIME_ENV == "LOCAL":
            return

        s3_path = BUCKET
        if self.__env in (MLSENV.STG, MLSENV.PRD):
            s3_path = f"{BUCKET}-{self.__env.value}"
        s3_path = f"{s3_path}/{mls_model.model_name}"

        force_option = "-f" if force else ""

        process_mkdir = subprocess.Popen(
            shlex.split(f"hdfs dfs {self.config.HDFS_OPTIONS} -mkdir -p s3a://{s3_path}"),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        process_mkdir.wait()
        if process_mkdir.returncode != 0:
            raise ModelRegistryError(f"{mls_model.model_name}/{mls_model.model_version}: S3 폴더 생성에 실패했습니다.")

        process_put = subprocess.Popen(
            shlex.split(f"hdfs dfs {self.config.HDFS_OPTIONS} -put {force_option} {model_path} s3a://{s3_path}"),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        process_put.wait()
        if process_put.returncode != 0:
            raise ModelRegistryError(f"{mls_model.model_name}/{mls_model.model_version}: S3 복사가 실패했습니다.")

        if mls_model.model_lib == "autogluon":
            mls_model.set_local_path()

    def save_and_deploy(
        self,
        mls_model: "MLSModel",
        ml_model_client: "MLModelClient",
        force: bool = False,
        custom_predict_async_path: str = None,
    ) -> "ManualModel":
        """
        모델 바이너리(model.joblib)와 정보(model.json)를 MLS 모델 레지스트리에 등록하고, 해당 바이너리를 참조하는 MLS의 일반 모델(ManualModel)을 생성(deploy)합니다.

        일반 모델은 deploy 후 버킷에 연결되어 정상 동작하기 까지 약 한 시간이 소요됩니다.

        ## Args

        - mls_model: (`sktmls.models.MLSModel`) 모델 객체
        - ml_model_client: (`sktmls.models.MLModelClient`) 모델 클라이언트
        - force: (bool) 이미 모델 레지스트리에 등록된 경우 덮어 쓸 것인지 여부 (기본값: `False`)
        - custom_predict_async_path: (optional) (str) predict_async.py 파일 경로 (기본값: None)

        ## Example

        ```python
        ml_model_client = MLModelClient(env=MLSENV.STG, runtime_env=MLSRuntimeENV.YE, username="mls_account", password="mls_password")
        model_registry = ModelRegistry(env=MLSENV.STG)
        model_registry.save_and_deploy(gbm_model, ml_model_client)
        ```
        """
        self.save(mls_model, custom_predict_async_path=custom_predict_async_path, force=force)

        try:
            return ml_model_client.create_manual_model(
                name=mls_model.model_name,
                version=mls_model.model_version,
                model_lib=mls_model.model_lib,
                model_data=f"/models/{mls_model.model_name}/{mls_model.model_version}/model.joblib",
                features=",".join(mls_model.features),
                model_meta={
                    "name": mls_model.model_name,
                    "version": mls_model.model_version,
                    "model_lib": mls_model.model_lib,
                    "model_lib_version": mls_model.model_lib_version,
                    "model_data": f"/models/{mls_model.model_name}/{mls_model.model_version}/model.joblib",
                    "features": mls_model.features,
                },
            )
        except MLSClientError as e:
            if not force:
                raise e

            manual_model = ml_model_client.get_manual_model(name=mls_model.model_name, version=mls_model.model_version)
            return ml_model_client.update_manual_model(
                manual_model=manual_model,
                model_lib=mls_model.model_lib,
                model_data=f"/models/{mls_model.model_name}/{mls_model.model_version}/model.joblib",
                features=",".join(mls_model.features),
                model_meta={
                    "name": mls_model.model_name,
                    "version": mls_model.model_version,
                    "model_lib": mls_model.model_lib,
                    "model_lib_version": mls_model.model_lib_version,
                    "model_data": f"/models/{mls_model.model_name}/{mls_model.model_version}/model.joblib",
                    "features": mls_model.features,
                },
            )

    def list_models(self) -> List[str]:
        """
        MLS 모델 레지스트리에 등록된 모든 모델 이름을 리스트로 가져옵니다.

        ## Returns
        list(str)

        ## Example

        ```python
        model_registry = ModelRegistry(env=MLSENV.STG)
        model_names = model_registry.list_models()
        ```
        """
        if self.config.MLS_RUNTIME_ENV == "LOCAL":
            return [x.name for x in MLS_MODEL_DIR.iterdir() if x.is_dir()]

        s3_path = BUCKET
        if self.__env in (MLSENV.STG, MLSENV.PRD):
            s3_path = f"{BUCKET}-{self.__env.value}"

        s3_path = f"s3a://{s3_path}/"
        process = subprocess.Popen(
            shlex.split(f"hdfs dfs {self.config.HDFS_OPTIONS} -ls {s3_path}"),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        process.wait()
        if process.returncode != 0:
            raise ModelRegistryError(f"Listing models in ({s3_path}) is FAILED.")

        output = [row.split(s3_path)[-1] for row in process.stdout.read().decode().split("\n") if s3_path in row]
        return output

    def list_versions(self, model_name: str) -> List[str]:
        """
        MLS 모델 레지스트리에 등록된 모델의 모든 버전을 리스트로 가져옵니다.

        ## Args

        - model_name: (str) 모델 이름

        ## Returns
        list(str)

        ## Example

        ```python
        model_registry = ModelRegistry(env=MLSENV.STG)
        model_versions = model_registry.list_versions("hello_model")
        ```
        """
        if self.config.MLS_RUNTIME_ENV == "LOCAL":
            return [x.name for x in MLS_MODEL_DIR.joinpath(model_name).iterdir() if x.is_dir()]

        s3_path = BUCKET
        if self.__env in (MLSENV.STG, MLSENV.PRD):
            s3_path = f"{BUCKET}-{self.__env.value}"
        s3_path = f"s3a://{s3_path}/{model_name}/"

        process = subprocess.Popen(
            shlex.split(f"hdfs dfs {self.config.HDFS_OPTIONS} -ls {s3_path}"),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        process.wait()
        if process.returncode != 0:
            raise ModelRegistryError(f"Listing versions in ({s3_path}) is FAILED.")

        output = [row.split(s3_path)[-1] for row in process.stdout.read().decode().split("\n") if s3_path in row]
        return output

    def load(self, model_name: str, model_version: str) -> "MLSModel":
        """
        MLS 모델 레지스트리로부터 모델 객체를 가져옵니다.

        ## Args
        - model_name: (str) 모델 이름
        - model_version: (str) 모델 버전

        ## Returns
        `sktmls.models.MLSModel`

        ## Example

        ```python
        model_registry = ModelRegistry(env=MLSENV.STG)
        hello_model_v1 = model_registry.load(model_name="hello_model", model_version="v1")
        results = hello_model_v1.predict([1, 2, 3])
        ```
        """
        model_path = MLS_MODEL_DIR.joinpath(model_name, model_version)
        model_name_path = MLS_MODEL_DIR.joinpath(model_name)
        model_binary_path = model_path.joinpath(MODEL_BINARY_NAME)
        pytorch_binary_path = model_path.joinpath(PYTORCH_BINARY_NAME)

        if self.config.MLS_RUNTIME_ENV == "LOCAL":
            mls_model = joblib.load(model_binary_path)
            if mls_model.model_lib == "autogluon":
                mls_model.set_local_path()
            elif mls_model.model_lib == "pytorch":
                mls_model.models = [torch.jit.load(pytorch_binary_path)]

            return mls_model

        s3_path = BUCKET
        if self.__env in (MLSENV.STG, MLSENV.PRD):
            s3_path = f"{BUCKET}-{self.__env.value}"
        s3_path = f"s3a://{s3_path}/{model_name}/{model_version}"

        model_name_path.mkdir(parents=True, exist_ok=True)

        process = subprocess.Popen(
            shlex.split(f"hdfs dfs {self.config.HDFS_OPTIONS} -get -f {s3_path} {model_name_path}"),
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE,
        )
        process.wait()
        if process.returncode != 0:
            raise ModelRegistryError(f"{model_name}/{model_version}: 모델 가져오기가 실패했습니다.")

        mls_model = joblib.load(model_binary_path)
        if mls_model.model_lib == "autogluon":
            mls_model.set_local_path()
        elif mls_model.model_lib == "pytorch":
            mls_model.models = [torch.jit.load(pytorch_binary_path)]

        if hasattr(mls_model, "custom_predict_async"):
            mls_model.load_custom_predict_async()

        return mls_model
