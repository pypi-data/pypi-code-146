# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['stb']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'platformdirs>=2.6.2,<3.0.0',
 'pysh>=3.1.0,<4.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'tomlkit>=0.11.6,<0.12.0',
 'typer[all]>=0.6.1,<0.7.0',
 'typing-extensions>=4.3.0,<5.0.0']

entry_points = \
{'console_scripts': ['stb = stb:app']}

setup_kwargs = {
    'name': 'stb-mnt',
    'version': '1.8.0',
    'description': 'A universal tool for local microservice management.',
    'long_description': '# stb\n\nA universal tool for local microservice management\n\n## Installation\n\n```bash\npipx install stb-mnt\n```\n\n## Usage\n\n### Setup\n\n* To download and setup backend/service1 microservice as a subdirectory to the current working directory, use:\n\n```bash\nstb setup backend/service1\n```\n\n* To download and setup backend/service1 and backend/service2 as subdirectories to current working directory, use:\n\n```bash\nstb setup backend/service1 backend/service2\n```\n\n* To setup backend/service1 that you have already cloned, use:\n\n```bash\nstb setup backend/service1 --no-clone\n```\n\nNote that if you want to clone repositories, you must first set a `git_url` using `stb config set git_url` command\n\n### Update\n\n* To update .env file in accordance with .env.example in a microservice:\n\n```bash\nstb update env\n```\n\n* To synchronize service ports between all installed microservices (you can specify which ones will run locally with the `--local` option):\n\n```bash\nstb update ports\n```\n\n* To install the dependencies from poetry.lock file and update submodules:\n\n```bash\nstb update package\n```\n\n* To update poetry.lock file, install dependencies, update submodules, stash current changes, checkout to master, pull from remote, and recreate databases:\n\n```bash\nstb update package -pucd\n```\n\nor  \n\n```bash\nstb update package --pull --update --checkout --reset-databases\n```\n\n### DB\n\n* To upgrade migrations in a microservice:\n\n```bash\nstb db ugrade\n```\n\n* To create databases and upgrade its migrations in a microservice:\n\n```bash\nstb db create\n```\n\n* To drop databases in a microservice:\n\n```bash\nstb db drop\n```\n\n* To drop and recreate databases, and upgrade migrations in a microservice:\n\n```bash\nstb db reset\n```\n\n* To upgrade migrations in parallel for faster upgrades (useful for large monoliths with multiple databases), you can use the -p (--parallel) option:\n\n```bash\nstb db create -p\n```\n  \n```bash\nstb db reset -p\n```\n  \n* To force dropping of databases in case another program is using them at the same time, you can use the -f (--force) option:\n\n```bash\nstb db drop -f\n```\n  \n```bash\nstb db reset -f\n```\n  \n### Use\n\n`stb use` allows you to take a company private package and install either a cloud version or a local version of it. STB will preserve all extras and will gracefully handle any issues that might happen while updating.\n\n* To install a local version of `my_package` that is located at `../my_package`:\n\n```bash\nstb use my_package ../my_package\n```\n\n* To install a cloud version of `my_package` with tag `8.3.1`:\n\n```bash\nstb use my_package 8.3.1\n```\n\n### Run\n\n* To update and run the select services concurrently:\n\n```bash\nstb run service1 service2\n```\n\n### Config\n\n* To set a git url for cloning:\n\n```bash\nstb config set git_url git@github.com:mycompany\n```\n\n### How directories are selected for update/db\n\nFor every update, you can specify:\n\n1) A microservice directory, which will cause stb to update only that microservice\n2) Several microservice directories, which will cause stb to update these microservices and integrate them together (for example, `update ports` assigns ports to local microservices and updates their links in other microservices to match the assigned ports)\n3) A directory with multiple microservice subdirectories inside it, which is equivalent to (2) with the list of subdirectories as arguments\n4) Nothing, which will choose the current working directory as the first argument and will be equivalent to (1) or (3)\n',
    'author': 'Stanislav Zmiev',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
