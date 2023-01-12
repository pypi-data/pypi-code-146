from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GenerateContextIDsInput2(TcBaseObj):
    """
    This structure is the input sructure for the generateContextSpecificIDs service.
    This contains the informanion of context name and number of IDs to be generated for that context name.
    
    :var clientID: A unique string supplied by the caller. This ID is used to identify returned
    GenerateContextIDResponse elements and Partial Errors associated with this input GenerateContextIDsInput2.
    :var contextName: Name of the context for which IDs to be generated. A context name is a string that can be up to
    256 characters long. This string should not be empty, in order to generate IDs, an error is returned if user tries
    to generate ID for a empty context name.
    :var contextTypeName: The name of the business object for which the property values are to be generated and
    validated. An error 39007 is returned by the operation if the type name is not valid.
    :var contextPropName: Property name associated with the Context Name. This property name will be used to validate
    ID uniqueness.
    :var validateIDs: If true, the IDs should be validated for uniquness, otherwise no validation will be done. If
    false, contextType and contextPropName can be NULL.
    :var numberOfIDs: The number of IDs to be generated for a given context name. This is a mandatory field and should
    not be 0 or any negative number to generate IDs. An error is returned, if user tries to generate ID for a context
    name with invalid value (0 or negative number) for this field.
    """
    clientID: str = ''
    contextName: str = ''
    contextTypeName: str = ''
    contextPropName: str = ''
    validateIDs: bool = False
    numberOfIDs: int = 0
