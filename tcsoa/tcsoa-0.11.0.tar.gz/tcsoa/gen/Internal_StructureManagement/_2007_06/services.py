from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BOMWindow, Item, BusinessObject
from tcsoa.gen.Internal.StructureManagement._2007_06.PublishByLink import CreateIDCWindowResponse
from tcsoa.gen.Internal.StructureManagement._2007_06.GlobalAlternate import GlobalAlternateResponse, PreferredGlobalAlternateInput, GlobalAlternateListInput
from tcsoa.gen.Internal.StructureManagement._2007_06.Restructure import MoveNodeParameter, SplitOccurrenceParameter, InsertLevelParameter
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class RestructureService(TcService):

    @classmethod
    def insertLevel(cls, input: List[InsertLevelParameter]) -> ServiceData:
        """
        Insert one item above the selected BOM lines, absolute occurrences, predecessor will be preserved, Incremental
        Change Element will be adjusted.
        
        Note:
        - The operation cannot be invoked in pending edit mode.
        - The selected lines should be in same BOM.
        - The operation will need to be run in incremental change context if any selected line has Incremental Change.
        - When the operation is invoked in incremental context and one of the selected line has REMOVE Incremental
        Change, the line will be skipped.
        - When the operation is invoked in incremental context and one of the selected line has ADD Incremental Change,
        the operation will fail.
        - If any selected line has any absolute occurrence, after insert level operation, the new Appearance Path Node
        of the newly created line will share the same absolute occurrence object with the Appearance Path Node of the
        original line if user has revised the structure before calling the operation.
        
        
        
        Use cases:
        - User creates a new item and adds it as new level above some packed lines by calling the operation with the
        packed lines and the newly created item. After insert level, the new lines are still packed.
        - A structure has predecessor relationship among lines, user adds a new level above some but not all of the
        lines by invoking the operation with an existing item, the item will be added as new level on the selected
        lines and the predecessor relationship will be maintained among the selected lines.
        - Selected lines have some absolute occurrences but not in current context, user invokes the
        
        """
        return cls.execute_soa_method(
            method_name='insertLevel',
            library='Internal-StructureManagement',
            service_date='2007_06',
            service_name='Restructure',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def moveNode(cls, input: List[MoveNodeParameter]) -> ServiceData:
        """
        Move pending-cut BOMLines to the selected BOMLine, absolute occurrences, predecessor relationship will be
        preserved, Incremental Change Element and modular variants data will be adjusted.
        
        Note:
        - The operation cannot be invoked in pending edit mode.
        - The operation will need to be run in incremental change context if any selected line has incremental change.
        - When the operation is invoked in incremental context and one of the selected line has REMOVE incremental
        change, the line will be skipped.
        - When the operation is invoked in incremental context and one of the selected line has ADD incremental change,
        the operation will fail.
        - Incremental Change Elements of the source line will be carried over to the new line.
        - If reference designator validation is enabled, reference designator value will be wiped out for the new lines
        if the original reference designator value is no longer valid.
        - For modular variants, if the line is moved out of context, variant condition will be invalid, the operation
        will wipe out the variant condition.
        - If any selected line has any absolute occurrence, after this operation, the new appearance path node of the
        newly created line will share the same absolute occurrence object with the Appearance Path Node of the original
        line if user has revised the structure before calling the operation.
        - If a line is moved out of the context of its absolute occurrence, the absolute occurrence will be lost.
        - When preference TC_move_to_special_case_detect is enabled, the operation will check a special case that the
        operation cannot support and will abort the operation if the case exists. The special case is that if we move a
        line which carries absolute occurrences, to a line, the occurrence thread of which line has multiple lines in
        the structure.
        
        
        
        Use cases:
        If user has the following structure
        
        Root
        +----sub0
        +----sub1
        +-------------------------leaf1 ( absocc1 in context of root)
        +-------------------------sub11
        +-------------------------leaf2(absocc2 in context of sub1)
        
        User moves leaf1 and leaf2 to sub0 to get:
        
        Root
        +----sub0
        +-------------------------leaf1 ( absocc1 in context of root)
        +-------------------------leaf2
        +----sub1
        +-------------------------sub11
        """
        return cls.execute_soa_method(
            method_name='moveNode',
            library='Internal-StructureManagement',
            service_date='2007_06',
            service_name='Restructure',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def removeLevel(cls, bomLines: List[BOMLine]) -> ServiceData:
        """
        Remove the selected BOMLines and attach the children of the removed lines to the parent of the selected lines,
        absolute occurrences, predecessor relationship will be preserved, Incremental Change Element and modular
        variants will be adjusted.
        
        Note:
        - The operation cannot be invoked in pending edit mode.
        - The operation cannot be used for root lines.
        - The operation will need to be run in incremental change context if any selected line has Incremental Change.
        - When the operation is invoked in incremental context and one of the selected line has REMOVE Incremental
        Change, the line will be skipped.
        - When the operation is invoked in incremental context and one of the selected line has ADD Incremental Change,
        the operation will fail.
        - The final quantity of the new occurrence will be the calculated based on the quantity of the selected line
        and the child.
        - AppearanceGroupBOPLine will not participate in the operation
        - If reference designator validation is enabled, reference designator value will be wiped out for the new lines.
        - Options on the selected lines will be copied to the parent and variant conditions of the selected lines and
        their children will be merged together for both modular variants and legacy variants.
        - Absolute occurrences in context of the removed lines will be lost.
        - If any selected line has any absolute occurrence, after insert level operation, the new Appearance Path Node
        of the newly created line will share the same absolute occurrence object with the Appearance Path Node of the
        original line if user has revised the structure before calling the operation.
        
        
        
        Use cases:
        If user has the following structure
        
        Root (optionRoot)
        +----toBeRemoved ( optionA, quantity=4, load if optionRoot = 1)
        +-------------------------leaf ( absocc1 in context of toBeRemoved, aboscc2 in context of root, quantity=5,
        load if optionA=A)
        
        User removes level of toBeRemoved by invoking the operation and get the following structure:
        
        Root (optionRoot, optionA)
        +---------leaf (aboscc2 in context of root, quantity=20, load if optionA=A && optionRoot=1)
        """
        return cls.execute_soa_method(
            method_name='removeLevel',
            library='Internal-StructureManagement',
            service_date='2007_06',
            service_name='Restructure',
            params={'bomLines': bomLines},
            response_cls=ServiceData,
        )

    @classmethod
    def splitOccurrence(cls, input: List[SplitOccurrenceParameter]) -> ServiceData:
        """
        Split certain quantity of occurrences from the selected BOMLines, absolute occurrences will be preserved.
        
        Note:
        - The operation cannot be invoked in pending edit mode.
        - The operation cannot be used for root lines.
        - The operation will need to be run in incremental change context if any selected line has incremental change.
        - When the operation is invoked in incremental context and one of the selected line has ADD incremental change,
        the operation will fail.
        - Objects of types specified by preference BOM_objects_excluded_from_split will not perform the operation.
        - If reference designator validation is enabled, reference designator value will be wiped out for the new lines.
        - If any selected line has any absolute occurrence, after insert level operation, the new Appearance Path Node
        of the newly created line will have a copy of the absolute occurrence object for the Appearance Path Node of
        the original line.
        - Packed lines will not be supported.
        - Quantity should be bigger than zero and less than the total of the original quantity.
        
        
        
        Use cases:
        User has a line which has absolute occurrence data, quantity for the line is 10.5, user can split the
        occurrence by quantity 0.5 by calling the operation and get two lines, one has quantity 0.5 and the other one
        has quantity 10.0, both lines will have the same absolute occurrence data.
        """
        return cls.execute_soa_method(
            method_name='splitOccurrence',
            library='Internal-StructureManagement',
            service_date='2007_06',
            service_name='Restructure',
            params={'input': input},
            response_cls=ServiceData,
        )


class GlobalAlternateService(TcService):

    @classmethod
    def listGlobalAlternates(cls, items: List[Item]) -> GlobalAlternateResponse:
        """
        This operation gets the lists of Global Alternates for the selected set of items. A global alternate is
        interchangeable with another item in all circumstances, regardless of where the other item is used in the
        product structure.
        
        Use cases:
        In order to list all the global alternates of the selected item, the user can select an item or a BOMLine in
        the product structure, and then call 'listGlobalAlternates' operation to get the global alternates for the
        selected item.
        """
        return cls.execute_soa_method(
            method_name='listGlobalAlternates',
            library='Internal-StructureManagement',
            service_date='2007_06',
            service_name='GlobalAlternate',
            params={'items': items},
            response_cls=GlobalAlternateResponse,
        )

    @classmethod
    def removeRelatedGlobalAlternates(cls, input: List[GlobalAlternateListInput]) -> GlobalAlternateResponse:
        """
        Remove selected global alternates from the list of global alternates of the selected item. A global alternate
        is interchangeable with another item in all circumstances, regardless of where the other item is used in the
        product structure.
        
        Use cases:
        In order to remove one or more global alternates from the global alternate list of the selected item, the user
        can call 'removeRelatedGlobalAlternates' operation and pass in the selected item and a list of selected global
        alternates to be removed from the list.
        """
        return cls.execute_soa_method(
            method_name='removeRelatedGlobalAlternates',
            library='Internal-StructureManagement',
            service_date='2007_06',
            service_name='GlobalAlternate',
            params={'input': input},
            response_cls=GlobalAlternateResponse,
        )

    @classmethod
    def setPreferredGlobalAlternate(cls, input: List[PreferredGlobalAlternateInput]) -> ServiceData:
        """
        Make the specified global alternate the preferred global alternate for the specified item, or remove the
        preferred designation from a global alternate for the specified item.
        
        Use cases:
        - The user calls 'setPreferredGlobalAlternates' operation to set preferred global alternate, which designates a
        nonpreffered global alternate as the preferred one.
        - The user calls 'setPreferredGlobalAlternates' operation to unset preferred global alternate, which removes
        the preffered designation from a global alternate.
        
        """
        return cls.execute_soa_method(
            method_name='setPreferredGlobalAlternate',
            library='Internal-StructureManagement',
            service_date='2007_06',
            service_name='GlobalAlternate',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def addRelatedGlobalAlternates(cls, input: List[GlobalAlternateListInput]) -> GlobalAlternateResponse:
        """
        This operation adds specified items to the list of global alternates of the selected item. A global alternate
        is interchangeable with another item in all circumstances, regardless of where the other item is used in the
        product structure.
        
        Use cases:
        In order to add one or more global alternates to the selected item, the user can call
        'addRelatedGlobalAlternates' operation and pass in the selected item and a list of items to be defined as
        global alternates of the selected item.
        """
        return cls.execute_soa_method(
            method_name='addRelatedGlobalAlternates',
            library='Internal-StructureManagement',
            service_date='2007_06',
            service_name='GlobalAlternate',
            params={'input': input},
            response_cls=GlobalAlternateResponse,
        )


class RedliningService(TcService):

    @classmethod
    def revertAllPendingEdits(cls, windows: List[BOMWindow]) -> ServiceData:
        """
        Resets those properties on all BOMLines of the specified windows that have pended edits, back to their database
        values. Also reverses the structure modifications (additions/removals) done to all BOMLines, back to pre-edited
        state. The functionality is only applicable when editing with option to mark pending edits enabled.
        
        Use cases:
        The user must first have established a single-structure editing session in a BOMWindow, with the ability to
        create pending edits enabled. If the user wants to remove all pending edits from this session, this method will
        restore the edited structure to the state that existed at the start of the session.
        """
        return cls.execute_soa_method(
            method_name='revertAllPendingEdits',
            library='Internal-StructureManagement',
            service_date='2007_06',
            service_name='Redlining',
            params={'windows': windows},
            response_cls=ServiceData,
        )

    @classmethod
    def revertPendingEdits(cls, bomLines: List[BOMLine]) -> ServiceData:
        """
        Resets those properties on the specified BOMLines that have pended edits, back to their database values. Also
        reverses the structure modifications (additions/removals) done to the specified BOMLines, back to pre-edited
        state. The functionality is only applicable when editing with option to mark pending edits enabled.
        
        Use cases:
        The user must first have established a single-structure editing session in a BOMWindow, with the ability to
        create pending edits enabled. If the user wants to remove pending edits from specific BOMLines, this method
        will restore the edited BOMLine to the status that existed at the start of the session.
        """
        return cls.execute_soa_method(
            method_name='revertPendingEdits',
            library='Internal-StructureManagement',
            service_date='2007_06',
            service_name='Redlining',
            params={'bomLines': bomLines},
            response_cls=ServiceData,
        )


class PublishByLinkService(TcService):

    @classmethod
    def createIDCWindowForDesignAsm(cls, comps: List[BusinessObject]) -> CreateIDCWindowResponse:
        """
        Creates IDCWindow for BOMLines or ItemRevisions. The BOMLine or ItemRevision is used to find Text Dataset
        attached through Rendering relation.  The IDCWindow is created with 'BOMWRITER' as context. Top BOMLine of
        BOMWindow is created with Text named reference of the Dataset.
        
        Use cases:
        Create IDWindow with PLMXML file for visualization purpose.
        """
        return cls.execute_soa_method(
            method_name='createIDCWindowForDesignAsm',
            library='Internal-StructureManagement',
            service_date='2007_06',
            service_name='PublishByLink',
            params={'comps': comps},
            response_cls=CreateIDCWindowResponse,
        )
