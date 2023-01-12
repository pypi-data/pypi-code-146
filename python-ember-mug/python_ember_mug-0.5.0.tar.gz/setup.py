# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ember_mug', 'ember_mug.cli', 'tests', 'tests.cli']

package_data = \
{'': ['*']}

install_requires = \
['bleak-retry-connector>=2.13.0', 'bleak>=0.19.2']

entry_points = \
{'console_scripts': ['ember-mug = ember_mug.cli:run_cli']}

setup_kwargs = {
    'name': 'python-ember-mug',
    'version': '0.5.0',
    'description': 'Python Library for Ember Mugs.',
    'long_description': '# Python Ember Mug\n\n[![pypi](https://img.shields.io/pypi/v/python-ember-mug.svg)](https://pypi.org/project/python-ember-mug/)\n[![python](https://img.shields.io/pypi/pyversions/python-ember-mug.svg)](https://pypi.org/project/python-ember-mug/)\n[![Build Status](https://github.com/sopelj/python-ember-mug/actions/workflows/dev.yml/badge.svg)](https://github.com/sopelj/python-ember-mug/actions/workflows/dev.yml)\n[![codecov](https://codecov.io/gh/sopelj/python-ember-mug/branch/main/graphs/badge.svg)](https://codecov.io/github/sopelj/python-ember-mug)\n![Project Maintenance](https://img.shields.io/maintenance/yes/2023.svg?style=for-the-badge)\n\nPython Library for Ember Mugs\n\n* Documentation: <https://sopelj.github.io/python-ember-mug>\n* GitHub: <https://github.com/sopelj/python-ember-mug>\n* PyPI: <https://pypi.org/project/python-ember-mug/>\n* Free software: MIT\n\n## Summary\n\nLibrary to attempt to interact with Ember Mugs via Bluetooth using the bleak library.\nThis was created for use with my [Home Assistant integration](https://github.com/sopelj/hass-ember-mug-component),\nbut could be useful separately and has a simple CLI interface too.\n\n**Note**: I have only tested with my Ember Mug 2, but others should work. (Please let me know)\n\n## Features\n\n* Finding mugs\n* Connecting to Mugs\n* Reading Information (Colour, temp, liquid level, etc.)\n* Writing (Desired temp, colour, temperature unit)*\n* Polling for changes\n\n*** Writing only works if the mug has been set up in the app previously\n\n## Usage\n\n### Python\n\n```python\nfrom ember_mug.scanner import find_mug, discover_mugs\nfrom ember_mug.mug import EmberMug\n\n# if first time with mug in pairing\nmugs = await discover_mugs()\ndevice = mugs[0]\n# after paired you can simply use\ndevice = await find_mug()\nmug = EmberMug(device)\nasync with mug.connection() as con:\n    print(\'Connected.\\nFetching Info\')\n    await con.update_all()\n    print(mug.formatted_data)\n```\n\n### CLI\n\nIt can also be run via command line either directly with `ember-mug --help` or as a module with `python -m ember_mug --help`\nThere are four options with different subsections. You can see them by specifying them before help. eg `ember-mug poll --help`\n\n```bash\nember-mug discover  # Finds the mug in pairing mode for the first time\nember-mug poll  # fetches info and keeps listening for notifications\nember-mug get name target-temp  # Prints name and target temp of mug\nember-mug set --name "My mug" --target-temp 56.8  # Sets the name and target temp to specified values\n```\n\nBasic options:\n\n| Command     | Use                                                                            |\n|-------------|--------------------------------------------------------------------------------|\n| `discover`  | Find/List all detected unpaired mugs in pairing mode                           |\n| `find`      | Find *one* already paired mugs                                                 |\n| `info`      | Connect to *one* mug and print its current state                               |\n| `poll`      | Connect to *one* mug and print its current state and keep watching for changes |\n| `get`       | Get the value(s) of one or more attribute(s) by name                           |\n| `set`       | Set one or more values on the mug                                              |\n\n\n![CLI Example](./docs/images/cli-example.png)\n\n## Caveats\n\n- Since this api is not public, a lot of guesswork and reverse engineering is involved, so it\'s not perfect.\n- If the mug has not been set up in the app since it was reset, writing is not allowed. I don\'t know what they set in the app, but it changes something, and it doesn\'t work without it.\n- Once that mug has been set up in the app, you should ideally forget the device or at least turn off bluetooth whilst using it here, or you will probably get disconnected often\n- I haven\'t figured out some attributes like udsk, dsk, location and timezone.\n\n## Troubleshooting\n\n### \'Operation failed with ATT error: 0x0e\' or another connection error\nThis seems to be caused by the bluetooth adaptor being in some sort of passive mode. I have not yet figured out how to wake it programmatically so sadly, you need to manually open `bluetoothctl` to do so.\nPlease ensure the mug is in pairing mode (ie the light is flashing blue) and run the `bluetoothctl` command. You don,t need to type anything. run it and wait until the mug connects.\n\n## Todo\n- Test with other devices. Please let me know if you have tried it with others.\n\n## Credits\n\nThis package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [waynerv/cookiecutter-pypackage](https://github.com/waynerv/cookiecutter-pypackage) project template.\n',
    'author': 'Jesse Sopel',
    'author_email': 'jesse.sopel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sopelj/python-ember-mug',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
