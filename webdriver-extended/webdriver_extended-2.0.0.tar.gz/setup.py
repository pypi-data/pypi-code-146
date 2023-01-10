# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webdriver_extended', 'webdriver_extended.chrome']

package_data = \
{'': ['*']}

install_requires = \
['selenium>=4.0.0']

setup_kwargs = {
    'name': 'webdriver-extended',
    'version': '2.0.0',
    'description': '',
    'long_description': '# `webdriver-extended`\n\n`webdriver-extended` is a `webdriver` with more features. Only Chrome is supported at the moment.\n\nRead the dosctrings of the code to understand the features. They include but are not limited to file downloading support, checking if headless, and opening a new tab.\n',
    'author': 'Zeke Marffy',
    'author_email': 'zmarffy@me.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
