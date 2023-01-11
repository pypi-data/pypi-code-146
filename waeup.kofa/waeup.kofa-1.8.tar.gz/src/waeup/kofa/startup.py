## $Id: startup.py 12110 2014-12-02 06:43:10Z henrik $
##
## Copyright (C) 2012 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
"""WSGI application factories that additionally set environment vars.

The `grokcore.startup` factories for creating WSGI applications
currently do not support setting of arbitrary environment vars.

The below factories add this feature.

Environment vars can be set in any ``.ini`` file used at startup. In
the ``[DEFAULT]`` section set the option ``env_vars`` with key/value
pairs as value like so::

  [DEFAULT]
  zope_conf = <path-to-zope.conf>
  env_vars = KEY1 value1
             KEY2 value2

This would set the env vars ``KEY1`` and ``KEY2`` to the respective
values on startup on an instance.

To activate these factories, in the ``setup.py`` of your project use::

  [paste.app_factory]
  main = waeup.kofa.startup:env_app_factory
  debug = waeup.kofa.startup:env_debug_app_factory

in the entry points section (replacing the references to respective
`grokcore.startup` factories.

Info for developers: paster on startup delivers the options from
``[DEFAULT]`` section in `.ini` file as a dictionary in the
`global_conf`.
"""
import os
from ConfigParser import RawConfigParser
from grokcore.startup import application_factory, debug_application_factory

def _set_env_vars(global_conf):
    """Set vars from `global_conf['env_vars']` in `os.environ`.
    """
    env_vars = global_conf.get('env_vars', None)
    if not env_vars:
        return
    for line in env_vars.split('\n'):
        key, val = [x.strip() for x in line.strip().split(' ', 1)]
        os.environ[key] = val
    return

def env_app_factory(global_conf, **local_conf):
    """A WSGI application factory that sets environment vars.

    This app factory provides applications as expected by ``paster``
    and useable as ``[paste.app_factory]`` plugin in setup.py.

    It's a replacement for the stock app factory provided by
    `grokcore.startup`.

    Additionally it supports extrapolation of the DEFAULT var
    ``env_vars`` in .ini files used to configure paster.

    With this factory you can set enviroment vars (as in `os.environ`)
    via the ``env_vars`` keyword set in some `.ini` file::

      env_vars = MY_KEY some_value

    would set the environment variable ``MY_KEY`` to the value
    ``some_value`` before creating the actual app.

    You can also set multiple keys/values at once like this::

      env_vars = MY_KEY1  Some value
                 Another_key Anoter_value

    Note, that keys may not contain whitespaces while values
    may. Both, keys and values, are stripped before being set.
    """
    _set_env_vars(global_conf)
    return application_factory(global_conf, **local_conf)

def env_debug_app_factory(global_conf, **local_conf):
    """A debugger application factory.

    This is a wrapper around the real factory from `grokcore.startup`
    that does the same additional things as :func:`env_app_factory`:
    it sets environment vars given in `env_vars` option of a
    configuring .ini file for paster.
    """
    _set_env_vars(global_conf)
    return debug_application_factory(global_conf, **local_conf)
