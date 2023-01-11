from __future__ import annotations

from tcsoa.gen.Translation._2007_06.TranslationManagement import CreateTranslationRequestArgs, CreateTranslationRequestResponse
from typing import List
from tcsoa.base import TcService


class TranslationManagementService(TcService):

    @classmethod
    def createTranslationRequest(cls, inputs: List[CreateTranslationRequestArgs]) -> CreateTranslationRequestResponse:
        """
        Create a translation request within Teamcenter for use with translation services.
        This operation creates a ETSTranslationRequest object in the Teamcenter database.    
        
        
        Use cases:
        The ETS application provides the ability to process requests in an asynchronous fashion thus removing the
        processing burden from the clients to a provisioned machine dedicated to processing these requests.
        """
        return cls.execute_soa_method(
            method_name='createTranslationRequest',
            library='Translation',
            service_date='2007_06',
            service_name='TranslationManagement',
            params={'inputs': inputs},
            response_cls=CreateTranslationRequestResponse,
        )
