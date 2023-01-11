from semantha_sdk.api import SemanthaAPIEndpoint
from semantha_sdk.rest.RestClient import RestClient


class MetadataTypes(SemanthaAPIEndpoint):
    """ api/model/metadatatypes endpoint. """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/metadatatypes"

    def get_metadatatypes(self):
        pass
