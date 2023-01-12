from tcsoa.gen.Internal_Administration._2013_05.services import UserManagementService as imp0
from tcsoa.gen.Internal_Administration._2014_10.services import UserManagementService as imp1
from tcsoa.gen.Internal_Administration._2018_11.services import SiteManagementService as imp2
from tcsoa.gen.Internal_Administration._2007_06.services import PreferenceManagementService as imp3
from tcsoa.gen.Internal_Administration._2018_06.services import PreferenceManagementService as imp4
from tcsoa.gen.Internal_Administration._2008_06.services import IRMService as imp5
from tcsoa.gen.Internal_Administration._2016_09.services import VolumeManagementService as imp6
from tcsoa.gen.Internal_Administration._2017_11.services import IRMService as imp7
from tcsoa.gen.Internal_Administration._2007_06.services import AuthorizationService as imp8
from tcsoa.gen.Internal_Administration._2019_06.services import UserManagementService as imp9
from tcsoa.gen.Internal_Administration._2012_10.services import OrganizationManagementService as imp10
from tcsoa.gen.Internal_Administration._2011_06.services import OrganizationManagementService as imp11
from tcsoa.gen.Internal_Administration._2009_10.services import PersonManagementService as imp12
from tcsoa.gen.Internal_Administration._2015_10.services import UserManagementService as imp13
from tcsoa.base import TcService


class UserManagementService(TcService):
    activateUsers2 = imp0.activateUsers2
    activateUsers3 = imp1.activateUsers2
    getGroupRoleViewModelRows = imp9.getGroupRoleViewModelRows
    resetUserPassword = imp13.resetUserPassword


class SiteManagementService(TcService):
    createOrUpdateSites = imp2.createOrUpdateSites


class PreferenceManagementService(TcService):
    createPreferenceCategories = imp3.createPreferenceCategories
    deletePreferenceCategories = imp4.deletePreferenceCategories
    deletePreferences = imp3.deletePreferences
    exportPreferences = imp3.exportPreferences
    getModifiedSitePreferences = imp3.getModifiedSitePreferences
    getNonSessionPreferences = imp3.getNonSessionPreferences
    importPreferences = imp3.importPreferences


class IRMService(TcService):
    getACLsByType = imp5.getACLsByType
    getAccessorsInfo = imp7.getAccessorsInfo


class VolumeManagementService(TcService):
    getAccessibleVolumes = imp6.getAccessibleVolumes


class AuthorizationService(TcService):
    getAuthorization = imp8.getAuthorization
    setAuthorization = imp8.setAuthorization


class OrganizationManagementService(TcService):
    getOrganizationGroupMembers = imp10.getOrganizationGroupMembers
    getOrganizationGroups = imp11.getOrganizationGroups


class PersonManagementService(TcService):
    getStringProperties = imp12.getStringProperties
    setStringProperties = imp12.setStringProperties
