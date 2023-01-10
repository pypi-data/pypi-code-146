from __future__ import annotations

from tcsoa.gen.Internal.TCXMLImportExport._2020_12.Briefcase import ImportObjectsFromBriefcaseInput, ExportObjectsToBriefcaseInput
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class BriefcaseService(TcService):

    @classmethod
    def importObjectsFromBriefcase(cls, input: ImportObjectsFromBriefcaseInput) -> ServiceData:
        """
        Imports the objects from a briefcase package file (.bcz) in asynchronous mode using the specified Transfer
        Option Set object and the additional options for scoping data. The import user will be notified with the import
        results when the import is completed.
        """
        return cls.execute_soa_method(
            method_name='importObjectsFromBriefcase',
            library='Internal-TCXMLImportExport',
            service_date='2020_12',
            service_name='Briefcase',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def importObjectsFromBriefcaseAsync(cls, input: ImportObjectsFromBriefcaseInput) -> None:
        """
        Imports the objects from a Briefcase package in asynchronous mode using the specified Transfer Option Set
        object and the additional options for data scoping. The user will be notified with the import results when the
        import is completed.
        """
        return cls.execute_soa_method(
            method_name='importObjectsFromBriefcaseAsync',
            library='Internal-TCXMLImportExport',
            service_date='2020_12',
            service_name='Briefcase',
            params={'input': input},
            response_cls=None,
        )

    @classmethod
    def exportObjectsToBriefcase(cls, input: ExportObjectsToBriefcaseInput) -> ServiceData:
        """
        Exports the objects to the target site into a briefcase package file (.bcz) in asynchronous mode using the
        specified Transfer Option Set object and the additional options for scoping data. The export user will be
        notified with the export resultant data when the export is completed.
        """
        return cls.execute_soa_method(
            method_name='exportObjectsToBriefcase',
            library='Internal-TCXMLImportExport',
            service_date='2020_12',
            service_name='Briefcase',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def exportObjectsToBriefcaseAsync(cls, input: ExportObjectsToBriefcaseInput) -> None:
        """
        Exports the objects to the target site into a briefcase package file (.bcz) in asynchronous mode using the
        specified Transfer Option Set object and the additional options for scoping data. The export user will be
        notified with the export resultant data when the export is completed.
        """
        return cls.execute_soa_method(
            method_name='exportObjectsToBriefcaseAsync',
            library='Internal-TCXMLImportExport',
            service_date='2020_12',
            service_name='Briefcase',
            params={'input': input},
            response_cls=None,
        )
