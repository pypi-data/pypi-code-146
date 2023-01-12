from __future__ import annotations

from tcsoa.gen.Core._2010_09.DataManagement import PropInfo, EventTypesResponse, SetPropertyResponse, VerifyExtensionInfo, PostEventObjectProperties, StaticTableDataResponse, VerifyExtensionResponse, CreateOrUpdateStaticTableDataResponse, PostEventResponse, EventObject, StaticTableInfo, RowData
from tcsoa.gen.BusinessObjects import Fnd0StaticTable
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getStaticTableData(cls, staticTable: Fnd0StaticTable) -> StaticTableDataResponse:
        """
        Returns a list of objects of type TableProperties which are associated with Fnd0StaticTable  object.
        Fnd0StaticTable object has an attribute fnd0StaticTableData which is an array of TableProperties objects.  Any
        failures will be returned with the input object mapped to the error message in the ServiceData list of partial
        errors.
        
        Use cases:
        This operation is used to get the data for attribute fnd0StaticTableData of Fnd0StaticTable object. Attribute
        fhd0StaticTableData is an array of TableProperties objects. When user selects Cdm0DataReqItemRevision object,
        the attribute cdm0EventsList is displayed in the summary as well as on View/Edit Properties menu in RAC. The
        attribute cdm0EventsList is Typed Reference to Fnd0StaticTable object.
        """
        return cls.execute_soa_method(
            method_name='getStaticTableData',
            library='Core',
            service_date='2010_09',
            service_name='DataManagement',
            params={'staticTable': staticTable},
            response_cls=StaticTableDataResponse,
        )

    @classmethod
    def postEvent(cls, input: List[PostEventObjectProperties], eventTypeName: str) -> PostEventResponse:
        """
        This operation will post an event for each of the Teamcenter business objects in the input list, with all the
        supplied information: 'secondaryObject', properties to be logged, and the error details. . Partial failures
        will be returned in the 'serviceData'.
        
        Use cases:
        Most events are posted by Teamcenter server logic. Use this operation to make an event known only to your
        client code recorded in Audit Manager or supported by Subscription Manager.
        Use Case1: Auditing events
        This operation helps auditing Teamcenter objects history by logging audit records when event eventTypeName
        occurs on primaryObject.
        - When site preference TC_audit_manager is set to ON and no Audit Definition exists for object type
        primaryObject and the eventTypeName, no audit records will be logged. Audit Definitions are Audit Manager
        Application configurations and can be viewed in Audit Manager Application.
        - When site preference TC_audit_manager is set to ON and Audit Definition exists for object type primaryObject
        and the eventTypeName, audit records will be logged with all the information provided in the structure
        PostEventObjectProperties
        - No audit records are written when preference TC_audit_manager is set to OFF or if the event posted is not
        defined as Auditable.
        
        
        
        Use Case2: Subscription Notifications    
        the site preference TC_subscription is set to ON , users can create subscriptions for notifications for certain
        events on Teamcenter Objects  The event posted must be described as subscribable and there should also exist an
        associated subscription object for the notification to occur.
        
        Exceptions:
        >Service Exception.
        Throws ServiceException with error message, error code, error count and severity.  Error code and message will
        be returned as per which audit or notification operation failed during processing.
        """
        return cls.execute_soa_method(
            method_name='postEvent',
            library='Core',
            service_date='2010_09',
            service_name='DataManagement',
            params={'input': input, 'eventTypeName': eventTypeName},
            response_cls=PostEventResponse,
        )

    @classmethod
    def setProperties(cls, info: List[PropInfo], options: List[str]) -> SetPropertyResponse:
        """
        This operation is provided to update Teamcenter object instances for the given name/value pairs. This operation
        works for all supported property value types. Each object need to be passed with its property name/value
        pairs.Passing options are not mandatory, empty list is allowed. When no options are provided, it just updates
        the objects as per the inputs. Alternatively you can pass following valid options to control updating the data.
        - QUERY: option is used to define the overall behavior of object properties setting from Excel Live and Word
        Live. Once this option is passed, server honours the preference value of TC_setProperties. Please see the
        Preferences and Environment Variables Reference documentation for preference TC_setProperties for more
        information.
        
        
        Note:It must be the 0th element when set as in the option list.
        - ENABLE_PSE_BULLETIN_BOARD: To enable the generation of PSE bulletin board events. These events are processed
        through Bulletin board callback mechanism. 
        
        """
        return cls.execute_soa_method(
            method_name='setProperties',
            library='Core',
            service_date='2010_09',
            service_name='DataManagement',
            params={'info': info, 'options': options},
            response_cls=SetPropertyResponse,
        )

    @classmethod
    def verifyExtension(cls, extensionInfo: List[VerifyExtensionInfo]) -> VerifyExtensionResponse:
        """
        This operation checks if an extension exists on an operation of a specific type.
        """
        return cls.execute_soa_method(
            method_name='verifyExtension',
            library='Core',
            service_date='2010_09',
            service_name='DataManagement',
            params={'extensionInfo': extensionInfo},
            response_cls=VerifyExtensionResponse,
        )

    @classmethod
    def createOrUpdateStaticTableData(cls, staticTableInfo: StaticTableInfo, rowProperties: List[RowData]) -> CreateOrUpdateStaticTableDataResponse:
        """
        This creates a new Table along with Rows or updates an existing Table with rows and their values based on input
        StaticTableInfo and created Table rows are added to the Table. ServiceData is updated with newly
        created/updated Table.
        
        Use cases:
        This operation is used to create/update the data for TableProperties objects of Fnd0StaticTable object. When
        user selects Cdm0DataReqItemRevision object, the attribute cdm0EventsList is displayed in the summary as well
        as on View/Edit Properties menu in RAC. The attribute cdm0EventsList is type referenced to Fnd0StaticTable.
        User can add the data in columns for each row of the table or adds rows to the table or deletes rows. After
        creation/updation of the table, user saves the object which invokes this SOA operation.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateStaticTableData',
            library='Core',
            service_date='2010_09',
            service_name='DataManagement',
            params={'staticTableInfo': staticTableInfo, 'rowProperties': rowProperties},
            response_cls=CreateOrUpdateStaticTableDataResponse,
        )

    @classmethod
    def getEventTypes(cls, input: List[EventObject]) -> EventTypesResponse:
        """
        The getEventTypes operation retrieves the valid Auditable and Subscribable events for each of the
        businessObject in the input 'EventObject' vector. When an event is auditable, you can audit actions on
        Teamcenter objects when that event happens on the businessObject. When an event is Subscribable, that means
        subscriptions can be created for that event. Partial failures, if any, will be returned in the serviceData.
        """
        return cls.execute_soa_method(
            method_name='getEventTypes',
            library='Core',
            service_date='2010_09',
            service_name='DataManagement',
            params={'input': input},
            response_cls=EventTypesResponse,
        )
