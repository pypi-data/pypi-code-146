# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quiltplus']

package_data = \
{'': ['*']}

install_requires = \
['quilt3>=5.1.0,<6.0.0', 'trio>=0.22.0,<0.23.0']

setup_kwargs = {
    'name': 'quiltplus',
    'version': '0.4.1',
    'description': "Resource-oriented Python API for Quilt's decentralized social knowledge platform",
    'long_description': "# quiltplus\nResource-oriented API for Quilt's decentralized social knowledge platform\n\n# Developmment\n## Setup\n\n```\ngit clone https://github.com/quiltdata/quiltplus\ncd quiltplus\npoetry self update\npoetry install\npoetry run pytest-watch\n```\n## Pushing Changes\nBe sure you to first set your [API token](https://pypi.org/manage/account/) using `poetry config pypi-token.pypi <pypi-api-token>`\n```\n# merge PR\npoetry version patch # minor major\npoetry build\npoetry publish\n# create new branch\npoetry version prepatch # preminor premajor\n```\n",
    'author': 'Ernest Prabhakar',
    'author_email': 'ernest@quiltdata.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
