from __future__ import annotations

from tcsoa.gen.Internal.ImportExport._2010_04.L10NImportExport import TransientFileTicketStatusInfo, ObjectsInfo, ExportObjectsForTranslationResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class L10NImportExportService(TcService):

    @classmethod
    def importTranslations(cls, fileInfo: List[TransientFileTicketStatusInfo]) -> ExportObjectsForTranslationResponse:
        """
        This operation imports localized values for all the business objects specified in list of
        'TransientFileTicketStatusInfo' structure.
        """
        return cls.execute_soa_method(
            method_name='importTranslations',
            library='Internal-ImportExport',
            service_date='2010_04',
            service_name='L10NImportExport',
            params={'fileInfo': fileInfo},
            response_cls=ExportObjectsForTranslationResponse,
        )

    @classmethod
    def exportObjectsForTranslation(cls, inpuInfo: ObjectsInfo) -> ExportObjectsForTranslationResponse:
        """
        This operation exports Teamcenter business objects into XML file based on the criteria specified by
        'ObjectsInfo' structure. This operation is used to export Teamcenter business object that contains localized
        properties so that site administrator or other privileged user can translate the properties to desired locale
        and import back into database using the 'importObjectsForTranslation' operation. If the session user does not
        have the necessary privilege or if 'ObjectsInfo' structure is not valid then operation would fail and the error
        is returned in the 'ServiceData'. This operation is used to export selected business objects for review or
        translate into desired locale. These two modes are explained below:
        
        - Review: This exports business objects into XML file for selected statuses where valid localized translation
        exist for given locale. This exported file can be used by language expert to review existing translation for
        their accuracy.  
        - Translate: The operation exports business objects into XML file for which there is no translation so that
        language expert can use this XML file and provide a valid language translation in selected locale.
        
        """
        return cls.execute_soa_method(
            method_name='exportObjectsForTranslation',
            library='Internal-ImportExport',
            service_date='2010_04',
            service_name='L10NImportExport',
            params={'inpuInfo': inpuInfo},
            response_cls=ExportObjectsForTranslationResponse,
        )

    @classmethod
    def filterObjectsForTranslation(cls, inputInfo: ObjectsInfo) -> ServiceData:
        """
        This operation is very similar to 'exportObjectsForTranslation'. The only difference is this operation returns
        a list of filtered objects instead of returning an XML file. This operation can be useful to present the
        filtered list of business objects that contain localized properties to the end user as oppose to creating an
        xml files however this can't be used to import the selected objects or modify the objects. If user intention is
        to modify the localized values for given business object then it's recommended to use
        'exportObjectsForTranslation' as opposed to this operation. This operation is used to filter selected business
        objects for review or translate into desired locale. These two modes are explained below:
        - Review: This filters business objects for selected statuses where valid localized translation exist for given
        locale. 
        - Translate: The operation filters and returns business objects for which there is no translation.
        
        """
        return cls.execute_soa_method(
            method_name='filterObjectsForTranslation',
            library='Internal-ImportExport',
            service_date='2010_04',
            service_name='L10NImportExport',
            params={'inputInfo': inputInfo},
            response_cls=ServiceData,
        )
