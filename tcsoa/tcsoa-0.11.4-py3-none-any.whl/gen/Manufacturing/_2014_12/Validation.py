from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class MaturityData(TcBaseObj):
    """
    Structure containing the result of maturity check and other relevant information
    
    :var evaluatedObject: The BusinessObject on which rules are evaluated. For example, a BOMLine from the structure is
    a valid object on which certain rules are evaluated.
    :var ruleResults: Map containing the result of the evaluation. The key of the map is uid of the rule and value of
    the map is list of PropertyData containing the result of the evaluation along with relevant data.
    
    The valid propertyName members of the PropertyData is:
    
    - status:  Specifies the status of the evaluation. Valid values of status are "Pass", "Fail", "Partial" and "NA"
    (Not Applicable).  "Pass" signifies that rule on evaluatedObject is passed, "Fail" signifies failed, "Partial"
    signifies partially passed and "NA" signifies that the rule is not applicable for the evaluated object.
    - statusDisplayValue: Display value of the rule evaluated on the object. It may not be same as outcome of rule.
    - ruleUID: uid of the rule
    
    
    :var objectLevelStatus: Overall result and status of evaluated object. 
    
    The valid propertyName member of the PropertyData is:
    
    - status:  Specifies the status of the evaluation. Valid values of status are "Pass", "Fail" and "Partial".  "Pass"
    signifies that all rules on evaluatedObject passed, "Fail" signifies that all rules failed and "Partial" signifies
    that some rule passed. Rules that are not applicable for the evaluated object are ignored for determining the
    overall status of the object.
    
    """
    evaluatedObject: BusinessObject = None
    ruleResults: CollectiveData = None
    objectLevelStatus: List[PropertyData] = ()


@dataclass
class MaturityReportRequest(TcBaseObj):
    """
    The input object to service. It contains below parameters - 
    
    inputObjects -    The input contains the BOMLine which acts as a scope for maturity check. The objects in the
    hierarchy of the scope are candidates for the check.
    
    ruleList -    The list of rules for which maturity is to be evaluated. Some of the rules may not be applicable to
    all objects in the scope.
    
    supportingInformation -    Additional supporting information that could be used to evaluate the maturity. Currently
    this input is not used by the operation.
    
    
    :var inputObjects: A list of BOMLine for which the maturity report is required. All objects in the hierarchy of the
    line are evaluated for the maturity check.
    :var selectedRules: A list of rules to evaluate the maturity. The 
    key and value (string, list(PropertyData)) of the map are uid of the rule and corresponding data respectively. The
    latter is list of structure PropertyData which has property name of the rule and data of that property
    respectively. The valid property name is "ruleUID" with value as UID of the rule.
     
    The rule in the list may be applicable to specific object type. The operation fetches those objects for a given
    scope and evaluates the rule. Both evaluated objects and status of the evaluation is reported in the response.
    
    For any two rules from the list, one may evaluate an object type different than that of another.
    :var supportingInformation: Additional supporting information required to evaluate the maturity. 
    Currently this input is not used by operation.
    """
    inputObjects: List[BusinessObject] = ()
    selectedRules: CollectiveData = None
    supportingInformation: List[PropertyData] = ()


@dataclass
class MaturityReportResponse(TcBaseObj):
    """
    The response is  the map containing maturity data and the service data. The map contains the evaluated object and
    its maturity status along with additional information related to checks. The evaluated objects type may not be of
    same type and may not be applicable to all the rules specified in input of the operation.
    
    :var serviceData: The service data containing partial errors.
    :var maturityResult: The result of getMaturityData operation, contains BusinessObjects and their maturity data.
    """
    serviceData: ServiceData = None
    maturityResult: MaturityResult = None


@dataclass
class PropertyData(TcBaseObj):
    """
    The detail information of the data in the form of property and its value.
    
    :var propertyName: Key to identify the data in the collection.
    :var value: Value of the property.
    :var dataType: Type of the data. It can be "boolean", "character", "date", "float", "double", "integer", "string"
    and "businessObject".
    """
    propertyName: str = ''
    value: List[str] = ()
    dataType: str = ''


"""
The result of getMaturityData operation, contains BusinessObjects and their maturity data.
"""
MaturityResult = Dict[BusinessObject, MaturityData]


"""
A list of rules to evaluate the maturity. The 
key and value (string, list(PropertyData)) of the map are uid of the rule and corresponding data respectively. The latter is vector of structure PropertyData which has property name of the rule and data of that property respectively. The valid property name is "ruleUID" with value as UID of the rule.
 
The rule in the list may be applicable to specific object type. The operation fetches those objects for a given scope and evaluates the rule. Both evaluated objects and status of the evaluation is reported in the response.

For any two rules from the list, one may evaluate an object type different than that of another.
"""
CollectiveData = Dict[str, List[PropertyData]]
