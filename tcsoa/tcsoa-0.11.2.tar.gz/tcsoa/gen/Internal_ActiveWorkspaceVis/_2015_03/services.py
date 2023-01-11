from __future__ import annotations

from tcsoa.gen.Internal.ActiveWorkspaceVis._2015_03.MassiveModelVisualization import GetIndexedProductsResponse, OccsGroupedByPropertyResponse, ProductAndConfigInfoInput, GetProductStructureIdResponse, UpdateCollectionInput, ProductStructureIdInput, GetStructureFilesResponse, GroupOccsByPropertyInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class MassiveModelVisualizationService(TcService):

    @classmethod
    def getIndexedProducts(cls) -> GetIndexedProductsResponse:
        """
        This operation retrieves the information about the product and configurations whose product structure
        information is indexed. The product and configuration information are returned only for products which have
        been enabled for massive model visualization(MMV).
        
        Use cases:
        The Quicksilver Data server(QDS) is deployed on a LAN closer to the visualization client. The QDS serves the
        product structure information to visualization clients connecting to it. The QDS is configured to periodically
        communicate to the Tcserver and retrieve the indexed product structure information.
        1.    QDS boots and invokes getIndexedProducts and gets the indexed products.
        2.     Invokes getStructureFiles operation on each of the indexed product to get the full product structure
        information represented in a binary file(*.mmp).
        3.    Periodically invokes getStructureFiles operation with previous delta identifier token to retrieve the
        changed product structure information.
        """
        return cls.execute_soa_method(
            method_name='getIndexedProducts',
            library='Internal-ActiveWorkspaceVis',
            service_date='2015_03',
            service_name='MassiveModelVisualization',
            params={},
            response_cls=GetIndexedProductsResponse,
        )

    @classmethod
    def getStructureFiles(cls, productAndConfigInfoInput: List[ProductAndConfigInfoInput]) -> GetStructureFilesResponse:
        """
        This operation retrieves the full or delta product structure information for the given product and
        configuration. The ticket to the file(s) that contain the  product structure information is returned via this
        operation. 
        When this operation is invoked by the client to get the full product structure file, the response may contain a
        single complete product structure file or a single complete product structure file and a set of delta product
        structure files. In case a complete and a set of files containing delta changes are sent then the receiving
        client has to merge the delta files into the complete structure file.
        When this operation is invoked by the client to get the delta product structure, the response may contain a set
        of delta product structure files or a single complete product structure file and a set of delta product
        structure files.  In case where only a set of delta files are returned, the client need to merge those file
        with its available complete structure file. When a single complete product structure file and a set of delta
        product structure files are returned, then this means that the delta token identifier could not be identified
        on the server and hence a complete product structure information has been returned.
        The response also contains a delta identifier token. This delta identifier token has to be passed during the
        next call to  getStructureFiles operation in case the client needs the delta files since the previous call to 
        getStructureFiles operation.
        
        
        Use cases:
        The Quicksilver Data server(QDS) is deployed on a LAN closer to the visualization client. The QDS acts as a
        product structure server for the visualization clients. The QDS is configured to periodically communicate to
        the Tcserver and retrieve the indexed product structure information.
        1.    QDS boots and invokes getIndexedProducts  and gets the products that are indexed.
        2.     Invokes getStructureFiles operation on each of the indexed product to get the full product structure 
        information represented in a binary file(*.mmp).
        3.    Since the product structure changes are continuously tracked and product structure file produced, the
        response would contain a complete product structure file along with a set of delta product structure files that
        were generated since the complete product structure file was produced.
        4.    If the product structure information is returned as a complete file and a set of delta files then the
        client merges the delta file into the complete structure to get the current complete product structure.
        5.    The QDS invokes getStructureFiles periodically to get the next delta that represents the product
        structure changes.
        6.    If only delta product structure file is returned then those files are merged with the complete product
        structure file that the client already has.
        """
        return cls.execute_soa_method(
            method_name='getStructureFiles',
            library='Internal-ActiveWorkspaceVis',
            service_date='2015_03',
            service_name='MassiveModelVisualization',
            params={'productAndConfigInfoInput': productAndConfigInfoInput},
            response_cls=GetStructureFilesResponse,
        )

    @classmethod
    def getStructureIdFromRecipe(cls, productStructureIdInput: List[ProductStructureIdInput]) -> GetProductStructureIdResponse:
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
        working" with "vrule2", it contacts the QDS server with this information. The QDS in turn  invokes this
        operation with the given information to determine the id of the mmp file, in this case it would return
        "UidOfBomIndexAdminData1" as id in its response.
        
        
        Use cases:
        The Quicksilver Data server(QDS) is deployed on a LAN closer to the visualization client. The QDS acts as a
        product structure server for the visualization clients. The QDS is configured to periodically communicate to
        the Tcserver and retrieve the indexed product structure information.
        1.    QDS boots and invokes getIndexedProducts  and gets the products that are indexed.
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
        client for it to apply  massive model visualization algorithm.
        """
        return cls.execute_soa_method(
            method_name='getStructureIdFromRecipe',
            library='Internal-ActiveWorkspaceVis',
            service_date='2015_03',
            service_name='MassiveModelVisualization',
            params={'productStructureIdInput': productStructureIdInput},
            response_cls=GetProductStructureIdResponse,
        )

    @classmethod
    def groupOccurrencesByProperties(cls, groupOccsByPropertyInputList: List[GroupOccsByPropertyInput]) -> OccsGroupedByPropertyResponse:
        """
        This operation classifies Awb0Element objects which are identified by their PFUID (An identifier used to
        identify a product structure line in ACE index BOM) into groups. In the list of 'GroupOccsByPropertyInput',
        each input contains an internal property name, list of property values in 'PropertyGroupingValue' identifying
        the grouping criteria and a list of PFUIDs that need to be organized into groups. Each 'PropertyGroupingValue'
        input contains a start and an end value. The end value is to be used for range values if populated. 
        
        The response contains the PFUIDs that were grouped based on the property name and values. PFUIDs that could not
        be grouped as per input property names and values are retuned back in a separate list.
        
        
        Use cases:
        Use case1: 
        Coloring the part assembly displayed in Active Workspace by visualization server when rendering in
        non-MMV(Massive Model Visualization) mode .
        1.    In the Active Workspace client, a user wants to visualize an assembly.
        2.    The color of the parts displayed in the visualization view has to match the colors on the bar chart for
        the objects in the search results.
        3.    The AW visualization client invokes the visualization server with the criteria that contain the color
        code to group the rendered objects based on the property name and property values.
        4.    The AW visualization server initially renders all the current objects it has in its view in a see through
        mode
        5.    The AW visualization server now invokes 'Teamcenter::Soa::Query::_2014_11::Finder::
        groupObjectsByProperties' and passes the property name, property values and the objects that it is currently
        displaying.
        6.    AW visualization server on receiving the objects grouped based on property names and values, renders the
        parts based on the colors associated to the group.
        
        Use case2: 
        Coloring the part assembly displayed in Active Workspace by visualization server when rendering in MMV(Massive
        Model Visualization) mode .
        1.    In the Active Workspace client, a user wants to visualize an assembly.
        2.    The color of the parts displayed in the visualization view has to match the colors on the bar chart for
        the objects in the search results.
        3.    The AW visualization client invokes the visualization server with the criteria that contain the color
        code to group the rendered objects based on the property name and property values.
        4.    The AW visualization server initially renders all the current objects it has in its view in a see through
        mode
        5.    The AW visualization server since it is rendering in MMV mode does not have Business Objects instead has
        the PFUID of the parts. The AW visualization server now invokes 'groupOccurrencesByProperties' and passes the
        property name, property values, and the PFUID of the objects that it is currently displaying.
        6.    AW visualization server on receiving the PFUID grouped based on property names and values, renders the
        parts based on the colors associated to the group.
        """
        return cls.execute_soa_method(
            method_name='groupOccurrencesByProperties',
            library='Internal-ActiveWorkspaceVis',
            service_date='2015_03',
            service_name='MassiveModelVisualization',
            params={'groupOccsByPropertyInputList': groupOccsByPropertyInputList},
            response_cls=OccsGroupedByPropertyResponse,
        )

    @classmethod
    def updateDeltaCollection(cls, updateCollectionInput: List[UpdateCollectionInput]) -> ServiceData:
        """
        This operation updates the Awv0MMPDeltaCollection dataset with the file that contains product structure changes.
        
        Use cases:
        The system administrator sets up the runTcFTSIndexer to run periodically.
        1.    The TcFtsIndexer finds all the Awb0BOMIndexAdminData that contains product and configuration whose
        product structure  need to be indexed.
        2.     Invokes processBomIndex operation which returns the product structure information in TcXML format.
        3.    TcXML file is transformed into SOLR schema and uploaded into SOLR.
        4.    TcXML file is also transformed into MMP format using the tcxml2mmp converter utility.
        5.    An upload ticket is obtained for the MMP file using the getRegularFileTicketsForUpload operation.
        6.    The file is uploaded to Teamcenter volume using FCC.
        7.    The uploaded file is committed to Teamcenter as ImanFile object using commitRegularFiles operation.
        8.    The ImanFile object is now associated to Awv0MMPDeltaCollection using updateDeltaCollection.
        """
        return cls.execute_soa_method(
            method_name='updateDeltaCollection',
            library='Internal-ActiveWorkspaceVis',
            service_date='2015_03',
            service_name='MassiveModelVisualization',
            params={'updateCollectionInput': updateCollectionInput},
            response_cls=ServiceData,
        )
