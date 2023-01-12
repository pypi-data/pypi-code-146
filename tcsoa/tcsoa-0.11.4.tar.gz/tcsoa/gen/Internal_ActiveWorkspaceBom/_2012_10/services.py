from __future__ import annotations

from tcsoa.gen.BusinessObjects import Awb0SavedBookmark
from tcsoa.gen.Internal.ActiveWorkspaceBom._2012_10.OccurrenceManagement import InfoForAddElemResp, InfoForAddToBookmarkResp, InfoForAddElemData, ChildOccurrencesResp, InsertLevelResponse, ChildOccurrencesData, NxtOccsInProdData, NxtChildOccurrencesData, ProductOccurrencesInput, InsertLevelInputData, OccsInProdResp
from tcsoa.gen.Internal.ActiveWorkspaceBom._2012_10.BOMIndexManagement import ProcessBomIndexResponse, CreBOMIndxAdmDataInfo, CreBOMIndxAdmDataResp, ProcessBomIndexInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class BOMIndexManagementService(TcService):

    @classmethod
    def createBOMIndexAdminData(cls, productContexts: List[CreBOMIndxAdmDataInfo]) -> CreBOMIndxAdmDataResp:
        """
        This operation creates Awb0BOMIndexAdminData instances for the given products and configuration rules and/or
        updates existing Awb0BOMIndexAdminData instances with the new list of variant rules. The state of the
        created/updated Awb0BOMIndexAdminData instances is set to' 'ReadyToIndex''; a scheduled process generates the
        index in the background.The product can be an ItemRevision or CollaborativeDesign(CD). The configuration rules
        comprise of a list of RevisionRule(s) with effectivity information and a list of saved SavedVariantRule(s) with
        their owning ItemRevision(s).
        
        Use cases:
        The system administrator sets up the 'runTcFTSIndexer'('TeamcenterFTSIndexer') to run periodically.
        
        A new product has to be indexed for a given configuration.
        - The client invokes 'createBOMIndexAdminData' with the product and the configuration rules that need to
        applied during indexing. New Awb0BOMIndexAdminData instance gets created for the given product and
        configuration.
        - 'runTcFTSIndexer'  invokes 'processBOMIndex'   to generate BOM index. The input for the 'processBOMIndex'  
        is the Awb0BOMIndexAdminData instances whose states are 'ReadyToIndex', 'IndexGenSuccess',
        'IndexExportSuccess', and 'SolrIndexGenSuccess'.
        
        
        
        A existing product that has already been  indexed have to re- indexed for modified configuration.
        
        - The client invokes 'createBOMIndexAdminData' with the product and the configuration rules that need to
        applied during indexing. The existing Awb0BOMIndexAdminData instance gets updated for the given product and
        changed configuration.
        - 'runTcFTSIndexer'  invokes 'processBOMIndex'   to generate BOM index. The input for the 'processBOMIndex'  
        is the Awb0BOMIndexAdminData instances whose states are 'ReadyToIndex', 'IndexGenSuccess',
        'IndexExportSuccess', and 'SolrIndexGenSuccess'.
        
        """
        return cls.execute_soa_method(
            method_name='createBOMIndexAdminData',
            library='Internal-ActiveWorkspaceBom',
            service_date='2012_10',
            service_name='BOMIndexManagement',
            params={'productContexts': productContexts},
            response_cls=CreBOMIndxAdmDataResp,
        )

    @classmethod
    def processBomIndex(cls, input: ProcessBomIndexInfo) -> ProcessBomIndexResponse:
        """
        This operation manages( generates, updates  or deletes ) indices for the given product and configuration.
        Additionally this operation also generates a 'TCXML' file which represents the configured product indices. The
        product and the configuration rules for which the indices are to be generated or deleted is specified through
        the input Awb0BOMIndexAdminData objects.  
        If the given product was already indexed for the given configuration rules, invoking this operation updates(
        deltas) for the  the indices related to modified structures.  
        
        
        Use cases:
        The system administrator sets up the 'runTcFTSIndexer(TeamcenterFTSIndexer)' to run periodically.
        
        Generation and synchronization of Indices for a configured product
        
        Having set up 'runTcFTSIndexer'  to run periodically, the system administrator performs the following sequence
        when a product has to be indexed for a given set of configuration rules and kept upto date with the changes to
        product structure:
        - Create a text file which contains the information about the product and  RevisionRule and or SavedVariantRule
        that must be used for configuration .
        - Execute 'bomindex_admin' utility using '-function=create' option and provide the text file that contains the
        product and the configuration rules.
        - Executing the 'bomindex_admin' utility persists the product and the configuration rules on
        Awb0BOMIndexAdminData instance with a '"ReadyToIndex"' state.
        
        
        
        The runTcFTSIndexer  utility performs the following sequence to index a configured product:
        
        - Invokes processBomIndex  by passing the 'processingOptions' as 'updateTIEAMTables=true'.
        - Finds all the Awb0BOMIndexAdminData instances in the database using the 'findObjectsByClassAndAttributes'
        operation from the 'Finder' service.
        - Invokes 'processBomIndex'  with Awb0BOMIndexAdminData instances whose states are 'ReadyToIndex',
        'IndexGenSuccess', 'IndexExportSuccess', and 'SolrIndexGenSuccess'.
        - 'runTcFTSIndexer'  utility downloads the 'TCXML' file using the transient file tickets returned in the
        response of 'processBomIndex' call. The 'TCXML' file contains the representation of the configured product
        index that was generated.
        - 'runTcFTSIndexer'  uses the 'TCXML' file to update the 'SOLR' database which will be used during context
        search .
        - On successful update of 'SOLR' database the 'runTcFTSIndexer' utility sets the state as 'SolrIndexGenSuccess'
        on the Awb0BOMIndexAdminData instance using the 'setProperties' operation from the 'Core' service.
        
        
        
        Deletion of Indices for a configured product
        
        The system administrator performs the following sequence when the indices of a configured product are to be
        deleted:
        - Create a text file which contains the information about the product, RevisionRule and or SavedVariantRule for
        which the indices were generated .
        - Execute 'bomindex_admin' utility using '-function=delete' option and provide the text file that contains the
        product and the configuration rules.
        - Executing the 'bomindex_admin' utility finds the Awb0BOMIndexAdminData instance corresponding to the product
        and the configuration rules specified in the input file and sets the status on it as 'MarkedForDeletion'.
        
        
        
        The 'runTcFTSIndexer'  utility performs the following sequence to delete the indices of a configured product:
        - Finds all the Awb0BOMIndexAdminData instances in the database using the 'findObjectsByClassAndAttributes'
        operation from the 'Finder' service.
        - Invokes 'processBomIndex'  with Awb0BOMIndexAdminData instances whose states are 'MarkedForDeletion'.
        - 'runTcFTSIndexer'  utility checks the state of the Awb0BOMIndexAdminData instances returned by the
        'processBomIndex' . For all those instances with state 'IndexDelSuccess' the utility deletes the indices in
        'SOLR'.
        - 'runTcFTSIndexer'  now deletes the Awb0BOMIndexAdminData instances whose status is  'SolrIndexDelSuccess' 
        using 'deleteObjects' operation from 'Core' service.
        
        """
        return cls.execute_soa_method(
            method_name='processBomIndex',
            library='Internal-ActiveWorkspaceBom',
            service_date='2012_10',
            service_name='BOMIndexManagement',
            params={'input': input},
            response_cls=ProcessBomIndexResponse,
        )


class OccurrenceManagementService(TcService):

    @classmethod
    def getChildOccurrences(cls, input: List[ChildOccurrencesData]) -> ChildOccurrencesResp:
        """
        This operation retrieves the child occurrences for the set of input parent occurrences. The child occurrences
        may be a the same level or different levels based on input 'firstLevelOnly'.The number of occurrences retuned
        depends on the paging configuration given in input.
        """
        return cls.execute_soa_method(
            method_name='getChildOccurrences',
            library='Internal-ActiveWorkspaceBom',
            service_date='2012_10',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=ChildOccurrencesResp,
        )

    @classmethod
    def getInfoForAddElement(cls, getInfoForElementIn: InfoForAddElemData) -> InfoForAddElemResp:
        """
        This operation retreives information required for creating an Awb0Element under product specified in
        Awb0ProductContextInfo or Awb0Element. The operation also returns allowable type name(s) to search existing
        object through Full Text Search. The preferred type is the parent type if that is allowed.
        """
        return cls.execute_soa_method(
            method_name='getInfoForAddElement',
            library='Internal-ActiveWorkspaceBom',
            service_date='2012_10',
            service_name='OccurrenceManagement',
            params={'getInfoForElementIn': getInfoForElementIn},
            response_cls=InfoForAddElemResp,
        )

    @classmethod
    def getInfoForAddToBookmark(cls) -> InfoForAddToBookmarkResp:
        """
        This operation retreives information required for adding a product to a Awb0SavedBookmark. The operation also
        returns allowable type name(s) to search an existing object through Full Text Search.
        """
        return cls.execute_soa_method(
            method_name='getInfoForAddToBookmark',
            library='Internal-ActiveWorkspaceBom',
            service_date='2012_10',
            service_name='OccurrenceManagement',
            params={},
            response_cls=InfoForAddToBookmarkResp,
        )

    @classmethod
    def getNextChildOccurrences(cls, input: List[NxtChildOccurrencesData]) -> ChildOccurrencesResp:
        """
        This operation gets the next set of child occurrences for given parent occurrence(s).
        """
        return cls.execute_soa_method(
            method_name='getNextChildOccurrences',
            library='Internal-ActiveWorkspaceBom',
            service_date='2012_10',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=ChildOccurrencesResp,
        )

    @classmethod
    def getNextOccurrencesInProduct(cls, inputData: List[NxtOccsInProdData]) -> OccsInProdResp:
        """
        Get the next set of occurrences in the product. This method should called by passing in the cursor object
        returned by a call to 'getOccurrenceInProduct' or a previous call to 'getNextOccurrencesInProduct'.
        """
        return cls.execute_soa_method(
            method_name='getNextOccurrencesInProduct',
            library='Internal-ActiveWorkspaceBom',
            service_date='2012_10',
            service_name='OccurrenceManagement',
            params={'inputData': inputData},
            response_cls=OccsInProdResp,
        )

    @classmethod
    def getOccurrencesInProduct(cls, inputData: List[ProductOccurrencesInput]) -> OccsInProdResp:
        """
        This operation fetches occurrences in a product. The inputs allow providing the configuration and filter
        information that will help idenfity the occurrences to return. The objects attached to the occurrences can be
        returned by specifying the relation types and object types to return. This operation only returns an page of
        occurrences. Call the method 'GetNextOccurrencesInProduct' to load the next set of occurrences in the product.
        """
        return cls.execute_soa_method(
            method_name='getOccurrencesInProduct',
            library='Internal-ActiveWorkspaceBom',
            service_date='2012_10',
            service_name='OccurrenceManagement',
            params={'inputData': inputData},
            response_cls=OccsInProdResp,
        )

    @classmethod
    def insertLevel(cls, input: List[InsertLevelInputData]) -> InsertLevelResponse:
        """
        This operation creates an Awb0Element object for the given Item object and inserts it as a parent of the given
        Awb0Element objects.
        """
        return cls.execute_soa_method(
            method_name='insertLevel',
            library='Internal-ActiveWorkspaceBom',
            service_date='2012_10',
            service_name='OccurrenceManagement',
            params={'input': input},
            response_cls=InsertLevelResponse,
        )

    @classmethod
    def updateSavedBookmark(cls, savedBookmarkObjects: List[Awb0SavedBookmark]) -> ServiceData:
        """
        This operation updates the Awb0SavedBookmark objects based on corresponding Awb0Autobookmark object.
        """
        return cls.execute_soa_method(
            method_name='updateSavedBookmark',
            library='Internal-ActiveWorkspaceBom',
            service_date='2012_10',
            service_name='OccurrenceManagement',
            params={'savedBookmarkObjects': savedBookmarkObjects},
            response_cls=ServiceData,
        )
