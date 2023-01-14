# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meteo_render']

package_data = \
{'': ['*'], 'meteo_render': ['templates/family/*', 'templates/family/img/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0', 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'meteo-render',
    'version': '0.1.0',
    'description': 'Retrieve open-meteo.com data and render it into HTML pages',
    'long_description': None,
    'author': 'Jack Grahl',
    'author_email': 'jack.grahl@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
