from abc import ABC, abstractmethod
from typing import Union

from pydantic import BaseModel

from pymbse.query.config.notebook_script_config import GitLabConfig
from pymbse.query.config.pymbse_config import NotebookScriptConfig
from pymbse.query.model_api.snapshot.model_snapshot import ModelSnapshot


class ModelAPI(BaseModel, ABC):
    root_model_config: Union[NotebookScriptConfig, GitLabConfig]
    cache_db_ip_with_port: str
    root_model_metadata_hash: str
    input_parameters: dict
    input_files: dict

    def get_figures_of_merit(self) -> dict:
        return self.execute().figures_of_merit

    def get_artefacts(self) -> dict:
        return self.execute().artefacts

    def get_artefact(self, artefact_name: str) -> str:
        model_snapshot = self.execute()
        if artefact_name not in model_snapshot.artefacts:
            print(
                "An artefact %s is missing. Returning an empty string." % artefact_name
            )
            return ""

        return model_snapshot.artefacts[artefact_name]

    @abstractmethod
    def execute(self) -> ModelSnapshot:
        """Abstract method executing a model to be implemented by subclasses."""
