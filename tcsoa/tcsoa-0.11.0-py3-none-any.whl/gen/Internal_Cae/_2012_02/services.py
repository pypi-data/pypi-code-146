from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from typing import List
from tcsoa.base import TcService


class SimulationProcessManagementService(TcService):

    @classmethod
    def importSimulationObjects(cls, processHierarchy: str, workingDirectory: str, itemID: str, itemKey: str, revisionID: str, xmlFileName: str, itemCreationSetting: str, datasetCreationSetting: str) -> bool:
        """
        This internal operation will import the output files generated from execution of simulation tool launch process
        into Teamcenter objects. Based on the input values of parameters itemCreationSetting and
        datasetCreationSetting, ItemRevision and Dataset objects will be created or modified to store the imported
        simulation tool launch data.
        
        It is pre-requisite that Simulation Administrator or user with DBA privileges must configure the simulation
        tool and store it in XML format as a named reference with the Dataset name specified in the preference
        CAE_simulation_tool_config_dsname.
        
        To use this operation, the user should have either a simulation_author or rtt_author license.
        
        
        Use cases:
        Use Case 1: Import Simulation Objects with "As_Needed" Item Creation Setting
        When this operation is executed with Item creation setting "As_Needed", no new Teamcenter Item will be created
        if there exists one as per the process output configuration. If found none, new Item will be created as per the
        process output configuration.
        
        Use Case 2: Import Simulation Objects with "Always" Item Creation Setting
        When this operation is executed with Item creation setting "Always", new Teamcenter Item will be created as per
        the process output configuration.
        
        Use Case 3: Import Simulation Objects with "Never" Item Creation Setting
        When this operation is executed with Item creation setting "Never" and if no existing Item is found as per the
        process output configuration, no new Teamcenter Item will be created.
        
        Use Case 4: Import Simulation Objects with "As_Needed" Dataset Creation Setting
        When this operation is executed with Dataset creation setting "As_Needed", no new Teamcenter Dataset will be
        created if there exists one as per the process output configuration. If found none, new Dataset will be created
        as per the process output configuration.
        
        Use Case 5: Import Simulation Objects with "Always" Dataset Creation Setting
        When this operation is executed with Dataset creation setting "Always", new Teamcenter Dataset will be created
        as per the process output configuration.
        
        Use Case 6: Import Simulation Objects with "Never" Dataset Creation Setting
        When this operation is executed with Dataset creation setting "Never" and if no existing Dataset is found as
        per the process output configuration, no new Teamcenter Dataset will be created.
        """
        return cls.execute_soa_method(
            method_name='importSimulationObjects',
            library='Internal-Cae',
            service_date='2012_02',
            service_name='SimulationProcessManagement',
            params={'processHierarchy': processHierarchy, 'workingDirectory': workingDirectory, 'itemID': itemID, 'itemKey': itemKey, 'revisionID': revisionID, 'xmlFileName': xmlFileName, 'itemCreationSetting': itemCreationSetting, 'datasetCreationSetting': datasetCreationSetting},
            response_cls=bool,
        )


class StructureManagementService(TcService):

    @classmethod
    def generateNodeXML(cls, bomlines: List[BOMLine], domain: str) -> str:
        """
        This internal operation generates a NodeXML representation of the BOMLine object(s) identified in the parameter
        and the selected domain defined as LOV under StructureMap Domains  in  BMIDE. NodeXML is XML-based and is most
        commonly used in the process for creating Data Map and StructureMap rules. The generated NodeXML consists of
        the visible attributes and their values associated with the Item, ItemRevision, related Form objects and the
        BOMLine. The NodeXML syntax is in compliance with the schema defined in tcsim_sm_node.xsd, located in TC_DATA.
        
        For more details on building and executing Data Map and StructureMap rules, please refer to the "Creating
        StructureMap rules" section in the Simulation Process Management Guide->Using StructureMaps chapter of the
        Teamcenter documentation.
        
        
        Use cases:
        Use Case 1: Generate a NodeXML for a selected BOMLine
        When a BOM structure is present or accessible, select one or more BOMLine objects from the BOM structure and
        the selected StructureMap Domain and invoke the generateNodeXML operation to generate the NodeXML
        interpretation of the selected BOMLine objects.
        """
        return cls.execute_soa_method(
            method_name='generateNodeXML',
            library='Internal-Cae',
            service_date='2012_02',
            service_name='StructureManagement',
            params={'bomlines': bomlines, 'domain': domain},
            response_cls=str,
        )
