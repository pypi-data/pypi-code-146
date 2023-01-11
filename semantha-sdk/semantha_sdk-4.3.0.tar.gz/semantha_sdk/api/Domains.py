from __future__ import annotations

from semantha_sdk.model.DomainConfiguration import DomainConfiguration
from semantha_sdk.model.DomainSettings import DomainSettings
from semantha_sdk.model.Domains import Domains as _DomainsDTO, Domain as _DomainDTO
from semantha_sdk.rest.RestClient import RestClient
from semantha_sdk.response.SemanthaPlatformResponse import SemanthaPlatformResponse
from semantha_sdk.api.Documents import Documents
from semantha_sdk.api.ReferenceDocuments import ReferenceDocuments
from semantha_sdk.api.References import References
from semantha_sdk.api.DocumentAnnotations import DocumentAnnotations
from semantha_sdk.api.DocumentComparisons import DocumentComparisons
from semantha_sdk.api import SemanthaAPIEndpoint


class Domain(SemanthaAPIEndpoint):
    """ Endpoint for a specific domain.

        References: documents, documentannotations, documentcomparisons, documentclasses,
            modelclasses, modelinstances, referencedocuments, references,
            settings, stopwords, similaritymatrix, tags and validation.
    """
    def __init__(self, session: RestClient, parent_endpoint: str, domain_name: str):
        super().__init__(session, parent_endpoint)
        self._domain_name = domain_name
        self.__documents = Documents(session, self._endpoint)
        self.__document_annotations = DocumentAnnotations(session, self._endpoint)
        self.__document_comparisons = DocumentComparisons(session, self._endpoint)
        self.__reference_documents = ReferenceDocuments(session, self._endpoint)
        self.__references = References(session, self._endpoint)

    @property
    def _endpoint(self):
        return self._parent_endpoint + f"/{self._domain_name}"

    @property
    def documents(self):
        return self.__documents

    @property
    def document_annotations(self):
        return self.__document_annotations

    @property
    def reference_documents(self) -> ReferenceDocuments:
        return self.__reference_documents

    @property
    def references(self) -> References:
        return self.__references

    def get_metadata(self) -> SemanthaPlatformResponse:
        return self._session.get(f"{self._endpoint}/metadata").execute()

    def get_rule(self) -> SemanthaPlatformResponse:
        return self._session.get(f"{self._endpoint}/rules").execute()

    def get_documentclasses(self) -> SemanthaPlatformResponse:
        return self._session.get(f"{self._endpoint}/documentclasses").execute()

    def get_subclasses(self, id: str) -> SemanthaPlatformResponse:
        return self._session.get(
            f"{self._endpoint}/documentclasses/{id.lower()}/documentclasses"
        ).execute()

    def get_class_with_subclasses(self, id: str) -> SemanthaPlatformResponse:
        return self._session.get(f"{self._endpoint}/documentclasses/{id.lower()}").execute()

    def get_class_documents(self, id: str) -> SemanthaPlatformResponse:
        return self._session.get(
            f"{self._endpoint}/documentclasses/{id.lower()}/referencedocuments"
        ).execute()

    def get_configuration(self) -> DomainConfiguration:
        """Get the domain configuration"""
        return self._session.get(f"{self._endpoint}").execute().to(DomainConfiguration)

    def get_model_classes(self) -> SemanthaPlatformResponse:
        return self._session.get(f"{self._endpoint}/modelclasses").execute()

    def get_settings(self) -> DomainSettings:
        """Get the domain settings"""
        return self._session.get(f"{self._endpoint}/settings").execute().to(DomainSettings)

    def get_stopwords(self) -> list[str]:
        """Get all stopwords that are defined for the domain"""
        return self._session.get(f"{self._endpoint}/stopwords").execute().as_list()

    def get_tags(self) -> list[str]:
        """Get all tags that are defined for the domain"""
        return self._session.get(f"{self._endpoint}/tags").execute().as_list()



# TODO: Add docstrings, comments, type hints and error handling.
class Domains(SemanthaAPIEndpoint):
    """
        References:
            Specific domains by name
    """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/domains"

    def get_all(self) -> list[_DomainDTO]:
        """ Get all available domains """
        return self._session.get(self._endpoint).execute().to(_DomainsDTO).domains

    def get_one(self, domain_name: str) -> Domain:
        # Returns a Domain object for the given domainname, throws error if id doesn't exist
        return Domain(self._session, self._endpoint, domain_name)
