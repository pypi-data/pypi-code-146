# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mongo_tooling_metrics', 'mongo_tooling_metrics.lib']

package_data = \
{'': ['*']}

install_requires = \
['distro>=1.5.0,<2.0.0',
 'gitpython>=3.1.29,<4.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'pymongo>=4.3.3,<5.0.0',
 'setuptools>=58.1.0,<59.0.0']

setup_kwargs = {
    'name': 'mongo-tooling-metrics',
    'version': '0.0.11',
    'description': 'A slim library which leverages Pydantic to reliably collect type enforced metrics and store them to MongoDB.',
    'long_description': 'None',
    'author': 'Tausif Rahman',
    'author_email': 'tausif.rahman@mongodb.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
