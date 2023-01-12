# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faddr']

package_data = \
{'': ['*'], 'faddr': ['static/*', 'templates/*']}

install_requires = \
['fastapi[all]>=0.87.0,<0.88.0',
 'loguru>=0.6.0,<0.7.0',
 'pydantic[dotenv]>=1.10.2,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'ray>=1,<2',
 'rich>=12.6.0,<13.0.0',
 'sqlalchemy>=1.4.44,<2.0.0',
 'ttp>=0.9.1,<0.10.0']

entry_points = \
{'console_scripts': ['faddr = faddr.faddr:main',
                     'faddr-db = faddr.faddr_db:main',
                     'faddr-rest = faddr.faddr_rest:main']}

setup_kwargs = {
    'name': 'faddr',
    'version': '0.6.0',
    'description': 'Tool to parse configuration of network devices such as Juniper routers and store gathered data in database',
    'long_description': '# FAddr\n\n[![CodeFactor](https://www.codefactor.io/repository/github/kido5217/faddr/badge)](https://www.codefactor.io/repository/github/kido5217/faddr)\n[![GitHub top language](https://img.shields.io/github/languages/top/kido5217/faddr)](https://www.python.org/)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/faddr)](https://pypi.org/project/faddr/)\n[![GitHub](https://img.shields.io/github/license/kido5217/faddr)](https://opensource.org/licenses/MIT)\n\nFAddr is a Python program for parsing configuration of network devices such as Juniper and Cisco routers and storing gathered data in database.\n\n## Installation\n\nUse the package manager [pip](https://pip.pypa.io/en/stable/) to install faddr.\n\n```bash\npip install faddr\n```\n\n## Usage\n\nGenerate database:\n\n```bash\nfaddr-db\n```\n\nFind ip address termination point:\n\n```bash\nfaddr 10.20.30.1\n```\n\n## Contributing\n\nPull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.\n\nPlease make sure to update tests as appropriate.\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n',
    'author': 'Fedor Suchkov',
    'author_email': 'f.suchkov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kido5217/faddr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
