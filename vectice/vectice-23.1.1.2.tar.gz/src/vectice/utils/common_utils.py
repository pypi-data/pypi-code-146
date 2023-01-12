from __future__ import annotations

from typing import TYPE_CHECKING

from vectice.api.json.code import CodeInput
from vectice.api.json.code_version import CodeVersionCreateBody
from vectice.models.git_version import CodeSource

if TYPE_CHECKING:
    from logging import Logger

    from vectice.api.client import Client
    from vectice.models.datasource.datawrapper import DataWrapper


def _check_code_source(client: Client, project_id: int, _logger: Logger) -> int | None:
    """
    Naive implementation that uses the commit hash to name the code. So we will only have one code version.
    Allows us to easily get the same commit and reuse it.
    """
    try:
        from git import InvalidGitRepositoryError, NoSuchPathError, Repo
    except ModuleNotFoundError as e:
        _logger.warning("The GitPython module is not installed.")
        raise ModuleNotFoundError(e)
    try:
        repository = Repo(".", search_parent_directories=True)
    except InvalidGitRepositoryError:
        _logger.warning("Extracting the git version failed as the repository is invalid.")
        return None
    except NoSuchPathError:
        _logger.warning("Extracting the git version failed as the path is not correct.")
        return None

    code = CodeSource(repository)
    git_version = code.git_version
    code_input = CodeInput(name=code.git_version.commitHash)
    try:
        code_output = client.create_code_gql(project_id, code_input)
    except Exception:
        code_output = client.get_code(code.git_version.commitHash, project_id)
        code_version_output = client.get_code_version("Version 1", code_output.id)
        _logger.warning("The code commit exists already.")
        return int(code_version_output.id)
    if code.user_declared_version:
        user_declared_version = code.user_declared_version.__dict__
    else:
        user_declared_version = {}
    code_version_body = CodeVersionCreateBody(
        action="CREATE_GIT_VERSION", gitVersion=git_version.__dict__, userDeclaredVersion=user_declared_version
    )
    code_version_output = client.create_code_version_gql(code_output.id, code_version_body)
    _logger.info("Code captured and will be linked to asset.")
    code_version_id = int(code_version_output.id)
    return code_version_id


def _check_for_code(
    data_sources: tuple[DataWrapper, DataWrapper, DataWrapper], client: Client, project_id: int, _logger: Logger
) -> int | None:
    code_version_id = None
    for dataset_source in data_sources:
        if dataset_source.capture_code:
            code_version_id = _check_code_source(client, project_id, _logger)
    return code_version_id
