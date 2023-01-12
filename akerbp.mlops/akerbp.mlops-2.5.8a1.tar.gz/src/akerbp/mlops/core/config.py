# config.py
import os
import re
import traceback
from dataclasses import asdict
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any, Union

import yaml
from pydantic import FilePath
import logging
from logging import config as logging_config
from akerbp.mlops.core.exceptions import MissingMetadataError
from pydantic.dataclasses import dataclass
from akerbp.mlops.core import helpers

from akerbp.mlops.core.logger_config import LOGGING_CONFIG

logging_config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logging.captureWarnings(True)


def validate_categorical(
    setting: Union[str, None, bool], name: str, allowed: List[Optional[str]]
) -> None:
    """Helper function to validate categorical variables in the framework

    Args:
        setting (Optional[str]): variable to validate. Defaults to None
        name (str): name of the variable to validate
        allowed (List[Optional[str]]): list of allowed values for the variable.

    Raises:
        ValueError: message with the name of the invalid variable and the allowed values
    """
    if setting not in allowed:
        m = f"{name}: allowed values are {allowed}, got '{setting}'"
        raise ValueError(m)


@dataclass
class EnvVar:
    """Dataclass for keeping track of environmental variables

    Attributes:
        env (Optional[str]): environment. Defaults to None
        service_name (Optional[str]): service name. Defaults to None
        platform (Optional[str]): platform. Defaults to None
        local_deployment (Optional[Union[str, bool]]): local deployment. Defaults to False
    """

    env: Union[str, None, bool] = None
    service_name: Union[str, None, bool] = None
    platform: Union[str, None, bool] = None
    local_deployment: Optional[Union[str, bool]] = False
    testing_only: Optional[Union[str, bool]] = False

    def __post_init__(self):
        """Post initialization function of the dataclass that validates the attributes env, platform and service_name
        Allowed values for attributes:
            env: 'dev', 'test', 'prod'
            platform: 'cdf', 'local'
            service_name: 'training', 'prediction'
        """
        if self.env:
            validate_categorical(self.env, "Environment", ["dev", "test", "prod"])
        else:
            logger.warning("ENV environmental variable is not set")
        validate_categorical(self.platform, "Platform", ["cdf", "local"])
        if self.env and self.env != "dev":
            validate_categorical(
                self.service_name, "Service  name", ["training", "prediction"]
            )


def _read_env_vars() -> EnvVar:
    """
    Read environmental variables and initialize EnvVar object with those that
    were set (i.e. ignored those with None value). Note that
    Default values:
        LOCAL_DEPLOYMENT: 'False'
        DEPLOYMENT_PLATFORM: 'cdf'
        TESTING_ONLY: 'False'
    """
    envs = dict(
        env=os.getenv("ENV"),
        service_name=os.getenv("SERVICE_NAME"),
        local_deployment=os.getenv("LOCAL_DEPLOYMENT", "False"),
        platform=os.getenv("DEPLOYMENT_PLATFORM", "cdf"),
        testing_only=os.getenv("TESTING_ONLY", "False"),
    )
    envs = {k: v for k, v in envs.items() if v is not None}

    # For local testing
    if envs["local_deployment"] == "False" and envs["env"] == "dev":
        envs["platform"] = "local"

    return EnvVar(
        env=envs.get("env"),
        service_name=envs.get("service_name"),
        local_deployment=envs.get("local_deployment", "False"),
        platform=envs.get("platform"),
        testing_only=envs.get("testing_only"),
    )


envs = _read_env_vars()
envs_dic = asdict(envs)


@dataclass
class CdfKeys:
    """dataclass for keeping track of CDF keys

    Attributes:
        data (str, optional): CDF Data key. Defaults to None
        files (str, optional): CDF Files key. Defaults to None
        functions (str, optional): CDF Functions key. Defaults to None
    """

    data: Optional[str]
    files: Optional[str]
    functions: Optional[str]


_api_keys = CdfKeys(
    data=os.getenv("COGNITE_API_KEY_DATA"),
    files=os.getenv("COGNITE_API_KEY_FILES"),
    functions=os.getenv("COGNITE_API_KEY_FUNCTIONS"),
)
api_keys = asdict(_api_keys)


def update_cdf_keys(new_keys: Dict) -> None:
    """
    Update the CDF keys and assign to a global dictionary

    Args:
        new_keys (Dict): dictionary with the new keys
    """
    global api_keys
    api_keys = asdict(CdfKeys(**new_keys))


def generate_default_project_settings(
    yaml_file: Path = Path("mlops_settings.yaml"), n_models: int = 2
) -> None:
    """Generate default the mlops_settings.yaml file from a hardcoded template

    Args:
        yaml_file (Path, optional): path to the mlops_settings.yaml file. Defaults to Path("mlops_settings.yaml")
        n_models (int, optional): number of models to generate. Defaults to 2

    """
    if yaml_file.exists():
        raise Exception(f"Settings file {yaml_file} exists already.")

    default_config_template = [
        """
model_name: my_model
human_friendly_model_name: 'My model'
model_file: model_code/my_model.py
req_file: model_code/requirements.model
test_file: model_code/test_model.py
artifact_folder: artifact_folder
platform: cdf
dataset: mlops
info:
    prediction:
        description: Description prediction service for my_model
        metadata:
            required_input:
                - input_1
                - input_2
            training_wells:
                - 3/1-4
            input_types:
                - float
                - int
            units:
                - s/ft
                - 1
            output_curves:
                - output_1
            output_units:
                - s/ft
            petrel_exposure: False
            imputed: True
            num_filler: -999.15
            cat_filler: UNKNOWN
        owner: datascientist@akerbp.com
    training:
        << : *desc
        description: Description training service for my_model
        metadata:
            training_wells:
                - 3/1-4
            required_input:
                - input_1
                - input_2
            output_curves:
                - output_1
            hyperparameters:
                param1: value1
                param2: value2
                param3: value3
        owner: datascientist@akerbp.com
"""
    ]
    default_config_list = default_config_template * n_models
    default_config = "---".join(default_config_list)
    with open(yaml_file, "w") as f:
        f.write(default_config)


def validate_model_reqs(req_file: FilePath) -> None:
    # Model reqs is renamed to requirements.txt during deployment
    if req_file.name == "requirements.model":
        with req_file.open() as f:
            req_file_string = f.read()
            if "akerbp.mlops" not in req_file_string:
                m = "Model requirements should include akerbp.mlops package"
                raise Exception(m)
            if "MLOPS_VERSION" not in req_file_string:
                m = 'akerbp.mlops version should be "MLOPS_VERSION"'
                raise Exception(m)


@dataclass
class ServiceSettings:
    """dataclass for keeping track of service settings variables

    Attributes:
        model_name (str): name of the model
        human_friendly_model_name (str): human friendly name of the model, displayed on CDF
        model_file (FilePath): path to the model interface
        req_file (FilePath): path to the model requirements
        info (dict): info of the model. Defaults to None
        test_file (FilePath, optional): path to the model test suite. Defaults to None
        artifact_folder (FilePath, optional): path to the model artifacts. Defaults to None
        platform (str, optional): platform of the model. Defaults to "cdf"
        dataset (str, optional): dataset of the model. Defaults to "mlops"
        model_id (str, optional): id of the model. Defaults to None

    """

    model_name: str  # Remember to modify generate_default_project_settings()
    human_friendly_model_name: str
    model_file: FilePath  # if fields are modified
    req_file: FilePath
    info: Dict
    test_file: Optional[FilePath] = None
    artifact_folder: Optional[Path] = None
    artifact_version: Optional[int] = None
    keep_all_models: Optional[bool] = None
    models_to_keep: Optional[int] = None
    platform: str = "cdf"
    dataset: str = "mlops"
    model_id: Optional[str] = None

    def __post_init_post_parse__(self):
        """post initialization function of the dataclass that validates model requirements and deployment platform variables.
        Moreover, the model interface and test suite import paths are set as class attributes,
        as well as a dictionary containing the required files for running the model (based on deployment platform)

        Raises:
            Exception: If model name contains special characters not supported by the framework
            ValueError: If specifying a model id when deploying a training service
        """
        # Validation
        if not re.match("^[A-Za-z0-9_]*$", self.model_name):
            m = "Model name can only contain letters, numbers and underscores"
            raise Exception(m)

        validate_model_reqs(self.req_file)

        validate_categorical(self.platform, "Deployment platform", ["cdf", "local"])

        if self.model_id and envs.service_name == "training":
            raise ValueError("Unexpected model_id setting (training service)")

        # Derived fields
        if envs.env == "dev" and envs.local_deployment == "False":
            self.platform = "local"

        self.model_import_path = helpers.as_import_path(self.model_file)
        self.test_import_path = helpers.as_import_path(self.test_file)

        self.files = {
            "model code": helpers.get_top_folder(self.model_file),
            "handler": ("akerbp.mlops.cdf", "handler.py"),
            "artifact folder": self.artifact_folder,
        }


def store_service_settings(
    c: ServiceSettings, yaml_file: Path = Path("mlops_service_settings.yaml")
) -> None:
    """Store service settings in a yaml file during deployment

    Args:
        c (ServiceSettings): service settings for the model to deploy
        yaml_file (Path, optional): path to service settings. Defaults to Path("mlops_service_settings.yaml").

    """
    logger.info("Write service settings file")

    def factory(data: List[Tuple[str, Any]]) -> Dict[str, str]:
        """
        Take a list of tuples as input. Returns a suitable dictionary.
        Transforms Path objects to strings (linux style path).

        Args:
            data (List[Tuple[str, Any]]): list of tuples to transform

        Returns:
            Dict[str, str]: dictionary with the transformed paths
        """

        def path2str(x: Union[Path, str]) -> str:
            """transforms a Path to a string

            Args:
                x (Union[Path, str]): input path

            Returns:
                str: output string
            """
            if not isinstance(x, Path):
                return x
            else:
                return x.as_posix()

        d = {k: path2str(v) for k, v in data}
        return d

    service_settings = asdict(c, dict_factory=factory)
    with yaml_file.open("w") as f:
        yaml.dump(service_settings, f)


@dataclass
class ProjectSettings:
    """
    dataclass for keeping track of project settings

    Attributes:
        project_settings (List[ServiceSettings]): list of service settings
    """

    project_settings: List[ServiceSettings]


def enforce_string_values_in_function_metadata(
    project_settings: ProjectSettings,
) -> ProjectSettings:
    """The metadata field in CDF functions requires both keys and values to be strings.
    This function iterates through the metadata of each model defined in the mlops settings file,
    and enforce the values to be string (keys are strings by default)

    Args:
        project_settings (ProjectSettings): project settings for each model defined in the settings file

    Returns:
        (ProjectSettings): project settings for each model defined in the settings file
    """
    for i, model_settings in enumerate(project_settings.project_settings):
        for service in list(model_settings.info.keys()):
            metadata = model_settings.info[service]["metadata"]
            for k, v in metadata.items():
                metadata[k] = str(v)
            model_settings.info[service]["metadata"] = metadata
        project_settings.project_settings[i] = model_settings
    return project_settings


def read_project_settings(
    yaml_file: Path = Path("mlops_settings.yaml"),
) -> List[ServiceSettings]:
    """Read project settings from the mlops_setting.yaml file

    Args:
        yaml_file (Path, optional): path to mlops settings. Defaults to Path("mlops_settings.yaml").

    Returns:
        List[ServiceSettings]: list of service settings for each model specified in the settings file
    """
    logger.info("Read project settings")
    with yaml_file.open() as f:
        settings = yaml.safe_load_all(f.read())

    downstream_settings = []
    for setting in settings:
        downstream_settings.append(setting)
        valid_metadata, missing_fields = metadata_validation(settings=setting)
        if valid_metadata:
            continue
        else:
            logger.error("Invalid metadata specification")
            error_message = f"The following field(s) are missing from the metadata specification: {missing_fields}"
            raise MissingMetadataError(error_message)

    model_settings = [ServiceSettings(**s) for s in downstream_settings]
    project_settings = ProjectSettings(project_settings=model_settings)
    project_settings = enforce_string_values_in_function_metadata(project_settings)

    return project_settings.project_settings


def metadata_validation(settings: dict) -> Tuple[bool, List[str]]:
    """Checks whether the mlopds settings contains all the required fields, as specified on confluence

    Args:
        settings (dict): mlops settings as dictionary

    Returns:
        bool: whether metadata is validated
    """
    required_fields = [
        "required_input",
        "optional_input",
        "output_curves",
        "petrel_exposure",
        "keyword_arguments",
        "supports_external_retrieval",
    ]

    required_fields_petrel = [
        "petrel_template_family",
    ]

    metadata = settings["info"]["prediction"]["metadata"]
    metadata_fields = metadata.keys()

    missing_fields = []
    for field in required_fields:

        if field == "petrel_exposure":
            try:
                petrel_exposure = metadata[field]
                if petrel_exposure:
                    for petrel_field in required_fields_petrel:
                        if petrel_field not in metadata_fields:
                            missing_fields.append(petrel_field)
            except KeyError:
                pass

        if field not in metadata_fields:
            missing_fields.append(field)

    if len(missing_fields) == 0:
        return True, missing_fields
    else:
        return False, missing_fields


def read_service_settings(
    yaml_file: Path = Path("mlops_service_settings.yaml"),
) -> ServiceSettings:
    """Read service settings from the mlops_service_settings.yaml file during deployment

    Args:
        yaml_file (Path, optional): path object to settings file. Defaults to Path("mlops_service_settings.yaml").

    Returns:
        ServiceSettings: service settings for the model to deploy
    """
    logger.info("Read service settings")
    with yaml_file.open() as f:
        settings = yaml.safe_load(f.read())
    service_settings = ServiceSettings(**settings)
    return service_settings


def validate_user_settings(yaml_file: Path = Path("mlops_settings.yaml")) -> None:
    """Validate the mlops_settings.yaml file

    Args:
        yaml_file (Path, optional): path to settings file. Defaults to Path("mlops_settings.yaml").
    """
    try:
        read_project_settings(yaml_file)
        logger.info("Settings file is ok :)")
    except Exception:
        trace = traceback.format_exc()
        error_message = f"Settings file is not ok! Fix this:\n{trace}"
        logger.error(error_message)
