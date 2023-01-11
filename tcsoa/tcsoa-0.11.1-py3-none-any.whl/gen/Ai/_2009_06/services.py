from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, AppInterface
from tcsoa.gen.Ai._2009_06.Ai import GenerateScopedMultipleStructure3Response
from typing import List
from tcsoa.gen.Ai._2008_06.Ai import ObjectsWithConfig
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def generateScopedMultipleStructure3(cls, aiObject: AppInterface, objectsToProcess: List[ObjectsWithConfig], exportTransferMode: str, serverMode: int) -> GenerateScopedMultipleStructure3Response:
        """
        GenerateScopedMultipleStructure3: Same as GenerateScopedMultipleStructure2 - except filetickets are returned.
        If aiObject is specified - it is only
        used to get the TransferMode (in case the exportTransferMode is not specified).
        objects or occurrence group objects - specified as application refs. The configuration is optional
        if the ids consist of StructureContexts. ApplicationRefs can be ids of occurrence from a previous
        export from TC, or APNs or AbsOccs, or OccurrenceGroup or an Item/Itemrev(only one in that last case).
        If the Appref is custom (non TcEng AppRef), occurrence appref must resolve to AbsOccurrence or APN ),
        or they can be ids of structure context/occurrence group objects. The return is the transient file ticket
        for the plmxml file generated. In case any of the input apprefs cannot be processed they will be returned
        in the data member of response. Errors during plmxml processing will be returned in partialerror as
        xml string, based on TcError.xsd in iman_data folder. Configuration structure can be used to specify
        default revrule (if true) all other fields are ignored. Basically, they are declared in the order of
        precedence (where duplication is possible).
        """
        return cls.execute_soa_method(
            method_name='generateScopedMultipleStructure3',
            library='Ai',
            service_date='2009_06',
            service_name='Ai',
            params={'aiObject': aiObject, 'objectsToProcess': objectsToProcess, 'exportTransferMode': exportTransferMode, 'serverMode': serverMode},
            response_cls=GenerateScopedMultipleStructure3Response,
        )

    @classmethod
    def getPersistentObjects(cls, inputLines: List[BusinessObject]) -> ServiceData:
        """
        Given a set of bomlines from the same window, create a private structure context and return that. If the input
        contains any persistent objects like a workspaceobject - those will be returned as is.
        """
        return cls.execute_soa_method(
            method_name='getPersistentObjects',
            library='Ai',
            service_date='2009_06',
            service_name='Ai',
            params={'inputLines': inputLines},
            response_cls=ServiceData,
        )
