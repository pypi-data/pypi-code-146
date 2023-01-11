from __future__ import annotations

from tcsoa.gen.Internal.MultiSite._2007_06.RemoteOperation import IdsmIeOpt, SendObjectsRetentions, IdsmObjectDesc, DateElement, SendObjectsSubstitutions, IdsmIeFailures
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class IDSM11CheckSyncStatusIn(TcBaseObj):
    """
    'IDSM11CheckSyncStatusIn' structure holds the information required to retrieve the sync status of the business
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
    clientInfo: IDSM11ClientInfo = None
    commandToken: int = 0
    objectsToCheck: List[str] = ()
    lmdDates: List[DateElement] = ()


@dataclass
class IDSM11CheckSyncStatusOut(TcBaseObj):
    """
    'IDSM11CheckSyncStatusOut' structure holds the business object sync status code and the failure code occurred
    during the sync operation.
    
    :var statusCodes: It is status of object w.r.t to IDSM server 
    - 0 == does not exist
    - 1 == exists
    - 2 == exists as a readonly copy
    - 3 == exists as a stub.
    
    
    :var failureCodes: List of ifail failure codes, occurred during the sync operation.
    """
    statusCodes: List[int] = ()
    failureCodes: List[int] = ()


@dataclass
class IDSM11CheckSyncStatusRes(TcBaseObj):
    """
    'IDSM11CheckSyncStatusRes' structure holds the information of the business object sync status with respect to the
    IDSM server.
    
    :var out: Sync state of the object, along with the failure codes.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, it is added for future use.
    """
    out: IDSM11CheckSyncStatusOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11ClientInfo(TcBaseObj):
    """
    'IDSM11ClientInfo' structure holds the client information required to access the remote IDSM server.
    
    :var clientSiteId: Unique id allocated to client Teamcenter server site.
    :var targetSiteId: IDSM server site ID.
    :var clientNode: Machine name where Teamcenter Server is running.
    :var userId: Teamcenter user ID.
    :var userName: Teamcenter username.
    :var osUserName: Username allocated to user for accessing operating system.
    :var groupName: Teamcenter group associated with the given user name.
    :var roleName: Teamcenter role associated with the given user name.
    :var clientCorrelationId: Correlation id of requesting client.
    :var userDataIp: Currently this attribute not used, it is added for future use.
    """
    clientSiteId: int = 0
    targetSiteId: int = 0
    clientNode: str = ''
    userId: str = ''
    userName: str = ''
    osUserName: str = ''
    groupName: str = ''
    roleName: str = ''
    clientCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11DescribeItemIn(TcBaseObj):
    """
    'IDSM11DescribeItemIn' structure holds the information required to retrieve the item s attribute value(s).
    
    :var clientInfo: An object having the requesting client information.
    :var itemId: Unique item id.
    """
    clientInfo: IDSM11ClientInfo = None
    itemId: str = ''


@dataclass
class IDSM11DescribeItemOut(TcBaseObj):
    """
    'IDSM11DescribeItemOut' structure holds the values and names of attributes retrieved from the IDSM server.
    
    :var attributes: List provides values for an item attribute name.
    :var attributeNames: List provides the available attribute names for an item.
    """
    attributes: List[str] = ()
    attributeNames: List[str] = ()


@dataclass
class IDSM11DescribeItemRes(TcBaseObj):
    """
    'IDSM11DescribeItemRes' structure provides the item information retrieved from IDSM server.
    
    :var out: An object with the item description.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    out: IDSM11DescribeItemOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11DescribeObjectIn(TcBaseObj):
    """
    'IDSM11DescribeObjectIn' structure holds the information required to retrieve the business object s attribute
    value(s).
    
    :var clientInfo: An object having the client information.
    :var tagsAsString: Object tag unique for the Teamcenter server session.
    """
    clientInfo: IDSM11ClientInfo = None
    tagsAsString: str = ''


@dataclass
class IDSM11DescribeObjectOut(TcBaseObj):
    """
    'IDSM11DescribeObjectOut' structure holds the description of object hold at IDSM server.
    
    :var objectDesc: The attribute provides the complete information of the object.
    """
    objectDesc: IdsmObjectDesc = None


@dataclass
class IDSM11DescribeObjectRes(TcBaseObj):
    """
    'IDSM11DescribeObjectRes' structure provides the object information retrieved from IDSM server.
    
    :var out: An object with the it s description, comprising  of site id, object tag, creataion date and last modified
    date as main constituent.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    out: IDSM11DescribeObjectOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11DistributedAppIn(TcBaseObj):
    """
    'IDSM11DistributedAppIn' structure holds the client information required to make the distributed call.
    
    :var clientInfo: An object having the client information.
    :var imanVersion: Teamcenter client version, internally this is converted to the client major version and minor
    version.
    :var imanIrmNumber: Teamcenter patch number.
    :var appName: Name of the application, client want to check service for.
    :var appOpCode: Op code of the service.
    DIST_IDSM_commit_synchronous_remote_import_op          0
    DIST_IDSM_exchange_supported_feature_set_op            1
    DIST_IDSM_ask_imported_sst_uids_op                     2
    DIST_IDSM_perform_checkpoint_function_op               3
    DIST_IDSM_identify_sst_client_op                       4
    DIST_IDSM_is_process_dead_op                           5
    DIST_IDSM_ask_server_process_info_op                   6
    DIST_IDSM_describe_object_l10n_attr_op                 7
    DIST_IDSM_start_plmxml_sync_op                         8
    DIST_IDSM_set_remote_site_logger_level_op           9
    
    :var appInputStrings: List of input strings for the controller.
    """
    clientInfo: IDSM11ClientInfo = None
    imanVersion: int = 0
    imanIrmNumber: int = 0
    appName: str = ''
    appOpCode: int = 0
    appInputStrings: List[str] = ()


@dataclass
class IDSM11DistributedAppOut(TcBaseObj):
    """
    'IDSM11DistributedAppOut' structure holds the strings returned by the controller.
    
    :var appOutputStrings: List of strings returned by the controller.
    """
    appOutputStrings: List[str] = ()


@dataclass
class IDSM11DistributedAppRes(TcBaseObj):
    """
    'IDSM11DistributedAppRes' structure holds the description of the service.
    
    :var out: An object with the service description.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    out: IDSM11DistributedAppOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11EndAskInfoIn(TcBaseObj):
    """
    'IDSM11EndAskInfoIn' structure holds the necessary information to finish the info file transfer.
    
    :var clientInfo: Correlation id of the IDSM server.
    :var infoType: This is not used internally.
    :var infoStagingDir: Complete path of the staging directory.
    :var abortFlag: Flag to determine the aborted operation.
    """
    clientInfo: IDSM11ClientInfo = None
    infoType: int = 0
    infoStagingDir: str = ''
    abortFlag: bool = False


@dataclass
class IDSM11EndExportItemIdListIn(TcBaseObj):
    """
    'IDSM11EndExportItemIdListIn' structure holds the necessary information to finish the remote item id import
    operation.
    
    :var clientInfo: An object having the requesting client information.
    :var exportStagingDir: Path of the export staging directory.
    """
    clientInfo: IDSM11ClientInfo = None
    exportStagingDir: str = ''


@dataclass
class IDSM11EndImportIn(TcBaseObj):
    """
    'IDSM11EndImportIn' structure holds information required to complete the remote export transaction.
    
    :var clientInfo: Object having the client information.
    :var importObjects: PUIDs of the objects to be imported.
    :var excludeObjects: PUIDs of the objects to be excluded.
    :var importOptions: Import options.
    :var importStagingDir: Complete path of the import staging directory.
    :var abortFlag: Flag to determine the aborted operation.
    :var compressPerformedFlg: Compression flag to determine if compression of the meta file requires.
    """
    clientInfo: IDSM11ClientInfo = None
    importObjects: List[str] = ()
    excludeObjects: List[str] = ()
    importOptions: List[IdsmIeOpt] = ()
    importStagingDir: str = ''
    abortFlag: bool = False
    compressPerformedFlg: int = 0


@dataclass
class IDSM11EndImportOut(TcBaseObj):
    """
    'IDSM11EndImportOut' structure holds the failures occurred during the remote export transaction.
    
    :var failures: List of failures on IDSM server, the list contain PUID of the failed object along with the ifail
    value.
    """
    failures: List[IdsmIeFailures] = ()


@dataclass
class IDSM11EndImportRes(TcBaseObj):
    """
    'IDSM11EndImportRes' structure holds the details required to access the remote IDSM server.
    
    :var out: List of IDSM failures.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, it is added for future use.
    """
    out: IDSM11EndImportOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11EndSendObjectsIn(TcBaseObj):
    """
    'IDSM11EndSendObjectsIn' structure holds the client information required to execute the distributed_execute utility
    remotely.
    
    :var clientInfo: Object having the client information.
    :var serverStagingDir: Complete path of the server staging directory.
    :var abortFlag: Flag to determine, if the export operation to be aborted after object send complete.
    """
    clientInfo: IDSM11ClientInfo = None
    serverStagingDir: str = ''
    abortFlag: bool = False


@dataclass
class IDSM11ExportStatusIn(TcBaseObj):
    """
    'IDSM11ExportStatusIn' structure holds information required to retrieve the status of ongoing import/export
    transaction.
    
    :var clientInfo: Object having the client information.
    :var exportStagingDir: Complete path of the staging directory.
    :var abortExport: Abort export operation.
    :var checkClientAfterNWsos: after no. of workspace objects, check for client, used for polling trigger.
    """
    clientInfo: IDSM11ClientInfo = None
    exportStagingDir: str = ''
    abortExport: bool = False
    checkClientAfterNWsos: int = 0


@dataclass
class IDSM11ExportStatusOut(TcBaseObj):
    """
    'IDSM11ExportStatusOut' structure holds the import/export status returned by 'idsm11ExportStatusSvc' operation. The
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
class IDSM11ExportStatusRes(TcBaseObj):
    """
    'IDSM11ExportStatusRes' structure holds the import/export status returned by 'idsm11ExportStatusSvc' operation.
    
    :var out: Export state of the object.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, it is added for future use.
    """
    out: IDSM11ExportStatusOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11FailureRes(TcBaseObj):
    """
    'IDSM11FailureRes' structure provides the partial failures with error message.
    
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11GetErrorStackIn(TcBaseObj):
    """
    'IDSM11GetErrorStackIn' structure holds information required to retrieve the error stack.
    
    :var clientInfo: Object having the client information.
    :var extraInt: Extra integer to convey information to the server.
    :var extraString: Extra string to convery information to the server.
    """
    clientInfo: IDSM11ClientInfo = None
    extraInt: int = 0
    extraString: str = ''


@dataclass
class IDSM11GetErrorStackOut(TcBaseObj):
    """
    'IDSM11GetErrorStackOut' structure holds the error stack.
    
    :var nStackEntries: Number of errors in the error stack.
    :var errorCodes: List of error codes
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
class IDSM11GetErrorStackRes(TcBaseObj):
    """
    'IDSM11GetErrorStackRes' structure holds the error stack along with the information required for logging.
    
    :var out: List of errors available in the stack.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, it is added for future use.
    """
    out: IDSM11GetErrorStackOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11LocateObjectIn(TcBaseObj):
    """
    'IDSM11LocateObjectIn' structure contains Integrated Distributed Services Manager (IDSM)               client info
    and input object tag which needs to be located.
    
    
    :var clientInfo: Object which has requesting client info.
    :var tagsAsString: Tag string of input object to be located.
    """
    clientInfo: IDSM11ClientInfo = None
    tagsAsString: str = ''


@dataclass
class IDSM11LocateObjectOut(TcBaseObj):
    """
    'IDSM11LocateObjectOut' structure holds owning site information and flag for object existence.
    
    :var found: Flag for object exists or not on remote site
    :var owningSiteId: Siteid of Owning site of an object.
    :var idsmSiteId: SiteId of IDSM server.
    """
    found: bool = False
    owningSiteId: int = 0
    idsmSiteId: int = 0


@dataclass
class IDSM11LocateObjectRes(TcBaseObj):
    """
    'IDSM11LocateObjectRes' structure holds locating information for input object and 'ServiceData'.
    
    :var out: Object which has owning site info of input object.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    out: IDSM11LocateObjectOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11PerformSendObjectsIn(TcBaseObj):
    """
    'IDSM11PerformSendObjectsIn' structure contains Integrated Distributed Services Manager 
    (IDSM) client info and other information required to send system objects to remote site.
    
    
    :var clientInfo: Object having which has requesting client info.
    :var serverStagingDir: Staging directory, files pushed from and pulled to this dir.
    :var emailAddresses: List of email addresses. Array of email addresses to which to send remote report.( Number of
    email addresses==0 implies no need to generate remote report file, unless required by 'report_file 'parameter or
    remote email preference.)
    
    :var substitutions: List of 'SendObjectsSubstitutions' objects which has attribute substitution specifications.
    
    :var retentions: List of 'SendObjectsRetentions' objects which has attribute retentions. 
    
    :var compressPerformedFlg: Compression flag to check if Compression is active.
    :var commandToPerform: Type of operation need to perform. The below 'enum' lists the supported operations.
    
    enum IDSM_send_sys_objects_cmd_e
    {
        IDSM_DSA_distribute_op,          //send to site to distribute                 
        IDSM_DSA_preview_distribute_op, // send to site to do a dry run distribute    
        IDSM_DSA_diff_op                // send to site to generate local diff report 
    } IDSM_send_sys_objects_cmd_t;
    
    :var commandOptionFlags: Operation command oprion flag.
    :var abortOnError: Flag to deteremine aborting on error.
    :var objectsXmlFile: XML objects file to send to remote site.
    :var plmxmlFileFormat: TRUE/FALSE, XML objects file is in plmxml format.
    :var objectsXmlFileOut: If sending objects for comparison or diff, name of XML file with remote objects to be
    pulled back.
    
    :var errorFile: Name of remote error file to pull back. (NULL implies no need to generate error file.).
    
    :var reportFile: Name of remote report file to pull back.  (NULL implies no need to  generate remote report file,
    unless required by email_addresses  or remote email preference.).
    """
    clientInfo: IDSM11ClientInfo = None
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
class IDSM11PerformSendObjectsOut(TcBaseObj):
    """
    'IDSM11PerformSendObjectsOut' structure contains export/import status information.
    
    :var returnFiles: List of output files to be returned to the client. It contains report file, status file etc. for
    export/import operation.
    
    :var compressSupportedFlg: Compression flag to check if Compression is active.
    """
    returnFiles: List[str] = ()
    compressSupportedFlg: int = 0


@dataclass
class IDSM11PerformSendObjectsRes(TcBaseObj):
    """
    'IDSM11PerformSendObjectsRes' structure provides information returned after sending objects to remote site and
    ServiceData.
    
    
    :var out: Object which has status info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    out: IDSM11PerformSendObjectsOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11RemoteNotificationIn(TcBaseObj):
    """
    'IDSM11RemoteNotificationIn' structure contains Integrated Distributed Services Manager (IDSM)  client info and
    other  information required to notify remote site.
    
    
    :var clientInfo: Object which has requesting client info.
    :var eventTypeName: Event type string for sending notification type to the remote site.
    
    :var replicatedObjects: List of tag strings of input objects for which the notiifiction required to send at remote
    site.
    """
    clientInfo: IDSM11ClientInfo = None
    eventTypeName: str = ''
    replicatedObjects: List[str] = ()


@dataclass
class IDSM11RemoteNotificationOut(TcBaseObj):
    """
    'IDSM11StartExportItemIdListRes' structure provides failure code information.
    
    :var failureCodes: List of failure codes returned for each object given as an input.
    """
    failureCodes: List[int] = ()


@dataclass
class IDSM11RemoteNotificationRes(TcBaseObj):
    """
    'IDSM11RemoteNotificationRes' structure provides notification  information and 'ServiceData'.
    
    
    :var out: Object which has failure info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    out: IDSM11RemoteNotificationOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11RepublishObjectIn(TcBaseObj):
    """
    IDSM11RepublishObjectIn structure contains Integrated Distributed Services Manager (IDSM) client info and other
    information required to re-publish object to ODS.
    
    
    
    :var clientInfo: Object having which has requesting client info.
    :var tagsAsString: Tag string of input object to be re-published.
    :var odsSiteId: Target ods siteid to which input object to be published.
    """
    clientInfo: IDSM11ClientInfo = None
    tagsAsString: str = ''
    odsSiteId: int = 0


@dataclass
class IDSM11SetSyncOptionsIn(TcBaseObj):
    """
    'IDSM11SetSyncOptionsIn' structure contains Integrated Distributed Services Manager(IDSM) client info and other
    information required to set sync options.
    
    
    :var clientInfo: Object which has requesting client info.
    :var optionsToken: Sync option token integer value. Below are the valid values of option token
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
    clientInfo: IDSM11ClientInfo = None
    optionsToken: int = 0
    objectsOfInterest: List[str] = ()
    objectsNotifyOption: List[bool] = ()


@dataclass
class IDSM11SetSyncOptionsOut(TcBaseObj):
    """
    'IDSM11SetSyncOptionsOut' structure provides failure code info per object.
    
    :var failureCodes: List for failure code for each input object.
    """
    failureCodes: List[int] = ()


@dataclass
class IDSM11SetSyncOptionsRes(TcBaseObj):
    """
    'IDSM11SetSyncOptionsRes' structure provides information returned after setting sync options and ServiceData.
    
    :var out: Object which has failure info if any.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    out: IDSM11SetSyncOptionsOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11StartAskInfoIn(TcBaseObj):
    """
    'IDSM11StartAskInfoIn' structure contains Integrated Distributed Services Manager (IDSM) client info and other
    information required to start getting schema info.
    
    
    :var clientInfo: Object which has requesting client info.
    :var infoType: Info type flag as IDSM_schema_info to get type-class information which is required to be fetched
    from remote site.
    """
    clientInfo: IDSM11ClientInfo = None
    infoType: int = 0


@dataclass
class IDSM11StartAskInfoOut(TcBaseObj):
    """
    'IDSM11StartAskInfoOut' structure provides staging directory information.
    
    :var infoFiles: List which has name of the file which has to be pulled by client during file transfer.
    
    :var infoStagingDir: List which has name of the file which has to be pulled by client during file transfer.
    """
    infoFiles: List[str] = ()
    infoStagingDir: str = ''


@dataclass
class IDSM11StartAskInfoRes(TcBaseObj):
    """
    'IDSM11StartAskInfoRes' structure provides information required to start importing schema files and ServiceData.
    
    
    :var out: Object which has staging dierctory info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    out: IDSM11StartAskInfoOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11StartExportIn(TcBaseObj):
    """
    'IDSM11StartExportIn' structure contains Integrated Distributed Services Manager (IDSM) client info and other
    information required for export.
    
    
    :var clientInfo: Object which has requesting client info.
    :var exportObjects: List of tag string of objects to be exported.
    :var excludeObjects: List of tag string of objects to be excluded during export.
    
    :var includeObjects: List of tag string of objects to be included during export.
    
    :var reason: User input to explain, why the remote import of business object required. Its not a mandatory input
    and user can pass empty string.
    
    :var exportOptions: List of 'IdsmIeOpt' structure object which has IDSM Import and Export options.
    
    :var compressFlg: Compression flag to check if Compression is active.
    :var compressType: Type of compression read  from IDSM_Compression_Type site level preference, its default value of
      InfoZip .
    
    :var checkClientAfterNWsos: After no. of workspace objects, check for client, used for polling trigger.
    """
    clientInfo: IDSM11ClientInfo = None
    exportObjects: List[str] = ()
    excludeObjects: List[str] = ()
    includeObjects: List[str] = ()
    reason: str = ''
    exportOptions: List[IdsmIeOpt] = ()
    compressFlg: int = 0
    compressType: str = ''
    checkClientAfterNWsos: int = 0


@dataclass
class IDSM11StartExportItemIdListIn(TcBaseObj):
    """
    'IDSM11StartExportItemIdListIn' structure contains Integrated Distributed Services Manager (IDSM) client info and
    other information required to start export itemids list.
    
    
    :var clientInfo: Object which has requesting client info.
    :var queryStrings: List of query strings for querying itemids.
    :var compressFlg: Compression flag to check if Compression is active.
    :var compressType: Type of compression read  from IDSM_Compression_Type site level preference, its default value of
      InfoZip .   
    """
    clientInfo: IDSM11ClientInfo = None
    queryStrings: List[str] = ()
    compressFlg: int = 0
    compressType: str = ''


@dataclass
class IDSM11StartExportItemIdListOut(TcBaseObj):
    """
    Return result of calling IDSM11StartExportItemIdList.
    
    :var exportFiles: exportFiles
    :var exportStagingDir: exportStagingDir
    :var compressPerformedFlg: compressPerformedFlg
    """
    exportFiles: List[str] = ()
    exportStagingDir: str = ''
    compressPerformedFlg: int = 0


@dataclass
class IDSM11StartExportItemIdListRes(TcBaseObj):
    """
    Return result of calling IDSM11StartExportItemIdList.
    
    :var out: out
    :var serviceData: serviceData
    :var serverCorrelationId: serverCorrelationId
    :var userDataIp: userDataIp
    """
    out: IDSM11StartExportItemIdListOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11StartExportOut(TcBaseObj):
    """
    'IDSM11StartExportOut' structure contains information about Multi-site staging directory and compression flag.
    
    
    :var exportFiles: List of export files which has exported objects info created in export staging directory.
    
    :var exportStagingDir: Export staging directory path in which exportFiles files are pushed to and read from this
    directory.
    
    :var failures: List of 'IdsmIeFailures' structure object which has IDSM failure information.
    
    :var compressPerformedFlg: Compression flag to check whether exportFiles are compressed or not. IF compression is
    done set the correct flag for decompressing later in the flow.
    """
    exportFiles: List[str] = ()
    exportStagingDir: str = ''
    failures: List[IdsmIeFailures] = ()
    compressPerformedFlg: int = 0


@dataclass
class IDSM11StartExportRes(TcBaseObj):
    """
    'IDSM11StartExportRes' structure provides staging directory information for starting import  and 'ServiceData'.
    
    
    :var out: Object which has staging directory info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    out: IDSM11StartExportOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11StartImportIn(TcBaseObj):
    """
    'IDSM11StartImportIn' structure contains Integrated Distributed Services Manager (IDSM) client info and required
    POM transmit file  Details, compression flag to start export.
    
    
    :var clientInfo: Object having which has requesting client info.
    :var xmitFname: Path of the multisite transmit file of exporting site copied to file store.
    
    :var compressFlg: Compression flag to check if Compression is active for input files.
    
    :var compressType: Type of compression read  from IDSM_Compression_Type site level preference, its default value of
      InfoZip .
    """
    clientInfo: IDSM11ClientInfo = None
    xmitFname: str = ''
    compressFlg: int = 0
    compressType: str = ''


@dataclass
class IDSM11StartImportOut(TcBaseObj):
    """
    'IDSM11StartImportOut' structure contains information about Multi-site staging directory and             
    compression flag.
    
    
    :var importStagingDir: Server/importing side staging directory path in which exported objects files are  being
    transferred on the server.
    
    :var sendXmitFile: TRUE/FALSE, flag for whether to send POM transmit file from server.
    
    :var compressSupportedFlg: Compression flag to check if Compression is active on server/importing  site or not.
    """
    importStagingDir: str = ''
    sendXmitFile: bool = False
    compressSupportedFlg: int = 0


@dataclass
class IDSM11StartImportRes(TcBaseObj):
    """
    'IDSM11StartImportRes' structure provides staging directory information for starting export and  Servicedata.
    
    
    :var out: Object which has staging directory info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    out: IDSM11StartImportOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11StartSendObjectsIn(TcBaseObj):
    """
    'IDSM11StartSendObjectsIn' Integrated Distributed Services Manager (IDSM) client information and compression
    details.
    
    
    :var clientInfo: Object which has requesting client info.
    :var compressFlg: Compression flag to check if Compression is active or not.
    :var compressType: Type of compression read  from IDSM_Compression_Type site level preference, its default value of
      InfoZip .
    """
    clientInfo: IDSM11ClientInfo = None
    compressFlg: int = 0
    compressType: str = ''


@dataclass
class IDSM11StartSendObjectsOut(TcBaseObj):
    """
    'IDSM11StartSendObjectsOut' structure contains server side staging directory and compression flag.
    
    :var serverStagingDir: Server/importing side staging directory path in which object XML files are  being
    transferred on the server.
    
    :var compressSupportedFlg: Compression flag to check if Compression is active on server/importing  site or not.
    """
    serverStagingDir: str = ''
    compressSupportedFlg: int = 0


@dataclass
class IDSM11StartSendObjectsRes(TcBaseObj):
    """
    'IDSM11StartSendObjectsRes' structure contains information required to start the export and ServiceData.
    
    :var out: Object which has staging directory info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, it is added for future use.
    """
    out: IDSM11StartSendObjectsOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11VerifyObjectsIn(TcBaseObj):
    """
    'IDSM11VerifyObjectsIn' structure holds information required to verify input object and Integrated Distributed
    Services Manager (IDSM) client info.
    
    :var clientInfo: Object which has requesting client info.
    :var objectsToVerify: List of object tag string  to be verified in the database.
    """
    clientInfo: IDSM11ClientInfo = None
    objectsToVerify: List[str] = ()


@dataclass
class IDSM11VerifyObjectsOut(TcBaseObj):
    """
    'IDSM11VerifyObjectsOut' structure contains object verification status and failure code if any.
    
    :var verdicts:  List of verdicts after verification of input objects. Below are the valid values of verdict        
       
    -                  0 = does not exist
    -                  1 = exists
    -                  2 = exists as a readonly copy
    -                  3 = exists as a stub
    
    
    :var failureCodes: List of failure codes if any for each input object.
    """
    verdicts: List[int] = ()
    failureCodes: List[int] = ()


@dataclass
class IDSM11VerifyObjectsRes(TcBaseObj):
    """
    'IDSM11VerifyObjectsRes' structure contains object verification information retrieved from IDSM server and
    'ServiceData'.
    
    :var out: Object contains input objects verification status.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    out: IDSM11VerifyObjectsOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11VersionCheckIn(TcBaseObj):
    """
    - 'IDSM11VersionCheckIn' structure holds information required to get the IDSM server version.
    
    
    
    :var clientInfo: Object which has requesting client info.
    :var clientVersion: Requesting client version.
    """
    clientInfo: IDSM11ClientInfo = None
    clientVersion: int = 0


@dataclass
class IDSM11VersionCheckOut(TcBaseObj):
    """
    'IDSM11VersionCheckOut' structure holds the IDSM server version information.
    
    :var serverVersion: IDSM server version.
    :var clientRejected: Client rejected status if IDSM rejects client for some reason.
    """
    serverVersion: int = 0
    clientRejected: int = 0


@dataclass
class IDSM11VersionCheckRes(TcBaseObj):
    """
    'IDSM11VersionCheckRes' structure holds the IDSM version information and ServiceData.
    
    :var out: Object contains version info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    out: IDSM11VersionCheckOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''


@dataclass
class IDSM11XferInfoFileIn(TcBaseObj):
    """
    'IDSM11XferInfoFileIn' structure holds the information required to transfer files to remote site and Integrated
    Distributed Services Manager (IDSM) client info.
    
    :var clientInfo: Object which has requesting client info.
    :var infoType: Info type flag as IDSM_schema_info to get type-class information which is required to be fetched
    from remote site.
    
    :var infoStagingDir: Server side staging directory path received in first call.
    :var infoFile: Info file which needs to be pulled in suring transfer.
    :var startingBlock: Transfer happens block by block, so index for starting block.
    """
    clientInfo: IDSM11ClientInfo = None
    infoType: int = 0
    infoStagingDir: str = ''
    infoFile: str = ''
    startingBlock: int = 0


@dataclass
class IDSM11XferInfoFileOut(TcBaseObj):
    """
    'IDSM11XferInfoFileOut' structure holds the file data information which is transferred to remote site.
    
    :var fileData: Actual file data which in the form of bytes.
    :var fileDataSize: File data size which is pulled from server.
    :var transferComplete: Flag to indicate whether all file transfer is complete or not.
    :var moreFiles: It transfers one file at a time, so flag to check whether there are more files to be pulled in.
    """
    fileData: List[int] = ()
    fileDataSize: int = 0
    transferComplete: bool = False
    moreFiles: bool = False


@dataclass
class IDSM11XferInfoFileRes(TcBaseObj):
    """
    'IDSM11XferInfoFileRes' structure holds the file transfer output information.
    
    :var out: Object contains file transfer info.
    :var serviceData: Any failure is returned in the ServiceData list of partial errors with input object mapped to
    error message.
    
    :var serverCorrelationId: Correlation id of the IDSM server.
    :var userDataIp: Currently this attribute not used, currently it is added for future use.
    """
    out: IDSM11XferInfoFileOut = None
    serviceData: ServiceData = None
    serverCorrelationId: str = ''
    userDataIp: str = ''
