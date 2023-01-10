from __future__ import annotations

from tcsoa.gen.StructureManagement._2014_06.StructureVerification import ACFavoritesResponse, ACFavoriteInfo, ACFavoritesInput
from tcsoa.gen.BusinessObjects import BOMLine
from tcsoa.gen.StructureManagement._2014_06.StructureFilterWithExpand import ExpandAndSearchResponse, SearchCondition
from typing import List
from tcsoa.base import TcService


class StructureVerificationService(TcService):

    @classmethod
    def manageACFavorites(cls, input: ACFavoritesInput) -> ACFavoritesResponse:
        """
        This operation creates, updates or deletes an accountability check favorite. Internally the dataset
        representing the accountablity check favorite is created, updated or deleted.
        To create accountability check favorite, the parameters account settings, name, description and action are
        mandatory. 
        To update or delete accountability check favorite, the parameters action and datasetUID are mandatory.
        """
        return cls.execute_soa_method(
            method_name='manageACFavorites',
            library='StructureManagement',
            service_date='2014_06',
            service_name='StructureVerification',
            params={'input': input},
            response_cls=ACFavoritesResponse,
        )

    @classmethod
    def getACFavorite(cls, datasetUID: str) -> ACFavoriteInfo:
        """
        This operation returns accountability check settings for a given dataset UID of accountability check favorite.
        These settings from a favorite are usually required to populate the accountability check dialog whenever a
        favorite is loaded or when accountability check is run.
        """
        return cls.execute_soa_method(
            method_name='getACFavorite',
            library='StructureManagement',
            service_date='2014_06',
            service_name='StructureVerification',
            params={'datasetUID': datasetUID},
            response_cls=ACFavoriteInfo,
        )


class StructureFilterWithExpandService(TcService):

    @classmethod
    def expandAndSearch(cls, lines: List[BOMLine], searchConditions: List[SearchCondition]) -> ExpandAndSearchResponse:
        """
        This operation does a full expansion of the given lines, then performs the search on the expanded structure
        with the given search conditions. The lines of a structure and search criteria as BOMLine property value are
        required. This operation returns the result BOMLines with satisfied condition indexes.
        A user can search for BOMLine with multiple search criteria by separating those criteria with an "OR" operator.
        The output line contains the information about the search conditions in the form of indexes which are satisfied
        by a particular BOMLine.
        Logical operator for the first condition is ignored
        This service will support search criterias like "find no = 10 and quantity = 1 or quantity = 20 and AbsOccId =
        CFG". In this criteria "AND" has precedence over "OR" operator.
        
        Comparison are done on the basis of BOMLine property type only.
        
        Valid inputs for Date type property : A user must give input in a specific date format that is defined in
        timelocal.xml If the date format is not defined in timelocal.xml then default format will be considered as
        "dd-mmm-yyyy hh:mm" .
        Example. "01-jan-2010 12:23"
        
        Invalid inputs for Date type property :    "01-jan-201012:23", "01-january-2010 12:23", "32-jan-2010 12:23",
        "32-jan-20112 12:23"
        
        
        Valid inputs for String values : A user must give a valid string for search it should not contain spaces until
        u meant to find a string with spaces. Leading and trailing spaces will be taken care.
        Example: "validInput" , "validInput  ", "   validInput", "  validInput   "
        Invalid Input : "valid   Input"
        Note: Since Comparison is done on the basis of BOMLine property type only. There are some integer and double
        type properties which is defined as string on BOMLine so you need to pass the exact value in that case that
        will be a string comparison.
        Example : "010" and "10" will be considered as different values
        
        Valid inputs for Boolean type property : only true and false is allowed. For those properties which is shown as
        Y and N in Rich Client you should pass the value as Y and N only.
        
        Valid inputs for Double and Integer type property : A user must provide a valid value which could be parsed
        successfully to specified type.
        Example : "12334" , "234.456", "007854", "0088.675"
        Invalid Input : "345fg", "fr4567", "456.54er"
        
        Note: 1) If a condition contains a invalid inputValue than comparison for that property will be skipped.
        Results will be returned for valid values only.
        2) Equal operator(=) will be used for wild card search by default. User must not pass a wild card character('*'
        or '?') in a string value. Search will be case insensitive for all relational operators except "==" operator.
        3) Only "AND" and "OR" logical operators are supported.
        4) For integer, double and Date types "=" and "==" operators have same behavior.
        
        
        Use cases:
        Search for BOMLine with their properties - A User can search for BOMLine in a collapsed structure by giving
        criteria as their property values like "bl_item_item_id = 000016" where bl_item_item_id is a property and
        000016 is input value given by user for search. 
        Example1: A User searches for some BOMLines by giving the criteria "find no. =10 OR quantity > 1" and BOMLine1
        satisfies the condition "find no. =10" and BOMLine2 satisfies the condition "quantity > 1" then the first
        output line will contain the BOMLine1 and search condition index  as 0 and the second output line will contain
        the BOMLine2 and search condition index as 1.
        
        Example2: A User searches for some BOMLines by giving the criteria "find no = 10 and quantity > 1 or Find No =
        20 and quantity = 1" and BOMLine1 satisfies the condition "find no = 10 and quantity > 1" and BOMLine2
        satisfies the condition "Find No = 20 and quantity = 1" then the first output line will contain the BOMLine1
        and search condition index  as 0,1 and the second output line will contain the BOMLine2 and search condition
        index as 
        """
        return cls.execute_soa_method(
            method_name='expandAndSearch',
            library='StructureManagement',
            service_date='2014_06',
            service_name='StructureFilterWithExpand',
            params={'lines': lines, 'searchConditions': searchConditions},
            response_cls=ExpandAndSearchResponse,
        )
