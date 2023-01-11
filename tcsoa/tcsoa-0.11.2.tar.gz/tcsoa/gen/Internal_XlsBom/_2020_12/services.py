from __future__ import annotations

from tcsoa.gen.Internal.XlsBom._2020_12.Import import ImportExcelData, StructureInfoResp, ImportExcelResp, ExcelImportInput
from tcsoa.base import TcService


class ImportService(TcService):

    @classmethod
    def importExcelAndUpdateMappingGrp(cls, importExcelData: ImportExcelData) -> ImportExcelResp:
        """
        Description:
        Imports an Excel file into Teamcenter and creates the product structure and sets the properties on objects
        based on the values given in Excel file. The input Excel file contains a level column to indicate the level of
        the object in the structure. "Level" and "Object Type" columns are mandatory in the input Excel sheet. The
        input Excel file is parsed to import the data to create product structure in Teamcenter. This operation
        supports the creation of new objects and update of the existing objects. The column headers in excel are mapped
        to their respective properties which are saved as a mapping group on "import". This operation support create
        and update of mapping groups.
        
        Parameters:
        importExcelData2      A list of type and property related data and the file ticket of the Excel file to
        imported.
        
        Use cases:
        Use Case:
        1.    The user creates a new mapping group by mapping the property names with the column headers in the Excel
        sheet, giving a new group name and clicking on "Import" button.
        2.    The user uses an existing mapping group by selecting a group name which populates the existing mappings
        and clicking on "Import" button.
        3.    The user updates an existing mapping group by selecting a group name, changing some of the existing
        mappings and clicking on "Import" button.
        """
        return cls.execute_soa_method(
            method_name='importExcelAndUpdateMappingGrp',
            library='Internal-XlsBom',
            service_date='2020_12',
            service_name='Import',
            params={'importExcelData': importExcelData},
            response_cls=ImportExcelResp,
        )

    @classmethod
    def importExcelAndUpdateMappingGrpAsync(cls, importExcelData: ImportExcelData) -> None:
        """
        Imports an Excel file into Teamcenter and creates the product structure and sets the properties on objects
        based on the values given in Excel file. The input Excel file contains a level column to indicate the level of
        the object in the structure." Level" and "Object Type" columns are mandatory in the input Excel sheet. The
        input Excel file is parsed to import the data to create product structure in Teamcenter. This operation
        supports the creation of new objects and update of the existing objects. The column headers in excel are mapped
        to their respective properties which are saved as a mapping group on "import". This operation support create
        and update of mapping groups.
        
        Use cases:
        1.    The user creates a new mapping group by mapping the property name with the column headers in the Excel
        sheet, giving a new group name and clicking on "Import" button.
        2.    The user uses an existing mapping group by selecting a group name which populates the existing mappings
        and clicking on "Import" button.
        3.    The user updates an existing mapping group by selecting a group name, changing some of the existing
        mappings and clicking on "Import" button.
        """
        return cls.execute_soa_method(
            method_name='importExcelAndUpdateMappingGrpAsync',
            library='Internal-XlsBom',
            service_date='2020_12',
            service_name='Import',
            params={'importExcelData': importExcelData},
            response_cls=None,
        )

    @classmethod
    def getStructureInfoFromExcel(cls, inputData: ExcelImportInput) -> StructureInfoResp:
        """
        This operation retrieves the page of structure information from the input Excel file. The output also contains
        a cursor that defines the place to start the next page location. The cursor must be passed back in to any
        subsequent call to get the next page of nodes.
        """
        return cls.execute_soa_method(
            method_name='getStructureInfoFromExcel',
            library='Internal-XlsBom',
            service_date='2020_12',
            service_name='Import',
            params={'inputData': inputData},
            response_cls=StructureInfoResp,
        )
