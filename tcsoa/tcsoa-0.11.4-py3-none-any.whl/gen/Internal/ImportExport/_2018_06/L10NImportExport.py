from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.base import TcBaseObj
from tcsoa.gen.Internal.ImportExport._2010_04.L10NImportExport import TypePropertiesInfo
from dataclasses import dataclass


@dataclass
class ObjectsInfo2(TcBaseObj):
    """
    'ObjectsInfo2' structure contains parameter required to filter Teamcenter business objects based on selected
    criteria that can be used to export localized business objects for review or translation purpose.
    
    :var translationsExist: If true, mode is Review mode; otherwise, false, mode is Translate.
    Review mode allows user to export all localized business objects into XML file based on status and locale selected.
    Translate mode exports business objects into XML file for selected target locale.
    :var locale: The name of the desired locale. The valid locale name should be in the format as outlined in the Java
    Standard Language (i.e. en_US for English, United States). A full list of locales supported by the Teamcenter
    server can be obtained from the service operation
    'Teamcenter::Soa::Core::_2010_04::LanguageInformation.getLanguageList'. This can also be set to English word Master
    for exporting all business objects into XML file that needs to be translated to different locale. This parameter
    works in conjunction with "translationsExist" and "statuses".
    If "locale" is set to Master, it indicates translate mode and valid values for other parameters:
    "translationsExist" must be "false", In case of value is set to "true", the 'ServiceData' contains error 269002.
    "statuses" should be empty; this value is ignored for Master locale. If "locale" is set to any other valid locale
    value then possible values for other parameters and behavior is: "translationsExist" is set to "true" indicate
    review mode. This will export all the business objects for selected "statuses".
    :var statuses: A list of status to filter the localized values on. The status may be one or more of the following:
    "Approved"
    "In-Review"
    "Pending"
    "Invalid"
    This is ignored if mode is "translate" ( 'translationsExist' is false ) and selected locale is Master. In "review"
    mode nothing is exported in case of invalid "statuses" is passed and operation returns error 269002 in
    'ServiceData'.
    :var transferOptionSet: The name of the Transfer Option Set that is used while exporting objects. This is retrieved
    using 'Teamcenter::Soa::GlobalMultiSite::_2007_06::ImportExport::getAllTransferOptionSets' operation.
    :var objects: A list of Teamcenter business objects which need to be filtered or exported basedon the passed in
    parameters.
    :var typesPropertiesInfo: A list of type names and the corresponding properties.
    """
    translationsExist: bool = False
    locale: str = ''
    statuses: List[str] = ()
    transferOptionSet: str = ''
    objects: List[BusinessObject] = ()
    typesPropertiesInfo: List[TypePropertiesInfo] = ()
