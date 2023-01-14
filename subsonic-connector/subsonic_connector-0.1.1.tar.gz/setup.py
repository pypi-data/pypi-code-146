# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subsonic_connector']

package_data = \
{'': ['*']}

install_requires = \
['py-sonic>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'subsonic-connector',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Subsonic Connector\n\n## Status\n\nThis software is in its early development phase.\n\n## Instructions\n\nCreate your own `.env` file. Use `.sample.env` as a reference for the format of the file.\n\n### Initialization\n\nFrom a terminal, type\n\n```text\npoetry shell\npoetry install\n```\n\n### Test execution\n\nThen you can run the simple test using the following command:\n\n```text\npython subsonic_connector/test-cn.py\n```\n\nMake sure to load the variables specified in the `.env` file.  \nThe test is currently just a `main`.\n',
    'author': 'GioF71',
    'author_email': 'giovanni.fulco@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
