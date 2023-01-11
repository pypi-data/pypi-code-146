from __future__ import annotations

from tcsoa.gen.BusinessObjects import AppInterface
from tcsoa.gen.Ai._2010_09.Ai import GenerateAndEvaluateStructureResponse
from typing import List
from tcsoa.gen.Ai._2008_06.Ai import ObjectsWithConfig
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def generateAndEvaluateStructure(cls, aiObject: AppInterface, objectsToProcess: List[ObjectsWithConfig], exportTransferMode: str, absoluteXmlFileName: str, xpaths: List[str]) -> GenerateAndEvaluateStructureResponse:
        """
        Service to generate a plmxml based on the input objects, configuration, transfermode provided and  evaluate the
        specified xpaths 1.0 expressions against that plmxml. Optionally - a pre-existing xml file can be specified
        (via a full path accessible in tc server environment). In that case, only the xpaths argument is used along
        with the absoluteXmlFile argument.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='generateAndEvaluateStructure',
            library='Ai',
            service_date='2010_09',
            service_name='Ai',
            params={'aiObject': aiObject, 'objectsToProcess': objectsToProcess, 'exportTransferMode': exportTransferMode, 'absoluteXmlFileName': absoluteXmlFileName, 'xpaths': xpaths},
            response_cls=GenerateAndEvaluateStructureResponse,
        )
