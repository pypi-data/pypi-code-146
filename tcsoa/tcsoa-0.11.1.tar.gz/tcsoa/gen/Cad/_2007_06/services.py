from __future__ import annotations

from tcsoa.gen.Cad._2007_06.StructureManagement import CreateUpdateClassicOptionsInput, DelClassicOptionsInput, DeleteVariantCondInput, GetConfiguredItemRevisionResponse, CreateOrUpdateVariantCondInput, GetConfiguredItemRevisionInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def createOrUpdateClassicOptions(cls, inputObjects: List[CreateUpdateClassicOptionsInput]) -> ServiceData:
        """
        In the Create mode this operation creates a new option(s), with given option values, and declares them against
        the given ItemRevision object. In the update mode following operations can be performed with the given option 
        - 1.    Replace the current text value for the specified index with a new string from option revision. 
        - 2.    Add a new value to the option revision. 
        - 3.    Remove an existing value from the option revision.
        
        
        
        Use cases:
        This operation will be used when user wants to create classic variant options for a given BOMLine object(s).
        This also can be used to update an Option 
        - a) adding a new value 
        - b) removing an existing value 
        - c) replace an existing value by new value.
        
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateClassicOptions',
            library='Cad',
            service_date='2007_06',
            service_name='StructureManagement',
            params={'inputObjects': inputObjects},
            response_cls=ServiceData,
        )

    @classmethod
    def createOrUpdateVariantConditions(cls, inputObjects: List[CreateOrUpdateVariantCondInput]) -> ServiceData:
        """
        This operation is to 'create' or 'update' (depending on the Operation) a variantCondition ( which is variant
        expression of type load if) for a BOMLine object.
        
        Use cases:
        This operation will be used when user wants to create a new or update an existing classic variant condition for
        a given BOMLine objects.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateVariantConditions',
            library='Cad',
            service_date='2007_06',
            service_name='StructureManagement',
            params={'inputObjects': inputObjects},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteClassicOptions(cls, inputObjects: List[DelClassicOptionsInput]) -> ServiceData:
        """
        Delete option deletes the option and all the values associated with it.
        """
        return cls.execute_soa_method(
            method_name='deleteClassicOptions',
            library='Cad',
            service_date='2007_06',
            service_name='StructureManagement',
            params={'inputObjects': inputObjects},
            response_cls=ServiceData,
        )

    @classmethod
    def deleteVariantConditions(cls, inputObjects: List[DeleteVariantCondInput]) -> ServiceData:
        """
        This service will be used to delete the variant Condition(load_if) associated with a BOMLine If the variant
        condition exists then it will be deleted.
        Failure will be with client id and error message in the ServiceData.
        """
        return cls.execute_soa_method(
            method_name='deleteVariantConditions',
            library='Cad',
            service_date='2007_06',
            service_name='StructureManagement',
            params={'inputObjects': inputObjects},
            response_cls=ServiceData,
        )

    @classmethod
    def getConfiguredItemRevision(cls, inputs: List[GetConfiguredItemRevisionInfo]) -> GetConfiguredItemRevisionResponse:
        """
        Finds the revision of the given item / item revision that is configured when the given revision rule is used to
        configure the given item / item revision.
        """
        return cls.execute_soa_method(
            method_name='getConfiguredItemRevision',
            library='Cad',
            service_date='2007_06',
            service_name='StructureManagement',
            params={'inputs': inputs},
            response_cls=GetConfiguredItemRevisionResponse,
        )
