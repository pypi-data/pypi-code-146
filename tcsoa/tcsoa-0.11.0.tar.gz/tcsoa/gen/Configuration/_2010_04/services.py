from __future__ import annotations

from tcsoa.gen.Configuration._2010_04.SmartUiBldr import GetValuesForComponentResponse, ComponentInfo, ForTypePreferences, ListObjectsForComponentsResponse, CurrentSelectionsMap, ListForerunnersForComponentsResponse, GetPropertiesForSelectionsResponse, ListValuesForComponentsResponse, GetResultForSelectionsResponse
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SmartUiBldrService(TcService):

    @classmethod
    def getPropertiesForSelections(cls, rootComponent: ComponentInfo, forTypePref: ForTypePreferences, currentSelections: CurrentSelectionsMap, container: str) -> GetPropertiesForSelectionsResponse:
        """
        As per the given Smart Code configuration, the getPropertiesForSelections operation is used to get the Form
        properties and their corresponding values.  
        
        For example if 'Component Type' is mapped to 'user_data_1' on Item Master Form through FieldSet,
        getPropertiesForSelections method returns a map containing ( 'user_data_1', 'BA (component part)' ) as an
        entry. This map contains as many elements as the number of FieldSet entries in Smart Code configuration.
        """
        return cls.execute_soa_method(
            method_name='getPropertiesForSelections',
            library='Configuration',
            service_date='2010_04',
            service_name='SmartUiBldr',
            params={'rootComponent': rootComponent, 'forTypePref': forTypePref, 'currentSelections': currentSelections, 'container': container},
            response_cls=GetPropertiesForSelectionsResponse,
        )

    @classmethod
    def getResultForSelections(cls, rootComponent: ComponentInfo, currentSelections: CurrentSelectionsMap, alsoGetMappedProperties: bool) -> GetResultForSelectionsResponse:
        """
        The getResultForSelections operation is used to get the Smart Code for Item ID as per the given Smart Code
        configuration.
        For example for the below mentioned selections, final ItemID - 300005190 is generated using
        getResultForSelections::
        { "ITEM_COMP_TYPE","BA(Component part)", "ITEM_MACHINE_TYPE","A-Type",
         "ITEM_COUNTER_1","300005", "ITEM_DIMENSION","1",  "ITEM_DIMENSION_RW","190"   }
        """
        return cls.execute_soa_method(
            method_name='getResultForSelections',
            library='Configuration',
            service_date='2010_04',
            service_name='SmartUiBldr',
            params={'rootComponent': rootComponent, 'currentSelections': currentSelections, 'alsoGetMappedProperties': alsoGetMappedProperties},
            response_cls=GetResultForSelectionsResponse,
        )

    @classmethod
    def getValuesForComponent(cls, component: List[ComponentInfo], rootComponent: ComponentInfo, currentSelections: CurrentSelectionsMap) -> GetValuesForComponentResponse:
        """
        For a given set of user selections, getValuesForComponents returns the next available Smart Code value/string
        in the database for the given Component. 
        For Example, if previously assigned Item ID's Smart Code is -  "300010", getValuesForComponents returns
        "300011" as the next available Smart Code value for Item ID for the given component.
        """
        return cls.execute_soa_method(
            method_name='getValuesForComponent',
            library='Configuration',
            service_date='2010_04',
            service_name='SmartUiBldr',
            params={'component': component, 'rootComponent': rootComponent, 'currentSelections': currentSelections},
            response_cls=GetValuesForComponentResponse,
        )

    @classmethod
    def listForerunnersForComponents(cls, components: List[ComponentInfo], currentSelections: CurrentSelectionsMap) -> ListForerunnersForComponentsResponse:
        """
        As per the given Smart Code configuration, the listForerunnersForComponents operation is used to get all the
        components implicitly dependent on each of the given component.
        """
        return cls.execute_soa_method(
            method_name='listForerunnersForComponents',
            library='Configuration',
            service_date='2010_04',
            service_name='SmartUiBldr',
            params={'components': components, 'currentSelections': currentSelections},
            response_cls=ListForerunnersForComponentsResponse,
        )

    @classmethod
    def listObjectsForComponents(cls, compInfo: List[ComponentInfo], typePref: ForTypePreferences, currSelection: CurrentSelectionsMap) -> ListObjectsForComponentsResponse:
        """
        The listObjectsForComponents operation  is used to get the components explicitly dependent on each of the given
        components as per the Smart Code configuration set by the user.
        
        For example if we pass 'Component Type' as the input component, its explicit dependents 'Machine Type' will be
        returned as output components.
        """
        return cls.execute_soa_method(
            method_name='listObjectsForComponents',
            library='Configuration',
            service_date='2010_04',
            service_name='SmartUiBldr',
            params={'compInfo': compInfo, 'typePref': typePref, 'currSelection': currSelection},
            response_cls=ListObjectsForComponentsResponse,
        )

    @classmethod
    def listValuesForComponents(cls, compInfo: List[ComponentInfo], typePref: ForTypePreferences, currSelection: CurrentSelectionsMap) -> ListValuesForComponentsResponse:
        """
        The  listValuesForComponents operation is used to get the Smart Code values for Item IDs that each of the given
         component  can assume as per the Smart Code configuration set by the user.
        """
        return cls.execute_soa_method(
            method_name='listValuesForComponents',
            library='Configuration',
            service_date='2010_04',
            service_name='SmartUiBldr',
            params={'compInfo': compInfo, 'typePref': typePref, 'currSelection': currSelection},
            response_cls=ListValuesForComponentsResponse,
        )

    @classmethod
    def ungetValuesForComponents(cls, components: List[ComponentInfo], rootComponent: ComponentInfo, currentSelections: CurrentSelectionsMap) -> ServiceData:
        """
        The ungetValuesForComponents operation is used to undo the generated Smart Code for the Item ID if users do not
        want to proceed with the Item creation after generating the Smart Code. 
        
        For example after generating the Smart Code for Item ID, if users want to cancel Item creation,
        ungetValuesForComponents operation resets the Smart Code counters/numbers/attributes back to the earlier values
        so that these values are reusable
        """
        return cls.execute_soa_method(
            method_name='ungetValuesForComponents',
            library='Configuration',
            service_date='2010_04',
            service_name='SmartUiBldr',
            params={'components': components, 'rootComponent': rootComponent, 'currentSelections': currentSelections},
            response_cls=ServiceData,
        )
