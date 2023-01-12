from __future__ import annotations

from tcsoa.gen.Internal.GlobalMultiSite._2010_02.LowlevelOwnershipTransfer import ObjectsForOwnershipTransferResponse
from tcsoa.base import TcService


class LowlevelOwnershipTransferService(TcService):

    @classmethod
    def getObjectsForOwnershipTransfer(cls, tcGSMessageId: str, changeOwnershipToSite: int, dryrun: bool, startDate: str, endDate: str) -> ObjectsForOwnershipTransferResponse:
        """
        This is an internal operation. It generates a report of source objects which were replicated to target site
        (specified in changeOwnershipToSite) between start date and end date using site consolidation tool. Date range
        is valid only for dry run mode. The report has the following format
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
        It is invoked by BPEL process of Global services when user runs sitcons_xfer_owner_mgr utility of site
        consolidation.
        """
        return cls.execute_soa_method(
            method_name='getObjectsForOwnershipTransfer',
            library='Internal-GlobalMultiSite',
            service_date='2010_09',
            service_name='LowlevelOwnershipTransfer',
            params={'tcGSMessageId': tcGSMessageId, 'changeOwnershipToSite': changeOwnershipToSite, 'dryrun': dryrun, 'startDate': startDate, 'endDate': endDate},
            response_cls=ObjectsForOwnershipTransferResponse,
        )
