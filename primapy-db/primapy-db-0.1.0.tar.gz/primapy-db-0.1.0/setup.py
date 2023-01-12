# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['primapy_db']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'primapy-db',
    'version': '0.1.0',
    'description': 'Python DB library',
    'long_description': '',
    'author': 'Team AMOps',
    'author_email': 'amops@prima.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
