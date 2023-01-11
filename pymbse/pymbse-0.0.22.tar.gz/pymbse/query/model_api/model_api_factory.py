from pymbse.query.config.model_type import ModelType
from pymbse.query.model_api.notebook_script_api import (
    NotebookModelAPI,
    ScriptModelAPI,
    NotebookScriptModelAPI,
    GitLabNotebookModelAPI,
)

model_type_to_api = {
    ModelType.NOTEBOOK: NotebookModelAPI,
    ModelType.SCRIPT: ScriptModelAPI,
    ModelType.NOTEBOOK_SCRIPT: NotebookScriptModelAPI,
    ModelType.GITLAB_NOTEBOOK: GitLabNotebookModelAPI
}
