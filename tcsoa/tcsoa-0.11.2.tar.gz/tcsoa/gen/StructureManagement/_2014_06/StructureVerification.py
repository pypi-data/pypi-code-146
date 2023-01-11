from __future__ import annotations

from tcsoa.gen.StructureManagement._2012_02.StructureVerification import ACInput
from tcsoa.gen.BusinessObjects import Dataset
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ACFavoriteInfo(TcBaseObj):
    """
    Accountability check settings which can be used to run accountability check or to load the settings in the
    accountability check dialog. The following partial errors may be returned in ServiceData element.
        204045        Input dataset UID is not a valid dataset of accountability check favorite.
        204047        The accountability check favorites XML is invalid. It may contain the entries that               
         cannot be evaluated by XML parser.
    
    
    :var accSettings: Accountability check settings.
    :var serviceData: Teamcenter service data.
    """
    accSettings: ACInput = None
    serviceData: ServiceData = None


@dataclass
class ACFavoritesInput(TcBaseObj):
    """
    The required parameters for the manageACFavorites method.
    
    :var accSettings: Accountability check settings to save. May have empty values for update and delete actions.
    :var name: Name of the dataset containing accountability check settings of the favorite.  May have empty string for
    update and delete actions.
    :var description: Description of the favorite that is being created or updated. May have empty string for update
    and delete actions.
    :var datasetUID: UID of the dataset to be updated or deleted . If the value is empty a new dataset is created. 
    :var action: Specifies the action to be performed on the dataset. Possible values are "create", "update" or
    "delete".
    """
    accSettings: ACInput = None
    name: str = ''
    description: str = ''
    datasetUID: str = ''
    action: str = ''


@dataclass
class ACFavoritesResponse(TcBaseObj):
    """
    The created or updated DataSet. The following partial errors may be returned:
        204042        Input dataset uid is not a valid dataset to update the accountability check favorites.
        204043        No transient volume directory, cannot create favorites xml file.
        204044        Invalid accountability check favorites xml.
        204045        Dataset missing named reference file.
        204046        Parser unable to parse xml named reference file.
        204047        Dataset is not text type.
    
    
    :var dataset: Dataset containing the accountability check settings.
    :var serviceData: Teamcenter service data.
    """
    dataset: Dataset = None
    serviceData: ServiceData = None
