from __future__ import annotations

from tcsoa.gen.Internal.ActiveWorkspaceVis._2018_05.MassiveModelVisualization import GetProductStructureIdResponse2
from typing import List
from tcsoa.gen.Internal.ActiveWorkspaceVis._2015_03.MassiveModelVisualization import ProductStructureIdInput
from tcsoa.base import TcService


class MassiveModelVisualizationService(TcService):

    @classmethod
    def getStructureIdFromRecipe2(cls, productStructureIdInput: List[ProductStructureIdInput]) -> GetProductStructureIdResponse2:
        """
        This operation retrieves the id that is used to identify a product structure information. The id is a unique
        identifier which gets written into the MMP file as the product Id. The Quicksilver Data server(QDS) maintains
        the product structure information for different product and configurations. Now when the Visualization client
        sends a request to QDS asking information about a product and configuration, the QDS invokes this operation to
        determine the id of the structure which contain information about the requested product and configuration.
        
        Say for example the QDS may have a product structure information with id "UidOfBomIndexAdminData1" that
        contains product structure information of product1 for RevisionRule as "Latest Working" and VariantRule
        "vrule1", "vrule2", "vrule3" and a product structure information with id "UidOfBomIndexAdminData2" that
        contains product structure information of product2 for RevisionRule as "Latest Released" and VariantRule
        "vrule1", "vrule2", "vrule3" and. Now if the Visualization client wants to display the product1 for "Latest
        working" with "vrule2", it contacts the QDS server with this information. The QDS in turn invokes this
        operation with the given information to determine the id of the mmp file, in this case it would return
        "UidOfBomIndexAdminData1" as id in its response.
        
        Use cases:
        The Quicksilver Data server(QDS) is deployed on a LAN closer to the visualization client. The QDS acts as a
        product structure server for the visualization clients. The QDS is configured to periodically communicate to
        the Tcserver and retrieve the indexed product structure information.
        1.    QDS boots and invokes getIndexedProducts and gets the products that are indexed.
        2.     Invokes getStructureFiles operation on each of the indexed product to get the product structure
        information represented in a binary file(*.mmp).
        3.    If the product structure information is returned as a complete file and a set of delta files then the
        client merges the delta file into the complete structure to get the current complete product structure .
        4.    If only delta product structure file is returned then those files are merged with the complete file that
        the client already has.
        5.    A visualization client requests product structure information for a given product and configuration using
        a recipe object. The recipe object could be Awb0ProductContextInfo or 
        VisStructureContext etc. Now QDS invokes getStructureIdFromRecipe to determine which file contains the
        requested product structure information.
        6.    The spatial structure corresponding to the product structure file is then served to the visualization
        client for it to apply massive model visualization algorithm.
        """
        return cls.execute_soa_method(
            method_name='getStructureIdFromRecipe2',
            library='Internal-ActiveWorkspaceVis',
            service_date='2018_05',
            service_name='MassiveModelVisualization',
            params={'productStructureIdInput': productStructureIdInput},
            response_cls=GetProductStructureIdResponse2,
        )
