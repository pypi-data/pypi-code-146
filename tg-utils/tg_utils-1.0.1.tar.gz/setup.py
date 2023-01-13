# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tg_utils',
 'tg_utils.health_check',
 'tg_utils.health_check.checks',
 'tg_utils.health_check.checks.celery_beat',
 'tg_utils.health_check.checks.elvis',
 'tg_utils.health_check.checks.phantomjs']

package_data = \
{'': ['*'],
 'tg_utils': ['locale/et/LC_MESSAGES/*',
              'templates/admin/edit_inline/no_obj_head/*']}

install_requires = \
['django>=2.2']

extras_require = \
{'health-check': ['django-health-check', 'psutil', 'requests'],
 'lock': ['python-redis-lock', 'redis'],
 'model-hash': ['hashids'],
 'profiling': ['yappi']}

setup_kwargs = {
    'name': 'tg-utils',
    'version': '1.0.1',
    'description': 'Common utils for Django-based projects.',
    'long_description': "===============================\ntg-utils\n===============================\n\n.. image:: https://img.shields.io/pypi/v/tg-utils.svg\n        :target: https://pypi.python.org/pypi/tg-utils\n\n.. image:: https://github.com/thorgate/tg-utils/actions/workflows/python-package.yml/badge.svg?branch=master\n        :target: https://github.com/thorgate/tg-utils/actions\n\n.. image:: https://readthedocs.org/projects/tg-utils/badge/?version=latest\n        :target: https://readthedocs.org/projects/tg-utils/?badge=latest\n        :alt: Documentation Status\n\n\nCollection of various utils for Django-based projects.\n\nThis is code that we're using in our projects at Thorgate and we're hoping you'll find some of it useful as well.\n\n* Free software: ISC license\n* Documentation: https://tg-utils.readthedocs.org.\n\n\nFeatures\n--------\n\n* Model utils, e.g. timestamped and closable models, QuerySets that send out a signal when objects are modified.\n* Templated email sending.\n* Profiling utilities.\n* Unique filename generation for uploads.\n* Using hashids for models (instead of exposing primary keys).\n* System checks for email and Sentry configuration.\n* Mixin for easier implementation of ordering in Django's generic ListView.\n* Mixin for making admin view read-only.\n* Decorator for annotating admin methods.\n* JS/CSS compressors for `Django Compressor <https://django-compressor.readthedocs.org/en/latest/>`_.\n* Health-check endpoints (with and without token authentication)\n\n\nCredits\n---------\n\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n",
    'author': 'Thorgate',
    'author_email': 'code@thorgate.eu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/thorgate/tg-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.2,<4',
}


setup(**setup_kwargs)
