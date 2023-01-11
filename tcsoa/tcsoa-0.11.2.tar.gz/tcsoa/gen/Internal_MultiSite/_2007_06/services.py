from __future__ import annotations

from tcsoa.gen.Internal.MultiSite._2007_06.ObjectDirectory import DistributedAppResponse, ClientInfoProperties, QueryItemIdRecordResponse, LocatePublishedObjectResponse, DescribePublicationRecordsResponse, QueryPublicationRecordsResponse, ItemIdRecordsProperties, GetODSVersionResponse, DistributedAppProperties, PublicationRecordProperties
from tcsoa.gen.Internal.MultiSite._2007_06.TcEntObjectDirectory import TcEntClientInfoProperties, TcEntPublicationRecordProperties, QueryPublicationRecordsProperties, DescribePublicationRecordsResponse, QueryPublicationRecordsResponse, RepublishObjectInputProperties, GetODSVersionResponse
from tcsoa.gen.Internal.MultiSite._2007_06.RemoteOperation import IDSM7StartExportRes, IDSM6DescribeItemIn, IDSM4XferImportFileRes, IDSM6StartSendObjectsRes, IDSM1LocateObjectRes, IDSM1XferInfoFileRes, IDSM9DescribeObjectIn, IDSM6EndExportItemIdListIn, IDSM4GetErrorStackIn, IDSM1VerifyObjectsRes, IDSM1EndExportIn, IDSM7AskVersionRes, IDSM2DescribeObjectRes, IDSM2VersionCheckRes, IDSM4XferExportFileRes, IDSM3EndImportIn, IDSM4CheckSyncStatusRes, IDSM7DistributedAppIn, IDSM1LocateObjectIn, IDSM1EndAskInfoIn, IDSM3ExportStatusIn, IDSM6StartExportItemIdListRes, IDSM7AskVersionIn, IDSM4RemoteNotificationRes, IDSM3StartImportRes, IDSM4GetErrorStackRes, IDSM6DescribeItemRes, IDSM1StartAskInfoIn, IDSM6EndSendObjectsIn, IDSM4SetSyncOptionsIn, IDSM2DescribeObjectIn, IDSM2VersionCheckIn, IDSM6PerformSendObjectsIn, IDSM1XferInfoFileIn, IDSM3StartImportIn, IDSM1StartAskInfoRes, IDSM9DescribeObjectRes, IDSM6StartExportItemIdListIn, IDSM6PerformSendObjectsRes, IDSM3ExportStatusRes, IDSM7DistributedAppRes, IDSM1EndImportRes, IDSM7StartExportIn, IDSM4XferImportFileIn, IDSM4SetSyncOptionsRes, IDSM4RemoteNotificationIn, IDSM4CheckSyncStatusIn, IDSM1VerifyObjectsIn, IDSM6StartSendObjectsIn, IDSM1RepublishObjectIn, IDSM4XferExportFileIn
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class RemoteOperationService(TcService):

    @classmethod
    def idsm1EndAskInfoSvc(cls, inputs: IDSM1EndAskInfoIn) -> ServiceData:
        """
        The 'idsm1EndAskInfoSvc' operation is used to finish the info file transfer.  This is the last operation in the
        sequence of transferring info file and finishes the info file transfer process.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is' idsm1_end_ask_info_1_svc().
        '
        
        Use cases:
        This operation is called while creating or updating the dataset. 'idsm1StartAskInfoSvc' call will be made to
        get the schema info of the given site, then type and classinfo will be fetched out of it, on successful
        completion of the call, info file is transferred to server staging directory using 'idsm1XferInfoFileSvc'. The
        'idsm1EndAskInfoSvc' closes the communication channel and finishes the file transfer.
        """
        return cls.execute_soa_method(
            method_name='idsm1EndAskInfoSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def idsm1EndExportSvc(cls, inputs: IDSM1EndExportIn) -> ServiceData:
        """
        The 'idsm1EndExportSvc' operation completes the Remote Import transaction. This is the last operation in the
        sequence and cleans up files from Multi-Site staging directory and cannot be called in isolation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is 'idsm1_end_export_1_svc().'
        
        
        Use cases:
        This operation is called while creating or updating the dataset. 'idsm1StartAskInfoSvc' call will be made to
        get the schema info of the given site, then type and classinfo will be fetched out of it, on successful
        completion of the call, info file is transferred to server staging directory using 'idsm1XferInfoFileSvc'. The
        'idsm1EndAskInfoSvc' closes the communication channel and finishes the file transfer.
        """
        return cls.execute_soa_method(
            method_name='idsm1EndExportSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def idsm1LocateObjectSvc(cls, inputs: IDSM1LocateObjectIn) -> IDSM1LocateObjectRes:
        """
        The 'idsm1LocateObjectSvc' operation locates the owning site of the remote object given in
        'IDSM1LocateObjectIn' input structure.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is' idsm1_locate_object_1_svc().'
        
        
        Use cases:
        'idsm1LocateObjectSvc' operation invoked during remote import of stub object. Export Assembly from site1 to
        site2 with including BOM. On site2, open assembly in PSE (Product Structure Editor) and it shows components as
        Remote Objects, do import on that object(s), which tries to find the owning site of the object. It tries to
        locate the stub object by finding its owning site by checking publication record for that object by calling
        'locatePublishedObjects'.
        """
        return cls.execute_soa_method(
            method_name='idsm1LocateObjectSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM1LocateObjectRes,
        )

    @classmethod
    def idsm1RepublishObjectSvc(cls, inputs: IDSM1RepublishObjectIn) -> ServiceData:
        """
        publish the object to ODS
        """
        return cls.execute_soa_method(
            method_name='idsm1RepublishObjectSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def idsm1StartAskInfoSvc(cls, inputs: IDSM1StartAskInfoIn) -> IDSM1StartAskInfoRes:
        """
        The 'idsm1StartAskInfoSvc' operation is call used to get the information about the server side staging
        directory i.e. where the files are being transferred on the server side while get type-class mapping file from
        remote site. This basically opens a file transfer channel used to transfer files from the server.
        
        This is the first operation in the sequence which gets information about the Multi-Site staging directory and
        cannot be called in isolation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'idsm1_start_ask_info_1_svc().
        '
        
        Use cases:
        'idsm1StartAskInfoSvc' operation is invoked while getting type class files from the remote site in HTTP
        multisite environment. This is called from database_verify() utility.
        Operation sequence is as below:
        - idsm1StartAskInfoSvc
        - idsm1XferInfoFileSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm1StartAskInfoSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM1StartAskInfoRes,
        )

    @classmethod
    def idsm1VerifyObjectsSvc(cls, input: IDSM1VerifyObjectsIn) -> IDSM1VerifyObjectsRes:
        """
        The 'idsm1VerifyObjectsSvc' operation is used to verify if the object exist at the target site given in
        IDSM1VerifyObjectsIn input object.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is' idsm1_verify_objects_1_svc().'
        
        
        
        Use cases:
        'idsm1VerifyObjectsSvc' operation is called in case of importing stub objects from structure manager where it
        tries to check whether these objects exist at target site and their verdict in HTTP multisite environment.
        """
        return cls.execute_soa_method(
            method_name='idsm1VerifyObjectsSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'input': input},
            response_cls=IDSM1VerifyObjectsRes,
        )

    @classmethod
    def idsm1XferInfoFileSvc(cls, inputs: IDSM1XferInfoFileIn) -> IDSM1XferInfoFileRes:
        """
        The 'idsm1XferInfoFileSvc' operation transfers the type class mapping file from the remote site(s) Multi-Site
        staging directory to the local site Multi-Site staging directory. 
        
        This is the second operation in the sequence and cannot be called in isolation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is' idsm1_xfer_info_file_1_svc().'
        
        
        Use cases:
        idsm1XferInfoFileSvc operation is invoked while getting type class files from the remote site in HTTP multisite
        environment. This is called from database_verify() utility.
        Operation sequence is as below:
        - idsm1StartAskInfoSvc
        - idsm1XferInfoFileSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm1XferInfoFileSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM1XferInfoFileRes,
        )

    @classmethod
    def idsm2DescribeObjectSvc(cls, inputs: IDSM2DescribeObjectIn) -> IDSM2DescribeObjectRes:
        """
        The 'idsm2DescribeObjectSvc' operation used to retrieve the object description from IDSM server.  Consumer
        should provide the client information and the tag of the object, as an input.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is' idsm2_describe_object_1_svc().'
        
        
        Use cases:
        To import the remote objects at the local site, object(s) published to the Object Directory Service (ODS) needs
        to be first searched and then imported. While loading the ODS published remote objects, this operation is
        called to get the object information.
        """
        return cls.execute_soa_method(
            method_name='idsm2DescribeObjectSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM2DescribeObjectRes,
        )

    @classmethod
    def idsm2VersionCheckSvc(cls, inputs: IDSM2VersionCheckIn) -> IDSM2VersionCheckRes:
        """
        The 'idsm2VersionCheckSvc' operation gets the Integrated Distributed Services Manager (IDSM) server version
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'idsm2_version_check_1_svc().'
        
        
        Use cases:
        'idsm2VersionCheckSvc' operation is called prior to all IDSM requests made by client to check version of IDSM
        for compatibility in HTTP multisite environment.  It is also used by some of the Distributed(DIST) ITKs prior
        to make any IDSM request.
        """
        return cls.execute_soa_method(
            method_name='idsm2VersionCheckSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM2VersionCheckRes,
        )

    @classmethod
    def idsm3EndImportSvc(cls, inputs: IDSM3EndImportIn) -> IDSM1EndImportRes:
        """
        The 'idsm3EndImportSvc' operation imports remote business objects to the local site. When a user at Source Site
        selects business objects (e.g, Item) for remote export, these objects are written into object.meta file at the
        Source Site and transferred over to the Target Site. Integrated Distributed Services Manager (IDSM) service at
        the Target Site imports the content of this file and idsm3EndImportSvc is the last operation in the sequence
        and cannot be called in isolation.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is 'idsm3_end_import_1_svc().'
        
        
        Use cases:
        To Remote Export business object(s), a series of operations needs to be performed and 'idsm3EndImportSvc' gets
        invoked to complete the remote import transaction. 
        Operation sequence for remote export
        - idsm3StartImportSvc
        - idsm4XferImportFileSvc
        - idsm3EndImportSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm3EndImportSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM1EndImportRes,
        )

    @classmethod
    def idsm3ExportStatusSvc(cls, inputs: IDSM3ExportStatusIn) -> IDSM3ExportStatusRes:
        """
        The 'idsm3ExportStatusSvc' operation returns the export/import status of business objects.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding rpc call is 'idsm3_export_status_1_svc().'
        
        
        Use cases:
        - In case of the remote import, this operation is used to check the status of the remote import invoked by the
        earlier call 'idsm3StartExportSvc'(). The status informs the remote site whether import is complete and if it s
        in process, then how many workspace objects are exported so far. The reported workspace objects will be in the
        multiples of 'checkClientAfterNWsos' supplied in the 'IDSM3ExportStatusIn' structure.
        - In case of the remote export, this operation is used to check the status of the remote export finished by the
        earlier call 'idsm3EndImportSvc'(). The status informs the remote site whether export is complete and if it s
        in process, then how many workspace objects are exported so far. The reported workspace objects will be in the
        multiples of 'checkClientAfterNWsos' supplied in the 'IDSM3ExportStatusIn' structure.
        
        """
        return cls.execute_soa_method(
            method_name='idsm3ExportStatusSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM3ExportStatusRes,
        )

    @classmethod
    def idsm3StartImportSvc(cls, inputs: IDSM3StartImportIn) -> IDSM3StartImportRes:
        """
        The 'idsm3StartImportSvc' operation gets information about the server side staging directory i.e. where the
        files are being transferred on the server during export.
        
        This is the first operation in the sequence and cannot be called in isolation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'idsm3_start_import_1_svc().'
        
        
        Use cases:
        To Remote Export business object(s), a series of operations needs to be performed and Idsm3StartImportSvc gets
        invoked as a first step. 
        Operation sequence for remote export.
        - idsm3StartImportSvc
        - idsm4XferImportFileSvc
        - idsm3EndImportSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm3StartImportSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM3StartImportRes,
        )

    @classmethod
    def idsm4CheckSyncStatusSvc(cls, inputs: IDSM4CheckSyncStatusIn) -> IDSM4CheckSyncStatusRes:
        """
        The 'idsm4CheckSyncStatusSvc' operation is used to check the sync status of the input set of object(s) in the
        IDSM4CheckSyncStatusIn structure. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is 'idsm4_check_sync_status_1_svc().
        '
        
        
        Use cases:
        This operation is called from the auto sync handler to retrieve the object sync state. The auto sync handler
        used to extend and customize task actions.
        """
        return cls.execute_soa_method(
            method_name='idsm4CheckSyncStatusSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM4CheckSyncStatusRes,
        )

    @classmethod
    def idsm4GetErrorStackSvc(cls, inputs: IDSM4GetErrorStackIn) -> IDSM4GetErrorStackRes:
        """
        The 'idsm4GetErrorStackSvc' operation is used to retrieve the error stack.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding rpc call is' idsm4_get_error_stack_1_svc().'
        
        
        Use cases:
        While performing the checkpoint transaction, this operation is called from the data_share & data_sync utility.
        """
        return cls.execute_soa_method(
            method_name='idsm4GetErrorStackSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM4GetErrorStackRes,
        )

    @classmethod
    def idsm4RemoteNotificationSvc(cls, inputs: IDSM4RemoteNotificationIn) -> IDSM4RemoteNotificationRes:
        """
        The 'idsm4RemoteNotificationSvc' operation performs remote notification and subscription for object at remote
        site based on IDSM4RemoteNotificationIn input structure.
        
        This is the last operation in the sequence and cannot be called in isolation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'idsm4_remote_notification_1_svc().'
        
        
        Use cases:
        'idsm4RemoteNotificationSvc' operation is called in automatic synchronization to notify and subscribe remote
        site in HTTP multisite environment.
        """
        return cls.execute_soa_method(
            method_name='idsm4RemoteNotificationSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM4RemoteNotificationRes,
        )

    @classmethod
    def idsm4SetSyncOptionsSvc(cls, inputs: IDSM4SetSyncOptionsIn) -> IDSM4SetSyncOptionsRes:
        """
        The 'idsm4SetSyncOptionsSvc' operation used to sets sync options on the objects after object import from
        importing site.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'idsm4_set_sync_options_1_svc ().'
        
        
        Use cases:
        'idsm4SetSyncOptionsSvc' operation is called during remote import and is called from importing site in HTTP
        multisite environment.
        """
        return cls.execute_soa_method(
            method_name='idsm4SetSyncOptionsSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM4SetSyncOptionsRes,
        )

    @classmethod
    def idsm4XferExportFileSvc(cls, inputs: IDSM4XferExportFileIn) -> IDSM4XferExportFileRes:
        """
        The 'idsm4XferExportFileSvc' operation transfers object.meta file and bulk data files from the local site s
        Multi-Site staging directory to the remote Integrated Distributed Services Manager (IDSM) site s Multi-Site
        staging directory.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is 'idsm4_xfer_export_file_1_svc().'
        
        
        Use cases:
        To remote import the business object, first the source site user creates an Item and publishes it to the
        default Object Directory Service (ODS).  The target site user performs remote search with the item id and
        imports it to the target site using the remote import operation. On successful completion of remote import
        operation, the item is imported to the target site database. To Remote Import the business object, the series
        of operations needs to be performed and this operation gets invoked as a last step in the Remote Import
        transaction. The sequence of operations are as below 
        - idsm7StartExportSvc
        - idsm3ExportStatusSvc
        - idsm4XferExportFileSvc
        - idsm1EndExportSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm4XferExportFileSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM4XferExportFileRes,
        )

    @classmethod
    def idsm4XferImportFileSvc(cls, inputs: IDSM4XferImportFileIn) -> IDSM4XferImportFileRes:
        """
        The 'idsm4XferImportFileSvc' operation transfers object.meta file and bulk data files from the remote site(s)
        Multi-Site staging directory to the local site Multi-Site staging directory. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is 'idsm4_xfer_import_file_1_svc().'
        
        
        Use cases:
        To Remote Export business object(s), a series of operations needs to be performed and idsm4XferImportFileSv
        gets invoked to perform the object.meta file and bulk data file from remote site to local site. 
        Operation sequence for remote export
        - idsm3StartImportSvc
        - idsm4XferImportFileSvc
        - idsm3EndImportSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm4XferImportFileSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM4XferImportFileRes,
        )

    @classmethod
    def idsm6DescribeItemSvc(cls, inputs: IDSM6DescribeItemIn) -> IDSM6DescribeItemRes:
        """
        The 'idsm6DescribeItemSvc' operation retrieves item information for a given item.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is 'idsm6_describe_item_1_svc().'
        
        
        Use cases:
        This operation is called from data_share utility, for reporting the duplicate items. For the supplied item id,
        this operation will get item information available with the remote Integrated Distributed Services Manager
        (IDSM) server and reports the duplicate items.
        """
        return cls.execute_soa_method(
            method_name='idsm6DescribeItemSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM6DescribeItemRes,
        )

    @classmethod
    def idsm6EndExportItemIdListSvc(cls, inputs: IDSM6EndExportItemIdListIn) -> ServiceData:
        """
        The 'idsm6EndExportItemIdListSvc' is used to delete the server staging directory, and set finished status. 
        This is the last operation in the sequence of remote item id import operation and finishes the remote item id
        import process.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding rpc call is 'idsm6_end_export_item_id_list_1_svc().'
        
        
        Use cases:
        At the moment this API is not used, and it may be added considering future requirement.
        """
        return cls.execute_soa_method(
            method_name='idsm6EndExportItemIdListSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def idsm6EndSendObjectsSvc(cls, inputs: IDSM6EndSendObjectsIn) -> ServiceData:
        """
        The 'idsm6EndSendObjectsSvc' ends the system object s remote import process. The operation gets called, if
        abort flag is set to true by the previous operation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is' idsm6_end_ send_objects_1_svc().'
        
        
        Use cases:
        This operation is called from the 'distributed_execute' utility. The utility is used to generate the item
        reports locally as well as remotely. To generate the report, internally this utility calls the 'item_report'
        utility.
        """
        return cls.execute_soa_method(
            method_name='idsm6EndSendObjectsSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def idsm6PerformSendObjectsSvc(cls, inputs: IDSM6PerformSendObjectsIn) -> IDSM6PerformSendObjectsRes:
        """
        The 'idsm6PerformSendObjectsSvc' operation sends system objects to the remote site based on
        IDSM6PerformSendObjectsIn input.  This is the third operation in the sequence used in sending system objects
        such as Users, Groups, Persons, etc to the remote site. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'idsm6_perform_send_objects_1_svc().'
        
        
        Use cases:
        'idsm6StartSendObjectsSvc' operation gets invoked from   dsa_util  utility while sending system objects such as
        Users, Groups, Persons, etc to remote site.
        Operation sequence is as below
        - idsm6StartSendObjectsSvc
        - file transfer via DIST call
        - idsm6PerformSendObjectsSvc  
        - idsm6EndSendObjectsSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm6PerformSendObjectsSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM6PerformSendObjectsRes,
        )

    @classmethod
    def idsm6StartExportItemIdListSvc(cls, inputs: IDSM6StartExportItemIdListIn) -> IDSM6StartExportItemIdListRes:
        """
        The 'idsm6StartExportItemIdListSvc' operation gets information about the server side staging directory and
        output export files. 
        
        This is the first operation in the sequence and cannot be called in isolation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
                      
        Corresponding RPC call is 'idsm6_start_export_item_id_list_1_svc().'
        
        
        Use cases:
        'idsm6StartExportItemIdListSvc' operation is called from data_share utility while finding duplicate itemids at
        the remote site.
        """
        return cls.execute_soa_method(
            method_name='idsm6StartExportItemIdListSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM6StartExportItemIdListRes,
        )

    @classmethod
    def idsm6StartSendObjectsSvc(cls, inputs: IDSM6StartSendObjectsIn) -> IDSM6StartSendObjectsRes:
        """
        The 'idsm6StartSendObjectsSvc' operation gets information about the server side staging directory i.e. where
        the files are being transferred on the server side while sending system objects to the remote site. 
        
        This is the first operation in the sequence which gets information about the Multi-Site staging directory and
        cannot be called in isolation. 
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is' idsm6_start_send_objects_1_svc().'
        
        
        Use cases:
        'idsm6StartSendObjectsSvc' operation gets invoked from   dsa_util  utility while sending system objects such as
        Users, Groups, Persons, etc to the remote site.
                Operation sequence is as below
        - idsm6StartSendObjectsSvc
        - file transfer via Distributed (DIST) ITK call
        - idsm6PerformSendObjectsSvc  
        - idsm6EndSendObjectsSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm6StartSendObjectsSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM6StartSendObjectsRes,
        )

    @classmethod
    def idsm7AskVersionSvc(cls, inputs: IDSM7AskVersionIn) -> IDSM7AskVersionRes:
        """
        The 'idsm7AskVersionSvc' operation gets the idsm server version information.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'idsm7_ask_version_1_svc().'
        
        
        Use cases:
        'idsm7AskVersionSvc' operation is called during remote check-in operation.
        """
        return cls.execute_soa_method(
            method_name='idsm7AskVersionSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM7AskVersionRes,
        )

    @classmethod
    def idsm7DistributedAppSvc(cls, inputs: IDSM7DistributedAppIn) -> IDSM7DistributedAppRes:
        """
        This distributed call checks, if the Integrated Distributed Services Manager (IDSM) provides the supplied
        service to the client. The op codes are used to specify the operation. Please refer the 'IDSM7DistributedAppIn'
        structure for the list of op codes.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is 'idsm7_distributed_app_1_svc().'
        
        
        Use cases:
        This operation is called from the' DIST_IDSM_commit_synchronous_remote_import()', to check if the commit
        synchronous remote import operation supported by IDSM server.
        """
        return cls.execute_soa_method(
            method_name='idsm7DistributedAppSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM7DistributedAppRes,
        )

    @classmethod
    def idsm7StartExportSvc(cls, inputs: IDSM7StartExportIn) -> IDSM7StartExportRes:
        """
        The 'idsm7StartExportSvc' operation exports business objects at the remote site during a Remote Import
        transaction. When a user at Source Site selects business objects (e.g, Item) for remote import, the request is
        sent to the Target Site to export these objects into object.meta file at the Target Site and transferred over
        to the Source Site (requesting site). IDSM service at the Target Site exports the objects and creates
        object.meta file. The 'idsm7StartExportSvc' is the first operation in the sequence and hence cannot be called
        in isolation.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is' idsm7_start_export_1_svc().'
        
        
        Use cases:
        To remote import the business object, first the source site user creates an Item and publishes it to the
        default Object Directory Service (ODS) site.  The target site user performs remote search with the item id and
        imports it to the target site using the remote import operation. On successful completion of remote import
        operation, the item is imported to the target site database. To Remote Import the business object, the series
        of operations needs to be performed and this operation gets invoked as a first step in the Remote Import
        transaction. 
        The sequence of operations is as below 
        - idsm7StartExportSvc
        - idsm3ExportStatusSvc
        - idsm4XferExportFileSvc
        - idsm1EndExportSvc
        
        """
        return cls.execute_soa_method(
            method_name='idsm7StartExportSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM7StartExportRes,
        )

    @classmethod
    def idsm9DescribeObjectSvc(cls, inputs: IDSM9DescribeObjectIn) -> IDSM9DescribeObjectRes:
        """
        The 'idsm9DescribeObjectSvc' operation used to retrieve the object description from IDSM server.  Consumer
        should provide the client information and the tag of the object, as an input.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        The corresponding RPC call is 'idsm9_describe_object_1_svc().'
        
        
        Use cases:
        To import the remote objects at the local site, object(s) published to the Object Directory Service (ODS) needs
        to be first searched and then imported. While loading the ODS published remote objects, this operation is
        called to get the object information.
        """
        return cls.execute_soa_method(
            method_name='idsm9DescribeObjectSvc',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='RemoteOperation',
            params={'inputs': inputs},
            response_cls=IDSM9DescribeObjectRes,
        )


class ObjectDirectoryService(TcService):

    @classmethod
    def locatePublishedObjects(cls, clientInfo: ClientInfoProperties, objTagAsString: List[str]) -> LocatePublishedObjectResponse:
        """
        The 'locatePublishedObjects' operation locates published objects from the Object Directory Service (ODS) site
        for a given list of Tags.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in an
        HTTP based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence
        is invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods9_locate_object_1_svc()'.
        
        Use cases:
        'locatePublishedObjects' operation gets called while importing stub objects from PSE (Product Structure
        Editor). It tries to locate the stub object by finding its owning site by checking publication record for that
        object. Export Assembly from site1 to site2 with including BOM. On site2, open assembly in PSE and it shows
        components as Remote Object(s), do import on that object(s), which tries to find the owning site of the object.
        """
        return cls.execute_soa_method(
            method_name='locatePublishedObjects',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'objTagAsString': objTagAsString},
            response_cls=LocatePublishedObjectResponse,
        )

    @classmethod
    def publishObjects(cls, clientInfo: ClientInfoProperties, records: List[PublicationRecordProperties]) -> ServiceData:
        """
        The 'publishObjects' operation creates the 'PublicationRecords' at the Object Directory Service (ODS) site for
        each 'PublicationRecordProperties' input given.  
         
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in an
        HTTP based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence
        is invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods9_publish_object_1_svc().'
        
        
        Use cases:
        'publishObjects' operation gets called  in ODS publish object operation. The business object(s) can be shared
        within the Multi-Site federation. To remote import (Pull case) it must be published to the ODS. It can either
        be called from Rich Client (RAC) or from command line data_share (publish switch) utility.
        
        """
        return cls.execute_soa_method(
            method_name='publishObjects',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'records': records},
            response_cls=ServiceData,
        )

    @classmethod
    def queryItemIdRecords(cls, clientInfo: ClientInfoProperties, itemId: List[str]) -> QueryItemIdRecordResponse:
        """
        The 'queryItemIdRecords' operation queries the ItemId Records from the central itemid registry for each
        'BoMfkInfo' input given. It checks whether input itemids are registered or not.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in an
        HTTP basedMulti-Site environment. This operation acts as a wrapper call to server side RPC function and hence
        is invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods9_describe_item_1_svc().'
        
        Use cases:
        'queryItemIdRecords' operation gets invoked in below use cases check whether given itemid is registered or not.
        - New Item creation when auto register is ON.
        - Registering  Item to  registry.
        
        """
        return cls.execute_soa_method(
            method_name='queryItemIdRecords',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'itemId': itemId},
            response_cls=QueryItemIdRecordResponse,
        )

    @classmethod
    def queryPublicationRecords(cls, clientInfo: ClientInfoProperties, queryString: str, sortKeys: List[str], sortOrder: List[int]) -> QueryPublicationRecordsResponse:
        """
        The 'queryPublicationRecords' operation queries the PublicationRecords from the Object Directory Service (ODS)
        site based on the input query String. This query string should be in POM SQL query format.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in an
        HTTP based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence
        is invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods9_execute_query_1_svc().'
        
        
        Use cases:
        'queryPublicationRecords' operation is called in ODS Remote search operation from the Rich Client (RAC) .It
        searches the ODS server for published objects that satisfy the search criteria.
        """
        return cls.execute_soa_method(
            method_name='queryPublicationRecords',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'queryString': queryString, 'sortKeys': sortKeys, 'sortOrder': sortOrder},
            response_cls=QueryPublicationRecordsResponse,
        )

    @classmethod
    def unpublishObjects(cls, clientInfo: ClientInfoProperties, objTagAsString: List[str]) -> ServiceData:
        """
        The 'unpublishObjects' operation deletes the PublicationRecord from the Object Directory Service (ODS) site for
        each 'objTagAsString' input given.  
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in an
        HTTP based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence
        is invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods9_unpublish_object_1_svc().'
        
        Use cases:
        'unpublishObjects' operation gets called in ODS unpublish object operation. In Multi-Site federation to remote
        import (Pull case) the Business Object (BO), it must be published to the ODS. And to revoke the sharing, the
        business object should be unpublished from ODS. It can either be called from Rich Client (RAC) or from command
        line data_share (unpublish switch) utility.
        
        """
        return cls.execute_soa_method(
            method_name='unpublishObjects',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'objTagAsString': objTagAsString},
            response_cls=ServiceData,
        )

    @classmethod
    def updatePublicationRecords(cls, clientInfo: ClientInfoProperties, records: List[PublicationRecordProperties]) -> ServiceData:
        """
        The 'updatePublicationRecords' opertaion updates the PublicationRecord at the Object Directory Service (ODS)
        site for each 'PublicationRecordProperties' input given.  
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods9_refresh_object_1_svc().'
        
        
        Use cases:
        'updatePublicationRecords' operation gets invoked in Integrated Distributed Service Manager (IDSM) re-publish
        object operation after object is exported to other site with ownership transfer in use cases like remote
        import/export. The ownership transfer operation performed on the business objects (BOs) change its ownership.
        After transfer of ownership, if it is not re-published then the BO has the wrong entry for the owning siteId in
        PublicationRecord at ODS site. In order to correct it, the BOs needs to be republished to the ODS server.
        """
        return cls.execute_soa_method(
            method_name='updatePublicationRecords',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'records': records},
            response_cls=ServiceData,
        )

    @classmethod
    def createItemIdRecords(cls, clientInfo: ClientInfoProperties, records: List[ItemIdRecordsProperties]) -> ServiceData:
        """
        The 'createItemIdRecords' operation creates Item Records in the item registry based on
        'ItemIdRecordsProperties' input.
        
        This operation is integrated with Multi-Site Remote Procedure Call ( RPC) framework and is callable only in an
        HTTP based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence
        is invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods9_register_item_1_svc()'.
        
        
        Use cases:
        - Admin user(s) set the 'ITEM_id_always_register_on_creation' to TRUE on all sites within a Multi-Site
        federation. On item creation the items created automatically registers with the central item registry.
        - Admin user(s) can register existing item(s) with the central item registry, using Register 
        
        """
        return cls.execute_soa_method(
            method_name='createItemIdRecords',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'records': records},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteItemIdRecords(cls, clientInfo: ClientInfoProperties, itemId: List[str]) -> ServiceData:
        """
        The 'deleteItemIdRecords' operation deletes Item Records from the item registry for each 'BoMfkInfo' input.
        
        This operation is integrated with Multi-Site Remote Procedure Call ( RPC) framework and is callable only in an
        HTTP based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence
        is invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods9_unregister_item_1_svc()'.
        
        
        Use cases:
        Admin user(s) can unregister existing item(s) from the central item registry, using Unregister Item Id command
        in the Rich Client (RAC) or command line utility data_share  f=unregister.
        """
        return cls.execute_soa_method(
            method_name='deleteItemIdRecords',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'itemId': itemId},
            response_cls=ServiceData,
        )

    @classmethod
    def describePublicationRecords(cls, clientInfo: ClientInfoProperties, publishedObjTagsAsString: List[str]) -> DescribePublicationRecordsResponse:
        """
         The 'describePublicationRecords' operation returns the 'PublicationRecord' properties for a given list of
        published objects. 
         
        This operation is integrated with Multi-Site Remote Procedure Call ( RPC) framework and is callable only in an
        HTTP based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence
        is invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods9_describe_object_1_svc().'
        
        
        Use cases:
        'describePublicationRecords' operation gets called via Object Directory Service (ODS) remote search in HTTP
        Multi-Site environment.  ODS Remote search returns list of the Published objects as per search criteria. For
        the list of published objects, describePublicationRecords operation is called to get the publicationRecord
        properties on each object.
        """
        return cls.execute_soa_method(
            method_name='describePublicationRecords',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'publishedObjTagsAsString': publishedObjTagsAsString},
            response_cls=DescribePublicationRecordsResponse,
        )

    @classmethod
    def distributedApplication(cls, clientInfo: ClientInfoProperties, distAppProps: List[DistributedAppProperties]) -> DistributedAppResponse:
        """
        The 'distributedApplication' operation is a generic operation which is corresponding to its counterpart in
        Remote Procedure Call (RPC).
        
        This operation is integrated with Multi-Site RPC framework and is callable only in HTTP based Multi-Site
        environment. This operation acts as a wrapper call to server side RPC function and hence is invoked from within
        the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods9_distributed_app_1_svc().'
        
        
        Use cases:
        'distributedApplication' operation id used by Distributed (DIST) ITKs to send an RPC call.
        """
        return cls.execute_soa_method(
            method_name='distributedApplication',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo, 'distAppProps': distAppProps},
            response_cls=DistributedAppResponse,
        )

    @classmethod
    def getODSVersion(cls, clientInfo: ClientInfoProperties) -> GetODSVersionResponse:
        """
        The 'getODSVersion' operation gets the Object Directory Service (ODS) server version information.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in HTTP
        based Multi-Site environment. This operation acts as a wrapper call to server side RPC function and hence is
        invoked from within the Multi-Site framework. Consequently no other clients can invoke this operation.
        
        Corresponding RPC call is 'ods9_version_check_1_svc().'
        
        
        Use cases:
        'getODSVersion' operation gets invoked prior to send any ODS requests to ODS server for getting ODS version for
        Multi-site compatibility check.
        """
        return cls.execute_soa_method(
            method_name='getODSVersion',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='ObjectDirectory',
            params={'clientInfo': clientInfo},
            response_cls=GetODSVersionResponse,
        )


class TcEntObjectDirectoryService(TcService):

    @classmethod
    def publishObjects(cls, clientInfo: TcEntClientInfoProperties, records: List[TcEntPublicationRecordProperties]) -> ServiceData:
        """
        The publishObjects operation creates the PublicationRecords on the Object Directory Service (ODS) site for each
        TcEntPublicationRecordProperties input supplied.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        
        
        Use cases:
        The business objects can be shared within the Multi-Site federation. To share it must be published to the
        Object Directory Services (ODS) or exported to the remote site. The 'publishObjects' operation is called while
        publishing the business object to ODS; the Teamcenter Enterprise client calls it.
        """
        return cls.execute_soa_method(
            method_name='publishObjects',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='TcEntObjectDirectory',
            params={'clientInfo': clientInfo, 'records': records},
            response_cls=ServiceData,
        )

    @classmethod
    def queryPublicationRecords(cls, clientInfo: TcEntClientInfoProperties, queryParams: List[QueryPublicationRecordsProperties]) -> QueryPublicationRecordsResponse:
        """
        The 'queryPublicationRecords' operation queries the PublicationRecords from the Object Directory Service (ODS)
        server based on the input query String. This query string should be in POM SQL query format.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        Use cases:
        Within a Multi-Site federation the object published to ODS server can be remote searched from the Rich Client
        (RAC). The 'queryPublicationRecords' operation is called in remote search operation. At ODS server it searches
        for published objects that satisfy the search criteria.
        """
        return cls.execute_soa_method(
            method_name='queryPublicationRecords',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='TcEntObjectDirectory',
            params={'clientInfo': clientInfo, 'queryParams': queryParams},
            response_cls=QueryPublicationRecordsResponse,
        )

    @classmethod
    def republishObjectAfterOwnershipTransfer(cls, clientInfo: TcEntClientInfoProperties, republishParams: List[RepublishObjectInputProperties]) -> ServiceData:
        """
        The 'republishObjectAfterOwnershipTransfer' operation is used by Teamcenter Enterprise client to re-publish the
        objects, after ownership transfer performed. It updates the PublicationRecord on the Object Directory Services
        (ODS) server for each 'RepublishObjectInputProperties' input set of objects.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        
        Use cases:
        The ownership transfer operation performed on the business objects (BOs) change its ownership. After transfer
        of ownership, if it is not re-published then the BO has the wrong entry for the owner. In order to correct it,
        the BOs needs to be republished to the ODS server. 'republishObjectAfterOwnershipTransfer' operation is called
        while BOs republished to the ODS server.
        """
        return cls.execute_soa_method(
            method_name='republishObjectAfterOwnershipTransfer',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='TcEntObjectDirectory',
            params={'clientInfo': clientInfo, 'republishParams': republishParams},
            response_cls=ServiceData,
        )

    @classmethod
    def unpublishObjects(cls, clientInfo: TcEntClientInfoProperties, objTagsAsString: List[str]) -> ServiceData:
        """
        The 'unpublishObjects' operation deletes the PublicationRecord from the Object Directory Service  (ODS) site
        for each 'objTagAsString' input set of objects.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        
        Use cases:
        The business objects can be shared within the Multi-Site federation. To share, it must be published to the
        Object Directory Services (ODS) or exported to the remote site. And to revoke the sharing, the business object
        should be unpublished from ODS. The 'unpublishObjects' operation is called while unpublishing the business
        object from ODS; the Teamcenter Enterprise client calls it.
        """
        return cls.execute_soa_method(
            method_name='unpublishObjects',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='TcEntObjectDirectory',
            params={'clientInfo': clientInfo, 'objTagsAsString': objTagsAsString},
            response_cls=ServiceData,
        )

    @classmethod
    def describePublicationRecords(cls, clientInfo: TcEntClientInfoProperties, publishedObjTagAsString: List[str]) -> DescribePublicationRecordsResponse:
        """
        The 'describePublicationRecords' operation returns the PublicationRecord of published objects based on the
        TcEnterprise client information and the published object tag.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        Use cases:
        The 'describePublicationRecords' operation gets called via Object Directory Service (ODS) remote search in HTTP
        Multi-Site environment.  ODS Remote search returns list of the published objects as per search criteria. For
        the list of published object, describePublicationRecords operation is called to get the PublicationRecord
        properties on each object.
        """
        return cls.execute_soa_method(
            method_name='describePublicationRecords',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='TcEntObjectDirectory',
            params={'clientInfo': clientInfo, 'publishedObjTagAsString': publishedObjTagAsString},
            response_cls=DescribePublicationRecordsResponse,
        )

    @classmethod
    def getODSVersion(cls, clientInfo: TcEntClientInfoProperties) -> GetODSVersionResponse:
        """
        The 'getODSVersion' returns the Object Directory Services (ODS) server release information, for the requesting
        TcEnterprise client information.
        
        This operation is integrated with Multi-Site Remote Procedure Call (RPC) framework and is callable only in
        Hypertext Transfer Protocol (HTTP) based Multi-Site environment. This operation acts as a wrapper call to
        server side RPC function and hence is invoked from within the Multi-Site framework. Consequently no other
        clients can invoke this operation.
        
        Use cases:
        Multi-site federation supports the data transfer between different Teamcenter versions, as well with the
        Teamcenter Enterprise. To check the compatibility the 'getODSVersion' operation invoked for checking the
        version of ODS server.
        """
        return cls.execute_soa_method(
            method_name='getODSVersion',
            library='Internal-MultiSite',
            service_date='2007_06',
            service_name='TcEntObjectDirectory',
            params={'clientInfo': clientInfo},
            response_cls=GetODSVersionResponse,
        )
