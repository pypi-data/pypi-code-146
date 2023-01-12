# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['macrometa_target_postgres']

package_data = \
{'': ['*']}

install_requires = \
['c8connector==0.0.11',
 'inflection==0.3.1',
 'joblib==1.2.0',
 'pipelinewise-singer-python==1.2.0',
 'psycopg2-binary==2.9.3',
 'pylint==2.6.0',
 'pytest-cov==2.10.1',
 'pytest==6.2.5']

entry_points = \
{'console_scripts': ['macrometa-target-postgres = '
                     'macrometa_target_postgres:main']}

setup_kwargs = {
    'name': 'macrometa-target-postgres',
    'version': '0.0.4',
    'description': 'Pipelinewise target for writing data into Postgres.',
    'long_description': 'None',
    'author': 'Macrometa',
    'author_email': 'info@macrometa.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.11',
}


setup(**setup_kwargs)
