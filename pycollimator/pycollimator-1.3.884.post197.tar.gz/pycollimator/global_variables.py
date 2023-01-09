import re
import typing as T

from pycollimator.log import Log


class GlobalVariables:
    """
    global variables stores information about user's authentication and the project
    folder they are currently in
    """

    _instance: "GlobalVariables" = None
    _envRegex = re.compile("https://(dev|test|app).collimator.ai")

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(GlobalVariables, cls).__new__(cls)
        return cls._instance

    def set_auth_token(self, token: str, project: str = None, api_url: str = None) -> None:
        if api_url is None:
            api_url = "https://app.collimator.ai"
        self.auth_token = token
        self.project = project
        self.api_url = api_url
        Log.trace("auth_token:", self.auth_token, "project:", self.project, "api_url:", self.api_url)

    @classmethod
    def _get_instance(cls) -> "GlobalVariables":
        if cls._instance is None:
            cls()
        return cls._instance

    @classmethod
    def project_uuid(cls):
        """
        stores the project uuid associated with the folder.
        """
        return cls._get_instance().project

    @classmethod
    def token(cls):
        """
        stores the authentication token
        """
        return cls._get_instance().auth_token

    @classmethod
    def url(cls):
        """
        stores the url, used for environment logic
        """
        return cls._get_instance().api_url

    @classmethod
    def custom_headers(cls) -> T.Dict[str, str]:
        """
        stores the authentication headers used in all API requests
        """
        # FIXME I think requests should be handling the content-type header for us
        custom_headers = {
            "X-Collimator-API-Token": cls._get_instance().auth_token,
            "Accept": "application/json",
            # "content-type": "application/json",
        }
        return custom_headers


def get_project_url() -> str:
    return GlobalVariables.url() + "/projects/" + GlobalVariables.project_uuid()


def set_auth_token(token: str, project_uuid: str = None, api_url: str = None) -> None:
    GlobalVariables._get_instance().set_auth_token(token, project_uuid, api_url)
