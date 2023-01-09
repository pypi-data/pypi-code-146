# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labos']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.6.2,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'scikit-learn>=1.2.0,<2.0.0',
 'scipy>=1.10.0,<2.0.0',
 'sympy>=1.11.1,<2.0.0',
 'telegram>=0.0.1,<0.0.2']

setup_kwargs = {
    'name': 'labos',
    'version': '0.1.0',
    'description': 'Paquete para trabajar en el labo',
    'long_description': '',
    'author': 'joctavio287',
    'author_email': 'joctavio287@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.11.1',
}


setup(**setup_kwargs)
