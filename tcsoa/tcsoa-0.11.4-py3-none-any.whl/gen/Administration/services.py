from tcsoa.gen.Administration._2008_03.services import IRMService as imp0
from tcsoa.gen.Administration._2017_05.services import GroupManagementService as imp1
from tcsoa.gen.Administration._2017_05.services import RoleManagementService as imp2
from tcsoa.gen.Administration._2017_05.services import UserManagementService as imp3
from tcsoa.gen.Administration._2006_03.services import IRMService as imp4
from tcsoa.gen.Administration._2007_06.services import AuthorizationService as imp5
from tcsoa.gen.Administration._2008_12.services import AuthorizationService as imp6
from tcsoa.gen.Administration._2007_01.services import UserManagementService as imp7
from tcsoa.gen.Administration._2015_07.services import UserManagementService as imp8
from tcsoa.gen.Administration._2012_09.services import PreferenceManagementService as imp9
from tcsoa.gen.Administration._2016_03.services import UserManagementService as imp10
from tcsoa.gen.Administration._2012_10.services import IRMService as imp11
from tcsoa.gen.Administration._2010_04.services import IRMService as imp12
from tcsoa.gen.Administration._2016_10.services import UserManagementService as imp13
from tcsoa.gen.Administration._2010_04.services import DisciplineManagementService as imp14
from tcsoa.gen.Administration._2018_11.services import IRMService as imp15
from tcsoa.gen.Administration._2018_11.services import OrganizationManagementService as imp16
from tcsoa.gen.Administration._2012_09.services import UserManagementService as imp17
from tcsoa.gen.Administration._2008_06.services import PreferenceManagementService as imp18
from tcsoa.gen.Administration._2014_10.services import UserManagementService as imp19
from tcsoa.gen.Administration._2011_05.services import PreferenceManagementService as imp20
from tcsoa.gen.Administration._2007_06.services import PreferenceManagementService as imp21
from tcsoa.gen.Administration._2015_03.services import UserManagementService as imp22
from tcsoa.base import TcService


class IRMService(TcService):
    activateUsers = imp0.activateUsers
    checkAccessorsPrivileges = imp4.checkAccessorsPrivileges
    deactivateUsers = imp0.deactivateUsers
    getAMImpactedObjects = imp11.getAMImpactedObjects
    getAccessorTypes = imp12.getAccessorTypes
    getEffectiveACLInfo = imp4.getEffectiveACLInfo
    getEffectiveACLInfo2 = imp12.getEffectiveACLInfo2
    getExtraProtectionInfo = imp4.getExtraProtectionInfo
    getExtraProtectionInfo2 = imp12.getExtraProtectionInfo2
    getPrivilegeNames = imp12.getPrivilegeNames
    getSessionInfoFromTicket = imp15.getSessionInfoFromTicket
    getSessionInfoTicket = imp15.getSessionInfoTicket
    getSessionValues = imp11.getSessionValues
    removeAccessor = imp4.removeAccessor
    setPrivileges = imp4.setPrivileges


class GroupManagementService(TcService):
    addChildGroups = imp1.addChildGroups


class RoleManagementService(TcService):
    addRolesToGroup = imp2.addRolesToGroup
    removeRolesFromGroup = imp2.removeRolesFromGroup


class UserManagementService(TcService):
    addUsersAsGroupMembers = imp3.addUsersAsGroupMembers
    createDisciplines = imp7.createDisciplines
    createOrUpdateUser = imp8.createOrUpdateUser
    deleteUser = imp10.deleteUser
    getCurrentCountryPageInfo = imp13.getCurrentCountryPageInfo
    getUserGroupMembers = imp17.getUserGroupMembers
    makeUser = imp19.makeUser
    removeGroupMembers = imp3.removeGroupMembers
    saveAndValidateCurrentCountry = imp13.saveAndValidateCurrentCountry
    setGroupMemberProperties = imp17.setGroupMemberProperties
    setUserProfileProperties = imp22.setUserProfileProperties


class AuthorizationService(TcService):
    checkAuthorization = imp5.checkAuthorization
    checkAuthorizationAccess = imp6.checkAuthorizationAccess


class PreferenceManagementService(TcService):
    deletePreferenceDefinitions = imp9.deletePreferenceDefinitions
    deletePreferencesAtLocations = imp9.deletePreferencesAtLocations
    getPreferences = imp9.getPreferences
    getPreferencesAtLocations = imp9.getPreferencesAtLocations
    importPreferencesAtLocationDryRun = imp9.importPreferencesAtLocationDryRun
    importPreferencesAtLocations = imp9.importPreferencesAtLocations
    lockSitePreferences = imp18.lockSitePreferences
    refreshPreferences = imp20.refreshPreferences
    removeStalePreferenceInstancesAtLocations = imp9.removeStalePreferenceInstancesAtLocations
    setPreferences = imp21.setPreferences
    setPreferences2 = imp9.setPreferences2
    setPreferencesAtLocations = imp9.setPreferencesAtLocations
    setPreferencesDefinition = imp9.setPreferencesDefinition
    unlockSitePreferences = imp18.unlockSitePreferences


class DisciplineManagementService(TcService):
    getDiscipline = imp14.getDiscipline


class OrganizationManagementService(TcService):
    getUserConsentStatement = imp16.getUserConsentStatement
    recordUserConsent = imp16.recordUserConsent
