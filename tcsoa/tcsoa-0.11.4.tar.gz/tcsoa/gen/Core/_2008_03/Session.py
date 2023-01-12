from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FavoritesContainer(TcBaseObj):
    """
    A Favorites object that contains one or more subordinate favorite containers and/or Teamcenter objects supporting a
    hierarchical favorites structure.
    
    :var clientId: The identifier that relates a set of favorites container information to reported errors.
    :var id: The container identifier that is unique for all favorites. The identifier format is four numeric
    characters with leading zeros.
    :var type: The container type.
    :var displayName: The display name used for the favorites container.
    :var parentId: The parent container identifier.  An identifier of 0000 indicates the root container.
    """
    clientId: str = ''
    id: str = ''
    type: str = ''
    displayName: str = ''
    parentId: str = ''


@dataclass
class FavoritesInfo(TcBaseObj):
    """
    Input information for setting the favorites for the session user.
    
    :var curFavorites: The client copy of the current favorites containers and objects. If current containers and
    objects are specified, they must match the current saved favorites exactly for the specified new favorites to be
    saved.  If 'curFavorites' does not match the current saved favorites in Teamcenter, 'newFavorites' will not be
    saved.  This provides the client the ability to protect against simultaneous updates by two clients.
    :var newFavorites: The new favorites containers and objects to be saved.  The containers and objects specified in
    'newFavorites' make up the entire list of favorites.  If no new containers and no new objects are specified, the
    saved favorites for the session user will be cleared.
    """
    curFavorites: FavoritesList = None
    newFavorites: FavoritesList = None


@dataclass
class FavoritesList(TcBaseObj):
    """
    A hierarchical favorites tree structure list that contains all the favorites containers and favorites objects for
    the current session user. The favorites section can be populated only if 'FavoritesSection' is passed as a key in
    the input map to this API.
    
    :var containers: List of favorite containers for the current session user.
    :var objects: List of favorite objects for the current session user.
    """
    containers: List[FavoritesContainer] = ()
    objects: List[FavoritesObject] = ()


@dataclass
class FavoritesObject(TcBaseObj):
    """
    A Teamcenter favorites object.
    
    :var clientId: The identifier that relates a set of favorites object information to reported errors.
    :var objectTag: The favorite object.
    :var displayName: The display name used for the favorites object.
    :var parentId: The parent container identifier.  An identifier of 0000 indicates the root container.
    """
    clientId: str = ''
    objectTag: BusinessObject = None
    displayName: str = ''
    parentId: str = ''


@dataclass
class FavoritesResponse(TcBaseObj):
    """
    The set of Favorites containers and Favorites objects that define a hierarchical Favorites structure for the
    current session user.
    
    :var output: List of favorite containers and favorite objects for the current session user.
    :var serviceData: The service data. This operation will populate the Service Data plain objects list with the
    Favorite containers and objects.
    """
    output: FavoritesList = None
    serviceData: ServiceData = None


@dataclass
class ConnectResponse(TcBaseObj):
    """
    Indicates number of licenses avaliable and any failure
    
    :var outputVal: The number of available licenses for the specified featureKey parameter.
    :var serviceData: The ServiceData structure contains these potential error numbers:
          214401: The initialization of the license module has failed.
          214402: Detaching the requested license has failed.
          214403: The deallocation of the license feature key has failed.
          214404: Checking of the license feature key has failed.
          214405: The allocation of the license feature key has failed.
          214406: The module is not purchased.
          214407: The passed in action is invalid.
    """
    outputVal: int = 0
    serviceData: ServiceData = None
