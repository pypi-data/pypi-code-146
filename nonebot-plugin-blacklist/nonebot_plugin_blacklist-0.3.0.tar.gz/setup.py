# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_blacklist']

package_data = \
{'': ['*']}

install_requires = \
['nonebot-adapter-onebot>=2.2.0,<3.0.0', 'nonebot2>=2.0.0-rc.2,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-blacklist',
    'version': '0.3.0',
    'description': 'Blacklist in NoneBot2',
    'long_description': '<div align="center">\n  <a href="https://v2.nonebot.dev/store"><img src="https://raw.githubusercontent.com/tkgs0/nbpt/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>\n  <br>\n  <p><img src="https://raw.githubusercontent.com/tkgs0/nbpt/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>\n</div>\n\n<div align="center">\n\n# nonebot-plugin-blacklist\n\n_✨ NoneBot 黑名单插件 ✨_\n\n\n<a href="./LICENSE">\n    <img src="https://img.shields.io/github/license/tkgs0/nonebot-plugin-blacklist.svg" alt="license">\n</a>\n<a href="https://pypi.python.org/pypi/nonebot-plugin-blacklist">\n    <img src="https://img.shields.io/pypi/v/nonebot-plugin-blacklist.svg" alt="pypi">\n</a>\n<a href="https://www.python.org">\n    <img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">\n</a>\n\n</div>\n\n  \n## 📖 介绍\n  \n基于 [A-kirami](https://github.com/A-kirami) 大佬的 [黑白名单](https://github.com/A-kirami/nonebot-plugin-namelist) 插件 魔改(?)的仅黑名单插件  \n  \n超级用户不受黑名单影响  \n  \n## 💿 安装\n  \n**使用 nb-cli 安装**  \n在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装  \n```bash\nnb plugin install nonebot-plugin-blacklist\n```\n  \n**使用 pip 安装**  \n```bash\npip install nonebot-plugin-blacklist\n```\n  \n打开 nonebot2 项目的 `bot.py` 文件, 在其中写入\n```python\nnonebot.load_plugin(\'nonebot_plugin_blacklist\')\n```\n  \n## 🎉 使用\n  \n拉黑:  \n```\n拉黑用户 qq qq1 qq2\n拉黑群 qq qq1 qq2\n拉黑所有群\n拉黑所有好友\n```\n  \n解禁:  \n```\n解禁用户 qq qq1 qq2\n解禁群 qq qq1 qq2\n解禁所有群\n解禁所有好友\n```\n  \n查看黑名单:  \n```\n查看用户黑名单\n查看群聊黑名单\n\n重置黑名单\n```\n  \n群内发送 **`/静默`**, **`/响应`** 可快捷拉黑/解禁当前群聊  \n`拉黑/解禁所有` 只对已添加的群/好友生效  \n  \n',
    'author': '月ヶ瀬',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tkgs0/nonebot-plugin-blacklist',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
