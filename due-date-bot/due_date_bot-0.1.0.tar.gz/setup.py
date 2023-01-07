# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ddbot']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0', 'python-telegram-bot[job-queue]>=20.0,<21.0']

entry_points = \
{'console_scripts': ['ddbot = ddbot.app:main']}

setup_kwargs = {
    'name': 'due-date-bot',
    'version': '0.1.0',
    'description': 'Receive telegram messages with pregnancy status',
    'long_description': '# DueDateBot\n\nReceive telegram messages with\n\n`$ ddbot 2023-12-06 -l cz --token <your-bot-token> `',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
