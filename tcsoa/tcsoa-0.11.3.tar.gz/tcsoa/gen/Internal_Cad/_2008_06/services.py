from __future__ import annotations

from tcsoa.gen.Internal.Cad._2008_06.DataManagement import FeatureQueryInfo, QueryRelatedFeaturesResponse
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def queryRelatedFeatures(cls, featureQueryInfos: List[FeatureQueryInfo]) -> QueryRelatedFeaturesResponse:
        """
        QueryRelatedFeatures allows the user to query for all Feature elements ( GDE and GDELink ) related to an Item
        Revision.
        This query can return all GDE and GDELink elements related to the Item Revision, the GDELinks ( and parent Item
        Revision ) that reference the GDEs and the GDEs ( and parent Item Revision ) referenced by the GDELinks.
        
        Use cases:
        The client wants to know what Feature relations exist in Teamcenter for a particular item Revision. The client
        supplies an item revision, GDE Occurrence, or Occurrence note as the starting point and specifies the data to
        be returned. The client will then get a list of GDE and GDELinks referenced in the hierarchy.
        """
        return cls.execute_soa_method(
            method_name='queryRelatedFeatures',
            library='Internal-Cad',
            service_date='2008_06',
            service_name='DataManagement',
            params={'featureQueryInfos': featureQueryInfos},
            response_cls=QueryRelatedFeaturesResponse,
        )
