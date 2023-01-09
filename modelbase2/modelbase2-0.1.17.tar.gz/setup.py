# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['modelbase2', 'modelbase2.core', 'modelbase2.ode', 'modelbase2.utils']

package_data = \
{'': ['*']}

install_requires = \
['black>=22.3.0,<23.0.0',
 'ipywidgets>=8.0.0,<9.0.0',
 'matplotlib>=3.5.0,<4.0.0',
 'modelbase>=1.14.0,<2.0.0',
 'numpy>=1.21.4,<2.0.0',
 'pandas>=1.3.4,<2.0.0',
 'python-libsbml>=5.19.2,<6.0.0',
 'scipy>=1.7.2,<2.0.0',
 'sympy>=1.9,<2.0',
 'tqdm>=4.62.3,<5.0.0',
 'typing-extensions>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'modelbase2',
    'version': '0.1.17',
    'description': 'A package to build metabolic models',
    'long_description': 'None',
    'author': 'Marvin van Aalst',
    'author_email': 'marvin.vanaalst@gmail.com',
    'maintainer': 'Marvin van Aalst',
    'maintainer_email': 'marvin.vanaalst@gmail.com',
    'url': 'https://gitlab.com/qtb-hhu/modelbase-software',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
