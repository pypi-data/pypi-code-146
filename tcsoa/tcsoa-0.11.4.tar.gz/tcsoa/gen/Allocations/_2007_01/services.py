from __future__ import annotations

from tcsoa.gen.Allocations._2007_01.Allocation import AllocationContextInput, GetAllocationWindowResponse, AllocationLineInput, GetAllocatedBOMViewResponse, AllocationWindowInfo, AllocationLineInfo
from tcsoa.gen.BusinessObjects import BusinessObject, PSBOMView, AllocationMapRevision, RevisionRule, AllocationWindow, AllocationLine, BOMWindow, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class AllocationService(TcService):

    @classmethod
    def addAllocationLines(cls, allocWindowInput: AllocationWindow, inputAllocationLines: List[AllocationLineInfo]) -> ServiceData:
        """
        The operation is used to create new AllocationLine objects between BOMLine objects of different product
        structures. This operation needs an AllocationWindow object with an associated AllocationMapRevision object,
        for which AllocationLine will be created and a list of structure AllocationLineInfo which consists of name,
        type and reason for creation AllocationLine with from and to BOMLines from different structure. This operation
        will return created AllocationLine objects in the service data as created objects. If BOMLine is same for
        source and target, then error will be reported and stored as service data error.
        
        Use cases:
        AllocationLine is a runtime representation of an Allocation object as well as it provides runtime properties.
        It will maintain sources and targets information for Allocation. When you want traceability between different
        aspects of a product, you can use this operation to create AllocationLine objects.
        """
        return cls.execute_soa_method(
            method_name='addAllocationLines',
            library='Allocations',
            service_date='2007_01',
            service_name='Allocation',
            params={'allocWindowInput': allocWindowInput, 'inputAllocationLines': inputAllocationLines},
            response_cls=ServiceData,
        )

    @classmethod
    def closeAllocationWindow(cls, allocWindowInput: AllocationWindow, force: bool) -> ServiceData:
        """
        The operation closes the AllocationWindow and returns the unique identifier string of the AllocationWindow
        business Object in the deleted object list of ServiceData
        
        Use cases:
        Use case 1: Close Allocation Window after create 
        - Create new AllocationWindow, and adding allocations between multiple product structure and save, modify
        further and the AllocationWindow will be closed. Any unsaved Allocation changes will not be saved to Teamcenter
        before close.
        
        
        
        Use case 2: Close Allocation Window after Open
        - Open an AllocationWindow using an existing AllocationMapRevsion object. Add necessary Allocation objects,
        modify any existing Allocation objects, delete any unwanted Allocation. Save the AllocationWindow. Close the
        AllocationWindow. Any unsaved Allocation changes will not be saved to Teamcenter when the AllocationWindow
        closes.
        
        """
        return cls.execute_soa_method(
            method_name='closeAllocationWindow',
            library='Allocations',
            service_date='2007_01',
            service_name='Allocation',
            params={'allocWindowInput': allocWindowInput, 'force': force},
            response_cls=ServiceData,
        )

    @classmethod
    def modifyAllocationLines(cls, allocWindowInput: AllocationWindow, inputAllocationLines: List[AllocationLineInput]) -> ServiceData:
        """
        The operation is used to modify AllocationLine objects created between BOMLine objects of different product
        structures which are already present in an AllocationWindow. This operation needs an AllocationWindow object
        with an associated AllocationMapRevision object, for which AllocationLine will be modified for source or target
        BOMLine objects and a list of structure AllocationLineInput which consists of AllocationLine object and
        structure AllocationLineInfo. An AllocationLineInfo object information like from and to BOMLine objects are
        used for this modification purpose. This operation will return the modified AllocationLine objects in the
        service data as updated objects. If the BOMLine is the same for both source and target, then an error will be
        reported and stored as a service data error.
        
        Use cases:
        AllocationLine is a runtime representation of an Allocation object as well as it provides runtime properties.
        It will maintain source and target information for an Allocation. Use this operation to modify AllocationLine
        objects between different aspects of a product.
        """
        return cls.execute_soa_method(
            method_name='modifyAllocationLines',
            library='Allocations',
            service_date='2007_01',
            service_name='Allocation',
            params={'allocWindowInput': allocWindowInput, 'inputAllocationLines': inputAllocationLines},
            response_cls=ServiceData,
        )

    @classmethod
    def openAllocationWindow(cls, allocWindowInput: AllocationWindowInfo, icContext: BusinessObject) -> GetAllocationWindowResponse:
        """
        The operation creates an AllocationWindow for the given allocation context object. After creating the
        AllocationWindow object, the operation opens the AllocationWindow and sets the RevisionRule and the incremental
        change context on the opened AllocationWindow. The operation finds all the configured AllocationLine objects
        corresponding to the given BOMWindow objects and returns them to the user along with the AllocationWindow
        object.
        
        Use cases:
        The AllocationWindow is usually created and opened to find different allocations between two or more BOM View
        objects. For example the user wants to find various functions defined in the functional model of a product
        allocated to different ECUs in the logical model. In this case an AllocationWindow for given allocation context
        is created and opened. All the function to ECU allocations relevant to the opened functional and logical model
        for the given revision rule and incremental change context are fetched and displayed to the user in the form of
        AllocationLine objects.
        """
        return cls.execute_soa_method(
            method_name='openAllocationWindow',
            library='Allocations',
            service_date='2007_01',
            service_name='Allocation',
            params={'allocWindowInput': allocWindowInput, 'icContext': icContext},
            response_cls=GetAllocationWindowResponse,
        )

    @classmethod
    def saveAllocationWindow(cls, allocWindowInput: AllocationWindow) -> ServiceData:
        """
        Saves any modifications made in the AllocationWindow. Newly created Allocation objects will be saved to
        Teamcenter. Allocation objects which are deleted will be removed from Teamcenter. Any modification made to the
        Allocation will be updated in Teamcenter. If any new Incremental Change objects were created in this
        AllocationWindow, they will be saved to Teamcenter. If any AllocationLine objects are removed and if it is part
        of an Incremental Change object, it will be removed from Teamcenter. All changes made in the AllocationWindow
        will be saved and after save the AllocationLine objects of the AllocationWindow will be returned to the client.
        
        Use cases:
        Use case 1: Save Allocation Window after create and add allocations
        - After creation of a new AllocationWindow new AllocationLine objects can be added. After creating necessary
        allocations, the AllocationWindow is saved to save the changes to Teamcenter.
        
        
        
        Use case 2: Save Allocation Window after open and modification
        - After creation of a new AllocationWindow or opening an existing AllocationWindow, new AllocationLine objects
        can be added, existing allocations can be removed or modified for both source and target. After making
        necessary changes, the AllocationWindow is saved to save the changes to Teamcenter.
        
        """
        return cls.execute_soa_method(
            method_name='saveAllocationWindow',
            library='Allocations',
            service_date='2007_01',
            service_name='Allocation',
            params={'allocWindowInput': allocWindowInput},
            response_cls=ServiceData,
        )

    @classmethod
    def createAllocationContext(cls, input: AllocationContextInput) -> GetAllocationWindowResponse:
        """
        This operation is used to create an AllocationMap and AllocationMapRevision object  from the 
        AllocationContextInput structure. AllocationContextInput  consists of Name, id, Revision, type, list  of BOM
        (Bill of Material) Windows for which allocations has to be created. In this operation, it will create an
        AllocationMapRevision and sets it window to said context.
        
        Use cases:
        Allocation allows to map one or more BOMLine objects of two or more product structures. An AllocationMap is a
        business object that specifies how two structures are tied together by a set of allocations that exist between
        two structures. Defining such an AllocationMap needs allocation context which is carried out by this operation.
        """
        return cls.execute_soa_method(
            method_name='createAllocationContext',
            library='Allocations',
            service_date='2007_01',
            service_name='Allocation',
            params={'input': input},
            response_cls=GetAllocationWindowResponse,
        )

    @classmethod
    def deleteAllocationLines(cls, allocWindowInput: AllocationWindow, inputAllocationLines: List[AllocationLine]) -> ServiceData:
        """
        The operation is used to delete AllocationLine objects created between BOMLine objects of different product
        structures. This operation needs an AllocationWindow object with an associated AllocationMapRevision object,
        also a list of AllocationLine objects which  are going to be deleted. This operation will return deleted
        AllocationLine objects unique identifier string in the service data as deleted objects. The deletion of
        AllocationLine objects are only allowed  on a Teamcenter Master site and if this operation is attempted from a
        Replica site then an error will be reported and stored as a service data error. If the AllocationWindow has any
        Incremental Context object set, the deletion of AllocationLine will be captured in the IncrementalChange
        business object.
        
        Use cases:
        AllocationLine is a runtime representation of an Allocation object as well as it provides runtime properties.
        It will maintain source and target information for an Allocation. Use this operation to delete Allocation
        between different aspects of a product.
        """
        return cls.execute_soa_method(
            method_name='deleteAllocationLines',
            library='Allocations',
            service_date='2007_01',
            service_name='Allocation',
            params={'allocWindowInput': allocWindowInput, 'inputAllocationLines': inputAllocationLines},
            response_cls=ServiceData,
        )

    @classmethod
    def findAllocatedBOMViews(cls, bomView: PSBOMView) -> GetAllocatedBOMViewResponse:
        """
        The operation identifies all the PSBOMView BusinessObjects that are associated to the input PSBOMView Business
        Object in context of any AllocationMap object.
        
        Use cases:
        Find any BOMViews which are associated to the input BOMView for Allocation functionality
        One or more BOMViews in the Product Structure are mapped using Allocation functionality in context of the
        AllocationMap object. Allocation objects are created between the BOMLine objects of a ProductStructure. If the
        user needs to identify the PSBOMView object which has any allocations associated with the input PSBOMView , the
        operation returns such associated PSBOMView Objects.
        """
        return cls.execute_soa_method(
            method_name='findAllocatedBOMViews',
            library='Allocations',
            service_date='2007_01',
            service_name='Allocation',
            params={'bomView': bomView},
            response_cls=GetAllocatedBOMViewResponse,
        )

    @classmethod
    def findAllocationContexts(cls, bomViews: List[PSBOMView]) -> ServiceData:
        """
        The operation identifies the AllocationMap Business objects which are used as context for the given input
        PSBOMView Business objects.
        
        Use cases:
        Find AllocationMap objects which are used as context for input PSBOMView objects for Allocation functionality
        Two or more PSBOMView of Product Structure are mapped using Allocation functionality in context of
        AllocationMapRevision object. Allocation objects are created between the BOMLine objects of ProductStructure.
        If user needs to identify for a given list of PSBOMView objects what are all the AllocationMap Business Objects
        which are used as context, the operation returns such AllocationMapRevision Objects.
        """
        return cls.execute_soa_method(
            method_name='findAllocationContexts',
            library='Allocations',
            service_date='2007_01',
            service_name='Allocation',
            params={'bomViews': bomViews},
            response_cls=ServiceData,
        )

    @classmethod
    def getBOMViews(cls, allocationContext: AllocationMapRevision) -> ServiceData:
        """
        In allocation functionality in context of an AllocationMapRevision object, allocations are created between  two
        or more product structures. This operation returns the PSBOMView objects associated to the given
        AllocationMapRevision object.
        
        Use cases:
        For the given AllocationMapRevision object, the PSBOMView objects associated to the AllocationWindow object to
        create allocations are identified and returned.
        """
        return cls.execute_soa_method(
            method_name='getBOMViews',
            library='Allocations',
            service_date='2007_01',
            service_name='Allocation',
            params={'allocationContext': allocationContext},
            response_cls=ServiceData,
        )

    @classmethod
    def changeAllocatedBOMWindows(cls, allocWindowInput: AllocationWindow, addBOMWindowList: List[BOMWindow], removeBOMWindowList: List[BOMWindow]) -> GetAllocationWindowResponse:
        """
        The operation allows modifying the BOMWindow business objects associated to the AllocationWindow while working
        with Allocation functionality. Allows user to add new BOMWindow objects to the AllocationWindow and remove any
        existing BOMWindow objects from the AllocationWindow. Once the BOMWindow objects associated are modified, the
        AllocationLine objects for the context of AllocationWindow are returned to the client. Any errors encountered
        will be returned as part of partial errors in ServiceData element.
        
        Use cases:
        To modify the BOMWindows associated to an AllocationWindow
        While working in allocation functionality, if the user wants to work with an additional product structure in
        addition to one which is opened already, or to close some unwanted product structure, the user can achieve this
        using this operation by providing the required BOMWindow business objects in addBOMWindowList and
        removeBOMWindowList.
        """
        return cls.execute_soa_method(
            method_name='changeAllocatedBOMWindows',
            library='Allocations',
            service_date='2007_01',
            service_name='Allocation',
            params={'allocWindowInput': allocWindowInput, 'addBOMWindowList': addBOMWindowList, 'removeBOMWindowList': removeBOMWindowList},
            response_cls=GetAllocationWindowResponse,
        )

    @classmethod
    def changeAllocationContext(cls, allocWindowInput: AllocationWindow, allocationContext: AllocationMapRevision, allocationRule: RevisionRule, icContext: ItemRevision) -> GetAllocationWindowResponse:
        """
        This operation is used to change the context object an AllocationMapRevision business object of the input
        AllocationWindow. This operation requires AllocationMapRevision object which user wants to set on
        AllocationWindow. This operation also sets the RevisionRule for AllocationWindow and Incremental Change object
        for the AllocationWindow.
        
        Use cases:
        Sets a new allocation context, Incremental Change context, RevisionRule for an AllocationWindow and reloads the
        allocations for the given set context.
        """
        return cls.execute_soa_method(
            method_name='changeAllocationContext',
            library='Allocations',
            service_date='2007_01',
            service_name='Allocation',
            params={'allocWindowInput': allocWindowInput, 'allocationContext': allocationContext, 'allocationRule': allocationRule, 'icContext': icContext},
            response_cls=GetAllocationWindowResponse,
        )

    @classmethod
    def changeICContext(cls, allocWindowInput: AllocationWindow, icContextRev: ItemRevision) -> ServiceData:
        """
        Sets the Incremental Change context for an AllocationWindow. Used to set a new Incremental Change context or
        remove the already set Incremental Change context set on an AllocationWindow. Once the Incremental Change is
        set, the AllocationLine objects for the context of AllocationWindow is returned to the client.
        
        Use cases:
        Use case 1:  Set a new Incremental Change Context on Allocation Window
        - Set a new Incremental Change context for the AllocationWindow. When the Incremental Change context is set on
        an AllocationWindow, the changes made to the AllocationWindow like adding a new Allocation, deleting any
        existing Allocation or modifying any Allocation will be captured in the IC context set. This Incremental Change
        context can be used later to get all the modification made for the given Incremental Change context object.
        
        
        
        Use Case 2:  Remove the Incremental Change Context set on Allocation Window
        - Remove any set Incremental Change context for the AllocationWindow. By passing an NULL input to the operation
        for Incremental Change context will unset the Incremental Change and there after any modifications made to
        AllocationWindow will not be captured incrementally.
        
        """
        return cls.execute_soa_method(
            method_name='changeICContext',
            library='Allocations',
            service_date='2007_01',
            service_name='Allocation',
            params={'allocWindowInput': allocWindowInput, 'icContextRev': icContextRev},
            response_cls=ServiceData,
        )
