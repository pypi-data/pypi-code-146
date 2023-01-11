from semantha_sdk.api import SemanthaAPIEndpoint
from semantha_sdk.rest.RestClient import RestClient
from semantha_sdk.api.ExtractorTypes import ExtractorTypes
from semantha_sdk.api.MetadataTypes import MetadataTypes
from semantha_sdk.api.DomainModel import Domains

class Model(SemanthaAPIEndpoint):
    """
        api/model endpoint

        References: datatypes, domains, exctractortypes, metadatatypes
    """

    def __init__(self, session: RestClient, parent_endpoint: str):
        super().__init__(session, parent_endpoint)
        self.__model_domains = Domains(session, self._endpoint)
        self.__extractor_types = ExtractorTypes(session, self._endpoint)
        self.__metadata_types = MetadataTypes(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/model"

    @property
    def domains(self):
        return self.__model_domains

    @property
    def extractortypes(self):
        return self.__extractor_types

    @property
    def metadatatypes(self):
        return self.__metadata_types
