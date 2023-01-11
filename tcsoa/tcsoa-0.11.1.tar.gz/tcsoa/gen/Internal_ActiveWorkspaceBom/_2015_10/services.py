from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.ActiveWorkspaceBom._2015_10.OccurrenceManagement import OccurrenceSelection
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class OccurrenceManagementService(TcService):

    @classmethod
    def saveSelections(cls, selections: List[OccurrenceSelection]) -> ServiceData:
        """
        This operation is used to save all the occurrences selected by the user in the Active Content Experience module
        of the Active Workspace Client. The selection data is stored in the Awb0BookmarkSubsetData object related to
        the Awb0BookmarkProductData object.
        
        Use cases:
        This service is intended to be called from within the Active Content Experience (ACE) module of the Active
        Workspace Client (AW). The following is an example scenario on how this service could be used.
        - User selects one or more occurrences in the ACE module of AW. 
        - User then clicks on an action command, such as the "Open in Solid Edge". 
        - The Open in Solid Edge command will first invoke this saveSelection() operation to save the selected
        occurrences to Teamcenter. 
        - The Open in Solid Edge command will then launch the Product Context object to the Solid Edge CAD integration. 
        - The Solid Edge CAD integration would then call the createBOMWindowsFromProductContexts() SOA operation to
        create a BOM Window based on the Product Context object launched from AW. 
        - The createBOMWindowsFromProductContexts() operation would return the BOM Window created for the Product
        Context object and the list of BOMLine objects corresponding to the occurrences selected in AW.
        
        """
        return cls.execute_soa_method(
            method_name='saveSelections',
            library='Internal-ActiveWorkspaceBom',
            service_date='2015_10',
            service_name='OccurrenceManagement',
            params={'selections': selections},
            response_cls=ServiceData,
        )
