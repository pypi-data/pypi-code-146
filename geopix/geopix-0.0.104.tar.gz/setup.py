# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geopix']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.10.4,<0.11.0', 'loguru>=0.6.0,<0.7.0']

setup_kwargs = {
    'name': 'geopix',
    'version': '0.0.104',
    'description': 'Helper functions to convert geo coords to pixel coords and back.',
    'long_description': '# geopix\n\n## Installation\n```sh\npip install geopix\n```\n\n## Getting Started\nSee tests.\n',
    'author': 'Michael Mohamed',
    'author_email': 'michael@foundationstack.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fsai-dev/fsai-cli-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
