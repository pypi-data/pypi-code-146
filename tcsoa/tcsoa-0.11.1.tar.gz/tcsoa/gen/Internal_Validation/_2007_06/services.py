from __future__ import annotations

from tcsoa.gen.Internal.Validation._2007_06.Validation import GetValResultsInput, GetValidationResultResponse, ValidationDataResponse, CreateOrUpdateValidationAgentsResponse, ValidationDataInfo, ValidationAgentInfo, ValidationResultsResponse, ValidationResultInfo
from typing import List
from tcsoa.base import TcService


class ValidationService(TcService):

    @classmethod
    def getValidationResults(cls, input: GetValResultsInput) -> GetValidationResultResponse:
        """
        This operation will return the found validation result objects based on the given validation target objects and
        the given validation checkers.
        
        Use cases:
        A validation result object is generated for a business object by a validation agent using the specialized
        validation logic that is defined by a validation data object. For example, the NX Check Mate validation agent
        will execute NX Check Mate tests to generate validation result objects for an NX part item revision object
        using the underlying UGMaster dataset object as a validation target.  This operation will be used to search for
        the validation result objects that a user will be interested in by reducing the search scope using the given
        input objects.
        """
        return cls.execute_soa_method(
            method_name='getValidationResults',
            library='Internal-Validation',
            service_date='2007_06',
            service_name='Validation',
            params={'input': input},
            response_cls=GetValidationResultResponse,
        )

    @classmethod
    def createOrUpdateValidationAgents(cls, inputs: List[ValidationAgentInfo]) -> CreateOrUpdateValidationAgentsResponse:
        """
        Creates or updates a group of validation agents.  When the ValidationAgentInfo.existingValidationAgent object
        is not NULL, this service will update the existing validation agent. If it is NULL, this service will create
        new validation agent. A validation agent of a given type will be uniquely identified by the object_name
        attribute of the validation agent item. If an existing validation agent of the given name, identified by
        ValidationAgentInfo.name structure member, does not exist, a new validation agent will be created. If an
        existing validation agent of the given name is found, a severe error will be returned while attempting to
        create a new validation agent.
        
        Use cases:
        This service will be used for a user to create new validation agents and/or update existing validation agents.
        A validation agent must be created before the user can utilize the validation application to execute validation
        business logic and create validation results.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateValidationAgents',
            library='Internal-Validation',
            service_date='2007_06',
            service_name='Validation',
            params={'inputs': inputs},
            response_cls=CreateOrUpdateValidationAgentsResponse,
        )

    @classmethod
    def createOrUpdateValidationData(cls, inputs: List[ValidationDataInfo]) -> ValidationDataResponse:
        """
        Creates or update a group of ValidationData objects.  A ValidationData object represents a validation checker
        of a certain validation agent in the database. When the ValidationDataInfo.existingValidationData object is not
        NULL, this service will update the existing ValidationData object. If it is NULL, this service will create new
        ValidationData object. A ValidationData object will be uniquely identified by the combination of
        validation_name attribute and validation_ application attribute of the ValidationData object. A new
        ValidationData object will be created if an existing ValidationData, identified by ValidationDataInfo.name and
        ValidationDataInfo.agentName structure members, does not exist. If an existing ValidationData object of the
        given name and agent name is found, a severe error will be returned while attempting to create a new
        ValidationData object.
        
        Use cases:
        This service will be used for a user to create new validation checkers and/or update existing validation
        checkers. A validation checker must be created before the user can utilize the validation application to
        execute validation business logic specified by the ValidationData object and create validation results.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateValidationData',
            library='Internal-Validation',
            service_date='2007_06',
            service_name='Validation',
            params={'inputs': inputs},
            response_cls=ValidationDataResponse,
        )

    @classmethod
    def createOrUpdateValidationResults(cls, inputs: List[ValidationResultInfo]) -> ValidationResultsResponse:
        """
        Creates or update a group of validation results.  When the ValidationResultInfo .existingValidationResult
        object is not NULL, this service will update the existing ValidationResult object. If
        ValidationResultInfo.existingValidationResult is NULL, this service will create new a new ValidationResult
        object. Before creating a new one, the service first attempts to validate the existence of the ValidationResult
        by the combination of ValidationResultInfo.targetObject, ValidationResultInfo.validationDataObject, and
        ValidationResultInfo.resultId structure members. If the ValidationResult object does not exist, a new
        ValidationResult object will be created. If a ValidationResult object already exists, an error message will be
        returned while attempting to create a new ValidationResult object.
        
        Use cases:
        The processes of a customer site may require that a part will be released to production only after the part
        meets compliance specified by business logic that is embedded with various validation checkers for certain
        validation application utility. After executing validation business logic on the part, the user will use this
        service to create new ValidationResult objects or update existing ValidationResult objects to demonstrate the
        compliance status of the part.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateValidationResults',
            library='Internal-Validation',
            service_date='2007_06',
            service_name='Validation',
            params={'inputs': inputs},
            response_cls=ValidationResultsResponse,
        )
