# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['coola']

package_data = \
{'': ['*']}

extras_require = \
{'all': ['numpy>=1.20,<2.0', 'torch>=1.10,<2.0']}

setup_kwargs = {
    'name': 'coola',
    'version': '0.0.4',
    'description': 'A light library to check if two complex/nested objects are equal or not',
    'long_description': '# coola\n\n<p align="center">\n   <a href="https://github.com/durandtibo/coola/actions">\n      <img alt="CI" src="https://github.com/durandtibo/coola/workflows/CI/badge.svg?event=push&branch=main">\n   </a>\n    <a href="https://pypi.org/project/coola/">\n      <img alt="PYPI version" src="https://img.shields.io/pypi/v/coola">\n    </a>\n   <a href="https://pypi.org/project/coola/">\n      <img alt="Python" src="https://img.shields.io/pypi/pyversions/coola.svg">\n   </a>\n   <a href="https://opensource.org/licenses/BSD-3-Clause">\n      <img alt="BSD-3-Clause" src="https://img.shields.io/pypi/l/coola">\n   </a>\n   <a href="https://codecov.io/gh/durandtibo/coola">\n      <img alt="Codecov" src="https://codecov.io/gh/durandtibo/coola/branch/main/graph/badge.svg">\n   </a>\n   <a href="https://github.com/psf/black">\n     <img  alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">\n   </a>\n   <a href="https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings">\n     <img  alt="Doc style: google" src="https://img.shields.io/badge/%20style-google-3666d6.svg">\n   </a>\n   <br/>\n</p>\n\n## Overview\n\n`coola` is a light Python library that provides simple functions to check in a single line if two\ncomplex/nested objects are equal or not.\n`coola` was initially designed to work\nwith [PyTorch `Tensor`s](https://pytorch.org/docs/stable/tensors.html)\nand [NumPy `ndarray`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html), but it\nis possible to extend it\nto [support other data structures](https://durandtibo.github.io/coola/customization).\n\n- [Motivation](#motivation)\n- [Documentation](https://durandtibo.github.io/coola/)\n- [Installation](#installation)\n- [Contributing](#contributing)\n- [API stability](#api-stability)\n- [License](#license)\n\n## Motivation\n\nLet\'s imagine you have the following dictionaries that contain both a PyTorch `Tensor` and a\nNumPy `ndarray`.\nYou want to check if the two dictionaries are equal or not.\nBy default, Python does not provide an easy way to check if the two dictionaries are equal or not.\nIt is not possible to use the default equality operator `==` because it will raise an error.\nThe `coola` library was developed to fill this gap. `coola` provides a function `objects_are_equal`\nthat can indicate if two complex/nested objects are equal or not.\n\n```python\nimport numpy\nimport torch\n\nfrom coola import objects_are_equal\n\ndata1 = {\'torch\': torch.ones(2, 3), \'numpy\': numpy.zeros((2, 3))}\ndata2 = {\'torch\': torch.zeros(2, 3), \'numpy\': numpy.ones((2, 3))}\n\nobjects_are_equal(data1, data2)\n```\n\n`coola` also provides a function `objects_are_allclose` that can indicate if two complex/nested\nobjects are equal within a tolerance or not.\n\n```python\nfrom coola import objects_are_allclose\n\nobjects_are_allclose(data1, data2, atol=1e-6)\n```\n\nPlease check the [quickstart page](https://durandtibo.github.io/coola/quickstart) to learn more on\nhow to use `coola`.\n\n## Installation\n\nWe highly recommend installing\na [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).\n`coola` can be installed from pip using the following command:\n\n```shell\npip install coola\n```\n\nTo make the package as slim as possible, only the minimal packages required to use `coola` are\ninstalled.\nTo include all the packages, you can use the following command:\n\n```shell\npip install coola[all]\n```\n\nPlease check the [get started page](https://durandtibo.github.io/coola/get_started) to see how to\ninstall only some specific packages or other alternatives to install the library.\n\n## Contributing\n\nPlease check the instructions in [CONTRIBUTING.md](.github/CONTRIBUTING.md).\n\n## API stability\n\n:warning: While `coola` is in development stage, no API is guaranteed to be stable from one\nrelease to the next.\nIn fact, it is very likely that the API will change multiple times before a stable 1.0.0 release.\nIn practice, this means that upgrading `coola` to a new version will possibly break any code that\nwas using the old version of `coola`.\n\n## License\n\n`coola` is licensed under BSD 3-Clause "New" or "Revised" license available in [LICENSE](LICENSE)\nfile.\n',
    'author': 'Thibaut Durand',
    'author_email': 'durand.tibo+gh@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/durandtibo/coola',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
