# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['psqlsync', 'psqlsync.ghmoteqlync']

package_data = \
{'': ['*']}

install_requires = \
['psycopg2-binary>=2.9.2,<3.0.0', 'tomli>=2.0.1,<3.0.0']

extras_require = \
{'dirgh': ['dirgh @ git+https://github.com/tiptenbrink/dirgh.git@main',
           'trio>=0.20.0,<0.22.0']}

entry_points = \
{'console_scripts': ['prep = psqlsync.ghremote.cli:run',
                     'psqlsync = psqlsync.cli:run']}

setup_kwargs = {
    'name': 'psqlsync',
    'version': '0.2.0',
    'description': 'Tool to create basic PostgreSQL backups and restore them from local files.',
    'long_description': 'None',
    'author': 'Tip ten Brink',
    'author_email': '75669206+tiptenbrink@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
