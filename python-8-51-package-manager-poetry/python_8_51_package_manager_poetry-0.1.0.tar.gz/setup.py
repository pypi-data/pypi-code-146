# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_8_51_package_manager_poetry', 'python_8_51_package_manager_poetry.km']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'python-8-51-package-manager-poetry',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Krzysztof',
    'author_email': 'programowanie.krzysiek@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
