from __future__ import annotations

from tcsoa.gen.Internal.Translation._2007_06.TranslationManagement import CreateDatasetOfVersionArgs, QueryTranslationRequestsArgs, QueryTranslationRequestsResponse, CreateDatasetOfVersionResponse, InsertDatasetVersionArgs, UpdateTranslationRequestResponse, UpdateTranslationRequestArgs, InsertDatasetVersionResponse
from typing import List
from tcsoa.base import TcService


class TranslationManagementService(TcService):

    @classmethod
    def insertDatasetVersion(cls, inputs: List[InsertDatasetVersionArgs]) -> InsertDatasetVersionResponse:
        """
        Insert a Dataset at a specific version.
        
        Use cases:
        When creating Datasets in the system, sometimes the versions are to be specified.  This is an important detail
        to maintain, especially during migration of external data into Teamcenter from another system.  This operation
        provides the ability to insert a Dataset at a particular version within the system which is different than the
        standard behavior provided by the Data Management Services.
        """
        return cls.execute_soa_method(
            method_name='insertDatasetVersion',
            library='Internal-Translation',
            service_date='2007_06',
            service_name='TranslationManagement',
            params={'inputs': inputs},
            response_cls=InsertDatasetVersionResponse,
        )

    @classmethod
    def queryTranslationRequests(cls, inputs: List[QueryTranslationRequestsArgs]) -> QueryTranslationRequestsResponse:
        """
        Query for ETSTranslationRequest  within the Teamcenter database
        
        Use cases:
        Instead of using saved queries to find ETSTranslationRequest objects in the system, you would use this method
        which is specific to finding ETSTranslationRequest objects.
        """
        return cls.execute_soa_method(
            method_name='queryTranslationRequests',
            library='Internal-Translation',
            service_date='2007_06',
            service_name='TranslationManagement',
            params={'inputs': inputs},
            response_cls=QueryTranslationRequestsResponse,
        )

    @classmethod
    def updateTranslationRequest(cls, inputs: List[UpdateTranslationRequestArgs]) -> UpdateTranslationRequestResponse:
        """
        Update an ETSTranslationRequest object within the Teamcenter database.  Only a few properties of the
        ETSTranslationRequest can be modified using this service.
        
        Use cases:
        When changes need to be made to an ETSTranslationRequest, this method will allow you to make changes to some
        fields of the ETSTranslationRequest object.
        """
        return cls.execute_soa_method(
            method_name='updateTranslationRequest',
            library='Internal-Translation',
            service_date='2007_06',
            service_name='TranslationManagement',
            params={'inputs': inputs},
            response_cls=UpdateTranslationRequestResponse,
        )

    @classmethod
    def createDatasetOfVersion(cls, inputs: List[CreateDatasetOfVersionArgs]) -> CreateDatasetOfVersionResponse:
        """
        Creates a new Dataset with a particular version.
        
        Use cases:
        If a Dataset does not already exist within Teamcenter and the application needs to create one at a particular
        version, this operation provides that ability.  This is a key factor when migrating data from other systems
        where the versions need to stay in sync for validation purposes.
        """
        return cls.execute_soa_method(
            method_name='createDatasetOfVersion',
            library='Internal-Translation',
            service_date='2007_06',
            service_name='TranslationManagement',
            params={'inputs': inputs},
            response_cls=CreateDatasetOfVersionResponse,
        )
