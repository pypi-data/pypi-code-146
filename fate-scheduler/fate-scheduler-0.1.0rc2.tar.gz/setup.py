# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fate',
 'fate.cli',
 'fate.cli.base',
 'fate.cli.command',
 'fate.conf',
 'fate.conf.base',
 'fate.conf.types',
 'fate.sched',
 'fate.sched.base',
 'fate.sched.base.util',
 'fate.task',
 'fate.util',
 'fate.util.compat',
 'fate.util.datastructure',
 'fate.util.log']

package_data = \
{'': ['*'], 'fate.cli': ['include/banner/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'argcmdr>=0.13.2,<0.14.0',
 'croniter>=1.3.5,<2.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pyyaml>=6.0,<7.0',
 'toml>=0.10.2,<0.11.0',
 'wcwidth>=0.2.5,<0.3.0']

entry_points = \
{'console_scripts': ['fate = fate:main',
                     'fated = fate:daemon',
                     'fates = fate:serve']}

setup_kwargs = {
    'name': 'fate-scheduler',
    'version': '0.1.0rc2',
    'description': 'The operating system-level command scheduler and manager.',
    'long_description': None,
    'author': 'Jesse London',
    'author_email': 'jesselondon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/chicago-cdac/fate',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
