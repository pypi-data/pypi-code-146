# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gridworks',
 'gridworks.data_classes',
 'gridworks.dev_utils',
 'gridworks.enums',
 'gridworks.types',
 'gridworks.types.old_versions']

package_data = \
{'': ['*']}

install_requires = \
['aiocache[redis,memcached]>=0.11.1,<0.12.0',
 'aioredis==1.3.1',
 'beaker-pyteal>=0.4.0,<0.5.0',
 'click>=8.0.1',
 'fastapi-utils>=0.2.1,<0.3.0',
 'fastapi>=0.88.0,<0.89.0',
 'pendulum>=2.1.2,<3.0.0',
 'pika-stubs>=0.1.3,<0.2.0',
 'pika>=1.3.1,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'pytz>=2022.7,<2023.0',
 'requests-async>=0.6.2,<0.7.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0',
 'sphinx-rtd-theme>=1.1.1,<2.0.0',
 'uvicorn[standard]>=0.19.0,<0.20.0']

entry_points = \
{'console_scripts': ['gridworks = gridworks.__main__:main']}

setup_kwargs = {
    'name': 'gridworks',
    'version': '0.0.11',
    'description': 'Gridworks',
    'long_description': "# Gridworks\n\n[![PyPI](https://img.shields.io/pypi/v/gridworks.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/gridworks.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/gridworks)][python version]\n[![License](https://img.shields.io/pypi/l/gridworks)][license]\n\n[![Read the documentation at https://gridworks.readthedocs.io/](https://img.shields.io/readthedocs/gridworks/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/thegridelectric/gridworks/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/thegridelectric/gridworks/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/gridworks/\n[status]: https://pypi.org/project/gridworks/\n[python version]: https://pypi.org/project/gridworks\n[read the docs]: https://gridworks.readthedocs.io/\n[tests]: https://github.com/thegridelectric/gridworks/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/thegridelectric/gridworks\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\nGridWorks uses distributed actors to balance the electric grid. What does this mean?\nIn today's world, more power comes from highly variable power sources such as wind and\nsolar. And yet, the number of electrons going into the grid must match the number coming\nout. This is where GridWorks comes in. GridWorks technology enables electrical devices\nwith some embedded storage or with flexibility to provide grid balancing. Furthermore,\nGridWorks allows these appliances to be more thrifty, using electricity when it is\ncheap and green.\n\nTo learn how using and contributing to GridWorks can support a cost-effective and rapid transition to a sustainable future:\n\n- Watch the beginning of the GridWorks story in [this 5 minute video](https://www.youtube.com/watch?v=5QFNQcp2Yzs)\n- Try some [Hello World](https://gridworks.readthedocs.io/en/latest/hello-gridworks.html) examples\n- Walk through this [10 MW simulation](https://gridworks.readthedocs.io/en/latest/story.html) of how GridWorks, if deployed in new heating systems, could cut home heating costs in half while reducing or eliminating the curtailing (i.e. turning off and wasting) of wind power\n- Learn the ropes of [GridWorks Communications](https://gridworks.readthedocs.io/en/latest/api-sdk-abi.html)\n\n## Algorand Blockchain Mechanics\n\nGridworks runs markets between distributed actors acting as avatars for physical devices on the grid. It needs a foundation of trustless, secure, scalabe validation and authentication. Out of the gate, you will need to understand how to work with the Algorand blockchain. If Algorand\ndevelopment is new to you or you want a refresher, consider starting [here](https://gridworks.readthedocs.io/en/latest/blockchain.html).\n\n## Usage\n\n`pip install gridworks` to install the foundational package.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Gridworks_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/thegridelectric/gridworks/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/thegridelectric/gridworks/blob/main/LICENSE\n[contributor guide]: https://github.com/thegridelectric/gridworks/blob/main/CONTRIBUTING.md\n[command-line reference]: https://gridworks.readthedocs.io/en/latest/usage.html\n",
    'author': 'GridWorks',
    'author_email': 'gridworks@gridworks-consulting.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/thegridelectric/gridworks',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
