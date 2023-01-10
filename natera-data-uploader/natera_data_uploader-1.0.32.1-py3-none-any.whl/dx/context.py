import dxpy

from soyuz.configuration import Parameters
from soyuz.configuration import Settings
from soyuz.data.storages import StorageType
from soyuz.utils import UploaderException, parse_and_validate_jwt_token


class Context(object):
    def __init__(self, params, settings):
        # type: (Parameters, Settings) -> None

        self.__params = params
        self.__settings = settings
        self.__project_id = None

    def initialize(self):
        if self.__settings.get_storage() == StorageType.DNANEXUS:
            if self.__params.get_jwt_token() or self.__settings.get_jwt_token():
                if not (self.__params.get_jwt_token_public_key_path() or self.__settings.get_jwt_token_public_key_path()):
                    raise UploaderException('Please provide correct path to JWT token public key')

                jwt_token = self.__params.get_jwt_token() or self.__settings.get_jwt_token()
                jwt_token_public_key_path = self.__params.get_jwt_token_public_key_path() or self.__settings.get_jwt_token_public_key_path()

                dnanexus_token = parse_and_validate_jwt_token(jwt_token, jwt_token_public_key_path)['soyuzUploadToken']
                self.__settings.set_token(dnanexus_token)
            else:
                self.__settings.set_token(self.__params.get_token() or self.__settings.get_token())

            self.__settings.set_token(self.__settings.get_token() or self.__params.get_token())

            if not self.__settings.get_token():
                raise UploaderException("Token was not specified")

            dxpy.set_security_context({'auth_token_type': 'Bearer', 'auth_token': self.__settings.get_token()})
            projects = self._get_projects()

            size = len(projects)
            if size == 0 or size > 1:
                raise UploaderException("Auth Token must have access to exactly 1 project with UPLOAD permission.")

            self.__project_id = projects[0]
            dxpy.set_project_context(self.__project_id)
            dxpy.set_workspace_id(self.__project_id)

    def get_project_id(self):
        # type: () -> str

        return self.__project_id

    def get_settings(self):
        # type: () -> Settings

        return self.__settings

    def get_params(self):
        # type: () -> Parameters

        return self.__params

    @staticmethod
    def _get_projects():
        result = []
        try:
            for project in dxpy.bindings.search.find_projects(level='UPLOAD'):
                result.append(str(project['id']))
        except dxpy.exceptions.InvalidAuthentication:
            pass
        return result

