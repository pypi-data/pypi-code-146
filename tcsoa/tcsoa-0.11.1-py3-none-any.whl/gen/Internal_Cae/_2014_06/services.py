from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, ItemRevision
from typing import List
from tcsoa.gen.Internal.Cae._2014_06.StructureManagement import MonitorResponse
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def loadSimulationDataMonitor(cls, rootbomline: BOMLine) -> MonitorResponse:
        """
        CAE Manager provides capabilities to create and manage CAE data. Often this consists of a simulation structure
        where each component is expected to have certain attribute values set and manage certain types of data. The
        analyst wants to quickly assess pertinent attribute values and existence of pertinent data of all components of
        a simulation structure. 
        The CAE Manager application will now provides the capability to configure and launch a "Simulation Data
        Monitor" to access the status of components loaded in the model view.
        This operation will get the simulation data monitor configuration from the client side (RAC) and depending upon
        the configuration it will get the status of components loaded in the model view.
        
        Use cases:
        This operation get the valid simulation data monitor configuration and when open simulation data monitor view
        command is invoked on the loaded simulation strucure on Model view, operation prepare a response containing the
        status of monitored components    attributes and attached files as per the simulation data monitor
        configuration.
        
        Step:
        1. Opens CAE Manager Application.
        2. Load simulation structure on Model view.
        3. Clicks on "Open Secondary Views" drop down.
        4. Select "Simulation Data Monitor" view from drop down list.
        """
        return cls.execute_soa_method(
            method_name='loadSimulationDataMonitor',
            library='Internal-Cae',
            service_date='2014_06',
            service_name='StructureManagement',
            params={'rootbomline': rootbomline},
            response_cls=MonitorResponse,
        )

    @classmethod
    def refreshSimulationDataMonitor(cls, itemrevisions: List[ItemRevision]) -> MonitorResponse:
        """
        CAE Manager provides capabilities to create and manage CAE data. Often this consists of a simulation structure
        where each component is expected to have certain attribute values set and manage certain types of data. The
        analyst wants to quickly assess pertinent attribute values and existence of pertinent data of all components of
        a simulation structure. 
        The CAE Manager application will now provides the capability to configure and launch a "Simulation Data
        Monitor" to access the status of components loaded in the model view.
        The analyst can leave the Simulation Data Monitor active for any desired length of time.
        CAE Manager will provide a refresh command in the monitor which will refresh the status of selected components.
        This operation will use the simulation data monitor configuration used at the time of load  and apply it again
        for the list of selected compoents from model view.
        
        
        Use cases:
        This operation get the simulation data monitor configuration used at the time load operation and when open
        refresh command is invoked on the selected components of simulation data monitor detail table, operation
        prepare a response containing the status of selected components attributes and attached files as per the
        simulation data monitor configuration.
        
        Step:
        1. Opens CAE Manager Application.
        2. Load simulation structure on Model view.
        3. Actor opens "Simulation Data Monitor" view from Model view.
        4. Select component(s) appearing on detail table.
        5. Clicks refresh icon appear on toolbar of Simulation Data Monitor view.
        """
        return cls.execute_soa_method(
            method_name='refreshSimulationDataMonitor',
            library='Internal-Cae',
            service_date='2014_06',
            service_name='StructureManagement',
            params={'itemrevisions': itemrevisions},
            response_cls=MonitorResponse,
        )
