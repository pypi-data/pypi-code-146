# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src',
 'vxdataset': 'src/vxdataset',
 'vxdataset.collector': 'src/vxdataset/collector',
 'vxdataset.datasource': 'src/vxdataset/datasource',
 'vxdataset.expr': 'src/vxdataset/expr',
 'vxdataset.loaders': 'src/vxdataset/loaders',
 'vxsched': 'src/vxsched',
 'vxsched.pubsubs': 'src/vxsched/pubsubs',
 'vxsched.scripts': 'src/vxsched/scripts',
 'vxsched.triggers': 'src/vxsched/triggers',
 'vxutils': 'src/vxutils',
 'vxutils.database': 'src/vxutils/database'}

packages = \
['vxdataset',
 'vxdataset.collector',
 'vxdataset.datasource',
 'vxdataset.expr',
 'vxdataset.loaders',
 'vxquant',
 'vxquant.agent',
 'vxquant.agent.mod',
 'vxquant.gateway',
 'vxquant.mdapi',
 'vxquant.mdapi.calenders',
 'vxquant.mdapi.features',
 'vxquant.mdapi.hq',
 'vxquant.model',
 'vxquant.model.tools',
 'vxquant.tdapi',
 'vxsched',
 'vxsched.pubsubs',
 'vxsched.scripts',
 'vxsched.triggers',
 'vxutils',
 'vxutils.database']

package_data = \
{'': ['*']}

install_requires = \
['numpy',
 'pandas',
 'polars[pyarrow]',
 'pymongo',
 'python-dateutil',
 'pyzmq',
 'requests',
 'scipy',
 'six',
 'tqdm']

setup_kwargs = {
    'name': 'vxquant',
    'version': '2022.12.27rc0',
    'description': '一个简单、易用、面向中国股市实盘的python量化交易框架',
    'long_description': '# vxquant\n\n#### 介绍\n一个简单、易用、面向中国股市实盘的python量化交易框架\n\n#### 模块架构\nvxquant 包括以下三个模块:\n1. vxquant  -- 量化交易中的标准化组件\n2. vxsched  -- 基于事件驱动的调度器实现\n3. vxutils  -- 各种常用的python小功能\n\n\n#### 安装教程\n\n1. 通过 pip 安装\n\n```python\n    pip install vxquant\n```\n\n2. 通过源代码安装\n\n```shell\n    git clone https://gitee.com/vxquant/vxquant && cd  vxquant/\n    pip install .\n```\n\n#### 使用说明\n\n1.  策略文件目录\n\n```python\n# 配置文件存放在 etc/ 目录中\netc/config.json\n# 日志文件存放在 log/ 目录中\nlog/vxquant.log\n# 策略文件存放在 mod/ 目录中\nmod/\n    demo1.py\n    demo2.py\n    demo3.py\n\n```\n\n2. demo1.py\n\n```python\n"""策略demo 1 """\n\nfrom vxsched import vxengine, vxEvent, vxContext, logger\n\n\n@vxengine.event_handler("__init__")\ndef demo1_init(context: vxContext, event: vxEvent) -> None:\n    """策略初始化"""\n    logger.info(f"title内容: {context.settings.title}")\n\n\n@vxengine.event_handler("every_tick")\ndef demo1_every_tick(context: vxContext, event: vxEvent) -> None:\n    """每个tick事件触发"""\n    logger.info(f"触发时间: {event.type}")\n\n```\n\n3. 运行策略\n\n```shell\n\npython -m vxsched -s worker -c etc/config.json -m mod/\n\n```\n\n\n#### 参与贡献\n\n1.  Fork 本仓库\n2.  新建 Feat_xxx 分支\n3.  提交代码\n4.  新建 Pull Request\n\n\n\n',
    'author': 'vex1023',
    'author_email': 'vex1023@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitee.com/vxquant/vxquant',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
