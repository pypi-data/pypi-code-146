# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['OlivOS', 'OlivOS.nonebot', 'OlivOS.nonebot.middlewares']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2>=2.0.0rc1,<3.0.0', 'olivos>=0.10.2,<0.11.0']

extras_require = \
{'onebot': ['nonebot-adapter-onebot>=2.0.0-beta.1,<3.0.0'],
 'telegram': ['nonebot-adapter-telegram>=0.1.0-beta.0,<0.2.0']}

setup_kwargs = {
    'name': 'olivos-nb2',
    'version': '0.2.0',
    'description': 'Load OlivOS plugin in NoneBot2',
    'long_description': '<div align="center">\n    <img width="200" src="docs/logo.png" alt="logo"></br>\n\n# OlivOS.nb2\n\n[NoneBot2](https://github.com/nonebot/nonebot2) 的 [OlivOS](https://github.com/OlivOS-Team/OlivOS) 兼容层插件\n\n**注意，本兼容层无法获得 API 的返回值！**\n\n[![License](https://img.shields.io/github/license/nonepkg/OlivOS.nb2)](LICENSE)\n![Python Version](https://img.shields.io/badge/python-3.7.3+-blue.svg)\n![NoneBot Version](https://img.shields.io/badge/nonebot-2.0.0a13+-red.svg)\n![PyPI Version](https://img.shields.io/pypi/v/OlivOS.nb2.svg)\n\n</div>\n\n## 安装\n\n### 从 PyPI 安装（推荐）\n\n- 使用 nb-cli  \n\n```sh\nnb plugin install OlivOS.nb2\n```\n\n- 使用 poetry\n\n```sh\npoetry add OlivOS.nb2\n```\n\n- 使用 pip\n\n```sh\npip install OlivOS.nb2\n```\n\n### 从 GitHub 安装（不推荐）\n\n- 使用 poetry\n\n```sh\npoetry add git+https://github.com/nonepkg/OlivOS.nb2.git\n```\n\n- 使用 pip\n\n```sh\npip install git+https://github.com/nonepkg/OlivOS.nb2.git\n```\n\n## 使用\n\n目前只有 OneBotV11（CQHTTP）平台的兼容层，其他平台待添加（Telegram 平台实验中）。\n\nOlivOS 插件请放入`./data/OlivOS/app/`。\n\n## 插件兼容名单\n\n**这里的插件指 OlivOS 插件。**未在此名单并不意味着无法加载，只是加载后可能出现位未知问题。\n\n- [OlivOS-Team/OlivaDiceCore](https://github.com/OlivOS-Team/OlivaDiceCore)\n- [OlivOS-Team/OlivaDiceJoy](https://github.com/OlivOS-Team/OlivaDiceJoy)\n- [OlivOS-Team/OlivaDiceLogger](https://github.com/OlivOS-Team/OlivaDiceLogger)\n- [Fishroud/OlivaBilibiliPlugin](https://github.com/Fishroud/OlivaBilibiliPlugin)\n\n### 已证实不兼容\n\n- [lunzhiPenxil/OlivOSOnebotV11](https://github.com/lunzhiPenxil/OlivOSOnebotV11) 使用 Thread\n- [OlivOS-Team/OlivaDiceMaster](https://github.com/OlivOS-Team/OlivaDiceMaster) 使用 Thread\n',
    'author': 'jigsaw',
    'author_email': 'j1g5aw@foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
