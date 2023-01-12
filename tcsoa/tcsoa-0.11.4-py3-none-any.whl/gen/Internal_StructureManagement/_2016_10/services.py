from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from tcsoa.gen.Internal.StructureManagement._2016_10.Effectivity import OccEffCutbackInfo, NetEffectivityResponse, CutbackUnitEffectivityResponse
from typing import List
from tcsoa.base import TcService


class EffectivityService(TcService):

    @classmethod
    def getUnitNetOccurrenceEffectivity(cls, bomlines: List[BOMLine]) -> NetEffectivityResponse:
        """
        The operation provides the following information on a BOMLine in the given BOMWindow structure: its occurrence
        effectivity, its calculated net effectivity (which is based on its unit occurrence effectivity), and whether
        the BOMLine would configure based on this calculated net effectivity. Note it is the occurrence Effectivity
        that actually determines whether the BOMLine is configured.
        
        The net effectivity calculation is based on the intersection of a BOMLine&rsquo;s unit occurrence Effectivity
        with the unit net effectivity of its parent hierarchy. For example, given a BOMLine with a unit occurrence
        Effectivity with range of 1-10 for an end Item, a child BOMLine with unit occurrence Effectivity with a range
        of 1-100 for the same end Item, would have a unit net effectivity of 1-10 for that end Item. That is, the child
        BOMLine effectivity range is constrained by the limited range of its parent BOMLine.
        
        Use cases:
        User would like to see net effectivity information for a BOMLine within a structure.
        """
        return cls.execute_soa_method(
            method_name='getUnitNetOccurrenceEffectivity',
            library='Internal-StructureManagement',
            service_date='2016_10',
            service_name='Effectivity',
            params={'bomlines': bomlines},
            response_cls=NetEffectivityResponse,
        )

    @classmethod
    def cutbackUnitOccurrenceEffectivity(cls, occEffCutbacks: List[OccEffCutbackInfo]) -> CutbackUnitEffectivityResponse:
        """
        The operation manages unit occurrence effectivity cutback information involving  PSOccurrence children of a
        given PSBOMViewRevision. 
        
        The cutback action on unit occurrence effectivity allows a user to define PSOccurrence children within a
        specific PSBOMViewRevision which should not be effective for the same units; designating one or more
        PSOccurrence objects as "replacing" objects, and one or more sibling PSOccurrence objects as being effectively
        "replaced" by the replacing objects. With this relationship identified, the user then stipulates a desired
        effectivity for the replacing objects, and the feature automatically proposes the effectivity range adjustments
        or "cut back" that would be needed in the unit occurrence effectivity of both the replacing and the replaced
        PSOccurrence objects. 
        
        This service does not currently support the applying of the cutback proposal values to the unit occurrence
        effectivities of the identified PSOccurrence objects. The applying of the cutback proposal values is done by
        the "PS-occ-effectivity-cutback" action workflow handler.
        
        The cutback action has two steps: setup and proposal. For example, during the cutback setup, you provide
        cutback information that a PSOccurrence "PartM" with a unit occurrence Effectivity with range of 1-UP for an
        end Item is to be replaced by a sibling PSOccurrence "PartN" with unit occurrence Effectivity with a range of
        1-100 for the same end Item. In this example both PartM and PartN are effective for the units 1-100, but the
        desire is to have them be mutually exclusive. If you enter a desired unit occurrence effectivity of 50-100 for
        the end Item, the feature provides a proposal that PartN would have a unit net effectivity with range 50-100
        for the same end Item, and a proposal that PartM would have a unit net effectivity with range 1-49,101-UP for
        the same end Item.
        
        Use cases:
        View Cutbacks &ndash; you indicate the PSBOMViewRevision for which cutback information is to be obtained. The
        result is the list of related cutback objects.
        
        Setup Cutback &ndash; you indicate which PSOccurrence objects within a given PSBOMViewRevision are to be
        mutually exclusive, designating some as replacing occurrences whose unit occurrence effectivities will affect
        those on occurrences designated as replaced. You enter an effectivity range and end item to drive the cutback
        action. The result is the entered cutback information is saved, proposal effectivity ranges are generated, and
        the cutback data is returned along with proposed effectivity ranges per designated PSOccurrence.
        
        Update Cutback &ndash; you modify which PSOccurrence objects within a given PSBOMViewRevision are to be
        mutually exclusive, designating some as replacing occurrences whose unit occurrence effectivities will affect
        those on occurrences designated as replaced. You change the effectivity range and end item to drive the cutback
        action. The result is the entered cutback information is saved, proposal effectivity ranges are re-generated,
        and the cutback data is returned along with proposed effectivity ranges per designated PSOccurrence.
        
        Delete Cutback &ndash; from a  list of cutbacks for a given PSBOMViewRevision, you select an active cutback to
        delete. The result is the active cutback is deleted, along with the related proposed effectivity ranges per
        designated PSOccurrence. 
        
        Override Proposal &ndash; from a list of cutbacks for a given PSBOMViewRevision, you select an active cutback
        to view. The active cutback along with proposed effectivity ranges per designated PSOccurrence are displayed.
        You select a designated PSOccurrence and modify a proposed effectivity range. The result is the modified range
        is saved, along with re-generated proposed effectivity ranges of affected designated PSOccurrence objects.
        """
        return cls.execute_soa_method(
            method_name='cutbackUnitOccurrenceEffectivity',
            library='Internal-StructureManagement',
            service_date='2016_10',
            service_name='Effectivity',
            params={'occEffCutbacks': occEffCutbacks},
            response_cls=CutbackUnitEffectivityResponse,
        )
