from __future__ import annotations

from tcsoa.gen.Classification._2007_01.Classification import TypedDocument, AttributeFormat
from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExtendedClassDef(TcBaseObj):
    """
    This structure contains the extended information about a class.
    
    :var classDef: This basic information about the class.
    :var parentDefs: List of the parent definitions specific to the class and the parent corresponding basic properties.
    :var classShortName: The short name of the class.
    :var classDescription: The description of the class.
    :var classUserData1: User data 1 added to the class.
    :var classUserData2: User data 2 added to the class.
    :var classChildCount: The count of child classes of the class. If not retrieved, the count is -1.
    :var classInstanceCount: The count of instances in the class. If not retrieved, the count is -1.
    :var classImagesLoaded: If true, value indicates that the image documents for this class were loaded. False, they
    were not loaded.
    :var classImageDocuments: A list of class documents attached to the class (like class image).
    """
    classDef: BaseClassDef = None
    parentDefs: List[BaseClassDef] = ()
    classShortName: str = ''
    classDescription: str = ''
    classUserData1: str = ''
    classUserData2: str = ''
    classChildCount: int = 0
    classInstanceCount: int = 0
    classImagesLoaded: bool = False
    classImageDocuments: List[TypedDocument] = ()


@dataclass
class GetChildrenExtendedOutput(TcBaseObj):
    """
    Structure containing the found classes for the given search criteria. Any failures with the search will be mapped
    to the error message in the ServiceData list of partial errors.
    
    :var classDescriptions: List of child classes found.
    """
    classDescriptions: List[ExtendedClassDef] = ()


@dataclass
class GetChildrenExtendedResponse(TcBaseObj):
    """
    Contains a list of child classes found for the given classes.
    
    :var classDescriptions: List of child classes found for input class IDs.
    :var svcData: Any failures with class ID mapped to the error message are returned in the ServiceData list of
    partial errors.
    """
    classDescriptions: List[GetChildrenExtendedOutput] = ()
    svcData: ServiceData = None


@dataclass
class BaseClassDef(TcBaseObj):
    """
    This structure contains the basic information about a class.
    
    :var classID: The ID of the class.
    :var classBO: Reference to the business object representing this class.
    :var className: The name of the class.
    :var isAbstract: If true, this class is abstract. Classification instances cannot be stored in this class. False,
    indicates that Classification instances can be stored in this class.
    :var classUnitBase: The unit system of the class:
    - 0 - The class supports the storage of metric objects only 
    - 1 - The class supports the storage of non-metric only 
    - 2 - The class supports both metric and non-metric objects
    
    
    :var classIconLoaded: If true, the icon file for this class is loaded. False, it is not loaded.
    :var classIconDocument: The icon document attached to this class.
    """
    classID: str = ''
    classBO: BusinessObject = None
    className: str = ''
    isAbstract: bool = False
    classUnitBase: int = 0
    classIconLoaded: bool = False
    classIconDocument: TypedDocument = None


@dataclass
class SearchClassesExtendedOutput(TcBaseObj):
    """
    Structure containing the found classes for the given search criteria. Any failures with the search will be mapped
    to the error message in the ServiceData list of partial errors.
    
    :var classDescriptions: List of classes found for input search criteria.
    """
    classDescriptions: List[ExtendedClassDef] = ()


@dataclass
class SearchClassesExtendedResponse(TcBaseObj):
    """
    Structure containing the found classes for the given search criteria. Any failures with the search will be mapped
    to the error message in the ServiceData list of partial errors.
    
    :var classDescriptions: List of classes found for input search criteria.
    :var svcData: Any failures with the search will be mapped to the error message in the ServiceData list of partial
    errors.
    """
    classDescriptions: List[SearchClassesExtendedOutput] = ()
    svcData: ServiceData = None


@dataclass
class ValueConversionInput(TcBaseObj):
    """
    Structure containing the value(s) and unit systems which should be used to convert the input values.
    
    :var inputValues: The input values. For regular attributes it's just one value. In case of VLA (variable length
    array) attributes each value has its own entry.
    The calling client is responsible for converting the different property types (int, float, date .etc) to a string
    using the appropriate functions in the SOA client framework's Property class.
    :var inputUnit: The input unit e.g. the unit definition ID "Length_mm" or also the display name "mm".
    :var outputUnit: The output unit e.g. the unit definition ID "Length_mm" or also the display name "mm".
    :var outputFormat: The output format to which the converted value should be formatted.
    :var options: The options parameter (This option is for future use).
    """
    inputValues: List[str] = ()
    inputUnit: str = ''
    outputUnit: str = ''
    outputFormat: AttributeFormat = None
    options: int = 0


@dataclass
class ValueConversionOutput(TcBaseObj):
    """
    The converted values. For regular attributes it's just one value, in case of VLA (variable length array)
    attributes, each value has its own entry.
    
    :var convertedValues: The converted values. For regular attributes it's just one value. In case of VLA (variable
    length array) attributes each value has its own entry.
    
    The calling client is responsible for converting the string value to the different property types  (int, float,
    date .etc) using the appropriate functions in the SOA client framework's Property class.
    """
    convertedValues: List[str] = ()


@dataclass
class ConvertValuesResponse(TcBaseObj):
    """
    Structure containing the converted values. Any failures with the conversion will be mapped to the error message in
    the ServiceData list of partial errors.
    
    :var convertedValues: The converted values.
    :var svcData: Any failures with the conversion will be mapped to the error message in the ServiceData list of
    partial errors.
    """
    convertedValues: List[ValueConversionOutput] = ()
    svcData: ServiceData = None
