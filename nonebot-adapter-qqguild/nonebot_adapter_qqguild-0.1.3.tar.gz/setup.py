# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot', 'nonebot.adapters.qqguild', 'nonebot.adapters.qqguild.api']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0-beta.1,<3.0.0', 'pydantic>=1.9.0,<2.0.0']

setup_kwargs = {
    'name': 'nonebot-adapter-qqguild',
    'version': '0.1.3',
    'description': 'QQ Guild adapter for nonebot2',
    'long_description': '<p align="center">\n  <a href="https://v2.nonebot.dev/"><img src="https://raw.githubusercontent.com/nonebot/adapter-qqguild/master/website/static/img/logo.png" width="500" alt="nonebot-adapter-onebot"></a>\n</p>\n\n<div align="center">\n\n# NoneBot-Adapter-QQGuild\n\n_✨ QQ 频道协议适配 ✨_\n\n</div>\n\n## 配置\n\n修改 NoneBot 配置文件 `.env` 或者 `.env.*`。\n\n### Driver\n\n参考 [driver](https://v2.nonebot.dev/docs/tutorial/configuration#driver) 配置项，添加 `ForwardDriver` 支持。\n\n如：\n\n```dotenv\nDRIVER=~httpx+~websockets\nDRIVER=~aiohttp\n```\n\n### QQGUILD_IS_SANDBOX\n\n是否为沙盒模式，默认为 `False`。\n\n```dotenv\nQQGUILD_IS_SANDBOX=true\n```\n\n### QQGUILD_BOTS\n\n配置机器人帐号，如：\n\n```dotenv\nQQGUILD_BOTS=\'\n[\n  {\n    "id": "xxx",\n    "token": "xxx",\n    "secret": "xxx",\n    "intent": {\n      "guild_messages": true,\n      "at_messages": false\n    }\n  }\n]\n\'\n```\n',
    'author': 'yanyongyu',
    'author_email': 'yyy@nonebot.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/nonebot/adapter-qqguild',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
