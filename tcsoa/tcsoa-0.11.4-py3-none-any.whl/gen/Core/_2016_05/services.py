from __future__ import annotations

from tcsoa.gen.Core._2016_05.DataManagement import PropData, GenerateContextSpecificIDsResponse, OptionsMap, SetPropsAndDetectOverwriteResponse, GenerateContextIDsInput
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def resetContextID(cls, contextNames: List[str]) -> ServiceData:
        """
        This service enables the client to reset the ID for given context names. When the IDs for a context name are
        reset, ID generation will begain from beginning value.
        
        WARNING: Be advised that if a client resets the ID for a context name, it is possible that repeated IDs will be
        returned from generateContextSpecificIDs service for that context name.
        
        Use cases:
        A client has a context name for which it has generated IDs and now wants to generate the IDs for that context
        name again from the beginning. Client calls this Teamcenter service to reset the ID for this context name. The
        next time the client calls generateContextSpecificIDs for this context block of returned IDs starts from the
        beginning value 0.
        """
        return cls.execute_soa_method(
            method_name='resetContextID',
            library='Core',
            service_date='2016_05',
            service_name='DataManagement',
            params={'contextNames': contextNames},
            response_cls=ServiceData,
        )

    @classmethod
    def setPropertiesAndDetectOverwrite(cls, propData: List[PropData], options: OptionsMap) -> SetPropsAndDetectOverwriteResponse:
        """
        This operation detects the overwrite condition for the business object instances if those are modified by any
        other session concurrently and updates the remaining objects with the new property values provided.
        
        Use this operation if the overwrite detection is required to avoid any unintentional overwriting of the objects
        due to concurrent modification of the object.
        
        The overwrite condition is detected only if the preference TC_overwrite_protection is set to "true", else the
        objects will be overwritten with new property values.
        
        Overwrite condition is detected by comparing database value of a property with the old value of a property
        available with client for the object.
        
        Each client using this SOA operation must remember old values to pass to this operation for detection of
        overwrite condition in addition to new/updated values.
        
        Also see Teamcenter::Soa::Core::2010_09::setProperties and Teamcenter::Soa::Core::2007_01::setProperties
        operations.
        
        Use cases:
        1. If no options are provided, the overwrite condition is detected based on old values and database values
        comparision. Only the objects, for which overwrite condition is not detected, are saved. For other objects,
        error will be returned.
        2. If the option USE_LAST_SAVED_DATE is true, overwrite condition is detected based on last saved date in
        addition to the old and database values comparision. 
        3. When IGNORE_OVERWRITE_DETECTION is  true, no overwrite condition is detected and all objects are overwritten
        with the values provided.
        4. When CHECK_IN_CHECKED_OUT_OBJECTS is provided with value "true", the objects will be checked in after
        setting the properties of the objects. The objects which are detected for overwrite condition are not checked
        in.
        5. When ENABLE_PSE_BULLETIN_BOARD is "true", it is used to enable the generation of PSE bulletin board events.
        These events are processed through Bulletin board callback mechanism.
        6. When ERROR_MODIFYING_NOT_CHECKEDOUT_OBJECTS is "true", the objects which are not checked-out will not be
        saved and a partial error 32015 for that object will be returned.
        """
        return cls.execute_soa_method(
            method_name='setPropertiesAndDetectOverwrite',
            library='Core',
            service_date='2016_05',
            service_name='DataManagement',
            params={'propData': propData, 'options': options},
            response_cls=SetPropsAndDetectOverwriteResponse,
        )

    @classmethod
    def generateContextSpecificIDs(cls, generateContextIDsIn: List[GenerateContextIDsInput]) -> GenerateContextSpecificIDsResponse:
        """
        Generates the range of unique IDs for input context names. The number of IDs generated for each context name
        depends on the input. If for a given context name, the ID has been reset using Teamcenter service
        resetContextID, then this service generates IDs for that context from the beginning.
        ID generation will also reset when the maximum limit is met. This limit is maximum number supported on 64 bit
        machine.
        
        WARNING: IDs generated using this service  are unique within a given context name, but are not guaranteed to be
        unique in all Teamcenter contextx. Caution should be used if requesting ids for item or other Teamcenter
        objects that require unique ids. The caller may choose to validate uniqueness in the use cases. By default
        Teamcenter will not allow an object be saved if it violates defined uniqueness criteria.
        
        Use cases:
        A user has a context name for which he wants to generate IDs. The user provides the context name and the number
        for IDs to be generated to this Teamcenter service. In response the user recives a block of IDs. If the user
        again uses this service to generate additional IDs for the same context name, new IDs are generated and
        returned in the response structure. The IDs generated in two calls of this service for a given context name are
        unique unless the service resetContextID has been called for that context between the two calls to generate IDs.
        """
        return cls.execute_soa_method(
            method_name='generateContextSpecificIDs',
            library='Core',
            service_date='2016_05',
            service_name='DataManagement',
            params={'generateContextIDsIn': generateContextIDsIn},
            response_cls=GenerateContextSpecificIDsResponse,
        )
