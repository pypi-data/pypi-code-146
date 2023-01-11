from __future__ import annotations

from tcsoa.gen.Internal.ImportExport._2017_11.FileImportExport import ImportDocumentInputData
from tcsoa.gen.ImportExport._2011_06.FileImportExport import ImportFromApplicationResponse1
from typing import List
from tcsoa.base import TcService


class FileImportExportService(TcService):

    @classmethod
    def importDocumentAsync(cls, input: ImportDocumentInputData) -> None:
        """
        This operation imports the selected Requirement Specification word document asynchronously to Teamcenter.
        Import will be done using keywords specified by user and will be done in the background.
        """
        return cls.execute_soa_method(
            method_name='importDocumentAsync',
            library='Internal-ImportExport',
            service_date='2017_11',
            service_name='FileImportExport',
            params={'input': input},
            response_cls=None,
        )

    @classmethod
    def importDocumentOffline(cls, inputs: List[ImportDocumentInputData]) -> ImportFromApplicationResponse1:
        """
        This operation imports a Requirement Specification document containing Requirement objects and related
        information. It creates SpecElement objects and saves associated data (FullText for each created object to
        store the content from the document and IMAN_Specification relation between FullText and each created object).
        The input structure for this operation contains type of specification elements (SpecElement) to be created,
        keyword parsing rules to be used during import, option to import as new specification or under the selected
        object and description to be set on the Specification once imported.
        """
        return cls.execute_soa_method(
            method_name='importDocumentOffline',
            library='Internal-ImportExport',
            service_date='2017_11',
            service_name='FileImportExport',
            params={'inputs': inputs},
            response_cls=ImportFromApplicationResponse1,
        )
