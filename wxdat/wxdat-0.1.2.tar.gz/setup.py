# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wxdat', 'wxdat.providers', 'wxdat.units']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'prometheus-client>=0.15.0,<0.16.0',
 'psycopg2>=2.9.5,<3.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'ratelimit>=2.2.1,<3.0.0',
 'requests>=2.28.1,<3.0.0',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'sqlalchemy>=1.4.46,<2.0.0']

entry_points = \
{'console_scripts': ['wxdat = wxdat.__main__:main']}

setup_kwargs = {
    'name': 'wxdat',
    'version': '0.1.2',
    'description': 'Weather data explorer.',
    'long_description': "# wxdat #\n\n[![PyPI](https://img.shields.io/pypi/v/wxdat.svg)](https://pypi.org/project/wxdat)\n[![LICENSE](https://img.shields.io/github/license/jheddings/wxdat)](LICENSE)\n[![Style](https://img.shields.io/badge/style-black-black)](https://github.com/ambv/black)\n\nA general purpose weather data recorder & explorer.\n\nWhile the primary purpose of this library is to record weather data, it can also be\nused as a framework for collecting weather information in other apps.\n\n## Installation ##\n\nInstall the published package using pip:\n\n    pip3 install wxdat\n\nThis project uses `poetry` to manage dependencies and a local virtual environment.  To\nget started, clone the repository and install the dependencies with the following:\n\n    poetry install\n\n## Usage ##\n\nRun the module and tell it which config file to use.\n\n    python3 -m wxdat --config wxdat.yaml\n\nIf you are using `poetry` to manage the virtual environment, use the following:\n\n    poetry run python -m wxdat --config wxdat.yaml\n\n## Configuration ##\n\nThe configuration file is a YAML document with a list of stations to export.  See the\nincluded default file for more details.\n\nAll stations have the following configuration values:\n* name - must be unique\n* type - the support station type\n\n## Supported Stations ##\n\nEventually, I'd like to add local stations, not just online sources.  Please see\nthe example configuration file for details on each provider.\n\n* AccuWeather\n* Ambient Weather Network\n* OpenWeatherMap\n* National Weather Service (NOAA)\n* Weather Underground\n\n## Unit Conversion ##\n\n`wxdat` also includes a limited set of conversion helpers for working with units.  In\ngeneral, the pattern for using them is:\n\n   from wxdat import units\n\n   # convert 100.0 from celsius to fahrenheit\n   temp = units.degC(100).degf\n",
    'author': 'jheddings',
    'author_email': 'jheddings@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
