from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2017_11.ResourceManagement import AddMultiToolCutterResponse, DeleteMultiToolCutterResponse
from tcsoa.gen.Internal.Manufacturing._2017_11.StructureManagement import AlternativeScopeForProductInputInfo, PasteByRuleResponse, AlternativeScopeForProductResponse, PasteByRuleInfoInput
from typing import List
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def pasteByRule(cls, inputInfo: PasteByRuleInfoInput) -> PasteByRuleResponse:
        """
        This operation copies the Mfg0BvrOperation lines from a Bill of Process (BOP) structure and paste  them to a
        PlantBOP. The paste behavior is controlled via a set of preferences. This operation accepts as input a list of
        BOMLine objects of type Mfg0BvrOperation or Mfg0BvrProcess.  The input BOMLine objects are traversed using the
        closure rule specified  in the preference PasteByRuleClosureRule to collect Mfg0BvrOperation lines.  For each
        Mfg0BvrOperation a new line will be created and pasted as a child of the target Mfg0BvrStation in the PlantBOP
        . An error will be issued if the same MEOperation already exist on any MEStation. Attachments and the child
        BOMLine objects of the source Mfg0BvrOperation line  are handled according to the cloning rule specified by the
        preference PasteByRuleCloningRule.
        
        The new BOMline creation and paste behaviour are controlled via the following set of preferences:
        - MEPasteByRuleOccProperties &ndash; list of occurrence properties to align between original source line and
        new equivalent line under the target line.
        - MEPasteByRuleClosureRule &ndash; name of closure rule to use to filter the input source lines.
        - MEPasteByRuleCloningRule &ndash; the cloning rule to use when creating new target line from source line and
        attachments.
        - MEPasteByRuleDatasetWarning &ndash; a list of dataset types if present on the source line that will raise a
        warning and will not be carried over.
        
        
        
        Use cases:
        Paste Operation/Process from BOP to MEStation in PlantBOP:
        
        Let&rsquo;s assume the source and target structures as below: 
        
        BOP (Source Structure)
           Process
              Operation1 (source)
                 ConsumedLine
                 Attached Dataset
              Process1 (source)
                 Operation2
                    Attached Dataset
           
        
        PlantBOP (Target Structure)
           ProcessArea
              ProcessStation (target)
        
                                  The user sends Operation1 and Process1 as the source lines and the Process Station as
        the 
                                  target line as parameters to this operation.  The resulting structure will look like
        below:
                                  
                   PlantBOP
                                     ProcessArea
                                        ProcessStation
                 Operation1 (New)
                    ConsumedLine
                    Attached Dataset (Referenced)
              
                 Operation2 (New)
                    Attached Dataset (Referenced)
        
        New Operation1 and Operation2 lines are created and added to Process Station. Additionally, references to the
        original operations attachments are made.
        """
        return cls.execute_soa_method(
            method_name='pasteByRule',
            library='Internal-Manufacturing',
            service_date='2017_11',
            service_name='StructureManagement',
            params={'inputInfo': inputInfo},
            response_cls=PasteByRuleResponse,
        )

    @classmethod
    def createAlternativeScopeForProduct(cls, altenativeScpForProdInfo: List[AlternativeScopeForProductInputInfo]) -> AlternativeScopeForProductResponse:
        """
        This service operation creates new Fnd0MfgAlternativeScope (a sub-class of AppearanceGroup) for each input root
        node of Bill of Material (BOM) structure and establishes a relation between them.
        Additionally, this operation creates child Fnd0MfgAlternativeScope objects below the newly created
        Fnd0MfgAlternativeScope. These child objects act as containers for the information specified in the input and
        stores the input BOMLine objects under them.
        
        Use cases:
        Use Case 1 : User opens a MECollaborationContext (CC) object, select some of the scope from Bill Of Process
        (BOP) structure to create Alternative CC. On the structure information page, user selects "Partial" scope for
        the BOM structure. A new section for the "Alternative Scope" is displayed. User can also select BOMLines from
        the BOM structure to add in the "Fnd0MfgAlternativeScope".
        An Fnd0MfgAlternativeScope containing  sub scopes with the selected obejcts from BOM structure is created.
        """
        return cls.execute_soa_method(
            method_name='createAlternativeScopeForProduct',
            library='Internal-Manufacturing',
            service_date='2017_11',
            service_name='StructureManagement',
            params={'altenativeScpForProdInfo': altenativeScpForProdInfo},
            response_cls=AlternativeScopeForProductResponse,
        )


class ResourceManagementService(TcService):

    @classmethod
    def addMultiToolCutter(cls, strItemRevUID: str) -> AddMultiToolCutterResponse:
        """
        This operation creates a new multitool cutter for an existing tool item revision. The new cutter is an
        additional Classification object (ICO) that is connected to the item revision (multiple classification of an
        item revision). 
        The operation classifies the ItemRevision specified by input parameter "strItemRevUID" into the same class in
        which the ItemRevision is already classified. 
        UID for newly created ICO and cutter ID for the same will be returned in the response from this operation. This
        operation will not create an ICO if the ItemRevision revision is not classified.
        This operation will internally check if the existing tool already has multitool classification objects attached
        and calculate the next cutter ID. If the tool has no existing multitool cutters defined, the default cutter ID
        is "2" (The existing ICO is the first cutter.). Otherwise, the next available cutter number is calculated. The
        new value of the cutter ID will be written into the "Cutter ID" attribute (Attribute ID: -45041) of the newly
        created ICO. Also the shared "Multitool" attribute (Attribute ID: - 45040) value will be set to "Yes" during
        execution of this service operation.
        The attributes "Cutter ID" and "Multitool" will be available on tool assembly classes as part of the MRL 4.1
        kit.
        
        Use cases:
        Multitools are tools those have more than one cutter. For example: a multitool with two cutters could support
        turning for one edge and grooving for the other. As another example, a multitool could have three cutters all
        supporting the same turning operation type. This operation will be useful when user wants to add a cutter to an
        existing tool item revision which is classified.
        """
        return cls.execute_soa_method(
            method_name='addMultiToolCutter',
            library='Internal-Manufacturing',
            service_date='2017_11',
            service_name='ResourceManagement',
            params={'strItemRevUID': strItemRevUID},
            response_cls=AddMultiToolCutterResponse,
        )

    @classmethod
    def deleteMultiToolCutter(cls, deleteICOUID: str) -> DeleteMultiToolCutterResponse:
        """
        This operation deletes multitool cutter with given UID (specified in the input parameter deleteICOUID) for an
        ItemRevision. The multitool cutter is a  Classification object (ICO) that is connected to the ItemRevision
        (multiple classification of an ItemRevision). After a multitool cutter is deleted and the number of cutters was
        reduced to one, the shared "Multitool" attribute (Attribute ID: -45040)  value will be set to empty. The tool
        assembly is then no longer a multitool. This will imply that there is only one Classification object (ICO)
        connected to the ItemRevision.
        
        The attribute "Multitool" will be available on tool assembly classes as part of the MRL 4.1 kit.
        
        Use cases:
        Multitools are tools those have more than one cutter. For example: a multitool with two cutters could support
        turning for one edge and grooving for the other. As another example, a multitool could have three cutters all
        supporting the same turning operation type.
        This operation will be useful when user wants to delete a cutter from an existing tool ItemRevision which is
        classified.
        """
        return cls.execute_soa_method(
            method_name='deleteMultiToolCutter',
            library='Internal-Manufacturing',
            service_date='2017_11',
            service_name='ResourceManagement',
            params={'deleteICOUID': deleteICOUID},
            response_cls=DeleteMultiToolCutterResponse,
        )
