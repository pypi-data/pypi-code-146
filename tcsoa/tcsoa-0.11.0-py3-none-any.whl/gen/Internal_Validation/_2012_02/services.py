from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.Validation._2012_02.Validation import ResultOverrideApproval, ValidationResultInfo2, ValidationResultsResponse2
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ValidationService(TcService):

    @classmethod
    def performActionOnOverrideApproval(cls, inputs: List[ResultOverrideApproval]) -> ServiceData:
        """
        This operation will perform the specified result override approval life cycle actions for given
        ValidationResult objects. This service will allow a user to create, edit, and/or delete validation result
        override requests, and will also allow designated privileged users to approve or reject override requests.
        
        Use cases:
        It is desirable that requests for override approval on failed checkers to be left to the design user
        discretion. The design user may have good justification to argue that a failed checker can be corrected at a
        later design stage. Therefore, the capability to approve a result override request on a failed checker by
        designated approvers in a company will be necessary to allow the part design to progress smoothly without
        passing an overridden failed checker.
        """
        return cls.execute_soa_method(
            method_name='performActionOnOverrideApproval',
            library='Internal-Validation',
            service_date='2012_02',
            service_name='Validation',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def createOrUpdateValidationResults2(cls, inputs: ValidationResultInfo2) -> ValidationResultsResponse2:
        """
        This service will create new ValidationResult objects or update existing ValidationResult objects.
        ValidationResult objects are created or updated after a validation application executes the specified
        validation business logic to validate against the specified validation target objects to ensure a validation
        target meets compliance.
        
        Use cases:
        The processes of a customer site may require that a part will be released to production only after the part
        meets compliance specified by business logic that is embedded with various validation checkers for certain
        validation application utility. After executing validation business logic on the part, the user will use this
        service to create new ValidationResult objects or update existing ValidationResult objects to demonstrate the
        compliance status of the part.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateValidationResults2',
            library='Internal-Validation',
            service_date='2012_02',
            service_name='Validation',
            params={'inputs': inputs},
            response_cls=ValidationResultsResponse2,
        )
