from __future__ import annotations

from tcsoa.gen.Internal.Visualization._2018_11.StructureManagement import ProductStructureIdInput, GetProductStructureIdResponse
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def getStructureIdFromRecipe(cls, productStructureIdInput: List[ProductStructureIdInput]) -> GetProductStructureIdResponse:
        """
        This operation retrieves the ID that is used to identify aproduct structure from Teamcenter that has been
        indexed and stored in the visualization data server (VDS) for accelerated visualization performance. The ID is
        a unique identifier which gets written into the MMP file (the file used to transport the indexed product
        structure to the VDS) as the product ID when the product is indexed. The Visualization Data server (VDS)
        maintains indexed product structure information for different products and configurations identified by these
        product IDs.
        
        The Visualization client invokes this operation to check if the product and configuration information for  the
        current visualization request matches that for any of the product structures that have been indexed in the VDS.
         If the product and configuration has been indexed in VDS, then this operation returns the product ID to the
        visualization client.  The visualization client uses this information to initiate a session with the VDS which
        allows the visualization client to retrieve the structure information from VDS instead of from Teamcenter.
        
        For example, the VDS may have indexed product structure data with structure ID "UidOfBomIndexAdminData1" for
        product1 with the RevisionRule  "Latest Working" and VariantRule "vrule1", "vrule2", "vrule3".  The VDS may
        also have indexed product structure data with ID "UidOfBomIndexAdminData2" for  product2 with RevisionRule 
        "Latest Released" and VariantRule "vrule1", "vrule2", "vrule3". If the Visualization client wants to display
        product1 with "Latest working" RevisionRule and VariantRule  "vrule2", it invokes this operation, gets the
        product id "UidOfBomIndexAdminData1" and uses this product id to get the structure information from the VDS.
        
        Use cases:
        VDS is deployed on a LAN close to the visualization client. The VDS acts as a product structure server for the
        visualization clients. The VDS is configured to periodically communicate to the Tcserver and retrieve the
        indexed product structure information.
        - VDS boots and invokes getIndexedProducts  and gets the products that are to be indexed.
        - VDS invokes getStructureFiles operation on each of the indexed products to get the product structure
        information represented in a binary file (*.mmp).
        - If the product structure information is returned as a complete file and a set of delta files then VDS merges
        the delta file into the complete structure to get the current complete product structure .
        - If only delta product structure file is returned then those files are merged with the complete product
        structure data the VDS already has.
        - The VDS is now ready to serve product structure to visualization clients.
        - The user selects an object in Teamcenter to be viewed in the visualization client. A recipe object is
        received by the visualization client from Teamcenter via the VVI generation process. This is the process to
        communicate to the viewer what the user has selected.
        - The visualization client invokes the getStructureIdFromRecipe to determine which product structure data in
        VDS contains the requested product structure information by passing the recipe object that encapsulates the
        product to configure and the configuration information. There are numerous of object types supported by the
        visualization client. Currently this service API supports the Awb0ProductContextInfo or VisStructureContext
        types.
        - The Visulalization client initiates a session with  the VDS using the Product ID returned by
        getStructureIdFromRecipe.
        - The VDS servers a spatial hierarchy file and corresponding product structure data for this structure ID  to
        the visualization client to enable  massive model visualization (MMV).
        
        """
        return cls.execute_soa_method(
            method_name='getStructureIdFromRecipe',
            library='Internal-Visualization',
            service_date='2018_11',
            service_name='StructureManagement',
            params={'productStructureIdInput': productStructureIdInput},
            response_cls=GetProductStructureIdResponse,
        )
