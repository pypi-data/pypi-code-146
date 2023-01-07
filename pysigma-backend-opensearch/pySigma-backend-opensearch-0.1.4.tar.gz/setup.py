# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sigma', 'sigma.backends.opensearch']

package_data = \
{'': ['*']}

install_requires = \
['pysigma-backend-elasticsearch>=0.1.2,<0.2.0', 'pysigma>=0.8.12,<0.9.0']

setup_kwargs = {
    'name': 'pysigma-backend-opensearch',
    'version': '0.1.4',
    'description': 'pySigma OpenSearch backend',
    'long_description': 'None',
    'author': 'Hendrik Baecker',
    'author_email': 'hendrik.baecker@dcso.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/SigmaHQ/pySigma-backend-opensearch',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
