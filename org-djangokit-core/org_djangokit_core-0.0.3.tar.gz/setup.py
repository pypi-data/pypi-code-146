# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['djangokit',
 'djangokit.core',
 'djangokit.core.templates',
 'djangokit.core.test',
 'djangokit.core.test.routes',
 'djangokit.core.test.routes._slug',
 'djangokit.core.test.routes.catchall',
 'djangokit.core.test.routes.docs._slug',
 'djangokit.core.views']

package_data = \
{'': ['*'],
 'djangokit.core': ['app/*', 'static/*', 'static/build/*'],
 'djangokit.core.templates': ['djangokit/*', 'djangokit/base/*'],
 'djangokit.core.test': ['static/*'],
 'djangokit.core.test.routes': ['docs/*']}

install_requires = \
['Django>=3.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'org-djangokit-core',
    'version': '0.0.3',
    'description': 'DjangoKit core',
    'long_description': '# DjangoKit Core\n\n> NOTE: DjangoKit is a full stack Django+React framework. See\n> https://djangokit.org/ for more information.\n\nThis package implements the core functionality of DjangoKit.\n',
    'author': 'Wyatt Baldwin',
    'author_email': 'self@wyattbaldwin.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
