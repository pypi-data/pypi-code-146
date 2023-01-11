from dofast.network import Twitter
from dofast.auth import auth


class API(object):
    def __init__(self):
        pass

    @property
    def twitter(self):
        keys = auth.twitter
        return Twitter(keys['consumer_key'], keys['consumer_secret'],
                       keys['access_token'], keys['access_token_secret'])
