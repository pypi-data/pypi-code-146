# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lib', 'lib.api']

package_data = \
{'': ['*']}

modules = \
['cli']
install_requires = \
['PyYaml', 'docopt', 'gitpython', 'requests']

entry_points = \
{'console_scripts': ['trident = cli:cli']}

setup_kwargs = {
    'name': 'trident-sync',
    'version': '0.1.1',
    'description': '三叉戟，异构项目同步升级工具，The heterogeneous repo sync and upgrade CLI',
    'long_description': '# repo-sync\n\n异构项目同步升级工具\n\n## 命令\n```shell\n\npython ./cli.py init https://github.com/fast-crud/fs-admin-antdv main . https://github.com/certd/certd v2 ./packages/ui/certd-server\n\npython ./cli.py start\n```',
    'author': 'xiaojunnuo',
    'author_email': 'xiaojunnuo@qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
