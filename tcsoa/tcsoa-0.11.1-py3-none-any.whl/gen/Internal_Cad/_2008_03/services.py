from __future__ import annotations

from tcsoa.gen.Internal.Cad._2008_03.DataManagement import ExportConfiguredNXAssemblyResponse, ExportConfiguredNXAssemblyInfo
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def exportConfiguredNXAssembly(cls, inputs: List[ExportConfiguredNXAssemblyInfo]) -> ExportConfiguredNXAssemblyResponse:
        """
        This operation is used by the command line utility ps_exportconfignxassembly and from the Teamcenter Rich
        Client Structure Manager, menu item Tools -> Export Configured UGNX Assembly.  This feature is enabled in
        Teamcenter Structure Manager only if the preference TC_ ExportConfigUGNXAssembly is true.  The assembly is
        configured using the given revision rule and saved variant rule.  The goal is to export a configured assembly
        structure to native NX.   This feature is supported by wrapping the existing functionality in a published BOM
        ITK. The client UI is designed to enable to user to initiate the export operation from the Structure Manager.
        
        Use cases:
        Usecase 1: 
        Initiating export configured UGNX assembly from the Teamcenter Rich Client.
        User configures a UGNX assembly in Structure Manager using revision rule and variant rule. 
        User selects the top BOMLine and initiates Tools->ExportConfiguredUGNXAssembly
        Upon completion of the operation, the entire configured structure in Structure Manager is exported to the temp
        directory.
        The precondition to this usecase is that the preference TC_ ExportConfigUGNXAssembly has to be true.
        
        Use case 2: 
        Initiating export configured UGNX assembly from the with the command line utility ps_ exportconfignxassembly
        User runs the command line utility ps_exportconfigurednxassembly with the following arguments: ItemId of the
        assembly, ItemRevId of the assembly, revision rule name, and variant rule name. The optional arguments are
        -display, -debug=<y or n> and the list of excluded items.
        Upon completion of the operation, the assembly and all its configured children are exported to the temp
        directory.
        """
        return cls.execute_soa_method(
            method_name='exportConfiguredNXAssembly',
            library='Internal-Cad',
            service_date='2008_03',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=ExportConfiguredNXAssemblyResponse,
        )
