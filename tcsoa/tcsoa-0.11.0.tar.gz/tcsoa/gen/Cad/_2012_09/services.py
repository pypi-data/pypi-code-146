from __future__ import annotations

from tcsoa.gen.Cad._2007_12.DataManagement import CreateOrUpdatePartsPref
from tcsoa.gen.Cad._2008_06.DataManagement import CreateOrUpdatePartsResponse
from typing import List
from tcsoa.gen.Cad._2012_09.DataManagement import PartInfo
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def createOrUpdateParts(cls, partInput: List[PartInfo], pref: CreateOrUpdatePartsPref) -> CreateOrUpdatePartsResponse:
        """
        'CreateOrUpdateParts' allows the user to create or update a set of Items, ItemRevisions, and Datasets (CAD
        concept of a Part includes these Teamcenter objects). The service first attempts to validate the existence of
        the Item, ItemRevision, and Dataset. If the Item already exist,s but the ItemRevision does not, then a new
        initial ItemRevision is created-any existing ItemRevisions are not revised. If the Item and ItemRevision
        already exist, but the Dataset does not, then only the Dataset is created. If the Dataset exists, a new version
        will be added to the existing series. If any of the objects exist but the input attribute values that differ
        from those already set, attempts are made to update the values if possible. If no Item object reference or
        ItemRevision object references are specified then a new Item and ItemRevision and related objects will be
        created. All objects created and updated will be returned in the 'ServiceData'. All partial errors will contain
        the 'clientIDs' for all items related to the error message, i.e. if a dataset encounters an error, then the ID
        for that error will be the item client ID concatenated with the item revision id concatenated with the dataset
        client ID, all separated by semi-colons ( ; ).
        
        Use cases:
        User wants to create a new CAD Part (item, item revision, and dataset). User fills in the 'CreateOrUpdateInput'
        structure with the information for the item and item ievision.
        
        User wants to create an item and item revision with one or more datasets. Client fills in the
        'CreateOrUpdateInput' structure with the information for the item and item revision from the user. Client also
        fills in one or more 'DatasetInfos' with the information about the datasets to create from the user. Upon
        return from the service, the client will extract the 'FileTickets' from the 'DatasetOutputs' and upload the
        data files for the datasets using FMS. Once the uploads have completed, then the client will use the
        'DatasetCommitInfos' to attach the upload files to the datasets using the Core Services 'commitDatasetFiles'.
        
        User wants to modify properties on an item, item revision or dataset. Client fills in the 'CreateOrUpdateInput'
        structure with the new information for the item or item revision. Client fills in the new information in a
        'DatasetInfo' structure then invokes the service using an existing item or item revision or dataset.
        
        User wants to create or update an existing item and/or item revision with User created Form object. The client
        fills in the necessary data to create or update an item and/or item revision. The client also specifies
        'itemExtraObjectInfo' and/or 'itemRevisionExtraObjectInfo' containing the form and relation to be used to
        attach the form to another object.
        
        User wants to add objects to a dataset. This can be done as Extra Objects or using the NamedReference feature.
        The user fills in the information necessary to create or update a dataset. The user can then specify
        'ExtraObjectInfo' data for attaching forms or 'NamedReferenceObjectInfo' for other objects.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateParts',
            library='Cad',
            service_date='2012_09',
            service_name='DataManagement',
            params={'partInput': partInput, 'pref': pref},
            response_cls=CreateOrUpdatePartsResponse,
        )
