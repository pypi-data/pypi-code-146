# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_gamedraw', 'nonebot_plugin_gamedraw.handles']

package_data = \
{'': ['*'], 'nonebot_plugin_gamedraw': ['resources/fonts/*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'aiofiles>=0.8.0,<0.9.0',
 'aiohttp>=3.7.4,<4.0.0',
 'cachetools>=5.0.0,<6.0.0',
 'cn2an>=0.5.16,<0.6.0',
 'dateparser>=1.1.0,<2.0.0',
 'lxml>=4.6.3,<5.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-apscheduler>=0.2.0,<0.3.0',
 'nonebot2>=2.0.0-beta.1,<3.0.0',
 'pypinyin>=0.42.0',
 'typing-extensions>=3.10.0,<5.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-gamedraw',
    'version': '0.4.2',
    'description': 'nonebot2 实现自动更新的 原神/明日方舟/赛马娘/坎公骑冠剑/公主连结/碧蓝航线/FGO/阴阳师 抽卡插件',
    'long_description': '',
    'author': 'HibiKier',
    'author_email': '775757368@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/HibiKier/nonebot_plugin_gamedraw',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<4.0.0',
}


setup(**setup_kwargs)
