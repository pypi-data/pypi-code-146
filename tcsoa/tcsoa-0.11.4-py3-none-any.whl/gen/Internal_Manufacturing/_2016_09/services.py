from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2016_09.StructureManagement import LinkStructuresResponse, DesignPartAlignmentInput, DesignPartAlignmentResponse, AsyncCreateCPCInputInfo, ObjectAlignmentInput, LinkStructuresInput, CreateDesignPartAlignmentInput, CompletenessCheckPartStructureResp
from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject
from tcsoa.gen.Internal.Manufacturing._2016_09.IPAManagement import DynamicIPAInputInfo, SaveDynamicIPALinesResponse, DynamicIPALinesResponse, CleanDynamicIPALinesResponse
from tcsoa.gen.Internal.Manufacturing._2016_09.DataManagement import CreateBOEfromPlantBOPResponse, SynchronizeBOPAndBOEInputInfo, SynchronizePlantBOPAndBOEResponse, LinkPlantBOPtoBOEResponse, LinkBOPtoBOEObjectInfo
from tcsoa.gen.Internal.Manufacturing._2016_09.ResourceManagement import GetVendorCatalogInfo3Response
from typing import List
from tcsoa.gen.Internal.Manufacturing._2016_09.StructureSearch import SearchBOEInputInfo, SearchBOEResponse
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class IPAManagementService(TcService):

    @classmethod
    def cleanDynamicIPALines(cls, inputLines: List[DynamicIPAInputInfo]) -> CleanDynamicIPALinesResponse:
        """
        The operation cleans DIPA(Mfg0BvrDynamicIPA) lines generated using SOA createDynamicIPALines for the input BOP
        lines.
        
        Use cases:
        Use case 1 : Recursively clean DIPA(Mfg0BvrDynamicIPA) nodes on top line of process structure
        
        You can invoke this operation on top line of process structure. This operation  cleans  all the
        DIPA(Mfg0BvrDynamicIPA)nodes uder all the sub-processes.  
        
        Use case 2 : Recursively clean DIPA(Mfg0BvrDynamicIPA) nodes on intermediate processes in process structure.
        
        You can invoke this operation  on specific processeses.
        This operation cleans DIPA(Mfg0BvrDynamicIPA) node for input processes and each of its sub-processes.
                   
        Use case 3: Clean DIPA nodes on one or more intermediate processes of process structure
        
        You can invoke this operation on one or more processes of process structure.This operation cleans
        DIPA(Mfg0BvrDynamicIPA) node for the input processes only.
        """
        return cls.execute_soa_method(
            method_name='cleanDynamicIPALines',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='IPAManagement',
            params={'inputLines': inputLines},
            response_cls=CleanDynamicIPALinesResponse,
        )

    @classmethod
    def saveContentOfDynamicIPALines(cls, inputDIPALines: List[BusinessObject]) -> SaveDynamicIPALinesResponse:
        """
        This operation persists the content of the input dynamic IPA (Mfg0BvrDynamicIPA) nodes to the database.
        
        Use cases:
        Use case 1 : Save one or more Dynamic IPA(Mfg0BvrDynamicIPA)
        You can invoke this operation for one or more dynamic IPA nodes below different processes.
        saveContentOfDynamicIPALines saves the children of DIPA nodes into the database and also sets the 'Is
        Persistent'(fnd0IsPersistent) property to true.
        """
        return cls.execute_soa_method(
            method_name='saveContentOfDynamicIPALines',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='IPAManagement',
            params={'inputDIPALines': inputDIPALines},
            response_cls=SaveDynamicIPALinesResponse,
        )

    @classmethod
    def updateDynamicIPALines(cls, inputLines: List[DynamicIPAInputInfo]) -> DynamicIPALinesResponse:
        """
        This operation updates all the DIPA (Mfg0BvrDynamicIPA) nodes for input processes; and for all its
        sub-processes in a hierachy, if the recursive flag is true.
        
        Use cases:
        Use case 1 : Update on top line of the process structure
         
        You can invoke this operation on top line of the process structure. This operation updates all the     
        DIPA(Mfg0BvrDynamicIPA) nodes under all the sub-processes. Recursive flag is ignored for the top line.
        
        Use case 2 : Update on one or more DIPA (Mfg0BvrDynamicIPA) nodes
        
        You can invoke this operation on specific DIPA (Mfg0BvrDynamicIPA) nodes. This operation updates only the
        DIPA(Mfg0BvrDynamicIPA) nodes provided as input.
        
        Use case 3 : Update recursive on one or more intermediate processes in the process structure
        
        You can invoke this operation on one or more processes in the process structure. This operation                
                updates DIPA(Mfg0BvrDynamicIPA)  nodes for input processes and each of its sub-process only if the
        recursive flag is true.
        """
        return cls.execute_soa_method(
            method_name='updateDynamicIPALines',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='IPAManagement',
            params={'inputLines': inputLines},
            response_cls=DynamicIPALinesResponse,
        )

    @classmethod
    def createDynamicIPALines(cls, inputLines: List[DynamicIPAInputInfo]) -> DynamicIPALinesResponse:
        """
        This operation creates the DIPA (Mfg0BvrDynamicIPA) containing the incoming parts as a flat list and adds it to
        the process structure. If the input process has more than one predecessors, it creates a separate DIPA node for
        each incoming path. If the recursive flag is true, it creates DIPA for every process having predecessors in the
        hierarchy of the input process. The operation considers occurrence types defined in
        'MEDynamicIPAOccurrenceTypes' preference; to determine which occurrence types to aggregate from predecessors in
        the given process structure to generate the DIPA (Mfg0BvrDynamicIPA). The default value for this preference
        will be 'MEConsumed'. 
        These new DIPA (Mfg0BvrDynamicIPA) nodes  are added under the appropriate process with 'MEDynamicWorkpiece'
        occurrence type.
        
        Use cases:
        Use case 1 : Create DIPA(Mfg0BvrDynamicIPA)on one or more processes in process structure.You can invoke this
        operation on one or more processes. If the recursive flag is false, the operation  
        creates DIPA (Mfg0BvrDynamicIPA) nodes only below the input processes with 'MEDynamicWorkpiece'occurrence type. 
        
        Use case 2 : Create Recursive DIPA(Mfg0BvrDynamicIPA) nodes for top line of process structure.You can invoke
        this operation on top line of process structure.It creates DIPA(Mfg0BvrDynamicIPA) nodes for all the sub-
        processes having predecessors.
        
        Use case 3 : Create Recursive DIPA(Mfg0BvrDynamicIPA) for intermediate processes in process sructure.You can
        invoke the operation on onr or more intermediate processes in process structure.This operation creates
        DIPA(Mfg0BvrDynamicIPA)  nodes for input processes and each of its sub-processes having predecessors.
        """
        return cls.execute_soa_method(
            method_name='createDynamicIPALines',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='IPAManagement',
            params={'inputLines': inputLines},
            response_cls=DynamicIPALinesResponse,
        )


class ResourceManagementService(TcService):

    @classmethod
    def getVendorCatalogInfo3(cls, catalogTypeFilter: int) -> GetVendorCatalogInfo3Response:
        """
        The multi-value preference "MRMGTCVendorCatalogRootDir" specifies one or more root directories where vendor
        tool catalogs may be stored on the Teamcenter server machine.
        This operation retrieves additional information about valid vendor catalogs contained in these root
        directories. It scans the given root directories for vendor catalogs of the requested type and returns detailed
        information for each valid catalog. This new operation supports GTC packages in GTC V1 and V2 format.
        """
        return cls.execute_soa_method(
            method_name='getVendorCatalogInfo3',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='ResourceManagement',
            params={'catalogTypeFilter': catalogTypeFilter},
            response_cls=GetVendorCatalogInfo3Response,
        )

    @classmethod
    def extractHolderData(cls, icoIds: List[str]) -> ServiceData:
        """
        This operation extracts tool holder data from Manufacturing Resource Manager resources by using the NX
        Graphicsbuilder functionality.  The NX Graphicsbuilder is called to extract the holder data from the given
        resources.  The resulting holder data is stored in the resources' assembly ICOs.
        """
        return cls.execute_soa_method(
            method_name='extractHolderData',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='ResourceManagement',
            params={'icoIds': icoIds},
            response_cls=ServiceData,
        )


class StructureManagementService(TcService):

    @classmethod
    def linkOrUnlinkStructures(cls, input: List[LinkStructuresInput]) -> LinkStructuresResponse:
        """
        This operation links or unlinks the PSBOMView objects of the  two input structures by the input relation.
        """
        return cls.execute_soa_method(
            method_name='linkOrUnlinkStructures',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=LinkStructuresResponse,
        )

    @classmethod
    def completenessCheckPartStructure(cls, input: List[ObjectAlignmentInput]) -> CompletenessCheckPartStructureResp:
        """
        This operation does a completeness check of the Part structure.  The operation recursively checks all the Part
        objects in the structure for completeness.  Part objects not marked as design required are marked complete.  If
        the Part is marked as design required the following checks are performed:
         
        - Is Part structure connected?
        -     Checks for relation Fnd0PartCadRelation. 
        - Are Part and Design revision aligned?
        -     Checks the Part object's child DesignRevision against the Part object's configured DesignRevision.
        - Is Part occurrence an End Item?
        - Is schema valid?
        - Does Design occurrence thread exist?
        - Does Design occurrence exist?
        - Are Part and Design revision connected properly?
        - Checks for Fnd0PartCadRelation.
        - Is Part BVR precise?
        
        """
        return cls.execute_soa_method(
            method_name='completenessCheckPartStructure',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=CompletenessCheckPartStructureResp,
        )

    @classmethod
    def removeDesignPartAlignment(cls, input: List[ObjectAlignmentInput]) -> DesignPartAlignmentResponse:
        """
        This service operation removes Design and Part objects alignment if it exist.  
        It will be the reversal of the what is done by the createDesignPartAlignment operation as described below:
        - Remove precise BOMViewRevision (BVR) indication on Part (if needed)
        - Remove Design occurrence from Part.
        - Remove relation between Part and Design revisions.
        - Remove End Item designation from Part.
        - Remove Represented By / Represented For relations for Part and Design.
        - Clear bl_abs_occ_id (IDIC) from Part.
        
        """
        return cls.execute_soa_method(
            method_name='removeDesignPartAlignment',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=DesignPartAlignmentResponse,
        )

    @classmethod
    def createAsyncCollabPlanningContext(cls, asyncCpcInput: AsyncCreateCPCInputInfo) -> None:
        """
        This service operation asynchronously creates a Collaboration Planning Context (CPC) with the given input
        structures that are to be cloned and/or referred to, and establishes a relation between input
        MECollaborationContext (CC) object and newly created CPC. CPC is basically a CC object itself, it is a term
        used for Alternative Management. This is asynchronous implementation for the
        Teamcenter::Soa::Manufacturing::_2015_10::StructureManagement createCollabPlanningContext service operation.
        
        Use cases:
        A user can asynchronously create a CPC object in Manufacturing Process Planner (MPP) application using an
        existing opened CC structure. Subsequently a relation Mfg0MEAlternatePlanningRel is created between newly
        created CPC and the original CC.
        Use Case 1: Open a CC structure, select some structures available in the CC and create a CPC asynchronously.
        
        Use Case 2: Open a CC structure, select some of the scopes in that structure and create a CPC asynchronously.
        
        Use Case 3: Open a CC structure, select some structures/scopes, provide whether they need to be referred or
        cloned and provide cloning parameters such as clone suppressed lines, carry-over ICs etc. to create a CPC
        asynchronously.
        """
        return cls.execute_soa_method(
            method_name='createAsyncCollabPlanningContext',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='StructureManagement',
            params={'asyncCpcInput': asyncCpcInput},
            response_cls=None,
        )

    @classmethod
    def verifyDesignPartAlignment(cls, input: List[DesignPartAlignmentInput]) -> DesignPartAlignmentResponse:
        """
        This operation does a series of verification checks against an existing Design and Part object alignment.   It
        returns as partial errors any of the validations that fail.  The validation performed is as follows:
        
        - Part structure is connected
        - Checks for Fnd0PartDesignLink relation
        - Part and Design revision aligned 
        - Checks Part child DesignRevision against Part configured DesignRevision
        - Is Part occurrence End Item?
        - Is schema valid?
        - Does Design occurrence thread exist?
        - Does Design occurrence exist?
        - Part and Design revision connected properly
        - Checks for Fnd0PartCadRelation relation
        - Is Part BOMViewRevision (BVR) precise?
        
        """
        return cls.execute_soa_method(
            method_name='verifyDesignPartAlignment',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=DesignPartAlignmentResponse,
        )

    @classmethod
    def createOrUpdateDesignPartAlignment(cls, input: List[CreateDesignPartAlignmentInput]) -> DesignPartAlignmentResponse:
        """
        This service operation is used to create or update Part and Design object alignments between Design and Part
        structures. It is possible to create two different types of alignments. One type of alignment includes
        assignment of the Design occurrence to the Part occurrence. The other alignment type does not include this
        Design occurrence assignment. The alignment with Design occurrence assignment includes all the steps of the
        other type of alignment with additional steps involving the Design occurrence alignment. The common create
        alignment steps are described here:
        
        Create matching bl_abs_occ_id (IDIC) between Design and Part occurrences.
        Copy BOMLine properties from Design occurrence to Part occurrences.
        The preference EDesignPartAlignProperties describes the properties to copy.
        Create relation of type internal name between objects DesignRevision and PartRevision.
        The PartRevision being primary and DesignRrevision as secondary.
        The Part and Design TC_Is_Represented_By relation is established.
        Part BOMLine property alignment link exist indicator is set true.
        
        Additional steps for create alignment with Design occurrence assignment:
        
        Assign Design occurrence under Part occurrence
        Mark Part BOMViewRevision (BVR) as Precise
        Mark Part occurrence as End Item
        
        
        Additionally, this service operation validates the existing alignment and updates the alignment with the
        current DesignRevision information.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateDesignPartAlignment',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=DesignPartAlignmentResponse,
        )

    @classmethod
    def findRelatedDesignOrPartStructures(cls, input: List[ObjectAlignmentInput]) -> DesignPartAlignmentResponse:
        """
        This operation finds all the Design structures related to the input Part BOMLine or alternatively finds all the
        Part structures related to the input Design BOMLline  and returns a list of structure roots.  The input can be
        any BOMLine in the source Part/Design structure.
        """
        return cls.execute_soa_method(
            method_name='findRelatedDesignOrPartStructures',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=DesignPartAlignmentResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def linkPlantBOPtoBOE(cls, linkBOPtoBOEObjectInfo: List[LinkBOPtoBOEObjectInfo]) -> LinkPlantBOPtoBOEResponse:
        """
        This operation links  the input source i.e. Plant Bill of Process (Plant BOP) and target i.e. Bill of
        Equipement (BOE) lines. Linking creates GRM relation Mfg0MELinkedBOERel between MEAppearancePathNode associated
        with source and target lines.
        If either source or target line is already linked to any of the lines in the target or source structures
        respectively then the current link is removed and a new link is created. But this is not applicable for the top
        lines i.e, Mfg0MEPlantBOP and MEPlant.
        During link, objects are linked based on the preference MEBOPToBOEObjectTypeMap. The preference
        MEBOPToBOEObjectTypeMap holds the information about the mapping between the object types. 
        If a mapping exists between the given source and target type then the types are linked otherwise an error is
        returned in service data.
        """
        return cls.execute_soa_method(
            method_name='linkPlantBOPtoBOE',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='DataManagement',
            params={'linkBOPtoBOEObjectInfo': linkBOPtoBOEObjectInfo},
            response_cls=LinkPlantBOPtoBOEResponse,
        )

    @classmethod
    def synchronizePlantBOPAndBOE(cls, synchronizeBopAndBoeInputInfo: List[SynchronizeBOPAndBOEInputInfo]) -> SynchronizePlantBOPAndBOEResponse:
        """
        This operation synchronizes the input source and target lines. Plant Bill of Process (Plant BOP) lines and Bill
        of Equipement (BOE) lines acts as source or target lines. The decision regarding which lines will act as source
        or target line will be taken by the user. 
        Synchronizing the Plant BOP structure and BOE structure will result in 
        
        1. Creating missing elements in target. The type of the element to be created will be identified by the
        preference MEBOPToBOEObjectTypeMap. MEAppearancePathNode associated with the new elements created in target
        will be linked with the MEAppearancePathNode associated with the source line.
        
        2. Copying of attributes from source line to target line. The attributes that are to be synchronized will be
        identified by the preference MEBOPToBOEObjectTypeMap.
        
        3. If the option for remove obsolete twin is provided then the target lines which do not have
        Mfg0MELinkedBOERel will be removed from the target structure.
        
        Use cases:
        Use case 1: Sync objects from Twin Structure
        This operation synchronizes the linked Plant BOP lines, BOE lines and hierarchy under it by
        1. Copying the attributes values from source to target for already linked lines.
        
        2. Creating an object in target structure for each object in source structure that does not have any connected
        object. 
        
        3. Removing every object in target structure that does not have any connected object in the source structure. 
        (Only if user had asked for it through the removeObsoleteTwin option)
        
        4. If a station or station process is created, linked station will be consumed in the station process.
        """
        return cls.execute_soa_method(
            method_name='synchronizePlantBOPAndBOE',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='DataManagement',
            params={'synchronizeBopAndBoeInputInfo': synchronizeBopAndBoeInputInfo},
            response_cls=SynchronizePlantBOPAndBOEResponse,
        )

    @classmethod
    def createBOEfromPlantBOP(cls, rootBOPLines: List[BOMLine]) -> CreateBOEfromPlantBOPResponse:
        """
        For Manufacturing planning both Bill of Equipment (BOE) and Plant Bill of Process (Plant BOP) are required. BOE
        stations hold location information and contain the equipment required for manufacturing. Plant BOP stations are
        used to define the sequences of the processes and hold information about the parts to be assembled in the
        station. The validation of the manufacturing process usually requires the combination of BOE and Plant BOP.
        This operation will create the Plant structures for the given input Plant BOP structures. The decision to
        create objects will be based on a preference. The preference MEBOPToBOEObjectTypeMap will hold the information
        about the mapped objects types which needs to be created. The new objects created will have same attribute
        values as that of originating object.
        
        Use cases:
        Use case 1: User create Plant structure for the selected Plant Bill of Process (Plant BOP)
        New BOE structure will be ceated for given Plant BOP structure. As part of the structure creation,
        MEAppearancePathNode will also be created for each line in the source (Plant BOP) and target (Plant) structure.
        The MEAppearancePathNode object of Plant BOP line will be connected to MEAppearancePathNode created for object
        in Plant with a GRM Relation Mfg0MELinkedBOERel. Station (MEStation) created in Plant structure (MEPlant) for
        any Station Process (Mfg0MEProcStatn) in Plant BOP (Mfg0MEPlantBOP) will be consumed in Station Process
        (Mfg0MEProcStatn).
        """
        return cls.execute_soa_method(
            method_name='createBOEfromPlantBOP',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='DataManagement',
            params={'rootBOPLines': rootBOPLines},
            response_cls=CreateBOEfromPlantBOPResponse,
        )


class StructureSearchService(TcService):

    @classmethod
    def getBOEForPlantBOPScope(cls, searchInput: SearchBOEInputInfo) -> SearchBOEResponse:
        """
        This operation searches the input Plant BOPLines for the Bill of Equipment ( BOEs) based on the search criteria
        and returns a list of all the matched BOEs.
        """
        return cls.execute_soa_method(
            method_name='getBOEForPlantBOPScope',
            library='Internal-Manufacturing',
            service_date='2016_09',
            service_name='StructureSearch',
            params={'searchInput': searchInput},
            response_cls=SearchBOEResponse,
        )
