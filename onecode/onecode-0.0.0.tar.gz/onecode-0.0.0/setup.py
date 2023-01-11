# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['onecode']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['onecode-add = onecode.cli.add:main',
                     'onecode-create = onecode.cli.create:main',
                     'onecode-extract = onecode.cli.extract:main',
                     'onecode-start = onecode.cli.start:main']}

setup_kwargs = {
    'name': 'onecode',
    'version': '0.0.0',
    'description': 'Python skeleton and library for OneCode procedures',
    'long_description': '# OneCode\n',
    'author': 'DeepLime',
    'author_email': 'support@deeplime.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/deeplime-io/onecode',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
