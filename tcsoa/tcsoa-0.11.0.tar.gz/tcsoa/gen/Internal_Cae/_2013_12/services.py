from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SimulationProcessManagementService(TcService):

    @classmethod
    def importSimulationObjects2(cls, processHierarchy: str, workingDirectory: str, itemID: str, objectUID: str, revisionID: str, xmlFileName: str, itemCreationSetting: str, datasetCreationSetting: str) -> ServiceData:
        """
        This internal operation will import the output files generated from execution of simulation tool launch process
        into Teamcenter objects. Based on the input values of parameters itemCreationSetting and datasetCreationSetting
        ItemRevision and Dataset objects will be created or modified. It is pre-requisite that the Simulation
        Administrator or user with DBA privileges must configure the simulation tool and store it in XML format as a
        named reference with the Dataset name specified in the preference CAE_simulation_tool_config_dsname. 
        
        Use cases:
        Use Case 1: Import Simulation Objects with As Needed Item Creation Setting
        When this operation is executed with Item creation setting As Needed, no new Teamcenter Item will be created if
        there exists one as per the process output configuration. If found none, new Item will be created as per the
        process output configuration.
        
        Use Case 2: Import Simulation Objects with Always Item Creation Setting
        When this operation is executed with Item creation setting Always, new Teamcenter Item will be created as per
        the process output configuration.
        
        Use Case 3: Import Simulation Objects with Never Item Creation Setting
        When this operation is executed with Item creation setting Never and if no existing Item is found as per the
        process output configuration, no new Teamcenter Item will be created.
        
        Use Case 4: Import Simulation Objects with As Needed Dataset Creation Setting
        When this operation is executed with Dataset creation setting As Needed, no new Teamcenter Dataset will be
        created if there exists one as per the process output configuration. If found none, new Dataset will be created
        as per the process output configuration.
        
        Use Case 5: Import Simulation Objects with Always Dataset Creation Setting
        When this operation is executed with Dataset creation setting Always, new Teamcenter Dataset will be created as
        per the process output configuration.
        
        Use Case 6: Import Simulation Objects with Never Dataset Creation Setting
        When this operation is executed with Dataset creation setting Never and if no existing Dataset is found as per
        the process output configuration, no new Teamcenter Dataset will be created.
        """
        return cls.execute_soa_method(
            method_name='importSimulationObjects2',
            library='Internal-Cae',
            service_date='2013_12',
            service_name='SimulationProcessManagement',
            params={'processHierarchy': processHierarchy, 'workingDirectory': workingDirectory, 'itemID': itemID, 'objectUID': objectUID, 'revisionID': revisionID, 'xmlFileName': xmlFileName, 'itemCreationSetting': itemCreationSetting, 'datasetCreationSetting': datasetCreationSetting},
            response_cls=ServiceData,
        )


class StructureManagementService(TcService):

    @classmethod
    def propagateCAEModelAttributes(cls) -> bool:
        """
        This operation propagates all selected attributes on a target CAEModel structure, on which the CAE
        Accountability Check was performed. It also attaches the named HTML report Dataset on CAEModel root Item. The
        HTML report contains old value, new value and propagation status of each partially matched attribute. Dataset
        name is driven from CAE_attribute_propagate_summary_dataset_name preference.
        
        
        Use cases:
        This operation is a follow-up operation based on the result from CAE Accountability Check comparison. If the
        user wants to propagate the target CAEModel attributes, then CAE Accountability Check operation should be
        performed with selected attributes between Product and Model structures. Then propagateCAEModelAttributes
        should be called to propagate the partially matched attributes.
        """
        return cls.execute_soa_method(
            method_name='propagateCAEModelAttributes',
            library='Internal-Cae',
            service_date='2013_12',
            service_name='StructureManagement',
            params={},
            response_cls=bool,
        )
