from __future__ import annotations

from tcsoa.gen.ImportExport._2012_09.FileImportExport import ImportFromApplicationInputData3
from tcsoa.gen.ImportExport._2011_06.FileImportExport import ImportFromApplicationResponse1
from typing import List
from tcsoa.base import TcService


class FileImportExportService(TcService):

    @classmethod
    def importFromApplication(cls, inputs: List[ImportFromApplicationInputData3]) -> ImportFromApplicationResponse1:
        """
        This operation imports a Requirement Specification document containing Requirement and Paragraph objects. It
        creates Requirement / Paragraph objects and associated data (FullText for each created Item to store the
        content from the document and IMAN_Specification relation between FullText and each created Item). The input
        structure for this operation contains file meta data information, type of specification elements (SpecElement)
        to be created, application format of the MS Word document being imported, keyword parsing options to be used
        during import, live or static import mode to be used for import, option to import as new specification or under
        the selected BOMLine object and description to be set on the Item once imported.
        """
        return cls.execute_soa_method(
            method_name='importFromApplication',
            library='ImportExport',
            service_date='2012_09',
            service_name='FileImportExport',
            params={'inputs': inputs},
            response_cls=ImportFromApplicationResponse1,
        )
