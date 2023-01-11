import os
from setuptools import setup, find_packages

version = '1.8'

install_requires =[
    'setuptools',
    #'gp.fileupload',
    'grok',
    'grokcore.startup',
    'grokui.admin',
    'hurry.query',
    'hurry.jquery',
    'hurry.jqueryui',
    'hurry.workflow >= 0.11',
    # Add extra requirements here
    'docutils', # For RST-processing...
    'zope.xmlpickle',
    'hurry.file',
    'hurry.zoperesource',
    'zc.sourcefactory',
    'megrok.layout',
    'reportlab',
    'Pillow',
    'psutil',
    'unicodecsv',
    'zope.app.authentication', # BBB: During switch to grok 1.1
    'zope.app.file',
    'zope.app.testing',        # XXX: test_permissions needs this
    'zope.app.undo',
    'zope.file',
    'zope.interface >= 3.6.0',
    'zope.testbrowser',        # XXX: test_permissions needs this
    'zope.i18n',
    'zope.mimetype',
    'zope.errorview',
    'zope.schema >= 3.8.0',
    'zope.sendmail',
    'ulif.loghandlers',
    'zc.async[z3]',
    'z3c.evalexception',
    'PyPDF2',
    ],

diazo_require = [
    'diazo',
    'webob',
    ]

# Having beaker installed additionally is a feature very recommended
# for production use. The default buildout includes beaker for tests,
# start scripts, and other parts that can benefit from it. The windows
# buildout does not include it due to compiling problems with the
# beaker package.
beaker_require = [
    'dolmen.beaker',
    ]

tests_require = [
    'z3c.testsetup',
    'zope.app.testing',
    'zope.testbrowser',
    'zope.testing',
    'unittest2',
    ]

docs_require = [
    'Sphinx',
    'collective.recipe.sphinxbuilder',
    'docutils',
    'roman',
    'repoze.sphinx.autointerface',
    ]

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    read('README.txt')
    + '\n\n'
    + read('CHANGES.txt')
    + '\n\n'
    + 'Download\n'
    + '********\n'
    )

setup(name = 'waeup.kofa',
      version = version,
      description = "A student online information and  registration portal",
      long_description = long_description,

      keywords = "portal waeup kofa student university registration grok zope",
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Framework :: Zope3',
        'Topic :: Education',
        'Topic :: Internet :: WWW/HTTP',
        ],
      author = "The WAeUP team.",
      author_email = "de@waeup.org",
      url = "http://www.waeup.org/",
      license = "GPL",
      package_dir = {'': 'src'},
      packages= find_packages('src'),
      namespace_packages = ['waeup',],
      include_package_data = True,
      zip_safe = False,
      install_requires = install_requires,
      tests_require = tests_require,
      extras_require = dict(
        test = tests_require,
        docs = docs_require,
        beaker = beaker_require,
        diazo = diazo_require,
        ),
      entry_points="""
      # Add entry points here
      #[hurry.resource.libraries]
      #waeup_kofa = waeup.kofa.browser.resources:waeup_kofa
      [console_scripts]
      kofa-debug = grokcore.startup:interactive_debug_prompt
      kofactl = grokcore.startup:zdaemon_controller
      analyze = waeup.kofa.maintenance:db_analyze
      fsdiff = waeup.kofa.maintenance:db_diff
      [paste.app_factory]
      main = waeup.kofa.startup:env_app_factory
      debug = waeup.kofa.startup:env_debug_app_factory

      """,
      )
