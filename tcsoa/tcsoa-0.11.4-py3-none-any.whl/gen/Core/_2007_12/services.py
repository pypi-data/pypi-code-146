from __future__ import annotations

from tcsoa.gen.Core._2007_12.DataManagement import ListAlternateIdDisplayRulesInfo, ValidateAlternateIdInput, ListAlternateIdDisplayRulesResponse, GetContextAndIdentifiersResponse, ValidateAlternateIdResponse, AlternateIdentifiersInput
from tcsoa.gen.BusinessObjects import BusinessObject, IdDispRule, ImanType
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.gen.Core._2007_12.Session import StateNameValue
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def listAlternateIdDisplayRules(cls, input: ListAlternateIdDisplayRulesInfo) -> ListAlternateIdDisplayRulesResponse:
        """
        Return the current display rule. If the current user flag is set then also return the display rules for the
        current user. If a list of users is supplied, then return the display rules for the list of users; otherwise
        return the display rules for all users.
        
        Use cases:
        Return the current display rule in effect and optionally return all the display rules for the current user.
        Also return the display rules for all users or for a list of users only.
        """
        return cls.execute_soa_method(
            method_name='listAlternateIdDisplayRules',
            library='Core',
            service_date='2007_12',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ListAlternateIdDisplayRulesResponse,
        )

    @classmethod
    def createAlternateIdentifiers(cls, input: List[AlternateIdentifiersInput]) -> ServiceData:
        """
        Create new alternate identifiers. Given an 'IdContext', an 'IdentifierType' and an Item ( and optionally an
        ItemRevision ), create an Identifier object to display an option part number when the 'IdContext' is valid.
        
        Use cases:
        User has a part number for an Item that is used to track the Item. The manufacturer of the Item has a different
        part number. The sales department has another part number. The user needs to keep all 3 part numbers with the
        Item and display them at different times. The user can get a list of 'IdContext' and 'IdentifierTypes' from the
        'getContextsAndIdentifierTypes' operation. Using the 'IdContext' and 'IdentifierType', the client can create an
        Identifer for the Item and ItemRevision to be displayed when the 'IdContext' is valid.
        """
        return cls.execute_soa_method(
            method_name='createAlternateIdentifiers',
            library='Core',
            service_date='2007_12',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def validateAlternateIds(cls, inputs: List[ValidateAlternateIdInput]) -> ValidateAlternateIdResponse:
        """
        Determines if the supplied alternateIds are valid. The USER exit USER_validate_alt_id is used for validation. A
        "modified" alternate id is returned. If the alternate id supplied is valid then the modified one returned is
        the same as the one supplied. If the alternate id supplied is not valid, then the one returned is a valid one.
        
        Use cases:
        The user has an alternate id that they wish to use for an object. The alternate id is sent to this function to
        determine if the new alternate id conforms to the rules defined by the user.
        """
        return cls.execute_soa_method(
            method_name='validateAlternateIds',
            library='Core',
            service_date='2007_12',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=ValidateAlternateIdResponse,
        )

    @classmethod
    def getContextsAndIdentifierTypes(cls, typeTags: List[ImanType]) -> GetContextAndIdentifiersResponse:
        """
        Returns the context and identifier types for the supplied identifiable types.
        
        Use cases:
        A user has defined several IdContexts and Idenitfiers in preparation for creating AlternateIds. This service
        returns the current IdContext and Identifiers allowing the user to select the appropriate data for AlternateId
        creation.
        """
        return cls.execute_soa_method(
            method_name='getContextsAndIdentifierTypes',
            library='Core',
            service_date='2007_12',
            service_name='DataManagement',
            params={'typeTags': typeTags},
            response_cls=GetContextAndIdentifiersResponse,
        )


class SessionService(TcService):

    @classmethod
    def setAndEvaluateIdDisplayRule(cls, identifiableObjects: List[BusinessObject], displayRule: IdDispRule, setRuleAsCurrentInDB: bool) -> ServiceData:
        """
        Set the ID display rule for the session and optionally set it in the database.  The business objects from the
        'identifiableObjects' list are expanded using the new ID display rule and returned. The rule is applied to all
        business objects process throughout the rest of the session.
        """
        return cls.execute_soa_method(
            method_name='setAndEvaluateIdDisplayRule',
            library='Core',
            service_date='2007_12',
            service_name='Session',
            params={'identifiableObjects': identifiableObjects, 'displayRule': displayRule, 'setRuleAsCurrentInDB': setRuleAsCurrentInDB},
            response_cls=ServiceData,
        )

    @classmethod
    def setUserSessionState(cls, pairs: List[StateNameValue]) -> ServiceData:
        """
        Set the desired user session state values.  To clear a field's value, pass an empty string "" as the value.
        Failure to set a particular state value will result in a Partial Error with the clientId set to the name of the
        state property. State values can be per client session or per server session. Client session state is kept
        separate for each client application sharing the same Teamcenter server session, while server session state is
        shared with all client application sharing the Teamcenter server session. Valid keys for the session state
        pairs are:
        
        - currentChangeNotice: The UID of the ChangeNotice business object for this session (client session). This is
        deprecated from release Teamcenter 11.5.
        - refreshPOM: If true the business objects in the POM are refreshed before returning property values.  This
        ensures property data is up-to-date, but is a performance hit (client session).
        - objectPropertyPolicy: The name of the current object property policy. This can also be controlled through the
        ObjectPropertyPolicyManager in the SOA client framework  (client session).
        - maxOperationBracketTime: Time (seconds) to bracket to limit a  POM refresh (client session).
        - maxOperationBracketInactiveTime: Time (seconds) to bracket to limit a  POM refresh (client session).
        - usePolicyOnly: If true, only properties defined in the current Object Property Policy will be returned.
        Objects that are added to the updated list of the ServiceData without named properties by default are returned
        with all properties currently loaded in the POM.
        - formatProperties: If true, the display value of the property will be formatted, if there is an active
        property formatter is attached to it. If false, the display value of the property will not be formatted, even
        if there is an active property formatter attached to it.
        - currentProject: The UID of the Project object (server session).
        - workContex: The UID of the WorkContext object (server session).
        - volume: The UID of the Volume object (server session).
        - local_volume: The UID of the LocalVolume object (server session).
        - groupMember: The UID of the GroupMember object (server session).
        - currentDisplayRule: The UID of the DisplayRule object (server session).
        - currentOrganization: The UID of the Organization object (server session).
        - locationCodePref: The CAGE/Location Code preference. This value is set on the Item attribute
        'fnd0OriginalLocationCode' when Item objects are created (server session).
        - currentChangeItem: The UID of the Change Item Revision business object for this session. This functionality
        is supported from Teamcenter 11.5.
        
        """
        return cls.execute_soa_method(
            method_name='setUserSessionState',
            library='Core',
            service_date='2007_12',
            service_name='Session',
            params={'pairs': pairs},
            response_cls=ServiceData,
        )
