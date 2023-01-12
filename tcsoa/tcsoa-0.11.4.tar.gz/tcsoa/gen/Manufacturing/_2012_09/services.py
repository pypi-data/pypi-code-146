from __future__ import annotations

from tcsoa.gen.Manufacturing._2012_09.DataManagement import CreateConfigInput, CreateConfigResponse, ApplyConfigInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.Manufacturing._2012_09.Validation import ValidationsChecksObjectsResponse, ValidationCheckExecutionParam, ValidationsChecksExecutionResponse


class DataManagementService(TcService):

    @classmethod
    def createOrUpdateConfigObjects(cls, input: List[CreateConfigInput]) -> CreateConfigResponse:
        """
        Creates or updates the configuration objects based on the input data.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateConfigObjects',
            library='Manufacturing',
            service_date='2012_09',
            service_name='DataManagement',
            params={'input': input},
            response_cls=CreateConfigResponse,
        )

    @classmethod
    def applyConfigObjects(cls, input: List[ApplyConfigInput]) -> ServiceData:
        """
        Apply configuration objects to applicable business objects.
        """
        return cls.execute_soa_method(
            method_name='applyConfigObjects',
            library='Manufacturing',
            service_date='2012_09',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ServiceData,
        )


class ValidationService(TcService):

    @classmethod
    def executeValidations(cls, input: List[ValidationCheckExecutionParam], failAllOnError: bool) -> ValidationsChecksExecutionResponse:
        """
        This SOA function is to execute the validation checks by the user choice from the UI
        """
        return cls.execute_soa_method(
            method_name='executeValidations',
            library='Manufacturing',
            service_date='2012_09',
            service_name='Validation',
            params={'input': input, 'failAllOnError': failAllOnError},
            response_cls=ValidationsChecksExecutionResponse,
        )

    @classmethod
    def getAllValidations(cls) -> ValidationsChecksObjectsResponse:
        """
        This SOA function is to get all the customized registered callback to show the user in the UI
        """
        return cls.execute_soa_method(
            method_name='getAllValidations',
            library='Manufacturing',
            service_date='2012_09',
            service_name='Validation',
            params={},
            response_cls=ValidationsChecksObjectsResponse,
        )
