from __future__ import annotations

from tcsoa.gen.Classification._2011_06.Classification import HierarchyInfoAndOptions, GetLibraryHierarchyResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def deleteChildrenInHierarchy(cls, optionsInput: List[HierarchyInfoAndOptions]) -> ServiceData:
        """
        Deletes classification class hierarchy based on the classification class identifier. All the child classes can
        be recursively deleted along with any classification views associated with those classification classes. If
        needed, the classification objects associated with classification classes & any workspace objects associated
        with the classification objects can also be deleted
        
        Use cases:
        User wants to delete a classification class hierarchy, or a part of it. User may also need to delete the
        associated data for these classes such as classification views, classification objects or workspace objects
        """
        return cls.execute_soa_method(
            method_name='deleteChildrenInHierarchy',
            library='Classification',
            service_date='2011_06',
            service_name='Classification',
            params={'optionsInput': optionsInput},
            response_cls=ServiceData,
        )

    @classmethod
    def getLibraryHierarchy(cls, libraryValues: List[str]) -> GetLibraryHierarchyResponse:
        """
        Gets the classification class details such as class ID, parent information, child count etc. for the specified
        library values criteria
        
        Use cases:
        The operation is called when the user queries to get class hierarchy information using the given library
        values.  The operation is typically used for data dictionary related functionality in classification area, and
        the library components are created using this feature in Teamcenter. Data dictionary is a central
        organizational repository for reusable components.
        
        Exceptions:
        >The operation will only throw a 'ServiceException' in cases when an error condition cannot be handled and an
        appropriate error message could not be added to the list of partial errors in 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='getLibraryHierarchy',
            library='Classification',
            service_date='2011_06',
            service_name='Classification',
            params={'libraryValues': libraryValues},
            response_cls=GetLibraryHierarchyResponse,
        )
