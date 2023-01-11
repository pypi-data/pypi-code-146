from collections import defaultdict
from typing import Dict, Set, Union

import pydantic
from pydantic import BaseModel
import yaml

from pymbse.query.config.hash_functions import hash_dict
from pymbse.query.config.model_type import ModelType
from pymbse.query.config.notebook_script_config import (
    NotebookScriptConfig,
    RootModelMetadataForHash, GitLabConfig,
)


class DatabaseConfig(BaseModel):
    """Class storing database configuration"""

    ip: str
    port: int

    def get_ip_with_port(self):
        return "http://%s:%d" % (self.ip, self.port)


class PyMBSEConfig(BaseModel):
    """Class putting together database configuration and model configurations"""

    database: DatabaseConfig
    models: Dict[str, Union[NotebookScriptConfig, GitLabConfig]]

    @pydantic.validator("models", pre=True)
    def validate(cls, models: dict):
        models_dct = {}
        for key, value in models.items():
            if value["model_type"] == ModelType.NOTEBOOK_SCRIPT.value:
                models_dct[key] = NotebookScriptConfig(**value)
            elif value["model_type"] == ModelType.GITLAB_NOTEBOOK.value:
                models_dct[key] = GitLabConfig(**value)
        return models_dct

    def hash_root_model_metadata(self, root_model: str, input_parameters: dict, input_files: dict) -> str:
        return hash_dict(
            self.create_root_model_metadata(root_model, input_parameters, input_files).dict()
        )

    def create_root_model_metadata(
        self, root_model: str, input_parameters: dict, input_files: dict
    ) -> RootModelMetadataForHash:
        root_model_config = self.models[root_model]
        model_dependency_order_to_hash = (
            self._create_model_dependency_order_to_metadata_hash_dict(root_model)
        )
        return root_model_config.create_model_metadata().upcast_to_root(
            input_parameters, input_files, model_dependency_order_to_hash
        )

    def _create_model_dependency_order_to_metadata_hash_dict(self, root_model) -> dict:
        """Method creating a dictionary mapping from a model dependency order element to its hash

        :param root_model: name of a model for which a snapshot is hashed
        :return: a dictionary mapping from model dependency to its hash
        """
        model_dependency_dict = self._convert_model_dependency_tree_to_dict(root_model)
        model_dependency_order = convert_model_dependency_dict_to_order(
            model_dependency_dict
        )
        model_dependency_order_without_root_model = [
            mdo for mdo in model_dependency_order if mdo != root_model
        ]
        mdo_to_hash = {}
        for model_dependency in model_dependency_order_without_root_model:
            mdo_to_hash[model_dependency] = self.models[
                model_dependency
            ].hash_model_metadata()

        return mdo_to_hash

    def _convert_model_dependency_tree_to_dict(self, root_model: str) -> dict:
        """Method converting a model dependency tree given by the model configuration to a dictionary mapping tree level
        (0 being the tree root) to a list of model names at that level. The tree root is given by the model variable

        :param root_model: a model name for which the dependency tree is converted. It is the tree root.
        :return: a dictionary mapping tree level to list of models at that level
        """
        mdo_dct = defaultdict(lambda: [])

        def mdo(model: str, level: int) -> None:
            """Function converting a dependency tree into a model dependency order (mdo). The function recursively
            traverses the tree and builds a dictionary mapping tree level (0-based index, where 0 is the root) to a list
            of models at that level. Models at a given level are executed independently.

            :param model: model name for which dependencies are expanded
            :param level: tree level (0-based index, where 0 is the root)
            """
            mdo_dct[level].append(model)

            needs = self.models[model].needs
            for need in needs:
                mdo(need, level + 1)

        mdo(root_model, 0)
        return mdo_dct


def convert_model_dependency_dict_to_order(model_dependency_dict: dict) -> Set[str]:
    """Function converting a model dependency dictionary, mapping from tree level (from root to leaves) to a list of
    models at that level, to a model dependency order (mdo) represented as a set. The mdo goes from the bottom-most
    models to the root

    :param model_dependency_dict: model dependency dictionary, mapping from tree level (from root to leaves) to a list
    of models at that level
    :return: a set of models representing an mdo
    """
    model_dependency_order = set()
    for level in sorted(model_dependency_dict.keys(), reverse=True):
        model_dependency_order |= set(model_dependency_dict[level])

    return model_dependency_order


def load_pymbse_config(pymbse_config_path: str) -> PyMBSEConfig:
    """Function loading PyMBSE configuration from a YAML file

    :param pymbse_config_path: an absolute path to a query configuration
    :return: an initialized PyMBSEConfig instance
    """
    with open(pymbse_config_path) as f:
        return PyMBSEConfig(**yaml.safe_load(f))
