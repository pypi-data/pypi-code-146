from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, POM_object
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ApplyBOMMarkupParam(TcBaseObj):
    """
    The parameter to apply BOMMarkup.
    
    :var bomLine: The BOMLine object whose Markup is to be applied. The MarkupChanges for the Occurrence of the line
    will not be applied.
    :var recursive: Flag that indicates whether to apply all Markups for the structure under the specified line.
    :var evaluate: Flag that indicates whether to check write access ('true') or actually modify ('false') the
    structure.
    """
    bomLine: BOMLine = None
    recursive: bool = False
    evaluate: bool = False


@dataclass
class CreateBOMMarkupOutput(TcBaseObj):
    """
    Created markup change and the containing markup object.
    
    :var markupChange: The created change object.
    :var markup: The markup object that contains the markup change.
    :var bomLine: The bomline related to the markup object.
    """
    markupChange: POM_object = None
    markup: POM_object = None
    bomLine: BOMLine = None


@dataclass
class CreateBOMMarkupParam(TcBaseObj):
    """
    Structure for the information to create a Markup Change object.
    
    :var bomLine: The selected line for the Markup action.
    :var markupType: Type of Markup to create: 
    - 1 for 'ADD'
    - 2 for 'REMOVE'
    - 4 for 'SUBSTITUTE'
    - 8 for 'REPLACE'
    - 16 for 'PROPERTY'
    - 32 for 'COMMENT'
    
    
    :var inputObject: Item or Item Revision to be used for substitute, replace or addition. It can be a variant
    expression object for a property value change to legacy variant condition.
    :var context: Context of the edit. It is the BOMView object for substitute and replace. Not used for any other type
    of Markup Change.
    :var propertyName: Name of the property to be modified. When used by 'ADD' Markup, it is one of the following
    properties: find number, quantity and occurrence type.
    :var propertyValue: String value of the property. If used by 'ADD' Markup, it is one of the property values to
    initialize the added line for the properties specified by propertyName.
    :var note: Plain text note for the change. It can be a proposed change that is not covered by supported Markup
    types, for example, to insert a level.
    """
    bomLine: BOMLine = None
    markupType: int = 0
    inputObject: BusinessObject = None
    context: BusinessObject = None
    propertyName: str = ''
    propertyValue: str = ''
    note: str = ''


@dataclass
class CreateBOMMarkupResponse(TcBaseObj):
    """
    The response of creating BOM Markups.
    
    :var createBOMMarkupsList: Set of Markups created given the input.
    :var serviceData: The service data of the operation.
    """
    createBOMMarkupsList: List[CreateBOMMarkupOutput] = ()
    serviceData: ServiceData = None
