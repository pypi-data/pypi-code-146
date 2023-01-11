from __future__ import annotations

from tcsoa.base import TcService


class ClassificationService(TcService):

    @classmethod
    def importClassificationDefinitions(cls, fileTicket: str, dryRun: bool) -> str:
        """
        Imports the json input containing classification definitions of type Cst0ClassDefinition,
        Cst0PropertyDefinition, Cst0KeyLOVDefinition or NodeDefinition and optionally validates them.
        The SOA accepts file ticket which will be used to read the json file contents from the transient volume, which
        will further be used to create classification definitions.
        The JSON file which is to be uploaded must follow one of the following JSON schema:-
        &bull;    TC_DATA\classification\json\1.1.0\schema\ Classification_Save_ClassDefinitions_Request.schema.json
        &bull;    TC_DATA\classification\json\1.1.0\schema\ Classification_Save_KeyLOVDefinitions_Request.schema.json
        &bull;    TC_DATA\classification\json\1.1.0\schema\ Classification_Save_PropertyDefinitions_Request.schema.json
        &bull;    TC_DATA\classification\json\1.0.0\schema\ Classification_Save_NodeDefinitions_Request.schema.json
        The response will include the information such as Name and IRDI (International Registration Data Identifier) of
        classification definitions.
        
        Use cases:
        This operation could be used when user wants to perform any of the following actions -
        &bull;    Validate json file without creating classification definitions.
        &bull;    Import a json file creating classification definitions.
        """
        return cls.execute_soa_method(
            method_name='importClassificationDefinitions',
            library='ClassificationCommon',
            service_date='2020_12',
            service_name='Classification',
            params={'fileTicket': fileTicket, 'dryRun': dryRun},
            response_cls=str,
        )

    @classmethod
    def searchClassificationDefinitions(cls, jsonRequest: str) -> str:
        """
        Searches classification definitions based on criteria provided in the input. Classification definitions include
        objects such as NodeDefinition, ClassDefinition, PropertyDefinition and KeyLOVDefinition. 
        The input criteria may include parameters that specify the property name, operator and the value to use while
        performing the search. 
        The response will include the number of objects found, the number of objects returned and object information
        such as Name and IRDI (International Registration Data Identifier).
        
        Use cases:
        This operation could be used when user wants to perform any of the following actions -
        &bull;    Get detailed information for specified object IRDI
        &bull;    Get objects matching the specified Name, Namespace, ID, Revision or any other object property.
        &bull;    Get objects sorted on specified property (eg. Last Modified Date)
        &bull;    Get top-level hierarchy of classes
        &bull;    Get paged search results
        """
        return cls.execute_soa_method(
            method_name='searchClassificationDefinitions',
            library='ClassificationCommon',
            service_date='2020_12',
            service_name='Classification',
            params={'jsonRequest': jsonRequest},
            response_cls=str,
        )
