from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class IDSM1ClientInfo(TcBaseObj):
    """
    'IDSM1ClientInfo' structure holds the client information required to access the remote IDSM server.
    
    :var clientSiteId: Requesting client siteid.
    :var targetSiteId: Target siteid to which request has been sent.       
    
    :var clientNode: Node name of requesting client.
    :var userId: Logged in userid of requesting client
    :var userName: Logged in username of requesting client.
    :var osUserName: OS logged in username of requesting client node.        
    
    :var groupName: Group name of userid of requesting client.
    :var roleName: Role name of userid of requesting client.  
    """
    clientSiteId: int = 0
    targetSiteId: int = 0
    clientNode: str = ''
    userId: str = ''
    userName: str = ''
    osUserName: str = ''
    groupName: str = ''
    roleName: str = ''


@dataclass
class IDSM1EndAskInfoIn(TcBaseObj):
    """
    'IDSM1EndAskInfoIn' structure holds the information required to finish the info file transfer.
    
    :var clientInfo: Correlation id of the IDSM server.
    :var infoType: This is not used internally.
    :var infoStagingDir: Complete path of the staging directory.
    :var abortFlag: Flag to determine the aborted operation.
    """
    clientInfo: IDSM1ClientInfo = None
    infoType: int = 0
    infoStagingDir: str = ''
    abortFlag: bool = False


@dataclass
class IDSM1EndExportIn(TcBaseObj):
    """
    IDSM1EndExportIn structure holds the client information and the server staging directory required to complete the
    remote import operation.
    
    :var clientInfo: Object having the client information.
    :var exportStagingDir: Complete path of the server staging directory.
    :var abortFlag: Flag to determine, if the remote import operation needs to be aborted.
    """
    clientInfo: IDSM1ClientInfo = None
    exportStagingDir: str = ''
    abortFlag: bool = False


@dataclass
class IDSM1EndImportOut(TcBaseObj):
    """
    'IDSM11EndImportOut' structure holds the failures occurred during the remote export transaction.
    
    :var failures: List of failures on IDSM server, the list contain PUID of the failed object along with the ifail
    value.
    """
    failures: List[IdsmIeFailures] = ()


@dataclass
class IDSM1EndImportRes(TcBaseObj):
    """
    'IDSM11EndImportRes' structure holds the details required to access the remote IDSM server.
    
    :var out: List of IDSM failures.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM1EndImportOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM1LocateObjectIn(TcBaseObj):
    """
    'IDSM1LocateObjectIn' structure contains Integrated Distributed Services Manager (IDSM) client info and input
    object tag which needs to be located.
    
    
    :var clientInfo: Object having which has requesting client info.
    :var tagsAsString: Tag string of input object to be located.
    """
    clientInfo: IDSM1ClientInfo = None
    tagsAsString: str = ''


@dataclass
class IDSM1LocateObjectOut(TcBaseObj):
    """
    'IDSM1LocateObjectOut' structure holds owning site information and flag for object existence.
    
    :var found: Flag for object exists or not on remote site.
    :var owningSiteId: Siteid of Owning site of an object.
    :var idsmSiteId: SiteId of IDSM server.
    """
    found: bool = False
    owningSiteId: int = 0
    idsmSiteId: int = 0


@dataclass
class IDSM1LocateObjectRes(TcBaseObj):
    """
    'IDSM1LocateObjectRes' structure holds locating information for input object and 'ServiceData'.
    
    :var out: Object which has owning site info of input object.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM1LocateObjectOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM1RepublishObjectIn(TcBaseObj):
    """
    IDSM1RepublishObjectIn structure contains Integrated Distributed Services Manager (IDSM) client info and other
    information required to republish object to ODS.
    
    
    :var clientInfo: Object having which has requesting client info.
    :var tagsAsString: Tag string of input object to be republished.
    :var odsSiteId: Target ods siteid to which input object to be published.
    """
    clientInfo: IDSM1ClientInfo = None
    tagsAsString: str = ''
    odsSiteId: int = 0


@dataclass
class IDSM1StartAskInfoIn(TcBaseObj):
    """
    IDSM1StartAskInfoIn structure contains Integrated Distributed Services Manager (IDSM) client info and other
    information required to start getting schema info.
    
    
    :var clientInfo: Object which has requesting client info.
    :var infoType: Info type flag as IDSM_schema_info to get type-class information which is required to be fetched
    from remote site.
    """
    clientInfo: IDSM1ClientInfo = None
    infoType: int = 0


@dataclass
class IDSM1StartAskInfoOut(TcBaseObj):
    """
    'IDSM1StartAskInfoOut' structure provides staging directory information.
    
    :var infoFiles: List which has name of the file which has to be pulled by client during file transfer.
    
    :var infoStagingDir: Server side staging directory path, info files pushed to and pulled from this dir.
    """
    infoFiles: List[str] = ()
    infoStagingDir: str = ''


@dataclass
class IDSM1StartAskInfoRes(TcBaseObj):
    """
    'IDSM1StartAskInfoRes' structure provides information required to start importing schema files and ServiceData.
    
    
    :var out: Object which has staging dierctory info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM1StartAskInfoOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM1VerifyObjectsIn(TcBaseObj):
    """
    'IDSM1VerifyObjectsIn' structure holds information required to verify input object and Integrated Distributed
    Services Manager (IDSM) client info.
    
    :var clientInfo: Object which has requesting client info.
    :var objectsToVerify: List of object tag string  to be verified in the database.
    """
    clientInfo: IDSM1ClientInfo = None
    objectsToVerify: List[str] = ()


@dataclass
class IDSM1VerifyObjectsOut(TcBaseObj):
    """
    'IDSM1VerifyObjectsOut' structure contains object verification status and failure code if any.
    
    :var verdicts: List of verdicts after verification of input objects 
                    Below are the valid values of verdict            
    -                  0 = does not exist
    -                  1 = exists
    -                  2 = exists as a readonly copy
    -                  3 = exists as a stub
    
    
    :var failureCodes: List of failure codes if any for each input object.
    """
    verdicts: List[int] = ()
    failureCodes: List[int] = ()


@dataclass
class IDSM1VerifyObjectsRes(TcBaseObj):
    """
    'IDSM1VerifyObjectsRes' structure contains object verification information retrieved from IDSM server and
    ServiceData.
    
    :var out: Object contains input objects verification status.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM1VerifyObjectsOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM1XferInfoFileIn(TcBaseObj):
    """
    'IDSM1XferInfoFileIn' structure holds the information required to transfer files to remote site and Integrated
    Distributed Services Manager (IDSM) client info.
    
    :var clientInfo: Object which has requesting client info.
    :var infoType: Info type flag as IDSM_schema_info to get type-class information which is required to be fetched
    from remote site.
    
    :var infoStagingDir: Server side staging directory path received in first call.
    :var infoFile: Info file which needs to be pulled in suring transfer.
    :var startingBlock: Transfer happens block by block, so index for starting block.
    """
    clientInfo: IDSM1ClientInfo = None
    infoType: int = 0
    infoStagingDir: str = ''
    infoFile: str = ''
    startingBlock: int = 0


@dataclass
class IDSM1XferInfoFileOut(TcBaseObj):
    """
    'IDSM1XferInfoFileOut' structure holds the file data information which is transferred to remote site.
    
    :var fileData: Actual file data which in the form of bytes.
    :var fileDataSize: File data size which is pulled from server.
    :var transferComplete: Flag to indicate whether all file transfer is complete or not.
    :var moreFiles: It transfers oen file at a time, so flag to check whether there are more files to be pulled in.
    """
    fileData: List[int] = ()
    fileDataSize: int = 0
    transferComplete: bool = False
    moreFiles: bool = False


@dataclass
class IDSM1XferInfoFileRes(TcBaseObj):
    """
    'IDSM1XferInfoFileRes' structure holds the file transfer output information.
    
    :var out: Object contains file transfer info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM1XferInfoFileOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM2DescribeObjectIn(TcBaseObj):
    """
    'IDSM2DescribeObjectIn' structure holds the information required to retrieve the business objects attribute
    value(s).
    
    :var clientInfo: An object having the client information.
    :var tagsAsString: Object tag unique for the Teamcenter server session.
    """
    clientInfo: IDSM1ClientInfo = None
    tagsAsString: str = ''


@dataclass
class IDSM2DescribeObjectOut(TcBaseObj):
    """
    'IDSM2DescribeObjectOut' structure holds the description of object hold at IDSM server.
    
    :var objectDesc: An object with the it s description, comprising  of site id, object tag, creataion date and last
    modified date as main constituent.
    """
    objectDesc: IdsmOldObjectDesc = None


@dataclass
class IDSM2DescribeObjectRes(TcBaseObj):
    """
    'IDSM2DescribeObjectRes' structure provides the object information retrieved from IDSM server.
    
    :var out: An object with the it s description, comprising  of site id, object tag, creataion date and last modified
    date as main constituent.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM2DescribeObjectOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM2VersionCheckIn(TcBaseObj):
    """
    'IDSM2VersionCheckIn' structure holds information required to get the IDSM server version.
    
    :var clientInfo: Object which has requesting client info.
    :var clientVersion: Requesting client version.
    """
    clientInfo: IDSM1ClientInfo = None
    clientVersion: int = 0


@dataclass
class IDSM2VersionCheckOut(TcBaseObj):
    """
    'IDSM2VersionCheckOut' structure holds the IDSM server version information.
    
    :var serverVersion: IDSM server version.
    :var clientRejected: Client rejected status if IDSM rejects client for some reason.
    """
    serverVersion: int = 0
    clientRejected: int = 0


@dataclass
class IDSM2VersionCheckRes(TcBaseObj):
    """
    'IDSM2VersionCheckRes' structure holds the IDSM version information and ServiceData.
    
    :var out: Object contains version info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM2VersionCheckOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM3EndImportIn(TcBaseObj):
    """
    'IDSM3EndImportIn' structure holds information required to complete the remote export transaction.
    
    :var clientInfo: Object having the client information.
    :var importObjects: PUIDs of the objects to be imported.
    :var excludeObjects: PUIDs of the objects to be excluded.
    :var importOptions: Import options.
    :var importStagingDir: Complete path of the import staging directory.
    :var abortFlag: Flag to determine the aborted operation.
    :var compressPerformedFlg: Compression flag to determine if compression of the meta file requires.
    """
    clientInfo: IDSM1ClientInfo = None
    importObjects: List[str] = ()
    excludeObjects: List[str] = ()
    importOptions: List[IdsmIeOpt] = ()
    importStagingDir: str = ''
    abortFlag: bool = False
    compressPerformedFlg: int = 0


@dataclass
class IDSM3ExportStatusIn(TcBaseObj):
    """
    'IDSM1ExportStatusIn' structure holds information required to retrieve the status of ongoing import/export
    transaction.
    
    :var clientInfo: Object having the client information.
    :var exportStagingDir: Complete path of the staging directory.
    :var abortExport: Abort export operation.
    :var checkClientAfterNWsos: After no. of workspace objects, check for client, used for polling trigger.
    """
    clientInfo: IDSM1ClientInfo = None
    exportStagingDir: str = ''
    abortExport: bool = False
    checkClientAfterNWsos: int = 0


@dataclass
class IDSM3ExportStatusOut(TcBaseObj):
    """
    'IDSM3ExportStatusOut' structure holds the import/export status returned by 'idsm3ExportStatusSvc' operation. The
    structure also provides information on failures occurred during the remote import/export transaction.
    
    :var exportComplete: Boolean to check, export completion status.
    :var workspaceObjects: Number of workspace objects processed.
    :var exportFiles: List of export files created for workspace object transfer.
    :var failures: List of IDSM import export failures.
    :var exportIfail: Export completion ifail code. It is set to abort ifail code if client ask for the abort.
    :var compressPerformedFlg: The compression flag set to true in order to perform the compression during export.
    """
    exportComplete: bool = False
    workspaceObjects: int = 0
    exportFiles: List[str] = ()
    failures: List[IdsmIeFailures] = ()
    exportIfail: int = 0
    compressPerformedFlg: int = 0


@dataclass
class IDSM3ExportStatusRes(TcBaseObj):
    """
    'IDSM3ExportStatusRes' structure holds the import/export status returned by 'idsm3ExportStatusSvc' operation.
    
    :var out: Export state of the object.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM3ExportStatusOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM3StartImportIn(TcBaseObj):
    """
    'IDSM3StartImportIn' structure contains Integrated Distributed Services Manager (IDSM) client info and required POM
    transmit file  Details, compression flag to start export.
    
    
    :var clientInfo: Object having which has requesting client info.
    :var xmitFname: Path of the multisite transmit file of exporting site copied to file store.
    
    :var compressFlg: Compression flag to check if Compression is active for input files.
    
    :var compressType: Type of compression read  from IDSM_Compression_Type site level preference, its default value of
     InfoZip .
    """
    clientInfo: IDSM1ClientInfo = None
    xmitFname: str = ''
    compressFlg: int = 0
    compressType: str = ''


@dataclass
class IDSM3StartImportOut(TcBaseObj):
    """
    'IDSM3StartImportOut' structure contains information about Multi-site staging directory and compression flag.
    
    
    :var importStagingDir: Server/importing side staging directory path in which exported objects files are  being
    transferred on the server.
    
    :var sendXmitFile: TRUE/FALSE, flag for whether to send POM transmit file from server.
    
    :var compressSupportedFlg: Compression flag to check if Compression is active on server/importing  site or not.
    """
    importStagingDir: str = ''
    sendXmitFile: bool = False
    compressSupportedFlg: int = 0


@dataclass
class IDSM3StartImportRes(TcBaseObj):
    """
    'IDSM3StartImportRes' structure provides staging directory information for starting export and  Servicedata.
    
    
    :var out: Object which has staging directory info.
    
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM3StartImportOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM4CheckSyncStatusIn(TcBaseObj):
    """
    'IDSM4CheckSyncStatusIn' structure holds the information required to retrieve the sync status of the business
    object(s).
    
    :var clientInfo: Object having the client information.
    :var commandToken: Type of operation needs to be performed. The below enum lists the supported operations.
    
    'enum' IDSM_sync_status_command_e
    {
        IDSM_CHECK_EXISTS,
        IDSM_CHECK_SYNCHRONIZABLE,
        IDSM_CHECK_IN_SYNC,
        IDSM_CHECK_IN_SYNC_GMT
    }
    
    :var objectsToCheck: List of PUIDs of the objects in consideration.
    :var lmdDates: Last modified dates of the respective objects.
    """
    clientInfo: IDSM1ClientInfo = None
    commandToken: int = 0
    objectsToCheck: List[str] = ()
    lmdDates: List[DateElement] = ()


@dataclass
class IDSM4CheckSyncStatusOut(TcBaseObj):
    """
    'IDSM4CheckSyncStatusOut' structure holds the business object sync status code and the failure code occurred during
    the sync operation.
    
    :var statusCodes: It is status of object w.r.t to IDSM server 
    - 0 == does not exist
    - 1 == exists
    - 2 == exists as a readonly copy
    - 3 == exists as a stub.
    
    
    :var failureCodes: List of ifail failure codes.
    """
    statusCodes: List[int] = ()
    failureCodes: List[int] = ()


@dataclass
class IDSM4CheckSyncStatusRes(TcBaseObj):
    """
    'IDSM4CheckSyncStatusRes' structure holds the information of the business object sync status with respect to the
    IDSM server.
    
    :var out: Sync state of the object, along with the failure codes.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM4CheckSyncStatusOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM4GetErrorStackIn(TcBaseObj):
    """
    IDSM4GetErrorStackIn structure holds information required to retrieve the error stack.
    
    :var clientInfo: Object having the client information.
    :var extraInt: Extra integer to convey information to the server.
    :var extraString: Extra string to convery information to the server.
    """
    clientInfo: IDSM1ClientInfo = None
    extraInt: int = 0
    extraString: str = ''


@dataclass
class IDSM4GetErrorStackOut(TcBaseObj):
    """
    'IDSM4GetErrorStackOut' structure holds the error stack.
    
    :var nStackEntries: Number of errors in the error stack.
    :var errorCodes: List of error codes.
    :var errorText: Error texts with respect to the error code.
    :var extraInt: Extra integer to convey the message to client. Now 1000 & 0 are used.
    :var extraString: Extra character(s) can be appended. E.g. The  \0 appended at the end.
    """
    nStackEntries: int = 0
    errorCodes: List[int] = ()
    errorText: List[str] = ()
    extraInt: int = 0
    extraString: str = ''


@dataclass
class IDSM4GetErrorStackRes(TcBaseObj):
    """
    'IDSM4GetErrorStackRes' structure holds the error stack along with the information required for logging.
    
    :var out: List of errors available in the stack.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM4GetErrorStackOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM4RemoteNotificationIn(TcBaseObj):
    """
    'IDSM4RemoteNotificationIn' structure contains Integrated Distributed Services Manager (IDSM)  client info and
    other  information required to notify remote site.
    
    
    :var clientInfo: Object which has requesting client info.
    :var eventTypeName: Event type string for sending notification type to the remote site. 
    
    :var replicatedObjects: List of tag strings of input objects for which the notiifiction required to send at remote
    site.
    """
    clientInfo: IDSM1ClientInfo = None
    eventTypeName: str = ''
    replicatedObjects: List[str] = ()


@dataclass
class IDSM4RemoteNotificationOut(TcBaseObj):
    """
    'IDSM4RemoteNotificationOut' structure provides failure code information.
    
    :var failureCodes: List of failure codes returned for each object given as an input.
    """
    failureCodes: List[int] = ()


@dataclass
class IDSM4RemoteNotificationRes(TcBaseObj):
    """
    'IDSM4RemoteNotificationRes' structure provides notification  information and 'ServiceData'.
    
    
    :var out: Object which has failure info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM4RemoteNotificationOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM4SetSyncOptionsIn(TcBaseObj):
    """
    'IDSM4SetSyncOptionsIn' structure contains Integrated Distributed Services Manager (IDSM) 
    client info and other information required to set sync options.
    
    
    :var clientInfo: Object which has requesting client info.
    :var optionsToken: Sync option token integer value. Below are the valid values of        
                  option token
    #define OBJIO_auto_sync                         1
    #define OBJIO_batch_sync                        2
    #define OBJIO_do_not_sync                       3
    #define OBJIO_auto_sync_and_notify            101
    #define OBJIO_batch_sync_but_notify           102
    #define OBJIO_do_not_sync_but_notify          103
    #define OBJIO_notify_and_sync_unchanged       104
    #define OBJIO_no_notify_and_sync_unchanged    105
    
    :var objectsOfInterest: List of object tag string for which sync options to be set.
    
    :var objectsNotifyOption: List of notification subscriptions option flag for each object in objectsOfInterest list.
    """
    clientInfo: IDSM1ClientInfo = None
    optionsToken: int = 0
    objectsOfInterest: List[str] = ()
    objectsNotifyOption: List[bool] = ()


@dataclass
class IDSM4SetSyncOptionsOut(TcBaseObj):
    """
    'IDSM4SetSyncOptionsOut' structure provides failure code info per object.
    
    :var failureCodes: List for failure code for each input object.
    """
    failureCodes: List[int] = ()


@dataclass
class IDSM4SetSyncOptionsRes(TcBaseObj):
    """
    'IDSM4SetSyncOptionsRes' structure provides information returned after setting sync options
     and 'ServiceData'.
    
    
    :var out: Object which has failure info if any.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM4SetSyncOptionsOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM4XferExportFileIn(TcBaseObj):
    """
    'IDSM4XferExportFileIn' structure holds the client and server information required to complete the file transfer
    from target site to source site.
    
    :var clientInfo: Object having the client information.
    :var exportStagingDir: Complete path of the server side staging directory.
    :var exportFile: Export file name.
    :var startingPosition: This attribute not used, pass 0.
    :var command: For import case pass CMD_get.    
    'enum' FTCommand 
    { 
        CMD_send, 
        CMD_get, 
        CMD_abort, 
        CMD_close 
    }
    
    :var extraInt: This attribute not used, pass 0.
    :var extraString: This attribute not used pass empty string.
    """
    clientInfo: IDSM1ClientInfo = None
    exportStagingDir: str = ''
    exportFile: str = ''
    startingPosition: int = 0
    command: int = 0
    extraInt: int = 0
    extraString: str = ''


@dataclass
class IDSM4XferExportFileOut(TcBaseObj):
    """
    'IDSM4XferExportFileOut' structure holds the information of remote server and the transferred file.
    
    :var portNumber: IDSM Server port number.
    :var serverId: IDSM server id.
    :var fileSize: File size of the transferred file.
    :var extraInt: This attribute not used, and returned as zero.
    :var extraString: This attribute not used and returned as empty string.
    """
    portNumber: int = 0
    serverId: int = 0
    fileSize: str = ''
    extraInt: int = 0
    extraString: str = ''


@dataclass
class IDSM4XferExportFileRes(TcBaseObj):
    """
    'IDSM4XferExportFileRes' structure holds the remote server information, returned by the 
    'idsm4XferExportFileSvc' operation.
    
    
    :var out: Object of IDSM4XferExportFileOut structure.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM4XferExportFileOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM4XferImportFileIn(TcBaseObj):
    """
    'IDSM4XferImportFileIn' structure holds the client and server information required to complete the file transfer
    from source site to target site.
    
    :var clientInfo: Object having the client information.
    :var importStagingDir: Complete path of the server side staging directory.
    :var importFile: Import file name.
    :var fileSize: File size.
    :var command: For import case pass CMD_send.
    'enum' FTCommand 
    { 
        CMD_send, 
        CMD_get, 
        CMD_abort, 
        CMD_close 
    }
    
    :var extraInt: This attribute not used, pass 0.
    :var extraString: This attribute not used pass empty string.
    """
    clientInfo: IDSM1ClientInfo = None
    importStagingDir: str = ''
    importFile: str = ''
    fileSize: str = ''
    command: int = 0
    extraInt: int = 0
    extraString: str = ''


@dataclass
class IDSM4XferImportFileOut(TcBaseObj):
    """
    'IDSM4XferImportFileOut' structure holds the information of remote server and the transferred file.
    
    :var portNumber: IDSM Server port number.
    :var serverId: IDSM server id.
    :var extraInt: This attribute not used, and returned as zero.
    :var extraString: This attribute not used, and returned as zero.
    """
    portNumber: int = 0
    serverId: int = 0
    extraInt: int = 0
    extraString: str = ''


@dataclass
class IDSM4XferImportFileRes(TcBaseObj):
    """
    'IDSM4XferImportFileRes' structure holds the remote server information, returned by the 
    'idsm4XferImportFileSvc' operation.
    
    
    :var out: Object of 'IDSM4XferExportFileOut' structure.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM4XferImportFileOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM6DescribeItemIn(TcBaseObj):
    """
    'IDSM6DescribeItemIn' structure holds the information required to retrieve the item s attribute value(s).
    
    :var clientInfo: Object having the client information.
    :var itemId: Unique item id.
    """
    clientInfo: IDSM1ClientInfo = None
    itemId: str = ''


@dataclass
class IDSM6DescribeItemOut(TcBaseObj):
    """
    'IDSM6DescribeItemOut' structure holds the values and names of attributes retrieved from the IDSM server.
    
    :var attributes: List provides values for an item attribute name.
    :var attributeNames: List provides the available attribute names for an item.
    """
    attributes: List[str] = ()
    attributeNames: List[str] = ()


@dataclass
class IDSM6DescribeItemRes(TcBaseObj):
    """
    'IDSM6DescribeItemRes' structure provides the item information retrieved from IDSM server.
    
    :var out: Attributes values of item.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM6DescribeItemOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM6EndExportItemIdListIn(TcBaseObj):
    """
    'IDSM6EndExportItemIdListIn' structure holds the necessary information to finish the remote item id import
    operation.
    
    :var clientInfo: Object having the client information.
    :var exportStagingDir: Complete path of the server side staging directory.
    """
    clientInfo: IDSM1ClientInfo = None
    exportStagingDir: str = ''


@dataclass
class IDSM6EndSendObjectsIn(TcBaseObj):
    """
    'IDSM6EndSendObjectsIn' structure holds the client information required to execute the distributed_execute utility
    remotely.
    
    :var clientInfo: Object having the client information.
    :var serverStagingDir: Complete path of the server staging directory.
    :var abortFlag: Flag to determine, if the export operation to be aborted after object send complete.
    """
    clientInfo: IDSM1ClientInfo = None
    serverStagingDir: str = ''
    abortFlag: bool = False


@dataclass
class IDSM6PerformSendObjectsIn(TcBaseObj):
    """
    'IDSM6PerformSendObjectsIn' structure contains Integrated Distributed Services Manager (IDSM) client info and other
    information required to send system objects to remote site.
    
    
    :var clientInfo: Object having which has requesting client info.
    :var serverStagingDir: Staging directory, files pushed from and pulled to this dir.
    :var emailAddresses: List of email addresses. Array of email addresses to which to send remote report.( Number of
    email addresses == 0  implies no need to generate remote report file, unless required by report_file parameter or
    remote email reference.)
    
    :var substitutions: List of 'SendObjectsSubstitutions' objects which has attribute substitution specifications.
    
    :var retentions: List of 'SendObjectsRetentions' objects which has attribute retentions.
    
    :var compressPerformedFlg: Compression flag to check if Compression is active.
    :var commandToPerform: Type of operation need to perform. The below enum 
                   lists the supported operations.
    typedef enum IDSM_send_sys_objects_cmd_e
    {
        IDSM_DSA_distribute_op,        
        IDSM_DSA_preview_distribute_op, 
        IDSM_DSA_diff_op                
    } IDSM_send_sys_objects_cmd_t;
    #define DSAM_item_report_merge          665
    #define DSAM_item_report_item_traversal 666
    #define DSAM_item_report                667
    #define DSAM_cleanup_shared_objects     668
    #define DSAM_fix_release_status         669
    #define DSAM_purge_datasets             670
    #define DSAM_export_recovery            671
    #define DSAM_item_export                672
    #define DSAM_datashare                  673
    
    :var commandOptionFlags: Operation command option flag.
    :var abortOnError: Flag to deteremine aborting on error.
    :var objectsXmlFile: XML objects file to send to remote site.
    :var plmxmlFileFormat: TRUE/FALSE, XML objects file is in plmxml format.
    :var objectsXmlFileOut: If sending objects for comparison or diff, name of XML file with remote objects to be
    pulled back.
    
    :var errorFile: Name of remote error file to pull back. (NULL implies no need to generate error file.).
    
    :var reportFile: Name of remote report file to pull back.(NULL implies no need to  generate remote report file,
    unless required by email_addresses  or remote email preference.).
    """
    clientInfo: IDSM1ClientInfo = None
    serverStagingDir: str = ''
    emailAddresses: List[str] = ()
    substitutions: List[SendObjectsSubstitutions] = ()
    retentions: List[SendObjectsRetentions] = ()
    compressPerformedFlg: int = 0
    commandToPerform: int = 0
    commandOptionFlags: int = 0
    abortOnError: bool = False
    objectsXmlFile: str = ''
    plmxmlFileFormat: bool = False
    objectsXmlFileOut: str = ''
    errorFile: str = ''
    reportFile: str = ''


@dataclass
class IDSM6PerformSendObjectsOut(TcBaseObj):
    """
    'IDSM6PerformSendObjectsOut' structure contains export/import status information.
    
    :var returnFiles: List of output files to be retruned to the client. It contains report file, status file etc for
    export/import operation.
    
    :var compressSupportedFlg: Compression flag to check if Compression is active.
    """
    returnFiles: List[str] = ()
    compressSupportedFlg: int = 0


@dataclass
class IDSM6PerformSendObjectsRes(TcBaseObj):
    """
    'IDSM6PerformSendObjectsRes' structure provides information returned after sending objects to remote site and
    ServiceData.
    
    
    :var out: Object which has status info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM6PerformSendObjectsOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM6StartExportItemIdListIn(TcBaseObj):
    """
    'IDSM6StartExportItemIdListIn' structure contains Integrated Distributed Services Manager (IDSM) client info and
    other information required to start export itemids list.
    
    
    :var clientInfo: Object which has requesting client info.
    :var queryStrings: List of query strings for querying itemids.
    :var compressFlg: Compression flag to check if Compression is active.
    :var compressType: Type of compression read  from IDSM_Compression_Type site level preference, its default value of
      InfoZip .
    """
    clientInfo: IDSM1ClientInfo = None
    queryStrings: List[str] = ()
    compressFlg: int = 0
    compressType: str = ''


@dataclass
class IDSM6StartExportItemIdListOut(TcBaseObj):
    """
    'IDSM6StartExportItemIdListOut' structure provides staging directory and other information.
    
    
    :var exportFiles: List  which has name of the file which has to be pulled by client during file transfer.
    
    :var exportStagingDir: Server side staging directory path, exportFiles files pushed to and pulled from this dir.
    
    :var compressPerformedFlg: Compression flag to check whether exportFiles are compressed or not. IF compression is
    done set the correct flag for decompressing later in the flow.
    """
    exportFiles: List[str] = ()
    exportStagingDir: str = ''
    compressPerformedFlg: int = 0


@dataclass
class IDSM6StartExportItemIdListRes(TcBaseObj):
    """
    'IDSM6StartExportItemIdListRes' structure provides information required to start import and ServiceData.
    
    
    :var out: Object which has staging directory info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM6StartExportItemIdListOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM6StartSendObjectsIn(TcBaseObj):
    """
    'IDSM6StartSendObjectsIn' Integrated Distributed Services Manager (IDSM)  client information and compression
    details.
    
    
    :var clientInfo: Object which has requesting client info.
    :var compressFlg: Compression flag to check if Compression is active or not.
    :var compressType: Type of compression read  from IDSM_Compression_Type site level preference, its default value of
      InfoZip .
    """
    clientInfo: IDSM1ClientInfo = None
    compressFlg: int = 0
    compressType: str = ''


@dataclass
class IDSM6StartSendObjectsOut(TcBaseObj):
    """
    'IDSM6StartSendObjectsOut' structure contains server side staging directory and compression flag.
    
    :var serverStagingDir: Server/importing side staging directory path in which object XML files are  being
    transferred on the server.
    
    :var compressSupportedFlg: Compression flag to check if Compression is active on server/importing  site or not.
    """
    serverStagingDir: str = ''
    compressSupportedFlg: int = 0


@dataclass
class IDSM6StartSendObjectsRes(TcBaseObj):
    """
    'IDSM6StartSendObjectsRes' structure contains information required to start the export and ServiceData.
    
    :var out: Object which has staging directory info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM6StartSendObjectsOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM7AskVersionIn(TcBaseObj):
    """
    'IDSM7AskVersionIn' structure holds the Integrated Distributed Services Manager (IDSM) client information required
    to access the remote IDSM server.
    
    :var clientInfo: Object which has requesting client info.
    """
    clientInfo: IDSM1ClientInfo = None


@dataclass
class IDSM7AskVersionOut(TcBaseObj):
    """
    'IDSM7AskVersionOut' structure holds IDSM server major and minor version.
    
    :var serverMajorVersion: IDSM server major version.
    :var serverMinorVersion: IDSM server minor version.
    :var serverQrmNumber: IDSM server qrm number.
    :var serverIrmNumber: IDSM server irm number.
    """
    serverMajorVersion: int = 0
    serverMinorVersion: int = 0
    serverQrmNumber: int = 0
    serverIrmNumber: int = 0


@dataclass
class IDSM7AskVersionRes(TcBaseObj):
    """
    'IDSM7AskVersionRes' structure holds IDSM server version information and ServiceData.
    
    :var out: Object which has version info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM7AskVersionOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM7DistributedAppIn(TcBaseObj):
    """
    'IDSM7DistributedAppIn' structure holds the client information required to make the distributed call.
    
    :var clientInfo: An object having the client information.
    :var imanVersion: Teamcenter client version, internally this is converted to the client major version and minor
    version.
    :var imanIrmNumber: Teamcenter patch number.
    :var appName: Name of the application, client want to check service for.
    :var appOpCode: Op code of the service.
    - DIST_IDSM_commit_synchronous_remote_import_op          0
    - DIST_IDSM_exchange_supported_feature_set_op            1
    - DIST_IDSM_ask_imported_sst_uids_op                     2
    - DIST_IDSM_perform_checkpoint_function_op               3
    - DIST_IDSM_identify_sst_client_op                       4
    - DIST_IDSM_is_process_dead_op                           5
    - DIST_IDSM_ask_server_process_info_op                   6
    - DIST_IDSM_describe_object_l10n_attr_op                 7
    - DIST_IDSM_start_plmxml_sync_op                         8
    - DIST_IDSM_set_remote_site_logger_level_op           9
    
    
    :var appInputStrings: List of input strings for the controller.
    """
    clientInfo: IDSM1ClientInfo = None
    imanVersion: int = 0
    imanIrmNumber: int = 0
    appName: str = ''
    appOpCode: int = 0
    appInputStrings: List[str] = ()


@dataclass
class IDSM7DistributedAppOut(TcBaseObj):
    """
    'IDSM7DistributedAppOut' structure holds the strings returned by the controller.
    
    :var appOutputStrings: List of strings returned by the controller.
    """
    appOutputStrings: List[str] = ()


@dataclass
class IDSM7DistributedAppRes(TcBaseObj):
    """
    'IDSM7DistributedAppRes' structure holds the description of the service.
    
    :var out: An object with the service description.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM7DistributedAppOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM7StartExportIn(TcBaseObj):
    """
    'IDSM7StartExportIn' structure contains Integrated Distributed Services Manager (IDSM) client info and other
    information required for export.
    
    
    :var clientInfo: Object which has requesting client info.
    :var exportObjects: List of tag string of objects to be exported.
    :var excludeObjects: List of tag string of objects to be excluded during export.
    
    :var includeObjects: String vector of tag string of objects to be included during export.
    
    :var reason: User input to explain, why the remote import of business object required. Its not a mandatory input
    and user can pass empty string.
    
    :var exportOptions: List of objects which has IDSM Import and Export options.
    :var compressFlg: Compression flag to check if Compression is active.
    :var compressType: Type of compression read  from IDSM_Compression_Type site level preference, its default value of
      InfoZip .
    
    :var checkClientAfterNWsos: After no. of workspace objects, check for client, used for polling trigger.
    """
    clientInfo: IDSM1ClientInfo = None
    exportObjects: List[str] = ()
    excludeObjects: List[str] = ()
    includeObjects: List[str] = ()
    reason: str = ''
    exportOptions: List[IdsmIeOpt] = ()
    compressFlg: int = 0
    compressType: str = ''
    checkClientAfterNWsos: int = 0


@dataclass
class IDSM7StartExportOut(TcBaseObj):
    """
    'IDSM7StartExportOut' structure contains information about Multi-site staging directory and compression flag.
    
    
    :var exportFiles: Listof export files which has exported objects info created in export staging directory.
    
    :var exportStagingDir: Export staging directory path in which exportFiles files are pushed to and read from this
    directory.
    
    :var failures: Object  which has IDSM failure information.
    :var compressPerformedFlg: Compression flag to check whether exportFiles are compressed or not. IF compression is
    done set the correct flag for decompressing later in the flow.
    """
    exportFiles: List[str] = ()
    exportStagingDir: str = ''
    failures: List[IdsmIeFailures] = ()
    compressPerformedFlg: int = 0


@dataclass
class IDSM7StartExportRes(TcBaseObj):
    """
    'IDSM7StartExportRes' structure provides staging directory information for starting import and ServiceData.
    
    
    :var out: Object which has staging directory info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM7StartExportOut = None
    serviceData: ServiceData = None


@dataclass
class IDSM9DescribeObjectIn(TcBaseObj):
    """
    'IDSM9DescribeObjectIn' structure holds the information required to retrieve the business object s attribute
    value(s).
    
    :var clientInfo: An object having the client information.
    :var tagsAsString: Object tag unique for the Teamcenter server session.
    """
    clientInfo: IDSM1ClientInfo = None
    tagsAsString: str = ''


@dataclass
class IDSM9DescribeObjectOut(TcBaseObj):
    """
    'IDSM9DescribeObjectOut' structure holds the description of object hold at IDSM server.
    
    :var objectDesc: The attribute provides the complete information of the object.
    """
    objectDesc: IdsmObjectDesc = None


@dataclass
class IDSM9DescribeObjectRes(TcBaseObj):
    """
    IDSM9DescribeObjectRes structure provides the object information retrieved from IDSM server.
    
    :var out: An object with the it s description, comprising  of site id, object tag, creataion date and last modified
    date as main constituent.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    """
    out: IDSM9DescribeObjectOut = None
    serviceData: ServiceData = None


@dataclass
class IdsmIeFailures(TcBaseObj):
    """
    'IdsmIeFailures' structure holds the list of object failed to remote export & the respective failures occurred.
    
    :var failingObject: PUID of the failing object.
    :var failureCode: ifail value.
    """
    failingObject: str = ''
    failureCode: int = 0


@dataclass
class IdsmIeOpt(TcBaseObj):
    """
    'IdsmIeOpt' structure holds information which will influence the remote export transaction.
    
    :var optType: An import option.
    :var optValue: Value of an import option.
    """
    optType: int = 0
    optValue: IdsmIeOptVal = None


@dataclass
class IdsmIeOptVal(TcBaseObj):
    """
    'IdsmIeOptVal' structure holds information which will influence the remote export transaction.
    
    :var optVal: Value of an import option.
    :var stringOptVal: Name of the an import option.
    """
    optVal: int = 0
    stringOptVal: str = ''


@dataclass
class IdsmObjectDesc(TcBaseObj):
    """
    IdsmObjectDesc structure holds description of the object hold at IDSM server.
    
    :var siteId: Unique id of site where object belongs to.
    :var tagAsString: Tag of the object unique within Teamcenter session.
    :var objectLastModDate: Last modified date of the object.
    :var objectCreationDate: Creation date of the object.
    :var objectReleaseStatusNames: Release status name applied to the object.
    :var customAttrNames: Any custom attributes applied on the object.
    :var customAttrValues: Values of the custom attributes.
    :var objectId: Unique id of the object.
    :var objectRevId: Revision id of the object.
    :var objectName: Name of the object.
    :var objectDesc: Description of the object.
    :var objectClass: Class of the object.
    :var objectType: Type of the object.
    :var objectOwner: Owner who has object ownership.
    :var objectGroup: Group who has access to this object.
    """
    siteId: int = 0
    tagAsString: str = ''
    objectLastModDate: datetime = None
    objectCreationDate: datetime = None
    objectReleaseStatusNames: List[str] = ()
    customAttrNames: List[str] = ()
    customAttrValues: List[str] = ()
    objectId: str = ''
    objectRevId: str = ''
    objectName: str = ''
    objectDesc: str = ''
    objectClass: str = ''
    objectType: str = ''
    objectOwner: str = ''
    objectGroup: str = ''


@dataclass
class IdsmOldObjectDesc(TcBaseObj):
    """
    IdsmOldObjectDesc structure holds description of the object hold at IDSM server.
    
    
    :var siteId: Unique id of site where object belongs to.
    :var tagAsString: Tag of the object unique within Teamcenter session.
    :var objectCreationDate: Creation date of the object.
    :var objectReleaseStatusNames: Release status name applied to the object.
    :var objectId: Unique id of the object.
    :var objectName: Name of the object.
    :var objectDesc: Description of the object.
    :var objectClass: Class of the object.
    :var objectType: Type of the object.
    :var objectOwner: Owner who has object ownership.
    :var objectGroup: Group who has access to this object.
    :var objectLastModDate: Last modified date of the object.
    """
    siteId: int = 0
    tagAsString: str = ''
    objectCreationDate: datetime = None
    objectReleaseStatusNames: List[str] = ()
    objectId: str = ''
    objectName: str = ''
    objectDesc: str = ''
    objectClass: str = ''
    objectType: str = ''
    objectOwner: str = ''
    objectGroup: str = ''
    objectLastModDate: datetime = None


@dataclass
class SendObjectsRetentions(TcBaseObj):
    """
    'SendObjectsRetentions' structure contains object retention info.
    
    :var className: Class name of the object.
    :var attrName: Attribute name of the object.
    """
    className: str = ''
    attrName: str = ''


@dataclass
class SendObjectsSubstitutions(TcBaseObj):
    """
    'SendObjectsSubstitutions' structure contains object substitution info.
    
    :var className: Class name of the object.
    :var attrName: Attribute name of the object.
    :var attrValue: Attribute value for a given attribute name.
    :var substitutionValue: Substitution value of an attribute.
    """
    className: str = ''
    attrName: str = ''
    attrValue: str = ''
    substitutionValue: str = ''


@dataclass
class DateElement(TcBaseObj):
    """
    DateElement structure holds the timestamp of the business object, and used to capture its last modified date.
    
    :var dateVal: Holds last modified dates of the respective object.
    """
    dateVal: datetime = None
