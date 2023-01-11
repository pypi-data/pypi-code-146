from __future__ import annotations

from tcsoa.gen.Classification._2009_10.Classification import GetKeyLOVsResponse2, GetAttributesForClassesResponse2, KeyLOVDefinition2, AutoComputeAttributesMap, AutoComputeAttributesResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class ClassificationService(TcService):

    @classmethod
    def createOrUpdateKeyLOVs(cls, keyLOVsInput: List[KeyLOVDefinition2]) -> ServiceData:
        """
        The operation creates or updates  the key-LOV objects based on the input such as name, id etc., if the input ID
        matches that of an existing key-LOV, it will be updated. Else new key-LOV object will be created. A key-LOV is
        a list of values used in classification. The key-LOVs are used to define one or more values that can be set for
        classification dictionary attributes
        
        Typical format of a Key-LOV 
        
            <key-LOV ID>:<key-LOV Name>
            <Key10>:<Value10>
            <Key20>:<Value20>
        
        Example of a Key-LOV:
        
        -33381 : Design Categories
            Des1 : Bearing
            Des2 : Bracket
            Des3 : Frame
            Des4 : LeadBox
        
        
        Use cases:
        User wants to create new key-LOVs to be used with classification or need to update the existing ones in
        classification.
        
        Exceptions:
        >Throws 'ServiceException' (SOA Framework class that holds model objects and partial errors) when
        classification system fails to create or update Key-LOV values for the given Key-LOV ID
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateKeyLOVs',
            library='Classification',
            service_date='2009_10',
            service_name='Classification',
            params={'keyLOVsInput': keyLOVsInput},
            response_cls=ServiceData,
        )

    @classmethod
    def autoComputeAttributes(cls, icoId: str, wso: WorkspaceObject, classId: str, viewId: str, inputAttrs: AutoComputeAttributesMap, unitSystem: int, mode: int) -> AutoComputeAttributesResponse:
        """
        Computes the attribute values  of classification object based on other attribute values within the same object
        or an associated classification view. Or the value can be computed based on attribute values of the object
        being classified. A classification object is also called ICO.
        
        Use cases:
        User need to automatically compute classification attribute values for attributes marked as 'AutoComputed'. The
        values can be computed based on - other attribute values belonging to same classification object or an
        associated classification view or attribute values of the object being classified.
        
        Exceptions:
        >The operation will only throw a 'ServiceException' in cases when an error condition cannot be handled and an
        appropriate error message could not be added to the list of partial errors in 'ServiceData'.
        """
        return cls.execute_soa_method(
            method_name='autoComputeAttributes',
            library='Classification',
            service_date='2009_10',
            service_name='Classification',
            params={'icoId': icoId, 'wso': wso, 'classId': classId, 'viewId': viewId, 'inputAttrs': inputAttrs, 'unitSystem': unitSystem, 'mode': mode},
            response_cls=AutoComputeAttributesResponse,
        )

    @classmethod
    def getAttributesForClasses2(cls, classIds: List[str]) -> GetAttributesForClassesResponse2:
        """
        Provides information on class attributes for the classification classes based on input classification class
        ids. Detailed information about class attributes is provided & includes class attribute name, description,
        format, unit system, minimum/maximum value, configuration set & extended properties.
        
        Use cases:
        When user wants to view details of all class attributes associated with a classification class. The method is
        similar to 'getAttributesForClasses()' method, but provides information in a slightly different format. Also
        additional information like that on the extended properties of class attributes is provided
        
        Exceptions:
        >The operation will only throw a 'ServiceException' for an unknown type of exception.
        In all other cases failures will be returned with the Class ID mapped to the error message in the 'ServiceData'
        list of partial errors of the returned 'GetAttributesForClassesResponse2' structure.
        """
        return cls.execute_soa_method(
            method_name='getAttributesForClasses2',
            library='Classification',
            service_date='2009_10',
            service_name='Classification',
            params={'classIds': classIds},
            response_cls=GetAttributesForClassesResponse2,
        )

    @classmethod
    def getKeyLOVs2(cls, keyLOVIds: List[str]) -> GetKeyLOVsResponse2:
        """
        Gets the information for classification key-LOVs  based on given ID(s). Information such as key-LOV's name,
        display options, owning site, shared sites, deprecation status and key and value entries can be obtained. A
        key-LOV is a list of values used in classification. The key-LOVs are used to define one or more values that can
        be set for classification dictionary attributes
        
        Typical format of a Key-LOV -
        
            <key-LOV ID>:<key-LOV Name>
            <Key10>:<Value10>
            <Key20>:<Value20>
         
        Example of a KeyLOV:
        
        - 33381:Design Categories
            Des1:Bearing
            Des2:Bracket
            Des3:Frame
            Des4:LeadBox
        
        Use cases:
        User wants to retrieve the information for an existing key-LOV using the key-LOV's unique identifier. This
        operation is similar to 'getKeyLOVs''()'operation, but provides more detailed information about the required
        key-LOV.
        
        Exceptions:
        >The operation will only throw a 'ServiceException' for an unknown type of exception.In all other cases
        failures will be returned with the Key-LOV ID mapped to the error message in the 'ServiceData' list of partial
        errors of 'GetKeyLOVsResponse' return structure.
        """
        return cls.execute_soa_method(
            method_name='getKeyLOVs2',
            library='Classification',
            service_date='2009_10',
            service_name='Classification',
            params={'keyLOVIds': keyLOVIds},
            response_cls=GetKeyLOVsResponse2,
        )
