from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ValidationCheckCallbackParam(TcBaseObj):
    """
    Validation Check Callback Param
    
    :var type: The type of the validation always MFG_ValidationChecksCallback
    :var library: Customized DLL Name
    :var name: Customized Name - The name of the validation test
    :var func: Customized Function name
    :var failAllOnError: Continue to the next test if the previous test failed.
    """
    type: str = ''
    library: str = ''
    name: str = ''
    func: str = ''
    failAllOnError: bool = False


@dataclass
class ValidationCheckExecutionErrors(TcBaseObj):
    """
    Validation Check Execution Errors
    
    :var object: the non valid object line
    :var validationErrors: validationErrors
    :var validationTest: The validation check that failed.
    """
    object: BusinessObject = None
    validationErrors: List[ValidationCheckExecutionErrorsDetails] = ()
    validationTest: ValidationCheckCallbackParam = None


@dataclass
class ValidationCheckExecutionErrorsDetails(TcBaseObj):
    """
    Validation Check Execution Errors Details
    
    :var msgId: could be ifail or lov (msgId from ValidationNotice struct)
    :var msg: description of the localized error
    :var object: The object on which the validation check failed
    :var validationNoticeType: The type of the returned notice from the callback functions
    """
    msgId: int = 0
    msg: str = ''
    object: BusinessObject = None
    validationNoticeType: str = ''


@dataclass
class ValidationCheckExecutionParam(TcBaseObj):
    """
    Validation Check Execution Param
    
    :var root: The root object to be validated, could be any line type of Mfg0BvrProcess or Mfg0BvrOperation or its
    derived.
    :var validationChecks: all the validation checks to perform on the object
    """
    root: BusinessObject = None
    validationChecks: List[ValidationCheckCallbackParam] = ()


@dataclass
class ValidationsChecksExecutionResponse(TcBaseObj):
    """
    Validations Checks Execution Response
    
    :var errors: errors
    :var serviceData: Standard ServiceData member
    """
    errors: List[ValidationCheckExecutionErrors] = ()
    serviceData: ServiceData = None


@dataclass
class ValidationsChecksObjectsResponse(TcBaseObj):
    """
    Validations Checks Objects Response
    
    :var params: params
    :var serviceData: serviceData
    """
    params: List[ValidationCheckCallbackParam] = ()
    serviceData: ServiceData = None
