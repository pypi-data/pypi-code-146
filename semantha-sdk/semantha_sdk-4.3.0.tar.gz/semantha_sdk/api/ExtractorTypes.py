from semantha_sdk.api import SemanthaAPIEndpoint
from semantha_sdk.rest.RestClient import RestClient


class ExtractorTypes(SemanthaAPIEndpoint):
    """ api/model/extractortypes endpoint. """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/extractortypes"

    def get_extractortypes(self):
        pass