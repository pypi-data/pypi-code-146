from __future__ import annotations

from tcsoa.gen.Internal.StructureManagement._2007_12.BrokenLinks import FindAndFixInput, FindCandidatesResponse, RepairBrokenLinksParam
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class BrokenLinksService(TcService):

    @classmethod
    def repairBrokenLinks(cls, input: List[RepairBrokenLinksParam]) -> ServiceData:
        """
        Repair the broken links by linking the broken link with the candidate.
        
        Use cases:
        User has a big product structure, and many assemblies are consumed in process structure. The product structure
        is restructured, so quite some links are showing as broken. User invokes the operation
        'getBrokenLinkInfoWithFixOpt' and finds all candidates for the broken links. Some broken links have more than
        one candidates, user selects one candidate for each broken link and fixes them by invoking this operation.
        """
        return cls.execute_soa_method(
            method_name='repairBrokenLinks',
            library='Internal-StructureManagement',
            service_date='2007_12',
            service_name='BrokenLinks',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def getBrokenLinkInfoWithFixOpt(cls, input: List[FindAndFixInput]) -> FindCandidatesResponse:
        """
        For manufacturing, links are built between structures, for example, product structures and process structures.
        Sometimes, a link can be broken due to structure changes. This operation finds broken links and candidates for
        repair with fix option.
        
        1.    If broken link scope is passed in, find the broken link in the scope (quick or thorough)
        2.    If search criteria is not empty, find the candidates for the broken links
        - Most commonly used criteria is item id.
        - Property "'bl_abs_occ_id'", "'bl_usage_address'", "'bl_position_designator'" and any occurrence note will not
        require revision rule. Other property will require revision rule to find candidates.
        - Properties can be mandatory or optional for matching. All mandatory properties and at least one optional
        property should match for a line to qualify as a candidate to repair a broken link.
        
        
        3.    If automatic fix is enabled and one-to-one match is found, fix the broken links
        
        Use cases:
        - User has a linked structure, but the source is deleted by accident. User adds it back and calls the operation
        to repair the broken link by passing the broken link, the root of the product structure, and option to
        automatic fix, the broken link will be automatically fixed by using the added back line.
        - User has a big product structure, and many assemblies are consumed in process structure. The product
        structure is restructured, so quite some links are showing as broken. User invokes this operation by using the
        root links of the two structures, item id, "'bl_abs_occ_id'", "'bl_usage_address'", "'bl_position_designator'"
        as mandatory criteria and does a thorough search. It will return all candidates for the broken links. Some
        broken links have more than one candidates, user selects one candidate for each broken link and fixes them by
        invoking 'repairBrokenLinks' operation.
        
        """
        return cls.execute_soa_method(
            method_name='getBrokenLinkInfoWithFixOpt',
            library='Internal-StructureManagement',
            service_date='2007_12',
            service_name='BrokenLinks',
            params={'input': input},
            response_cls=FindCandidatesResponse,
        )
