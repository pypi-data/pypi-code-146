# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['airplane', 'airplane.api', 'airplane.builtins', 'airplane.runtime']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=1.10.0,<2.0.0',
 'deprecation>=2.1.0,<3.0.0',
 'docstring-parser>=0.14.1,<0.15.0',
 'inflection>=0.5.1,<0.6.0',
 'python-slugify>=6.1.2,<7.0.0',
 'requests>=2.25.1,<3.0.0',
 'typing-extensions>=4.3.0,<5.0.0']

setup_kwargs = {
    'name': 'airplanesdk',
    'version': '0.3.15',
    'description': 'A Python SDK for writing Airplane tasks',
    'long_description': '# Airplane Python SDK [![PyPI](https://img.shields.io/pypi/v/airplanesdk)](https://pypi.org/project/airplanesdk/) [![PyPI - License](https://img.shields.io/pypi/l/airplanesdk)](./LICENSE) [![Docs](https://img.shields.io/badge/Docs-airplane-blue)](https://docs.airplane.dev/creating-tasks/python)\n\nSDK for writing [Airplane](https://airplane.dev) tasks in Python.\n\nTo learn more, see [the Airplane SDK docs](https://docs.airplane.dev/tasks/python-sdk).\n',
    'author': 'Airplane',
    'author_email': 'support@airplane.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://airplane.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
