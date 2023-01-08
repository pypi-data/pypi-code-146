# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2022 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
ASGI Views
"""

from http.cookies import SimpleCookie

from beaker.session import SignedCookie
from pyramid.interfaces import ISessionFactory


class MockRequest(dict):
    """
    Fake request class, needed for re-construction of the user's web
    session.
    """
    environ = {}

    def add_response_callback(self, func):
        pass


class WebsocketView(object):

    def __init__(self, pyramid_config):
        self.pyramid_config = pyramid_config
        self.registry = self.pyramid_config.registry
        self.model = self.rattail_config.get_model()

    @property
    def rattail_config(self):
        return self.registry['rattail_config']

    def get_rattail_app(self):
        return self.rattail_config.get_app()

    async def authorize(self, scope, receive, send, permission):

        # is user authorized for this socket?
        authorized = await self.has_permission(scope, permission)

        # wait for client to connect
        message = await receive()
        assert message['type'] == 'websocket.connect'

        # allow or deny access, per authorization
        if authorized:
            await send({'type': 'websocket.accept'})
        else: # forbidden
            await send({'type': 'websocket.close'})

        return authorized

    async def get_user(self, scope, session=None):
        app = self.get_rattail_app()
        model = self.model

        # load the user's web session
        user_session = self.get_user_session(scope)
        if user_session:

            # determine user uuid
            user_uuid = user_session.get('auth.userid')
            if user_uuid:

                # use given db session, or make a new one
                with app.short_session(config=self.rattail_config,
                                       session=session) as s:

                    # load user proper
                    return s.query(model.User).get(user_uuid)

    def get_user_session(self, scope):
        settings = self.registry.settings
        beaker_key = settings['beaker.session.key']
        beaker_secret = settings['beaker.session.secret']

        # get ahold of session identifier cookie
        headers = dict(scope['headers'])
        cookie = headers.get(b'cookie')
        if not cookie:
            return
        cookie = cookie.decode('utf_8')
        cookie = SimpleCookie(cookie)
        morsel = cookie[beaker_key]

        # simulate pyramid_beaker logic to get at the actual session
        cookieheader = morsel.output(header='')
        cookie = SignedCookie(beaker_secret, input=cookieheader)
        session_id = cookie[beaker_key].value
        factory = self.registry.queryUtility(ISessionFactory)
        request = MockRequest()
        # nb. cannot pass 'id' to our factory, but things still work
        # if we assign it immediately, before load() is called
        session = factory(request)
        session.id = session_id
        session.load()

        return session

    async def has_permission(self, scope, permission):
        app = self.get_rattail_app()
        auth_handler = app.get_auth_handler()

        # figure out if user is authorized for this websocket
        session = app.make_session()
        user = await self.get_user(scope, session=session)
        authorized = auth_handler.has_permission(session, user, permission)
        session.close()

        return authorized
