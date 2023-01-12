from __future__ import annotations

from tcsoa.gen.Cad._2008_03.StructureManagement import AskChildPathBOMLinesResponse, AskChildPathBOMLinesInfo
from tcsoa.gen.Cad._2007_12.DataManagement import CreateOrUpdatePartsPref
from tcsoa.gen.Cad._2007_01.DataManagement import CreateOrUpdatePartsResponse
from typing import List
from tcsoa.gen.Cad._2008_03.DataManagement import PartInfo3, ResolveAttrMappingsResponse, ResolveAttrMappingsInfo
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def resolveAttrMappings(cls, info: List[ResolveAttrMappingsInfo]) -> ResolveAttrMappingsResponse:
        """
        Retrieves CAD attribute mapped properties for item revisions or datasets.  Attribute Mapping is a scheme
        whereby Teamcenter attributes can be retrieved or set via a defined path to the attribute from the starting
        object, usually a dataset.  For example, a mapped attribute can be defined in the client integration with a
        particular name ATTR1.  Using Teamcenter attribute mapping, the customizer can define a path named ATTR1 from a
        starting point item revision type or dataset type to the actual attribute that holds the value for ATTR1. The
        client integration then can access the attribute using the attribute mapping title ATTR1 and the starting point
        object.
        For more information about Attribute Mapping including examples with syntax, please consult the "Configuring
        attribute mapping section" of the Application Administration Guide in Teamcenter Online Help.
        
        Use cases:
        A user performs a File Open operation on an existing Teamcenter dataset.  The client integration has defined an
        attribute mapping in Teamcenter for that Dataset type.  The resolveAttrMappings call performed as a part of the
        File Open, sends the mapping definition, defined by the mapping title, and the Dataset as input.  The operation
        traverses from the input Dataset to the mapped property which in this case resides on the Datasets parent Item
        Revision.  The operation will return the item revision and the mapped property name such that the client
        integration can retrieve the property value from the item revision.  The value is then displayed in the
        attribute data for the dataset in the client integration.
        """
        return cls.execute_soa_method(
            method_name='resolveAttrMappings',
            library='Cad',
            service_date='2008_03',
            service_name='DataManagement',
            params={'info': info},
            response_cls=ResolveAttrMappingsResponse,
        )

    @classmethod
    def createOrUpdateParts(cls, info: List[PartInfo3], pref: CreateOrUpdatePartsPref) -> CreateOrUpdatePartsResponse:
        """
        CreateOrUpdateParts allows the user to create or update a set of parts using Items, Item Revisions, Datasets
        and ExtraObjects and also changes the ownership of the newly created object to the user/group supplied.
        If the user supplies a valid Item object reference without specifying a valid item revision object reference or
        id, then only the item will be updated.
        If the user specifies a valid item object reference with a null item revision object reference and a non-null
        revision id, then a new item revision will be created and attached to the item with no relations from the new
        item revision to the previous item revision.
        If the user specifies a valid item object reference and a valid item revision object reference, then the item
        and item revision and related objects will be updated.
        If no item object reference or item revision object references are specified then a new item and item revision
        and related objects will be created.
        All objects created and updated will be returned in the ServiceData.
        All partial errors will contain the clientIDs for all items related to the error message, i.e. if a dataset
        encounters an error, then the ID for that erro will be the item client ID concantentated with the item revision
        id contantenated with the dataset client ID, all separated by semi-colons ( ; ).
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateParts',
            library='Cad',
            service_date='2008_03',
            service_name='DataManagement',
            params={'info': info, 'pref': pref},
            response_cls=CreateOrUpdatePartsResponse,
        )


class StructureManagementService(TcService):

    @classmethod
    def askChildPathBOMLines(cls, input: List[AskChildPathBOMLinesInfo]) -> AskChildPathBOMLinesResponse:
        """
        Given one or more sets of product structure information containing child paths specified by PS Occurrence
        Thread chains, this method returns the corresponding BOM Lines.
        """
        return cls.execute_soa_method(
            method_name='askChildPathBOMLines',
            library='Cad',
            service_date='2008_03',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=AskChildPathBOMLinesResponse,
        )
