# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['weather_command', 'weather_command.models']

package_data = \
{'': ['*']}

install_requires = \
['camel-converter[pydantic]==3.0.0',
 'httpx==0.23.3',
 'pydantic==1.10.4',
 'rich==13.0.1',
 'tenacity==8.1.0',
 'typer==0.7.0']

entry_points = \
{'console_scripts': ['weather-command = weather_command.main:app']}

setup_kwargs = {
    'name': 'weather-command',
    'version': '5.0.0',
    'description': 'Command line weather app',
    'long_description': '# Weather Command\n\n[![Tests Status](https://github.com/sanders41/weather-command/workflows/Testing/badge.svg?branch=main&event=push)](https://github.com/sanders41/weather-command/actions?query=workflow%3ATesting+branch%3Amain+event%3Apush)\n[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sanders41/weather-command/main.svg)](https://results.pre-commit.ci/latest/github/sanders41/weather-command/main)\n[![Coverage](https://codecov.io/github/sanders41/weather-command/coverage.svg?branch=main)](https://codecov.io/gh/sanders41/weather-command)\n[![PyPI version](https://badge.fury.io/py/weather-command.svg)](https://badge.fury.io/py/weather-command)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/weather-command?color=5cc141)](https://github.com/sanders41/weather-command)\n\nA command line weather app\n\n## Installation\n\nInstallation with [pipx](https://github.com/pypa/pipx) is recommended.\n\n```sh\npipx install weather-command\n```\n\nAlternatively Weather Command can be installed with pip.\n\n```sh\npip install weather-command\n```\n\n## Usage\n\nFirst an API key is needed from [OpenWeather](https://openweathermap.org/), A free account is all that\nis needed. Once you have your API key create an environment variable named `OPEN_WEATHER_API_KEY` that\nconstains your API key.\n\n```sh\nexport OPEN_WEATHER_API_KEY=your-api-key\n```\n\nEach time the shell is restarted this variable will be cleared. To avoid this it can be added to your\nprofile. For example if your shell is zsh the API key can be added to the `~/.zshenv` file. Doing this\nwill prevent the need to re-add the key each time the shell is started.\n\nTo get the weather for a city:\n\n```sh\nweather-command city seattle\n```\n\nOnce installed you can also add aliases to your shell to make it quick to get a forecast. For example\nif your shell is zsh you can add something like the following to your `~/.zshrc` file:\n\n```sh\nalias we="weather-command zip 98109 -i --am-pm"\nalias wed="weather-command zip 98109 -i --am-pm -f daily"\nalias weh="weather-command zip 98109 -i --am-pm -f hourly"\n```\n\nAfter adding this to the `~/.zshrc` you will need to restart your terminal. After that typing `we`\nwill get the current forecast, `wed` will get the daily forecast and `weh` will get the hourly forecast.\n\n## Contributing\n\nContributions to this project are welcome. If you are interesting in contributing please see our [contributing guide](CONTRIBUTING.md)\n',
    'author': 'Paul Sanders',
    'author_email': 'psanders1@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sanders41/weather-command',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
