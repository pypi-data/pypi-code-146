from __future__ import annotations

from tcsoa.gen.Core._2008_03.Session import FavoritesResponse, ConnectResponse, FavoritesInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SessionService(TcService):

    @classmethod
    def connect(cls, featureKey: str, action: str) -> ConnectResponse:
        """
        Performs Teamcenter Flexlm license related operations, depending on the input parameters.
        
        The low level actions are:
        
        1.  ILM__init_module: Initializes the license module (if it has not already been initialized).
        2.  ILM__leave_module: Deallocates a license of the given module. If the user had N free licenses for this
        module, (N plus one) will be left after this call.
        3.  ILM__check_module: Checks to see if the user has bought the specified module and returns the number of
        purchased licenses.
        4.  ILM__enter_module: Allocates one license of the given module. If the user has bought N licenses for this
        module, (N minus one) will be left after this call.
        5.  ILM__exit_module: Leaves the module.
        """
        return cls.execute_soa_method(
            method_name='connect',
            library='Core',
            service_date='2008_03',
            service_name='Session',
            params={'featureKey': featureKey, 'action': action},
            response_cls=ConnectResponse,
        )

    @classmethod
    def setFavorites(cls, input: FavoritesInfo) -> ServiceData:
        """
        This operation saves new favorite containers and favorite objects for the current session user.
        
        Any partial errors encountered during this operation are returned using the 'clientID' specified by the caller.
        A service exception is thrown if an error is encountered that is not related to a specific favorite container
        or favorite object.  You can use favorites to track containers and objects you access frequently, such as
        folders, parts or forms.  For example, the Newstuff folder could be added as a container to the list of
        favorites.
        
        
        Use cases:
        User saves a container to their favorites list.
        
        For this operation, the list of all current favorites for the user and the list containing the container the
        user desires to add are supplied as input and the new container is added to the list of saved favorites in
        Teamcenter.
        
        
        Exceptions:
        >'Service Exception'    Thrown if an empty or invalid container or object input parameter is specified or the
        list of current favorites specified is no longer current.
        """
        return cls.execute_soa_method(
            method_name='setFavorites',
            library='Core',
            service_date='2008_03',
            service_name='Session',
            params={'input': input},
            response_cls=ServiceData,
        )

    @classmethod
    def getFavorites(cls) -> FavoritesResponse:
        """
        This operation retrieves the saved Favorites containers and Favorites objects for the current session user. 
        You can use Favorites to track containers and objects you access frequently, such as folders, parts or forms.
        
        If errors are encountered, partial results are returned. Partial errors are returned with client IDs reflecting
        the index value of the saved Favorite. A service exception is thrown if an error is encountered that is not
        related to a specific Favorite container or Favorite object.
        
        Any Teamcenter object that is returned as a Favorite object is added to 'ServiceData' plain objects.  For
        example, if an item exists in the list of Favorite objects, the object tag value for that item will be returned
        in the 'ServiceData' list of plain objects.
        
        
        Use cases:
        User logs in and selects their saved Favorites.
        
        The Favorites view in the client application is populated with the Favorites containers and objects returned
        from this operation.
        
        
        Exceptions:
        >'Service Exception'    Thrown if the retrieval of saved favorites fails for the current user, the favorites
        preference value is missing a field or if the favorites object for the specified ID is not found.
        """
        return cls.execute_soa_method(
            method_name='getFavorites',
            library='Core',
            service_date='2008_03',
            service_name='Session',
            params={},
            response_cls=FavoritesResponse,
        )
