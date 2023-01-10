from __future__ import annotations

from tcsoa.gen.Cad._2018_06.StructureManagement import AssemblyConfigurationResponse
from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def writeAssemblyConfigurationDetails(cls, bomWindow: BusinessObject, optionSetName: str) -> AssemblyConfigurationResponse:
        """
        This operation gets the fully unpacked product structure for the input configured structure. It takes as input
        a bomWindow object of a structure that is already configured, in say, the Teamcenter Rich client and  a TIE
        export option set name. The fully qualified product structure that in the output can be used by, say, a CAD
        client to open the structure with the exact same configuration.
        This operation allows a user to configure a product structure in the Teamcenter Rich Client (RAC) and then open
        it in a CAD or other client application. That hand-off includes a fully qualified product structure that the
        CAD application would use to construct the product in the exact same configuration as that in the RAC.
        This operation uses the TIE export process to get the product structure data to write to the file. The
        structure data written will be the fully unpacked structure.
        The export option set will control the level and scope of the structure and related objects to traverse.
        Individual CAD integrations should define or create an option set that includes the CAD data types.
        
        Use cases:
        A user configures an assembly in a particular way, using Revision Rule, Variants, Effectivity, etc in the
        Strcuture Manager application in RAC. After setting up all the configuration details, the user wishes to open
        the assembly in a CAD application.  The user expectation is that the assembly as opened in the CAD application
        will mirror the product structure in the Structure Manager.
        
        To make this happen, the CAD application should add a custom "Open in CAD" command in the Structure Manager
        application. The command will call this SOA operation with the selected BOM Window as the input. The TIE export
        option to be used will be CAD specific.
        This operation will then write the structure data to an xml file in the transient volume and return the file
        read ticket. The file can be downloaded by using the regular file download ITKs/SOAs. 
        The CAD application will download the file and read the structure details and load/open the structure
        accordingly. 
        These are the various use cases used to configure Product Structure in Structure Manager and used to write data
        in TCXML file.
        """
        return cls.execute_soa_method(
            method_name='writeAssemblyConfigurationDetails',
            library='Cad',
            service_date='2018_06',
            service_name='StructureManagement',
            params={'bomWindow': bomWindow, 'optionSetName': optionSetName},
            response_cls=AssemblyConfigurationResponse,
        )
