from __future__ import annotations

from tcsoa.gen.BusinessObjects import AppInterface
from tcsoa.gen.Ai._2007_12.Ai import GenerateScopedMultipleStructureResponse, GenerateScopedSyncRequestResponse, ObjectsWithConfig
from typing import List
from tcsoa.gen.Ai._2006_03.Ai import RequestDetail
from tcsoa.base import TcService


class AiService(TcService):

    @classmethod
    def generateScopedMultipleStructure(cls, aiObject: AppInterface, objectsToProcess: List[ObjectsWithConfig], exportTransferMode: str, serverMode: int) -> GenerateScopedMultipleStructureResponse:
        """
        GenerateScopedMultipleStructure: Same as GenerateScopedSyncRequest - except no aiObject is needed. If specified
        - it is only
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
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='generateScopedMultipleStructure',
            library='Ai',
            service_date='2007_12',
            service_name='Ai',
            params={'aiObject': aiObject, 'objectsToProcess': objectsToProcess, 'exportTransferMode': exportTransferMode, 'serverMode': serverMode},
            response_cls=GenerateScopedMultipleStructureResponse,
        )

    @classmethod
    def generateScopedSyncRequest(cls, aiObject: AppInterface, objectsToProcess: List[ObjectsWithConfig], requestDetail: RequestDetail) -> GenerateScopedSyncRequestResponse:
        """
        Generates a new Sync Request for the given occurrences (from any context) or Structure Context
        objects or occurrence group objects - specified as application refs. The configuration is optional
        if the ids consist of StructureContexts. ApplicationRefs can be ids of occurrence from a previous
        export from TC, or APNs or AbsOccs, or OccurrenceGroup or an Item/Itemrev(only one in that last case).
        If the Appref is custom (non TcEng AppRef), occurrence appref must resolve to AbsOccurrence or APN ),
        or they can be ids of structure context/occurrence group objects. The return will be the details
        of the newly created Sync Request. Note that the name, desc, scope, updateType of this request are
        based on the passed in requestDetail. The other fields of the RequestDetail are
        not used during input. In case any of the input apprefs cannot be processed they will be returned
        in the failedIndices structure. Errors during plmxml processing will be returned in partialerror
        , based on TcError.xsd in iman_data folder.
        
        Exceptions:
        >Thrown on service failure.
        """
        return cls.execute_soa_method(
            method_name='generateScopedSyncRequest',
            library='Ai',
            service_date='2007_12',
            service_name='Ai',
            params={'aiObject': aiObject, 'objectsToProcess': objectsToProcess, 'requestDetail': requestDetail},
            response_cls=GenerateScopedSyncRequestResponse,
        )
