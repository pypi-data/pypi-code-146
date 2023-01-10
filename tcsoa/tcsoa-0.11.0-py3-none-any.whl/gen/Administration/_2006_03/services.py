from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, User
from tcsoa.gen.Administration._2006_03.IRM import GetProtectionReportResponse, PrivilegeSettingInput, GetACLInfoResponse, CheckAccessorPrivilegesResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class IRMService(TcService):

    @classmethod
    def removeAccessor(cls, objects: List[BusinessObject], accessorType: str, accessorId: str) -> ServiceData:
        """
        This operation removes the specified accessors from the given objects. Objects in the given list can be either
        AM_ACL (named Access Control List) objects or POM_application_object. If the object is a named ACL then the
        Access Control Entry (ACE)  from the named ACL is removed.  If the object is a POM_application_object then
        object ACL entry with the specified accessor type and accessor id is removed.  Objects on which given accessor
        is removed successfully are returned in the updated list of the ServiceData.  Objects on which accessor removal
        resulted in an error are returned in the list of failures in the ServiceData.  Invalid accessor type and
        accessor ID will result in error code 525120.
        
        Use cases:
        Modifying a Named ACL or removing an object ACL from Teamcenter Rich Application Client (RAC) calls this
        operation.
        """
        return cls.execute_soa_method(
            method_name='removeAccessor',
            library='Administration',
            service_date='2006_03',
            service_name='IRM',
            params={'objects': objects, 'accessorType': accessorType, 'accessorId': accessorId},
            response_cls=ServiceData,
        )

    @classmethod
    def setPrivileges(cls, privilegeSettings: List[PrivilegeSettingInput], accessorType: str, accessorId: str) -> ServiceData:
        """
        This operation can be used to grant or deny a set of privileges to the specified accessor type and accessor id
        on the given object.  Either a named Access Control List (ACL) or a POM_application_object can be submitted as
        input to this operation.  If the object is a POM_application_object then an object ACL will be added on the
        object. If the object is a named ACL then an ACE entry is either modified or added to the named ACL. For
        invalid Accessor type and Accessor Id this operation will return the error 525101.
        
        Use cases:
        - Updating named ACL objects by either modifying existing ACE entries or by adding new ACE entries for the
        specified accessor.
        - Adding new object ACLs on a POM_application_object for the specified accesor.
        
        """
        return cls.execute_soa_method(
            method_name='setPrivileges',
            library='Administration',
            service_date='2006_03',
            service_name='IRM',
            params={'privilegeSettings': privilegeSettings, 'accessorType': accessorType, 'accessorId': accessorId},
            response_cls=ServiceData,
        )

    @classmethod
    def getEffectiveACLInfo(cls, objects: List[BusinessObject]) -> GetACLInfoResponse:
        """
        This operation can be used to get the effective Access Control List (ACL) information.  Effective ACL
        information displays the Access Control Entries (ACEs) that are applicable to the business object with respect
        to the user for whom access privileges are being evaluated on the object. Applicable ACEs are picked up from
        the ACLs that are configured against the Access Manager Rules which are evaluated to true for the given object
        based on the object's type, class, attributes, status and project to which it is assigned to etc.  By looking
        at the effective ACL table end user will be able to understand what privileges or granted, what privileges are
        denied for the user on the object and, what ACL and Accessor Type are involved in either granting or denying a
        particular access privilege. This operation can be used to get all the information required to render the
        effective ACL table. Limitation with this operation is it does not support localization. Hence all the strings
        returned by this or internal values. For more information on ACLs, ACEs, effective ACLs please refer to the
        Access Manager guide in Teamcenter.
        
        Use cases:
        ACL list dialog in Teamcenter Rich Application Client (RAC) used to call this operation to get the effective
        ACL information before it was replaced with the new operation getEffectiveACLInfo2 that supports localization
        of ACL names, Accessor type names and privilege names.
        """
        return cls.execute_soa_method(
            method_name='getEffectiveACLInfo',
            library='Administration',
            service_date='2006_03',
            service_name='IRM',
            params={'objects': objects},
            response_cls=GetACLInfoResponse,
        )

    @classmethod
    def getExtraProtectionInfo(cls, user: User, objects: List[BusinessObject]) -> GetProtectionReportResponse:
        """
        This operation can be used to get the additional access protection information for a given user on a set of
        business objects.  Additional protection information can be used to understand what Named ACL, what Accessor
        and what AM rule path are involved in arriving at the verdict for an access privilege on a given object for the
        given user. This helps the user to understand why a particular privilege on the given object is granted or
        denied for the given user.  This operation does not support localization. Hence all the strings returned by
        this operation are internal values.  This operation is replaced by a new operation getExtraProtectionInfo2 that
        supports localization.
        
        Use cases:
        Extra Protection Information dialog in Teamcenter Rich Application Client (RAC) used to call this operation
        before it was replaced with the new operation getExtraProtectionInfo2 that supports localization.
        """
        return cls.execute_soa_method(
            method_name='getExtraProtectionInfo',
            library='Administration',
            service_date='2006_03',
            service_name='IRM',
            params={'user': user, 'objects': objects},
            response_cls=GetProtectionReportResponse,
        )

    @classmethod
    def checkAccessorsPrivileges(cls, groupMember: BusinessObject, objects: List[BusinessObject], privilegeNames: List[str]) -> CheckAccessorPrivilegesResponse:
        """
        This operation gets the verdicts for the given access privileges for the given GroupMember on the given set of
        business objects.  This operation finds the accessors for the combination of given groupMember's user, role and
        group and then uses the list of found accessors to determine the verdicts for the given access privileges for
        the given GroupMember on the given business objects. The business objects can be any POM_object.  Privilege
        Names must be internal names of the Access Manager AM_Privilege objects.  If a privilege object with any of the
        given names does not exist in the system then this operation will return the error 525101.  However, evaluation
        of the valid privilege names will continue. Following are the list of valid privilege names. For functional
        description about these privileges please refer to the Access Manager guide in Teamcenter documentation.
        
        ADD_CONTENT
        ASSIGN_TO_PROJECT
        Administer_ADA_Licenses
        BATCH_PRINT
        CHANGE
        CHANGE_OWNER
        CICO
        COPY
        DELETE
        DEMOTE
        DIGITAL_SIGN
        EXPORT
        IMPORT
        IP_ADMIN
        IP_Classifier
        ITAR_ADMIN
        ITAR_Classifier
        MARKUP
        PROMOTE
        PUBLISH
        READ
        REMOTE_CICO
        REMOVE_CONTENT
        REMOVE_FROM_PROJECT
        SUBSCRIBE
        TRANSFER_IN
        TRANSFER_OUT
        TRANSLATION
        UNMANAGE
        WRITE
        WRITE_ICOS
        """
        return cls.execute_soa_method(
            method_name='checkAccessorsPrivileges',
            library='Administration',
            service_date='2006_03',
            service_name='IRM',
            params={'groupMember': groupMember, 'objects': objects, 'privilegeNames': privilegeNames},
            response_cls=CheckAccessorPrivilegesResponse,
        )
