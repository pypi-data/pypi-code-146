from __future__ import annotations

from tcsoa.gen.Internal.StructureManagement._2014_12.BrokenLinks import BrokenLinkReplacementResponse, BrokenLinkSearchInput
from tcsoa.gen.Internal.StructureManagement._2014_12.StructureVerification import GetPropPropagationStatusDetailsResp, ImpactedLinesCriteria, GetStructureChangeDetailsResponse, StructureChangeDetailsElement, CreateOrUpdatePropagationDetailsResp, CreateOrUpdateReviewStatusResponse, FindReviewStatusResponse, GetPropPropagationStatusDetailsIn, GetStructureChangeImpactedLinesResponse, CreateOrUpdatePropagationDetailsIn, CreateOrUpdateReviewStatusIn, FindReviewStatusIn
from typing import List
from tcsoa.gen.Internal.StructureManagement._2014_12.Restructure import ReplaceItemsParameter
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureVerificationService(TcService):

    @classmethod
    def getPropertyPropagationStatusDetails(cls, input: List[GetPropPropagationStatusDetailsIn]) -> GetPropPropagationStatusDetailsResp:
        """
        This method is used where there are a set of lines that have property changes associated with them and a set of
        target lines where these property changes might be propagated to.  The method takes in these two sets of lines
        and the property changes.  The method will return the current values of the properties for all the lines and
        the current propagation status for each of the property changes.
        In the context of Change Tracker, this operation will be called when a user selects an impacted line in the
        impacted panel showing property changes.  Change Tracker is a  feature in Manufacturing Process Planner for
        finding and managing changes to structures.
        
        """
        return cls.execute_soa_method(
            method_name='getPropertyPropagationStatusDetails',
            library='Internal-StructureManagement',
            service_date='2014_12',
            service_name='StructureVerification',
            params={'input': input},
            response_cls=GetPropPropagationStatusDetailsResp,
        )

    @classmethod
    def getStructureChangeDetails(cls, detailsElements: List[StructureChangeDetailsElement]) -> GetStructureChangeDetailsResponse:
        """
        This operation gets detailed information about a changed value on the input line.  The types of changes tracked
        are changes performed under incremental change, revision effecitivity, occurrence effectivity or a given time
        period.  Currently the method only supports changes performed under incremental change.  The input argument is
        the line that changed, the value that changed and configuration information on how to find that line in a
        different configuration.  The operation returns the changed value of that line in the other specified
        configuration.
        """
        return cls.execute_soa_method(
            method_name='getStructureChangeDetails',
            library='Internal-StructureManagement',
            service_date='2014_12',
            service_name='StructureVerification',
            params={'detailsElements': detailsElements},
            response_cls=GetStructureChangeDetailsResponse,
        )

    @classmethod
    def getStructureChangeImpactedLines(cls, impactedLinesCriteria: List[ImpactedLinesCriteria]) -> GetStructureChangeImpactedLinesResponse:
        """
        This operation finds impacted lines in the target structure that are affected by changes made in the source
        structure.   The type of changes made in the source structure that are supported are the following:
        
        - Incremental changes
        - Revision effectivity changes
        - Occurrence effectivity changes
        - Time period changes
        
        
        
        The operation returns a list of impacted lines and affected values.
        """
        return cls.execute_soa_method(
            method_name='getStructureChangeImpactedLines',
            library='Internal-StructureManagement',
            service_date='2014_12',
            service_name='StructureVerification',
            params={'impactedLinesCriteria': impactedLinesCriteria},
            response_cls=GetStructureChangeImpactedLinesResponse,
        )

    @classmethod
    def createOrUpdatePropagationDetails(cls, input: List[CreateOrUpdatePropagationDetailsIn]) -> CreateOrUpdatePropagationDetailsResp:
        """
        This method is needed in situations where there is a source structure and a target structure and some
        equivalent lines between the two structures.  This operation sets or updates the propagation status for a given
        set of target lines.  The actual target lines are determined by the scope and search parameters passed as
        inputs to the method. In the context of Change Tracker, it is called every time when the user changes the
        Review Status value of an impacted line.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdatePropagationDetails',
            library='Internal-StructureManagement',
            service_date='2014_12',
            service_name='StructureVerification',
            params={'input': input},
            response_cls=CreateOrUpdatePropagationDetailsResp,
        )

    @classmethod
    def createOrUpdateReviewStatus(cls, input: List[CreateOrUpdateReviewStatusIn]) -> CreateOrUpdateReviewStatusResponse:
        """
        This operation sets summary review status for the changes happened on the BOMLine objects in the source
        structure. This summary review status indicate if the selected scopes in the impacted target structure have
        been processed and how they are processed.
        
        Use cases:
        This operation is needed in situations where there is a source structure and impacted target structure and the
        user needs to set the summary review status associated with specified target scopes. In the context of the
        Change Tracker tool in Manufacturing Process Planner,  it is called every time impacted target scope is set or
        changed, to display the summary review status of each change.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateReviewStatus',
            library='Internal-StructureManagement',
            service_date='2014_12',
            service_name='StructureVerification',
            params={'input': input},
            response_cls=CreateOrUpdateReviewStatusResponse,
        )

    @classmethod
    def findReviewStatus(cls, input: List[FindReviewStatusIn]) -> FindReviewStatusResponse:
        """
        This operation takes as input the BOMLine objects in a source structure having changes, and returns summary
        review status objects for currently selected target structure scopes that these changes may have impact on.
        
        Use cases:
        This operation is needed in situations where there is a source structure and impacted target structure, and the
        user needs to find the summary review status associated with specified target scopes. In the context of the
        Change Tracker tool in Manufacturing Process Planner,  it is called every time the impacted target scope is set
        or changed, to display the summary review status of each change.
        """
        return cls.execute_soa_method(
            method_name='findReviewStatus',
            library='Internal-StructureManagement',
            service_date='2014_12',
            service_name='StructureVerification',
            params={'input': input},
            response_cls=FindReviewStatusResponse,
        )


class RestructureService(TcService):

    @classmethod
    def replaceItems(cls, replaceInputs: List[ReplaceItemsParameter]) -> ServiceData:
        """
        Replaces an ItemRevision representing a node in the structure with replacement ItemRevision based on the given
        option. The options are
        - Only the selected    Replaces a single selected BOMLine.
        - All sibling occurrences of the selected in the parent assembly. Replaces all BOMLines in the immediate parent
        assembly, referencing the same ItemRevision.
        - All occurrences of the selected in the whole structure. Replaces all BOMLines in the entire structure,
        referencing the same ItemRevision.
        
        
        
        The following restrictions apply to this operation:
        - The preference PS_replace_with_substructure is applied
        - If the selected line has substitutes, the operation will fail.
        - If the selected line or its parent is linked to variant Item the operation will fail.
        - If it is a variant ItemRevision, the ItemRevision to replace it should be a matching variant ItemRevision.
        
        
        
        Note:
        The operation only supports Item objects. Objects of GeneralDesignElement are not supported.
        
        Use cases:
        1. Replace all occurrences in the structure:
        A user wants to replace all occurrences of a ItemRevision in a structure. The user calls the operation with the
        selected BOMLine and replacement ItemRevision. All the occurrences for the ItemRevision in the structure will
        be replaced with the replacement ItemRevision.
        
        2. Replace all occurrences in the structure with partial errors:
        A user wants to replace all occurrences of an ItemRevision in a structure. BOMView Revision of some of the
        occurrences are released. The user calls the operation with selected BOMLine and replacement ItemRevision. The
        occurrences of an ItemRevision whose BOMView Revision is released will fail to be replaced but the other
        ItemRevisions will be replaced. All the failures will be reported to the user for any further action.
        
        3. Replace sibling occurrences:
        A user wants to replace all sibling occurrences of a ItemRevision in the immediate parent assembly. The user
        calls the operation with the ItemRevision and replacement ItemRevision. All the sibling occurrences of the
        ItemRevision in the immediate parent assembly will be replaced with the replacement ItemRevision.
        """
        return cls.execute_soa_method(
            method_name='replaceItems',
            library='Internal-StructureManagement',
            service_date='2014_12',
            service_name='Restructure',
            params={'replaceInputs': replaceInputs},
            response_cls=ServiceData,
        )


class BrokenLinksService(TcService):

    @classmethod
    def getBrokenLinkAndReplacements(cls, brokenLinkInput: BrokenLinkSearchInput) -> BrokenLinkReplacementResponse:
        """
        This service operation finds the broken links in a Bill Of Process (BOP) and searches for replacement
        candidates in the given product structure. The search is based on the specified criteria. 
        This service optionally repairs the broken links if it finds a single replacement candidate.
        
        
        Use cases:
        User has some part consumption in a BOP and accidently some of the parts are removed or replaced from the
        source product structures. This creates broken link in BOP which can be repaired through this service.
        Use Case 1: Find broken link and replacement candidates 
        Description: User can select the root of BOP and find all broken links. Additionally, replacement candidates
        from the product structure are searched based on the search criteria. The search criteria cantains property
        names, their values and whether the criterion is mandatory or optional. User can select the replacement
        candidate to repair the broken links.
        
        Use case 2 : Find broken link and replacement candidates with auto repair
        Description: User can select the option to repair the broken links automatically. This would happen when only
        one replacement candidate is found for the given search criteria.
        """
        return cls.execute_soa_method(
            method_name='getBrokenLinkAndReplacements',
            library='Internal-StructureManagement',
            service_date='2014_12',
            service_name='BrokenLinks',
            params={'brokenLinkInput': brokenLinkInput},
            response_cls=BrokenLinkReplacementResponse,
        )
