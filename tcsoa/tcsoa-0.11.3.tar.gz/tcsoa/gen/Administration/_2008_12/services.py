from __future__ import annotations

from tcsoa.gen.BusinessObjects import User, Group, Role
from typing import List
from tcsoa.gen.Administration._2007_06.Authorization import NameAuthorizationList, NameInfo
from tcsoa.base import TcService


class AuthorizationService(TcService):

    @classmethod
    def checkAuthorizationAccess(cls, user: User, group: Group, role: Role, inputNames: List[NameInfo]) -> NameAuthorizationList:
        """
        This operation can be used to get authorization access on the given applications and utilities for the given
        user, group and role combination. Rule domain specifies accessibility need to be checked on an application or
        on a utility. Valid values for the domain are "utility" and "application".  If some other string is specified
        as rule domain this operation will return error code 290006.  However accessibility check for correct domain
        names will continue. Following are the valid application names and utility names for this operation. For more
        information on authorization rules please refer to Authorization guide in Teamcenter documentation.
        
        List of application IDs:
        Organization
        Business_Modeler_IDE
        Access_Manager
        Archive_Restore
        Setup_Wizard
        Workflow_Designer
        PLMXML_Import_Export
        Project
        Subscription_Monitor
        Classification_Admin
        Report_Designer
        Application_Configuration
        EIntegrator_Admin
        Audit_Manager
        Authorization
        Schema_Editor
        Appearance_Configuration
        ADA License
        
        List of utility IDs:
        data_share
        export_recovery
        database_verify
        update_project_data
        data_sync
        dsa_util
        import_export_business_rules
        purge_invalid_subscriptions
        create_change_types
        fsc_admin
        ada_util
        attribute_export
        
        Use cases:
        To check user's accessibility.
        
        - While opening an admin application.
        - While running an admin utility
        
        """
        return cls.execute_soa_method(
            method_name='checkAuthorizationAccess',
            library='Administration',
            service_date='2008_12',
            service_name='Authorization',
            params={'user': user, 'group': group, 'role': role, 'inputNames': inputNames},
            response_cls=NameAuthorizationList,
        )
