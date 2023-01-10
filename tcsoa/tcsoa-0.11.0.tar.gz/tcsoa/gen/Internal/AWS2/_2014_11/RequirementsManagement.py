from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetExportTemplateResponse(TcBaseObj):
    """
    The GetExportTemplateResponse structure contains the information about type of template and the display name of the
    template. The type of template can be "SpecTemplate" or "ExcelTemplate".
    
    :var serviceData: The Service data which may contain the following partial errors.
    224013 : The selected input object is not an business object of type Item or ItemRevision.
    224014 : The valid values for templateTypes are "SpecTemplate", "ExcelTemplate" or both.
    :var outTmplNames: The type of template as key and a vector of  
    templates found in the system as value. Example- The  
    "SpecTemplate" as the key and a list of all the SpecTemplates found in the database as the value. The
    "ExcelTemplate" as the key and a list of all the ExcelTemplates found in the database as the value. The
    "SpecTemplate" and "ExcelTemplate" are objects of type "SpecTemplate" and "ExcelTemplate" respectively.
    """
    serviceData: ServiceData = None
    outTmplNames: TemplateTypeVsTemplateNames = None


@dataclass
class GetTemplateInput(TcBaseObj):
    """
    The datastructure is used to collect input parameters like selected objects, type of template to be retrieved and
    additional information used for filtering.
    
    :var inputObjects: The selected objects for which the export templates are to be retrieved. The selected business
    object can be any type of Item or ItemRevision.
    :var templateTypes: The type of template to fetch, Value can be: "SpecTemplate","ExcelTemplate", or both.
    :var requestPref: A map of key and value pairs  (string, string) used for filtering and sorting. This is used as a
    future placeholder to implement template filtering and sorting. Currently its value will be blank.
    """
    inputObjects: List[BusinessObject] = ()
    templateTypes: List[str] = ()
    requestPref: RequestPreference = None


"""
The map which can have a key and value pair, used for options for filtering and sorting of export templates. The key and value are case sensitive.
"""
RequestPreference = Dict[str, str]


"""
This map will hold the type of template as key and vector of name of all templates found in the system with this name as value. Example - The SpecTemplate or "ExcelTemplate" as the key and a vector of all the template as the value.
"""
TemplateTypeVsTemplateNames = Dict[str, List[str]]
