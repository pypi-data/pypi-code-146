# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datasets_genie']

package_data = \
{'': ['*']}

install_requires = \
['faker>=15.3.4,<16.0.0']

setup_kwargs = {
    'name': 'datasets-genie',
    'version': '0.1.1',
    'description': 'Package for generating fake data in CSV, JSON, and XML formats. It can be used to create placeholder data for testing or demonstration purposes.',
    'long_description': '# datasets-genie\n\npackage for generating fake data in CSV, JSON, and XML formats. It can be used to create placeholder data for testing or demonstration purposes.\n\n```\npip install datasets-genie\n```\n\n',
    'author': 'Sai Ranga Reddy Nukala',
    'author_email': 'sairangareddy22@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
