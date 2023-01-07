# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shioajicaller',
 'shioajicaller.cli',
 'shioajicaller.codes',
 'shioajicaller.server']

package_data = \
{'': ['*']}

install_requires = \
['aioredis==2.0.0',
 'gmqtt>=0.6.10,<0.7.0',
 'orjson>=3.8.0,<4.0.0',
 'python-dotenv>=0.19.0,<0.20.0',
 'redis>=3.5.3,<4.0.0',
 'shioaji[speed]>=1.0.0,<2.0.0',
 'websockets>=10.0,<11.0']

extras_require = \
{':sys_platform == "linux"': ['uvloop>=0.17.0,<0.18.0']}

entry_points = \
{'console_scripts': ['shioajicaller = shioajicaller.cli:run']}

setup_kwargs = {
    'name': 'shioajicaller',
    'version': '0.4.0.0',
    'description': 'shioaj warp caller',
    'long_description': 'None',
    'author': 'Steve Lo',
    'author_email': 'info@sd.idv.tw',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
