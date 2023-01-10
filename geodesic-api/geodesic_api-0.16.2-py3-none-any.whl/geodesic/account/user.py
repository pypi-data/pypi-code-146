import re
from geodesic.bases import _APIObject
from geodesic.descriptors import _RegexDescr, _StringDescr
from geodesic.service import ServiceClient
from geodesic.client import raise_on_error
from geodesic.widgets import get_template_env, jinja_available
from typing import List
from geodesic.utils import DeferredImport

user_widget = DeferredImport('geodesic.widgets.geodesic_widgets.user_widget')

display = DeferredImport('IPython.display')


# ServiceClient for the Krampus Version 1 users API.
users_client = ServiceClient('krampus', 1, "users")

# Regex to check for valid emails.
email_re = re.compile(r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"
                      r"\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\""
                      r")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]"
                      r"|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z"
                      r"0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")

KRAMPUS_READ = 'krampus:read'
SPACETIME_READ = 'spacetime:read'
SPACETIME_WRITE = 'spacetime:write'
ENTANGLEMENT_READ = 'entanglement:read'
ENTANGLEMENT_WRITE = 'entanglement:write'
TESSERACT_READ = 'tesseract:read'
TESSERACT_WRITE = 'tesseract:write'
BOSON_READ = 'boson:read'
BOSON_WRITE = 'boson:write'
TED_WRITE = 'ted:write'

valid_permissions = [
    KRAMPUS_READ,
    SPACETIME_READ,
    SPACETIME_WRITE,
    ENTANGLEMENT_READ,
    ENTANGLEMENT_WRITE,
    TESSERACT_READ,
    TESSERACT_WRITE,
    BOSON_READ,
    BOSON_WRITE,
    TED_WRITE
]


class User(_APIObject):
    """
    The User class to represent user info and control/update profile and permissions.
    Certain functionality will be restricted to admins.

    Args:
        **info: metadata about a particular user, this can be used to create or update
        the User's profile.
    """
    _limit_setitem = [
        "subject",
        "alias",
        "first_name",
        "last_name",
        "middle_name",
        "email",
        "avatar",
        "pronouns",
        "bio"
    ]

    subject = _StringDescr(doc='the unique identifer of the subject')
    alias = _StringDescr(doc="the user's common name", default="")
    first_name = _StringDescr(doc="user's first name", default="")
    middle_name = _StringDescr(doc="user's middle name", default="")
    last_name = _StringDescr(doc="user's last name", default="")
    email = _RegexDescr(regex=email_re, empty_allowed=True, doc="user's email address", default="")
    avatar = _StringDescr(doc="publically accessible link to the user's avatar/profile pic", default="")
    pronouns = _StringDescr(doc="user's preferred personal pronouns", default="")
    bio = _StringDescr(doc="user's short bio", default="")
    org = _StringDescr(doc="user's organization")

    def __init__(self, **info) -> None:
        # client for the users API
        self._client = users_client
        super().__init__(**info)

    @property
    def roles(self) -> List[str]:
        """
        Gets and returns all of the roles for this user: admin/internal/user. Global roles
        CANNOT be set through the REST API.
        """
        res = raise_on_error(self._client.get(f'{self.subject}/roles'))
        return res.json()['roles']

    @property
    def permissions(self) -> List[str]:
        """
        Gets and returns the user's permissions as a list of strings.

        Returns:
            permissions: the user's permissions for various services.
        """
        res = raise_on_error(self._client.get(f'{self.subject}/permissions'))
        return res.json()['permissions']

    @permissions.setter
    def permissions(self, permissions: List[str]) -> None:
        """
        Sets the user's permissions on the server side.

        Args:
            permissions: a list of permission strings. Only certain permissions are valid.
        """

        for permission in permissions:
            if permission not in valid_permissions:
                raise ValueError(f"{permission} is not valid. Valid options are {valid_permissions}")

        raise_on_error(self._client.put(f'{self.subject}/permissions', permissions=permissions))

    @property
    def enabled(self) -> bool:
        """
        Checks if this user's account is currently enabled in the system. Disabled accounts can't do anything.

        Returns:
            enabled: whether or not the user's account is enabled.
        """
        res = raise_on_error(self._client.get(f'{self.subject}/naughty'))
        if res.json()['naughty']:
            return False
        return True

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        """
        Enable or disable a user's account. Only available to admins

        Args:
            enabled: Whether to enable or disable this user's account
        """
        raise_on_error(self._client.put(f'{self.subject}/naughty', naughty=not enabled))

    def create(self) -> None:
        """
        Creates this user on the server side. Only available to admins
        """
        if self.subject is None:
            raise ValueError("must create user with a 'subject' specified")
        raise_on_error(self._client.post('', user=self))

    def save(self) -> None:
        """
        Updates this user on the server side. Only available to the admins or the current user
        """
        if self.subject is None:
            raise ValueError("cannot update a User with no subject")
        raise_on_error(self._client.put(f'{self.subject}', user=self))

    def delete(self):
        """
        Delete this account and all associations. Only available to admins or the current user.
        """
        if self.subject is None:
            raise ValueError("cannot delete a User without specifying a subject")
        raise_on_error(self._client.delete(f'{self.subject}'))

    def _ipython_display_(self, **kwargs):
        return user_widget.UserWidget(self)._ipython_display_(**kwargs)


def myself() -> User:
    """
    Returns the current logged in user

    Returns:
        user: The currently logged in User.
    """
    res = raise_on_error(users_client.get("self"))
    return User(**res.json()['user'])


def get_user(subject: str) -> User:
    """
    Returns the requested user if the requestor has permissions

    Args:
        subject: the subject of the requested user

    Returns:
        user: the requested User
    """
    res = raise_on_error(users_client.get(subject))
    return User(**res.json()['user'])


def get_users() -> List[User]:
    """
    Returns all users, if the current user has permission

    Returns:
        users: a list of all users.
    """
    res = raise_on_error(users_client.get(""))
    return [User(**u) for u in res.json()['users']]
