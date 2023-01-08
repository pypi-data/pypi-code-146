# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyazo_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0.0,<8.0.0', 'pyperclip>=1.7.0,<2.0.0', 'requests>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['pyazo = pyazo_cli.pyazo:main']}

setup_kwargs = {
    'name': 'pyazo-cli',
    'version': '0.3.2',
    'description': '',
    'long_description': "# Pyazo\n\nPyazo is a self-hosted screenshot and image upload utility. It allows you to take a screenshot of a part of your screen and automatically upload it to your own server. You can also directly upload an image from your computer.\n\nIt is comprised of a cross-platform client written in Python which defers the actual taking of the screenshot to the built-in OS tools (macOS and Windows) or common utilities (Linux distributions). The server is written as a RESTful FastAPI app with support for basic user accounts and image sharing options.\n\n## Compatibility\n\n* Python >= 3.6 (check with `python --version`)\n\nThe following OSes have off-the-shelf compatibility. You can add more back ends for missing systems or configurations.\n\n* Linux (`scrot`, `maim`, or `import` (ImageMagick))\n* macOS\n* Windows 10\n\n## Installation\n\n* Install [Python] 3\n* Install client requirements:\n\n- [requests](https://pypi.org/project/requests/)\n- [pyperclip](https://pypi.org/project/pyperclip/)\n- [click](https://pypi.org/project/click/)\n- [pillow](https://pypi.org/project/pillow/) (Windows only)\n\n## Configuration\n\nCreate an external config file. Pyazo extends the default config with the provided values. The following table contain all options and the location of the user config file.\n\n### Client\n\n* Example Config: `config.ini.sample`\n* Placement Path: `~/.config/pyazo/config.ini` (`~` refers to the user home directory)\n\n| Key                | Default                                   | Description                                                              |\n|--------------------|-------------------------------------------|--------------------------------------------------------------------------|\n| url                | https://example.com                       | API endpoint to send the image file in a POST request                    |\n| token              | ' '                                       | JWT token (https://github.com/pyazo-screenshot/api/blob/master/README.md)|\n| util               | maim                                      | Built-in tool or common utility for taking a screenshot                  |\n| output_dir         | `$(xdg-user-dir PICTURES)`/screenshots    | Place to store the image after taking a screenshot                       |\n\n## License\n\nBSD 3-Clause\n\n[Python]: <https://www.python.org/downloads/>\n",
    'author': 'Jelena Dokic',
    'author_email': 'jrubics@hacke.rs',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/pyazo-screenshot/cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
