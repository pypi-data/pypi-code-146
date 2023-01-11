# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py3toolkit']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'dataclasses-json>=0.5.7,<0.6.0',
 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'py3toolkit',
    'version': '0.1.2',
    'description': 'my python3 toolkit for daily use',
    'long_description': 'None',
    'author': 'codeskyblue',
    'author_email': 'codeskyblue@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
