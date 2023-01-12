from __future__ import annotations

from tcsoa.gen.Internal.GlobalMultiSite._2020_01.Briefcase import RemoveMarkOTResponse, AddMarkOTResponse, QueryMarkOTResponse, GetObjectsLockInfoResponse
from typing import List
from tcsoa.gen.Internal.GlobalMultiSite._2020_01.OwnershipRecovery import RecoverOwnershipResponse, OtTransactionResponse, OtSearchInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class BriefcaseService(TcService):

    @classmethod
    def queryMarkOT(cls, objects: List[str], userId: str, targetSiteId: int, needHelperObjects: bool, appId: str) -> QueryMarkOTResponse:
        """
        This operation queries for marks of briefcase ownership transfer. All the input parameters are the search
        criteria.
        
        Use cases:
        &bull;    A user logs into Teamcenter RAC and opens the view "Briefcase Ownership Transfer".
        &bull;    The view "Briefcase Ownership Transfer" calls this operation to query the OT marks owned by the
        current user. 
        &bull;    The operation returns all found OT marks owned by the logged in user.
        &bull;    The returned OT marks are displayed in "Briefcase Ownership Transfer" view.
        """
        return cls.execute_soa_method(
            method_name='queryMarkOT',
            library='Internal-GlobalMultiSite',
            service_date='2020_01',
            service_name='Briefcase',
            params={'objects': objects, 'userId': userId, 'targetSiteId': targetSiteId, 'needHelperObjects': needHelperObjects, 'appId': appId},
            response_cls=QueryMarkOTResponse,
        )

    @classmethod
    def removeMarkOTForCurrentUser(cls, objects: List[str], appId: str) -> RemoveMarkOTResponse:
        """
        This operation removes the marks for briefcase ownership transfer. The following search criteria are used to
        search for marks and remove them.
        &bull;    A list of business object UID to search marks on them. 
        &bull;    Owned by the current logged user.
        &bull;    Application ID. If the value is empty, the operation searches marks owned by all applications.
        
        Use cases:
        &bull;    A user logs into Teamcenter RAC and open the view "Briefcase Ownership Transfer". 
        &bull;    Business objects with marks for Briefcase ownership transfer are display in this view.
        &bull;    A user chooses one or multiple objects and clicks the "Remove" button.
        &bull;    RAC calls this operation and send the selected business objects as input.
        &bull;    Application ID with the value "BC" is the input parameter for this operation too.
        &bull;    The operation removes all the marks found on the given business objects and the application id.
        &bull;    After this operation is completed, RAC calls another service operation "queryMarkOT" to refresh marks
        in the view "Briefcase Ownership Transfer".
        """
        return cls.execute_soa_method(
            method_name='removeMarkOTForCurrentUser',
            library='Internal-GlobalMultiSite',
            service_date='2020_01',
            service_name='Briefcase',
            params={'objects': objects, 'appId': appId},
            response_cls=RemoveMarkOTResponse,
        )

    @classmethod
    def addMarkOTForCurrentUser(cls, objects: List[str], targetSiteId: int, appId: str) -> AddMarkOTResponse:
        """
        This operation adds marks to the specific business objects to lock them for briefcase ownership transfer. The
        marks are owned by the current user only. After the marks are applied, other users cannot modify the objects or
        mark them for ownership. The marks exist after the owning user logs out Teamcenter. The marks can be removed
        after briefcase export is completed or be removed explicitly from Briefcase ownership transfer view.
        
        Use cases:
        &bull;    A user logs in to Teamcenter RAC.
        &bull;    In "My Teamcenter" application, one or multiple items are selected. In right-click context menu
        window, the menu "Mark for Ownership Transfer" is clicked.
        &bull;    RAC first calls the service operation "getObjectsLockInfo" to get locks from the selected business
        objects.
        &bull;    If no locks are found, this operation is called to add marks on these selected business objects.
        &bull;    The operation first adds T locks on these objects. Then it adds ownership transfer marks on these
        objects.
        &bull;    The operation returns the success and failure information.
        &bull;    RAC displays the failure information.
        &bull;    The successful locked business objects are displayed in the view "Briefcase Ownership Transfer".
        """
        return cls.execute_soa_method(
            method_name='addMarkOTForCurrentUser',
            library='Internal-GlobalMultiSite',
            service_date='2020_01',
            service_name='Briefcase',
            params={'objects': objects, 'targetSiteId': targetSiteId, 'appId': appId},
            response_cls=AddMarkOTResponse,
        )

    @classmethod
    def getObjectsLockInfo(cls, objects: List[str]) -> GetObjectsLockInfoResponse:
        """
        This operation queries for modification locks on the specific business objects.
        
        Use cases:
        &bull;    A user logs in to Teamcenter RAC.
        &bull;    In My Teamcenter application, he selects one or several items and right click. A context menu window
        pops up and he clicks the menu "Mark for Ownership Transfer".
        &bull;    RAC calls the operation and uses the selected items as input parameter.
        &bull;    The operation returns the found M locks and T locks on the specified business objects.
        """
        return cls.execute_soa_method(
            method_name='getObjectsLockInfo',
            library='Internal-GlobalMultiSite',
            service_date='2020_01',
            service_name='Briefcase',
            params={'objects': objects},
            response_cls=GetObjectsLockInfoResponse,
        )


class OwnershipRecoveryService(TcService):

    @classmethod
    def recoverOwnership(cls, transactionId: str, dryRun: bool) -> RecoverOwnershipResponse:
        """
        Recovers the ownership of all the objects associated with the briefcase transaction that includes ownership
        transfer (OT). This operation makes the objects as local at exporting site and replica at importing site. The
        operation also supports dry run mode to review the objects for which ownership would be changed before actually
        implementing the ownership changes.
        This will recover the ownership only if that import/export briefcase transaction with OT was performed by the
        current user. DBA users can recover the ownership transferred in transactions done any user.
        
        Use cases:
        This operation is used to recover ownership of objects associated with a briefcase transaction that includes OT
        when that ownership has been inadvertently transferred. Id of the briefcase transaction is used to recover the
        ownership of its associated objects.
        """
        return cls.execute_soa_method(
            method_name='recoverOwnership',
            library='Internal-GlobalMultiSite',
            service_date='2020_01',
            service_name='OwnershipRecovery',
            params={'transactionId': transactionId, 'dryRun': dryRun},
            response_cls=RecoverOwnershipResponse,
        )

    @classmethod
    def recoverOwnershipUsingBriefcase(cls, briefcaseUid: str, dryRun: bool) -> RecoverOwnershipResponse:
        """
        Recovers the ownership of all the objects associated with a briefcase transaction that includes ownership
        transfer (OT). This operation makes the objects as local at exporting site and replica at importing site. The
        operation also supports dry run mode to review the objects for which ownership would be changed before actually
        implementing the ownership changes.
        This will recover the ownership only if the briefcase was exported/imported by the current user. DBA users can
        recover the ownership of objects associated with briefcases exported/imported by any user.
        
        Use cases:
        This operation is used to recover ownership of objects associated with a briefcase transaction that includes OT
        when that ownership has been inadvertently transferred. UID of the briefcase is used to recover the ownership
        of its associated objects.
        """
        return cls.execute_soa_method(
            method_name='recoverOwnershipUsingBriefcase',
            library='Internal-GlobalMultiSite',
            service_date='2020_01',
            service_name='OwnershipRecovery',
            params={'briefcaseUid': briefcaseUid, 'dryRun': dryRun},
            response_cls=RecoverOwnershipResponse,
        )

    @classmethod
    def deleteOtTransaction(cls, transactionId: str) -> ServiceData:
        """
        Deletes the briefcase transaction that includes OT from the database. Once deleted, you cannot recover
        ownership of the objects associated with the specified transaction.
        Non-DBA users can only delete the transactions performed by themselves. DBA users can delete any transaction.
        
        Use cases:
        This operation is used to delete a briefcase transaction record that was carried out with OT from database.
        Once deleted, ownership recovery cannot be done for objects associated with that briefcase transaction.
        """
        return cls.execute_soa_method(
            method_name='deleteOtTransaction',
            library='Internal-GlobalMultiSite',
            service_date='2020_01',
            service_name='OwnershipRecovery',
            params={'transactionId': transactionId},
            response_cls=ServiceData,
        )

    @classmethod
    def findOtTransactions(cls, otSearchInfo: OtSearchInfo) -> OtTransactionResponse:
        """
        Search briefcase transactions which include ownership transfer of objects by giving the information or criteria
        for transaction search. For non-DBA users, the search result will only contain the transactions done by the
        user i.e. briefcase exported/imported by the current user. DBA users will get the briefcase transactions done
        by all users.
        Search can be done on following criteria &ndash;
        - siteId - All briefcases with OT exported to or imported from the site with the given id will be listed. If
        the siteId is not given, then the briefcases exported from/ imported to current site are listed.
        - transactionType - Allowed values for transaction type are&ndash; import, export or empty string. This will
        limit the search results to only imported or exported briefcases to given site.
        - startDate - Specifies the earliest date and time a briefcase transaction must have occurred to be included in
        the search result.
        - endDate - Specifies the latest date and time a briefcase transaction must have occurred to be included in the
        search result.
        - briefcaseName - Name of the briefcase file.
        
        
        
        Use cases:
        This operation is used to find briefcases transactions(export/import) that include ownership transfer of
        Teamcenter objects. You can select the required briefcase for ownership recovery from the list returned based
        on the input search criteria.
        """
        return cls.execute_soa_method(
            method_name='findOtTransactions',
            library='Internal-GlobalMultiSite',
            service_date='2020_01',
            service_name='OwnershipRecovery',
            params={'otSearchInfo': otSearchInfo},
            response_cls=OtTransactionResponse,
        )
