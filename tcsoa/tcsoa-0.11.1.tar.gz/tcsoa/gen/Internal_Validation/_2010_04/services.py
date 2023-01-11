from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, POM_object
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ValidationService(TcService):

    @classmethod
    def getValidationResults2(cls, validationAgentRevObjects: List[POM_object], valDataObjects: List[POM_object], selectedObjects: List[BusinessObject], targetObjects: List[POM_object]) -> ServiceData:
        """
        This operation will return validation result objects in the ServiceData structure. This operation will take the
        given validation agents, validation data objects, selected objects, and/or validation target objects to build
        the search criteria to find the validation result objects. Validation agents represent applications that were
        used to generate the validation result objects. Validation data objects represent the specialized validation
        checkers that are referenced by the validation result objects.  The selected objects represent the owning
        business objects of the validation result objects. The target objects represent the validation target objects
        that are referenced by the validation result objects.
        
        Use cases:
        A validaiton result object is generated for a business object by a validation agent using the specialized
        validation logic that is defined by a validation data object. For example, the NX Check Mate validation agent
        will execute NX Check Mate tests to generate validation result objects for an NX part item revision object
        using the underlying UGMaster dataset object as a validation target.  This operation will be used to search for
        the validation result objects that a user will be interested in by reducing the search scope using the given
        input objects.
        """
        return cls.execute_soa_method(
            method_name='getValidationResults2',
            library='Internal-Validation',
            service_date='2010_04',
            service_name='Validation',
            params={'validationAgentRevObjects': validationAgentRevObjects, 'valDataObjects': valDataObjects, 'selectedObjects': selectedObjects, 'targetObjects': targetObjects},
            response_cls=ServiceData,
        )

    @classmethod
    def getValidationTargets(cls, validationAgentRevObjects: List[POM_object], valDataObjects: List[POM_object], selectedObjects: List[BusinessObject]) -> ServiceData:
        """
        This operation will execute validation business logic of the given validation agent to generate
        ValidationResult objects. This operation will take the given validation agent, validation data objects, the
        selected business objects, and validation target objects to generate the ValidationResult objects. The given
        validation agent represents the validation application that will be responsible for generating the validation
        result objects. Validation data objects represent the specialized validation checkers that are referenced by
        the validation result objects.  The selected objects represent the owning business objects of the validation
        result objects and will be used to collect the associated validation target objects to be combined with the
        given 'targetObjects' list for validation evaluation. The target objects represent the validation target
        objects that are referenced by the generated validation result objects.
        
        Use cases:
        This operation can be used to find out the list of associated validation target objects that will be evaluated
        by validation agents and checkers in validation operations.
        """
        return cls.execute_soa_method(
            method_name='getValidationTargets',
            library='Internal-Validation',
            service_date='2010_04',
            service_name='Validation',
            params={'validationAgentRevObjects': validationAgentRevObjects, 'valDataObjects': valDataObjects, 'selectedObjects': selectedObjects},
            response_cls=ServiceData,
        )

    @classmethod
    def runValidation(cls, validationAgentRev: POM_object, valDataObjects: List[POM_object], selectedObjects: List[BusinessObject], targetObjects: List[POM_object]) -> ServiceData:
        """
        This operation will execute validation business logic of the given validation agent to generate
        ValidationResult objects.  This operation will take the given validation agent, validation data objects, the
        selected business objects, and validation target objects to generate the ValidationResult objects. The given
        validation agent represents the validation application that will be responsible for generating the validation
        result objects. Validation data objects represent the specialized validation checkers that are referenced by
        the validation result objects.  The selected objects represent the owning business objects of the validation
        result objects and will be used to collect the associated validation target objects to be combined with the
        given 'targetObjects' list for validation evaluation. The target objects represent the validation target
        objects that are referenced by the generated validation result objects.
        
        Use cases:
        A Validation Administrator or System Administrator uses the Validation Manager application to create validation
        agents and checkers. The applications used to validate the data must be configured to perform validations for
        the defined objects. You do this by creating validation agents and checkers for each desired application. To
        enable object validation functionality, validation agents and checkers must be defined within the relevant
        applications.
        
        This operation will enable a user to use a given validation agent to generate the ValidationResult objects by
        invoking the validation business logic specified by a list of validation checkers on the selected business
        objects or on the given validation target objects. The ValidationResult objects will show the Pass or Fail
        result status of a business object for each individual validation checker and each validation target object.
        """
        return cls.execute_soa_method(
            method_name='runValidation',
            library='Internal-Validation',
            service_date='2010_04',
            service_name='Validation',
            params={'validationAgentRev': validationAgentRev, 'valDataObjects': valDataObjects, 'selectedObjects': selectedObjects, 'targetObjects': targetObjects},
            response_cls=ServiceData,
        )
