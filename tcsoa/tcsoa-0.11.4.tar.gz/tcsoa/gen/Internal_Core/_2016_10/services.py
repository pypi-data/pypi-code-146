from __future__ import annotations

from typing import List
from tcsoa.gen.Core._2012_09.DataManagement import RelateInfoIn
from tcsoa.gen.Internal.Core._2016_10.DataManagement import SaveAsIn, ReviseIn
from tcsoa.gen.Core._2013_05.DataManagement import ReviseObjectsResponse
from tcsoa.gen.Core._2011_06.DataManagement import SaveAsObjectsResponse
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def reviseObjectsInBulk(cls, reviseData: List[ReviseIn]) -> ReviseObjectsResponse:
        """
        This operation revises the given objects and copies or creates new objects in bulk using input property values
        and deep copy data. Deep copy processing is recursive such that relations between secondary objects, or from
        secondary objects to the revised object, are replicated during the operation based on deep copy rule
        configurations. This operation supports codeless configuration of custom properties. The following list of
        revisable types are supported for this operation:
        - Identifier and its sub-types
        - ItemRevision and its sub-types
        - Mdl0BaselineRevision and its sub-types
        - Mdl0ConditionalElement and its sub-types
        - Cpd0DesignControlElement and its sub-types
        - Ptn0Partition and its sub-types
        - Cpd0DesignModelElement and its sub-types
        - Cpd0ShapeDesignRevision and its sub-types
        - Bom0ConfigurableBomElement and its sub-types
        - Cfg0AbsConfiguratorWSO and its sub-types
        
        """
        return cls.execute_soa_method(
            method_name='reviseObjectsInBulk',
            library='Internal-Core',
            service_date='2016_10',
            service_name='DataManagement',
            params={'reviseData': reviseData},
            response_cls=ReviseObjectsResponse,
        )

    @classmethod
    def saveAsObjectsInBulkAndRelate(cls, saveAsData: List[SaveAsIn], relationInfo: List[RelateInfoIn]) -> SaveAsObjectsResponse:
        """
        This operation performs SaveAs operation in bulk on the input target business objects and its related objects
        as new instances. Related objects are identified using deep copy rules. Optionally, this operation relates the
        new object to the input target object or to a default folder and in this case the size of saveAsData and the
        size of relationInfo have to be the same. The following list of types are supported for this operation: 
        
        - ItemRevision and its sub-types
        - Mdl0BaselineRevision and its sub-types
        - Cpd0ShapeDesignRevision and its sub-types
        - Mdl0ApplicationModel and its sub-types
        - Mdl0ModelElement and its sub-types
        - Mdl0AttributeGroup and its sub-types
        - Mdl0ConditionalElement and its sub-types
        - Asp0Aspect and its sub-types
        - Mdl0ManagedAttrGroup and its sub-types
        - Cpd0DesignControlElement and its sub-types
        - Cpd0DesignFeature and its sub-types
        - Cpd0DesignModelElement and its sub-types
        - Ptn0Partition and its sub-types
        
        
        
        Use cases:
        Use Case 1: SaveAs without relate.
        - Client constructs the "SaveAs" dialog for a business object using SaveAs operation descriptor. The
        information returned by that operation allows client to construct the SaveAs dialogs and DeepCopy panels for
        user input.
        - Once the user input is received, client makes subsequent invocation to this operation to execute SaveAs on
        the object. 
        - The method is invoked with "relate" option as false. New object is created using values passed in. It is not
        found under Home / NewStuff folder / anyother parent object. The new object stays dangling.
        Use Case 2: SaveAs and relate to default folder.
        - Client invokes SaveAs operation as mentioned in use case 1 with "relate" as true but chooses not to specify
        target object or relation. 
        - This operation will choose a default folder and choose a default relation to be used. The default folder is
        decided based on the value set for the preference, WsoInsertNoSelectionsPref. 
        - When the preference value is set as 1, the default folder will be the New Stuff folder of the service user. 
        - When the preference value is 2, the default folder will be the Home folder of the service user.
        - Newly created object is related to the default folder using default relation. For any other value of the
        preference, the relation will not be created.
        Use Case 3: SaveAs and relate to specified target object using specified relation.
        - Client invokes SaveAs operation as mentioned in use case 1. The input parameter carrying the relation info
        has boolean flag "relate" which is true, a valid target object and a property name to which the relation is to
        be created.
        - After a successful creation, this operation relates the newly created object to the specified target object
        using specified relation.
        """
        return cls.execute_soa_method(
            method_name='saveAsObjectsInBulkAndRelate',
            library='Internal-Core',
            service_date='2016_10',
            service_name='DataManagement',
            params={'saveAsData': saveAsData, 'relationInfo': relationInfo},
            response_cls=SaveAsObjectsResponse,
        )
