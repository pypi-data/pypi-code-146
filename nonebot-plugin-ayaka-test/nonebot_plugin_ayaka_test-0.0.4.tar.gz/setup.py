# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '..'}

packages = \
['ayaka_test', 'ayaka_test.old']

package_data = \
{'': ['*'],
 'ayaka_test': ['.git/*',
                '.git/hooks/*',
                '.git/info/*',
                '.git/logs/*',
                '.git/logs/refs/heads/*',
                '.git/logs/refs/remotes/origin/*',
                '.git/objects/01/*',
                '.git/objects/05/*',
                '.git/objects/06/*',
                '.git/objects/08/*',
                '.git/objects/0f/*',
                '.git/objects/10/*',
                '.git/objects/18/*',
                '.git/objects/21/*',
                '.git/objects/25/*',
                '.git/objects/29/*',
                '.git/objects/2e/*',
                '.git/objects/30/*',
                '.git/objects/31/*',
                '.git/objects/36/*',
                '.git/objects/3b/*',
                '.git/objects/41/*',
                '.git/objects/46/*',
                '.git/objects/48/*',
                '.git/objects/4a/*',
                '.git/objects/4b/*',
                '.git/objects/4f/*',
                '.git/objects/52/*',
                '.git/objects/59/*',
                '.git/objects/5f/*',
                '.git/objects/66/*',
                '.git/objects/6a/*',
                '.git/objects/6c/*',
                '.git/objects/79/*',
                '.git/objects/89/*',
                '.git/objects/8a/*',
                '.git/objects/9b/*',
                '.git/objects/9d/*',
                '.git/objects/9f/*',
                '.git/objects/ac/*',
                '.git/objects/ae/*',
                '.git/objects/af/*',
                '.git/objects/b4/*',
                '.git/objects/bb/*',
                '.git/objects/be/*',
                '.git/objects/bf/*',
                '.git/objects/ca/*',
                '.git/objects/cd/*',
                '.git/objects/d0/*',
                '.git/objects/d4/*',
                '.git/objects/d6/*',
                '.git/objects/d7/*',
                '.git/objects/da/*',
                '.git/objects/db/*',
                '.git/objects/de/*',
                '.git/objects/e3/*',
                '.git/objects/e9/*',
                '.git/objects/eb/*',
                '.git/objects/ed/*',
                '.git/objects/f5/*',
                '.git/objects/f6/*',
                '.git/objects/f8/*',
                '.git/objects/f9/*',
                '.git/refs/heads/*',
                '.git/refs/remotes/origin/*',
                'dist/*']}

install_requires = \
['nonebot2>=2.0.0b5,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka-test',
    'version': '0.0.4',
    'description': 'ayaka_test',
    'long_description': '<div align="center">\n\n# ayaka_test - 0.0.4\n\n</div>\n\n## 文档\n\nhttps://bridgel.github.io/ayaka_doc/latest/develop/test\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/nonebot-plugin-ayaka-test',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
