# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bodhi',
 'bodhi.server',
 'bodhi.server.auth',
 'bodhi.server.consumers',
 'bodhi.server.migrations',
 'bodhi.server.migrations.versions',
 'bodhi.server.scripts',
 'bodhi.server.services',
 'bodhi.server.static',
 'bodhi.server.tasks',
 'bodhi.server.views',
 'tests',
 'tests.auth',
 'tests.consumers',
 'tests.functional',
 'tests.scripts',
 'tests.services',
 'tests.tasks',
 'tests.views']

package_data = \
{'': ['*'],
 'bodhi.server': ['email/templates/*', 'locale/*', 'templates/*'],
 'bodhi.server.static': ['css/*',
                         'fonts/*',
                         'fonts/font-awesome/*',
                         'fonts/hack/eot/*',
                         'fonts/hack/eot/latin/*',
                         'fonts/hack/web-ttf/*',
                         'fonts/hack/web-ttf/latin/*',
                         'fonts/hack/woff/*',
                         'fonts/hack/woff/latin/*',
                         'fonts/hack/woff2/*',
                         'fonts/hack/woff2/latin/*',
                         'fonts/open-sans/*',
                         'ico/*',
                         'img/*',
                         'js/*',
                         'vendor/chartjs/*',
                         'vendor/fedora-bootstrap/*',
                         'vendor/jquery-typeahead/*',
                         'vendor/jquery/*',
                         'vendor/messenger/css/*',
                         'vendor/messenger/js/*',
                         'vendor/moment/*',
                         'vendor/selectize/*',
                         'vendor/typeahead/*'],
 'tests.consumers': ['pungi.basepath/*']}

install_requires = \
['Jinja2>=2.11.3',
 'Markdown>=3.3.6',
 'PyYAML>=5.4.1',
 'SQLAlchemy>=1.3.24',
 'alembic>=1.5.5',
 'arrow>=0.17.0',
 'authlib>=0.15.4',
 'backoff>=1.10.0',
 'bleach>=3.2.3',
 'bodhi-messages>=7.0.0,<8.0.0',
 'celery>=5.2.1',
 'click>=7.1.2',
 'colander>=1.8.3',
 'cornice>=5.0.3',
 'dogpile.cache>=1.1.2',
 'fedora-messaging>=3.0.0',
 'feedgen>=0.9.0',
 'koji>=1.27.1',
 'libcomps',
 'munch>=2.5.0',
 'packaging>=21.3',
 'prometheus-client>=0.13.1',
 'psycopg2>=2.8.6',
 'py3dns>=3.2.1',
 'pyLibravatar>=1.6',
 'pyasn1-modules>=0.2.8',
 'pyramid-fas-openid>=0.4.0',
 'pyramid-mako>=1.0.2',
 'pyramid>=1.10.5',
 'python-bugzilla>=3.2.0',
 'requests>=2.25.1',
 'simplemediawiki>=1.2.0b2,<2.0.0',
 'waitress>=1.4.4']

entry_points = \
{'console_scripts': ['bodhi-approve-testing = '
                     'bodhi.server.scripts.compat:approve_testing',
                     'bodhi-check-policies = '
                     'bodhi.server.scripts.compat:check_policies',
                     'bodhi-clean-old-composes = '
                     'bodhi.server.scripts.compat:clean_old_composes',
                     'bodhi-expire-overrides = '
                     'bodhi.server.scripts.compat:expire_overrides',
                     'bodhi-push = bodhi.server.push:push',
                     'bodhi-sar = bodhi.server.scripts.sar:get_user_data',
                     'bodhi-shell = '
                     'bodhi.server.scripts.bshell:get_bodhi_shell',
                     'bodhi-skopeo-lite = '
                     'bodhi.server.scripts.skopeo_lite:main',
                     'bodhi-untag-branched = '
                     'bodhi.server.scripts.untag_branched:main',
                     'initialize_bodhi_db = '
                     'bodhi.server.scripts.initializedb:main'],
 'paste.app_factory': ['main = bodhi.server:main']}

setup_kwargs = {
    'name': 'bodhi-server',
    'version': '7.0.1',
    'description': 'Bodhi server',
    'long_description': "=====\nBodhi\n=====\n\nWelcome to Bodhi, Fedora's update gating system.\n\nBodhi is designed to democratize the package update testing and release process for RPM based Linux\ndistributions. It provides an interface for developers to propose updates to a distribution, and an\ninterface for testers to leave feedback about updates through a +1/-1 karma system.\n\nBodhi’s main features are:\n\n\n- Provides an interface for developers and release engineers to manage pushing out package updates\n  for multiple distribution versions.\n- Generates pre-release test repositories for end users and testers to install proposed updates.\n- Gives testers an interface to leave feedback about package updates, leading to higher quality\n  package updates.\n- Announces the arrival of new packages entering the collection.\n- Publishes end-user release notes known as errata.\n- Generates yum repositories.\n- Queries ResultsDB for automated test results and displays them on updates.\n\n\n\nDocumentation\n=============\n\nYou can read Bodhi's\n`release notes <https://fedora-infra.github.io/bodhi/user/release_notes.html>`_\nand documentation `online <https://fedora-infra.github.io/bodhi>`_.\n\nIf you are interested in contributing to Bodhi, you can read the\n`developer documentation`_.\n\n.. _developer documentation: https://fedora-infra.github.io/bodhi/docs/developer/index.html\n\n\nIRC\n===\n\nCome join us on `Libera <https://www.libera.chat/>`_! We've got two channels:\n\n* #bodhi - We use this channel to discuss upstream bodhi development\n* #fedora-apps - We use this channel to discuss Fedora's Bodhi deployment (it is more generally\n  about all of Fedora's infrastructure applications.)\n",
    'author': 'Fedora Infrastructure Team',
    'author_email': 'None',
    'maintainer': 'Fedora Infrastructure Team',
    'maintainer_email': 'infrastructure@lists.fedoraproject.org',
    'url': 'https://bodhi.fedoraproject.rog',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
