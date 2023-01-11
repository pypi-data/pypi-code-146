import importlib
import logging
import os
import sys

import yaml

ROOT_YAML_NODE = "flavors"
FLAVOR_NAME = "python_function"
MAIN = "loader_module"
CODE = "code"
DATA = "data"
ENV = "env"
PY_VERSION = "python_version"


def read_config(model_uri: str):
    config_path = os.path.join(model_uri, "MLmodel")
    with open(config_path) as fp:
        config = yaml.safe_load(fp)
    if ROOT_YAML_NODE not in config or FLAVOR_NAME not in config[ROOT_YAML_NODE]:
        raise ValueError(
            "Python model runner requires model supporting python_function flavor"
        )

    return config[ROOT_YAML_NODE][FLAVOR_NAME]


def load_model(model_uri):
    logging.getLogger(__name__).info(f"Loading model config from {model_uri}")
    conf = read_config(model_uri)
    logging.getLogger(__name__).info(f"Model configuration: {conf}")
    if CODE in conf and conf[CODE]:
        code_path = os.path.join(model_uri, conf[CODE])
        _add_code_to_system_path(code_path=code_path)
    data_path = os.path.join(model_uri,
                             conf[DATA]) if (DATA in conf) else model_uri

    # Needed when loading spark models, we have seen that the logger is very noisy for these
    # specific components.
    logging.getLogger('pyspark').setLevel(logging.ERROR)
    logging.getLogger('py4j').setLevel(logging.ERROR)
    logging.getLogger('py4j.java_gateway').setLevel(logging.ERROR)

    # In some deployments, user or library code (ie. pyspark) may create temp files which by
    # default are created at /tmp/... which might not have all permissions available. This dir
    # seems to solve problems associated with that.
    temp_dir_for_model_runner = "/tmp/model_runner_temp"
    os.makedirs(temp_dir_for_model_runner, exist_ok=True)
    os.environ["TMPDIR"] = temp_dir_for_model_runner
    logging.getLogger(__name__).info(
        f"Set temp file dir to: {temp_dir_for_model_runner}."
    )

    logging.getLogger(__name__).info(f"Loading the model module: {conf[MAIN]}.")
    module = importlib.import_module(conf[MAIN])
    # In case we are reloading the model from an interactive kernel like a notebook,
    # we'd want to reload the module to make sure we pick up on any new changes.
    module = importlib.reload(module)
    logging.getLogger(__name__).info(
        f"Loading the model pyfunc with data path: {data_path}."
    )
    return module._load_pyfunc(data_path)


def _add_code_to_system_path(code_path):
    sys.path = [code_path] + _get_code_dirs(code_path) + sys.path


def _get_code_dirs(src_code_path, dst_code_path=None):
    """
    Obtains the names of the subdirectories contained under the specified source code
    path and joins them with the specified destination code path.

    :param src_code_path: The path of the source code directory for which to list subdirectories.
    :param dst_code_path: The destination directory path to which subdirectory names should be
                          joined.
    """
    if not dst_code_path:
        dst_code_path = src_code_path
    return [
        (os.path.join(dst_code_path, x))
        for x in os.listdir(src_code_path)
        if os.path.isdir(x) and not x == "__pycache__"
    ]
