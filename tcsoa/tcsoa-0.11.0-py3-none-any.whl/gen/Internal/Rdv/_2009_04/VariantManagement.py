from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, NamedVariantExpression, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetMultipleNVEResponse(TcBaseObj):
    """
    This structure contains the list of created NVEs and 'ServiceData' object.
    
    :var aNves: List of newly created NamedVariantExpressions. One for each successfully created NVEs.
    :var serviceData: The 'ServiceData' object containing full/partial errors.
    """
    aNves: List[NamedVariantExpression] = ()
    serviceData: ServiceData = None


@dataclass
class GetSVRInfo(TcBaseObj):
    """
    The 'GetSVRInfo' structure refers to the object containing information about Saved Variant Rule.
    
    :var itemRev: Reference to the ItemRevision object of the product context on which SVR is to be created
    :var svrData: List of 'SVRData' objects which contains the information like SVR name, description, relation, option
    value pair.
    """
    itemRev: ItemRevision = None
    svrData: List[SVRData] = ()


@dataclass
class GetSVRResponse(TcBaseObj):
    """
    This is a structure that has references of all the created/modified SVRs in the operation along with the
    'ServiceData'.
    
    :var aSVRs: A collection of all the created/modified SVR(s).
    :var serviceData: An object of 'ServiceData' which contains updated data model objects and/or error objects with
    error messages.
    """
    aSVRs: List[BusinessObject] = ()
    serviceData: ServiceData = None


@dataclass
class MultipleNamedVariantExpressions(TcBaseObj):
    """
    This structure contains the information required to create multiple NVEs. It contains the Architecture Breakdown
    revision object, a boolean flag and list of 'NamedVariantExpressionsInfo' structure.
    
    :var archRev: Reference to the Architecture Breakdown revision object. If this reference is not supplied then NVE
    will not be created.
    
    :var ignoreDuplicates: Boolean value to indicate whether duplicate NVE should be checked or not. 
    If it is false then uniqueness of NVE will be checked.
    If it is true then uniqueness of NVE will not be checked then multiple NVEs can be created with the same variant
    condition.
    
    
    :var nveInfo: List of 'NamedVariantExpressionsInfo' objects. Each  object contains the information required to
    create a Named Variant Expression.
    """
    archRev: ItemRevision = None
    ignoreDuplicates: bool = False
    nveInfo: List[NamedVariantExpressionsInfo] = ()


@dataclass
class NamedVariantExpressionsInfo(TcBaseObj):
    """
    This structure contains the information required to create a NVE. It contains name, description and
    VariantCondition.
    
    :var code: Name of the NamedVariantExpression. When shared NVE is used it is mandatory to supply the name. If code
    is not supplied then NVE will be created without any name. These kinds of NVE cannot be shared.
    :var desc: Description of the NamedVariantExpression. It is not mandatory. If description is not supplied NVE will
    be created without description.
    :var varCondition: Variant Conditions for the NamedVariantExpression. It is required that a valid variant condition
    is supplied for this operation to succeed.
    """
    code: str = ''
    desc: str = ''
    varCondition: BusinessObject = None


@dataclass
class SVRData(TcBaseObj):
    """
    The 'SVRData' structure contains the information about Saved Variant Rule(s) which are to be created.
    
    :var varRule: Specifies the default BOMVariantRule. If the SVR being created already exists then this default
    variant rule is applied on existing rule.
    :var name: Specifies the name of SVR
    :var desc: Specifies the description of SVR
    :var relation: Specifies the relation with which SVR will be attached to the provided ItemRevision object
    :var option: List of options to be set in the variant rule
    :var value: List of values corresponding to the supplied options. This attribute is used in conjunction with the
    option attribute, i.e. option value pair
    """
    varRule: BusinessObject = None
    name: str = ''
    desc: str = ''
    relation: str = ''
    option: List[BusinessObject] = ()
    value: List[str] = ()


@dataclass
class DeleteNamedVariantExpressions(TcBaseObj):
    """
    This structure contains architecture breakdown and the list of NVEs to be deleted.
    
    :var archRev: Reference to the Architecture Breakdown revision object. If this reference is not supplied then this
    operation will fail.
    :var code: List of the Named Variant Expressions to be deleted.
    """
    archRev: ItemRevision = None
    code: List[NamedVariantExpression] = ()
