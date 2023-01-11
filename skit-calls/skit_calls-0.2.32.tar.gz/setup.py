# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['skit_calls', 'skit_calls.data']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3,<6.0',
 'aiofiles==0.8.0',
 'aiohttp==3.8.1',
 'attrs==20.3.0',
 'dvc[s3]==2.9.5',
 'loguru==0.5.3',
 'numpy==1.22.0',
 'pandas==1.4.2',
 'psycopg2==2.9.3',
 'pydash>=5.1.0,<6.0.0',
 'toml==0.10.2',
 'tqdm==4.62.1']

entry_points = \
{'console_scripts': ['skit-calls = skit_calls.cli:main']}

setup_kwargs = {
    'name': 'skit-calls',
    'version': '0.2.32',
    'description': 'Library to fetch calls from a given environment.',
    'long_description': 'None',
    'author': 'ltbringer',
    'author_email': 'amresh.venugopal@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/skit-ai/skit-calls',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
