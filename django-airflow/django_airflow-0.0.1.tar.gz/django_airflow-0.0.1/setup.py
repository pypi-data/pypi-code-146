# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_airflow']

package_data = \
{'': ['*']}

install_requires = \
['apache-airflow>=2.0', 'django>=3.2']

setup_kwargs = {
    'name': 'django-airflow',
    'version': '0.0.1',
    'description': 'using Django features in Airflow DAG',
    'long_description': '# django-airflow\ndjango airflow\n',
    'author': 'Youngkwang Yang',
    'author_email': 'immutable000@gmail.com',
    'maintainer': 'Youngkwang Yang',
    'maintainer_email': 'immutable000@gmail.com',
    'url': 'https://github.com/2ykwang/django-airflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
