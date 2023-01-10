# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pycta']

package_data = \
{'': ['*']}

install_requires = \
['pandas', 'plotly']

setup_kwargs = {
    'name': 'tinycta',
    'version': '0.0.4',
    'description': '...',
    'long_description': '# TinyCTA\n\nUnderlying package for the 10-line cta\n',
    'author': 'Thomas Schmelzer',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tschm/TinyCTA',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.0,<3.11',
}


setup(**setup_kwargs)
