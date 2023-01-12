import logging
from datetime import datetime

import pytz
from twisted.web.resource import IResource, ErrorPage
from twisted.web.util import DeferredResource
from zope.interface import implementer

from txhttputil.site.AuthCredentials import AuthCredentials
from txhttputil.site.AuthUserDetails import IUserSession
from txhttputil.site.BasicResource import BasicResource
from .AuthResource import LoginResource, LoginSucceededResource

logger = logging.getLogger(name=__name__)

__author__ = 'synerty'


@implementer(IResource)
class FormBasedAuthSessionWrapper(object):
    """
    Copied partly from C{twisted.web._auth.wrapper.HTTPAuthSessionWrapper}
    """

    isLeaf = False

    def __init__(self,
                 siteRootResource: BasicResource,
                 credentialChecker: AuthCredentials):
        self._siteRootResource = siteRootResource
        self._credentialChecker = credentialChecker

    def _authorizedResource(self, request):
        """
        Get the L{IResource} which the given request is authorized to receive.
        If the proper authorization headers are present, the resource will be
        requested from the portal.  If not, an anonymous login_page attempt will be
        made.
        """

        # If the user has a logged in session, let them continue
        # With out this, every HTTP request would result in a login screen.
        userSession = IUserSession(request.getSession())
        if userSession.userDetails.loggedIn:
            request.getSession().touch()
            return self._siteRootResource

        # TRY Basic HTTP Authentication
        # TODO, txHttpUtil is using FORM based authentication instead
        # authheader = request.getHeader('authorization')
        # if authheader:
        #     factory, respString = self._selectParseHeader(authheader)
        #     if factory is None:
        #         return LoginResource()
        #
        #     try:
        #         credentials = factory.decode(respString, request)
        #     except error.LoginFailed:
        #         return LoginResource()
        #     except:
        #         logger.error("Unexpected failure from credentials factory")
        #         return ErrorPage(500, None, None)
        #     else:
        #         return DeferredResource(self._login(credentials))

        # TRY form based authentication

        a = request.args
        if b"username" in a and b"password" in a:
            user = a[b'username'][0]
            pass_ = a[b"password"][0]

            deferred = self._credentialChecker.check(user, pass_)

            def checkResult(userDetails):
                if not userDetails:
                    return LoginResource()

                userDetails.loggedIn = True
                userDetails.loginDate = datetime.now(pytz.utc)

                userSession = IUserSession(request.getSession())
                userSession.userDetails = userDetails

                return LoginSucceededResource()

            def error(failure):
                logger.error("Unexpected failure from credentials factory")
                logger.error(failure.value)
                return ErrorPage(500, None, None)

            deferred.addCallback(checkResult)
            deferred.addErrback(error)

            return DeferredResource(deferred)

        # Return login_page form
        return LoginResource()

    def render(self, request):
        """
        Find the L{IResource} avatar suitable for the given request, if
        possible, and render it.  Otherwise, perhaps render an error page
        requiring authorization or describing an internal server failure.
        """
        return self._authorizedResource(request).render(request)

    def getChildWithDefault(self, path, request):
        """
        Inspect the Authorization HTTP header, and return a deferred which,
        when fired after successful authentication, will return an authorized
        C{Avatar}. On authentication failure, an C{UnauthorizedResource} will
        be returned, essentially halting further dispatch on the wrapped
        resource and all children
        """
        # Don't consume any segments of the request - this class should be
        # transparent!
        request.postpath.insert(0, request.prepath.pop())
        return self._authorizedResource(request)

        # def _login(self, credentials):
        #     """
        #     Get the L{IResource} avatar for the given credentials.
        #
        #     @return: A L{Deferred} which will be called back with an L{IResource}
        #         avatar or which will errback if authentication fails.
        #     """
        #     d = self._portal.login(credentials, None, IResource)
        #     d.addCallbacks(self._loginSucceeded, self._loginFailed)
        #     return d
        #
        # def _loginSucceeded(self, (interface, avatar, logout)):
        #     """
        #     Handle login_page success by wrapping the resulting L{IResource} avatar
        #     so that the C{logout} callback will be invoked when rendering is
        #     complete.
        #     """
        #
        #     class ResourceWrapper(proxyForInterface(IResource, 'resource')):
        #         """
        #         Wrap an L{IResource} so that whenever it or a child of it
        #         completes rendering, the cred logout hook will be invoked.
        #
        #         An assumption is made here that exactly one L{IResource} from
        #         among C{avatar} and all of its children will be rendered.  If
        #         more than one is rendered, C{logout} will be invoked multiple
        #         times and probably earlier than desired.
        #         """
        #
        #         def getChildWithDefault(self, name, request):
        #             """
        #             Pass through the lookup to the wrapped resource, wrapping
        #             the result in L{ResourceWrapper} to ensure C{logout} is
        #             called when rendering of the child is complete.
        #             """
        #             return ResourceWrapper(self.resource.getChildWithDefault(name, request))
        #
        #         def render(self, request):
        #             """
        #             Hook into response generation so that when rendering has
        #             finished completely (with or without error), C{logout} is
        #             called.
        #             """
        #             request.notifyFinish().addBoth(lambda ign: logout())
        #             return super(ResourceWrapper, self).render(request)
        #
        #     return ResourceWrapper(avatar)
        #
        # def _loginFailed(self, result):
        #     """
        #     Handle login_page failure by presenting either another challenge (for
        #     expected authentication/authorization-related failures) or a server
        #     error page (for anything else).
        #     """
        #     if result.check(error.Unauthorized, error.LoginFailed):
        #         return UnauthorizedResource(self._credentialFactories)
        #     else:
        #         logger.error(str(result) +
        #                      "HTTPAuthSessionWrapper.getChildWithDefault encountered "
        #                      "unexpected error")
        #     return ErrorPage(500, None, None)
        #
        # def _selectParseHeader(self, header):
        #     """
        #     Choose an C{ICredentialFactory} from C{_credentialFactories}
        #     suitable to use to decode the given I{Authenticate} header.
        #
        #     @return: A two-tuple of a factory and the remaining portion of the
        #         header value to be decoded or a two-tuple of C{None} if no
        #         factory can decode the header value.
        #     """
        #     elements = header.split(' ')
        #     scheme = elements[0].lower()
        #     for fact in self._credentialFactories:
        #         if fact.scheme == scheme:
        #             return (fact, ' '.join(elements[1:]))
        #     return (None, None)
