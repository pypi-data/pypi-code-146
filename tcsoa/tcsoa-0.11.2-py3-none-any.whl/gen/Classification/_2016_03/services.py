from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Classification._2016_03.Classification import ValueConversionInput, SearchClassesExtendedResponse, ConvertValuesResponse, GetChildrenExtendedResponse
from typing import List
from tcsoa.gen.Classification._2007_01.Classification import SearchAttribute
from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def convertValues(cls, valueConversionInputs: List[ValueConversionInput]) -> ConvertValuesResponse:
        """
        This operation converts the input value using provided input and output unit.
        
        The conversion happens only when the output format represents a numerical format. For String and KeyLOV(Stxt)
        formats, no conversion will occur, and the input string will be returned as is.
        
        Use cases:
        When creating classification classes, you can define whether a class contains only metric ICOs, only nonmetric
        ICOs, or both. If the classification administrator specifies that a class can contain both, you can search for
        an object using either of the unit systems you define, and the search mechanism finds a match, regardless of
        the unit in which the object is stored. For example, if you search for a bolt with a width of 5/8th inches, the
        classification search mechanism finds a bolt that is stored with a width of 1.6 centimeters. This operation
        supplies this conversion mechanism.
        """
        return cls.execute_soa_method(
            method_name='convertValues',
            library='Classification',
            service_date='2016_03',
            service_name='Classification',
            params={'valueConversionInputs': valueConversionInputs},
            response_cls=ConvertValuesResponse,
        )

    @classmethod
    def searchClassesExtended(cls, searchCriterias: List[SearchAttribute], sortAttributes: List[int], filterForWriteAccess: bool, options: int) -> SearchClassesExtendedResponse:
        """
        Finds the classification classes based on provided search criteria and provides detailed information about
        those classes. The user can search using a search expression on attributes of the class (class ID, name, used
        attribute etc.). For example, the user shall be able to search all the classes whose name begins with a
        particular set of characters and where the class ID matches certain pattern. The order of search results can
        also be sorted on various criteria. 
        
        In comparison to 'searchForClasses' it contains extended information about the class itself and also extended
        information about its parent classes.
        
        Use cases:
        The user needs to search for classification classes using a search criterion based on various attributes of a
        class. The search criterion can be based on one or more attributes.
        """
        return cls.execute_soa_method(
            method_name='searchClassesExtended',
            library='Classification',
            service_date='2016_03',
            service_name='Classification',
            params={'searchCriterias': searchCriterias, 'sortAttributes': sortAttributes, 'filterForWriteAccess': filterForWriteAccess, 'options': options},
            response_cls=SearchClassesExtendedResponse,
        )

    @classmethod
    def getChildrenExtended(cls, classObjects: List[BusinessObject], filterForWriteAccess: bool, options: int) -> GetChildrenExtendedResponse:
        """
        Gets the detailed information about immediate children in the classification hierarchy for given group(s) or
        class(es). It also contains all detailed information about the parent classes within the hierarchy. 
        
        In comparison to 'getChildren' it contains extended information about the class itself and also extended
        information about its parent classes.
        
        Use cases:
        User wants to get the details of the class "Tools and Components" and all the classes under it, to render the
        entire hierarchy.
        """
        return cls.execute_soa_method(
            method_name='getChildrenExtended',
            library='Classification',
            service_date='2016_03',
            service_name='Classification',
            params={'classObjects': classObjects, 'filterForWriteAccess': filterForWriteAccess, 'options': options},
            response_cls=GetChildrenExtendedResponse,
        )
