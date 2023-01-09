# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dockyard_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'requests>=2.28.1,<3.0.0',
 'selenium>=4.7.2,<5.0.0',
 'tabulate>=0.9.0,<0.10.0',
 'webdriver-setup>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['dcli = dockyard_cli.main:main']}

setup_kwargs = {
    'name': 'dockyard-cli',
    'version': '0.1.6',
    'description': 'CLI for dockyard',
    'long_description': 'Usage\n======\n\n1. `dcli configure` - Configure dockyard CLI \n2. `dcli login` - Login to dockyard  \n3. `dcli list` - List dockyard workspaces\n4. `dcli activate` - Set active workspace. Subsequent commands use this workspace if no workspace name is specified.\n5. `dcli ssh [workspace name]` - SSH to dockyard workspace\n6. `dcli scp <source> <target>` - Transfer files/directories to/from workspace.\n\n    a) source/target could be a local path (including .)\n\n    b) source/target could be a remote relative path inside workspace directory `<workspace_name>:<path>`\n\n    c) source/target could be a remote full path inside workspace `<workspace_name>:/<path>` or `<workspace_name>:~/<path>`\n\n7. `dcli code` - Start local VSCode and connect to dockyard workspace\n\n8. `dcli vnc` -  VNC connection to dockyard workspace\n\n9. `dcli start` - Start given workspace\n\n10. `dcli stop` - Stop given workspace\n\n',
    'author': 'rsingh',
    'author_email': 'rsingh@altoslabs.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
