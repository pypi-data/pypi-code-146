from __future__ import annotations

from tcsoa.gen.ImportExport._2012_09.FileImportExport import ImportFromApplicationInputData3
from tcsoa.base import TcService


class FileImportExportService(TcService):

    @classmethod
    def importSpecAsync(cls, input: ImportFromApplicationInputData3) -> None:
        """
        This operation imports the selected Requirement Specification word document asynchronously to Teamcenter.
        Following are the supported input application formats:
        - MSWordXML- This mode provides the capability of importing MSWord document to Teamcenter.
        
        
        
        Use cases:
        User selects or navigates inside a folder and clicks on the Import Specification button in the toolbar. This
        will show a panel with options to browse a Word file, a dropdown lists to select a Specification type and a
        SpecElement type. If user clicks on Import button, the Word document is imported in Teamcenter. User receives a
        notification in active workspace client after the import completes.
        """
        return cls.execute_soa_method(
            method_name='importSpecAsync',
            library='Internal-ImportExport',
            service_date='2017_05',
            service_name='FileImportExport',
            params={'input': input},
            response_cls=None,
        )
