from __future__ import annotations

from tcsoa.gen.Internal.ImportExport._2010_04.L10NImportExport import ExportObjectsForTranslationResponse
from tcsoa.gen.Internal.ImportExport._2018_06.L10NImportExport import ObjectsInfo2
from tcsoa.base import TcService


class L10NImportExportService(TcService):

    @classmethod
    def exportObjectsForTranslation2(cls, inputObjectsInfo: ObjectsInfo2) -> ExportObjectsForTranslationResponse:
        """
        This operation exports Teamcenter business objects into XML file based on the criteria specified by
        'ObjectsInfo2' structure. This operation is used to export Teamcenter business object that contains localized
        properties so that site administrator or other privileged user can translate the properties to desired locale
        and import back into database using the
        'Teamcenter::Soa::Internal::ImportExport::_2010_04::L10NImportExport::importObjectsForTranslation' operation.
        If the session user does not have the necessary privilege or if 'ObjectsInfo2' structure is not valid then
        operation would fail and the error is returned in the 'ServiceData'. This operation is used to export selected
        business objects for review or translate into desired locale. These two modes are explained below:
        - Review: This exports business objects into XML file for selected statuses where valid localized translation
        exist for given locale. This exported file can be used by language expert to review existing translation for
        their accuracy.
        - Translate: The operation exports business objects into XML file for which there is no translation so that
        language expert can use this XML file and provide a valid language translation in selected locale.
        
        
        
        Use cases:
        General description covers this section.
        """
        return cls.execute_soa_method(
            method_name='exportObjectsForTranslation2',
            library='Internal-ImportExport',
            service_date='2018_06',
            service_name='L10NImportExport',
            params={'inputObjectsInfo': inputObjectsInfo},
            response_cls=ExportObjectsForTranslationResponse,
        )
