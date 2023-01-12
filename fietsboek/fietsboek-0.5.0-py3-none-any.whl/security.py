"""Module implementing the user authentication."""
from pyramid.authentication import AuthTktCookieHelper, SessionAuthenticationHelper
from pyramid.authorization import ACLHelper, Authenticated, Everyone
from pyramid.interfaces import ISecurityPolicy
from pyramid.security import Allowed, Denied
from pyramid.traversal import DefaultRootFactory
from sqlalchemy import select
from zope.interface import implementer

from . import models

ADMIN_PERMISSIONS = {"admin"}


@implementer(ISecurityPolicy)
class SecurityPolicy:
    """Implementation of the Pyramid security policy."""

    def __init__(self, cookie_secret):
        self.helper = SessionAuthenticationHelper()
        # The cookie_helper is used for the "Remember me" function, as the
        # authentication set by the cookie is deliberately kept for a long long
        # time. The session authentication on the other hand expires after the
        # set time (by default, 15 minutes).
        self.cookie_helper = AuthTktCookieHelper(cookie_secret, max_age=2**31 - 1)

    def identity(self, request):
        """See :meth:`pyramid.interfaces.ISecurityPolicy.identity`"""
        userid = self.helper.authenticated_userid(request)
        if userid is None:
            # Check if there is maybe a "Remember me" cookie
            auth_info = self.cookie_helper.identify(request) or {}
            userid = auth_info.get("userid")

        # Still no identity found
        if userid is None:
            return None

        query = select(models.User).filter_by(id=int(userid))
        return request.dbsession.execute(query).scalar_one_or_none()

    def authenticated_userid(self, request):
        """See :meth:`pyramid.interfaces.ISecurityPolicy.authenticated_userid`"""
        identity = self.identity(request)
        if identity is None:
            return None
        return str(identity.id)

    def permits(self, request, context, permission):
        """See :meth:`pyramid.interfaces.ISecurityPolicy.permits`"""
        identity = self.identity(request)
        # If the context is not there, we are on a static site that does not use ACL
        if isinstance(context, DefaultRootFactory):
            if identity is None:
                return Denied("User is not signed in.")
            if permission not in ADMIN_PERMISSIONS:
                return Allowed("User is signed in.")
            if identity.is_admin:
                return Allowed("User is an administrator.")
            return Denied("User is not an administrator.")

        # If the context is there, use ACL
        principals = [Everyone]
        if identity is not None:
            principals.append(Authenticated)
            principals.extend(identity.principals())

        if "secret" in request.GET:
            principals.append(f'secret:{request.GET["secret"]}')

        return ACLHelper().permits(context, principals, permission)

    def remember(self, request, userid, **kw):
        """See :meth:`pyramid.interfaces.ISecurityPolicy.remember`"""
        return self.helper.remember(request, userid, **kw)

    def remember_cookie(self, request, userid, **kw):
        """Return the headers for remembering the user using the cookie method.

        This is used for the "Remember me" functionality, as the cookie doesn't
        expire (unlike the session).

        The parameters are the same as for :meth:`remember`.
        """
        return self.cookie_helper.remember(request, userid, **kw)

    def forget(self, request, **kw):
        """See :meth:`pyramid.interfaces.ISecurityPolicy.forget`"""
        return self.helper.forget(request, **kw) + self.cookie_helper.forget(request, **kw)
