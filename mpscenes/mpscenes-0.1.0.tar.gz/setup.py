# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mpscenes', 'mpscenes.common', 'mpscenes.goals', 'mpscenes.obstacles']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'geomdl>=5.3.1,<6.0.0',
 'numpy>=1.22.0,<2.0.0',
 'omegaconf>=2.2.2,<3.0.0',
 'pyquaternion>=0.9.9,<0.10.0',
 'sympy>=1.7,<2.0']

extras_require = \
{'bullet': ['pybullet>=3.2.3,<4.0.0']}

setup_kwargs = {
    'name': 'mpscenes',
    'version': '0.1.0',
    'description': 'Generic motion planning scenes, including goals and obstacles.',
    'long_description': 'None',
    'author': 'Max',
    'author_email': 'm.spahn@tudelft.nl',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
