# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytamaro', 'pytamaro.de', 'pytamaro.it']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0', 'skia-python>=87.4,<88.0']

setup_kwargs = {
    'name': 'pytamaro',
    'version': '0.3.1',
    'description': 'Educational library for teaching problem decompositon using graphics',
    'long_description': 'None',
    'author': 'Luca Chiodini',
    'author_email': 'luca@chiodini.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
