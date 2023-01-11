from __future__ import annotations

from tcsoa.gen.Core._2014_10.DataManagement import SaveAsIn, GetPasteRelationsResponse2, ChildrenInputData, GenerateIdInput, GenerateIdsResponse, DeepCopyDataInput, GetDeepCopyDataResponse
from tcsoa.gen.Core._2013_05.DataManagement import GetPasteRelationsInputData
from typing import List
from tcsoa.gen.BusinessObjects import POM_object
from tcsoa.gen.Core._2014_10.ProjectLevelSecurity import PropagateDataElement
from tcsoa.gen.Core._2012_09.DataManagement import RelateInfoIn
from tcsoa.gen.Core._2011_06.DataManagement import SaveAsObjectsResponse
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ProjectLevelSecurityService(TcService):

    @classmethod
    def propagateData(cls, propagateDataElements: List[PropagateDataElement]) -> None:
        """
        This operation can propagate  security or anyother teamcenter data based on the source object and applicable
        propagation rules. The propagateData operation should only be invoked when propagation rule is configured to
        run in background. 
        The propagation rule defined in BMIDE states what data from source to desination object has to be
        propagated.For example project_list, license_list from Item to ItemRevision.
        
         The term "security data" is an abbreviated form of any of the following methods for applying additional
        security settings on an object.
        - Assigning a Project(s) to an object
        - Removing object from a Project(s)
        - Attaching an ADA license(s) to an object
        - Detaching an ADA license(s) from an object
        - Setting any of the classification attributes:
        - o    ip_classification
        - o    itar_classification
        - < other attributes > Note that customers can add their own attributes and configure them in the BMIDE to be
        propagated along with the ip_classification, and itar_classification attributes.
        
        
        
        Use cases:
        Use Case: Propagate security data from Cpd0CollaborativeDesign to Cp0DesignElement.
        
        Propagation rule for use case :
        Source type                -- Cpd0CollaborativeDesign.
        Direction                    -- Reverse.
        Destination type        -- Cp0DesignElement.
        Operation                -- All.
        property name            -- mdl0model_object.
        Property group            -- Security group I.
        Traversal condition    -- 4GDtraversalcondition.
        Propagation condition -- 4GDpropagationcondition.
        Style                        -- Merge.
        Background                -- TRUE.
        
        Property Group for use case: 
        Property group name             -- Security group I.
        List of properties in a group -- project_list, licence_list.
        
        For this use case the propagation rule and the property group shown in the above two tables respectively are
        applicable.
        Here the values from the properties project_list and the license_list would be propagated from
        Cpd0CollaborativeDesign to Cp0DesignElement through the operation propagateData.
        
        The above use case is one data propagation example. As part of this project (023479-Project ADA propagation for
        CPD) we are adding propagation rules into 4GD and foundation template. Customers can also add more rules.
        """
        return cls.execute_soa_method(
            method_name='propagateData',
            library='Core',
            service_date='2014_10',
            service_name='ProjectLevelSecurity',
            params={'propagateDataElements': propagateDataElements},
            response_cls=None,
        )


class DataManagementService(TcService):

    @classmethod
    def pruneNamedReferences(cls, namedReferences: List[POM_object]) -> ServiceData:
        """
        This operation performs a prune operation by a given list of Dataset 'named references', per the following
        criteria
        1. Remove the input named references from their owning Dataset
        2. Delete the input 'named reference' objects
        3. Delete the owning Dataset objects which contain no' named references' after the prune operation
        4. The pruned 'named references', deleted Datasets and updated Datasets will be returned 
        """
        return cls.execute_soa_method(
            method_name='pruneNamedReferences',
            library='Core',
            service_date='2014_10',
            service_name='DataManagement',
            params={'namedReferences': namedReferences},
            response_cls=ServiceData,
        )

    @classmethod
    def addChildren(cls, inputData: List[ChildrenInputData]) -> ServiceData:
        """
        This operation adds a list of objects as children to a list of parent objects which could be related by
        relation or reference properties. If the property name is not supplied as input it will use the default
        relation property between the parent and the children given by
        <ParentTypeName>_<ChildTypeName>_default_relation.
        Please see the Preferences and Environment variables reference in the Rich client interface guide for
        information on configuring these preferences.
        
        
        Use cases:
        Add MSWord object as target attachments to EPMTask object.
        
        Use AddChildren operation and provide EPMTask as the parentObj, MSWord object as the childrenObj and
        target_attachments as the property name. Also, provide clientId value to identify this add operation.
        Here, the target_attachments property is a runtime property. The AddChildren operation internally will modify
        two properties attachments and attachment_types which are saved in the database.
        """
        return cls.execute_soa_method(
            method_name='addChildren',
            library='Core',
            service_date='2014_10',
            service_name='DataManagement',
            params={'inputData': inputData},
            response_cls=ServiceData,
        )

    @classmethod
    def removeChildren(cls, inputData: List[ChildrenInputData]) -> ServiceData:
        """
        This operation removes a list of objects as children to a list of parent objects which could be related by
        relation or reference properties. If the property name is not supplied as input it will use the default
        relation property between the parent and the children given by ParentTypeName>_ChildTypeName>_default_relation.
        Please see the Preferences and Environment variables reference in the Rich client interface guide for
        information on configuring these preferences.
        
        
        Use cases:
        Remove Item object from Folder object with contents property name.
        
        Use RemoveChildren operation and provide Folder object as the parent object, Item object as the children object
        and contents as the property name. Also, provide clientId value to identify this remove children operation. The
        RemoveChildren operation will remove Item object from the Folder parent object.
        """
        return cls.execute_soa_method(
            method_name='removeChildren',
            library='Core',
            service_date='2014_10',
            service_name='DataManagement',
            params={'inputData': inputData},
            response_cls=ServiceData,
        )

    @classmethod
    def saveAsObjectsAndRelate(cls, iVecSoaSavAsIn: List[SaveAsIn], iVecSoaRelteInfoIn: List[RelateInfoIn]) -> SaveAsObjectsResponse:
        """
        This operation performs SaveAs on the input target business object and its related objects as new instances.
        Related objects are identifed using deep copy rules. Optionally, this method relates the new object to the
        input target object or to a default folder.
        
        Use cases:
        Use Case 1:     SaveAs without relate
        Client constructs the "SaveAs" dialog for a business object using SaveAs operation descriptor. The information
        returned by that operation allows client to construct the SaveAs dialogs and DeepCopy panels for user input.
        Once the user input is received, client makes subsequent invocation to this operation  to execute SaveAs on the
        object. The method is invoked with "relate" option as false.
        New object is created using values passed in. It is not found under Home / NewStuff folder / anyother parent
        object. The new object stays dangling.
        Use Case 2:     SaveAs and relate to default folder
        Client invokes SaveAs operation as mentioned in use case 1 with "relate" as true but chooses not to specify
        target object or relation. This operation will choose a default folder and choose a default relation to be
        used. The default folder is decided based on the value set for the preference, WsoInsertNoSelectionsPref. When
        the preference value is set as 1 the default folder will be the New Stuff folder of the service user. When the
        preference value is 2 the default folder will be the Home folder of the service user.
        Newly created object is related to the default folder using default relation. For any other value of the
        preference, the relation will not be created.
        Use Case 3:     SaveAs and relate to specified target object using specified relation
        Client invokes SaveAs operation as mentioned in use case 1. The input parameter carrying the relation info has
        the boolean "relate" flag which is true, a valid target object and a property name to which the relation is to
        be created.
        After a successful creation, this operation relates the newly created object to the specified target object
        using specified relation.
        """
        return cls.execute_soa_method(
            method_name='saveAsObjectsAndRelate',
            library='Core',
            service_date='2014_10',
            service_name='DataManagement',
            params={'iVecSoaSavAsIn': iVecSoaSavAsIn, 'iVecSoaRelteInfoIn': iVecSoaRelteInfoIn},
            response_cls=SaveAsObjectsResponse,
        )

    @classmethod
    def generateIdsUsingIDGenerationRules(cls, generateIdsInputs: List[GenerateIdInput]) -> GenerateIdsResponse:
        """
        This operation generates object ids using ID Generation Rules associated with the business object's property.
        Currently only Item and its subtypes are supported. Object ids are generated using information provided in
        createInput.
        This operation should be called in case of a specific requirement where ID Generation is independent of
        creating Objects. (e.g. in case of some CAD applications where ids are created first, used in the system with
        temporary objects which can be saved at the later point of time). In most of the cases
        ''Teamcenter::Soa::Core::_2008_06::createObjects(const std::vector<CreateIn> &input')' handles id Generation
        and object creation. 
        This operation should be invoked when an ID Generation Rule is attached to a Business Object. To identify
        whether the ID Generation Rule is attached to the Business Object, check if 'fnd0IdGenerator' property points
        to the compound Create Descriptor of same Business Object.
        
        For more information on how to configure ID Generation RUles, refer to the Business Modeler IDE Guide. 
        """
        return cls.execute_soa_method(
            method_name='generateIdsUsingIDGenerationRules',
            library='Core',
            service_date='2014_10',
            service_name='DataManagement',
            params={'generateIdsInputs': generateIdsInputs},
            response_cls=GenerateIdsResponse,
        )

    @classmethod
    def getDeepCopyData(cls, deepCopyDataInput: List[DeepCopyDataInput]) -> GetDeepCopyDataResponse:
        """
        This operation returns information required to perform save-as/revise on a POM_object. 
        
        Use cases:
        Client constructs the saveas dialog for a business object using this operation. The information returned by
        this operation allows a client to construct the DeepCopy panels in save-as wizard for user input. Once the user
        input is received, client can make subsequent invocation to the DataManagement.saveAsObjectsAndRelate operation
        to execute SaveAs on the object. 
        """
        return cls.execute_soa_method(
            method_name='getDeepCopyData',
            library='Core',
            service_date='2014_10',
            service_name='DataManagement',
            params={'deepCopyDataInput': deepCopyDataInput},
            response_cls=GetDeepCopyDataResponse,
        )

    @classmethod
    def getPasteRelations2(cls, inputs: List[GetPasteRelationsInputData]) -> GetPasteRelationsResponse2:
        """
        This operation returns the paste relation names for the given parent business objects and the child business
        objects name; the expandable relations and the preferred paste relation are also indicated.
        
        """
        return cls.execute_soa_method(
            method_name='getPasteRelations2',
            library='Core',
            service_date='2014_10',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=GetPasteRelationsResponse2,
        )
