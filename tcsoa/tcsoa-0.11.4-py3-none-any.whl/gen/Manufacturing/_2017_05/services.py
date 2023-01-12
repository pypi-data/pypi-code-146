from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Manufacturing._2017_05.ImportExport import NamesAndValues, MfgImportFromBriefcaseResponse
from tcsoa.gen.Manufacturing._2017_05.Validation import RegisteredCallbackObjectsResponse
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def importFromBriefcase(cls, fmsTicket: str, optionSetTag: BusinessObject, optionNamesAndValues: NamesAndValues, sessionOptionAndValues: NamesAndValues) -> MfgImportFromBriefcaseResponse:
        """
        This operation is applicable specifically for Manufacturing Process Planner MPP application.
        This operation performs following operation
        Teamcenter::Soa::GlobalMultiSite::_2008_06::ImportExport importObjectsFromOfflinePackage
        In addition to this, it supports asynchronous import of briefcase.
        
        Use cases:
        Use Case 1: Importing objects from briefcase
        This operation can be used in Manufacturing Process Planner (MPP) application to import Briefcase file into
        Teamcenter. Briefcase file is a zipped file containing TC XML and data set files. The TC XML file specifies the
        object to be imported. The import dialog presents various option sets to control the objects during import.
        First time import will create the objects and upload the datasets. Subsequent import of same object will update
        it. Importer log is generated and presented after the import.
        """
        return cls.execute_soa_method(
            method_name='importFromBriefcase',
            library='Manufacturing',
            service_date='2017_05',
            service_name='ImportExport',
            params={'fmsTicket': fmsTicket, 'optionSetTag': optionSetTag, 'optionNamesAndValues': optionNamesAndValues, 'sessionOptionAndValues': sessionOptionAndValues},
            response_cls=MfgImportFromBriefcaseResponse,
        )


class ValidationService(TcService):

    @classmethod
    def getAllRegisteredCallbacks(cls, callbackType: str) -> RegisteredCallbackObjectsResponse:
        """
        This operation returns all the registered customized callbacks for the given callback  type.
        """
        return cls.execute_soa_method(
            method_name='getAllRegisteredCallbacks',
            library='Manufacturing',
            service_date='2017_05',
            service_name='Validation',
            params={'callbackType': callbackType},
            response_cls=RegisteredCallbackObjectsResponse,
        )
