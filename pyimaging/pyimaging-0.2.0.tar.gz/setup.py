# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyimaging']

package_data = \
{'': ['*'], 'pyimaging': ['font/*']}

install_requires = \
['blind-watermark>=0.4.2,<0.5.0',
 'pillow>=9.4.0,<10.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pyimaging = pyimaging.main:app']}

setup_kwargs = {
    'name': 'pyimaging',
    'version': '0.2.0',
    'description': '轻量级 Python 图像处理',
    'long_description': '<h1 align="center">imaging</h1>\n\n<!-- English | [中文](README_zh.md) -->\n\n> 轻量级 Python 图像处理\n\n[![repo size](https://img.shields.io/github/repo-size/yiyungent/imaging.svg?style=flat)]()\n[![LICENSE](https://img.shields.io/github/license/yiyungent/imaging.svg?style=flat)](https://github.com/yiyungent/imaging/blob/main/LICENSE)\n[![downloads](https://img.shields.io/pypi/dm/pyimaging.svg?style=flat)](https://pypi.org/project/pyimaging/)\n[![QQ Group](https://img.shields.io/badge/QQ%20Group-894031109-deepgreen)](https://jq.qq.com/?_wv=1027&k=q5R82fYN)\n[![Telegram Group](https://img.shields.io/badge/Telegram-Group-blue)](https://t.me/xx_dev_group)\n\n\n## Introduce\n\n轻量级 Python 图像处理\n\n```bash\npip install pyimaging\n```\n\n\n```bash\npyimaging --help\n```\n\n\n## Usage\n\n\n### 图片批量加水印\n\n\n```bash\npyimaging watermark --imagedir "./source/_posts" --mark "yiyun" --space 200 --color "#b7ffab" --opacity 0.3 --size 20 --quality 100\n```\n\n### 其它功能待写文档\n\n\n\n## Donate\n\nimaging is an Apache-2.0 licensed open source project and completely free to use. However, the amount of effort needed to maintain and develop new features for the project is not sustainable without proper financial backing.\n\nWe accept donations through these channels:\n\n- <a href="https://afdian.net/@yiyun" target="_blank">爱发电</a> (￥5.00 起)\n- <a href="https://dun.mianbaoduo.com/@yiyun" target="_blank">面包多</a> (￥1.00 起)\n\n## Author\n\n**imaging** © [yiyun](https://github.com/yiyungent), Released under the [Apache-2.0](./LICENSE) License.<br>\nAuthored and maintained by yiyun with help from contributors ([list](https://github.com/yiyungent/imaging/contributors)).\n\n> GitHub [@yiyungent](https://github.com/yiyungent) Gitee [@yiyungent](https://gitee.com/yiyungent)\n',
    'author': 'yiyun',
    'author_email': 'yiyungent@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/yiyungent/imaging',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
