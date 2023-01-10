from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Classification._2007_01.Classification import ClassDef
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetLibraryHierarchyResponse(TcBaseObj):
    """
    Holds classification objects returned by 'getLibraryHierarchy()'' 'method.
    
    :var clsInfo: List of class references found for this library
    :var svcData: Any failures with Key-LOV ID mapped to the error message in the 'ServiceData' list of partial errors.
    """
    clsInfo: List[ClassInfo] = ()
    svcData: ServiceData = None


@dataclass
class HierarchyInfoAndOptions(TcBaseObj):
    """
    Structure representing the ClassId and options
    
    :var id: Class ID to be deleted.
    :var theRecurseOption: Flag to indicate if the delete operation should be recursively executed on the child classes
    for the given class.
    :var theViewsOption: Flag to indicate if the Views associated with the class being deleted should be removed first.
    If views exist and this flag does not indicate deleting them first, then a referential integrity error will be
    generated for the given class.
    :var theIcosOption: Flag to indicate if the Classification objects (ICO) should be delete first. If ICOs exist and
    this flag does not indicate deleting them first, then a referential integrity error will be generated for the given
    class.
    :var theWSOOption: Flag to indicate if the classified Workspace Objects should be deleted first.
    :var theChildrenOnlyOption: Flag to indicate if only the child classes should be deleted.
    :var theIgnoreOption: Flag to indicate if the operation to should continue on error.
    - FALSE: stop on first error 
    - TRUE: continue on error and report all failed objects back in the list of failed objects.
    
    """
    id: str = ''
    theRecurseOption: bool = False
    theViewsOption: bool = False
    theIcosOption: bool = False
    theWSOOption: bool = False
    theChildrenOnlyOption: bool = False
    theIgnoreOption: bool = False


@dataclass
class ClassInfo(TcBaseObj):
    """
    Structure representing class description in ClassDef structure and business object
    
    :var classDefn: Reference of the class definition structures holding all the class properties for the classes
    retrieved by this operation
    :var classBO: Reference to the business object found associated to this class.
    """
    classDefn: ClassDef = None
    classBO: BusinessObject = None
