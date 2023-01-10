from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Internal.GlobalMultiSite._2007_06.ImportExport import DryRunExportResponse, OwningSiteAndObjs, TransferFormula, ImportObjectsResponse, ConfirmExportResponse, CallToRemoteSiteResponse, NamesAndValues, ExportObjectsResponse
from tcsoa.gen.Internal.GlobalMultiSite._2007_06.Synchronizer import SyncResponse, OwnershipChangeReplicaUpdateResponse, StubReplicationMasterUpdateResponse, CheckSyncStateResponse, ReplicaDeletionMasterUpdateResponse, ObjectsByClass
from typing import List
from tcsoa.gen.Internal.GlobalMultiSite._2007_06.Briefcase import PackageBriefcaseContentsInfo, UnpackBriefcaseContentsResponse, PackageBriefcaseContentsResponse
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SynchronizerService(TcService):

    @classmethod
    def checkReplicaSyncState(cls, replicaSite: int, syncType: str, revisionRule: str, inputReplicaGSIdentityList: List[str]) -> CheckSyncStateResponse:
        """
        For all objects, pointed by input GSIdentity, returns up to date or out of date sync state based on object
        modification since the last export. This operation supports only object level synchronization.
        
        Use cases:
        From RAC, when the user selects &#39;Tools&#45;>MultiSite collaboration&#45;> Check replica sync state&#39;,
        this operation gets invoked and status gets displayed. This operation also gets called from TC Enterprise.
        """
        return cls.execute_soa_method(
            method_name='checkReplicaSyncState',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='Synchronizer',
            params={'replicaSite': replicaSite, 'syncType': syncType, 'revisionRule': revisionRule, 'inputReplicaGSIdentityList': inputReplicaGSIdentityList},
            response_cls=CheckSyncStateResponse,
        )

    @classmethod
    def updateMasterObjectsOnReplicaDeletion(cls, replicaSite: int, inputReplicaGSIdentityList: List[str], convertToStub: bool) -> ReplicaDeletionMasterUpdateResponse:
        """
        This is an internal operation which updates ImanExportRecord of deleted object. If replica object(s) are
        converted to stub then export status of ImanExportRecord gets updated to &#39;Covert to stub&#39;. If replica
        gets deleted, export status is updated to &#39;Deleted&#39;.
        
        Use cases:
        This operation gets triggered when replica workspace object gets deleted. For each workspace object, SOAP call
        is made to Global Services which in turn calls updateMasterObjectsOnReplicaDeletion on owning site to update
        ImanExpordRecord status.
        """
        return cls.execute_soa_method(
            method_name='updateMasterObjectsOnReplicaDeletion',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='Synchronizer',
            params={'replicaSite': replicaSite, 'inputReplicaGSIdentityList': inputReplicaGSIdentityList, 'convertToStub': convertToStub},
            response_cls=ReplicaDeletionMasterUpdateResponse,
        )

    @classmethod
    def updateObjectsOnOwnershipChange(cls, newOwningSite: int, inputReplicaGSIdentityList: List[str]) -> OwnershipChangeReplicaUpdateResponse:
        """
        This operation updates the owning site of replica objects pointed by input GSIdentities in the context of
        ownership change.
        
        Use cases:
        This operation is called by Global Services BPEL process in the context of ownership change. The owning site of
        objects which are in input list is changed to newOwningSite.
        """
        return cls.execute_soa_method(
            method_name='updateObjectsOnOwnershipChange',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='Synchronizer',
            params={'newOwningSite': newOwningSite, 'inputReplicaGSIdentityList': inputReplicaGSIdentityList},
            response_cls=OwnershipChangeReplicaUpdateResponse,
        )

    @classmethod
    def createExportRecordOnStubReplication(cls, replicaSite: int, transferFormula: str, transactionID: str, inputReplicaGSIdentityList: List[str]) -> StubReplicationMasterUpdateResponse:
        """
        Creates export records for all objects pointed by input GSIdentities on the master site in response to the stub
        object creation on replica site. This is an internal operation that is not exposed to the customers.
        
        Use cases:
        This operation is not in use.
        """
        return cls.execute_soa_method(
            method_name='createExportRecordOnStubReplication',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='Synchronizer',
            params={'replicaSite': replicaSite, 'transferFormula': transferFormula, 'transactionID': transactionID, 'inputReplicaGSIdentityList': inputReplicaGSIdentityList},
            response_cls=StubReplicationMasterUpdateResponse,
        )

    @classmethod
    def getCandidatesToSynchronizeForListOfClasses(cls, targetSite: int, classList: List[str]) -> SyncResponse:
        """
        This is an internal operation which returns a list of candidates that need to be synchronized based on input
        class list and target site.
        
        Use cases:
        
        """
        return cls.execute_soa_method(
            method_name='getCandidatesToSynchronizeForListOfClasses',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='Synchronizer',
            params={'targetSite': targetSite, 'classList': classList},
            response_cls=SyncResponse,
        )

    @classmethod
    def getCandidatesToSynchronizeForListOfObjects(cls, targetSite: int, objectsListToProcess: List[ObjectsByClass]) -> SyncResponse:
        """
        This is an internal operation which returns a list of candidates that need to be synchronized based on the
        input set of classes (mandatory) or list of objects (optional). Objects that are replicated at target site are
        taken into account.
        
        Use cases:
        
        """
        return cls.execute_soa_method(
            method_name='getCandidatesToSynchronizeForListOfObjects',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='Synchronizer',
            params={'targetSite': targetSite, 'objectsListToProcess': objectsListToProcess},
            response_cls=SyncResponse,
        )


class DataMigrationService(TcService):

    @classmethod
    def getRUO(cls) -> bool:
        """
        Returns the Replica Update Overide (RUO) value if the Global MultiSite (GMS) is in replicabypass mode,
        otherwise a false is returned.
        """
        return cls.execute_soa_method(
            method_name='getRUO',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='DataMigration',
            params={},
            response_cls=bool,
        )

    @classmethod
    def setRUO(cls, key: str, value: bool) -> ServiceData:
        """
        This operation sets a given logical 'value', if the GMS is in replicabypass mode.Gives an error as Mismatch key
        if GMS is not in replicabypass mode.
        """
        return cls.execute_soa_method(
            method_name='setRUO',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='DataMigration',
            params={'key': key, 'value': value},
            response_cls=ServiceData,
        )


class ImportExportService(TcService):

    @classmethod
    def importObjects(cls, masterSite: int, tcGSMessageId: str, fmsTickets: List[str], inputData: TransferFormula, synchronize: bool) -> ImportObjectsResponse:
        """
        Imports a list of objects and its dependents in Teamcenter XML (Tc XML)format from a specified source site
        based on the input transaction id, list of FMS tickets of the input TcXML files to be imported,
        'TransferFormula' and type of transfer(initial or synchronize).After the import, the objects would be owned by
        target site if ownership transfer session option is specified or they would be imported as replica objects
        meaning the ownership of the objects imported lies with the source site.
        
        Use cases:
        This operation is used in conjunction with exportObjects operation. importOperation will be executed at each
        target site after the exportObjects is called by the BPEL engine during both high level(Not so fast) and low
        level (Fast) data transfer. The low level use case is nothing but site consolidation triggered by teamcenter
        utility 'sitcons_replicate_mg'r which replicates the data from a source site to the target site using the TcXML
        low level (Fast transfer) transfer options. To perform fast transfer the session option name value pair has to
        be 
        - name=fastStream
        - value=yes
        
        
        If the session option fastStream is not specified it will be a high level transfer. Both high level and low
        level transfer require Global Services configured between two sites. TcXML format and schema are different in
        case of high level and low level transfer. The easiest way to identify a TcXML is to look for attribute
        format=high_level in case of high level and format=low_level  in case of low_level.
        """
        return cls.execute_soa_method(
            method_name='importObjects',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'masterSite': masterSite, 'tcGSMessageId': tcGSMessageId, 'fmsTickets': fmsTickets, 'inputData': inputData, 'synchronize': synchronize},
            response_cls=ImportObjectsResponse,
        )

    @classmethod
    def confirmExport(cls, targetSite: int, tcGSMessageId: str, fmsTicketOfFailedObjs: str, commit: bool) -> ConfirmExportResponse:
        """
        This operation should be called at the source site during data transfer after the import is done at the target
        site. First export at source site, import at target site and then a confirm export of failed/successful objects
        at source site. When export is done at the source site export records are created. 'confirmExport' will then
        update the export status in Export record of objects back at the source site after import based on the target
        site id, transaction id and the File Management System (FMS) tickets of file with failed objects.The caller is
        responsible to use FMS to transfer data files from one site to another.
        
        Use cases:
        This operation marks the data transfer from source site to target site as complete by reporting the status of
        objects imported at target site back to source site.
        """
        return cls.execute_soa_method(
            method_name='confirmExport',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'targetSite': targetSite, 'tcGSMessageId': tcGSMessageId, 'fmsTicketOfFailedObjs': fmsTicketOfFailedObjs, 'commit': commit},
            response_cls=ConfirmExportResponse,
        )

    @classmethod
    def requestExportToRemoteSites(cls, reason: str, sites: List[BusinessObject], objects: List[BusinessObject], optionSet: BusinessObject, optionNameAndValues: List[NamesAndValues], sessionOptionNamesAndValues: List[NamesAndValues]) -> CallToRemoteSiteResponse:
        """
        This operation exports objects to specified sites using Global Multisite.
        
        Use cases:
        This operation gets invoked from RAC when user does following actions from Navigator or structure manager
        1>    Tools->Export->To Remote Site Via Global Services.
        2>    Tools->Export->To PDX
        3>    Tools->Export->To Briefcase
        """
        return cls.execute_soa_method(
            method_name='requestExportToRemoteSites',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'reason': reason, 'sites': sites, 'objects': objects, 'optionSet': optionSet, 'optionNameAndValues': optionNameAndValues, 'sessionOptionNamesAndValues': sessionOptionNamesAndValues},
            response_cls=CallToRemoteSiteResponse,
        )

    @classmethod
    def requestImportFromRemoteSites(cls, reason: str, owningSitesAndObjs: List[OwningSiteAndObjs], optionSet: BusinessObject, optionNamesAndValues: List[NamesAndValues], sessionOptionNamesAndValues: List[NamesAndValues]) -> CallToRemoteSiteResponse:
        """
        Remote imports objcets to specified sites. E-mail notification would be sent to
        current user if session option for email notification is set to true.
        
        Use cases:
        This operation is not in use.
        """
        return cls.execute_soa_method(
            method_name='requestImportFromRemoteSites',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'reason': reason, 'owningSitesAndObjs': owningSitesAndObjs, 'optionSet': optionSet, 'optionNamesAndValues': optionNamesAndValues, 'sessionOptionNamesAndValues': sessionOptionNamesAndValues},
            response_cls=CallToRemoteSiteResponse,
        )

    @classmethod
    def dryRunExport(cls, targetSites: List[int], expObjList: List[str], tcGSMessageId: str, inputData: TransferFormula) -> DryRunExportResponse:
        """
        Provides information about an export as if the real export was done and generates a report, based on the input
        'TransferFormula' and global services transaction id for a list of objects which have to be exported.
        
        Use cases:
        This will be executed at the source site and is invoked by Business Process Execution Language(BPEL ) engine
        component of Teamcenter GlobalServices.
        """
        return cls.execute_soa_method(
            method_name='dryRunExport',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'targetSites': targetSites, 'expObjList': expObjList, 'tcGSMessageId': tcGSMessageId, 'inputData': inputData},
            response_cls=DryRunExportResponse,
        )

    @classmethod
    def exportObjects(cls, targetSites: List[int], expObjList: List[str], tcGSMessageId: str, inputData: TransferFormula, synchronize: bool) -> ExportObjectsResponse:
        """
        Exports a list of objects and its dependents in Teamcenter XML Tc XMLformat to specified target sites based on
        the input 'TransferFormula' and type of transfer initial or synchronize.The output TcXML file contains elements
        and its attributes which are traversed by applying the Transfer formula on items specified in input list.
        
        Use cases:
        Business Process Execution Language  BPEL  engine calls this operation to perform high level Not so fast and
        low level Fast transfer. This operation is used to do a data transfer from source site to target sites in case
        of high level. This is executed at the source site in both cases. For a low level transfer it is used by
        'Siteconsolidation' utility 'sitcons_replicate_mgr' which replicates the data from a source site to the target
        site using the TcXML low level Fast transfer options.This utility needs TcGS to be running and configured for
        site consolidation. To perform fast transfer the session option name value pair has to be 
        - name=fastStream 
        - value=yes
        
        
        If the session option fastStream is not specified it then it will be a high level transfer.In other words the
        input for both low level and high level are same except for options.
        """
        return cls.execute_soa_method(
            method_name='exportObjects',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='ImportExport',
            params={'targetSites': targetSites, 'expObjList': expObjList, 'tcGSMessageId': tcGSMessageId, 'inputData': inputData, 'synchronize': synchronize},
            response_cls=ExportObjectsResponse,
        )


class BriefcaseService(TcService):

    @classmethod
    def packageBriefcaseContents(cls, packageBriefcaseContentsInfo: PackageBriefcaseContentsInfo) -> PackageBriefcaseContentsResponse:
        """
        This operation packages TC XML file and the associated named reference files to an offline package called
        Briefcase. The input TCXML files may reference Iman files which are FMS tickets in the XML files.
        The Iman files referenced in the TC XML files are downloaded to the transient volume, the source TC XML file is
        updated to convert the FMS tickets to relative paths. A briefcase file is created by packing the TC XML files
        and related files. The briefcase file is attached to a briefcase dataset, and is sent to the mail folder of the
        user. 
        This operation should be used together with ImportExport::exportObjects. The exportObjects operation will
        generate some TC XML files, and those files are the input to this operation.
        
        
        Use cases:
        User performs a briefcase export on some selected objects through Global Services. After TC XML export is
        completed, the server will have the FMS tickets to TC XML files and export log files. Then it will invoke this
        operation to pack the briefcase. When completed, user can check its mail folder and find the briefcase file in
        the attached dataset.
        
        Exceptions:
        >ServiceException    If this operation cannot complete the whole process. The error may be but not limit to, a
        failure to download a file due to FMS issue; failures to create the briefcase file; failures to create the
        dataset; failures to send the mail.
        """
        return cls.execute_soa_method(
            method_name='packageBriefcaseContents',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='Briefcase',
            params={'packageBriefcaseContentsInfo': packageBriefcaseContentsInfo},
            response_cls=PackageBriefcaseContentsResponse,
        )

    @classmethod
    def unpackBriefcaseContents(cls, uidOfBriefcaseTcFile: str) -> UnpackBriefcaseContentsResponse:
        """
        Unpack a specific briefcase file. 
        This operation reads the briefcase file and extracts all the files from briefcase into transient volume;
        updates the TCXML file to convert the relative path of referenced files to FMS tickets; then return the FMS
        tickets of the updated TCXML files. 
        When unpack completed, the TCXML file is ready for import.
        This operation is invoked by the Global services.
        
        
        Use cases:
        User selects a briefcase file in TC server to do briefcase import. The server gets the UID of the briefcase
        file; unpack the briefcase file. After this operation completes, the server will get the TCXML files that are
        ready for TCXML import.
        
        Exceptions:
        >ServiceException    If this operation cannot complete the whole process. The error may be but not limit to, a
        failure to get the briefcase file from UID; failures to get file from ticket or failures to get ticket from
        file due to FMS issue; failures to unpack the briefcase file.
        """
        return cls.execute_soa_method(
            method_name='unpackBriefcaseContents',
            library='Internal-GlobalMultiSite',
            service_date='2007_06',
            service_name='Briefcase',
            params={'uidOfBriefcaseTcFile': uidOfBriefcaseTcFile},
            response_cls=UnpackBriefcaseContentsResponse,
        )
