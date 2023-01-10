from __future__ import annotations

from tcsoa.gen.Cad._2007_12.DataManagement import CreateOrUpdatePartsPref
from tcsoa.gen.Cad._2008_06.DataManagement import CreateOrUpdatePartsResponse
from typing import List
from tcsoa.gen.Cad._2010_09.DataManagement import PartInfo
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def createOrUpdateParts(cls, partInput: List[PartInfo], pref: CreateOrUpdatePartsPref) -> CreateOrUpdatePartsResponse:
        """
        CreateOrUpdateParts allows the user to update or create a set of parts using Items, Item Revisions, and
        Datasets and save the boudingbox information related to these objects.
        The service first attempts to validate the existence of the Item, Item Revision, and Dataset.
        If the Item and Item Revision already exist, but the Dataset does not, then only the Dataset is created.
        If the Dataset exists, a new version will be added to the existing series.
        If any of the objects exist but the input attribute values that differ from those already set, attempts are
        made to update the values if possible.
        If the boundingbox information exists it saves that information on that particular dataset else it willnot save
        the boudingbox information.
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
            service_date='2010_09',
            service_name='DataManagement',
            params={'partInput': partInput, 'pref': pref},
            response_cls=CreateOrUpdatePartsResponse,
        )
