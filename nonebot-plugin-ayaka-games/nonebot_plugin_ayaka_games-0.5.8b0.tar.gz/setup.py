# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ayaka_games']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-plugin-ayaka>=1.0.3b1,<1.1.0', 'pypinyin>=0.47.1,<0.48.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka-games',
    'version': '0.5.8b0',
    'description': 'ayaka小游戏合集',
    'long_description': '<div align="center">\n\n# ayaka文字小游戏合集 - 0.5.8b0\n\n基于[ayaka](https://github.com/bridgeL/nonebot-plugin-ayaka)开发的文字小游戏合集\n\n开发进度 9/10，还剩1个小游戏等待构思\n\n**特别感谢**  [@灯夜](https://github.com/lunexnocty/Meiri) 大佬的插件蛮好玩的~\n\n</div>\n\n## 文档\n\nhttps://bridgel.github.io/ayaka_doc/latest/games/game/\n\n## 踩坑\n\nCRLF换行符的文件，会在github上被强制换为LF换行符再发放，这会导致文件哈希值变化\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/nonebot-plugin-ayaka-games',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
