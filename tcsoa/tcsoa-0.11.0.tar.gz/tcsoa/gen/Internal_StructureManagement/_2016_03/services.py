from __future__ import annotations

from tcsoa.gen.Internal.StructureManagement._2016_03.StructureVerification import AlignMatchedCandidateElem, AdditionalData, FindMatchingCandidatesResp, SearchCandidateElems, AlignMatchedCandidatesResp
from typing import List
from tcsoa.base import TcService


class StructureVerificationService(TcService):

    @classmethod
    def alignMatchedCandidates(cls, inputObjects: List[AlignMatchedCandidateElem], additionalInfo: AdditionalData) -> AlignMatchedCandidatesResp:
        """
        This operation aligns matched pair of BOMLine objects. Alignment means the Absolute Occurrence Identifier
        (IDInContext Top Level) will be in sync after the operation completes successfully or the Manufacturing BOMLine
        object will be replaced by the Engineering BOMLine object. In addition, the specified properties will be
        synced. The properties to be aligned will be governed by the MEAlignPropertiesList preference and any
        additional ones passed via the additionalInfo generic structure using the key: AlignProperties and the value
        being a vector of internal BOMLine object property names.
        The AdditionalData type argument currently supports the following:
        AdditionalInfo.strMap:
        Key: AlignProperties
        Value: A list of internal BOMLine property names to be synced.
        """
        return cls.execute_soa_method(
            method_name='alignMatchedCandidates',
            library='Internal-StructureManagement',
            service_date='2016_03',
            service_name='StructureVerification',
            params={'inputObjects': inputObjects, 'additionalInfo': additionalInfo},
            response_cls=AlignMatchedCandidatesResp,
        )

    @classmethod
    def findMatchingCandidates(cls, inputObjects: List[SearchCandidateElems], additionalInfo: AdditionalData) -> FindMatchingCandidatesResp:
        """
        This operation returns candidate matching target BOMLine objects for the given source BOMLine objects, based on
        specified search criteria. The additionalInfo parameter currently supports the following:
        AdditionalInfo.strMap:
        Key: SearchCriteriaPreference
        Value: name of the preference containing the search criteria parameters at index 0.
        """
        return cls.execute_soa_method(
            method_name='findMatchingCandidates',
            library='Internal-StructureManagement',
            service_date='2016_03',
            service_name='StructureVerification',
            params={'inputObjects': inputObjects, 'additionalInfo': additionalInfo},
            response_cls=FindMatchingCandidatesResp,
        )
