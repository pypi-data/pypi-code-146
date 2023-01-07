# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['circuitsvis',
 'circuitsvis.tests',
 'circuitsvis.tests.snapshots',
 'circuitsvis.utils',
 'circuitsvis.utils.tests',
 'circuitsvis.utils.tests.snapshots']

package_data = \
{'': ['*'], 'circuitsvis': ['dist/cdn/*']}

install_requires = \
['importlib-metadata>=5.1.0,<6.0.0', 'numpy>=1.20,<2.0']

extras_require = \
{':sys_platform != "linux"': ['torch>=1,<1.13'],
 ':sys_platform == "linux"': ['torch>=1,<2']}

setup_kwargs = {
    'name': 'circuitsvis',
    'version': '1.36.0',
    'description': 'Mechanistic Interpretability Visualizations',
    'long_description': '# Circuits Vis\n\nMechanistic Interpretability visualizations.\n',
    'author': 'Alan Cooney',
    'author_email': '41682961+alan-cooney@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
