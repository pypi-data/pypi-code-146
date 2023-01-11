## $Id: testing.py 12598 2015-02-11 16:22:44Z uli $
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
"""Testing support for :mod:`waeup.kofa`.
"""
import grok
import doctest
import logging
import os.path
import re
import tempfile
import shutil
import unittest
import warnings
import zope.component
import waeup.kofa
from contextlib import contextmanager
from zc.async.interfaces import COMPLETED
from zope.app.testing.functional import (
    ZCMLLayer, FunctionalTestSetup, getRootFolder, sync, FunctionalTestCase)
from zope.component import getGlobalSiteManager, queryUtility, getUtility
from zope.security.testing import addCheckerPublic
from zope.testing import renormalizing
from zope.testing.cleanup import cleanUp
from waeup.kofa.interfaces import IKofaUtils

ftesting_zcml = os.path.join(
    os.path.dirname(waeup.kofa.__file__), 'ftesting.zcml')
FunctionalLayer = ZCMLLayer(ftesting_zcml, __name__, 'FunctionalLayer',
                            allow_teardown=True)


def get_all_loggers():
    """Get the keys of all logger defined globally.
    """
    result = logging.root.manager.loggerDict.keys()
    ws_loggers = [x for x in result if 'waeup.kofa' in x]
    if ws_loggers:
        # For debugging: show any remaining loggers from w.k. namespace
        print "\nLOGGERS: ", ws_loggers
    return result


def remove_new_loggers(old_loggers):
    """Remove the loggers except `old_loggers`.

    `old_loggers` is a list of logger keys as returned by
    :func:`get_all_loggers`. All globally registered loggers whose
    name is not in `old_loggers` is removed.
    """
    new_loggers = [key for key in logging.root.manager.loggerDict
                   if key not in old_loggers]
    for key in sorted(new_loggers, reverse=True):
        logger = logging.getLogger(key)
        for handler in logger.handlers:
            handler.close()
        del logger
        del logging.root.manager.loggerDict[key]
    return


def remove_logger(name):
    """Remove logger with name `name`.

    Use is safe. If the logger does not exist nothing happens.
    """
    if name in logging.root.manager.loggerDict.keys():
        del logging.root.manager.loggerDict[name]
    return


def setUpZope(test=None):
    """Initialize a Zope-compatible environment.

    Currently, we only initialize the event machinery.
    """
    zope.component.eventtesting.setUp(test)


def cleanUpZope(test=None):
    """Clean up Zope-related registrations.

    Cleans up all registrations and the like.
    """
    cleanUp()


def maybe_grok():
    """Try to grok the :mod:`waeup.kofa` package.

    For many tests, even simple ones, we want the components defined
    somewhere in the :mod:`waeup.kofa` package being registered. While
    grokking the complete package can become expensive when done many
    times, we only want to grok if it did not happen
    before. Furthermore regrokking the whole package makes no sense if
    done already.

    :func:`maybe_grok` checks whether any eventhandlers are already
    registered and does nothing in that case.

    The grokking of :mod:`waeup.kofa` is done with warnings disabled.

    Returns ``True`` if grokking was done, ``False`` else.

    .. The following samples should go into Sphinx docs directly....

    Sample
    ******

    Usage with plain Python testrunners
    -----------------------------------

    Together with the :func:`setUpZope` and :func:`cleanUpZope`
    functions we then can do unittests with all components registered
    and the event dispatcher in place like this::

      import unittest2 as unittest # Want Python 2.7 features
      from waeup.kofa.testing import (
        maybe_grok, setUpZope, cleanUpZope,
        )
      from waeup.kofa.app import University

      class MyTestCase(unittest.TestCase):

          @classmethod
          def setUpClass(cls):
              grokked = maybe_grok()
              if grokked:
                  setUpZope(None)
              return

          @classmethod
          def tearDownClass(cls):
              cleanUpZope(None)

          def setUp(self):
              pass

          def tearDown(self):
              pass

          def test_jambdata_in_site(self):
              u = University()
              self.assertTrue('jambdata' in u.keys())
              return

    Here the component registration is done only once for the whole
    :class:`unittest.TestCase` and no ZODB is needed. That means
    inside the tests you can expect to have all :mod:`waeup.kofa`
    components (utilities, adapter, events) registered but as objects
    have here still have no place inside a ZODB things like 'browsing'
    won't work out of the box. The benefit is the faster test
    setup/teardown.

    .. note:: This works only with the default Python testrunners.

         If you use the Zope testrunner (from :mod:`zope.testing`)
         then you have to use appropriate layers like the
         :class:`waeup.kofa.testing.KofaUnitTestLayer`.

    Usage with :mod:`zope.testing` testrunners
    ------------------------------------------

    If you use the standard Zope testrunner, classmethods like
    `setUpClass` are not executed. Instead you have to use a layer
    like the one defined in this module.

    .. seealso:: :class:`waeup.kofa.testing.KofaUnitTestLayer`

    """
    gsm = getGlobalSiteManager()
    # If there are any event handlers registered already, we assume
    # that waeup.kofa was grokked already. There might be a batter
    # check, though.
    if len(list(gsm.registeredHandlers())) > 0:
        return False
    # Register the zope.Public permission, normally done via ZCML setup.
    addCheckerPublic()
    warnings.simplefilter('ignore')   # disable (erraneous) warnings
    grok.testing.grok('waeup.kofa')
    warnings.simplefilter('default')  # reenable warnings
    return True


def setup_datacenter_conf():
    """Register a datacenter config utility for non-functional tests.
    """
    from waeup.kofa.interfaces import IDataCenterConfig
    conf = queryUtility(IDataCenterConfig)
    if conf is not None:
        return
    path = tempfile.mkdtemp()
    conf = {'path': path}
    gsm = getGlobalSiteManager()
    gsm.registerUtility(conf, IDataCenterConfig)
    return


def teardown_datacenter_conf():
    """Unregister a datacenter config utility for non-functional tests.
    """
    from waeup.kofa.interfaces import IDataCenterConfig
    conf = queryUtility(IDataCenterConfig)
    if conf is None:
        return
    path = conf['path']
    shutil.rmtree(path)
    gsm = getGlobalSiteManager()
    gsm.unregisterUtility(conf, IDataCenterConfig)
    return


class KofaUnitTestLayer(object):
    """A layer for tests that groks `waeup.kofa`.

    A Zope test layer that registers all :mod:`waeup.kofa` components
    before attached tests are run and cleans this registrations up
    afterwards. Also basic (non-waeup.kofa) components like the event
    dispatcher machinery are registered, set up and cleaned up.

    This layer does not provide a complete ZODB setup (and is
    therefore much faster than complete functional setups) but does
    only the registrations (which also takes some time, so running
    this layer is slower than test cases that need none or only a
    few registrations).

    The registrations are done for all tests the layer is attached to
    once before all these tests are run (and torn down once
    afterwards).

    To make use of this layer, you have to write a
    :mod:`unittest.TestCase` class that provides an attribute called
    ``layer`` with this class as value like this::

      import unittest
      from waeup.kofa.testing import KofaUnitTestLayer

      class MyTestCase(unittest.TestCase):

          layer = KofaUnitTestLayer

          # per-test setups and real tests go here...
          def test_foo(self):
              self.assertEqual(1, 1)
              return

    """
    @classmethod
    def setUp(cls):
        #setUpZope(None)
        grokked = maybe_grok()
        setup_datacenter_conf()
        return

    @classmethod
    def tearDown(cls):
        teardown_datacenter_conf()
        cleanUpZope(None)
        return


#: This extended :class:`doctest.OutputChecker` allows the following
#: additional matches when looking for output diffs:
#:
#: `N.NNN seconds`
#:    matches strings like ``12.123 seconds``
#:
#: `HTTPError:`
#:    matches ``httperror_seek_wrapper:``. This string is output by some
#:    virtual browsers you might use in functional browser tests to signal
#:    HTTP error state.
#:
#: `1034h`
#:    is ignored. This sequence of control chars is output by some
#:    (buggy) testrunners at beginning of output.
#:
#: `<10-DIGITS>`
#:    matches a sequence of 10 digits. Useful when checking accesscode
#:    numbers if you don't know the exact (random) code.
#:
#: `<6-DIGITS>`
#:    matches a sequence of 6 digits. Useful when checking accesscode
#:    numbers if you don't know the exact (random) code.
#:
#: `<YYYY-MM-DD hh:mm:ss>`
#:    matches any date and time like `2011-05-01 12:01:32`.
#:
#: `<DATE-AND-TIME>`
#:    same like ``<YYYY-MM-DD hh:mm:ss>`` but shorter.
checker = renormalizing.RENormalizing([
    # Relevant normalizers from zope.testing.testrunner.tests:
    (re.compile(r'\d+[.]\d\d\d seconds'), 'N.NNN seconds'),
    # Our own one to work around
    # http://reinout.vanrees.org/weblog/2009/07/16/invisible-test-diff.html:
    (re.compile(r'.*1034h'), ''),
    (re.compile(r'httperror_seek_wrapper:'), 'HTTPError:'),
    (re.compile('[\d]{6}'), '<6-DIGITS>'),
    (re.compile('[\d]{10}'), '<10-DIGITS>'),
    (re.compile('\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d [\+\-]\d\d\d\d [^ ]+'),
     '<YYYY-MM-DD hh:mm:ss TZ>'),
    (re.compile('\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d'), '<YYYY-MM-DD hh:mm:ss>'),
    (re.compile('\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d'), '<DATETIME>'),
    ])


old_loggers = []


def setUp(test):
    global old_loggers
    old_loggers = get_all_loggers()
    FunctionalTestSetup().setUp()


def tearDown(test):
    global old_loggers
    FunctionalTestSetup().tearDown()
    remove_new_loggers(old_loggers)


def doctestsuite_for_module(dotted_path):
    """Create a doctest suite for the module at `dotted_path`.
    """
    test = doctest.DocTestSuite(
        dotted_path,
        setUp=setUp,
        tearDown=tearDown,
        checker=checker,
        extraglobs=dict(
            getRootFolder=getRootFolder,
            sync=sync,),
        optionflags=(doctest.ELLIPSIS +
                     doctest.NORMALIZE_WHITESPACE +
                     doctest.REPORT_NDIFF),
        )
    test.layer = FunctionalLayer
    return test


optionflags = (
    doctest.REPORT_NDIFF + doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE)


def clear_logger_collector():
    from zope.component import queryUtility
    from waeup.kofa.interfaces import ILoggerCollector
    collector = queryUtility(ILoggerCollector)
    if collector is None:
        return
    keys = list(collector.keys())
    for key in keys:
        del collector[key]
    return


class FunctionalTestCase(FunctionalTestCase):
    """A test case that supports checking output diffs in doctest style.
    """

    def setUp(self):
        super(FunctionalTestCase, self).setUp()
        self.functional_old_loggers = get_all_loggers()
        return

    def tearDown(self):
        super(FunctionalTestCase, self).tearDown()
        remove_new_loggers(self.functional_old_loggers)
        clear_logger_collector()
        return

    def assertMatches(self, want, got, checker=checker,
                      optionflags=optionflags):
        """Assert that the multiline string `want` matches `got`.

        In `want` you can use shortcuts like ``...`` as in regular doctests.

        If no special `checker` is passed, we use an extended
        :class:`doctest.OutputChecker` as defined in
        :mod:`waeup.kofa.testing`.

        If optional `optionflags` are not given, use ``REPORT_NDIFF``,
        ``ELLIPSIS``, and ``NORMALIZE_WHITESPACE``.

        .. seealso:: :data:`waeup.kofa.testing.optionflags`

        .. seealso:: :data:`waeup.kofa.testing.checker`
        """
        if checker.check_output(want, got, optionflags):
            return
        diff = checker.output_difference(
            doctest.Example('', want), got, optionflags)
        self.fail(diff)


class FunctionalTestSetup(FunctionalTestSetup):
    """A replacement for the zope.app.testing class.

    Removes also loggers.
    """

    def setUp(self):
        self.old_loggers = get_all_loggers()
        super(FunctionalTestSetup, self).setUp()
        return

    def tearDown(self):
        super(FunctionalTestSetup, self).tearDown()
        remove_new_loggers(self.old_loggers)
        return


def get_doctest_suite(filename_list=[]):
    """Helper function to create doctest suites for doctests.

    The `filename_list` is a list of filenames relative to the
    w.k. dir.  So, to get a doctest suite for ``browser.txt`` and
    ``blah.txt`` in the ``browser/`` subpackage you have to pass
    ``filename_list=['browser/browser.txt','browser/blah.txt']`` and
    so on.

    The returned test suite must be registered somewhere locally for
    instance by something like:

      from waeup.kofa.testing import get_doctest_suite
      def test_suite():
        suite = get_doctest_suite(['mypkg/foo.txt', 'mypkg/bar.txt'])
        return suite

    and that's it.
    """
    suite = unittest.TestSuite()
    for filename in filename_list:
        path = os.path.join(
            os.path.dirname(__file__), filename)
        test = doctest.DocFileSuite(
            path,
            module_relative=False,
            setUp=setUp, tearDown=tearDown,
            globs=dict(getRootFolder=getRootFolder),
            optionflags=doctest.ELLIPSIS + doctest.NORMALIZE_WHITESPACE,
            checker=checker,
            )
        test.layer = FunctionalLayer
        suite.addTest(test)
    return suite


class FakeJob(object):
    # A job usable for simple async tests
    status = COMPLETED
    result = None
    acts_under_heavy_load = False  # set to True to mimic system high load

    def __init__(self, *args, **kw):
        self.args = args
        self.kwargs = kw


class FakeJobManager(object):
    # A fake job manager for testing async functionality

    def __init__(self):
        # make sure each instance maintains an own set of jobs/nums.
        self._jobs = dict()
        self._curr_num = 1

    def get(self, job_id):
        if job_id == '3':
            return FakeJob()
        return self._jobs.get(job_id, None)

    def put(self, job):
        if getattr(job, 'acts_under_heavy_load', False):
            return None
        num = str(self._curr_num)
        self._jobs[num] = job
        self._curr_num += 1
        return num

    def remove(self, job_id, site):
        if job_id in self._jobs:
            del self._jobs[job_id]
        return


@contextmanager
def expensive_actions():
    """A contextmanager to work with a modified `expensive_acrtions_allowed()`

    This method is part of local IKofaUtils.
    """
    utils = getUtility(IKofaUtils)
    old_func = utils.expensive_actions_allowed
    try:
        yield utils
    finally:
        # restore function after use
        utils.expensive_actions_allowed = old_func
