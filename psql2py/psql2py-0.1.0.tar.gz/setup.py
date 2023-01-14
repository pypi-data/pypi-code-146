# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['psql2py']

package_data = \
{'': ['*'], 'psql2py': ['templates/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'docstring-parser>=0.15,<0.16',
 'jinja2>=3.1.2,<4.0.0',
 'pg-docker>=0.5.0,<0.6.0',
 'psycopg2>=2.9.5,<3.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'sqlparse>=0.4.3,<0.5.0',
 'watchdog>=2.2.1,<3.0.0']

setup_kwargs = {
    'name': 'psql2py',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
