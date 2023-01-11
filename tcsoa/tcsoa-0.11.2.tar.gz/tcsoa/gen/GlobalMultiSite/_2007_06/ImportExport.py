from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Group, ClosureRule, ImanFile, PropertySet, Filter, TransferOptionSet, POM_imc, TransferMode, User, Role, PIEActionRule
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetActionRulesResponse(TcBaseObj):
    """
    The 'GetActionRulesResponse' structure defines the response from 'getActionRules' operation. It contains vector of
    action rule object references that were created on the server that satisfy the input criteria scope and schema
    format.
    
    :var actionRuleObjects: A list of action rule objects.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    actionRuleObjects: List[PIEActionRule] = ()
    serviceData: ServiceData = None


@dataclass
class GetAllTransferOptionSetsResponse(TcBaseObj):
    """
    The 'GetAllTransferOptionSetsResponse' structure defines the response from 'getAllTransferOptionSets' operation. It
    contains vector of transfer option set object references that were present on the server.
    
    :var optionSetObjects: A list of transfer option sets.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    optionSetObjects: List[TransferOptionSet] = ()
    serviceData: ServiceData = None


@dataclass
class GetAvailableTransferOptionSetsInputData(TcBaseObj):
    """
    The structure 'GetAvailableTransferOptionSetsInputData' defines input criteria for the operation
    'getAvailableTransferOptionSets'. The values of 'isPush', 'isExport' are to be known before calling this operation.
    
    Case 1: Remote Export    - on-line  --- 'isPush' = True   'isExport' = True
    Case 2: Remote Import    - on-line  --- 'isPush' = False  'isExport' = True
    Case 3: Briefcase Export - off-line --- 'isPush' = True   'isExport' = True
    case 4: Briefcase Import - off-line --- isPush = NA     isExport = False
    
    For 2007.1, the site can not be more than one for the Push case. The access rules will be evaluated thru RBF (Rules
    Based Framework) for the given user, group, role and all the option sets that satisfy the criteria will be returned
    
    :var user: The user reference that executing this API.
    :var group: The group reference that the executing user belongs to.
    :var role: The role reference that the executing user belongs to.
    :var site: The site that the user want to export to.
    :var isPush: Option that control the online or offline.
    :var isExport: Option that control the data transfer direction.
    """
    user: User = None
    group: Group = None
    role: Role = None
    site: List[POM_imc] = ()
    isPush: bool = False
    isExport: bool = False


@dataclass
class GetAvailableTransferOptionSetsResponse(TcBaseObj):
    """
    The 'GetAvailableTransferOptionSetsResponse' structure defines the response from 'getAvailableTransferOptionSets'
    operation. It contains vector of transfer option set object references that satisfies the input criteria.
    
    :var optionSetObjects: A list of transfer option set objects.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    optionSetObjects: List[TransferOptionSet] = ()
    serviceData: ServiceData = None


@dataclass
class GetClosureRulesResponse(TcBaseObj):
    """
    The 'GetClosureRulesResponse' structure defines the response from 'getClosureRules' operation. It contains vector
    of closure rule object references that were created on the server that satisfy the input criteria scope and schema
    format.
    
    :var closureRuleObjects: A list of closure rule objects.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    closureRuleObjects: List[ClosureRule] = ()
    serviceData: ServiceData = None


@dataclass
class GetFilterRulesResponse(TcBaseObj):
    """
    The 'GetFilterRulesResponse' structure defines the response from' getFilterRules' operation. It contains vector of
    filter rule object references that were created on the server that satisfy the input criteria scope and schema
    format.
    
    :var filterRuleObjects: A list of filter rule objects.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    filterRuleObjects: List[Filter] = ()
    serviceData: ServiceData = None


@dataclass
class GetPLMXMLRuleInputData(TcBaseObj):
    """
    The structure 'GetPLMXMLRuleInputData' is used for many operations related to PLMXML Admin application. This
    structure specifies input criteria for get list methods for Transfermode, closure rule, filter rule action rule.
    The get list operation is expected to return all rule objects based on the given scope and schema format.
    
    :var scope: The direction that scope rule is used. The allowed values are"EXPORT", "IMPORT" or "ALL". When the
    value is "EXPORT", only export based scope rules will be queried. Value "ALL" implies both export and import scope
    rules will be queried.
    :var schemaFormat: The schema format associated with the scope rule. The allowed values are "PLMXML" or  "TCXML" or
    "ALL". When the value is "PLMXML", only PLMXML based scope rules will be queried. Value "ALL" implies both PLMXML
    and TCXML scope rules will be queried.
    """
    scope: str = ''
    schemaFormat: str = ''


@dataclass
class GetPropertySetsResponse(TcBaseObj):
    """
    The 'GetPropertySetsResponse' structure defines the response from' getPropertySets' operation. It contains vector
    of property set object references that were created on the server that satisfy the input criteria scope. (Schema
    format is not applicable in input)
    
    :var propertySetObjects: A list of property set objects.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    propertySetObjects: List[PropertySet] = ()
    serviceData: ServiceData = None


@dataclass
class GetTransferModesResponse(TcBaseObj):
    """
    The 'GetTransferModesResponse' structure defines the response from 'getTransferModes' operation. It contains vector
    of transfer mode object references that were created on the server that satisfy the input criteria scope and schema
    format.
    
    :var transferModeObjects: A list of transfer mode objects.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    transferModeObjects: List[TransferMode] = ()
    serviceData: ServiceData = None


@dataclass
class NamesAndValue(TcBaseObj):
    """
    NameAndValue structure represents a generic name-value pair
    
    :var name: The name of the name-value pair
    :var value: The value of the name-value pair
    """
    name: str = ''
    value: str = ''


@dataclass
class OptionInputData(TcBaseObj):
    """
    Transfer Option Set is a the object which holds complete configuration
    information about the data transfer. It is basically collection of options.
    Options are grouped in UI to give better readability for the options
    The options will be grouped in GUI based on the group name. The default
    values will be true or false for 2007.1. If the readOnlyFlag is set on a
    particular option only "dba" can override the value during transfer. it will
    be shown to the regular user but read-only
    
    The OptionInputData structure defines complete data for one option (Symbol)
    
    :var realName: The real variable name that used in code.
    :var displayName: Specify the name that user see in the transfer option setting .
    :var description: The description for the transfer option.
    :var groupName: The group that the tranfer option belongs to in the whole transfer option set.
    :var defaultValue: The default value for this transfer option.
    :var readOnlyFlag: Specify that wheter this transfer option is modified in transfer option setting. If the value is
    true, this option will be unmodifiable in the transfer option setting.
    """
    realName: str = ''
    displayName: str = ''
    description: str = ''
    groupName: str = ''
    defaultValue: str = ''
    readOnlyFlag: bool = False


@dataclass
class RequestImportFromOfflinePackageResponse(TcBaseObj):
    """
    RequestImportFromOfflinePackageResponse structure defines the response from requestImportFromOfflinePackage
    operation. It contains message Id of the request and partial errors and objects that are imported.
    
    :var msgId: Message Id of this request, to be used to check the status import seesion run at Global Service.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors listed
    above in case of failure conditions.
    """
    msgId: str = ''
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateActionRuleInputData(TcBaseObj):
    """
    The 'CreateOrUpdateActionRuleInputData' specifies complete data for creating an action rule.
    
    :var name: The name of the action rule which can be 32 characters long.
    :var description: The description of the action rule which can be 240 characters long.
    :var scope: The action rule is for import or export.  The value can be "IMPORT" or "EXPORT".
    :var schemaFormat: The schema for the imported/exported xml file. The value can be "TCXML" or "PLMXML".
    :var actionLocation: The  location where the action happens. The value could be "PREACTION", "DURINGACTION" or
    "POSTACTION".
    :var actionName: The Function handler which will be invoked when this rule is executed. For how to create a
    function for a action rule, please refer to PLM XML Import Export Administration Guide.
    :var actionRuleToUpdate: Holds the reference of the action rule in case of modification.
    """
    name: str = ''
    description: str = ''
    scope: str = ''
    schemaFormat: str = ''
    actionLocation: str = ''
    actionName: str = ''
    actionRuleToUpdate: PIEActionRule = None


@dataclass
class CreateOrUpdateActionRuleResponse(TcBaseObj):
    """
    The 'CreateOrUpdateActionRuleResponse' structure defines the response from 'createOrUpdateActionRules' operation.
    It contains vector of action rule object references that were created on the server.
    
    :var actionRuleObjects: A list of created or modified action rule objects.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    actionRuleObjects: List[PIEActionRule] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateClosureRuleInputData(TcBaseObj):
    """
    The 'CreateOrUpdateClosureRuleInputData' specifies complete data for creating a closure rule.
    
    :var name: The name of the closure rule which can be 32 characters long.
    :var description: The description of the closure rule which can be 240 characters long.
    :var scope: The closure rule is for import or export.  The value can be "IMPORT" or "EXPORT".
    :var schemaFormat: The schema for the imported/exported xml file. The value can be "TCXML" or "PLMXML".
    :var comments: The comments for every clause in this closure rule which can be 240 characters long.
    :var depth: The depth for every clause in this closure rule.
    :var clauses: The clause contents of closure rule which can be 240 characters long.
    :var closureRuleToUpdate: Holds the reference of the closure rule in case of modification.
    """
    name: str = ''
    description: str = ''
    scope: str = ''
    schemaFormat: str = ''
    comments: List[str] = ()
    depth: List[int] = ()
    clauses: List[str] = ()
    closureRuleToUpdate: ClosureRule = None


@dataclass
class CreateOrUpdateClosureRuleResponse(TcBaseObj):
    """
    The 'CreateOrUpdateClosureRuleResponse' structure defines the response from 'createOrUpdateClosureRules' operation.
    It contains vector of closure rule object references that were created on the server.
    
    :var closureRuleObjects: A list of created or modified closure rule objects.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    closureRuleObjects: List[ClosureRule] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateFilterRuleInputData(TcBaseObj):
    """
    The 'CreateOrUpdateFilterRuleInputData' specifies complete data for creating a filter rule.
    
    :var name: The name of the filter rule which can be 32 characters long.
    :var description: The description of the filter rule which can be 240 characers long.
    :var scope: The filter rule is for import or export. The value can be "IMPORT" or "EXPORT".
    :var schemaFormat: The schema for the imported/exported xml file. The value can be "TCXML" or "PLMXML".
    :var clauses: The  clauses contents of filter rule which can be 128 characters long.
    :var filterRuleToUpdate: Holds the reference of the filter rule in case of modification.
    """
    name: str = ''
    description: str = ''
    scope: str = ''
    schemaFormat: str = ''
    clauses: List[str] = ()
    filterRuleToUpdate: Filter = None


@dataclass
class CreateOrUpdateFilterRuleResponse(TcBaseObj):
    """
    The 'CreateOrUpdateFilterRuleResponse' structure defines the response from 'createOrUpdateFilterRules' operation.
    It contains vector of filter rule object references that were created on the server.
    
    :var filterRuleObjects: A list of created or modified filter rule objects.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    filterRuleObjects: List[Filter] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdatePropertySetInputData(TcBaseObj):
    """
    The 'CreateOrUpdatePropertySetInputData' specifies complete data for creating a property set.
    
    :var name: The name of the property set which can be 32 characters long.
    :var description: The description of the property set which can be 240 characters long.
    :var scope: The property set is for import or export. The value can be "IMPORT" or "EXPORT".
    :var clauses: The clause contents of property set which can be 128 characters long.
    :var propertySetToUpdate: Holds the reference of the property set in case of modification.
    """
    name: str = ''
    description: str = ''
    scope: str = ''
    clauses: List[str] = ()
    propertySetToUpdate: PropertySet = None


@dataclass
class CreateOrUpdatePropertySetRuleResponse(TcBaseObj):
    """
    The 'CreateOrUpdatePropertySetResponse' structure defines the response from createOrUpdatePropertySets operation.
    It contains vector of property sets object references that were created on the server.
    
    :var propertySetObjects: A list of created or modified property set objects.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    propertySetObjects: List[PropertySet] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateTransferModeInputData(TcBaseObj):
    """
    The 'CreateOrUpdateTransferModeInputData' specifies complete data for creating a transfer mode.
    
    :var name: The name of the transfer mode which can be 128 characters long.
    :var description: The description of the transfer mode which can be 240 characters long.
    :var xsltFiles: The style sheet file reference for the transfer mode.
    :var configObjs: The revision rule reference for the transfer mode.
    :var actionList: The action rule reference for the transfer mode.
    :var tmToUpdate: Holds the reference of the transfer mode in case of modification.
    :var contextString: The context string used in export/import. The value can be 240 characters long.
    :var direction: Defines the transfer mode is for import or export.  The value can be "IMPORT" or "EXPORT".
    :var schemaFormat: The schema for the imported/exported xml file. The value can be "TCXML" or "PLMXML".
    :var isIncremental: Specifies whether transfermode can be used in incremental data transfer or not.
    :var isMultiSite: Specifies whether transfermode is multisite or not.
    :var closurerule: The closure rule reference for the transfer mode.
    :var filter: The filter rule reference for the transfer mode.
    :var propertyset: The property set reference for the transfer mode.
    """
    name: str = ''
    description: str = ''
    xsltFiles: List[ImanFile] = ()
    configObjs: List[BusinessObject] = ()
    actionList: List[BusinessObject] = ()
    tmToUpdate: TransferMode = None
    contextString: str = ''
    direction: str = ''
    schemaFormat: str = ''
    isIncremental: bool = False
    isMultiSite: bool = False
    closurerule: ClosureRule = None
    filter: Filter = None
    propertyset: PropertySet = None


@dataclass
class CreateOrUpdateTransferModeResponse(TcBaseObj):
    """
    The 'CreateOrUpdateTransferModeResponse' structure defines the response from 'createOrUpdateTransferModes'
    operation. It contains vector of transfer mode object references that were created on the server.
    
    :var transferModeObjects: A list of created or modified transfer mode objects.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    transferModeObjects: List[TransferMode] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateTransferOptionSetInputData(TcBaseObj):
    """
    The CreateOrUpdateTransferOptionSetInputData structure defines the input data for creating a
    TransferOptionSetObject.
    
    :var name: The name of the transfer opton set.
    :var description: The description of the transfer opton set.
    :var publiclyVisible: Specifies whether it is public or private. If the value is true, the transfer option set will
    be visibale and used for all user.
    :var siteId: Specifies the site reference (local site or remote site).
    :var transfermode: Specifies the transfer mode reference.
    :var options: The vector of options (See OptionInputData structure).
    :var optionSetObjectToModify: This holds the reference to transfer option set object in case of modification.
    """
    name: str = ''
    description: str = ''
    publiclyVisible: bool = False
    siteId: POM_imc = None
    transfermode: TransferMode = None
    options: List[OptionInputData] = ()
    optionSetObjectToModify: TransferOptionSet = None


@dataclass
class CreateOrUpdateTransferOptionSetResponse(TcBaseObj):
    """
    The CreateOrUpdateTransferOptionSetResponse structure defines the response from
    createOrUpdateTransferOptionSets operation. It contains vector of TransferOptionSet
    object references that were created on the server.
    
    :var transferOptionSets: A list of created or modified transfer option set objects.
    :var serviceData: Service data contains the list of created or modified objects and also the partial errors.
    """
    transferOptionSets: List[TransferOptionSet] = ()
    serviceData: ServiceData = None
