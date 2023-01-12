""" 
Author:		 Muhammad Tahir Rafique
Date:		 2023-01-02 12:01:44
Project:	 File Explorer
Description: Provide function to extract usefull information of current user.
"""

from explorer.models.user_role import UserRole

class UserDataExtractor():
    def __init__(self, user) -> None:
        """This class will receive user object and get usefull information from it."""
        self._user = user
        return None

    def getInfo(self):
        """Getting volume and action information for the current user."""
        # GETTING USER ROLES
        queryset = UserRole.userroles.filter(user=self._user)

        # LOOPING THROUGH EACH QUERY
        info = {}
        for query in queryset:
            # GETTING VOLUME OBJECT
            volume = query.getVolume()

            # ADDING VOLUME INFORMATION
            info[volume.name] = {
                'active': volume.active,
                'path': volume.path
            }

            # GETTING ACTION INFORMATION
            actions = []
            for act in query.getActions().all():
                actions.append(act.name)
            info[volume.name]['actions'] = actions
        return info