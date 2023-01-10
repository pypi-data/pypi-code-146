# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_anvil',
 'python_anvil.api_resources',
 'python_anvil.api_resources.mutations',
 'python_anvil.tests']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0,<9.0',
 'pydantic>=1.8.2,<2.0.0',
 'ratelimit>=2.2.1,<3.0.0',
 'requests>=2.25.0,<3.0.0',
 'tabulate>=0.8.9,<0.9.0']

entry_points = \
{'console_scripts': ['anvil = python_anvil.cli:cli']}

setup_kwargs = {
    'name': 'python-anvil',
    'version': '1.8.0',
    'description': 'Anvil API',
    'long_description': '![Horizontal Lockupblack](https://user-images.githubusercontent.com/293079/169453889-ae211c6c-7634-4ccd-8ca9-8970c2621b6f.png#gh-light-mode-only)\n![Horizontal Lockup copywhite](https://user-images.githubusercontent.com/293079/169453892-895f637b-4633-4a14-b997-960c9e17579b.png#gh-dark-mode-only)\n\n# Anvil API Library\n\n[![PyPI Version](https://img.shields.io/pypi/v/python-anvil.svg)](https://pypi.org/project/python-anvil)\n[![PyPI License](https://img.shields.io/pypi/l/python-anvil.svg)](https://pypi.org/project/python-anvil)\n\nThis is a library that provides an interface to access the [Anvil API](https://www.useanvil.com/developers) from applications\nwritten in the Python programming language.\n\n[Anvil](https://www.useanvil.com/developers/) provides easy APIs for all things paperwork.\n\n1. [PDF filling API](https://www.useanvil.com/products/pdf-filling-api/) - fill out a PDF template with a web request and structured JSON data.\n2. [PDF generation API](https://www.useanvil.com/products/pdf-generation-api/) - send markdown or HTML and Anvil will render it to a PDF.\n3. [Etch e-sign with API](https://www.useanvil.com/products/etch/) - customizable, embeddable, e-signature platform with an API to control the signing process end-to-end.\n4. [Anvil Workflows (w/ API)](https://www.useanvil.com/products/workflows/) - Webforms + PDF + e-sign with a powerful no-code builder. Easily collect structured data, generate PDFs, and request signatures.\n\nLearn more on our [Anvil developer page](https://www.useanvil.com/developers/). See the [API guide](https://www.useanvil.com/docs) and the [GraphQL reference](https://www.useanvil.com/docs/api/graphql/reference/) for full documentation.\n\n### Documentation\n\nGeneral API documentation: [Anvil API docs](https://www.useanvil.com/docs)\n\n# Setup\n\n## Requirements\n\n* Python 3.6.2+\n\n## Installation\n\nInstall it directly into an activated virtual environment:\n\n```shell\n$ pip install python-anvil\n```\n\nor add it to your [Poetry](https://python-poetry.org/) project:\n\n```shell\n$ poetry add python-anvil\n```\n',
    'author': 'Allan Almazan',
    'author_email': 'allan@useanvil.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.useanvil.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
