"""Exception definitions"""
from mlsteam_model_sdk.core import envs


class MLSteamException(Exception):
    def __hash__(self):
        return hash((super().__hash__(), str(self)))


class MissingConfigException(MLSteamException):
    def __init__(self) -> None:
        message = 'Config not found'
        super().__init__(message)


class InvalidConfigException(MLSteamException):
    def __init__(self, config_path: str) -> None:
        message = f'Could not access config directory at {config_path}'
        super().__init__(message)


class MissingApiTokenException(MLSteamException):
    def __init__(self):
        message = 'API token {env_api_token} is missing'
        super().__init__(
            message.format(env_api_token=envs.API_TOKEN_ENV)
        )


class InvalidApiTokenException(MLSteamException):
    def __init__(self):
        message = 'API token is invalid, make sure your API token is correct.'
        super().__init__(message)


class InvalidProjectException(MLSteamException):
    def __init__(self, puuid=None, project_name=None):
        if puuid is not None:
            message = f'Project (uuid={puuid}) is invalid or missing'
        else:
            message = f'Project (name={project_name or envs.PROJECT_ENV}) is invalid or missing'
        super().__init__(message)


class InvalidModelException(MLSteamException):
    def __init__(self, muuid=None, model_name=None):
        if muuid is not None:
            message = f'Model (uuid={muuid}) is invalid or missing'
        elif model_name is not None:
            message = f'Model (name={model_name}) is invalid or missing'
        else:
            message = 'Model is invalid or missing'
        super().__init__(message)


class InvalidModelVersionException(MLSteamException):
    def __init__(self, vuuid=None, version_name=None):
        if vuuid is not None:
            message = f'Model version (uuid={vuuid}) is invalid or missing'
        elif version_name is not None:
            message = f'Model version (name={version_name}) is invalid or missing'
        else:
            message = 'Model version is invalid or missing'
        super().__init__(message)


class ModelVersionNotFoundException(MLSteamException):
    def __init__(self, muuid=None, model_name=None, version_name=None,) -> None:
        message = f'Model version (muuid={muuid}, model_name={model_name}, version_name={version_name}) not found'
        super().__init__(message)
