from __future__ import annotations

from tcsoa.gen.Manufacturing._2015_10.StructureManagement import CreateCPCResponse, CreateCPCInputInfo
from tcsoa.gen.Manufacturing._2015_10.ImportExport import ImportManufaturingFeaturesResponse, ImportManufaturingFeaturesInput
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def importManufacturingFeatures(cls, input: ImportManufaturingFeaturesInput) -> ImportManufaturingFeaturesResponse:
        """
        This operation imports discrete and continuous manufaturing features (MFGs) from a given PLMXML file into a
        target product structure in Teamcenter. The PLMXML contains the data about the MFGs. The data contains the name
        of the MFGs. Their transform, their parts' connection, and their form attributes. There are two types of
        manufacturing features. Continuous MFG like arcweld ( Mfg0BVRArcWeld) and discrete MFGs like weld point
        (Mfg0BVRWeldPoint) and datum point (Mfg0BVRDatumPoint). For continuous MFGs, the PLMXML also contains the JT
        information.
        
        Use cases:
        none
        """
        return cls.execute_soa_method(
            method_name='importManufacturingFeatures',
            library='Manufacturing',
            service_date='2015_10',
            service_name='ImportExport',
            params={'input': input},
            response_cls=ImportManufaturingFeaturesResponse,
        )


class StructureManagementService(TcService):

    @classmethod
    def createCollabPlanningContext(cls, cpcInput: CreateCPCInputInfo) -> CreateCPCResponse:
        """
        This service operation creates a Collaboration Planning Context (CPC) with the given input  structures that are
        to be cloned and/or referred to, and establishes a relation between input MECollaborationContext (CC) object
        and newly created CPC. 
        CPC is a CC object itself, it is a term used for mix production.
        
        Use cases:
        A user creates a CPC object in Manufacturing Process Planner (MPP) application using an existing opened CC
        structure. Subsequently a relation Mfg0MEAlternatePlanningRel is created between newly created CPC and the
        orginal CC.
        
        Use Case 1: The user opens a CC structure, select some structures available in the CC and creates a CPC.
        
        Use Case 2: A user opens a CC structure, select some of the scopes in that structure and create a CPC.
        
        Use Case 3: A user opens a CC structure, select some structures/scopes, provide whether they need to be
        referred or cloned and provide cloning parameters such as Clone Suppressed Lines, Carry Over ICs etc. to create
        a CPC.
        """
        return cls.execute_soa_method(
            method_name='createCollabPlanningContext',
            library='Manufacturing',
            service_date='2015_10',
            service_name='StructureManagement',
            params={'cpcInput': cpcInput},
            response_cls=CreateCPCResponse,
        )
