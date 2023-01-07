# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigma', 'sigma.backends.elasticsearch', 'sigma.pipelines.elasticsearch']

package_data = \
{'': ['*']}

install_requires = \
['pysigma>=0.8.12,<0.9.0']

setup_kwargs = {
    'name': 'pysigma-backend-elasticsearch',
    'version': '0.1.2',
    'description': 'pySigma Elasticsearch backend',
    'long_description': 'None',
    'author': 'Thomas Patzke',
    'author_email': 'thomas@patzke.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/SigmaHQ/pySigma-backend-elasticsearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
