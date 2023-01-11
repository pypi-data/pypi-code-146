from __future__ import annotations

from tcsoa.gen.Administration._2010_04.IRM import AccessorTypesResponse, PrivNamesInfoResponse, ACLInfoResponse, ExtraProtectionInfoResponse
from tcsoa.gen.BusinessObjects import BusinessObject, User
from tcsoa.gen.Administration._2010_04.DisciplineManagement import GetDisciplineResponse
from typing import List
from tcsoa.base import TcService


class IRMService(TcService):

    @classmethod
    def getAccessorTypes(cls) -> AccessorTypesResponse:
        """
        This operation can be used to get the names of all the Accessor Types in Teamcenter. Accessor Types are used to
        configure access privileges for different accessors in Access Control List (ACL) table in Access Manager
        Application. Examples for the Accessor Types are "World", "User", "Group", and "Role in Group".  For more
        information on the Accessor Types please refer to the Access Manager guide in Teamcenter documentation. The
        returned names from this operation will include both internal names and corresponding client locale specific
        localized display names of the Accessor Types.  The display names of the Accessor Types are used for displaying
        in the User Interface.  Whereas, the internal names of the Accessor Types are used for internal processing of
        the rule tree evaluation.
        
        Use cases:
        In general wherever the Accessor Type names need to be displayed this operation can be used. At present
        following use cases in Teamcenter Rich Application Client (RAC) calls this operation.
        
        - Display the Accessor Type names in Extra Protection information dialog.
        - Display the Accessor Type names in Effective ACL dialog.
        
        """
        return cls.execute_soa_method(
            method_name='getAccessorTypes',
            library='Administration',
            service_date='2010_04',
            service_name='IRM',
            params={},
            response_cls=AccessorTypesResponse,
        )

    @classmethod
    def getEffectiveACLInfo2(cls, objects: List[BusinessObject]) -> ACLInfoResponse:
        """
        This operation can be used to get the effective Access Control List (ACL) information for a list of business
        objects.  Effective ACL information displays the Access Control Entries (ACEs) that are applicable to the
        business object with respect to the user for whom access privileges are being evaluated on the object.
        Applicable ACEs are picked up from the ACLs that are configured against the Access Manager Rules which are
        evaluated to true for the given business object based on details like the object's type, object's class, object
        attributes, object status and project to which it is assigned.  By looking at the effective ACL table end user
        will be able to understand what privileges or granted, what privileges are denied for the user on the object
        and, what ACL and Accessor Type are involved in either granting or denying a particular access privilege. For
        more information on ACLs, ACEs, effective ACLs please refer to the Access Manager guide in Teamcenter.
        
        Use cases:
        ACL list dialog in Teamcenter Rich Application Client (RAC) calls this operation to get the effective ACL
        information.
        """
        return cls.execute_soa_method(
            method_name='getEffectiveACLInfo2',
            library='Administration',
            service_date='2010_04',
            service_name='IRM',
            params={'objects': objects},
            response_cls=ACLInfoResponse,
        )

    @classmethod
    def getExtraProtectionInfo2(cls, user: User, objects: List[BusinessObject]) -> ExtraProtectionInfoResponse:
        """
        This operation can be used to get the additional access protection information for a given user on a set of
        business objects.  Additional protection information can be used to understand what Named ACL, what Accessor
        and what AM rule path are involved in arriving at the verdict for an access privilege on a given object for the
        given user. This helps the user to understand why a particular privilege on the given object is granted or
        denied for the given user.  At present this information is displayed only in RAC client in the "Extra
        Protection Information" dialog.  This operation supports localization of privilege names, ACL names and
        Accessor type names.
        
        Use cases:
        "Extra Protection Information" dialog in Teamcenter Rich Application Client (RAC)  calls this operation.
        """
        return cls.execute_soa_method(
            method_name='getExtraProtectionInfo2',
            library='Administration',
            service_date='2010_04',
            service_name='IRM',
            params={'user': user, 'objects': objects},
            response_cls=ExtraProtectionInfoResponse,
        )

    @classmethod
    def getPrivilegeNames(cls) -> PrivNamesInfoResponse:
        """
        This operation can be used to get the internal names and corresponding display values of all the access
        privileges in Teamcenter.  The display names of the privileges are used to display the privilege names in the
        User Interface in client specific locale.  Whereas, the internal privilege names are used for internal
        processing of the rule tree evaluation. Below is the list of access privileges in Teamcenter release 10.0. For
        functional information on each of these privileges please refer to the Access Manager guide in Teamcenter
        documentation.
        
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
        
        Use cases:
        This operation can be used in general wherever the privilege names need to be displayed. At present following
        use cases in Teamcenter Rich Application Client (RAC) calls this operation.
        
        - Display the privilege names in Access dialog.
        - Display the privilege names in Extra Protection information dialog.
        - Display the privilege names in effective Access Control List (ACL) dialog.
        - Display the privilege tool tips in Named ACL panel.
        
        """
        return cls.execute_soa_method(
            method_name='getPrivilegeNames',
            library='Administration',
            service_date='2010_04',
            service_name='IRM',
            params={},
            response_cls=PrivNamesInfoResponse,
        )


class DisciplineManagementService(TcService):

    @classmethod
    def getDiscipline(cls, disciplineName: str) -> GetDisciplineResponse:
        """
        This operation gets the Discipline object with given name. If no discipline object is found with the given
        name, the returned discipline object would be null.
        """
        return cls.execute_soa_method(
            method_name='getDiscipline',
            library='Administration',
            service_date='2010_04',
            service_name='DisciplineManagement',
            params={'disciplineName': disciplineName},
            response_cls=GetDisciplineResponse,
        )
