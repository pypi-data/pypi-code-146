# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pilibre', 'pilibre.config', 'pilibre.graph', 'pilibre.screensaver']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.3,<0.24.0', 'rich>=13.0.1,<14.0.0']

entry_points = \
{'console_scripts': ['pilibre = pilibre.main:main']}

setup_kwargs = {
    'name': 'pilibre',
    'version': '0.1.0',
    'description': 'Display hardware metrics from LibreHardwareMonitor, intended to be run on a small screen on a RaspberryPi.',
    'long_description': '<p align="center">\n  <img alt="PiLibre" src="docs/assets/logo.svg"/>\n</p>\n\n<div align="center">\n    <img alt="PyPI" src="https://img.shields.io/pypi/v/pilibre?style=for-the-badge">\n    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/pilibre?style=for-the-badge">\n    <img alt="GitHub" src="https://img.shields.io/github/license/acbuie/pilibre?style=for-the-badge">\n</div>\n\n<div align="center">\n    <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/acbuie/pilibre?style=for-the-badge">\n    <a href="https://github.com/acbuie">\n        <img alt="GitHub Profile" src="https://img.shields.io/static/v1?label=&message=Profile&style=for-the-badge&logo=github&labelColor=grey">\n    </a>\n</div>\n\nA small Python script for displaying hardware metrics. Metrics are pulled from `LibreHardwareMonitor`, and requires it to be installed on your PC and in server mode. It is designed to be run on a small computer with a small display. I intend to use a Raspberry Pi, but you could likely use something else.\n\n<!-- Some examples will go here! -->\n\n---\n\n## Installation\n\nPiLibre relies on `rich` and `httpx` on the display machine, and `LibreHardwareMonitor` on the machine from which you want to see metrics.\n\n- `rich`: For terminal display of the hardware metrics\n- `https`: To pull the JSON data served by `LibreHardwareMonitor`\n- `LibreHardwareMonitor`: For getting the hardware metrics of your computer.\n\n### Host Machine Setup\n\nThe host machine only needs to have `LibreHardwareMonitor` installed. The project can be found here: https://github.com/LibreHardwareMonitor/LibreHardwareMonitor and downloaded from here: https://github.com/LibreHardwareMonitor/LibreHardwareMonitor/releases.\n\nOnce installed:\n\n- Open the HTTP server via `Options -> HTTP Server`.\n- Take note of the IP address. This is the IP address of the local machine.\n- If you\'d like to change the default port, do so here.\n\n### Display Machine Setup\n\nThe machine you want to display metrics on needs to have the `PiLibre` application installed. The easiest way is to use `pipx`, but manual instructions are also included.\n\n#### pipx\n\n`pipx` is recommended for the simplest installation. This will install `PiLibre` into its own virtual environment, along with any dependencies.\n\nInstall `pipx` from here: https://github.com/pypa/pipx#install-pipx.\n\n```shell\npipx install git+https://github.com/acbuie/pilibre.git\n```\n\n#### Manually\n\nIf you know what you\'re doing, you can install the package via `Git` and run it manually, with `python -m src/pilibre`. As always, a virtual environment is recommended, so the requirements don\'t get installed into the system python. Runtime dependencies can be installed with `python -m pip install requirements.txt`.\n\nFirst, clone the project into a new directory.\n\n```shell\nmkdir pilibre\ncd pilibre\ngit clone https://github.com/acbuie/pilibre.git\n```\n\nOnce installed, create and activate a python virtual environment. Read about python virtual environments here: https://docs.python.org/3/tutorial/venv.html.\n\nThen, install the dependencies.\n\n```shell\npython -m pip install requirements.txt\n```\n\n## Usage\n\nUsage is very simple. Once the HTTP server is running on the host machine, simply specify the IP address and port in the config file and run the project.\n',
    'author': 'acbuie',
    'author_email': 'aidancbuie@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/acbuie/pilibre',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
