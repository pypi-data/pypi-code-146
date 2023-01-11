from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2015_03.FullTextSearch import GetIndexedObjectsResponse, GetAMImpactedObjectsResponse, GetModifiedObjectsToSyncResponse
from tcsoa.gen.Internal.AWS2._2015_03.DataManagement import GetStyleSheetIn, GetStyleSheetResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from datetime import datetime


class DataManagementService(TcService):

    @classmethod
    def getStyleSheet(cls, processEntireXRT: bool, input: List[GetStyleSheetIn]) -> GetStyleSheetResponse:
        """
        This operation returns the stylesheets and the required data to present that stylesheet for each input object.
        
        Use cases:
        Use Case 1: Open an object in ActiveWorkspace.
        When an object is selected in ActiveWorkspace, the user may choose to invoke the open operation. When that
        operation is executed the getStylesheet call is invoked and the Stylesheet is processed in order to display the
        data to the user.
        
        Use Case 2: List view with Summary
        When an object is selected in the ActiveWorkspace navigator, when in list view with summary mode, the
        getStyleSheet SOA operation is invoked, and the returned data is parsed/processed in order to present the data
        to the user in the Summary panel.
        
        Use Case 3: Show Object Info
        When an object is selected in ActiveWorkspace, a user may choose the "Show Object Info" command.  When
        executed, a panel slides out from the right hand side of the application, and the selected objects data is
        presented.  In order to populate the panel, the getStylesheet call is invoked and the returned data is parsed
        and processed in order to build the UI.
        """
        return cls.execute_soa_method(
            method_name='getStyleSheet',
            library='Internal-AWS2',
            service_date='2015_03',
            service_name='DataManagement',
            params={'processEntireXRT': processEntireXRT, 'input': input},
            response_cls=GetStyleSheetResponse,
        )


class FullTextSearchService(TcService):

    @classmethod
    def updateIndexIslandStatus(cls, applicationID: str, indexIslandUIDs: List[str], exportDate: datetime, status: int) -> ServiceData:
        """
        This operation updates the data islands that match the given input criteria with a status (1 - Replication
        Pending, 2 - Replication Complete, etc.) and exported date. Criteria include application ID, timestamp, and
        list of index island UIDs. 
        
        Use cases:
        Full Text Indexer error handling
        
        While indexing of data there might be issues during any step of the ETL (Extract, Transform and Load) process. 
        This operation will be used to set the status of the exported objects. The status that is updated will help in
        identifying the failed objects for error recovery. This operation will be used during indexing and sync when an
        error occurs.
        """
        return cls.execute_soa_method(
            method_name='updateIndexIslandStatus',
            library='Internal-AWS2',
            service_date='2015_03',
            service_name='FullTextSearch',
            params={'applicationID': applicationID, 'indexIslandUIDs': indexIslandUIDs, 'exportDate': exportDate, 'status': status},
            response_cls=ServiceData,
        )

    @classmethod
    def cleanupScratchTable(cls) -> ServiceData:
        """
        The scratch table contains records for the new and deleted objects. The applications consuming this data will
        have their unique application ID and the last processed timestamp entries in subscription table.  This
        operation deletes the records from the scratch table that are consumed by all the registered applications. The
        scratch table records whose last saved date is less than the minimum of the last processed date of subscription
        table will be deleted.
        
        Use cases:
        Full Text Indexer Sync
        
        When objects are created or deleted, the database triggers will add them to the scratch table.  During the Full
        Text Indexer Sync process, these new and deleted objects are queried and updated to the search index. On
        success, the data needs to be removed from the scratch table in order to avoid the table growing in size and
        leading to poor performance of queries. This new operation will help in cleaning only the data that is consumed
        by all the registered applications.  This operation will be called at the end or the sync process.
        """
        return cls.execute_soa_method(
            method_name='cleanupScratchTable',
            library='Internal-AWS2',
            service_date='2015_03',
            service_name='FullTextSearch',
            params={},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteIndexedIslands(cls, applicationID: str, indexIslandUIDs: List[str]) -> ServiceData:
        """
        The accountability table contains records for the indexed objects. When the principal objects are deleted, the
        index is cleared but the records in the accountability table still exist. This operation deletes the records
        from the accountability table whose island UIDs and the application id match the given criteria.
        
        Use cases:
        Full Text Indexer Sync
        
        When objects are created or deleted, the database triggers will add them to the scratch table.  During the Full
        Text Indexer Sync process, it queries for the deleted objects and updates the search index. On success, the
        data needs to be removed from the accountability table in order to avoid the table growing in size and leading
        to poor performance of queries. This new operation will help in cleaning the data. This operation will be
        called during the delete process of sync.
        """
        return cls.execute_soa_method(
            method_name='deleteIndexedIslands',
            library='Internal-AWS2',
            service_date='2015_03',
            service_name='FullTextSearch',
            params={'applicationID': applicationID, 'indexIslandUIDs': indexIslandUIDs},
            response_cls=ServiceData,
        )

    @classmethod
    def deregisterApplicationIDs(cls, applicationIDs: List[str]) -> ServiceData:
        """
        This operation deletes the records of the given list of application IDs from the subscription table.
        
        Use cases:
        Full Text Indexer Sync
        
        The Initial Condition for this use case is that all the data from Teamcenter database has already been indexed
        in the Search Engine. When there are Access Manager rule tree changes and the change has a global impact, then
        all of the indexed data has to be refreshed. In order to identify the globally impacted objects, an application
        ID called :FTS_REFRESH (a unique identifier representing the Full Text Search Refresh operation) is registered
        with TIE (Teamcenter Import Export). Once the indexing is complete and there are no more objects left to be
        refreshed, this operation is invoked to deregister and to signal to TIE that the necessary cleanup of data in
        the database can be done. This is necessary to limit the growth of the database tables used by TIE.
        """
        return cls.execute_soa_method(
            method_name='deregisterApplicationIDs',
            library='Internal-AWS2',
            service_date='2015_03',
            service_name='FullTextSearch',
            params={'applicationIDs': applicationIDs},
            response_cls=ServiceData,
        )

    @classmethod
    def getAMImpactedObjects(cls, amSyncAppID: str, applicationID: str) -> GetAMImpactedObjectsResponse:
        """
        This operation lists the business objects whose READ access is impacted by the changes in Access Manager rule
        tree. The rule tree changes considered are limited to those made after the previous call to this operation.
        This operation is usually called periodically and the objects whose read access is modified due to the changes
        to Access Manager rule tree between the previous call and the current one are determined and returned.
        Optionally, this operation returns the set of objects which is the intersection of objects impacted by Access
        Manager rule changes and objects previously indexed. Previously indexed objects are stored in ACCT_TABLE table.
        The application id will be used to further filter the objects impacted by Access manager rule changes and got
        previously indexed for  a particular application.
        """
        return cls.execute_soa_method(
            method_name='getAMImpactedObjects',
            library='Internal-AWS2',
            service_date='2015_03',
            service_name='FullTextSearch',
            params={'amSyncAppID': amSyncAppID, 'applicationID': applicationID},
            response_cls=GetAMImpactedObjectsResponse,
        )

    @classmethod
    def getIndexedObjects(cls, applicationID: str, subscriptionAppID: str, exportedDate: datetime, status: int, classNames: List[str], maxObjectCount: int) -> GetIndexedObjectsResponse:
        """
        This operation queries for the indexed objects matching the given input criteria. Criteria include application
        ID, timestamp, export or import status of the object and list of object class names. 
        """
        return cls.execute_soa_method(
            method_name='getIndexedObjects',
            library='Internal-AWS2',
            service_date='2015_03',
            service_name='FullTextSearch',
            params={'applicationID': applicationID, 'subscriptionAppID': subscriptionAppID, 'exportedDate': exportedDate, 'status': status, 'classNames': classNames, 'maxObjectCount': maxObjectCount},
            response_cls=GetIndexedObjectsResponse,
        )

    @classmethod
    def getModifiedObjectsToSync(cls, applicationID: str) -> GetModifiedObjectsToSyncResponse:
        """
        This operation finds all indexed objects that have been modified since the last "sync" run. 
        """
        return cls.execute_soa_method(
            method_name='getModifiedObjectsToSync',
            library='Internal-AWS2',
            service_date='2015_03',
            service_name='FullTextSearch',
            params={'applicationID': applicationID},
            response_cls=GetModifiedObjectsToSyncResponse,
        )
