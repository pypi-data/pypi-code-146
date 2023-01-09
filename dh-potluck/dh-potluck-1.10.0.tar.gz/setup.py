# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dh_potluck',
 'dh_potluck.celery',
 'dh_potluck.email',
 'dh_potluck.messaging',
 'dh_potluck.types',
 'dh_potluck.utils']

package_data = \
{'': ['*'], 'dh_potluck': ['templates/*']}

install_requires = \
['Flask>=2.1.3,<2.2.0',
 'boltons>=20.2.1,<21.0.0',
 'boto3>=1.25.4,<2.0.0',
 'confluent-kafka>=1.8.2,<1.9.0',
 'ddtrace==1.1.1',
 'flask-limiter>=2.7.0,<3.0.0',
 'flask-redis>=0.4.0,<0.5.0',
 'flask-smorest>=0.40.0,<0.41.0',
 'flask_sqlalchemy>=2.4.4,<3.0.0',
 'json-log-formatter>=0.3.0,<0.4.0',
 'mandrill>=1.0.60,<2.0.0',
 'marshmallow>=3.18.0,<4.0.0',
 'mixpanel>=4.10.0,<5.0.0',
 'requests>=2.28.1,<3.0.0',
 'setuptools>=65.5.0,<66.0.0',
 'sqlalchemy>=1.3,<2.0',
 'werkzeug>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'dh-potluck',
    'version': '1.10.0',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
