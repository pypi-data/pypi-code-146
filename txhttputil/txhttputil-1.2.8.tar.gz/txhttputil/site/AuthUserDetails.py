"""
 * Created by Synerty Pty Ltd
 *
 * This software is open source, the MIT license applies.
 *
 * Website : http://www.synerty.com
 * Support : support@synerty.com
"""
from twisted.python.components import registerAdapter
from twisted.web.server import Session
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import implementer


# TODO, Expand on this to allow restrictions to files, etc
class GroupDetails:
    def __init__(self, name):
        self.name = name
        self.readOnly = False


everyoneGroup = GroupDetails("everyone")


# TODO, Expand on this to allow username, etc
class UserDetails:
    def __init__(self):
        self.loggedIn = False
        self.loginDate = None
        self.groupDetails = None


class IUserSession(Interface):
    userDetails = Attribute("The details of the user.")


@implementer(IUserSession)
class UserSession(object):
    ''' User Access
    This class stores the details about the user that are required by the
    elements and resources to be able to allow access.
    '''

    def __init__(self, session):
        self.userDetails = UserDetails()
        self.readOnly = True
        self.groupId = None


registerAdapter(UserSession, Session, IUserSession)
