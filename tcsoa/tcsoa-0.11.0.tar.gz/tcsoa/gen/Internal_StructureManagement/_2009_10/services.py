from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMWindow, ItemRevision
from tcsoa.gen.Internal.StructureManagement._2009_10.EffectivitiesManagement import EffectivityGroupInputInfo, EffectivitiesInputInfo, GetEffectivityGrpListResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class EffectivitiesManagementService(TcService):

    @classmethod
    def setEndItemEffectivityGroups(cls, effectivityGrpInput: List[EffectivityGroupInputInfo]) -> ServiceData:
        """
        Apply a list of Fnd0EffectvtyGrpRevision objects to a BOMWindow
        
        Use cases:
        User selects a structure with occurrence Effectivity defined and opens it in a BOMWindow .  This structure can
        then be configured by applying a list of Fnd0EffectvtyGrpRevision objects to the BOMWindow. This use case
        requires Multi Unit Configuration to be enabled at the site.
        """
        return cls.execute_soa_method(
            method_name='setEndItemEffectivityGroups',
            library='Internal-StructureManagement',
            service_date='2009_10',
            service_name='EffectivitiesManagement',
            params={'effectivityGrpInput': effectivityGrpInput},
            response_cls=ServiceData,
        )

    @classmethod
    def createOrUpdateEffectivites(cls, effectivitiesInfo: List[EffectivitiesInputInfo], effectivityGroupRevision: ItemRevision) -> ServiceData:
        """
        Creates or updates effectivity information for the given Fnd0EffectvtyGrpRevision represented by the input
        parameter 'effectivityGroupRevision'.
        
        Use cases:
        - Create Effectivity objects for a given Fnd0EffectvtyGrpRevision  object.
        - Update Effectivity information like unit range and end item for a list of Effectivity objects belonging to an
        Fnd0EffectvtyGrpRevision
        - Remove an Effectivity object from an Fnd0EffectvtyGrpRevision object.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateEffectivites',
            library='Internal-StructureManagement',
            service_date='2009_10',
            service_name='EffectivitiesManagement',
            params={'effectivitiesInfo': effectivitiesInfo, 'effectivityGroupRevision': effectivityGroupRevision},
            response_cls=ServiceData,
        )

    @classmethod
    def getEffectivityGrpRevList(cls, bomWindow: BOMWindow) -> GetEffectivityGrpListResponse:
        """
        Gets the list of Fnd0EffectvtyGrpRevision objects applied on the given BOMWindow
        
        Use cases:
        User would like to retrieve the list of Fnd0EffectvtyGrpRevision objects applied to a BOMWindow
        """
        return cls.execute_soa_method(
            method_name='getEffectivityGrpRevList',
            library='Internal-StructureManagement',
            service_date='2009_10',
            service_name='EffectivitiesManagement',
            params={'bomWindow': bomWindow},
            response_cls=GetEffectivityGrpListResponse,
        )
