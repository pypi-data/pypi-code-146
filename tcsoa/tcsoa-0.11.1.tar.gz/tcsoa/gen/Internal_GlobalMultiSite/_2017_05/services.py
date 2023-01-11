from __future__ import annotations

from typing import List
from tcsoa.gen.GlobalMultiSite._2007_12.ImportExport import NamesAndValues
from tcsoa.base import TcService
from tcsoa.gen.Internal.GlobalMultiSite._2017_05.ImportExport import TransformDataResponse


class ImportExportService(TcService):

    @classmethod
    def transformData(cls, inputFileTickets: List[str], ruleFileNamesOrTickets: List[str], sessionOptions: List[NamesAndValues]) -> TransformDataResponse:
        """
        This operation transforms a list of input files into a specific output file by following a list of transform
        rules and a group of session options.
        
        Use cases:
        Applications need to transform their files into a file with different formats. The process of the
        transformation needs to be controlled by a group rules and options.
        E.g. TcIF needs to transform TCEngXML to TCXML files.
        """
        return cls.execute_soa_method(
            method_name='transformData',
            library='Internal-GlobalMultiSite',
            service_date='2017_05',
            service_name='ImportExport',
            params={'inputFileTickets': inputFileTickets, 'ruleFileNamesOrTickets': ruleFileNamesOrTickets, 'sessionOptions': sessionOptions},
            response_cls=TransformDataResponse,
        )
