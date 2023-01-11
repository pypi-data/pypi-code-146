from __future__ import annotations

from semantha_sdk.rest import RestClient
from semantha_sdk.api import SemanthaAPIEndpoint
from semantha_sdk.response import SemanthaPlatformResponse
from semantha_sdk.model import Class as ClassDTO


class Class(SemanthaAPIEndpoint):
    """ Endpoint for a specific class.

        Allows for accessing class instances.
    """

    def __init__(self, session: RestClient, parent_endpoint: str, classid: str):
        super().__init__(session, parent_endpoint)
        self.__classid = classid

    @property
    def _endpoint(self):
        return self._parent_endpoint + f"/{self.__classid}"

    def get_instance(self):
        """ Get all instances of the class """
        return self.__sesssion.get(self._endpoint).execute()

    def delete_instance(self):
        """ Delete all instances of the class """
        return self.__sesssion.delete(self._endpoint).execute()


class Classes(SemanthaAPIEndpoint):
    """ Endpoint for the classes in a domain.

        References: Specific api for specific classes

    """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/classes"

    def get_classes(self) -> SemanthaPlatformResponse:
        """ Get all classes """
        return self._session.get(self._endpoint).execute()

    def post_classes(self, classes: list[ClassDTO]) -> SemanthaPlatformResponse:
        """ Create one or more classes """
        body = [_class.data for _class in classes]
        return self._session.post(self._endpoint, body).execute()

    def delete_classes(self) -> SemanthaPlatformResponse:
        """ Delete all classes """
        return self._session.delete(self._endpoint).execute()

    def get_class(self, classid: str):
        """ Get a specific class by id """
        return Class(self._session, self._endpoint, classid)

    def put_class(self, _class: ClassDTO):
        """ Add a given class """
        body = _class.data
        return self._session.put(self._endpoint, body).execute()

    def delete_class(self, classid: str):
        """ Delete a class given its class id """
        return self._session.delete(self._endpoint + f"/{classid}").execute()
