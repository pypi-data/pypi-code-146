# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['portrayt',
 'portrayt.configuration',
 'portrayt.generators',
 'portrayt.interface',
 'portrayt.renderers']

package_data = \
{'': ['*']}

install_requires = \
['RPi.GPIO>=0.7.1,<0.8.0',
 'gradio>=3.3,<4.0',
 'inky>=1.3.2,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'replicate==0.0.1a16']

extras_require = \
{'opencv': ['opencv-python>=4.6.0.66,<5.0.0.0']}

entry_points = \
{'console_scripts': ['run-portrayt = portrayt.main:main']}

setup_kwargs = {
    'name': 'portrayt',
    'version': '1.0.0',
    'description': "This project combines e-paper, raspberry pi's, and StableDiffusion to make a picture frame that portrays anything you ask of it.",
    'long_description': "# portrayt\nThis project combines e-paper, raspberry pi's, and StableDiffusion to make a picture frame that portrays anything you ask of it.\n_________________\n\n[![PyPI version](https://badge.fury.io/py/portrayt.svg)](http://badge.fury.io/py/portrayt)\n[![Test Status](https://github.com/apockill/portrayt/workflows/Test/badge.svg?branch=main)](https://github.com/apockill/portrayt/actions?query=workflow%3ATest)\n[![Lint Status](https://github.com/apockill/portrayt/workflows/Lint/badge.svg?branch=main)](https://github.com/apockill/portrayt/actions?query=workflow%3ALint)\n[![codecov](https://codecov.io/gh/apockill/portrayt/branch/main/graph/badge.svg)](https://codecov.io/gh/apockill/portrayt)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://timothycrosley.github.io/isort/)\n\n_________________\n\nE-Ink Screen + Raspi on an easel             |  Dashboard View\n:-------------------------:|:-------------------------:\n![portrayt-easel.jpg](media%2Fportrayt-easel.jpg)  |  ![screenshot.png](media%2Fscreenshot.png)\n\n\n\n## Development\n\n### Installing python dependencies\n```shell\npoetry install\n```\n\n### Running Tests\n```shell\npytest .\n```\n\n### Formatting Code\n```shell\nbash .github/format.sh\n```\n\n### Linting\n```shell\nbash .github/check_lint.sh\n```\n\n## Running the Program\nInstall docker\n```bash\ncurl -sSL https://get.docker.com | sh\nsudo groupadd docker\nsudo usermod -aG docker $USER\n```\n\nCreate a .env file in your current directory and fill in the API key:\n```bash\nREPLICATE_API_TOKEN=<your token here>\nRENDERER=inky\n```\n\nBuild and run the image\n```bash\ndocker compose up --build -d\n```\n\nWhen using a Raspberry pi, make sure to enable the spi interface by going to `raspi-config`, \ninterface options, and selecting enable.\n\n### Running on desktop\nFor local development, OpenCV is used to render images to a window. The `.env` file needs\nto be updated to allow opencv to be installed (and used for rendering).\n\nIn the `.env` file, fill out the following:\n```\nREPLICATE_API_TOKEN=<your token here>\nRENDERER=opencv\nPOETRY_EXTRAS=--extras opencv\n```\n\nThen, in terminal give docker access to the X window manager:\n```bash\nxhost +\n```\n\nThen build and run using the above commands.",
    'author': 'Alex Thiele',
    'author_email': 'apocthiel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
