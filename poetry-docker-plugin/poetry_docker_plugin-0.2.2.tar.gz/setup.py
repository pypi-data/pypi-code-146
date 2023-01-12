# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_docker_plugin']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.2,<2.0.0']

entry_points = \
{'poetry.application.plugin': ['docker = '
                               'poetry_docker_plugin.plugin:DockerPlugin']}

setup_kwargs = {
    'name': 'poetry-docker-plugin',
    'version': '0.2.2',
    'description': 'A poetry plugin for configure and build docker images.',
    'long_description': '# Poetry Docker Plugin\n\n[![License: LGPL v3](https://img.shields.io/badge/License-MIT-blue.svg)](https://mit-license.org)\n![PyPI](https://img.shields.io/pypi/pyversions/poetry-docker-plugin)\n![PyPI](https://img.shields.io/pypi/v/poetry-docker-plugin?color=gree&label=pypi%20package)\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)\n\nA [Poetry](https://python-poetry.org) plugin for configuring and building docker images directly from python projects.\n\n## Installation\n\nIn order to install the plugin you need to have installed a poetry version `>1.0` and type:\n\n```bash\npoetry self add poetry-docker-plugin\n```\n\n## Usage\n\nAdd the following section to your pyproject.toml:\n\n```toml\n[tool.docker]\nimage_name = "org/custom_image:latest" # docker image name\nargs = { arg1 = "", version = "1.2.0" } # default values for args\nfrom = "python:3.9"\nlabels = { "com.github.vagmcs"="Awesome", "description"="This is a test image", "version"="0.1.0" }\ncopy = [\n    { source = "./poetry-docker-plugin-0.1.0.tar.gz", target = "/opt/pdp.tar.gz" },\n#    { source = "../pyproject.toml", target = "/tmp/pp.toml" }\n]\nenv.SERVICE_OPTS = "-Xms1g -Xmx2g -XX:+DoEscapeAnalysis -XX:+OptimizeStringConcat -XX:+DisableAttachMechanism"\nenv.SERVICE_CONFIGURATION = "/opt/service.conf"\nvolume = ["/data"]\nflow = [\n    { work_dir = "/opt" },\n    { run = "ls" },\n    { work_dir = "/tmp" },\n    { run = "ls /opt" },\n]\nexpose = [8888, 9999]\ncmd = ["run_service", "--verbose"]\nentrypoint = []\n```\n\nthen, as soon as you are done configuring, type:\n\n```bash\npoetry docker\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.',
    'author': 'Evangelos Michelioudakis',
    'author_email': 'vagmcs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/vagmcs/poetry-docker-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
