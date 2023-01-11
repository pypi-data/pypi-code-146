## $Id: logger.py 13776 2016-03-11 11:45:01Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
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
"""
Convenience stuff for logging.

Main component of :mod:`waeup.kofa.utils.logging` is a mix-in class
:class:`waeup.kofa.utils.logging.Logger`. Classes derived (also) from
that mix-in provide a `logger` attribute that returns a regular Python
logger logging to a rotating log file stored in the datacenter storage
path.

Deriving components (classes) should set their own `logger_name` and
`logger_filename` attribute.

The `logger_name` tells under which name the logger should be
registered Python-wise. This is usually a dotted name string like
``waeup.kofa.${sitename}.mycomponent`` which should be unique. If you
pick a name already used by another component, trouble is ahead. The
``${sitename}`` chunk of the name can be set literally like this. The
logger machinery will turn it into some real site name at time of
logging.

The `logger_filename` attribute tells how the logfile should be
named. This should be some base filename like
``mycomponent.log``. Please note, that some logfile names are already
used: ``main.log``, ``applications.log``, and ``datacenter.log``.

The `Logger` mix-in also cares for updating the logging handlers when
a datacenter location moves. That means you do not have to write your
own event handlers for the purpose. Just derive from `Logger`, set
your `logger_name` and `logger_filename` attribute and off you go::

  from waeup.kofa.utils.logger import Logger

  class MyComponent(object, Logger):
      # Yes that's a complete working class
      logger_name = 'waeup.kofa.${sitename}.mycomponent
      logger_filename = 'mycomponent.log'

      def do_something(self):
           # demomstrate how to use logging from methods
           self.logger.info('About to do something')
           try:
               # Do something here
           except IOError:
               self.logger.warn('Something went wrong')
               return
           self.logger.info('I did it')

As you can see from that example, methods of the class can log
messages simply by calling `self.logger`.

The datacenter and its storage are created automatically when you
create a :class:`waeup.kofa.app.University`. This also means that
logging with the `Logger` mix-in will work only inside so-called sites
(`University` instances put into ZODB are such `sites`).

Other components in this module help to make everything work.
"""
import os
import grok
import logging
from logging.handlers import WatchedFileHandler
from string import Template
from zope import schema
from zope.component import queryUtility
from zope.interface import Interface, Attribute, implements
from waeup.kofa.interfaces import (
    IDataCenter, IDataCenterStorageMovedEvent, ILoggerCollector)
from waeup.kofa.utils.helpers import get_current_principal

#: Default logging level (`logging.INFO`)
LEVEL = logging.INFO

class ILogger(Interface):
    logger_name = schema.TextLine(
        title = u'A Python logger name')
    logger_filename = schema.TextLine(
        title = u'A filename for the log file to use (basename)')
    logger = Attribute("Get a Python logger instance already set up")
    def logger_setup(logger):
        """Setup a logger.

        `logger` is an instance of :class:`logging.Logger`.
        """

    def logger_get_logfile_path():
        """Get path to logfile used.

        Return `None` if the file path cannot be computed.
        """

    def logger_get_logdir():
        """Get the directory of the logfile.

        Return `None` if the directory path cannot be computed.
        """

class ContextFilter(logging.Filter):
    """
    This is a filter which injects contextual information into the log.

    """

    def filter(self, record):
        user = get_current_principal()
        record.user = getattr(user, 'id', 'system')
        return True

class Logger(object):
    """Mixin-class that for logging support.

    Classes that (also) inherit from this class provide support for
    logging with waeup sites.

    By default a `logger` attribute is provided which returns a
    regular Python logger. This logger has already registered a file
    rotating log handler that writes log messages to a file `main.log`
    in datacenters ``log/`` directory. This is the main log file also
    used by other components. Therefore you can pick another filename
    by setting the `logger_filename` attribute.

    All methods and attributes of this mix-in start with ``logger_``
    in order not to interfere with already existing names of a class.

    Method names do not follow the usual Zope habit (CamelCase) but
    PEP8 convention (lower_case_with_underscores).
    """

    #: The filename to use when logging.
    logger_filename = 'main.log'

    #: The Python logger name used when
    #: logging. ``'waeup.kofa.${sitename}'`` by default. You can use the
    #: ``${sitename}`` placeholder in that string, which will be
    #: replaced by the actual used site name.
    logger_name = 'waeup.kofa.${sitename}'

    #: The format to use when logging.
    logger_format_str = '%(asctime)s - %(levelname)s - %(user)s - %(message)s'

    implements(ILogger)

    @property
    def logger(self):
        """Get a logger instance.

        Returns a standard logger object as provided by :mod:`logging`
        module from the standard library.

        Other components can use this logger to perform log entries
        into the logfile of this component.

        The logger is initialized the first time it is called.

        The logger is only available when used inside a site.

        .. note:: The logger default level is
                  :data:`logging.WARN`. Use
                  :meth:`logging.Logger.setLevel` to set a different level.
        """
        site = grok.getSite()
        sitename = getattr(site, '__name__', None)
        loggername = Template(self.logger_name).substitute(
            dict(sitename='%s' % sitename))
        logger = logging.getLogger(loggername)
        if site is None or sitename is None:
            # Site not added to ZODB yet. Log to commandline
            return logger
        if len(logger.handlers) != 1:
            handlers = [x for x in logger.handlers]
            for handler in handlers:
                handler.flush()
                handler.close()
                logger.removeHandler(handler)
            logger = self.logger_setup(logger)
        if logger is None:
            # It might happen, that we have no logger now.
            logger = logging.getLogger(loggername)
        return logger

    def logger_setup(self, logger):
        """Setup logger.

        The logfile will be stored in the datacenter logs/ dir.
        """
        filename = self.logger_get_logfile_path()
        if filename is None:
            return
        collector = queryUtility(ILoggerCollector)
        if collector is not None:
            site = grok.getSite()
            collector.registerLogger(site, self)

        # Create a rotating file handler logger.
        handler = WatchedFileHandler(
            filename, encoding='utf-8')
        handler.setLevel(LEVEL)
        formatter = logging.Formatter(self.logger_format_str)
        handler.setFormatter(formatter)

        # Don't send log msgs to ancestors. This stops displaying
        # logmessages on the commandline.
        logger.propagate = False
        logger.addHandler(handler)
        logger.setLevel(LEVEL)

        flt = ContextFilter()
        logger.addFilter(flt)
        return logger

    def logger_get_logfile_path(self):
        """Get the path to the logfile used.

        Returns the path to a file in local sites datacenter ``log/``
        directory (dependent on :meth:`logger_get_logdir`) and with
        :attr:`logger_filename` as basename.

        Override this method if you want a complete different
        computation of the logfile path. If you only want a different
        logfile name, set :attr:`logger_filename`. If you only want a
        different path to the logfile override
        :meth:`logger_get_logdir` instead.

        Returns ``None`` if no logdir can be fetched.

        .. note:: creates the logfile dir if it does not exist.

        """
        logdir = self.logger_get_logdir()
        if logdir is None:
            return None
        return os.path.join(logdir, self.logger_filename)

    def logger_get_logdir(self):
        """Get log dir where logfile should be put.

        Returns the path to the logfile directory. If no site is set,
        ``None`` is returned. The same applies, if the site has no
        datacenter.

        If the dir dies not exist already it will be created. Only the
        last part of the directory path will be created.
        """
        site = grok.getSite()
        if site is None:
            return None
        datacenter = site.get('datacenter', None)
        if datacenter is None:
            return None
        logdir = os.path.join(datacenter.storage, 'logs')
        if not os.path.exists(logdir):
            os.mkdir(logdir)
        return logdir

    def logger_logfile_changed(self):
        """React on logfile location change.

        If the logfile changed, we can set a different logfile. While
        changing the logfile is a rather critical operation you might
        not do often in production use, we have to cope with that
        especially in tests.

        What this method does by default (unless you override it):

        - It fetches the current logger and

          - Removes flushes, closes, and removes all handlers

          - Sets up new handler(s).

        All this, of course, requires to be 'in a site'.

        Use this method to handle moves of datacenters, for instance
        by writing an appropriate event handler.
        """
        logger = self.logger
        self.logger_shutdown()
        self.logger_setup(logger)
        return

    def logger_shutdown(self):
        """Remove all specific logger setup.
        """
        logger = self.logger
        handlers = [x for x in logger.handlers]
        for handler in handlers:
            handler.flush()
            handler.close()
            logger.removeHandler(handler)
        collector = queryUtility(ILoggerCollector)
        if collector is not None:
            collector.unregisterLogger(grok.getSite(), self)
        return


class LoggerCollector(dict, grok.GlobalUtility):
    """A global utility providing `ILoggerCollector`.

    A logging collector collects logging components. This helps to
    inform them when a logfile location changes.

    Logging components are registered per site they belong to.
    """

    implements(ILoggerCollector)

    def getLoggers(self, site):
        name = getattr(site, '__name__', None)
        if name is None:
            return []
        if name not in self.keys():
            return []
        return self[name]

    def registerLogger(self, site, logging_component):
        name = getattr(site, '__name__', None)
        if name is None:
            return
        if not name in self.keys():
            # new component
            self[name] = []
        if logging_component in self[name]:
            # already registered
            return
        self[name].append(logging_component)
        return

    def unregisterLogger(self, site, logging_component):
        name = getattr(site, '__name__', None)
        if name is None or name not in self.keys():
            return
        if logging_component not in self[name]:
            return
        self[name].remove(logging_component)
        return

@grok.subscribe(IDataCenter, IDataCenterStorageMovedEvent)
def handle_datacenter_storage_moved(obj, event):
    """Event handler, in case datacenter storage moves.

    By default all our logfiles (yes, we produce a whole bunch of it)
    are located in a ``log/`` dir of a local datacenter, the
    datacenter 'storage'. If this path changes because the datacenter
    is moved an appropriate event is triggered and we can react.

    Via the global ILoggerCollector utility, a small piece that allows
    self-registering of logging components, we can lookup components
    whose logfile path has to be set up anew.

    Each component we call has to provide ILogger or, more specific,
    the :meth:`logger_logfile_changed` method of this interface.
    """
    site = grok.getSite()
    if site is None:
        return
    collector = queryUtility(ILoggerCollector)
    loggers = collector.getLoggers(site)
    for logger in loggers:
        if hasattr(logger, 'logger_logfile_changed'):
            logger.logger_logfile_changed()
    return

from waeup.kofa.interfaces import IUniversity
@grok.subscribe(IUniversity, grok.IObjectRemovedEvent)
def handle_site_removed(obj, event):
    collector = queryUtility(ILoggerCollector)
    name = getattr(obj, '__name__', None)
    if name is None:
        return
    if name not in collector.keys():
        return
    del collector[name]
    return
