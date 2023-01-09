import json
import boto3
from shutil import copyfile


import cloudpickle
from botocore.exceptions import ClientError
from mlops_sdk.config import Config
from mlops_sdk.mlops_client import MlopsError
from mlops_sdk.ml import MlopsModel

from pathlib import Path
import hvac


def get_secrets(mount_point, path, parse_data=True):
    vault_client = hvac.Client()
    data = vault_client.secrets.kv.v2.read_secret_version(mount_point=mount_point, path=path)
    if parse_data:
        data = data["data"]["data"]
    return data


class ModelRegistryError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class ModelRegistry:
    """
    모델 레지스트리 클래스입니다.
    """

    def __init__(self, config: Config):
        self.config = config

        """
        ## Args

        ## Returns
        `mlops_sdk.ModelRegistry`

        ## Example

        ```python
        model_registry = ModelRegistry()
        ```
        """

    def save(self, ml_model: MlopsModel, force: bool = False, model_artifact: str = None) -> None:
        """
        모델 바이너리(model.joblib)와 정보(model.json)를 모델 레지스트리에 등록합니다.

        ## Args


        ## Example

        ```python
        model_registry = ModelRegistry()
        model_registry.save(gbm_model)
        ```
        """
        relative_path = Path("models")
        relative_path = relative_path.joinpath(ml_model.name, ml_model.version)

        path = Path.home().joinpath(relative_path)
        path.mkdir(parents=True, exist_ok=True)
        with open(path.joinpath("model.joblib"), "wb") as f:
            cloudpickle.dump(ml_model, f)

        if model_artifact:
            copyfile(model_artifact, str(path.joinpath("model.tar.gz")))

        with path.joinpath("model.json").open("w") as f:
            json.dump(
                {
                    "name": ml_model.name,
                    "version": ml_model.version,
                    "models": [m.__class__.__name__ for m in ml_model.models],
                    **ml_model.attrs,
                },
                f,
            )

        if self.config.RUNTIME_ENV == "LOCAL":
            client = boto3.client("s3")
            bucket_name = None
            s3_info = get_secrets(mount_point="datafabric", path="mlops/access/data_loader")

            if self.config.ENV == "DEV":
                bucket_name = s3_info["model_registry_dev"]
            elif self.config.ENV == "STG":
                bucket_name = s3_info["model_registry_stg"]
            elif self.config.ENV == "PRD":
                bucket_name = s3_info["model_registry_prd"]
            else:
                raise MlopsError(code=400, msg=f"ENV {self.config.ENV} does not exist.")

            try:
                client.head_bucket(Bucket=bucket_name)
            except ClientError:
                raise MlopsError(code=400, msg=f"Bucket {bucket_name} does not exist.")

            model_path = f"{ml_model.name}/{ml_model.version}"

            if not force:
                paginator = client.get_paginator("list_objects_v2")
                for response in paginator.paginate(Bucket=bucket_name, Prefix=model_path):
                    if "Contents" in response:
                        raise MlopsError(code=400, msg=f"Model binary & meta files already exist on {model_path}.")

            for file_name in ["model.joblib", "model.json"]:
                try:
                    client.upload_file(
                        Filename=f"{str(path)}/{file_name}", Bucket=bucket_name, Key=f"{model_path}/{file_name}"
                    )
                except ClientError as e:
                    raise MlopsError(code=400, msg=str(e))
