# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cipher',
 'cipher.factories',
 'cipher.models',
 'cipher.plotters',
 'cipher.proxies',
 'cipher.services',
 'cipher.sources',
 'cipher.use_cases',
 'cipher.utils',
 'cipher.values']

package_data = \
{'': ['*'], 'cipher': ['templates/*', 'templates/strategies/*']}

install_requires = \
['dependency-injector>=4.41.0,<5.0.0',
 'jinja2>=3.1.2,<4.0.0',
 'mplfinance>=0.12.9b7,<0.13.0',
 'pandas-ta>=0.3.14b0,<0.4.0',
 'pydantic[dotenv]>=1.10.4,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'typer>=0.7.0,<0.8.0',
 'ujson>=5.6.0,<6.0.0']

extras_require = \
{'finplot': ['finplot>=1.9.0,<2.0.0'], 'jupyter': ['jupyterlab>=3.5.2,<4.0.0']}

entry_points = \
{'console_scripts': ['cipher = cipher.cli:app']}

setup_kwargs = {
    'name': 'cipher-bt',
    'version': '0.1.0',
    'description': 'Cipher, a backtesting framework.',
    'long_description': '# Cipher - trading strategy backtesting framework\n\n![Tests](https://github.com/nanvel/cipher-bt/actions/workflows/tests.yml/badge.svg)\n\nDevelopment:\n```shell\nbrew install poetry\npoetry install\npoetry shell\n\npytest tests\n\ncipher --help\n```\n\nInitialize a new strategies folder and create a strategy:\n```bash\nmkdir my_strategies\ncd my_strategies\n\ncipher init\ncipher new my_strategy\npython my_strategy.py\n```\n',
    'author': 'Oleksandr Polieno',
    'author_email': 'oleksandr@nanvel.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
