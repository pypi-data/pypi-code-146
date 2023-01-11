from __future__ import annotations

from dataclasses import dataclass
import logging
import os
import shutil
import sys
import tempfile
from typing import List, Optional, Sequence
import zipfile

import click
import yaml

from truera.client.cli.cli_utils import ModelType
from truera.client.errors import DirectoryAlreadyExistsException
from truera.client.errors import FileDoesNotExistException
from truera.client.errors import InvalidFrameworkWrapperException
from truera.client.errors import MissingEnvironmentSpecException
from truera.client.errors import PackageVerificationException
from truera.client.util.conda_template import CondaTemplate
from truera.client.util.DataRobotMLmodelTemplate import \
    DataRobotMLmodelTemplate
from truera.client.util.H2oMLmodelTemplate import H2oMLmodelTemplate
from truera.client.util.MLeapMLmodel_template import MLeapMLmodelTemplate
from truera.client.util.PmmlMLmodel_template import PmmlMLmodelTemplate
from truera.client.util.PythonMLmodel_template import PythonMLmodelTemplate
from truera.utils.package_requirement_utils import get_module_version
from truera.utils.package_requirement_utils import model_runner_ml_requirements
from truera.utils.package_requirement_utils import sdk_packaging_requirements


class FrameworkSupportSpec:

    def __init__(
        self, name, root_framework, output_kinds, is_framework,
        supports_transform
    ):
        super().__init__()
        self.name = name
        self.root_framework = root_framework
        self.output_kinds = output_kinds
        self.is_framework = is_framework
        self.supports_transform = supports_transform


class PipDependencyParser:

    def __init__(self, pip_dep_list: Optional[Sequence[str]]):
        self.pip_dep_list = pip_dep_list
        if self.pip_dep_list is None:
            self.pip_dep_list = []
        self._parse_pip_deps()

    def _parse_pip_deps(self):
        self._package_name_to_version = {}
        if not isinstance(self.pip_dep_list, list):
            raise ValueError("Pip dependencies must be a list of strings!")
        for dep_str in self.pip_dep_list:
            dep_str_sliced = dep_str.split("==")
            if len(dep_str_sliced) != 2:
                raise ValueError(
                    f"Pip dependencies must be a list of strings of the form <PACKAGE_NAME>==<VERSION_NUMBER>! Provided dependencies: {self.pip_dep_list}"
                )
            package_name, version = dep_str_sliced
            package_name = package_name.strip()
            version = version.strip()
            self._check_if_conflicting_dependency(package_name, version)
            self._package_name_to_version[package_name] = version

    def get_package_names(self) -> Sequence[str]:
        return list(self._package_name_to_version.keys())

    def get_dependencies(self) -> Sequence[str]:
        return sorted(self.pip_dep_list)

    def _check_if_conflicting_dependency(self, package_name: str, version: str):
        if package_name in self._package_name_to_version and version != self._package_name_to_version[
            package_name]:
            raise ValueError(
                f"Multiple specified dependencies with package name {package_name}!"
            )

    def add_dependency(self, package_name: str, version_number: str):
        self._check_if_conflicting_dependency(package_name, version_number)
        self.pip_dep_list.append(f"{package_name}=={version_number}")
        self._package_name_to_version[package_name] = version_number

    def add_default_model_runner_dependencies(self):
        required_pkgs = model_runner_ml_requirements(
        ) + sdk_packaging_requirements()
        for pkg in required_pkgs:
            if pkg.package_name in self.get_package_names():
                continue
            version_str = get_module_version(pkg.package_name)
            if version_str:
                self.add_dependency(pkg.package_name, version_str)

    @staticmethod
    def parse_from_string(dep_str: str) -> PipDependencyParser:
        if dep_str is None:
            dep_str = ""
        dep_str = dep_str.strip()
        if not dep_str:
            return PipDependencyParser([])
        return PipDependencyParser([d.strip() for d in dep_str.split(",")])


# Frameworks and the underlying framework who's wrapper they share.
# To add a new framework, add a new entry and add a new framework wrapper file if the value
# is unique.
BUILT_IN_FRAMEWORK_WRAPPER_MAP = {
    "sklearn":
        FrameworkSupportSpec("sklearn", "sklearn",
                             ["classification", "regression"], True, True),
    "sklearn_pipeline":
        FrameworkSupportSpec("sklearn_pipeline", "sklearn_pipeline",
                             ["classification", "regression"], True, True),
    "sklearn_pipeline_xgb":
        FrameworkSupportSpec("sklearn_pipeline_xgb", "sklearn_pipeline_xgb",
                             ["classification", "regression"], True, True),
    "xgboost":
        FrameworkSupportSpec("xgboost", "xgboost",
                             ["classification", "regression"], True, True),
    "lightgbm":
        FrameworkSupportSpec("lightgbm", "lightgbm",
                             ["classification", "regression"], True, True),
    "catboost":
        FrameworkSupportSpec("catboost", "catboost",
                             ["classification", "regression"], True, True),
    "tensorflow":
        FrameworkSupportSpec("tensorflow", "tensorflow", ["classification"],
                             True, False),
    "pytorch":
        FrameworkSupportSpec("pytorch", "pytorch", ["classification"], True, False),
    "pyspark":
        FrameworkSupportSpec("pyspark", "pyspark",
                             ["classification", "regression"], True, False),
    "truera_pred_func":
        FrameworkSupportSpec("truera_pred_func", "truera_pred_func",
                             ["classification", "regression"], False, True),
    "custom_template":  # Template wrapper that can be provided to users creating a custom wrapper
        FrameworkSupportSpec("custom_template", "custom_template",
                             ["classification", "regression"], False, True)
}

BUILT_IN_FRAMEWORK_WRAPPER_LIST = [
    key for key in BUILT_IN_FRAMEWORK_WRAPPER_MAP.keys()
    if BUILT_IN_FRAMEWORK_WRAPPER_MAP[key].is_framework
]


@dataclass
class ModelFile:
    file_path: str
    relative_dir_in_code: str


def _get_file_name_from_path(path: str):
    head, tail = os.path.split(path)
    return tail or os.path.basename(head)


def check_output_dir_does_not_exist(output_dir: str):
    if os.path.isdir(output_dir):
        message = "The provided output directory already exists: " + output_dir + ". Please specify a new directory."
        raise DirectoryAlreadyExistsException(message)


def get_model_data_field(model_path, given_file_name):
    if given_file_name:
        return given_file_name
    if os.path.isfile(model_path):
        return _get_file_name_from_path(model_path)
    return "data"


def prepare_python_model_folder(
    model_file_path: str,
    output_dir: str,
    framework_wrapper: str,
    model_output_type: str,
    conda_file: str,
    dependencies: str,
    pip_dependencies: PipDependencyParser,
    *,
    pip_requirements_file: Optional[str] = None,
    python_version: Optional[str] = None,
    pip_version: Optional[str] = None,
    model_data_file_name: Optional[str] = None,
    model_code_files: Optional[List[ModelFile]] = None,
    logger: Optional[logging.Logger] = None,
    transform_file_path: Optional[str] = None
):
    model_data_file_name = get_model_data_field(
        model_file_path, model_data_file_name
    )
    if model_code_files is None:
        model_code_files = []
    if framework_wrapper.lower() not in BUILT_IN_FRAMEWORK_WRAPPER_MAP.keys():
        if not os.path.isfile(framework_wrapper):
            message = "Framework wrapper was not in the built in list or a valid path: " + framework_wrapper
            raise InvalidFrameworkWrapperException(message)
    elif model_output_type not in BUILT_IN_FRAMEWORK_WRAPPER_MAP[
        framework_wrapper.lower()].output_kinds:
        message = "Built in wrappers do not support the framework, output type combination of: " + framework_wrapper + ", " + model_output_type
        raise InvalidFrameworkWrapperException(message)
    if not os.path.isfile(model_file_path
                         ) and not os.path.isdir(model_file_path):
        message = "Specified path to model file is not a valid path: " + model_file_path
        raise FileDoesNotExistException(message)
    if transform_file_path:
        if not os.path.isfile(transform_file_path):
            message = "Pickle file for model transform is missing."
            raise FileDoesNotExistException(message)

    set_env_specs = [
        env_spec for env_spec in
        [conda_file, dependencies or pip_dependencies, pip_requirements_file]
        if (env_spec is not None)
    ]

    # none provided
    if len(set_env_specs) == 0:
        message = "No environment specification provided. Please provide a conda file or dependencies or pip dependencies or pip requirements file."
        raise MissingEnvironmentSpecException(message)

    # > 1 of dependencies, conda file, and pip_requirements_file were set - warn
    if len(set_env_specs) > 1:
        click.echo(
            "Warning: More than one environment specification provided from [conda file, pip requirements file, (dependencies, pip_dependencies)]. Defaulting to on option in the order: conda file, pip requirements file, dependencies & pip dependencies."
        )

    if conda_file and not os.path.isfile(conda_file):
        message = "Specified path to conda file is not a valid path: " + conda_file
        raise FileDoesNotExistException(message)

    if pip_requirements_file and not os.path.isfile(pip_requirements_file):
        message = "Specified path to pip requirements file is not a valid path: " + pip_requirements_file
        raise FileDoesNotExistException(message)

    check_output_dir_does_not_exist(output_dir)

    # We want to create the output directory with the following format:
    # output_dir/
    # |--MLmodel
    # |--model.pkl or `model_data_file_name`
    # |--conda.yaml
    # |--code/
    #    |--<framework>_predict_wrapper.py
    #    |-- other code dependencies required to run the model

    # First, create output_dir and output_dir/code - will fail if it already exists.
    # It's important to do any checks for failures before this so that we don't
    # create the folder if we're going to fail since the user will have to manually
    # delete the folder after we create the folder.
    code_dir = os.path.join(output_dir, "code")
    os.makedirs(code_dir, exist_ok=False)

    # Copy the pickle file into output_dir
    if os.path.isfile(model_file_path):
        shutil.copyfile(
            model_file_path, os.path.join(output_dir, model_data_file_name)
        )
    # checked that it is a file or a dir above, so this case is dir
    else:
        shutil.copytree(model_file_path, os.path.join(output_dir, "data"))

    # Copy the transformer pickle file into output_dir
    if transform_file_path:
        shutil.copyfile(
            transform_file_path, os.path.join(output_dir, "transformer.pkl")
        )

    # Copy the right wrapper file into the code directory
    # In the future we'll need to support a way to specify this file.
    wrapper_source = None
    wrapper_file_name = None

    if framework_wrapper in BUILT_IN_FRAMEWORK_WRAPPER_MAP.keys():
        wrapper_file_suffix = "_transform" if transform_file_path and BUILT_IN_FRAMEWORK_WRAPPER_MAP[
            framework_wrapper.lower()].supports_transform else ""
        wrapper_file_suffix = wrapper_file_suffix + "_predict_wrapper.py"
        wrapper_file_source_name = BUILT_IN_FRAMEWORK_WRAPPER_MAP[
            framework_wrapper.lower()
        ].root_framework + "_" + model_output_type + wrapper_file_suffix
        wrapper_file_name = framework_wrapper + "_" + model_output_type + wrapper_file_suffix
        wrapper_source = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "util",
            wrapper_file_source_name
        )
    else:
        wrapper_file_name = _get_file_name_from_path(framework_wrapper)
        wrapper_source = framework_wrapper
    shutil.copyfile(wrapper_source, os.path.join(code_dir, wrapper_file_name))

    if model_code_files:
        for code_file in model_code_files:
            copy_dir = os.path.join(code_dir, code_file.relative_dir_in_code)
            os.makedirs(copy_dir, exist_ok=True)
            file_name = _get_file_name_from_path(code_file.file_path)
            shutil.copyfile(
                code_file.file_path, os.path.join(copy_dir, file_name)
            )

    # Build the MLmodel file
    MLmodel = PythonMLmodelTemplate(
        wrapper_file_name[:-3],
        model_data_path=model_data_file_name,
        python_version=python_version
    )

    with open(os.path.join(output_dir, "MLmodel"), "w") as fp:
        fp.write(yaml.dump(MLmodel))

    # Build the conda.yaml file
    output_conda_file = os.path.join(output_dir, "conda.yaml")
    if conda_file is not None:
        shutil.copyfile(conda_file, output_conda_file)
    else:
        if pip_requirements_file:
            with open(pip_requirements_file) as f:
                pip_dependencies = PipDependencyParser(
                    [l.strip() for l in f.readlines()]
                )
                dependencies = ""
        conda = CondaTemplate(
            dependencies,
            pip_dependencies,
            python_version=python_version,
            pip_version=pip_version
        )

        with open(output_conda_file, "w") as fp:
            fp.write(yaml.dump(conda))


def create_temp_file_path(extension: Optional[str] = None):
    # In some scenarios, we cannot use NamedTemporaryFile
    # directly as it doesn't allow second open on Windows NT.
    # So we use NamedTemporaryFile to just create a name for us
    # and let it delete the file, but use the name later.
    with tempfile.NamedTemporaryFile(mode="w+") as file:
        file_name = file.name
        if extension:
            file_name += "." + extension
    return file_name


def prepare_template_model_folder(
    output_dir: str,
    model_output_type: str,
    model_path: Optional[str] = None,
    model_code_files: Optional[Sequence[str]] = None,
    pip_dependencies: Optional[Sequence[str]] = None,
    python_version: Optional[str] = None
):
    model_data_file_name = None
    pip_dependencies = PipDependencyParser(pip_dependencies)

    if not model_path:
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as fp:
            model_path = fp.name
            model_data_file_name = "model.tmp"
            fp.write(
                "Replace this file with your serialized model and update the generated MLmodel file with the new filename."
            )

    output_conda_file = None
    if not pip_dependencies.get_dependencies():
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as fp:
            conda = CondaTemplate(
                in_dependencies=None, in_pip_dependencies=pip_dependencies
            )
            output_conda_file = fp.name
            with open(output_conda_file, "w") as fp:
                fp.write(yaml.dump(conda))
                fp.write("# Add model dependencies to this file")

    model_code_files = [
        ModelFile(file_path=code_file, relative_dir_in_code='')
        for code_file in filter(
            lambda code_file: code_file if os.path.isfile(code_file) else print(
                f"File not found at path '{code_file}'. Manually move proper file to generated directory"
            ), model_code_files
        )
    ]

    prepare_python_model_folder(
        model_file_path=model_path,
        output_dir=output_dir,
        framework_wrapper='custom_template',
        model_output_type=model_output_type,
        conda_file=output_conda_file,
        dependencies=None,
        pip_dependencies=pip_dependencies,
        python_version=python_version,
        model_data_file_name=model_data_file_name,
        model_code_files=model_code_files
    )


def prepare_data_robot_model(
    jar_path: str, model_package_id: str, output_dir: str, api_version: int,
    logger
):
    if not os.path.isfile(jar_path):
        message = "Specified path to jar file is not a valid path: " + jar_path
        raise FileDoesNotExistException(message)

    check_output_dir_does_not_exist(output_dir)

    if api_version not in [1, 2]:
        raise PackageVerificationException(
            f"DataRobot API version must be either 1 or 2! Provided version: {api_version}"
        )
    model_type = ModelType.Datarobot_v1 if api_version == 1 else ModelType.Datarobot_v2

    # We want to create the output directory with the following format:
    # output_dir/
    # |--MLmodel
    # |--<user's jar>.jar

    # First, create output_dir - will fail if it already exists.
    # It's important to do any checks for failures before this so that we don't
    # create the folder if we're going to fail since the user will have to manually
    # delete the folder after we create the folder.
    os.makedirs(output_dir, exist_ok=False)

    # Copy in the user's Jar
    jar_file_name = _get_file_name_from_path(jar_path)
    shutil.copyfile(jar_path, os.path.join(output_dir, jar_file_name))

    # Build the MLmodel file
    MLmodel = DataRobotMLmodelTemplate(
        jar_file_name, model_package_id, model_type
    )

    with open(os.path.join(output_dir, "MLmodel"), "w") as fp:
        fp.write(yaml.dump(MLmodel))


def prepare_h2o_model(jar_path, model_zip_path, output_dir, logger):
    if not os.path.isfile(jar_path):
        message = "Specified path to jar file is not a valid path: " + jar_path
        raise FileDoesNotExistException(message)

    if not os.path.isfile(model_zip_path):
        message = "Specified path to zip file is not a valid path: " + model_zip_path
        raise FileDoesNotExistException(message)

    check_output_dir_does_not_exist(output_dir)

    # We want to create the output directory with the following format:
    # output_dir/
    # |--MLmodel
    # |--h2o-genmodel.jar
    # |--<user's model zip>.zip

    # First, create output_dir - will fail if it already exists.
    # It's important to do any checks for failures before this so that we don't
    # create the folder if we're going to fail since the user will have to manually
    # delete the folder after we create the folder.
    os.makedirs(output_dir, exist_ok=False)

    # Copy in the user's Jar
    jar_file_name = "h2o-genmodel.jar"
    shutil.copyfile(jar_path, os.path.join(output_dir, jar_file_name))

    # Copy in the user's model zip
    zip_file_name = _get_file_name_from_path(model_zip_path)
    shutil.copyfile(model_zip_path, os.path.join(output_dir, zip_file_name))

    # Build the MLmodel file
    MLmodel = H2oMLmodelTemplate(zip_file_name)

    with open(os.path.join(output_dir, "MLmodel"), "w") as fp:
        fp.write(yaml.dump(MLmodel))


def prepare_pmml_model(
    pmml_file, output_field, evaluator_jar_path, model_jar_path, output_dir,
    logger
):
    if not os.path.isfile(pmml_file):
        message = "Specified path to pmml file is not a valid path: " + pmml_file
        raise FileDoesNotExistException(message)
    if not os.path.isfile(evaluator_jar_path):
        message = "Specified path to jar file is not a valid path: " + evaluator_jar_path
        raise FileDoesNotExistException(message)
    if not os.path.isfile(model_jar_path):
        message = "Specified path to jar file is not a valid path: " + model_jar_path
        raise FileDoesNotExistException(message)

    check_output_dir_does_not_exist(output_dir)

    # We want to create the output directory with the following format:
    # output_dir/
    # |--MLmodel
    # |--evaluator_jar_path.jar
    # |--model_jar_path.jar
    # |--pmml_file.pmml

    # First, create output_dir - will fail if it already exists.
    # It's important to do any checks for failures before this so that we don't
    # create the folder if we're going to fail since the user will have to manually
    # delete the folder after we create the folder.
    os.makedirs(output_dir, exist_ok=False)

    # Copy in the user's Jars
    shutil.copyfile(
        evaluator_jar_path,
        os.path.join(output_dir, _get_file_name_from_path(evaluator_jar_path))
    )
    shutil.copyfile(
        model_jar_path,
        os.path.join(output_dir, _get_file_name_from_path(model_jar_path))
    )

    # Copy the pmml file
    pmml_file_name = _get_file_name_from_path(pmml_file)
    shutil.copyfile(pmml_file, os.path.join(output_dir, pmml_file_name))

    # Build the MLmodel file
    MLmodel = PmmlMLmodelTemplate(pmml_file_name, output_field)

    with open(os.path.join(output_dir, "MLmodel"), "w") as fp:
        fp.write(yaml.dump(MLmodel))


def prepare_mleap_model(zip, folder, version, output_dir, logger):
    if not (zip and
            os.path.isfile(zip)) and not (folder and os.path.isdir(folder)):
        message = f"Provided zip ({zip}) was not a valid file and provided folder ({folder}) was not a valid directory."
        raise FileDoesNotExistException(message)

    check_output_dir_does_not_exist(output_dir)

    if zip and os.path.isfile(zip) and folder and os.path.isdir(folder):
        click.echo(
            f"Warning: both zip and directory provided, defaulting to directory."
        )

    # We want to create the output directory with the following format:
    # output_dir/
    # |--MLmodel
    # |--mleap
    #    |-- model (contains mleap contents)

    # First, create output_dir - will fail if it already exists.
    # It's important to do any checks for failures before this so that we don't
    # create the folder if we're going to fail since the user will have to manually
    # delete the folder after we create the folder.
    os.makedirs(output_dir, exist_ok=False)

    output_mleap_folder = os.path.join(output_dir, "mleap", "model")

    if folder and os.path.isdir(folder):
        shutil.copytree(folder, output_mleap_folder)
    else:
        with zipfile.ZipFile(zip, 'r') as zip_ref:
            zip_ref.extractall(output_mleap_folder)

    # Build the MLmodel file
    MLmodel = MLeapMLmodelTemplate(version)

    with open(os.path.join(output_dir, "MLmodel"), "w") as fp:
        fp.write(yaml.dump(MLmodel))


def verify_python_model_folder(folder, logger=None, *, silent=False):
    if not os.path.isdir(folder):
        message = "Provided model folder is not a directory: " + folder
        raise PackageVerificationException(message)
    if not os.path.isfile(os.path.join(folder, "MLmodel")):
        message = "Provided model folder does not have a MLmodel file: " + folder
        raise PackageVerificationException(message)
    if not os.path.isfile(os.path.join(folder, "conda.yaml")):
        message = "Provided model folder does not have a conda.yaml file: " + folder
        raise PackageVerificationException(message)
    if not os.path.isdir(os.path.join(folder, "code")):
        message = "Provided model folder does not have a code directory: " + folder
        raise PackageVerificationException(message)

    wrapper_file_exists = False
    for f in os.listdir(os.path.join(folder, "code")):
        if f.endswith(".py"):
            wrapper_file_exists = True

    if not wrapper_file_exists:
        message = "Provided model folder does not have a code directory containing wrapper file: " + folder
        raise PackageVerificationException(message)

    _check_valid_yaml_file(folder, "MLmodel", logger)
    _check_valid_yaml_file(folder, "conda.yaml", logger)

    if not silent:
        click.echo("Verification Done")


def _check_valid_yaml_file(folder: str, file_name: str, logger):
    with open(os.path.join(folder, file_name), 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError:
            click.echo(file_name + " file was not valid yaml.")
            sys.exit(1)


def verify_h2o_model_folder(folder, logger, *, silent=False):
    if not os.path.isdir(folder):
        message = "Provided model folder is not a directory: " + folder
        raise PackageVerificationException(message)
    if not os.path.isfile(os.path.join(folder, "MLmodel")):
        message = "Provided model folder does not have a MLmodel file: " + folder
        raise PackageVerificationException(message)

    contains_jar = False
    contains_zip = False
    for f in os.listdir(folder):
        if f.endswith("h2o-genmodel.jar"):
            contains_jar = True
        if f.endswith(".zip"):
            contains_zip = True

    if not contains_jar:
        message = "Provided model folder does not have a h2o-genmodel.jar file: " + folder
        raise PackageVerificationException(message)

    if not contains_zip:
        message = "Provided model folder does not have a zip file: " + folder
        raise PackageVerificationException(message)

    _check_valid_yaml_file(folder, "MLmodel", logger)

    if not silent:
        click.echo("Verification Done")


def verify_datarobot_model_folder(folder, logger, *, silent=False):
    if not os.path.isdir(folder):
        message = "Provided model folder is not a directory: " + folder
        raise PackageVerificationException(message)
    if not os.path.isfile(os.path.join(folder, "MLmodel")):
        message = "Provided model folder does not have a MLmodel file: " + folder
        raise PackageVerificationException(message)

    if not any([f.endswith(".jar") for f in os.listdir(folder)]):
        message = f"Provided model folder does not have a jar file: {folder}"
        raise PackageVerificationException(message)

    model_yaml = _check_valid_yaml_file(folder, "MLmodel", logger)
    DataRobotMLmodelTemplate.validate_mlmodel_yaml(model_yaml)
    if not silent:
        click.echo("Verification Done")


def verify_pmml_model_folder(folder, logger, *, silent=False):
    if not os.path.isdir(folder):
        message = "Provided model folder is not a directory: " + folder
        raise PackageVerificationException(message)
    if not os.path.isfile(os.path.join(folder, "MLmodel")):
        message = "Provided model folder does not have a MLmodel file: " + folder
        raise PackageVerificationException(message)

    jar_files = [file for file in os.listdir(folder) if file.endswith(".jar")]
    if not len(jar_files) == 2:
        message = f"Provided model folder does not two jar files: {folder}. Provided jar files: {jar_files}. Pmml evaluator and model jars are expected."
        raise PackageVerificationException(message)

    _check_valid_yaml_file(folder, "MLmodel", logger)

    if not silent:
        click.echo("Verification Done")


def verify_mleap_model_folder(folder, logger, *, silent=False):
    if not os.path.isdir(folder):
        message = "Provided model folder is not a directory: " + folder
        raise PackageVerificationException(message)
    if not os.path.isfile(os.path.join(folder, "MLmodel")):
        message = "Provided model folder does not have a MLmodel file: " + folder
        raise PackageVerificationException(message)

    if not os.path.isdir(os.path.join(folder, "mleap")):
        message = "Provided model folder does not have a mleap directory: " + folder
        raise PackageVerificationException(message)

    _check_valid_yaml_file(folder, "MLmodel", logger)

    if not silent:
        click.echo("Verification Done")
