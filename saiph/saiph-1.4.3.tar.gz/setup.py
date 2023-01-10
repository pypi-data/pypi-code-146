# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['saiph',
 'saiph.lib',
 'saiph.reduction',
 'saiph.reduction.utils',
 'saiph.tests']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21,<2.0',
 'pandas>=1.3,<2.0',
 'pydantic>=1.10.4,<2.0.0',
 'scikit-learn>=1.0,<2.0',
 'scipy>=1.7,<2.0',
 'toolz>=0.11.2,<0.12.0']

extras_require = \
{'matplotlib': ['matplotlib>=3.5.2,<4.0.0']}

setup_kwargs = {
    'name': 'saiph',
    'version': '1.4.3',
    'description': 'A projection package',
    'long_description': 'None',
    'author': 'Octopize',
    'author_email': 'help@octopize.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
