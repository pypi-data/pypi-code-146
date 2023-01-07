# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pve_cli', 'pve_cli.proxmox', 'pve_cli.util']

package_data = \
{'': ['*']}

install_requires = \
['proxmoxer>=2.0.1,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['pve-cli = pve_cli.main:cli']}

setup_kwargs = {
    'name': 'pve-cli',
    'version': '0.2.3',
    'description': 'CLI Tool to manage VMs and more on proxmox clusters',
    'long_description': '# pve-cli\n\nCLI Tool to manage VMs and more on proxmox clusters\n\n## Config\n\nFor config option reference see `config.example.toml`.\nThe config file path can be provided via command line option `--config`/`-c` and is searched by default in the following\npaths:\n\n* Linux (Unix): `~/.config/pve-cli/config.toml`\n* MacOS: `~/Library/Application Support/pve-cli/config.toml`\n* Windows: `C:\\Users\\<user>\\AppData\\Local\\pve-cli\\config.toml`\n\nThis leverages the [`get_app_dir`](https://click.palletsprojects.com/en/8.1.x/api/#click.get_app_dir) method\nfrom [`click`](https://click.palletsprojects.com).\n\n\n',
    'author': 'Dominik Rimpf',
    'author_email': 'dev@drimpf.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
