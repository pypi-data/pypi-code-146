# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['utbot_mypy_runner']

package_data = \
{'': ['*']}

install_requires = \
['mypy==0.971']

setup_kwargs = {
    'name': 'utbot-mypy-runner',
    'version': '0.1.18',
    'description': '',
    'long_description': '',
    'author': 'Ekaterina Tochilina',
    'author_email': 'katerina_t_n@mail.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
