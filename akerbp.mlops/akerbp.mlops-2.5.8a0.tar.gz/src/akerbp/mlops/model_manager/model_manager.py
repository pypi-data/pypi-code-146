"""Model Manager module for handling model artifacts in CDF.

This module deals with uploading, promoting and downloading of model artifacts
to/from CDF.
"""
import os
from pathlib import Path
import logging
from logging import config as logging_config
import akerbp.mlops.cdf.helpers as cdf
from akerbp.mlops.core import config
from akerbp.mlops.core.helpers import confirm_prompt
from akerbp.mlops.core.exceptions import MissingClientError
from typing import Optional, Dict, Union, Any
import pandas as pd
from shutil import unpack_archive
from akerbp.mlops.core.logger_config import LOGGING_CONFIG


logging_config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logging.captureWarnings(True)

env = config.envs.env
dataset_id = "mlops"

try:
    project_settings = config.read_project_settings()
except FileNotFoundError:
    logger.warning(
        "No 'mlops_settings.yaml' file found. You can still use model_manager, but with limited functionality."
    )
    project_settings = None


def setup(
    cdf_api_keys: Optional[Dict] = None, dataset_external_id: str = "mlops"
) -> None:
    """
    Set up the model manager. This involves setting up the CDF client and the
    dataset used to store artifacts.

    Args:
        cdf_api_keys (:obj:`dict`, optional): dictionary with cdf keys
        dataset_external_id (str): external id for the dataset (use None for no dataset)
    """
    if cdf_api_keys:
        cdf.api_keys = cdf_api_keys
    cdf.set_up_cdf_client()
    set_active_dataset(dataset_external_id)


def set_active_dataset(external_id: str) -> None:
    """
    Set current active dataset

    Args:
        external_id (str): external id for the dataset (use None for no dataset)
    """
    global dataset_id
    dataset_id = cdf.get_dataset_id(external_id)
    m = f"Active dataset: {external_id=}, {dataset_id=}"
    logger.info(m)


def upload_new_model_version(
    model_name: str, env: str, folder: Path, metadata: Dict = {}
) -> Any:
    """
    Upload a new model version. Files in a folder are archived and stored
    with external id `model_name/env/version`, where version is automatically
    increased.

    Args:
        model_name: name of the model
        env: name of the environment ('dev', 'test', 'prod')
        folder: (Path) path to folder whose content will be uploaded
        metadata: dictionary with metadata (it should not contain a 'version' key)

    Returns:
        (dict): model metadata
    """
    file_list = cdf.query_file_versions(
        external_id_prefix=f"{model_name}/{env}/",
        directory_prefix="/mlops",
        uploaded=None,  # count any file
        dataset_id=dataset_id,
    )
    if not file_list.empty:
        latest_v = file_list.metadata.apply(lambda d: int(d["version"])).max()
    else:
        latest_v = 0

    version = int(latest_v) + 1  # int64 isn't json-serializable
    if "version" in metadata:
        logger.error(
            "Metadata should not contain a 'version' key. " "It will be overwritten"
        )
    metadata["version"] = version
    external_id = f"{model_name}/{env}/{version}"

    if not isinstance(folder, Path):
        folder = Path(folder)

    folder_info = cdf.upload_folder(
        external_id=external_id,
        path=folder,
        metadata=metadata,
        target_folder="/mlops",
        dataset_id=dataset_id,
    )
    logger.info(
        f"Artifacts with {external_id=} uploaded from folder '{folder}' to {folder_info.directory} ({folder_info.name})"
    )
    return folder_info


def find_model_version(model_name: str, env: str, metadata: Dict) -> str:
    """
    Model external id is specified by the model name and the environment
    (starts with `{model_name}/{env}`), and a query to the metadata. If this is
    not enough, the latest version is chosen.

    Args:
        model_name (str): name of the model
        env (str): name of the environment ('dev', 'test', 'prod')
        metadata (dict): metadata of the model artifacts
    Returns:
        (str): external id of the model
    """
    file_list = cdf.query_file_versions(
        directory_prefix="/mlops",
        external_id_prefix=f"{model_name}/{env}",
        metadata=metadata,
        dataset_id=dataset_id,
    )

    latest_artifact_version = None
    if (n_models := file_list.shape[0]) == 0:
        message = f"No model artifacts found for model with {model_name=}, {env=} and metadata {metadata}. \
            Upload/promote artifacts or specify the correct model name before redeploying"
        raise Exception(message)
    elif n_models > 1:
        logger.info(
            f"Found {n_models} model artifact folders in {env} environment. Choosing the latest version, or the version specified in mlops_settings.yaml"
        )
        latest_artifact_version = file_list.loc[
            file_list.uploadedTime.argmax(), "externalId"
        ].split("/")[-1]
        logger.info(f"Latest artifact version found is {latest_artifact_version}")
    if project_settings is None:
        raise FileNotFoundError(
            "Missing 'mlops_settings.yaml' file, not possible to use this functionality"
        )

    for c in project_settings:
        if c.model_name == model_name:
            if c.artifact_version is not None:
                artifact_version = c.artifact_version
                if (
                    latest_artifact_version is not None
                    and artifact_version > latest_artifact_version
                ):
                    raise Exception(
                        f"Artifact version {artifact_version} is greater than the number of artifacts {n_models} in {env}. Please specify a valid artifact version"
                    )
                external_id = f"{model_name}/{env}/{artifact_version}"
                logger.info(
                    f"Deploying model with specified artifact version ({artifact_version}) to {env} environment"
                )
            else:
                external_id = str(
                    file_list.loc[file_list.uploadedTime.argmax(), "externalId"]
                )
                artifact_version = external_id.split("/")[-1]
                logger.info(
                    f"No artifact version specified in the settings. Deploying model with latest artifact version ({artifact_version}) to {env} environment"
                )
        else:
            latest_version = str(
                file_list.loc[file_list.uploadedTime.argmax(), "externalId"].split("/")[
                    -1
                ]
            )
            external_id = f"{model_name}/{env}/{latest_version}"
            continue

    return external_id


def download_model_version(
    model_name: str,
    env: str,
    folder: Union[Path, str],
    metadata: Dict = {},
    version: Optional[str] = None,
) -> str:

    """
    Download a model version to a folder. First the model's external id is found
    (unless provided by the user), and then it is downloaded to the chosen
    folder (creating the folder if necessary).

    Args:
        model_name (str): name of the model
        env (str): name of the environment ('dev', 'test', 'prod')
        folder (Union[Path,str]): path to folder where the artifacts are downloaded
        metadata (dict): metadata of the artifacts, doesn't make sense when passing a version (see next parameter)
        version (int, optional): artifact version to download from CDF
    Returns:
        (str): external id of the downloaded model artifacts
    """
    if isinstance(folder, str):
        folder = Path(folder)

    if version:
        external_id = f"{model_name}/{env}/{version}"
    else:
        external_id = find_model_version(model_name, env, metadata)

    if not folder.exists():
        folder.mkdir()
    cdf.download_folder(external_id, folder)
    logger.info(f"Downloaded model with {external_id=} to {folder}")

    return external_id


def set_up_model_artifact(artifact_folder: Path, model_name: str) -> str:
    """
    Set up model artifacts.
    When the prediction service is deployed, we need the model artifacts. These
    are downloaded, unless there's already a folder (local development
    environment only)

    Args:
        artifact_folder (Path):
        model_name: str

    Returns:
        (str): model id provided by the model manager or an existing folder in dev
    """
    if artifact_folder.exists():
        if env == "dev":
            logger.info(f"Use model artifacts in {artifact_folder=}")
            model_id = f"{model_name}/dev/1"
            return model_id
        else:
            message = f"Existing, local artifacts won't be used ({env=}). Download uploaded artifacts from CDF Files"
            logger.info(message)

    logger.info("Downloading serialized model")
    model_id = download_model_version(model_name, env, artifact_folder)
    return model_id


def get_model_version_overview(
    model_name: Optional[str] = None,
    env: Optional[str] = None,
    output_logs: bool = True,
    metadata: Dict = {},
) -> pd.DataFrame:
    """
    Get overview of model artifact versions.

    Args:
        model_name (:obj:`str`, optional): name of the model or None for any
        env (:obj:`str`, optional): name of the environment ('dev', 'test', 'prod')
        metadata (dict): artifact metadata. Defaults to an empty dictionary.

    Returns:
        (pd.DataFrame): model artifact data (external id, id, etc.)
    """
    if env is not None:
        env = env.lower()
    # All mlops files with right metadata
    file_list = cdf.query_file_versions(
        directory_prefix="/mlops",
        external_id_prefix=None,
        uploaded=None,
        metadata=metadata,
        dataset_id=dataset_id,
    )

    # query CDF based on the external id
    if model_name:
        index = file_list.externalId.str.contains(model_name + "/")
        file_list = file_list.loc[index]
    if env:
        index = file_list.externalId.str.contains("/" + env + "/")
        file_list = file_list.loc[index]
    if not dataset_id:
        index = file_list.dataSetId.isnull()
        file_list = file_list.loc[index]
    sorted_file_list = file_list.sort_values(
        by="lastUpdatedTime",
        ascending=False,
    )
    if output_logs:
        logger.info("Sorting artifacts chronologically")
        if env is None:
            logger.info("For more granular control you can specify the 'env' argument")
    return sorted_file_list


def validate_model_id(external_id: str, verbose: bool = True) -> bool:
    """
    Validate that model id follows MLOps standard: model/env/id

    Args:
        external_id (str): model id
        verbose (bool): Whether to print a warning if model id is invalid. Defaults to True.
    Returns:
        (bool): True if name is valid, False otherwise
    """
    supported_environments = ["dev", "test", "prod"]
    try:
        _, environment, version = external_id.split("/")
    except ValueError:
        if verbose:
            m = "Expected model id format: 'model/env/id'"
            logger.error(m)
        return False
    if environment not in supported_environments:
        if verbose:
            m = f"Supported environments: {supported_environments}"
            logger.error(m)
        return False
    try:
        int(version)
    except ValueError:
        if verbose:
            m = f"Version should be integer, got '{version}' instead"
            logger.error(m)
        return False
    return True


def delete_model_version(external_id: str, confirm: bool = True) -> None:
    """
    Delete a model artifact version

    Args:
        external_id (str): artifact's external id in CDF Files.
        confirm (bool): whether the user will be asked to confirm deletion. Defaults to True.
    """
    if not validate_model_id(external_id):
        raise ValueError()
    model, environment, version = external_id.split("/")
    if not cdf.file_exists(external_id, "/mlops"):
        return

    confirmed = False
    if confirm:
        question = f"Delete {model=}, {environment=}, {version=}?"
        confirmed = confirm_prompt(question)

    if not confirm or confirmed:
        cdf.delete_file(dict(external_id=external_id))


def promote_model(model_name: str, **kwargs) -> None:
    """
    Promote a model version from test to prod

    Keyword Args:
        confirm (bool): Whether to confirm the promotion, defaults to True
        version (int): Version number. Defaults to None,
            where the latest version number is queried from CDF.
    Args:
        model_name (str): name of model
    """
    version = kwargs.get("version", None)
    confirm = kwargs.get("confirm", True)
    if version is None:
        logger.info(
            "No version number specified, will query CDF for the latest version uploaded to test"
        )
        external_id_function = f"{model_name}-prediction-test"
        version = cdf.get_latest_artifact_version(external_id=external_id_function)
        logger.info(f"Latest uploaded model version in test is {version}")
    external_id = f"{model_name}/test/{version}"
    if not cdf.file_exists(external_id, "/mlops", dataset_id):
        logger.warning(
            f"Model version {external_id} doesn't exist in test, nothing to promote."
        )
        return

    confirmed = False
    if confirm:
        question = f"Promote {model_name=}, environment=test, {version=} to production?"
        confirmed = confirm_prompt(question)

    target_ext_id = f"{model_name}/prod/{version}"
    if cdf.file_exists(
        external_id=target_ext_id, directory="/mlops", dataset_id=dataset_id
    ):
        logger.info(
            f"Model version {target_ext_id} already exists in production, nothing new to promote."
        )
        return

    if not confirm or confirmed:
        try:
            client = cdf.global_client["files"]
        except KeyError as e:
            raise MissingClientError(
                "Set up model manager before promoting artifacts"
            ) from e

        old_filename = client.files.retrieve(external_id=external_id).name
        cdf.copy_file(
            external_id,
            target_ext_id,
            dataset_id=dataset_id,
            overwrite_name=True,
            name=old_filename.replace("test", "prod"),
        )


def get_latest_model_in_env(model_name: str, env: str) -> int:
    """Return the number of uploaded artifact versions for a given model in a given environment.
    Note that the output of get_model_version_overview(args) is sorted chronologically, so the first
    element is the latest

    Args:
        model_name (str): model name as specified in settings file
        env (str): environment, in {"dev", "test", "prod"}

    Returns:
        int: number of models
    """
    return int(
        get_model_version_overview(model_name=model_name, env=env)
        .externalId.iloc[0]
        .split("/")[-1]
    )


def download_deployment_folder(model_name: str, env: str, **kwargs) -> None:
    """Download deployment folder containing a subfolder with uploaded artifacts,
    model interface and test suite, also referred to as 'model code',  and requirements.
    If no version is specified, the function will extract and download the latest.

    If the 'target_path' is not specified in the kwargs,
    the resulting deployment folder is downloaded as a zip-file and unpacked as follows:

    mlops_deployment_folder/<model_name>/<env>/v<version>/*

    One can choose to ignore specific files by passing the 'files_to_ignore' kwargs
    as a list of filenames. The function will iterate through the entire tree and
    delete all files matching the elements in the list. This is particularly useful
    when wanting to call a model as a feature engineering step in another deployed model,
    and you want to speed up inference time by calling the model interface directly
    from source

    Args:
        model_name (str): model_name to download, as specified in mlops settings file.
        env (str): environment

    Keyword Args:
        version (int): version number, defaults to None (latest)
        files_to_ignore (list[str]): list of files to ignore, defaults to []
        target_path (str): relative target path of deployment folder, defaults to None
    """
    version = kwargs.get("version", None)
    files_to_ignore = kwargs.get("files_to_ignore", [])
    final_target_path = kwargs.get("target_path", None)
    if final_target_path is None:
        final_target_path = f"./mlops_deployment_folder/{model_name}/{env}/v{version}"
    latest_version = get_latest_model_in_env(model_name=model_name, env=env)
    if version is None:
        version = latest_version
        logger.info(
            f"No version number specified, downloading the latest version ({version}) by default"
        )

    if latest_version < version:
        raise ValueError(
            f"Specified version number is greater than the latest uploaded artifacts for model {model_name} in {env}"
        )
    else:
        logger.info(
            f"Downloading (zipped) deployment folder for model {model_name} in {env}, version {version}"
        )
        zipped_target_path = Path(f"{model_name}-{env}-{version}_deployment.zip")
        external_id = f"{model_name}-prediction-{env}-{version}"
        cdf.download_file(
            id=dict(id=None),
            path=zipped_target_path,
            external_id=dict(external_id=external_id),
        )
        logger.info(f"Unzipping deployment folder => '{final_target_path}' ")
        unpack_archive(filename=zipped_target_path, extract_dir=final_target_path)

        # Ignore specified files
        for file_to_ignore in files_to_ignore:
            logger.info(
                f"Removing file '{file_to_ignore}' from folder '{final_target_path}'"
            )
            path_to_ignore = os.path.join(final_target_path, file_to_ignore)
            try:
                os.remove(path_to_ignore)
            except Exception as e:
                logger.warning(f"Failed to remove file '{path_to_ignore}': {e}")
                continue

        # Delete zipped folder
        os.remove(zipped_target_path)
