from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.ImportExport._2011_06.FileImportExport import ImportExportOptions
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ImportDocumentInputData(TcBaseObj):
    """
    Structure represents the parameters required to import a requirement specification.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var transientFileWriteTicket: Transient File write ticket for the file to be imported.
    :var childSpecElementType: Type of child elements to be created on import.
    :var specificationType: Type of top level object to be created. RequirementSpec is default.
    :var selectedObject: Object under which new structure will be imported.
    :var keywordImportOptions: List of options to be used during keyword import.
    :var specDesc: Description to be set for an Specification.
    """
    clientId: str = ''
    transientFileWriteTicket: str = ''
    childSpecElementType: str = ''
    specificationType: str = ''
    selectedObject: BusinessObject = None
    keywordImportOptions: KeywordImportOptions = None
    specDesc: str = ''


@dataclass
class KeywordImporCondition(TcBaseObj):
    """
    Structure contains the operation type and keyword value provided by the user.
    
    :var opType: An operation type which is  to be applied on the document together with the values.
    Suppored operation types are :
    WORD_PARTIAL_MATCH : Searches for the partial occurrence of the given string.
    WORD_EXACT_MATCH : Searches for the exact occurrence of the given string.
    HAS_STYLE : Searches for the text with given style.
    :var keyword: The keyword here means the text to be searched for in the MS word document, is 
    provided by user to be used with operation type for Keyword Import keyword.
    Ex.  if the opType is WORD_EXACT_MATCH and value is "car" then the exact occurrence of "car" has to be looked up in
    the document .
    """
    opType: str = ''
    keyword: str = ''


@dataclass
class KeywordImportOptions(TcBaseObj):
    """
    Structure to specify the options to be used during keyword import.
    
    :var importOptions: Generic options in the form of key-value pairs to be used for processing.
    Ex. PermanentConvertToHTML, TRUE
    This option is used to convert the word file data in to HTML format to get this edited in active workspace client.
    RunInBackGround, TRUE
    This option is used to run Import process in background.
    :var keywordImportRules: Keyword import rules to be used.
    """
    importOptions: List[ImportExportOptions] = ()
    keywordImportRules: List[KeywordImportRule] = ()


@dataclass
class KeywordImportRule(TcBaseObj):
    """
    Structure contains the Rules provided by user to be used during keyword Import.
    
    :var targetChildType: SpecElement type which is to be created if the keyword rule evaluates to true on the document
    text.
    :var conditionProcessingType: The condition processing type, Supported values are: ANY and ALL. ANY is default.
    ANY &ndash; if any of the condition are met then only apply this rule.
    ALL -  if all the conditions are met then only apply this rule.
    :var keywordImportConditions: The conditions to be applied on the document to determine the types of objects to be
    created.
    """
    targetChildType: str = ''
    conditionProcessingType: str = ''
    keywordImportConditions: List[KeywordImporCondition] = ()
