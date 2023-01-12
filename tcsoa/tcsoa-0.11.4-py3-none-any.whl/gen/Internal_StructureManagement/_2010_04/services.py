from __future__ import annotations

from tcsoa.gen.Internal.StructureManagement._2010_04.BOMMarkup import ApplyBOMMarkupParam, CreateBOMMarkupResponse, CreateBOMMarkupParam
from tcsoa.gen.BusinessObjects import BOMWindow
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class BOMMarkupService(TcService):

    @classmethod
    def savePendingEditsAsMarkup(cls, window: BOMWindow) -> CreateBOMMarkupResponse:
        """
        All pending edits of the specified window are persisted as Markups.
        NOTE: not implemented
        
        Use cases:
        The user must first have established a single-structure editing session in a BOMWindow, with the ability to
        create pending edits enabled. If the user wants to keep the pending edits of the current BOMWindow after the
        conclusion of this session, this method will create BOMMarkups corresponding to the pending edits and store
        them in the database.
        """
        return cls.execute_soa_method(
            method_name='savePendingEditsAsMarkup',
            library='Internal-StructureManagement',
            service_date='2010_04',
            service_name='BOMMarkup',
            params={'window': window},
            response_cls=CreateBOMMarkupResponse,
        )

    @classmethod
    def createBOMMarkup(cls, input: List[CreateBOMMarkupParam]) -> CreateBOMMarkupResponse:
        """
        Creates the Markup Change objects for the specified base structures. The Markup Changes are added to active
        Markups. This operation may create a new Markup object, if no active Markup exists, and the created new Markup
        object will be attached to the BOMViewRevision object of the BOMLine. If the line has no BOMViewRevision
        object, it will create one.
        
        Note:
        - If a line is marked as to be removed, no additional Markup Change can be created for the line.
        - If a line already has a Markup Change, the line cannot be marked for removal.
        - If a line already has a 'PROPERTY' Markup Change for exactly the same property, the old property value Markup
        Change will be overridden by the new proposed property value change.
        - If a line already has a Markup Change for replace, it cannot have another 'REPLACE' Markup Change or a
        'SUBSTITUTE' Markup Change.
        - If a line already has a Markup Change for substitute change to add a substitute or remove a substitute, the
        line cannot have a 'REPLACE' Markup Change.
        - If a line already has a Markup Change for substitute change to add a substitute or remove a substitute, the
        line cannot have another exactly the same substitute Markup Change.
        
        
        
        Use cases:
        - If user wants to create an 'ADD' Markup Change to a line, user can call the operation with the BOMLine object
        and the Item/Item Revision to be added. If user wants have initial value to find number, quantity and
        occurrence type properties for the 'ADD' Markup Changes, user will need to add property Markup Changes for
        these properties immediately after the 'ADD' Markup Change in the input of the operation. 
        - If user wants to make a Markup Change to add a substitute, user can call the operation by passing in the
        selected line, Item/Item Revision object as input object, and its BOMView object as context.
        - If user wants to make a Markup Change to change legacy variant condition, user can call the operation by
        passing the selected line,  the variant expression object of the variant condition as input object,  and
        "bl_condition_tag" as the property name to create the Markup Change object.
        
        """
        return cls.execute_soa_method(
            method_name='createBOMMarkup',
            library='Internal-StructureManagement',
            service_date='2010_04',
            service_name='BOMMarkup',
            params={'input': input},
            response_cls=CreateBOMMarkupResponse,
        )

    @classmethod
    def applyBOMMarkup(cls, input: List[ApplyBOMMarkupParam]) -> ServiceData:
        """
        This operation applies  proposed MarkupChanges that were stored in the active Markup for the specified Bill of
        Material, if the 'evaluate' flag is 'false'. If the 'evaluate' flag is 'true', the write access to perform the
        save is checked and no modification is actually attempted. The objects that the user could not modify are
        returned in the partial errors. If the 'recursive' flag is set, then all active Markups in the structure under
        the specified BOM are evaluated and/or saved. Processing continues through the structure, and all errors
        encountered are reported in the output. Applied Markup changes will be set to 'applied' status and applied
        Markup will be set to not-active status. The Markup can be tracked from the BOMViewRevision object where it is
        attached.
        
        Use cases:
        - When the structure has MarkupChanges, user may want to check if he can apply the Changes to the structure by
        invoking the operation to evaluate the write access to apply the MarkupChanges. If no write access, user may
        revise the structure or ask author of the structure to apply the MarkupChanges.
        - User who has write access to the structure after MarkupChanges are approved can invoke the operation to apply
        all MarkupChanges of the structure including substructures.
        
        """
        return cls.execute_soa_method(
            method_name='applyBOMMarkup',
            library='Internal-StructureManagement',
            service_date='2010_04',
            service_name='BOMMarkup',
            params={'input': input},
            response_cls=ServiceData,
        )
