# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiohcloud', 'aiohcloud.enums', 'aiohcloud.handlers', 'aiohcloud.types']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.2.0,<23.0.0',
 'httpx>=0.23.2,<0.24.0',
 'typing-extensions>=4.4.0,<5.0.0']

setup_kwargs = {
    'name': 'aiohcloud',
    'version': '0.0.7',
    'description': 'Asynchronous python library for Hetzner Cloud API.',
    'long_description': '<div align="center">\n<h1><a href="https://github.com/IHosseini083/AIOHCloud"><b>AIOHCloud</b></a></h1>\n<a href="https://github.com/IHosseini083/AIOHCloud/actions?query=workflow%3ARelease" target="_blank">\n    <img src="https://github.com/IHosseini083/AIOHCloud/workflows/Release/badge.svg" alt="Release">\n</a>\n<a href="https://github.com/IHosseini083/AIOHCloud/actions/workflows/publish-docs.yml?query=event%3Apush+workflow%3A%22Publish+Docs%22+branch%3Amain" target="_blank">\n    <img src="https://github.com/IHosseini083/AIOHCloud/actions/workflows/publish-docs.yml/badge.svg" alt="Docs">\n</a>\n<a href="https://www.python.org">\n    <img src="https://img.shields.io/pypi/pyversions/aiohcloud.svg" alt="Python Versions">\n</a>\n<a href="https://github.com/IHosseini083/AIOHCloud">\n    <img src="https://img.shields.io/pypi/v/aiohcloud.svg" alt="PyPI Version">\n</a>\n<br>\n<a href="https://github.com/psf/black">\n    <img src="https://img.shields.io/static/v1?label=code%20style&message=black&color=black&style=flat" alt="Code Style: black">\n</a>\n<a href="https://github.com/pre-commit/pre-commit">\n    <img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat" alt="pre-commit">\n</a>\n</div>\n\n_AIOHCloud_ is an asynchronous python library for Hetzner Cloud API inspired from the [hcloud-python]\nproject and complies with Hetzner Cloud API standards mentioned in its [documentation](https://docs.hetzner.cloud).\n\nKey features of _AIOHCloud_ are:\n\n- It\'s fully type hinted and plays nicely with your IDE/Editor and preferred linters.\n- Representing API types using Python objects to access their properties easily.\n- Fully asynchronous operations via [httpx] framework.\n\n## Requirements\n\n_AIOHCloud_ requires you to have Python 3.8+ installed.\n\nIt also uses the following external packages:\n\n- [httpx] to send HTTP requests.\n- [attrs] for creating API response models.\n\n## Installation\n\nYou can install _AIOHCloud_ from [PyPI](https://pypi.org/project/aiohcloud/) using pip:\n\n```bash\npip install aiohcloud\n```\n\n## Usage\n\nTo see how to use _AIOHCloud_ you can check out the [documentation](https://aiohcloud.iliya.dev/).\n\n## License\n\nThis project is licensed under the terms of the [GPL-3.0] licence.\n\n<p align="center">&mdash; ⚡ &mdash;</p>\n\n<!-- Links -->\n\n[GPL-3.0]: https://www.gnu.org/licenses/gpl-3.0.en.html "GNU General Public License v3.0"\n[hcloud-python]: https://github.com/hetznercloud/hcloud-python/ "hcloud-python is a library for the Hetzner Cloud API."\n[httpx]: https://github.com/encode/httpx "A next generation HTTP client for Python"\n[attrs]: https://github.com/python-attrs/attrs "Python Classes Without Boilerplate"\n',
    'author': 'Seyed Iliya',
    'author_email': 'pyseyed@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/IHosseini083/AIOHCloud',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
