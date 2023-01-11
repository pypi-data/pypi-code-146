from __future__ import annotations

from tcsoa.gen.Internal.Cad._2013_05.DataManagement import FeatureQueryInfo, QueryPartRelatedFeaturesResponse
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def queryPartRelatedFeatures(cls, featureQueryInfo: List[FeatureQueryInfo]) -> QueryPartRelatedFeaturesResponse:
        """
        Return the PartToPart Relation information for a set of ItemRevisions.
        
        Use cases:
        User is using the NX Relation Browser. They select some items and want to know what the part to part relations
        are.
        """
        return cls.execute_soa_method(
            method_name='queryPartRelatedFeatures',
            library='Internal-Cad',
            service_date='2013_05',
            service_name='DataManagement',
            params={'featureQueryInfo': featureQueryInfo},
            response_cls=QueryPartRelatedFeaturesResponse,
        )
