# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['bearface']

package_data = \
{'': ['*']}

install_requires = \
['omegaconf>=2.1,<3.0']

extras_require = \
{'all:python_version < "3.11"': ['torch>=1.10,<2.0']}

setup_kwargs = {
    'name': 'bearface',
    'version': '0.0.1',
    'description': 'A library of custom OmegaConf resolvers',
    'long_description': '# :bear: bearface :bear:\n\n<p align="center">\n   <a href="https://github.com/durandtibo/bearface/actions">\n      <img alt="CI" src="https://github.com/durandtibo/bearface/workflows/CI/badge.svg?event=push&branch=main">\n   </a>\n    <a href="https://pypi.org/project/bearface/">\n      <img alt="PYPI version" src="https://img.shields.io/pypi/v/bearface">\n    </a>\n   <a href="https://pypi.org/project/bearface/">\n      <img alt="Python" src="https://img.shields.io/pypi/pyversions/bearface.svg">\n   </a>\n   <a href="https://opensource.org/licenses/BSD-3-Clause">\n      <img alt="BSD-3-Clause" src="https://img.shields.io/pypi/l/bearface">\n   </a>\n   <a href="https://codecov.io/gh/durandtibo/bearface">\n      <img alt="Codecov" src="https://codecov.io/gh/durandtibo/bearface/branch/main/graph/badge.svg">\n   </a>\n   <a href="https://github.com/psf/black">\n     <img  alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n   </a>\n   <a href="https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings">\n     <img  alt="Doc style: google" src="https://img.shields.io/badge/%20style-google-3666d6.svg">\n   </a>\n   <br/>\n</p>\n\n## Overview\n\n`bearface` is a library of custom [OmegaConf](https://github.com/omry/omegaconf) resolvers.\nThe resolvers can be easily registered in your python project by adding the following lines:\n\n```python\nfrom bearface import register_resolvers\n\nregister_resolvers()\n```\n\n- [Documentation](https://durandtibo.github.io/bearface/)\n- [Installation](#installation)\n- [Contributing](#contributing)\n- [API stability](#api-stability)\n- [License](#license)\n\n## Installation\n\nWe highly recommend installing\na [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).\n`bearface` can be installed from pip using the following command:\n\n```shell\npip install bearface\n```\n\nTo make the package as slim as possible, only the minimal packages required to use `bearface` are\ninstalled.\nTo include all the packages, you can use the following command:\n\n```shell\npip install bearface[all]\n```\n\nPlease check the [get started page](https://durandtibo.github.io/bearface/get_started) to see how to\ninstall only some specific packages or other alternatives to install the library.\n\n## Contributing\n\nPlease check the instructions in [CONTRIBUTING.md](.github/CONTRIBUTING.md).\n\n## API stability\n\n:warning: While `bearface` is in development stage, no API is guaranteed to be stable from one\nrelease to the next.\nIn fact, it is very likely that the API will change multiple times before a stable 1.0.0 release.\nIn practice, this means that upgrading `bearface` to a new version will possibly break any code that\nwas using the old version of `bearface`.\n\n## License\n\n`bearface` is licensed under BSD 3-Clause "New" or "Revised" license available in [LICENSE](LICENSE)\nfile.\n',
    'author': 'Thibaut Durand',
    'author_email': 'durand.tibo+gh@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/durandtibo/bearface',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
