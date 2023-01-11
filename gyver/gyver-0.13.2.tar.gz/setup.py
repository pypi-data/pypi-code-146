# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gyver',
 'gyver.boto',
 'gyver.boto.simple_queue',
 'gyver.cache',
 'gyver.config',
 'gyver.crypto',
 'gyver.database',
 'gyver.database.drivers',
 'gyver.database.query',
 'gyver.database.session.asgi',
 'gyver.utils']

package_data = \
{'': ['*']}

install_requires = \
['context-handler>=5.1.0,<6.0.0',
 'cryptography>=38.0.4,<39.0.0',
 'orjson>=3.8.1,<4.0.0',
 'pydantic[email]>=1.10.2,<2.0.0',
 'typing-extensions>=4.4.0,<5.0.0']

extras_require = \
{':sys_platform != "linux"': ['tzdata>=2022.6,<2023.0'],
 'cache': ['redis>=4.4.0,<5.0.0'],
 'db-mariadb': ['pymysql>=1.0.2,<2.0.0', 'asyncmy>=0.2.5,<0.3.0'],
 'db-mysql': ['aiomysql>=0.1.1,<0.2.0', 'pymysql>=1.0.2,<2.0.0'],
 'db-pg': ['psycopg2>=2.9.5,<3.0.0', 'asyncpg>=0.27.0,<0.28.0'],
 'db-sqlite': ['aiosqlite>=0.17.0,<0.18.0'],
 'sqlalchemy': ['sqlalchemy>=1.4.43,<2.0.0']}

setup_kwargs = {
    'name': 'gyver',
    'version': '0.13.2',
    'description': 'Toolbox for web development',
    'long_description': '\n# Gyver\n\nToolbox for web development\n\n\n## Authors\n\n- [@guscardvs](https://www.github.com/guscardvs)\n\n\n## Installation\n\nInstall gyver with pip\n\n```bash\n  pip install gyver\n```\n    \n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n\n\n## Roadmap\n\n- Database helpers\n\n- Http helpers\n\n',
    'author': 'Gustavo Correa',
    'author_email': 'self.gustavocorrea@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/guscardvs/gyver',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
