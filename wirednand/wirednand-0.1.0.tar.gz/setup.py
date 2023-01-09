# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wirednand']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['wirednand = wirednand.__main__:main']}

setup_kwargs = {
    'name': 'wirednand',
    'version': '0.1.0',
    'description': 'Logic circuit simulator. Building a computer from NAND gates.',
    'long_description': '<p align="center">\n    <a href="https://guiferviz.github.io/wirednand" target="_blank">\n        <img src="https://guiferviz.github.io/wirednand/images/logo.png"\n             alt="Wired NAND logo"\n             width="200">\n    </a>\n</p>\n<p align="center">\n    <a href="https://github.com/guiferviz/wirednand/actions/workflows/cicd.yaml" target="_blank">\n        <img src="https://github.com/aidictive/wirednand/actions/workflows/cicd.yaml/badge.svg"\n             alt="Wired NAND CI pipeline status">\n    </a>\n    <a href="https://app.codecov.io/gh/guiferviz/wirednand/" target="_blank">\n        <img src="https://img.shields.io/codecov/c/github/aidictive/wirednand"\n             alt="Wired NAND coverage status">\n    </a>\n    <a href="https://github.com/guiferviz/wirednand/issues" target="_blank">\n        <img src="https://img.shields.io/github/issues/guiferviz/wirednand"\n             alt="Wired NAND issues">\n    </a>\n    <a href="https://github.com/aidictive/wirednand/graphs/contributors" target="_blank">\n        <img src="https://img.shields.io/github/contributors/guiferviz/wirednand"\n             alt="Wired NAND contributors">\n    </a>\n    <a href="https://pypi.org/project/wirednand/" target="_blank">\n        <img src="https://pepy.tech/badge/wirednand"\n             alt="Wired NAND total downloads">\n    </a>\n    <a href="https://pypi.org/project/wirednand/" target="_blank">\n        <img src="https://pepy.tech/badge/wirednand/month"\n             alt="Wired NAND downloads per month">\n    </a>\n    <br />\n    Logic circuit simulator. Building a computer from NAND gates.\n</p>\n\n---\n\n#\xa0Wired NAND\n\n:books: **Documentation**:\n<a href="https://guiferviz.github.io/wirednand" target="_blank">\n    https://guiferviz.github.io/wirednand\n</a>\n\n:keyboard: **Source Code**:\n<a href="https://github.com/guiferviz/wirednand" target="_blank">\n    https://github.com/guiferviz/wirednand\n</a>\n\n---\n\n## 🤔 What is this?\n\nTODO\n\n\n## 🤓 How it works?\n\nTODO\n\n\n## Credits\n\n* Logo generated with [dreamlike.art](https://dreamlike.art/).\n',
    'author': 'guiferviz',
    'author_email': 'guiferviz@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/guiferviz/wirednand',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
