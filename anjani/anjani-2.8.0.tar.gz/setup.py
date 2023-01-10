# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anjani',
 'anjani.core',
 'anjani.custom_plugins',
 'anjani.language',
 'anjani.plugins',
 'anjani.util',
 'anjani.util.db']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'Pyrogram>=2.0.93,<3.0.0',
 'TgCrypto>=1.2.5,<2.0.0',
 'aiohttp>=3.8.3,<4.0.0',
 'aiorun>=2022.11.1,<2023.0.0',
 'colorlog>=6.7.0,<7.0.0',
 'meval>=2.5,<3.0',
 'pymongo>=4.3.3,<5.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'typing-extensions>=4.4.0,<5.0.0']

extras_require = \
{':python_version < "3.10"': ['aiopath>=0.5.12,<0.6.0'],
 ':python_version >= "3.10"': ['aiopath>=0.6.11,<0.7.0'],
 ':sys_platform == "windows"': ['certifi>=2022.12.7,<2023.0.0'],
 'all': ['scikit-learn==1.2.0'],
 'all:sys_platform == "linux"': ['uvloop>=0.17.0,<0.18.0'],
 'ml': ['scikit-learn==1.2.0'],
 'uvloop:sys_platform == "linux"': ['uvloop>=0.17.0,<0.18.0']}

entry_points = \
{'console_scripts': ['anjani = anjani.main:start']}

setup_kwargs = {
    'name': 'anjani',
    'version': '2.8.0',
    'description': 'Telegram group management bot',
    'long_description': "# Anjani\n\n[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)\n\n[![DeepSource](https://deepsource.io/gh/userbotindo/Anjani.svg/?label=active+issues)](https://deepsource.io/gh/userbotindo/Anjani/?ref=repository-badge)\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/23d2794692ad47a18849e06823aeaf6f)](https://www.codacy.com/gh/userbotindo/Anjani/dashboard?utm_source=github.com&utm_medium=referral&utm_content=userbotindo/Anjani&utm_campaign=Badge_Grade)\n\nCan be found on Telegram as [Anjani](https://t.me/dAnjani_bot).\n\nAnjani is a modern, easy-to-develop, fully async Telegram group managing bot for Telegram.\n\n## Requirements\n\n-   Python 3.9 or higher.\n-   [Telegram API key](https://docs.pyrogram.org/intro/setup#api-keys).\n-   [Telegram Bot Token](https://t.me/botfather)\n-   [MongoDB Database](https://cloud.mongodb.com/).\n\n## Features\n\n-   Easy to develop with object oriented models.\n-   Fully asynchronous with async / await.\n-   Type-hinted method making it easy to create plugins.\n-   Localization support.\n-   Class based plugin system.\n\n## [Documentation](https://userbotindo.com/anjani/docs/home)\n\n## [Installing](https://userbotindo.com/anjani/docs/install)\n\n## Plugin\n\nIf you want to make your custom plugins, refer to [Anjani's Plugins Guide](https://userbotindo.com/anjani/docs/plugin/creating-your-own-plugin).\n\n## Credits\n\n-   [Marie](https://github.com/PaulSonOfLars/tgbot)\n-   [Pyrobud](https://github.com/kdrag0n/pyrobud)\n-   [All Contributors 👥](https://github.com/userbotindo/Anjani/graphs/contributors)\n",
    'author': 'Gaung Ramadhan',
    'author_email': 'hi@mrmiss.my.id',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/userbotindo/anjani#readme',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<=3.11',
}


setup(**setup_kwargs)
