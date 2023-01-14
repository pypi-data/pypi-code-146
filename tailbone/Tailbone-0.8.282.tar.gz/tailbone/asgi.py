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
ASGI App Utilities
"""

from __future__ import unicode_literals, absolute_import

import os
import logging

import six
from six.moves import configparser

from rattail.util import load_object

from asgiref.wsgi import WsgiToAsgi


log = logging.getLogger(__name__)


class TailboneWsgiToAsgi(WsgiToAsgi):
    """
    Custom WSGI -> ASGI wrapper, to add routing for websockets.
    """

    async def __call__(self, scope, *args, **kwargs):
        protocol = scope['type']
        path = scope['path']

        if protocol == 'websocket':
            websockets = self.wsgi_application.registry.get(
                'tailbone_websockets', {})
            if path in websockets:
                await websockets[path](scope, *args, **kwargs)

        try:
            await super().__call__(scope, *args, **kwargs)
        except ValueError as e:
            # The developer may wish to improve handling of this exception.
            # See https://github.com/Pylons/pyramid_cookbook/issues/225 and
            # https://asgi.readthedocs.io/en/latest/specs/www.html#websocket
            pass
        except Exception as e:
            raise e


def make_asgi_app(main_app=None):
    """
    This function returns an ASGI application.
    """
    path = os.environ.get('TAILBONE_ASGI_CONFIG')
    if not path:
        raise RuntimeError("You must define TAILBONE_ASGI_CONFIG env variable.")

    # make a config parser good enough to load pyramid settings
    configdir = os.path.dirname(path)
    parser = configparser.ConfigParser(defaults={'__file__': path,
                                                 'here': configdir})

    # read the config file
    parser.read(path)

    # parse the settings needed for pyramid app
    settings = dict(parser.items('app:main'))

    if isinstance(main_app, six.string_types):
        make_wsgi_app = load_object(main_app)
    elif callable(main_app):
        make_wsgi_app = main_app
    else:
        if main_app:
            log.warning("specified main app of unknown type: %s", main_app)
        make_wsgi_app = load_object('tailbone.app:main')

    # construct a pyramid app "per usual"
    app = make_wsgi_app({}, **settings)

    # then wrap it with ASGI
    return TailboneWsgiToAsgi(app)


def asgi_main():
    """
    This function returns an ASGI application.
    """
    return make_asgi_app()
