from __future__ import annotations

from tcsoa.gen.Internal.GlobalMultiSite._2010_02.LowlevelOwnershipTransfer import ObjectsForOwnershipTransferResponse, UpdateOwnershipTransferResponse, TransferOwnershipResponse
from tcsoa.base import TcService


class LowlevelOwnershipTransferService(TcService):

    @classmethod
    def transferOwnership(cls, tcGSMessageId: str, dryrun: bool, isSrcSiteExtinct: bool, fmsTicketOfObjs: str) -> TransferOwnershipResponse:
        """
        This is an internal operation which transfers ownership of objects that are in the input file. This is executed
        at the target site. Ownership is changed for more than one object. It is advisable to run this operation in dry
        run mode first and then perform actual ownership transfer. In dry run mode, actual ownership is not changed but
        validation is performed for the list of input objects.
        
        Output of this operation is a file which has status of ownership change. Format of the file in dry run mode
        with source extinct flag is as follows
        #Dry Run Report
        # TIE transfer data status (low level) 
        # Syslog FileName    :  C:\Temp\tcxml_xfer_ownership10302d08.syslog
        #$SourceSiteID: 100001
        #$TargetSiteID: 100002
        #$DryRun: Yes
        #$SourceExtinct: Yes
        #PUID        IslandAnchorUIDs    Status
        ArD53SsdAABaaA ArD53SsdAABaaA 0
        QLK53SsdAABaaA ArD53SsdAABaaA 0
        
        #$Dry Run With Extinct
        #$Report of objects at target site db that are 
        #$owned by source site and not in consolidation list 
        QLK53SsdAABaBA    Item
        
        Following are the status codes and their interpretation
        0 : Success
        1: Failure [Island is inconsistent]
        2: Object is missing at target site
        3: New object at target site
        
        
        Use cases:
        If getObjectsForOwnershipTransfer operation succeeds, then this operation is invoked by the BPEL process of
        Global Services when user runs sitcons_xfer_owner_mgr utility of site consolidation.
        """
        return cls.execute_soa_method(
            method_name='transferOwnership',
            library='Internal-GlobalMultiSite',
            service_date='2010_02',
            service_name='LowlevelOwnershipTransfer',
            params={'tcGSMessageId': tcGSMessageId, 'dryrun': dryrun, 'isSrcSiteExtinct': isSrcSiteExtinct, 'fmsTicketOfObjs': fmsTicketOfObjs},
            response_cls=TransferOwnershipResponse,
        )

    @classmethod
    def updateOwnershipTransfer(cls, tcGSMessageId: str, changeOwnershipToSite: int, dryrun: bool, isSrcSiteExtinct: bool, fmsTicketOfObjs: str) -> UpdateOwnershipTransferResponse:
        """
        This is an internal operation. The input file has information about the status of failed or successful islands.
        It generates a report which has status of ownership transfer. Report is saved in the database as TEXT dataset.
        In dry run mode, failed islands are marked as inconsistent. If dry run mode is false then function does
        following:
            (1) Updates the ownership transfer status to the accountability table
            (2) Updates the ownership at the source site
        
        
        Use cases:
        This is invoked by the BPEL process of Global Services when user runs sitcons_xfer_owner_mgr utility of site
        consolidation.
        """
        return cls.execute_soa_method(
            method_name='updateOwnershipTransfer',
            library='Internal-GlobalMultiSite',
            service_date='2010_02',
            service_name='LowlevelOwnershipTransfer',
            params={'tcGSMessageId': tcGSMessageId, 'changeOwnershipToSite': changeOwnershipToSite, 'dryrun': dryrun, 'isSrcSiteExtinct': isSrcSiteExtinct, 'fmsTicketOfObjs': fmsTicketOfObjs},
            response_cls=UpdateOwnershipTransferResponse,
        )

    @classmethod
    def getObjectsForOwnershipTransfer(cls, tcGSMessageId: str, changeOwnershipToSite: int, dryrun: bool) -> ObjectsForOwnershipTransferResponse:
        """
        This is an internal operation which collects source objects that are replicated to a target site (specified in
        changeOwnershipToSite) using site consolidation tool and generates a report. This is executed on the exporting
        site. For this operation, the dry run mode does not have much significance. The report has the following format
        #Accountability Data
        # puids for ownership transfer (low level)
        # Syslog-FileName    :  C:\Temp\tcxml_xfer_ownership26585f2e.syslog
        #$DryRun: Yes
        #$SourceSiteID: 100001
        #$TargetSiteID: 100002
        #PUID         IslandAnchorUIDs
        QLK53SsdAABaaA ArD53SsdAABaaA
        QLG53SsdAABaaA ArD53SsdAABaaA
        ArN53SsdAABaaA ArD53SsdAABaaA
        
        
        Use cases:
        It gets invoked by BPEL process of Global services when user runs sitcons_xfer_owner_mgr utility of site
        consolidation.
        """
        return cls.execute_soa_method(
            method_name='getObjectsForOwnershipTransfer',
            library='Internal-GlobalMultiSite',
            service_date='2010_02',
            service_name='LowlevelOwnershipTransfer',
            params={'tcGSMessageId': tcGSMessageId, 'changeOwnershipToSite': changeOwnershipToSite, 'dryrun': dryrun},
            response_cls=ObjectsForOwnershipTransferResponse,
        )
