from tcsoa.gen.Internal_Core._2018_11.services import LogicalObjectService as imp0
from tcsoa.gen.Internal_Core._2020_04.services import LogicalObjectService as imp1
from tcsoa.gen.Internal_Core._2017_11.services import LogicalObjectService as imp2
from tcsoa.gen.Internal_Core._2018_06.services import LogicalObjectService as imp3
from tcsoa.gen.Internal_Core._2020_01.services import ActiveModelerService as imp4
from tcsoa.gen.Internal_Core._2008_06.services import SessionService as imp5
from tcsoa.gen.Internal_Core._2008_06.services import FileManagementService as imp6
from tcsoa.gen.Internal_Core._2010_09.services import FileManagementService as imp7
from tcsoa.gen.Internal_Core._2008_06.services import DataManagementService as imp8
from tcsoa.gen.Internal_Core._2008_06.services import DispatcherManagementService as imp9
from tcsoa.gen.Internal_Core._2012_10.services import DataManagementService as imp10
from tcsoa.gen.Internal_Core._2008_03.services import SessionService as imp11
from tcsoa.gen.Internal_Core._2007_01.services import DataManagementService as imp12
from tcsoa.gen.Internal_Core._2010_09.services import DataManagementService as imp13
from tcsoa.gen.Internal_Core._2013_05.services import ProjectLevelSecurityService as imp14
from tcsoa.gen.Internal_Core._2007_06.services import ProjectLevelSecurityService as imp15
from tcsoa.gen.Internal_Core._2013_05.services import LicensingService as imp16
from tcsoa.gen.Internal_Core._2014_10.services import FileManagementService as imp17
from tcsoa.gen.Internal_Core._2017_05.services import FileManagementService as imp18
from tcsoa.gen.Internal_Core._2010_04.services import ProjectLevelSecurityService as imp19
from tcsoa.gen.Internal_Core._2007_12.services import SessionService as imp20
from tcsoa.gen.Internal_Core._2014_11.services import SessionService as imp21
from tcsoa.gen.Internal_Core._2013_05.services import PresentationManagementService as imp22
from tcsoa.gen.Internal_Core._2017_05.services import PresentationManagementService as imp23
from tcsoa.gen.Internal_Core._2017_11.services import TypeService as imp24
from tcsoa.gen.Internal_Core._2010_04.services import DataManagementService as imp25
from tcsoa.gen.Internal_Core._2017_11.services import DataManagementService as imp26
from tcsoa.gen.Internal_Core._2009_10.services import ThumbnailService as imp27
from tcsoa.gen.Internal_Core._2013_05.services import ThumbnailService as imp28
from tcsoa.gen.Internal_Core._2018_11.services import FileManagementService as imp29
from tcsoa.gen.Internal_Core._2012_02.services import DataManagementService as imp30
from tcsoa.gen.Internal_Core._2006_03.services import SessionService as imp31
from tcsoa.gen.Internal_Core._2011_06.services import ICTService as imp32
from tcsoa.gen.Internal_Core._2007_05.services import SessionService as imp33
from tcsoa.gen.Internal_Core._2016_10.services import DataManagementService as imp34
from tcsoa.gen.Internal_Core._2012_09.services import EnvelopeService as imp35
from tcsoa.gen.Internal_Core._2014_10.services import LicensingService as imp36
from tcsoa.gen.Internal_Core._2018_12.services import LicensingService as imp37
from tcsoa.gen.Internal_Core._2010_04.services import StructureManagementService as imp38
from tcsoa.gen.Internal_Core._2007_09.services import DataManagementService as imp39
from tcsoa.base import TcService


class LogicalObjectService(TcService):
    addIncludedLogicalObjects = imp0.addIncludedLogicalObjects
    addMemAndPresentedPropsWithWrite = imp1.addMemAndPresentedPropsWithWrite
    addMembersAndPresentedProps = imp2.addMembersAndPresentedProps
    addMembersAndPresentedProps2 = imp3.addMembersAndPresentedProps2
    createLogicalObjectTypes = imp2.createLogicalObjectTypes
    createLogicalObjectTypes2 = imp3.createLogicalObjectTypes2
    deleteLogicalObjectTypes = imp2.deleteLogicalObjectTypes
    deleteMembersAndPresentedProps = imp2.deleteMembersAndPresentedProps
    updateMembers = imp3.updateMembers


class ActiveModelerService(TcService):
    addPropertiesOnTypes = imp4.addPropertiesOnTypes
    createTypes = imp4.createTypes


class SessionService(TcService):
    cancelOperation = imp5.cancelOperation
    disableUserSessionState = imp11.disableUserSessionState
    getProperties = imp20.getProperties
    getSecurityToken = imp21.getSecurityToken
    initTypeByNames = imp31.initTypeByNames
    initTypeByUids = imp31.initTypeByUids
    refreshPOMCachePerRequestDeprecated = imp33.refreshPOMCachePerRequestDeprecated


class FileManagementService(TcService):
    commitRegularFiles = imp6.commitRegularFiles
    commitReplacedFiles = imp7.commitReplacedFiles
    getFileTransferTickets = imp6.getFileTransferTickets
    getPlmdFileTicketForDownload = imp17.getPlmdFileTicketForDownload
    getPlmdFileTicketForReplace = imp18.getPlmdFileTicketForReplace
    getPlmdFileTicketForUpload = imp17.getPlmdFileTicketForUpload
    getRegularFileTicketsForUpload = imp6.getRegularFileTicketsForUpload
    getTransientFileTicketsForDownload = imp29.getTransientFileTicketsForDownload
    getWriteTickets = imp6.getWriteTickets
    postCleanUpFileCommits = imp17.postCleanUpFileCommits
    updateImanFileCommits = imp6.updateImanFileCommits


class DataManagementService(TcService):
    createCachedRelations = imp8.createCachedRelations
    createRelateAndSubmitObjects = imp10.createRelateAndSubmitObjects
    getAttributeValues = imp12.getAttributeValues
    getDatasetFiles = imp13.getDatasetFiles
    getOrganizationInformation = imp12.getOrganizationInformation
    getSubscribableTypesAndSubTypes = imp25.getSubscribableTypesAndSubTypes
    getTCSessionAnalyticsInfo = imp26.getTCSessionAnalyticsInfo
    getViewableData = imp30.getViewableData
    multiRelationMultiLevelExpand = imp8.multiRelationMultiLevelExpand
    reviseObject = imp8.reviseObject
    reviseObjectsInBulk = imp34.reviseObjectsInBulk
    saveAsNewItemObject = imp8.saveAsNewItemObject
    saveAsObjectsInBulkAndRelate = imp34.saveAsObjectsInBulkAndRelate
    setDefaultProjectForProjectMembers = imp8.setDefaultProjectForProjectMembers
    whereUsedOccGroup = imp39.whereUsedOccGroup


class DispatcherManagementService(TcService):
    createDatasetOfVersion = imp9.createDatasetOfVersion
    insertDatasetVersion = imp9.insertDatasetVersion
    queryDispatcherRequests = imp9.queryDispatcherRequests
    updateDispatcherRequests = imp9.updateDispatcherRequests


class ProjectLevelSecurityService(TcService):
    getFilteredObjectsInProject = imp14.getFilteredObjectsInProject
    getFilteredProjectData = imp15.getFilteredProjectData
    getProjectsSmartFolderHierarchy = imp15.getProjectsSmartFolderHierarchy
    getProjectsSmartFolderHierarchy2 = imp19.getProjectsSmartFolderHierarchy2
    getTopLevelSmartFolderHierarchy = imp15.getTopLevelSmartFolderHierarchy


class LicensingService(TcService):
    getLicenseBundles = imp16.getLicenseBundles
    updateLicenseServer = imp36.updateLicenseServer
    updateLicenseServer2 = imp37.updateLicenseServer2


class PresentationManagementService(TcService):
    getSharedCommonClientFiles = imp22.getSharedCommonClientFiles
    getStylesheet = imp22.getStylesheet
    getStylesheetPerPage = imp23.getStylesheetPerPage


class TypeService(TcService):
    getSubTypeHierarchicalTrees = imp24.getSubTypeHierarchicalTrees


class ThumbnailService(TcService):
    getThumbnailFileTickets = imp27.getThumbnailFileTickets
    getThumbnailFileTickets2 = imp28.getThumbnailFileTickets2
    updateThumbnail = imp27.updateThumbnail


class ICTService(TcService):
    invokeICTMethod = imp32.invokeICTMethod


class EnvelopeService(TcService):
    sendEmail = imp35.sendEmail


class StructureManagementService(TcService):
    validateInStructureAssociations = imp38.validateInStructureAssociations
