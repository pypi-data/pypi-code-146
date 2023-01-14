# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['zq_django_util',
 'zq_django_util.exceptions',
 'zq_django_util.logs',
 'zq_django_util.logs.migrations',
 'zq_django_util.response',
 'zq_django_util.utils',
 'zq_django_util.utils.auth',
 'zq_django_util.utils.oss',
 'zq_django_util.utils.user']

package_data = \
{'': ['*'], 'zq_django_util.logs': ['templates/*']}

install_requires = \
['djangorestframework-simplejwt>=4.7,<6.0',
 'drf-standardized-errors>=0.9.0,<0.13.0',
 'oss2>=2.13.0,<3.0']

setup_kwargs = {
    'name': 'zq-django-util',
    'version': '0.1.2',
    'description': '自强Studio Django 工具',
    'long_description': '<div align="center">\n\n# zq-django-util\n**自强 Studio Django 工具**\n\n<!-- markdownlint-disable-next-line MD036 -->\n</div>\n\n<p align="center">\n  <a href="https://github.com/Nagico/zq-django-util/actions/workflows/code_check.yml">\n    <img src="https://github.com/Nagico/zq-django-util/actions/workflows/code_check.yml/badge.svg" alt="CI">\n  </a>\n  <a href="https://zq-django-util.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/zq-django-util/badge/?version=latest" alt="Documentation Status" />\n  </a>\n  <a href="https://codecov.io/gh/Nagico/zq-django-util" >\n    <img src="https://codecov.io/gh/Nagico/zq-django-util/branch/master/graph/badge.svg" alt="cov"/>\n  </a>\n  <a href="https://pypi.org/project/zq-django-util/">\n  <img src="https://img.shields.io/pypi/v/zq-django-util" alt="pypi">\n  </a>\n</p>\n<!-- markdownlint-enable MD033 -->\n\n[English Version](README_EN.md)\n\n## 简介\n\nzq-django-util 是用于辅助搭建 django-drf 应用的工具集合，其中包含：\n\n- 标准异常、响应处理\n- jwt、微信认证\n- oss 存储与直传\n- 默认分页类\n- 测试 ViewSet\n\n详细文档：[zq-django-util.readthedocs.io](https://zq-django-util.readthedocs.io/)\n\n## 依赖需求\n\n- Python 3.8+\n- Django 3.2+\n- Django REST framework 3.12+\n\n**强烈建议**使用官方支持的最新版本，当前的测试环境为：Python 3.10, Django 4.1, DRF 3.14\n\n## 安装\n\n- 安装 zq-django-util 包\n\n使用 `pip` 安装：\n```shell\npip install zq-django-util\n```\n\n使用 `poetry` 安装：\n```shell\npoetry add zq-django-util\n```\n\n## 使用\n\n可以根据以下说明进行配置，以启用相关功能。\n\n[使用文档](docs/usage)\n\n## 开发\n\n本项目使用 Poetry 进行依赖管理，Pytest 进行单元测试。\n\n[开发文档](docs/development)\n',
    'author': 'Nagico',
    'author_email': 'yjr888@vip.qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Nagico/zq-django-util',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
