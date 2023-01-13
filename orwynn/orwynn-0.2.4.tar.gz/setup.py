# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['orwynn',
 'orwynn.app',
 'orwynn.apprc',
 'orwynn.boot',
 'orwynn.cls',
 'orwynn.config',
 'orwynn.controller',
 'orwynn.controller.endpoint',
 'orwynn.controller.http',
 'orwynn.controller.websocket',
 'orwynn.crypto',
 'orwynn.database',
 'orwynn.di',
 'orwynn.di.collecting',
 'orwynn.di.init',
 'orwynn.dt',
 'orwynn.error',
 'orwynn.file',
 'orwynn.fmt',
 'orwynn.indication',
 'orwynn.log',
 'orwynn.mapping',
 'orwynn.middleware',
 'orwynn.model',
 'orwynn.module',
 'orwynn.mongo',
 'orwynn.mp',
 'orwynn.parsing',
 'orwynn.proxy',
 'orwynn.rnd',
 'orwynn.router',
 'orwynn.service',
 'orwynn.singleton',
 'orwynn.test',
 'orwynn.uio',
 'orwynn.validation',
 'orwynn.web',
 'orwynn.worker']

package_data = \
{'': ['*']}

install_requires = \
['bcrypt>=4.0.1,<5.0.0',
 'colorama>=0.4.6,<0.5.0',
 'coverage>=6.5.0,<7.0.0',
 'dictdiffer>=0.9.0,<0.10.0',
 'fastapi>=0.88.0,<0.89.0',
 'httpx>=0.23.1,<0.24.0',
 'loguru>=0.6.0,<0.7.0',
 'pyjwt>=2.6.0,<3.0.0',
 'pymongo>=4.3.3,<5.0.0',
 'pytest-asyncio>=0.20.3,<0.21.0',
 'pytest>=7.2.0,<8.0.0',
 'python-benedict>=0.28.1,<0.29.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'pyyaml>=6.0,<7.0',
 'uvicorn[standard]>=0.20.0,<0.21.0',
 'websockets>=10.4,<11.0']

setup_kwargs = {
    'name': 'orwynn',
    'version': '0.2.4',
    'description': 'Scalable web-framework with out-of-the-box architecture',
    'long_description': '# Orwynn',
    'author': 'ryzhovalex',
    'author_email': 'thed4rkof@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
