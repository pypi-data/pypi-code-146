from __future__ import annotations

from tcsoa.gen.Internal.MultiSite._2011_06.ObjectDirectory import BoMfkInfo, ItemIdRecordsProperties, PublicationRecordProperties
from tcsoa.gen.Internal.MultiSite._2012_02.ObjectDirectory import ODSOperationResponse, ClientInfoProperties, QueryItemIdRecordResponse, LocatePublishedObjectResponse, DescribePublicationRecordsResponse, QueryPublicationRecordsResponse
from tcsoa.gen.Internal.MultiSite._2012_02.RemoteOperation import IDSM11EndImportIn, IDSM11StartExportItemIdListRes, IDSM11VersionCheckIn, IDSM11VerifyObjectsRes, IDSM11DescribeItemIn, IDSM11StartAskInfoIn, IDSM11PerformSendObjectsRes, IDSM11GetErrorStackRes, IDSM11SetSyncOptionsIn, IDSM11DistributedAppRes, IDSM11DescribeObjectIn, IDSM11CheckSyncStatusIn, IDSM11DescribeObjectRes, IDSM11RemoteNotificationRes, IDSM11StartImportRes, IDSM11EndAskInfoIn, IDSM11FailureRes, IDSM11CheckSyncStatusRes, IDSM11SetSyncOptionsRes, IDSM11GetErrorStackIn, IDSM11DescribeItemRes, IDSM11StartExportIn, IDSM11ExportStatusIn, IDSM11StartExportItemIdListIn, IDSM11VerifyObjectsIn, IDSM11EndExportItemIdListIn, IDSM11RemoteNotificationIn, IDSM11VersionCheckRes, IDSM11RepublishObjectIn, IDSM11StartSendObjectsIn, IDSM11StartExportRes, IDSM11EndSendObjectsIn, IDSM11LocateObjectRes, IDSM11XferInfoFileRes, IDSM11StartSendObjectsRes, IDSM11ExportStatusRes, IDSM11DistributedAppIn, IDSM11StartImportIn, IDSM11StartAskInfoRes, IDSM11XferInfoFileIn, IDSM11EndImportRes, IDSM11LocateObjectIn, IDSM11PerformSendObjectsIn
from typing import List
from tcsoa.base import TcService


class RemoteOperationService(TcService):

    @classmethod
    def idsm11CheckSyncStatusSvc(cls, inputs: IDSM11CheckSyncStatusIn) -> IDSM11CheckSyncStatusRes:
        """
        The 'idsm11CheckSyncStatusSvc' operation is used to check the sync status of the input set of object(s) in the
        'IDSM11CheckSyncStatusIn' structure. 
        
        This operation is integrated with MultiSite Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based MultiSite environment. This operation acts as a wrapper call to server
        side RPC function and hence is invoked from within the MultiSite framework. Consequently no other clients can
        invoke this operation.
        
        The corresponding RPC call is idsm11_check_sync_status_1_svc().
        
        
        Use cases:
        - This operation is called from the auto sync handler to retrieve the object sync state. The auto sync handler
        used to extend and customize task actions. 
        
        """
        return cls.execute_soa_method(
            method_name='idsm11CheckSyncStatusSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11CheckSyncStatusRes,
        )

    @classmethod
    def idsm11DescribeItemSvc(cls, inputs: IDSM11DescribeItemIn) -> IDSM11DescribeItemRes:
        """
        The 'idsm11DescribeItemSvc' operation retrieves item information for a given item.
        
        This operation is integrated with MultiSite Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based MultiSite environment. This operation acts as a wrapper call to server
        side RPC function and hence is invoked from within the MultiSite framework. Consequently no other clients can
        invoke this operation.
        
        The corresponding RPC call is 'idsm11_describe_item_1_svc()'.
        
        
        Use cases:
        - This operation is called from data_share utility, for reporting the duplicate items. For the supplied item
        id, this operation will get item information available with the remote Integrated Distributed Services Manager
        (IDSM) server and reports the duplicate items. 
        
        """
        return cls.execute_soa_method(
            method_name='idsm11DescribeItemSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11DescribeItemRes,
        )

    @classmethod
    def idsm11DescribeObjectSvc(cls, inputs: IDSM11DescribeObjectIn) -> IDSM11DescribeObjectRes:
        """
        The 'idsm11DescribeObjectSvc' operation used to retrieve the object description from Integrated Distributed
        Services Manager (IDSM) server.  Consumer should provide the client information and the tag of the object, as
        an input.
        
        This operation is integrated with Multi-Site  Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site  environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site  framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding rpc call is 'idsm11_describe_object_1_svc().'
        
        
        Use cases:
        - To import the remote objects at the local site, object(s) published to the Object Directory Service (ODS)
        needs to be first searched and then imported. While loading the ODS published remote objects, this operation is
        called to get the object information.  
        
        """
        return cls.execute_soa_method(
            method_name='idsm11DescribeObjectSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11DescribeObjectRes,
        )

    @classmethod
    def idsm11DistributedAppSvc(cls, inputs: IDSM11DistributedAppIn) -> IDSM11DistributedAppRes:
        """
        This distributed call checks, if the Integrated Distributed Services Manager (IDSM) provides the supplied
        service to the client. The op codes are used to specify the operation. Please refer the
        'IDSM11DistributedAppIn' structure for the list of op codes.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is 'idsm11_distributed_app_1_svc().'
        
        
        Use cases:
        - This operation is called from the DIST_IDSM_commit_synchronous_remote_import(), to check if the commit
        synchronous remote import operation supported by IDSM server.
        
        """
        return cls.execute_soa_method(
            method_name='idsm11DistributedAppSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11DistributedAppRes,
        )

    @classmethod
    def idsm11EndAskInfoSvc(cls, inputs: IDSM11EndAskInfoIn) -> IDSM11FailureRes:
        """
        The 'idsm11EndAskInfoSvc' operation is used to finish the info file transfer.  This is the last operation in
        the sequence of transferring info file and finishes the info file transfer process.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is 'idsm11_end_ask_info_1_svc().'
        
        
        Use cases:
        This operation is called while creating or updating the dataset. 'idsm11StartAskInfoSvc' call will be made to
        get the schema info of the given site, then type and class-info will be fetched out of it, on successful
        completion of the call, info file is transferred to server staging directory using 'idsm11XferInfoFileSvc'. The
        'idsm11EndAskInfoSvc' closes the communication channel and finishes the file transfer.
        """
        return cls.execute_soa_method(
            method_name='idsm11EndAskInfoSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11FailureRes,
        )

    @classmethod
    def idsm11EndExportItemIdListSvc(cls, inputs: IDSM11EndExportItemIdListIn) -> IDSM11FailureRes:
        """
        The 'idsm11EndExportItemIdListSvc' is used to delete the server staging directory, and set finished status. 
        This is the last operation in the sequence of remote item id import operation and finishes the remote item id
        import process.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding rpc call is' idsm11_end_export_item_id_list_1_svc().'
        
        
        Use cases:
        At the moment this API is not used, and it has been added considering future requirement.
        """
        return cls.execute_soa_method(
            method_name='idsm11EndExportItemIdListSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11FailureRes,
        )

    @classmethod
    def idsm11EndImportSvc(cls, inputs: IDSM11EndImportIn) -> IDSM11EndImportRes:
        """
        The 'idsm11EndImportSvc' operation imports remote business objects to the local site. When a user at Source
        Site selects business objects (e.g, Item) for remote export, these objects are written into object.meta file at
        the Source Site and transferred over to the Target Site. Integrated Distributed Services Manager (IDSM) service
        at the Target Site imports the content of this file and 'idsm11EndImportSvc' is the last operation in the
        sequence and cannot be called in isolation.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is 'idsm11_end_import_1_svc().'
        
        
        
        Use cases:
        To Remote Export business object(s), a series of operations needs to be performed and 'Idsm11EndImportSvc' gets
        invoked to complete the remote import transaction. 
        Operation sequence for remote export
        - idsm11StartImportSvc
        - idsm4XferImportFileSvc
        - idsm11EndImportSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm11EndImportSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11EndImportRes,
        )

    @classmethod
    def idsm11EndSendObjectsSvc(cls, inputs: IDSM11EndSendObjectsIn) -> IDSM11FailureRes:
        """
        The 'idsm11EndSendObjectsSvc' ends the system object s remote import process. The operation gets called, if
        abort flag is set to true by the previous operation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        The corresponding RPC call is' idsm11_end_ send_objects_1_svc().'
        
        
        Use cases:
        This operation is called from the distributed_execute utility. The utility is used to generate the 'item'
        reports locally as well as remotely. To generate the report, internally this utility calls the item_report
        utility.
        """
        return cls.execute_soa_method(
            method_name='idsm11EndSendObjectsSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11FailureRes,
        )

    @classmethod
    def idsm11ExportStatusSvc(cls, inputs: IDSM11ExportStatusIn) -> IDSM11ExportStatusRes:
        """
        The 'idsm11ExportStatusSvc' operation returns the export/import status of business objects.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is 'idsm11_export_status_1_svc().'
        
        
        Use cases:
        - In case of the remote import, this operation is used to check the status of the remote import invoked by the
        earlier call 'idsm11StartExportSvc'. The status informs the remote site whether import is complete and if it s
        in process, then how many workspace objects are exported so far. The reported workspace objects will be in the
        multiples of 'checkClientAfterNWsos' supplied in the 'IDSM11ExportStatusIn' structure.
        - In case of the remote export, this operation is used to check the status of the remote export finished by the
        earlier call 'idsm11EndImportSvc'. The status informs the remote site whether export is complete and if it s in
        process, then how many workspace objects are exported so far. The reported workspace objects will be in the
        multiples of 'checkClientAfterNWsos' supplied in the 'IDSM11ExportStatusIn' structure.
        
        """
        return cls.execute_soa_method(
            method_name='idsm11ExportStatusSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11ExportStatusRes,
        )

    @classmethod
    def idsm11GetErrorStackSvc(cls, inputs: IDSM11GetErrorStackIn) -> IDSM11GetErrorStackRes:
        """
        The 'idsm11GetErrorStackSvc' operation is used to retrieve the error stack.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding rpc call is 'idsm11_get_error_stack_1_svc().'
        
        
        Use cases:
        While performing the checkpoint transaction, this operation is called from the data_share & data_sync utility.
        """
        return cls.execute_soa_method(
            method_name='idsm11GetErrorStackSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11GetErrorStackRes,
        )

    @classmethod
    def idsm11LocateObjectSvc(cls, inputs: IDSM11LocateObjectIn) -> IDSM11LocateObjectRes:
        """
        The 'idsm11LocateObjectSvc' operation locates the owning site of the remote object given in
        'IDSM11LocateObjectIn' input structure.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'idsm11_locate_object_1_svc().'
        
        
        Use cases:
        'idsm11LocateObjectSvc' operation invoked during remote import of stub object. Export Assembly from site1 to
        site2 with including BOM. On site2, open assembly in PSE (Product Structure Editor) and it shows components as
        Remote Object(s), do import on that object(s), which tries to find the owning site of the object. It tries to
        locate the stub object by finding its owning site by checking publication record for that object by calling
        'locatePublishedObjects'.
        """
        return cls.execute_soa_method(
            method_name='idsm11LocateObjectSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11LocateObjectRes,
        )

    @classmethod
    def idsm11PerformSendObjectsSvc(cls, inputs: IDSM11PerformSendObjectsIn) -> IDSM11PerformSendObjectsRes:
        """
        The 'idsm11PerformSendObjectsSvc' operation sends system objects to the remote site based on
        'IDSM11PerformSendObjectsIn' input.  This is the third operation in the sequence used in sending system objects
        such as Users, Groups, Persons, etc to the remote site. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'idsm11_perform_send_objects_1_svc().'
        
        
        Use cases:
        - idsm11PerformSendObjectsSvc operation gets invoked from   dsa_util  utility while sending system objects such
        as Users, Groups, Persons, etc to remote site.
        
        
        Operation sequence is as below
        - idsm11StartSendObjectsSvc
        - file transfer via DIST call
        - idsm11PerformSendObjectsSvc  
        - idsm11EndSendObjectsSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm11PerformSendObjectsSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11PerformSendObjectsRes,
        )

    @classmethod
    def idsm11RemoteNotificationSvc(cls, inputs: IDSM11RemoteNotificationIn) -> IDSM11RemoteNotificationRes:
        """
        The 'idsm11RemoteNotificationSvc' operation performs remote notification and subscription for object at remote
        site based on 'IDSM11RemoteNotificationIn' input structure.
        
        This is the last operation in the sequence and cannot be called in isolation. 
        
        This operation is integrated with Multi-Site RPC framework and is callable only in an http based 
         Multi-Site environment. This operation acts as a wrapper call to server side RPC function and 
        hence is invoked from within the Multi-Site framework. Consequently no other clients can 
        invoke this operation.
        
        Corresponding server side RPC call is 'idsm11_remote_notification_1_svc().'
        
        
        Use cases:
        'idsm11RemoteNotificationSvc' operation is called in automatic synchronization to notify and subscribe remote
        site in HTTP multisite environment.
        """
        return cls.execute_soa_method(
            method_name='idsm11RemoteNotificationSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11RemoteNotificationRes,
        )

    @classmethod
    def idsm11RepublishObjectSvc(cls, inputs: IDSM11RepublishObjectIn) -> IDSM11FailureRes:
        """
        The 'idsm11RepublishObjectSvc' operation updates the 'PublicationRecord' at the Object Directory Service (ODS)
        site for the object given in 'IDSM11RepublishObjectIn'.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        The corresponding RPC call is 'idsm11_republish_object_1_svc ().'
        
        
        Use cases:
        'idsm11RepublishObjectSvc' operation gets invoked for re-publishing the given object to ODS site after
        ownership transfer in use cases like remote import/export.  The ownership transfer operation performed on the
        business objects (BOs) change its ownership. After transfer of ownership, if it is not re-published then the BO
        has the wrong entry for the owning siteId in PublicationRecord at ODS site. In order to correct it, the BOs
        needs to be republished to the ODS server.
        """
        return cls.execute_soa_method(
            method_name='idsm11RepublishObjectSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11FailureRes,
        )

    @classmethod
    def idsm11SetSyncOptionsSvc(cls, inputs: IDSM11SetSyncOptionsIn) -> IDSM11SetSyncOptionsRes:
        """
        The 'idsm11SetSyncOptionsSvc' operation used to sets sync options on the objects after object import from
        importing site.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is' idsm11_set_sync_options_1_svc ().'
        
        
        Use cases:
        'idsm11SetSyncOptionsSvc' operation is called during remote import while syncing object(s) and is called from
        importing site in HTTP multisite environment.
        """
        return cls.execute_soa_method(
            method_name='idsm11SetSyncOptionsSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11SetSyncOptionsRes,
        )

    @classmethod
    def idsm11StartAskInfoSvc(cls, inputs: IDSM11StartAskInfoIn) -> IDSM11StartAskInfoRes:
        """
        The 'idsm11StartAskInfoSvc' operation is call used to get the information about the server side staging
        directory i.e. where the files are being transferred on the server side while get type-class mapping file from
        remote site. This basically opens a file transfer channel used to transfer files from the server.
        
        This is the first operation in the sequence which gets information about the Multi-Site staging directory and
        cannot be called in isolation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'idsm11_start_ask_info_1_svc().'
        
        
        Use cases:
        'idsm11StartAskInfoSvc' operation is invoked while getting type class files from the remote site in HTTP
        multisite environment. This is called from database_verify() utility.
        Operation sequence is as below:
        - idsm11StartAskInfoSvc
        - idsm11XferInfoFileSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm11StartAskInfoSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11StartAskInfoRes,
        )

    @classmethod
    def idsm11StartExportItemIdListSvc(cls, inputs: IDSM11StartExportItemIdListIn) -> IDSM11StartExportItemIdListRes:
        """
        The 'idsm11StartExportItemIdListSvc' operation gets information about the server side staging directory and
        output export files. 
        
        This is the first operation in the sequence and cannot be called in isolation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
                       
        Corresponding RPC call is' idsm11_start_export_item_id_list_1_svc().'
        
        
        Use cases:
        'idsm11StartExportItemIdListSvc' operation is called from data_share utility while finding duplicate itemId(s)
        at the remote site.
        """
        return cls.execute_soa_method(
            method_name='idsm11StartExportItemIdListSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11StartExportItemIdListRes,
        )

    @classmethod
    def idsm11StartExportSvc(cls, inputs: IDSM11StartExportIn) -> IDSM11StartExportRes:
        """
        The 'idsm11StartExportSvc' operation exports business objects at the remote site during a Remote Import
        transaction. When a user at Source Site selects business objects (e.g, Item) for remote import, the request is
        sent to the Target Site to export these objects into object.meta file at the Target Site and transferred over
        to the Source Site (requesting site). IDSM service at the Target Site exports the objects and creates
        object.meta file. The 'idsm11StartExportSvc' is the first operation in the sequence and hence cannot be called
        in isolation.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is' idsm11_start_export_1_svc().'
        
        
        Use cases:
        To remote import the business object, first the source site user creates an Item and publishes it to the
        default Object Directory Service (ODS) site.  The target site user performs remote search with the item id and
        imports it to the target site using the remote import operation. On successful completion of remote import
        operation, the item is imported to the target site database. To Remote Import the business object, the series
        of operations needs to be performed and this operation gets invoked as a first step in the Remote Import
        transaction. 
        The sequence of operations are as below 
        - idsm11StartExportSvc
        - idsm11ExportStatusSvc
        - idsm4XferExportFileSvc
        - idsm1EndExportSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm11StartExportSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11StartExportRes,
        )

    @classmethod
    def idsm11StartImportSvc(cls, inputs: IDSM11StartImportIn) -> IDSM11StartImportRes:
        """
        The 'idsm11StartImportSvc' operation gets information about the server side staging directory i.e. where the
        files are being transferred on the server during export.
        
        This is the first operation in the sequence and cannot be called in isolation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
                       
        Corresponding RPC call is 'idsm11_start_import_1_svc().'
        
        
        Use cases:
        To Remote Export business object(s), a series of operations needs to be performed and Idsm3StartImportSvc gets
        invoked as a first step. 
        Operation sequence for remote export.
        
        - idsm11StartImportSvc
        - idsm4XferImportFileSvc
        - idsm11EndImportSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm11StartImportSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11StartImportRes,
        )

    @classmethod
    def idsm11StartSendObjectsSvc(cls, inputs: IDSM11StartSendObjectsIn) -> IDSM11StartSendObjectsRes:
        """
        The 'idsm11StartSendObjectsSvc' operation gets information about the server side staging directory i.e. where
        the files are being transferred on the server side while sending system objects to the remote site. 
        
        This is the first operation in the sequence which gets information about the Multi-Site staging directory and
        cannot be called in isolation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is' idsm11_start_send_objects_1_svc().'
        
        
        Use cases:
        'idsm11StartSendObjectsSvc' operation gets invoked from   dsa_util  utility while sending system objects such
        as Users, Groups, Persons, etc to the remote site.
        Operation sequence is as below
        - idsm11StartSendObjectsSvc
        - file transfer via DIST call
        - idsm11PerformSendObjectsSvc  
        - idsm11EndSendObjectsSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm11StartSendObjectsSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11StartSendObjectsRes,
        )

    @classmethod
    def idsm11VerifyObjectsSvc(cls, inputs: IDSM11VerifyObjectsIn) -> IDSM11VerifyObjectsRes:
        """
        The 'idsm11VerifyObjectsSvc' operation is used to verify if the object exist at the target site given in
        'IDSM11VerifyObjectsIn' input structure.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
                       
        Corresponding RPC call is' idsm11_verify_objects_1_svc().'
        
        
        Use cases:
        'idsm11VerifyObjectsSvc' operation is called in case of importing stub objects from structure manager where it
        tries to check whether these objects exist at target site and their verdict in HTTP multisite environment.
        """
        return cls.execute_soa_method(
            method_name='idsm11VerifyObjectsSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11VerifyObjectsRes,
        )

    @classmethod
    def idsm11VersionCheckSvc(cls, inputs: IDSM11VersionCheckIn) -> IDSM11VersionCheckRes:
        """
        The 'idsm11VersionCheckSvc' operation gets the Integrated Distributed Services Manager (IDSM) server version.
        
        This operation is integrated with Multi-Site RPC framework and is callable only in HTTP based Multi-Site
        environment. This operation acts as a wrapper call to server side RPC function and hence is invoked from within
        the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        There is no RPC call added for this. But it can be added as per future requirement.
        
        
        Use cases:
        'idsm11VersionCheckSvc' operation is called prior to all IDSM requests made by client to check version of IDSM
        for compatibility in HTTP multisite environment.  It is also used by some of the Distributed (DIST) ITKs prior
        to make any IDSM request.
        """
        return cls.execute_soa_method(
            method_name='idsm11VersionCheckSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11VersionCheckRes,
        )

    @classmethod
    def idsm11XferInfoFileSvc(cls, inputs: IDSM11XferInfoFileIn) -> IDSM11XferInfoFileRes:
        """
        The 'idsm11XferInfoFileSvc' operation transfers the type class mapping file from the remote site(s) Multi-Site
        staging directory to the local site Multi-Site staging directory. 
        
        This is the second operation in the sequence and cannot be called in isolation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'idsm11_xfer_info_file_1_svc().'
        
        
        Use cases:
        idsm11XferInfoFileSvc operation is invoked while getting type class files from the remote site in HTTP
        multisite environment. This is called from database_verify() utility.
        Operation sequence is as below:
        - idsm11StartAskInfoSvc
        - idsm11XferInfoFileSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm11XferInfoFileSvc',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM11XferInfoFileRes,
        )


class ObjectDirectoryService(TcService):

    @classmethod
    def locatePublishedObjects(cls, clientInfo: ClientInfoProperties, objTagAsString: List[str]) -> LocatePublishedObjectResponse:
        """
        The 'locatePublishedObjects' operation locates the published objects from the Object Directory Service (ODS)
        site for each 'objTagAsString' input given.  
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods11_locate_object_1_svc().'
        
        Use cases:
        'locatePublishedObjects' operation gets called while importing stub objects from Structure Manager. It tries to
        locate the stub object by finding its owning site by checking publication record for that object. Export
        Assembly from site1 to site2 with including BOM. On site2, open assembly in Structure Manager and it shows
        components as Remote Object(s), do import on that object(s), which tries to find the owning site of the object.
        """
        return cls.execute_soa_method(
            method_name='locatePublishedObjects',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'objTagAsString': objTagAsString},
            response_cls=LocatePublishedObjectResponse,
        )

    @classmethod
    def publishObjects(cls, clientInfo: ClientInfoProperties, records: List[PublicationRecordProperties]) -> ODSOperationResponse:
        """
        The 'publishObjects' operation creates the PublicationRecords at the Object Directory Service (ODS) site for
        each 'PublicationRecordProperties' input given.  
         
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods11_1_publish_object_1_svc().'
        
        
        Use cases:
        'publishObjects' operation gets called in ODS publish object operation. The business object(s) can be shared
        within the Multi-Site federation. To remote import (Pull case) it must be published to the ODS. It can either
        be called from Rich Client (RAC) or from command line data_share (publish switch) utility.
        """
        return cls.execute_soa_method(
            method_name='publishObjects',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'records': records},
            response_cls=ODSOperationResponse,
        )

    @classmethod
    def queryItemIdRecords(cls, clientInfo: ClientInfoProperties, mfkInfo: List[BoMfkInfo]) -> QueryItemIdRecordResponse:
        """
        The 'queryItemIdRecords' operation queries the ItemId Records from the central itemid registry for each
        'BoMfkInfo' input given. It checks whether input itemids are registered or not.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation
        
        Corresponding RPC call is 'ods11_1_describe_item_1_svc().'
        
        
        Use cases:
        'queryItemIdRecords' operation gets invoked in below use cases check whether given itemid is registered or not.
        - New Item creation when auto register is ON.
        - Registering  Item to  registry.
        
        """
        return cls.execute_soa_method(
            method_name='queryItemIdRecords',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'mfkInfo': mfkInfo},
            response_cls=QueryItemIdRecordResponse,
        )

    @classmethod
    def queryPublicationRecords(cls, clientInfo: ClientInfoProperties, clientLocale: str, queryString: str, sortKeys: List[str], sortOrder: List[int]) -> QueryPublicationRecordsResponse:
        """
        The 'queryPublicationRecords' operation queries the PublicationRecords from the Object Directory Service (ODS)
        site based on the input query String. This query string should be in POM SQL query format.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods11_execute_query_1_svc().'
        
        
        Use cases:
        'queryPublicationRecords' operation is called in ODS Remote search operation from the Rich Client (RAC). It
        searches the ODS server for published objects that satisfy the search criteria.
        """
        return cls.execute_soa_method(
            method_name='queryPublicationRecords',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'clientLocale': clientLocale, 'queryString': queryString, 'sortKeys': sortKeys, 'sortOrder': sortOrder},
            response_cls=QueryPublicationRecordsResponse,
        )

    @classmethod
    def unpublishObjects(cls, clientInfo: ClientInfoProperties, objTagAsString: List[str]) -> ODSOperationResponse:
        """
        The 'unpublishObjects' operation deletes the PublicationRecord from the Object Directory Service (ODS) site for
        each 'objTagAsString' input given.  
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods11_unpublish_object_1_svc().'
        
        
        Use cases:
        'unpublishObjects' operation gets called in ODS unpublish object operation. In Multi-Site federation to remote
        import (Pull case) the Business Object (BO), it must be published to the ODS. And to revoke the sharing, the
        business object should be unpublished from ODS. It can either be called from Rich Client (RAC) or from command
        line data_share (unpublish switch) utility.
        """
        return cls.execute_soa_method(
            method_name='unpublishObjects',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'objTagAsString': objTagAsString},
            response_cls=ODSOperationResponse,
        )

    @classmethod
    def updatePublicationRecords(cls, clientInfo: ClientInfoProperties, records: List[PublicationRecordProperties]) -> ODSOperationResponse:
        """
        The 'updatePublicationRecords' operation updates the PublicationRecord at the Object Directory Service (ODS)
        site for each 'PublicationRecordProperties' input given.  
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods11_1_refresh_object_1_svc().'
        
        
        Use cases:
        'updatePublicationRecords' operation gets invoked in Integrates Distributed Service Manager (IDSM) re-publish
        object operation after object is exported to other site with ownership transfer in use cases like remote
        import/export. The ownership transfer operation performed on the business objects (BOs) change its ownership.
        After transfer of ownership, if it is not re-published then the BO has the wrong entry for the owning siteId in
        PublicationRecord at ODS site. In order to correct it, the BOs needs to be republished to the ODS server.
        """
        return cls.execute_soa_method(
            method_name='updatePublicationRecords',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'records': records},
            response_cls=ODSOperationResponse,
        )

    @classmethod
    def createItemIdRecords(cls, clientInfo: ClientInfoProperties, records: List[ItemIdRecordsProperties]) -> ODSOperationResponse:
        """
        The 'createItemIdRecords' operation creates Item Records in the item registry based on
        'ItemIdRecordsProperties' input.
        
        This operation is integrated with Multi-Site Remote Procedure Call ( RPC) framework and is callable only in an
        HTTP based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence
        is invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods11_1_register_item_1_svc()'.
        
        Use cases:
        - Admin user(s) set the ITEM_id_always_register_on_creation to TRUE on all sites within a Multi-Site
        federation. On item creation the items created automatically registers with the central item registry.
        - Admin user(s) can register existing item(s) with the central item registry, using Register Item Id command in
        the Rich Client(RAC) or command line utility data_share f=register.
        
        """
        return cls.execute_soa_method(
            method_name='createItemIdRecords',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'records': records},
            response_cls=ODSOperationResponse,
        )

    @classmethod
    def deleteItemIdRecords(cls, clientInfo: ClientInfoProperties, mfkInfo: List[BoMfkInfo]) -> ODSOperationResponse:
        """
        The 'deleteItemIdRecords' operation deletes Item Records from the item registry for each 'BoMfkInfo' input.
        
        This operation is integrated with Multi-Site Remote Procedure Call ( RPC) framework and is callable only in an
        HTTP based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence
        is invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods11_1_unregister_item_1_svc().'
        
        
        Use cases:
        Admin user(s) can unregister existing item(s) from the central item registry, using Unregister Item Id command
        in the Rich Client (RAC) or command line utility data_share  f=unregister.
        """
        return cls.execute_soa_method(
            method_name='deleteItemIdRecords',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'mfkInfo': mfkInfo},
            response_cls=ODSOperationResponse,
        )

    @classmethod
    def describePublicationRecords(cls, clientInfo: ClientInfoProperties, publishedObjTagsAsString: List[str], clientLocale: str) -> DescribePublicationRecordsResponse:
        """
        The 'describePublicationRecords' operation returns the 'PublicationRecord' properties for a given list of
        published objects. 
         
        This operation is integrated with Multi-Site Remote Procedure Call ( RPC) framework and is callable only in an
        HTTP based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence
        is invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        corresponding RPC call is 'ods11_describe_object_1_svc().'
        
        
        Use cases:
        'describePublicationRecords' operation gets called via Object Directory Service (ODS) remote search in HTTP
        Multi-Site environment.  ODS Remote search returns list of the Published objects as per search criteria. For
        the list of published object, 'describePublicationRecords' operation is called to get the publicationRecord
        properties on each object.
        """
        return cls.execute_soa_method(
            method_name='describePublicationRecords',
            library='Internal-MultiSite',
            service_date='2012_02',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'publishedObjTagsAsString': publishedObjTagsAsString, 'clientLocale': clientLocale},
            response_cls=DescribePublicationRecordsResponse,
        )
