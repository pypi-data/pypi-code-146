# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scroller']

package_data = \
{'': ['*'], 'scroller': ['qml/*', 'qml/delegates/*']}

install_requires = \
['pillow>=9.4.0,<10.0.0', 'pyside6>=6.4.2,<7.0.0']

entry_points = \
{'console_scripts': ['scroller = scroller.main:main']}

setup_kwargs = {
    'name': 'scroller',
    'version': '0.2.1',
    'description': '',
    'long_description': '<p align="center"><img src="https://i.ibb.co/RD4j25F/logo.png"></p>\n\n# scroller\n[![Test (CI)](https://github.com/robert-clayton/scroller/actions/workflows/test.yml/badge.svg)](https://github.com/robert-clayton/scroller/actions/workflows/test.yml)\n\nA simple application that scrolls through a folder\'s images.\n\n## Table of Contents\n- [Features](#features)\n- [Prerequisites](#prerequisites)\n- [Installation](#installation)\n- [Usage](#usage)\n- [Development](#development)\n- [Testing](#testing)\n- [Support](#support)\n- [Contribution](#contribution)\n- [License](#license)\n\n## Features\n- Scroll through images in a folder\n- Control scroll speed with scroll wheel\n- Add/Remove columns to scroll view\n- Save hovered image to `~/pictures/saved` via middle-click\n\n## Prerequisites\n- Python >=3.9, <3.12\n- Make\n- Poetry\n\n## Installation\nNavigate to the releases page found [here](https://github.com/robert-clayton/scroller/releases) and download the latest release. Extract the contents of the `scroller-v*.zip` archive and run `scroller.exe` found within.\n\n## Usage\nTo run the application, execute the following command:\n```sh\nmake run scroller\n```\n\n## Development\nClone the repository and run the following commands to install dependencies:\n```sh\ngit clone https://github.com/robert-clayton/scroller.git\ncd scroller && make install\n```\n\n## Testing\nTo run the tests, execute the following command:\n```sh\nmake test\n```\n\n## Support\nPlease [open an issue](https://github.com/robert-clayton/scroller/issues/new) for support.\n\n## Contribution\nWe appreciate any contribution, from fixing a grammar mistake in a comment to implementing complex algorithms. Please read this section if you are contributing your work.\n\nYour contribution will be tested by our automated testing on GitHub Actions to save time and mental energy. After you have submitted your pull request, you should see the GitHub Actions tests start to run at the bottom of your submission page. If those tests fail, then click on the details button try to read through the GitHub Actions output to understand the failure. If you do not understand, please leave a comment on your submission page and a community member will try to help.\n\nPlease help us keep our issue list small by adding fixes: #{$ISSUE_NO} to the commit message of pull requests that resolve open issues. GitHub will use this tag to auto-close the issue when the PR is merged.\n\n## Keybinds\n- `Ctrl-O` - set folder to view\n- `Scrollwheel` - increase/decrease scroll speed\n- `Ctrl-Scrollwheel` - add/remove column to scroll view\n- `Middle Mouse Button` - saves the hovered image to `~/pictures/saved` (on windows)\n\n## License\nThis project is licensed under the [LGPLv2.1](LICENSE) License. \n',
    'author': 'robert-clayton',
    'author_email': '41345902+robert-clayton@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
