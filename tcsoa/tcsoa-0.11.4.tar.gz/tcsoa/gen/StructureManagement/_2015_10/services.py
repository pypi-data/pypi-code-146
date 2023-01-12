from __future__ import annotations

from tcsoa.gen.StructureManagement._2015_10.Effectivity import EditRelStatusEffectivityInput, EditOccEffectivityInput, RemoveRelStatusEffectivityInput, RemoveOccEffectivitiesInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class EffectivityService(TcService):

    @classmethod
    def removeOccurrenceEffectivities(cls, input: List[RemoveOccEffectivitiesInput]) -> ServiceData:
        """
        This operation removes effectivity objects from the specified BOMLine objects.
        
        Use cases:
        User can remove an occurrence effectivity by choosing Tools->Effectivity->Occurrence Effectivity, then in the
        Occurrence Effectivity dialog box, click Remove to clear all boxes. Click OK and Teamcenter removes the
        effectivity object from the selected occurrence. Any other occurrences sharing this effectivity retain their
        references to the effectivity object.
        """
        return cls.execute_soa_method(
            method_name='removeOccurrenceEffectivities',
            library='StructureManagement',
            service_date='2015_10',
            service_name='Effectivity',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def removeReleaseStatusEffectivity(cls, input: List[RemoveRelStatusEffectivityInput]) -> ServiceData:
        """
        This operation removes effectivity object from the specified released status
        
        Use cases:
        User can remove a release status effectivity by choosing Views->Effectivity->Revision Effectivity, then in the
        Effectivity dialog, select the corresponding release status and click Delete.
        """
        return cls.execute_soa_method(
            method_name='removeReleaseStatusEffectivity',
            library='StructureManagement',
            service_date='2015_10',
            service_name='Effectivity',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def editOccurrenceEffectivity(cls, input: List[EditOccEffectivityInput]) -> ServiceData:
        """
        This operation updates effectivity object for the specified BOMLine
        
        Use cases:
        User can configure a release status by choosing Tools->Effectivity->Revision Effectivity, then in the
        Effectivity dialog, select the corresponding release status and click create. Define Unit/Date range to set
        effectivity on the release status.
        """
        return cls.execute_soa_method(
            method_name='editOccurrenceEffectivity',
            library='StructureManagement',
            service_date='2015_10',
            service_name='Effectivity',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def editReleaseStatusEffectivity(cls, input: List[EditRelStatusEffectivityInput]) -> ServiceData:
        """
        This operation updates effectivity object for the specified released status
        
        Use cases:
        - User can edit a release status by choosing Views->Effectivity->Revision Effectivity, then in the Revision
        Effectivity dialog box, select the corresponding release status effectivity and click Edit. Modify Unit/Date
        range to update effectivity on the release status.
        - User can also edit release status effectivity in My Teamcenter. Double-click the item status and change the
        displayed value.
        
        """
        return cls.execute_soa_method(
            method_name='editReleaseStatusEffectivity',
            library='StructureManagement',
            service_date='2015_10',
            service_name='Effectivity',
            params={'input': input},
            response_cls=ServiceData,
        )
