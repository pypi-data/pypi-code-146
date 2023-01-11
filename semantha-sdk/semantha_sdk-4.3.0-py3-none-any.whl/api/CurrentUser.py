from __future__ import annotations

from semantha_sdk.api import SemanthaAPIEndpoint
from semantha_sdk.model.UserData import UserData


class CurrentUser(SemanthaAPIEndpoint):
    """ Access information about the currently logged-in user. """

    @property
    def _endpoint(self):
        return self._parent_endpoint + "/currentuser"

    def get_user_data(self) -> UserData:
        return self._session.get(self._endpoint).execute().to(UserData)

    def get_user_roles(self) -> list[str]:
        return self._session.get(self._endpoint + "/roles").execute().as_list()
