from tcsoa.gen.Core._2014_10.services import DataManagementService as imp0
from tcsoa.gen.Core._2020_01.services import ProjectLevelSecurityService as imp1
from tcsoa.gen.Core._2008_06.services import DataManagementService as imp2
from tcsoa.gen.Core._2014_06.services import DigitalSignatureService as imp3
from tcsoa.gen.Core._2007_09.services import ProjectLevelSecurityService as imp4
from tcsoa.gen.Core._2017_05.services import ProjectLevelSecurityService as imp5
from tcsoa.gen.Core._2014_06.services import ReservationService as imp6
from tcsoa.gen.Core._2012_02.services import DataManagementService as imp7
from tcsoa.gen.Core._2006_03.services import ReservationService as imp8
from tcsoa.gen.Core._2006_03.services import DataManagementService as imp9
from tcsoa.gen.Core._2018_11.services import ProjectLevelSecurityService as imp10
from tcsoa.gen.Core._2006_03.services import FileManagementService as imp11
from tcsoa.gen.Core._2017_05.services import FileManagementService as imp12
from tcsoa.gen.Core._2008_03.services import SessionService as imp13
from tcsoa.gen.Core._2012_09.services import ProjectLevelSecurityService as imp14
from tcsoa.gen.Core._2007_12.services import DataManagementService as imp15
from tcsoa.gen.Core._2016_09.services import DataManagementService as imp16
from tcsoa.gen.Core._2010_04.services import DataManagementService as imp17
from tcsoa.gen.Core._2008_06.services import DispatcherManagementService as imp18
from tcsoa.gen.Core._2020_01.services import DataManagementService as imp19
from tcsoa.gen.Core._2008_06.services import StructureManagementService as imp20
from tcsoa.gen.Core._2018_06.services import DataManagementService as imp21
from tcsoa.gen.Core._2007_01.services import DataManagementService as imp22
from tcsoa.gen.Core._2010_09.services import DataManagementService as imp23
from tcsoa.gen.Core._2015_07.services import DataManagementService as imp24
from tcsoa.gen.Core._2007_01.services import ManagedRelationsService as imp25
from tcsoa.gen.Core._2007_06.services import DataManagementService as imp26
from tcsoa.gen.Core._2007_09.services import DataManagementService as imp27
from tcsoa.gen.Core._2016_05.services import DataManagementService as imp28
from tcsoa.gen.Core._2020_04.services import DataManagementService as imp29
from tcsoa.gen.Core._2013_05.services import DataManagementService as imp30
from tcsoa.gen.Core._2010_04.services import LanguageInformationService as imp31
from tcsoa.gen.Core._2007_06.services import LOVService as imp32
from tcsoa.gen.Core._2007_06.services import PropDescriptorService as imp33
from tcsoa.gen.Core._2011_06.services import PropDescriptorService as imp34
from tcsoa.gen.Core._2006_03.services import SessionService as imp35
from tcsoa.gen.Core._2011_06.services import SessionService as imp36
from tcsoa.gen.Core._2008_06.services import PropDescriptorService as imp37
from tcsoa.gen.Core._2012_10.services import DataManagementService as imp38
from tcsoa.gen.Core._2012_02.services import OperationDescriptorService as imp39
from tcsoa.gen.Core._2016_10.services import ProjectLevelSecurityService as imp40
from tcsoa.gen.Core._2015_10.services import FileManagementService as imp41
from tcsoa.gen.Core._2008_06.services import SessionService as imp42
from tcsoa.gen.Core._2013_05.services import LOVService as imp43
from tcsoa.gen.Core._2009_10.services import DataManagementService as imp44
from tcsoa.gen.Core._2011_06.services import LOVService as imp45
from tcsoa.gen.Core._2017_11.services import LogicalObjectService as imp46
from tcsoa.gen.Core._2018_06.services import LogicalObjectService as imp47
from tcsoa.gen.Core._2018_11.services import LogicalObjectService as imp48
from tcsoa.gen.Core._2008_06.services import ManagedRelationsService as imp49
from tcsoa.gen.Core._2007_01.services import SessionService as imp50
from tcsoa.gen.Core._2010_04.services import SessionService as imp51
from tcsoa.gen.Core._2011_06.services import OperationDescriptorService as imp52
from tcsoa.gen.Core._2011_06.services import DataManagementService as imp53
from tcsoa.gen.Core._2014_06.services import DataManagementService as imp54
from tcsoa.gen.Core._2007_01.services import FileManagementService as imp55
from tcsoa.gen.Core._2015_10.services import SessionService as imp56
from tcsoa.gen.Core._2009_10.services import ProjectLevelSecurityService as imp57
from tcsoa.gen.Core._2019_06.services import SessionService as imp58
from tcsoa.gen.Core._2009_04.services import ProjectLevelSecurityService as imp59
from tcsoa.gen.Core._2011_06.services import ReservationService as imp60
from tcsoa.gen.Core._2014_10.services import ProjectLevelSecurityService as imp61
from tcsoa.gen.Core._2015_10.services import DataManagementService as imp62
from tcsoa.gen.Core._2007_06.services import SessionService as imp63
from tcsoa.gen.Core._2012_02.services import SessionService as imp64
from tcsoa.gen.Core._2012_09.services import DataManagementService as imp65
from tcsoa.gen.Core._2011_06.services import EnvelopeService as imp66
from tcsoa.gen.Core._2007_12.services import SessionService as imp67
from tcsoa.gen.Core._2009_04.services import SessionService as imp68
from tcsoa.gen.Core._2008_06.services import ReservationService as imp69
from tcsoa.gen.Core._2019_06.services import DataManagementService as imp70
from tcsoa.gen.Core._2008_05.services import DataManagementService as imp71
from tcsoa.base import TcService


class DataManagementService(TcService):
    addChildren = imp0.addChildren
    addParticipants = imp2.addParticipants
    bulkCreateObjects = imp7.bulkCreateObjects
    changeOwnership = imp9.changeOwnership
    createAlternateIdentifiers = imp15.createAlternateIdentifiers
    createAttachAndSubmitObjects = imp16.createAttachAndSubmitObjects
    createConnections = imp2.createConnections
    createDatasets = imp9.createDatasets
    createDatasets2 = imp17.createDatasets
    createDatasets3 = imp2.createDatasets2
    createFolders = imp9.createFolders
    createIdDisplayRules = imp19.createIdDisplayRules
    createItems = imp9.createItems
    createObjects = imp2.createObjects
    createObjectsInBulkAndRelate = imp21.createObjectsInBulkAndRelate
    createOrUpdateForms = imp22.createOrUpdateForms
    createOrUpdateGDELinks = imp2.createOrUpdateGDELinks
    createOrUpdateItemElements = imp2.createOrUpdateItemElements
    createOrUpdateRelations = imp2.createOrUpdateRelations
    createOrUpdateStaticTableData = imp23.createOrUpdateStaticTableData
    createRelateAndSubmitObjects2 = imp24.createRelateAndSubmitObjects2
    createRelations = imp9.createRelations
    deleteObjects = imp9.deleteObjects
    deleteRelations = imp9.deleteRelations
    expandGRMRelationsForPrimary = imp26.expandGRMRelationsForPrimary
    expandGRMRelationsForPrimary2 = imp27.expandGRMRelationsForPrimary
    expandGRMRelationsForSecondary = imp26.expandGRMRelationsForSecondary
    expandGRMRelationsForSecondary2 = imp27.expandGRMRelationsForSecondary
    findDisplayableSubBusinessObjects = imp2.findDisplayableSubBusinessObjects
    findDisplayableSubBusinessObjectsWithDisplayNames = imp17.findDisplayableSubBusinessObjectsWithDisplayNames
    generateContextSpecificIDs = imp28.generateContextSpecificIDs
    generateContextSpecificIDs2 = imp29.generateContextSpecificIDs2
    generateIdsUsingIDGenerationRules = imp0.generateIdsUsingIDGenerationRules
    generateItemIdsAndInitialRevisionIds = imp9.generateItemIdsAndInitialRevisionIds
    generateNextValues = imp30.generateNextValues
    generateNextValuesForProperties = imp24.generateNextValuesForProperties
    generateRevisionIds = imp9.generateRevisionIds
    generateUID = imp22.generateUID
    getAvailableTypes = imp26.getAvailableTypes
    getAvailableTypesWithDisplayNames = imp17.getAvailableTypesWithDisplayNames
    getChildren = imp30.getChildren
    getContextsAndIdentifierTypes = imp15.getContextsAndIdentifierTypes
    getCreatbleSubBuisnessObjectNames = imp24.getCreatbleSubBuisnessObjectNames
    getDatasetCreationRelatedInfo = imp22.getDatasetCreationRelatedInfo
    getDatasetCreationRelatedInfo2 = imp17.getDatasetCreationRelatedInfo2
    getDatasetTypeInfo = imp26.getDatasetTypeInfo
    getDatasetTypesWithFileExtension = imp38.getDatasetTypesWithFileExtension
    getDeepCopyData = imp0.getDeepCopyData
    getDeepCopyData2 = imp24.getDeepCopyData
    getDomainOfObjectOrType = imp24.getDomainOfObjectOrType
    getEventTypes = imp23.getEventTypes
    getIdContexts = imp19.getIdContexts
    getIdentifierTypes = imp19.getIdentifierTypes
    getItemAndRelatedObjects = imp2.getItemAndRelatedObjects
    getItemCreationRelatedInfo = imp22.getItemCreationRelatedInfo
    getItemFromAttribute = imp44.getItemFromAttribute
    getItemFromId = imp22.getItemFromId
    getLocalizedProperties = imp17.getLocalizedProperties
    getLocalizedProperties2 = imp24.getLocalizedProperties2
    getNRPatternsWithCounters = imp2.getNRPatternsWithCounters
    getNextIds = imp2.getNextIds
    getPasteRelations = imp30.getPasteRelations
    getPasteRelations2 = imp0.getPasteRelations2
    getProperties = imp9.getProperties
    getRevNRAttachDetails = imp2.getRevNRAttachDetails
    getStaticTableData = imp23.getStaticTableData
    getSubTypeNames = imp30.getSubTypeNames
    getTableProperties = imp44.getTableProperties
    getTraceReport = imp53.getTraceReport
    getTraceReport2 = imp38.getTraceReport
    getTraceReport3 = imp54.getTraceReport2
    getTraceReportLegacy = imp54.getTraceReportLegacy
    isPropertyLocalizable = imp17.isPropertyLocalizable
    listAlternateIdDisplayRules = imp15.listAlternateIdDisplayRules
    loadObjects = imp27.loadObjects
    moveToNewFolder = imp22.moveToNewFolder
    postEvent = imp23.postEvent
    pruneNamedReferences = imp0.pruneNamedReferences
    purgeSequences = imp26.purgeSequences
    reassignParticipants = imp62.reassignParticipants
    refreshObjects = imp22.refreshObjects
    refreshObjects2 = imp38.refreshObjects2
    removeChildren = imp0.removeChildren
    removeNamedReferenceFromDataset = imp27.removeNamedReferenceFromDataset
    removeParticipants = imp2.removeParticipants
    resetContextID = imp28.resetContextID
    revise = imp9.revise
    revise2 = imp2.revise2
    reviseObjects = imp30.reviseObjects
    saveAsNewItem = imp22.saveAsNewItem
    saveAsNewItem2 = imp2.saveAsNewItem2
    saveAsObjectAndRelate = imp65.saveAsObjectAndRelate
    saveAsObjects = imp53.saveAsObjects
    saveAsObjectsAndRelate = imp0.saveAsObjectsAndRelate
    setDisplayProperties = imp9.setDisplayProperties
    setLocalizedProperties = imp17.setLocalizedProperties
    setLocalizedPropertyValues = imp17.setLocalizedPropertyValues
    setOrRemoveImmunity = imp26.setOrRemoveImmunity
    setProperties = imp22.setProperties
    setProperties2 = imp23.setProperties
    setPropertiesAndDetectOverwrite = imp28.setPropertiesAndDetectOverwrite
    setTableProperties = imp44.setTableProperties
    unlinkAndDeleteObjects = imp70.unlinkAndDeleteObjects
    unloadObjects = imp71.unloadObjects
    validateAlternateIds = imp15.validateAlternateIds
    validateIdValue = imp7.validateIdValue
    validateItemIdsAndRevIds = imp26.validateItemIdsAndRevIds
    validateRevIds = imp53.validateRevIds
    validateValues = imp30.validateValues
    verifyExtension = imp23.verifyExtension
    whereReferenced = imp22.whereReferenced
    whereReferencedByRelationName = imp26.whereReferencedByRelationName
    whereUsed = imp22.whereUsed
    whereUsed2 = imp7.whereUsed


class ProjectLevelSecurityService(TcService):
    addOrRemoveProjectMembers = imp1.addOrRemoveProjectMembers
    assignOrRemoveObjects = imp4.assignOrRemoveObjects
    assignOrRemoveObjectsFromProjects = imp5.assignOrRemoveObjectsFromProjects
    changeOwningProgram = imp10.changeOwningProgram
    copyProjects = imp14.copyProjects
    copyProjects2 = imp5.copyProjects2
    createProjects = imp14.createProjects
    createProjects2 = imp5.createProjects2
    getDefaultProject = imp40.getDefaultProject
    getFirstLevelProjectTeamStructure = imp1.getFirstLevelProjectTeamStructure
    getModifiableProjects = imp1.getModifiableProjects
    getPrivilegeInProjects = imp1.getPrivilegeInProjects
    getProjectTeamChildNodes = imp1.getProjectTeamChildNodes
    getProjectTeams = imp14.getProjectTeams
    getProjectsForAssignOrRemove = imp5.getProjectsForAssignOrRemove
    getUserProjects = imp57.getUserProjects
    getUserProjects2 = imp10.getUserProjects2
    loadProjectDataForUser = imp59.loadProjectDataForUser
    modifyProjects = imp14.modifyProjects
    modifyProjects2 = imp5.modifyProjects2
    propagateData = imp61.propagateData
    setPropagationEnabledProperties = imp5.setPropagationEnabledProperties
    setUserPrivilege = imp1.setUserPrivilege


class DigitalSignatureService(TcService):
    applySignatures = imp3.applySignatures
    getSignatureMessages = imp3.getSignatureMessages
    voidSignatures = imp3.voidSignatures


class ReservationService(TcService):
    bulkCancelCheckout = imp6.bulkCancelCheckout
    bulkCheckin = imp6.bulkCheckin
    bulkCheckout = imp6.bulkCheckout
    cancelCheckout = imp8.cancelCheckout
    checkin = imp8.checkin
    checkout = imp8.checkout
    getReservationHistory = imp8.getReservationHistory
    okToCheckout = imp60.okToCheckout
    transferCheckout = imp69.transferCheckout


class FileManagementService(TcService):
    commitDatasetFiles = imp11.commitDatasetFiles
    commitDatasetFilesInBulk = imp12.commitDatasetFilesInBulk
    getDatasetWriteTickets = imp11.getDatasetWriteTickets
    getDigestInfoForDatasets = imp41.getDigestInfoForDatasets
    getDigestInfoForFiles = imp41.getDigestInfoForFiles
    getFileReadTickets = imp11.getFileReadTickets
    getTransientFileTicketsForUpload = imp55.getTransientFileTicketsForUpload
    replaceFiles = imp12.replaceFiles


class SessionService(TcService):
    connect = imp13.connect
    getAvailableServices = imp35.getAvailableServices
    getClientCacheData = imp36.getClientCacheData
    getDisplayStrings = imp42.getDisplayStrings
    getFavorites = imp13.getFavorites
    getGroupMembership = imp35.getGroupMembership
    getPreferences = imp35.getPreferences
    getPreferences2 = imp50.getPreferences
    getPreferences3 = imp51.getPreferences2
    getSessionGroupMember = imp35.getSessionGroupMember
    getShortcuts = imp51.getShortcuts
    getTCSessionInfo = imp50.getTCSessionInfo
    getTypeDescriptions = imp36.getTypeDescriptions
    getTypeDescriptions2 = imp56.getTypeDescriptions2
    licenseAdmin = imp58.licenseAdmin
    login = imp35.login
    login2 = imp42.login
    login3 = imp36.login
    loginSSO = imp35.loginSSO
    loginSSO2 = imp42.loginSSO
    loginSSO3 = imp36.loginSSO
    logout = imp35.logout
    refreshPOMCachePerRequest = imp63.refreshPOMCachePerRequest
    registerState = imp64.registerState
    setAndEvaluateIdDisplayRule = imp67.setAndEvaluateIdDisplayRule
    setFavorites = imp13.setFavorites
    setObjectPropertyPolicy = imp50.setObjectPropertyPolicy
    setObjectPropertyPolicy2 = imp42.setObjectPropertyPolicy
    setObjectPropertyPolicy3 = imp64.setObjectPropertyPolicy
    setPreferences = imp35.setPreferences
    setSessionGroupMember = imp35.setSessionGroupMember
    setUserSessionState = imp67.setUserSessionState
    setUserSessionStateAndUpdateDefaults = imp56.setUserSessionStateAndUpdateDefaults
    sponsoredLogin = imp56.sponsoredLogin
    sponsoredLoginSSO = imp56.sponsoredLoginSSO
    startOperation = imp68.startOperation
    stopOperation = imp68.stopOperation
    unregisterState = imp64.unregisterState
    updateObjectPropertyPolicy = imp36.updateObjectPropertyPolicy


class DispatcherManagementService(TcService):
    createDispatcherRequest = imp18.createDispatcherRequest


class StructureManagementService(TcService):
    createInStructureAssociations = imp20.createInStructureAssociations
    getPrimariesOfInStructureAssociation = imp20.getPrimariesOfInStructureAssociation
    getSecondariesOfInStructureAssociation = imp20.getSecondariesOfInStructureAssociation
    removeInStructureAssociations = imp20.removeInStructureAssociations


class ManagedRelationsService(TcService):
    createRelation = imp25.createRelation
    getManagedRelations = imp49.getManagedRelations
    getTraceReport = imp25.getTraceReport
    modifyRelation = imp25.modifyRelation


class LanguageInformationService(TcService):
    getAllTranslationStatuses = imp31.getAllTranslationStatuses
    getLanguagesList = imp31.getLanguagesList


class LOVService(TcService):
    getAttachedLOVs = imp32.getAttachedLOVs
    getInitialLOVValues = imp43.getInitialLOVValues
    getLOVAttachments = imp45.getLOVAttachments
    getNextLOVValues = imp43.getNextLOVValues
    validateLOVValueSelections = imp43.validateLOVValueSelections


class PropDescriptorService(TcService):
    getAttachedPropDescs = imp33.getAttachedPropDescs
    getAttachedPropDescs2 = imp34.getAttachedPropDescs2
    getCreateDesc = imp37.getCreateDesc


class OperationDescriptorService(TcService):
    getDeepCopyData = imp39.getDeepCopyData
    getSaveAsDesc = imp52.getSaveAsDesc


class LogicalObjectService(TcService):
    getLogicalObjects = imp46.getLogicalObjects
    getLogicalObjects2 = imp47.getLogicalObjects2
    getLogicalObjectsWithContext = imp48.getLogicalObjectsWithContext


class EnvelopeService(TcService):
    sendAndDeleteEnvelopes = imp66.sendAndDeleteEnvelopes
