# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_chess']

package_data = \
{'': ['*']}

install_requires = \
['chess>=1.9.0,<2.0.0',
 'nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0',
 'nonebot-plugin-datastore>=0.4.0,<0.5.0',
 'nonebot-plugin-htmlrender>=0.0.4',
 'nonebot2>=2.0.0-rc.1,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-chess',
    'version': '0.2.9',
    'description': 'Nonebot2 国际象棋插件',
    'long_description': '## nonebot-plugin-chess\n\n适用于 [Nonebot2](https://github.com/nonebot/nonebot2) 的国际象棋插件。\n\n\n### 安装\n\n- 使用 nb-cli\n\n```\nnb plugin install nonebot_plugin_chess\n```\n\n- 使用 pip\n\n```\npip install nonebot_plugin_chess\n```\n\n\n人机功能 需要使用遵循 [UCI协议](https://www.xqbase.com/protocol/uci.htm) 的引擎\n\n需要在 `.env` 文件中添加 引擎的可执行文件的路径\n\n```\nchess_engine_path=/path/to/your/engine\n```\n\n推荐的引擎：\n\n - [Stockfish](https://stockfishchess.org/)\n\n\n### 使用\n\n**以下命令需要加[命令前缀](https://v2.nonebot.dev/docs/api/config#Config-command_start) (默认为`/`)，可自行设置为空**\n\n@我 + “国际象棋人机”或“国际象棋对战”开始一局游戏；\n\n可使用“lv1~8”指定AI等级，如“国际象棋人机lv5”，默认为“lv4”；\n\n发送 起始坐标格式，如“e2e4”下棋；\n\n在坐标后加棋子字母表示升变，如“e7e8q”表示升变为后；\n\n对应的字母：K：王，Q：后，B：象，N：马，R：车，P：兵\n\n发送“结束下棋”结束当前棋局；\n\n发送“显示棋盘”显示当前棋局；\n\n发送“悔棋”可进行悔棋（人机模式可无限悔棋；对战模式只能撤销自己上一手下的棋）；\n\n\n或者使用 `chess` 指令：\n\n可用选项：\n\n - `-e`, `--stop`, `--end`: 停止下棋\n - `-v`, `--show`, `--view`: 显示棋盘\n - `--repent`: 悔棋\n - `--reload`: 重新加载已停止的游戏\n - `--battle`: 对战模式，默认为人机模式\n - `--black`: 执黑，即后手\n - `-l <LEVEL>`, `--level <LEVEL>`: 人机等级，可选 1~8，默认为 4\n\n\n### 示例\n\n<div align="left">\n    <img src="https://s2.loli.net/2022/05/02/1gqSQUfnLuvkpAm.png" width="500" />\n</div>\n\n\n### 特别感谢\n\n- [niklasf/python-chess](https://github.com/niklasf/python-chess) A chess library for Python\n- [official-stockfish/Stockfish](https://github.com/official-stockfish/Stockfish) UCI chess engine\n',
    'author': 'meetwq',
    'author_email': 'meetwq@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/noneplugin/nonebot-plugin-chess',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
