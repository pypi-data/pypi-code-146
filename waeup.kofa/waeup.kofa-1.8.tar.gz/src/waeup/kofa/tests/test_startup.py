# Tests for local startup functions.
import os
import shutil
import tempfile
import unittest
from zope.app.wsgi import WSGIPublisherApplication
from waeup.kofa.startup import env_app_factory, env_debug_app_factory

ZOPE_CONF_TEMPL = '''
site-definition %s

<zodb>
  <mappingstorage />
</zodb>

<eventlog>
  <logfile>
    path STDOUT
  </logfile>
</eventlog>
'''

class StartUpTests(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.site_zcml = os.path.join(self.workdir, 'site.zcml')
        open(self.site_zcml, 'w').write('<configure />')
        self.zope_conf = os.path.join(self.workdir, 'zope.conf')
        open(self.zope_conf, 'wb').write(ZOPE_CONF_TEMPL % self.site_zcml)
        return

    def tearDown(self):
        shutil.rmtree(self.workdir)
        for name in ('TEST_FOO', 'TEST_BAR'):
            if name in os.environ:
                del os.environ[name]
        return

    def test_env_app_factory(self):
        # We can create plain WSGI apps
        factory = env_app_factory({'zope_conf': self.zope_conf})
        self.assertTrue(
            isinstance(factory, WSGIPublisherApplication))
        return

    def test_env_app_factory_single_env_var(self):
        # We can create WSGI apps with a single env var set
        factory = env_app_factory({'zope_conf': self.zope_conf,
                                   'env_vars': 'TEST_FOO value1'})
        self.assertEqual(os.environ.get('TEST_FOO', None), 'value1')
        return

    def test_env_app_factory_multiple_env_vars(self):
        # We can create WSGI apps with multiple env vars set
        env_vars = 'TEST_FOO  value1   \n  TEST_BAR  value2'
        factory = env_app_factory({'zope_conf': self.zope_conf,
                                   'env_vars': env_vars})
        self.assertEqual(os.environ.get('TEST_FOO', None), 'value1')
        self.assertEqual(os.environ.get('TEST_BAR', None), 'value2')
        return

    def test_env_debug_app_factory(self):
        # We can create debugger WSGI apps
        factory = env_debug_app_factory({'zope_conf': self.zope_conf})
        self.assertTrue(
            isinstance(factory, WSGIPublisherApplication))
        return
        pass

    def test_env_debug_app_factory_single_env_var(self):
        # We can create debugger WSGI apps with a single env var set
        factory = env_debug_app_factory({'zope_conf': self.zope_conf,
                                         'env_vars': 'TEST_FOO value1'})
        self.assertEqual(os.environ.get('TEST_FOO', None), 'value1')
        return
