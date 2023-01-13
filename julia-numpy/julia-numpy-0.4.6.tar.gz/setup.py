# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jnumpy', 'jnumpy.tests', 'jnumpy.tests.extension']

package_data = \
{'': ['*'],
 'jnumpy': ['JNumPyEnv/*', 'TyPython/Project.toml', 'TyPython/src/*'],
 'jnumpy.tests.extension': ['src/*']}

install_requires = \
['numpy>=1.18,<2.0', 'tomli>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'julia-numpy',
    'version': '0.4.6',
    'description': 'Writing Python C extensions in Julia within 5 minutes.',
    'long_description': None,
    'author': 'thautwarm',
    'author_email': 'twshere@outlook.com',
    'maintainer': 'songjhaha',
    'maintainer_email': 'songjh96@foxmail.com',
    'url': 'https://github.com/Suzhou-Tongyuan/jnumpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
