from __future__ import annotations

from tcsoa.gen.Rdv._2008_05.ContextManagement import AddPartSolutionResponse, GetProductItemResponse, RemoveABEPartsInputInfo, ReplacePartSolutionResponse, GetRemoveABEPartsResponse, ReplacePartSolutionInputInfo, AddPartSolutionInputInfo
from typing import List
from tcsoa.base import TcService


class ContextManagementService(TcService):

    @classmethod
    def removePartsRelatedToABE(cls, inputs: List[RemoveABEPartsInputInfo]) -> GetRemoveABEPartsResponse:
        """
        Deletes all the related Part Solutions of an Architecture Breakdown Element (ABE). The links through which the
        Part solutions are related to the Architecture Breakdown Element are also removed.
        
        Use cases:
        The 'removePartsRelatedToABE' operation is called when user wants to remove all part solutions related to
        Architecture Breakdown Element and their corresponding links. The user can specify the input Architecture
        Breakdown Element and top line to which the Architecture Breakdown Element is linked using
        'RemoveABEPartsInputInfo' object.
        """
        return cls.execute_soa_method(
            method_name='removePartsRelatedToABE',
            library='Rdv',
            service_date='2008_05',
            service_name='ContextManagement',
            params={'inputs': inputs},
            response_cls=GetRemoveABEPartsResponse,
        )

    @classmethod
    def replacePartInProduct(cls, inputs: List[ReplacePartSolutionInputInfo]) -> ReplacePartSolutionResponse:
        """
        get the required Information for replace part in product
        """
        return cls.execute_soa_method(
            method_name='replacePartInProduct',
            library='Rdv',
            service_date='2008_05',
            service_name='ContextManagement',
            params={'inputs': inputs},
            response_cls=ReplacePartSolutionResponse,
        )

    @classmethod
    def addPartToProduct(cls, inputs: List[AddPartSolutionInputInfo]) -> AddPartSolutionResponse:
        """
        get the required Information for add part to product
        """
        return cls.execute_soa_method(
            method_name='addPartToProduct',
            library='Rdv',
            service_date='2008_05',
            service_name='ContextManagement',
            params={'inputs': inputs},
            response_cls=AddPartSolutionResponse,
        )

    @classmethod
    def getProductItemInfo(cls) -> GetProductItemResponse:
        """
        Returns a list of all Product Items found in the database. The following preferences can be used to define an
        object as a Product Item. 
        The preference PortalDesignContextProductItemProperties is used to specify one or more of the following
        properties to be used to define the object as Product Item. Multiple properties could be specified at the same
        time and the algorithm will check all the specified property values to be satisfied in order to deem an object
        as a Product Item.
        -     object_type
        -     object_desc
        -     owning_group
        
        
        For Example: PortalDesignContextProductItemProperties = object_type,object_desc
        The preference PortalDesignContextProductItemProperties.<property_name>  is used to specify the value to be
        checked in order to determine whether the object is a Product Item. For example:
        PortalDesignContextProductItemProperties.object_type = CORP_Vehicle
        Only an object of type Item or its sub type could be defined as a Product Item. The operation will return empty
        if any other objects are specified.
        The default values are
        PortalDesignContextProductItemProperties = object_type, object_desc
        PortalDesignContextProductItemProperties.object_type=Item
        PortalDesignContextProductItemProperties.object_desc=Product
        
        Use cases:
        The 'getProductItemInfo' operation is called when user wants to fetch all Product Items present in the database
        which are defined by setting the PortalDesignContextProductItemProperties preference.
        """
        return cls.execute_soa_method(
            method_name='getProductItemInfo',
            library='Rdv',
            service_date='2008_05',
            service_name='ContextManagement',
            params={},
            response_cls=GetProductItemResponse,
        )
