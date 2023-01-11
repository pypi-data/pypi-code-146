from __future__ import annotations

from tcsoa.gen.Internal.OccMgmt._2020_05.ImportExport import ImportExcelData, ImportExcelResponse, MappingGroupInput, MappingGroupResponse
from typing import List
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def importExcelAndUpdateMappingGrp(cls, importExcelData: List[ImportExcelData]) -> ImportExcelResponse:
        """
        Imports an Excel file into Teamcenter and creates the product structure and sets the properties on objects
        based on the values given in Excel file. The input Excel file contains a level column to indicate the level of
        the object in the structure. "Level" and "Object Type" columns are mandatory in the input Excel sheet. The
        input Excel file is parsed to import the data to create product structure in Teamcenter. This operation
        supports the creation of objects only. Update and Delete are not supported. The column headers in excel are
        mapped to their respective properties which are saved as a mapping group on "import". This operation support
        create and update of mapping groups.
        
        Use cases:
        1.    The user creates a new mapping group by mapping the property names with the column headers in the Excel
        sheet, giving a new group name and clicking on "Import" button.
        2.    The user uses an existing mapping group by selecting a group name which populates the existing mappings
        and clicking on "Import" button.
        3.    The user updates an existing mapping group by selecting a group name, changing some of the existing
        mappings and clicking on "Import" button.
        """
        return cls.execute_soa_method(
            method_name='importExcelAndUpdateMappingGrp',
            library='Internal-OccMgmt',
            service_date='2020_05',
            service_name='ImportExport',
            params={'importExcelData': importExcelData},
            response_cls=ImportExcelResponse,
        )

    @classmethod
    def importExcelAndUpdateMappingGrpAsync(cls, importExcelData: List[ImportExcelData]) -> None:
        """
        Imports an Excel file into Teamcenter and creates the product structure and sets the properties on objects
        based on the values given in Excel file. The input Excel file contains a level column to indicate the level of
        the object in the structure." Level" and "Object Type" columns are mandatory in the input Excel sheet. The
        input Excel file is parsed to import the data to create product structure in Teamcenter. This operation
        supports the creation of objects only. Update and Delete are not supported. The column headers in excel are
        mapped to their respective properties which are saved as a mapping group on "import". This operation support
        create and update of mapping groups.
        
        Use cases:
        1.    The user creates a new mapping group by mapping the property names with the column headers in the Excel
        sheet, giving a new group name and clicking on "Import" button.
        2.    The user uses an existing mapping group by selecting a group name which populates the existing mappings
        and clicking on "Import" button.
        3.    The user updates an existing mapping group by selecting a group name, changing some of the existing
        mappings and clicking on "Import" button.
        """
        return cls.execute_soa_method(
            method_name='importExcelAndUpdateMappingGrpAsync',
            library='Internal-OccMgmt',
            service_date='2020_05',
            service_name='ImportExport',
            params={'importExcelData': importExcelData},
            response_cls=None,
        )

    @classmethod
    def getMappingGroupInfo(cls, inputs: List[MappingGroupInput]) -> MappingGroupResponse:
        """
        Returns all the mapping group information which includes the names of all mapping groups as well as the mapping
        information of each group. The input Excel file contains a level column to indicate the level of the object in
        the structure. "Level" and "Object Type" columns are mandatory in the input Excel sheet. The column headers of
        the excel file are mapped to their respective properties which are saved into a mapping group. The user can
        create, update or delete the mapping group. The input Excel file is parsed to import the data to create product
        structure in Teamcenter.
        
        Use cases:
        1) User clicks on the "Browse" button to parse an Excel file with a header row that contains display names of
        the properties. This header information is parsed and user is presented mapping screens to map the property
        names with the column headers in the Excel sheet.
        2) If the user selects an existing saved mapping group, the mapped properties get populated for the respective
        column headers.
        """
        return cls.execute_soa_method(
            method_name='getMappingGroupInfo',
            library='Internal-OccMgmt',
            service_date='2020_05',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=MappingGroupResponse,
        )
