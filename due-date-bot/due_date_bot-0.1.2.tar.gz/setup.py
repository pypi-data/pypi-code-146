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
    'version': '0.1.2',
    'description': 'Receive telegram messages with your pregnancy status.',
    'long_description': '# DueDateBot\n\nKeep track of your due date via a Telegram bot.\n\n### Usage\n\nSimply install from PyPI\n\n`pip install due-date-bot`\n\nor using Poetry\n\n`poetry install`\n\n\nand run\n\n`ddbot`, e.g.: `ddbot -l cz --token <bot-token> 2023-08-12`\n\n** Can be easily run as a systemd service as well.',
    'author': 'Jonas',
    'author_email': 'magicturtle423@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
