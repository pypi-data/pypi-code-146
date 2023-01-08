# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cert_host_scraper']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0',
 'requests>=2.27.1,<3.0.0',
 'rich>=11,<14',
 'single-source>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['cert-host-scraper = cert_host_scraper.cli:cli']}

setup_kwargs = {
    'name': 'cert-host-scraper',
    'version': '0.7.0',
    'description': '',
    'long_description': '# Cert Host Scraper\n\n![CI](https://github.com/inverse/cert-host-scraper/workflows/CI/badge.svg)\n[![PyPI version](https://badge.fury.io/py/cert-host-scraper.svg)](https://badge.fury.io/py/cert-host-scraper)\n![PyPI downloads](https://img.shields.io/pypi/dm/cert-host-scraper?label=pypi%20downloads)\n[![License](https://img.shields.io/github/license/inverse/cert-host-scraper.svg)](LICENSE)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nQuery the certificate transparency log from [crt.sh](https://crt.sh) by a given a keyword and returns the status code of the matched results. Optionally filtering the results by status code.\n\n## Usage\n\n```bash\ncert-host-scraper search your-domain.com [--status-code 200] [--clean/--no-clean]\n```\n\n## Installation\n\nWith pipx:\n\n```bash\npipx install cert-host-scraper\n```\n\nWith pip:\n\n```bash\npip install cert-host-scraper\n```\n\n## Development\n\nRequires [poetry][0] and Python 3.10.\n\n```\npoetry install\npoetry run python -m cert_host_scraper.cli\n```\n\n## License\n\nMIT\n[0]: https://python-poetry.org\n',
    'author': 'Malachi Soord',
    'author_email': 'inverse.chi@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/inverse/cert-host-scraper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
