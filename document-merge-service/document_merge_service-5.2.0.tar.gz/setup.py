# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['document_merge_service',
 'document_merge_service.api',
 'document_merge_service.api.data',
 'document_merge_service.api.management',
 'document_merge_service.api.management.commands',
 'document_merge_service.api.migrations',
 'document_merge_service.api.tests',
 'document_merge_service.api.tests.snapshots',
 'document_merge_service.tests']

package_data = \
{'': ['*'], 'document_merge_service.api.data': ['loadtest/*']}

install_requires = \
['Babel>=2.11.0,<3.0.0',
 'Django>=3.2.16,<4.0.0',
 'Jinja2>=3.1.2,<4.0.0',
 'django-cors-headers>=3.13.0,<4.0.0',
 'django-environ>=0.9.0,<0.10.0',
 'django-filter>=22.1,<23.0',
 'django-generic-api-permissions>=0.2.0,<0.3.0',
 'djangorestframework>=3.14.0,<4.0.0',
 'docx-mailmerge>=0.5.0,<0.6.0',
 'docxtpl>=0.16.4,<0.17.0',
 'openpyxl>=3.0.10,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'python-memcached>=1.59,<2.0',
 'requests>=2.28.1,<3.0.0',
 'uWSGI>=2.0.21,<3.0.0',
 'xltpl>=0.16,<0.17']

extras_require = \
{'databases': ['mysqlclient>=2.1.1,<3.0.0', 'psycopg2-binary>=2.9.5,<3.0.0'],
 'mysql': ['mysqlclient>=2.1.1,<3.0.0'],
 'pgsql': ['psycopg2-binary>=2.9.5,<3.0.0']}

setup_kwargs = {
    'name': 'document-merge-service',
    'version': '5.2.0',
    'description': 'Merge Document Template Service',
    'long_description': 'None',
    'author': 'Adfinis AG',
    'author_email': 'None',
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
