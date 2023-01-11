from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ValidationResult, POM_object
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class NameValueStruct(TcBaseObj):
    """
    This structure holds property names and values for each property. The strings for the 'values' element must be
    derived from the Teamcenter::Soa::Client::Property::toXXXString() functions. This will ensure the strings for a
    Date, float, and other property types are formatted correctly.
    
    :var name: The name of the property.
    :var values: The property values.
    """
    name: str = ''
    values: List[str] = ()


@dataclass
class PropInfo(TcBaseObj):
    """
    This structure holds information about object and property information.
    
    :var object: Pointer to an object.
    :var vecNameVal: A vector of structures that contain <property name, property values vector>  pairs of the given
    business object.
    """
    object: BusinessObject = None
    vecNameVal: List[NameValueStruct] = ()


@dataclass
class ReportDatasetInfo(TcBaseObj):
    """
    The DatasetInfo struct represents all of the data necessary to construct the dataset object.
    
    :var clientId: Unique client identifier string.
    :var name: The name for a dataset. If it is an empty string, a name will be automatically generated.
    :var type: The dataset type used to create a dataset. A valid dataset type name string will be required.
    """
    clientId: str = ''
    name: str = ''
    type: str = ''


@dataclass
class ResultOverrideApproval(TcBaseObj):
    """
    The structure contains inputs for performing specified actions for override approval of a validation result.
    
    :var clientId: Unique client identifier
    :var targetBo: A target Business Object whose override approval will be processed.
    :var action: The action to be performed for result override approval.
    1    Create override approval
    2    Update override approval
    3    Approve override approval
    4    Reject override approval
    5    Remove override approval
    :var objectPropNameValues: A vector of PropInfo for result override approval. Empty vector should be given if the
    action is to remove override approval or when the action is to be performed on all applicable ValidationResult
    objects that belong to the given target Business Object.
    """
    clientId: str = ''
    targetBo: POM_object = None
    action: int = 0
    objectPropNameValues: List[PropInfo] = ()


@dataclass
class UpdateInput(TcBaseObj):
    """
    The inputs required for updating an existing ValidationResult object.
    
    :var clientId: Unique client identifier string.
    :var targetBo: The target Business Object whose validation results are to be updated.
    :var removeReportDatasetNamedRefs: The flag indicates whether the named refs of report datasets of ValidationResult
    objects will be removed.
    :var objectPropNameValues: A vector of PropInfo to be used for updating a ValidationResult object.
    """
    clientId: str = ''
    targetBo: POM_object = None
    removeReportDatasetNamedRefs: bool = False
    objectPropNameValues: List[PropInfo] = ()


@dataclass
class ValidationResultInfo2(TcBaseObj):
    """
    The ValidationResultInfo2 structure is the main input to the createOrUpdateValidationResults2 This struct refers to
    the existing ValidationResult, attribute list, report files, and one or more Dataset structs used to create those
    report datasets.
    
    :var createInputVec: A vector of CreateIn  structs required for creating new ValidationResult objects.
    :var updateInputVec: A vector of UpdateInput structs  required for updating existing ValidationResult objects.
    """
    createInputVec: List[CreateIn] = ()
    updateInputVec: List[UpdateInput] = ()


@dataclass
class ValidationResultsOutput2(TcBaseObj):
    """
    The newl created ValidationResult objects are returned.
    
    :var clientId: Unique client identifier string.
    :var resultObject: Pointer to a newly created ValidationResult object.
    """
    clientId: str = ''
    resultObject: ValidationResult = None


@dataclass
class ValidationResultsResponse2(TcBaseObj):
    """
    Holds the response for createOrUpdateValidationResults2.
    
    :var output: The output structure holding the created ValidationResult objects.
    :var serviceData: Holds model objects and partial errors.
    """
    output: List[ValidationResultsOutput2] = ()
    serviceData: ServiceData = None


@dataclass
class CreateIn(TcBaseObj):
    """
    Input for create operation including unique client identifier string.
    
    :var clientId: Unique client identifier string.
    :var targetBo: This object is the validation target Business Object that logically owns the newly created
    ValidationResult object. The concept is that there is an ItemRevision (which is the targetBo for NX Check Mate)
    that owns the ValidationResult that is to be created.
    :var checkerClassName: The checker class name of the referenced validation checker.
    :var paramsCreateInput: The required inputs for creating a ValidationParams object.
    :var reportDataset: Information to create new empty report datasets and attached them to the ValidationResult.
    :var data: Input data for create operation to create a ValidationResult object.
    """
    clientId: str = ''
    targetBo: POM_object = None
    checkerClassName: str = ''
    paramsCreateInput: CreateInput = None
    reportDataset: ReportDatasetInfo = None
    data: CreateInput = None


@dataclass
class CreateInput(TcBaseObj):
    """
    'CreateInput' structure used to capture the inputs required for creation of a validation result business object.
    
    :var boName: Map containing string property values.
    :var stringProps: Map containing string property values.
    :var boolArrayProps: Map containing bool array property values.
    :var dateProps: Map containing DateTime property values.
    :var dateArrayProps: Map containing DateTime array property values.
    :var tagProps: Map containing tag property values.
    :var tagArrayProps: Map containing tag array property values.
    :var compoundCreateInput: CreateInput for compounded objects.
    :var stringArrayProps: Map containing string array property values.
    :var doubleProps: Map containing double property values.
    :var doubleArrayProps: Map containing double array property values.
    :var floatProps: Map containing float property values.
    :var floatArrayProps: Map containing float array property values
    :var intProps: Map containing int property values.
    :var intArrayProps: Map containing int array property values.
    :var boolProps: Map containing bool property values.
    """
    boName: str = ''
    stringProps: StringMap = None
    boolArrayProps: BoolVectorMap = None
    dateProps: DateMap = None
    dateArrayProps: DateVectorMap = None
    tagProps: TagMap = None
    tagArrayProps: TagVectorMap = None
    compoundCreateInput: CreateInputMap = None
    stringArrayProps: StringVectorMap = None
    doubleProps: DoubleMap = None
    doubleArrayProps: DoubleVectorMap = None
    floatProps: FloatMap = None
    floatArrayProps: FloatVectorMap = None
    intProps: IntMap = None
    intArrayProps: IntVectorMap = None
    boolProps: BoolMap = None


"""
CreateInputMap that contains <property name, CreateInput vector> pairs.
"""
CreateInputMap = Dict[str, List[CreateInput]]


"""
DateMap that contains <property name, date value> pairs.
"""
DateMap = Dict[str, datetime]


"""
DateVectorMap that contains <property name, date value vector> pairs.
"""
DateVectorMap = Dict[str, List[datetime]]


"""
DoubleMap that contains <property name, double value> pairs.
"""
DoubleMap = Dict[str, float]


"""
DoubleVectorMap that contains <property name, double value vector> pairs.
"""
DoubleVectorMap = Dict[str, List[float]]


"""
FloatMap that contains <property name, float value> pairs.
"""
FloatMap = Dict[str, float]


"""
FloatVectorMap that contains <property name, float value vector> pairs.
"""
FloatVectorMap = Dict[str, List[float]]


"""
IntMap that contains <property name, integer value> pairs.
"""
IntMap = Dict[str, int]


"""
IntVectorMap that contains <property name, integer value vector> pairs.
"""
IntVectorMap = Dict[str, List[int]]


"""
StringMap that contains <property name, property value> pairs.
"""
StringMap = Dict[str, str]


"""
BoolMap that contains <property name, bool value> pairs.
"""
BoolMap = Dict[str, bool]


"""
StringVectorMap that contains <property name, string value vector> pairs.
"""
StringVectorMap = Dict[str, List[str]]


"""
TagMap that contains <property name, object identifier> pairs.
"""
TagMap = Dict[str, BusinessObject]


"""
TagVectorMap that contains <property name, object identifier vector> pairs.
"""
TagVectorMap = Dict[str, List[BusinessObject]]


"""
BoolVectorMap that contains <property name, bool value vector> pairs.
"""
BoolVectorMap = Dict[str, List[bool]]
