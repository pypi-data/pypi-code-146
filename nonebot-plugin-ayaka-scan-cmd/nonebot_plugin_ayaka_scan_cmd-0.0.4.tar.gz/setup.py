# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

modules = \
['nonebot_plugin_ayaka_scan_cmd']
install_requires = \
['ayaka>=0.0.0.4,<0.0.1.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka-scan-cmd',
    'version': '0.0.4',
    'description': '扫描当前所有matcher，总结命令',
    'long_description': '<div align="center">\n\n# 命令探查 0.0.4\n\n猜测未知插件的使用方法\n\n</div>\n\n## 使用方法\n\n| 命令     | 效果       |\n| -------- | ---------- |\n| 命令探查 | 启动本插件 |\n| 退出     | 关闭本插件 |\n\n启动本插件后，发送命令\n\n| 命令                 | 效果                       |\n| -------------------- | -------------------------- |\n| 列表                 | 查看所有已安装的插件的名称 |\n| 查看 `编号`/`插件名` | 查看指定插件的命令         |\n| 商店 `编号`/`插件名` | 在nb商店中搜索插件的信息   |\n\n## 使用效果 \n\n![图片](pics/0.png)\n![图片](pics/1.png)\n![图片](pics/2.png)\n![图片](pics/3.png)\n![图片](pics/4.png)\n![图片](pics/5.png)\n\n## 实现原理\n\n遍历`nonebot.matcher.matchers`对象，分析所有`Matcher`\n\n下载`https://raw.githubusercontent.com/nonebot/nonebot2/master/website/static/plugins.json`，获取插件信息\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/nonebot-plugin-ayaka-scan-cmd',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
