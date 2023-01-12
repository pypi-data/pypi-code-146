from txhttputil.site.AuthUserDetails import UserDetails, everyoneGroup
from txhttputil.util.DeferUtil import maybeDeferredWrap



class AuthCredentials:

    @maybeDeferredWrap
    def check(self, username, password):
        """ Check

        @:return UserDetails if the login was successful, otherwise None

        """

        raise NotImplementedError()


class AllowAllAuthCredentials(AuthCredentials):

    @maybeDeferredWrap
    def check(self, username, password):
        """ Check

        @:return UserDetails if the login was successful, otherwise None

        """
        user = UserDetails()
        user.group = everyoneGroup
        return user
