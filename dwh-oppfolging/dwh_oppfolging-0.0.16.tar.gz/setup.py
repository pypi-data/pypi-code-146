# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dwh_oppfolging',
 'dwh_oppfolging.apis',
 'dwh_oppfolging.db',
 'dwh_oppfolging.misc']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-secret-manager>=2.12.6,<3.0.0',
 'ijson>=3.1.4,<4.0.0',
 'oracledb>=1.2.1,<2.0.0',
 'pendulum>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'dwh-oppfolging',
    'version': '0.0.16',
    'description': 'Oppfolging python package for DWH ETL',
    'long_description': 'None',
    'author': 'Team Oppfolging',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
