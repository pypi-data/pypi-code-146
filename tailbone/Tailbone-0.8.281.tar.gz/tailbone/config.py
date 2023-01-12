# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2023 Lance Edgar
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
Rattail config extension for Tailbone
"""

from __future__ import unicode_literals, absolute_import

import warnings
from pkg_resources import parse_version

from rattail.config import ConfigExtension as BaseExtension
from rattail.db.config import configure_session

from tailbone.db import Session


class ConfigExtension(BaseExtension):
    """
    Rattail config extension for Tailbone.  Does the following:

     * Adds the rattail config object to the constructor kwargs for the
       underlying Session factory.

     * Configures the main Tailbone database session so that it records
       changes, if the config file so dictates.
    """
    key = 'tailbone'

    def configure(self, config):
        Session.configure(rattail_config=config)
        configure_session(config, Session)

        # provide default theme selection
        config.setdefault('tailbone', 'themes', 'default, falafel')
        config.setdefault('tailbone', 'themes.expose_picker', 'true')


def csrf_token_name(config):
    return config.get('tailbone', 'csrf_token_name', default='_csrf')


def csrf_header_name(config):
    return config.get('tailbone', 'csrf_header_name', default='X-CSRF-TOKEN')


def get_buefy_version(config):
    warnings.warn("get_buefy_version() is deprecated; please use "
                  "tailbone.util.get_libver() instead",
                  DeprecationWarning, stacklevel=2)

    version = config.get('tailbone', 'libver.buefy')
    if version:
        return version

    return config.get('tailbone', 'buefy_version',
                      default='latest')


def get_buefy_0_8(config, version=None):
    if not version:
        version = get_buefy_version(config)
    if version == 'latest':
        return False
    return parse_version(version) < parse_version('0.9')


def global_help_url(config):
    return config.get('tailbone', 'global_help_url')


def protected_usernames(config):
    return config.getlist('tailbone', 'protected_usernames')


def should_expose_websockets(config):
    return config.getbool('tailbone', 'expose_websockets',
                          usedb=False, default=False)
