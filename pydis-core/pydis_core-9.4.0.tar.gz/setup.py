# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydis_core', 'pydis_core.exts', 'pydis_core.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiodns==3.0.0', 'discord.py==2.1.0', 'statsd==4.0.1']

extras_require = \
{'async-rediscache': ['async-rediscache[fakeredis]==1.0.0rc2']}

setup_kwargs = {
    'name': 'pydis-core',
    'version': '9.4.0',
    'description': 'PyDis core provides core functionality and utility to the bots of the Python Discord community.',
    'long_description': '# bot-core ![Version]\n\n[Version]: https://img.shields.io/github/v/tag/python-discord/bot-core?label=latest&logo=version\n',
    'author': 'Python Discord',
    'author_email': 'info@pythondiscord.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pythondiscord.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.10.0,<3.12.0',
}


setup(**setup_kwargs)
