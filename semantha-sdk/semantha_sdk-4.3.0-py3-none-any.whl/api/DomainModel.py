from semantha_sdk.api import SemanthaAPIEndpoint
from semantha_sdk.api.Boostwords import Boostwords
from semantha_sdk.api.Synonyms import Synonyms
from semantha_sdk.rest.RestClient import RestClient


class DomainModel(SemanthaAPIEndpoint):
    """ Endpoint for a specific domain.

        References: attributes, backups, boostwords, classes, extractors,
            formatters, instances, metadata, namedentities, regexes, relations,
            rulefunctions, rules, synonyms
    """

    def __init__(self, session: RestClient, parent_endpoint: str, domain_name: str):
        super().__init__(session, parent_endpoint)
        self._domain_name = domain_name
        self.__boostwords = Boostwords(session, self._endpoint)
        self.__synonyms = Synonyms(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + f"/{self._domain_name}"

    @property
    def boostwords(self):
        return self.__boostwords

    @property
    def synonyms(self):
        return self.__synonyms


class Domains(SemanthaAPIEndpoint):
    """
        References:
            Specific domains by name
    """
    @property
    def _endpoint(self):
        return self._parent_endpoint + "/domains"

    def get_one(self, domain_name: str) -> DomainModel:
        # Returns a Domain object for the given domainname, throws error if id doesn't exist
        return DomainModel(self._session, self._endpoint, domain_name)
