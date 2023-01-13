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
    'version': '0.3.0',
    'description': 'A poetry plugin for configure and build docker images.',
    'long_description': '# Poetry Docker Plugin\n\n[![License: LGPL v3](https://img.shields.io/badge/License-MIT-blue.svg)](https://mit-license.org)\n![PyPI](https://img.shields.io/pypi/pyversions/poetry-docker-plugin)\n![PyPI](https://img.shields.io/pypi/v/poetry-docker-plugin?color=gree&label=pypi%20package)\n[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)\n\nA [Poetry](https://python-poetry.org) plugin for configuring and building docker images directly from python projects.\n\n## Installation\n\nIn order to install the plugin you need to have installed a poetry version `>1.0` and type:\n\n```bash\npoetry self add poetry-docker-plugin\n```\n\n## Simple Example\n\nLet\'s assume that you have created a Poetry project having the following `pyproject.toml` configuration:\n\n```toml\n[tool.poetry]\nname = "example_project"\nversion = "1.0.0"\ndescription = "An example poetry project."\nauthors = ["Evangelos"]\n\n[tool.poetry.dependencies]\npython = "3.11"\n\n[tool.poetry.scripts]\nrun_service = "app.service:start"\n```\n\nyour project also declares a poetry script that starts a service. Then, by adding the following minimal docker configuration in your `pyproject.toml` you can build your docker image:\n\n```toml\n[tool.docker]\ncopy = [\n    { source = "example_project-1.0.0.tar.gz", target = "/app/example_project.tar.gz" },\n]\nflow = [\n    { run = "pip install /app/example_project.tar.gz" },\n]\nexpose = [8000]\ncmd = ["run_service"]\n```\n\nNote that there is no docker [FROM](https://docs.docker.com/engine/reference/builder/#from)  command, and thus `poetry-docker-plugin` automatically figures out the python version and use `python:3.11` as the base image. Moreover, since we have not defined a name for the image, it derives one, using the first author name and the project name. Thus, by running the command `poetry docker`, poetry builds a docker image ready to run your service in port 8000.\n \n## Docker Configuration Skeleton\n\nThe configuration below outlines all supported commands:\n\n```toml\n[tool.docker]\nimage_name = "org/image_name:version"\nargs = { version = "1.2.0" } # default values for args\nfrom = "python:3.11"\nlabels = { "description" = "Poetry docker plugin is awesome." }\ncopy = [\n    { source = "./poetry-docker-plugin-0.1.0.tar.gz", target = "/opt/pdp.tar.gz" },\n]\nenv.SERVICE_CONFIGURATION = "/opt/service.conf"\nvolume = ["/data"]\nflow = [\n    # a sequence of WORKDIR and RUN commands\n    { work_dir = "/opt" },\n    { run = "ls" },\n    { work_dir = "/tmp" },\n    { run = "ls /opt" },\n]\nexpose = [8888, 9999]\n# alternatively you may use entrypoint = []\ncmd = ["run_service", "--verbose"]\n```\n\nthen, as soon as you are done configuring, type:\n\n```bash\npoetry docker\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.',
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
