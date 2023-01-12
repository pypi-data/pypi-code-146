from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, VariantRule, Awb0BOMIndexAdminData, RevisionRule, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProcessBomIndexInfo(TcBaseObj):
    """
    This structure contains  the processing options and the instances of Awb0BOMIndexAdminData whose state are either
    'ReadyToIndex', 'IndexGenSuccess', 'IndexExportSuccess', 'SolrIndexGenSuccess' and 'MarkedForDeletion'.
    
    :var biadObjs: Awb0BOMIndexAdminData  instances which has to be  processed for indexing.
    :var processingOptions: A map that contains the option and values. 
    The following options are currently supported
    Key:'updateTIEAMTables'
    Value:'true'
    Description: Update the TIE Access Manager(AM) tables if there is a change in the AM rule tree.
    """
    biadObjs: List[Awb0BOMIndexAdminData] = ()
    processingOptions: StringToStringMap = None


@dataclass
class ProcessBomIndexOutput(TcBaseObj):
    """
    This structure contains the processed Awb0BOMIndexAdminData instance,  FMS file tickets for the 'TCXML' and export
    log file. If the indexes were up-to-date then 'tcxmlFileTicket' would be an empty string. If  the 
    Awb0BOMIndexAdminData instance was marked for deletion then the 'tcxmlFileTicket' and the 'exportLogFileTicket'
    would be empty.
    
    :var biadObj: Awb0BOMIndexAdminData  instance which was processed.
    :var tcxmlFileTicket: Transient file ticket of the tcxml file.
    :var exportLogFileTicket: Transient file ticket of the export log  file.
    """
    biadObj: Awb0BOMIndexAdminData = None
    tcxmlFileTicket: str = ''
    exportLogFileTicket: str = ''


@dataclass
class ProcessBomIndexResponse(TcBaseObj):
    """
    This structure contains a list of the processed Awb0BOMIndexAdminData  instances,  the transient file ticket to a
    file that contains the 'TCXML' representation of configured product indexes and the transient file ticket to export
    log file that was created during index generation.
    The 'outputList' is ordered in same order as input 'bomIndexObjs'.
    
    :var outputList: A list of 'ProcessBomIndexOutput' structures.
    :var serviceData: The Service Data through which the errors are communicated to the client.
    Following are some possible errors returned in ServiceData:
    - 203408 - Transfer Option Set could not be found.
    - 11001 -  TIE internal error.
    - 11112 - No configured revision is found for the given top line Item.
    
    """
    outputList: List[ProcessBomIndexOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreBOMIndxAdmDataInfo(TcBaseObj):
    """
    'CreBOMIndxAdmDataInfo' contains the product and configuration rules information for which the 'BOM' index should
    be generated.
    
    :var product: The product can be ItemRevision or CollaborativeDesign, for which  the 'BOM' index should be
    generated.
    :var cfgRuleInfos: List of configuration rules including RevisionRule(s) and SavedVariantRule(s) to use for
    configuring the given product.
    """
    product: BusinessObject = None
    cfgRuleInfos: List[IndxCnfgRulesInfo] = ()


@dataclass
class CreBOMIndxAdmDataResp(TcBaseObj):
    """
    'CreBOMIndxAdmDataResp' contains the list of Awb0BOMIndexAdminData instances that were created or updated.
    
    :var bomIndexAdminDataObjs: List of Awb0BOMIndexAdminData instances that are created or updated.
    :var serviceData: The 'ServiceData' through which the errors are communicated to the client.
    """
    bomIndexAdminDataObjs: List[Awb0BOMIndexAdminData] = ()
    serviceData: ServiceData = None


@dataclass
class IndxCnfgRulesInfo(TcBaseObj):
    """
    'IndxCnfgRulesInfo' contains the list of RevisionRule(s) with the effectivity information and a list of saved
    VariantRule(s) with their owning ItemRevision(s) which are applicable to the given product. The configuration rules
    will be used to configure the structure for indexing. For each of saved VariantRule the owning ItemRevision must
    also be specified.
    
    :var revisionRuleInfo: The base RevisionRule used to configure the product.
    :var variantRules: List of saved VariantRule(s) used for structure configuration.
    :var svrOwningItemRevs: List of ItemRevision(s) to which the saved VariantRule(s) are associated.
    """
    revisionRuleInfo: IndxRevisionRuleInfo = None
    variantRules: List[VariantRule] = ()
    svrOwningItemRevs: List[ItemRevision] = ()


@dataclass
class IndxRevisionRuleInfo(TcBaseObj):
    """
    Structure containing the revision rules with effectivity info used to configure a product in the BOM Index
    
    :var revisionRule: The base RevisionRule used to configure the product.
    :var effectivityEndItem: The end item used as RevisionRule effectivity criteria; it can be an Item or ItemRevision.
    :var effectivityDate: The effectivity date used as RevisionRule effectivity criteria.
    :var effectivityUnit: The effectivity unit number used as RevisionRule effectivity criteria along with effectivity
    end item. The unit number is a positive interger. Initialize it with -1 if unit number is not to be considered.
    """
    revisionRule: RevisionRule = None
    effectivityEndItem: BusinessObject = None
    effectivityDate: datetime = None
    effectivityUnit: int = 0


"""
A map to associate a string key to a string value.
"""
StringToStringMap = Dict[str, str]
