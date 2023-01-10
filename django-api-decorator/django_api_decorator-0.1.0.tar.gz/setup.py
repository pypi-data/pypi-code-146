# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_api_decorator',
 'django_api_decorator.management',
 'django_api_decorator.management.commands']

package_data = \
{'': ['*']}

install_requires = \
['Django>=3', 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'django-api-decorator',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Orhan Hirsch',
    'author_email': 'orhan.hirsch@oda.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
