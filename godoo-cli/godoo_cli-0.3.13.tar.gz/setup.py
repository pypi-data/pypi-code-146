# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['godoo_cli',
 'godoo_cli.commands',
 'godoo_cli.commands.rpc',
 'godoo_cli.git',
 'godoo_cli.helpers']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.1.27,<4.0.0',
 'godoo-rpc==0.0.3',
 'openupgradelib>=3.3.4,<4.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'rich>=12.6.0,<13.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'typer[all]>=0.7.0,<0.8.0']

extras_require = \
{'codequality': ['pylint-odoo>=8.0.16,<9.0.0',
                 'black>=22.10.0,<23.0.0',
                 'isort>=5.10.1,<6.0.0',
                 'flake8>=5.0.4,<6.0.0'],
 'devcontainer': ['ipdb>=0.13.9,<0.14.0',
                  'debugpy>=1.6.0,<2.0.0',
                  'pre-commit>=2.20.0,<3.0.0',
                  'watchdog>=2.1.7,<3.0.0',
                  'py-spy>=0.3.11,<0.4.0',
                  'rope>=0.23.0,<0.24.0',
                  'inotify>=0.2.10,<0.3.0']}

entry_points = \
{'console_scripts': ['godoo = godoo_cli:launch_cli']}

setup_kwargs = {
    'name': 'godoo-cli',
    'version': '0.3.13',
    'description': 'Wrapper around Odoo-Bin with some convinience RPC functions.',
    'long_description': '# gOdoo Dev Environment\n\n![OdooLogo](https://raw.githubusercontent.com/OpenJKSoftware/gOdoo/main/assets/odoo_logo.png)\n![ComposeLogo](https://raw.githubusercontent.com/docker/compose/v2/logo.png)\n\n[<img src="https://raw.githubusercontent.com/OpenJKSoftware/gOdoo/main/assets/godoo-main-cli.png" width="1000"/>](image.png)\n\n**gOdoo** is short for **go Odoo**. \\\nIt is a [Vscode Devcontainer](https://code.visualstudio.com/docs/remote/containers) Environment for [Odoo](https://odoo.com/)\nwith Python CLI `godoo` convenience wrapper around `odoo-bin`.\n\nThis repository is the base source for the Python package [godoo-cli](https://pypi.org/project/godoo-cli/) and serves as\nan all batteries included development environment.\n\nMade Possible by: [WEMPE Elektronic GmbH](https://wetech.de)\n\n# gOdoo-cli\n\nPython package that provides `godoo` command line interface around `odoo-bin`.\n\nIt\'s build with [Typer](https://github.com/tiangolo/typer) to provide some convenience Wrappers for Odoo development and\nDeployment.\n\nMost flags can be configured by Env variables. \\\nUse `godoo --help` to find out more. HINT: Install tab-completion with `godoo --install-completion`\n\n# Docker\n\nThis workspace also contains Docker and Docker-Compose files. \\\n\nThey are used to provide either easy Odoo instances where the source is pulled according to\n[ODOO_MANIFEST.yml](./ODOO_MANIFEST.yml), or as a all batteries included devcontainer for VScode.\n\n## Requirements\n\n- [Docker Compose](https://github.com/docker/compose)\n- [Traefik](https://doc.traefik.io/traefik/) container running with docker provider and "traefik" named docker network.\n  Example: [Traefik Devproxy](https://github.com/joshkreud/traefik_devproxy)\n- SSH Agent running. (check `echo $SSH_AUTH_SOCK`)\\\n  This gets passed trough in the Buildprocess to clone Thirdparty repos.\n\n## Just wanna have a quick and easy Odoo Instance?\n\n```bash\ngit clone https://github.com/OpenJKSoftware/gOdoo\ncd godoo\n. scripts/container_requirements.sh # Check Requirements\ndocker-compose build\ndocker-compose up\n# wait......\n# wait a bit mode ...\n# just a little bit longer ..\n# There we go.\n# Odoo should be reachable on \'https://godoo.docker.localhost\' assuming you didn\'t change .env TRAEFIK_HOST_RULE or COMPOSE_PROJECT_NAME\n```\n\n# Devcontainer\n\n## Features\n\n- All batteries included [Devcontainer](https://code.visualstudio.com/docs/remote/containers) with postgres service\n  Container and local DNS resolvig managed by [Traefik](https://doc.traefik.io/traefik/).\n- Easy fully working Odoo instance by `docker-compose up` with https access.\n- `godoo` CLI wrapper around Odoo. (Most flags can be configured by Environment Variables and are already preconfigured\n  in the Containers. See [.env.sample](./.env.sample))\n- `odoo-bin` is added to PATH and can thus be invoked from every folder.\n- Odoo will run in Proxy_Mode behind a Traefik reverse proxy for easy access on\n  `https://$COMPOSE_PROJECT_NAME.docker.localhost`\n- [Odoo Pylint plugin](https://github.com/OCA/pylint-odoo) preconfigured in vscode\n- Preinstalled vscode Extensions Highlights:\n  - [SQL Tools](https://marketplace.visualstudio.com/items?itemName=mtxr.sqltools) with preconfigured connection for\n    easy Database access in the Sidebar.\n  - [Docker Extension](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-docker) controls\n    container host.\n  - [Odoo Snippets](https://marketplace.visualstudio.com/items?itemName=mstuttgart.odoo-snippets)\n  - [Odoo Developments](https://marketplace.visualstudio.com/items?itemName=scapigliato.vsc-odoo-development) can Grab\n    Odoo Model information from a running Server\n  - [Todo Tree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree)\n\n## Usage\n\n1. For Docker on windows: Clone the repo into the WSL2 Filesystem for better IO performance\n2. Have [Traefik](https://github.com/traefik/traefik) Running on `docker.localhost`\n   [Example](https://github.com/joshkreud/traefik_devproxy) \\\n   There must be a Docker network called `traefik` that can reach traefik.\n3. Open Devcontianer:\n   - If you have the Devcontainer CLI: `devcontainer open .`\n   - If not open the workspace in Local Vscode. In the Command pallete search for `Reopen in container`\n4. From **within the container** start Odoo using one of the following commands:\n   - You can enable godoo tab-completion by `godoo --install-completion`\n   - `make` -> Loads Odoo + Workspace Addons\n   - `make bare` -> Loads Odoo with ony `web` installed.\n   - `make kill` -> Search for `odoo-bin` processes and kill them\n   - `make reset` -> Drops DB, deletes config file and datafolder\n   - The full init script is available via "`godoo`". (See --help for Options)\n5. Open Odoo `https://$COMPOSE_PROJECT_NAME.docker.localhost`\\\n   For example `COMPOSE_PROJECT_NAME=godoo` --> [https://godoo.docker.localhost](https://godoo.docker.localhost)\n6. Login with `admin:admin`\n7. Profit!\n\n### Access to Odoo and Thirdparty addon Source\n\nYou can access the Odoo source by opening the VsCode workspace [full.code-workspace](full.code-workspace) from within\nthe Container. This will open a [Multi-Root Workspace](https://code.visualstudio.com/docs/editor/multi-root-workspaces).\nReally waiting for https://github.com/microsoft/vscode-remote-release/issues/3665 here.\n\n## Reset Devcontainer Data\n\nWhen you screwed up so bad its time to just start Over godoo has you covered:\n\n### Automatic Reset\n\nThere are 3 Options to reset the Dev Env.\n\n1. From **Outside** the Container run `make reset` in the project root to delete docker volumes and restart the\n   container. (Vscode will prompt to reconnect if still open)\n2. From **Outside** the Container run `make reset-hard` in the project root to force rebuild the main Odoo container and\n   then do the same as `make reset`\n3. From **Inside** the Container run `make reset` to drop the DB and delete varlib and the bootstrap flag, which is way\n   quicker than the other options.\n\n### Manual Reset\n\n1. Close vscode\n2. Remove `app` and `db` container from docker.\n3. Remove volumes: `db, odoo_thirdparty, odoo_web, vscode_extensions`\n4. Restart Devcontainer\n\n## Python Debugging\n\n### VsCode Debugging\n\nDebugging doesn\'t reliably work with\n[Odoo Multiprocess](https://www.odoo.com/documentation/14.0/developer/misc/other/cmdline.html#multiprocessing) mode\nenabled. \\\nThe container ships with a Vscode Debug profile, that sets `--workers 0` to allow for Debugging Breakpoints. See [.vscode/launch.json](./.vscode/launch.json)\n\n### Interactive Shell\n\nUse `godoo shell` to enter an interactive shell on the Database.\n\n# Odoo Modules\n\n## Third Party Modules (manifest.yml)\n\nThe `godoo` bootstrap function, will download some modules using git. \\\nWhich Repos to download is specified in `ODOO_MANIFEST.yml` ([Default](./ODOO_MANIFEST.yml)) \\\nNot all of the cloned addons are automatically installed. \\\nInstall them via the Apps Page in Odoo using `godoo rpc modules install` or using `odoo-bin`.\\\nModules downloaded on the Odoo Marketplace can be dropped as a `.zip` archive in [./thirdparty](./thirdparty)\n',
    'author': 'Joshua Kreuder',
    'author_email': 'Joshua_Kreuder@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/OpenJKSoftware/gOdoo',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
