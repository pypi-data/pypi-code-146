# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gempyp',
 'gempyp.config',
 'gempyp.data_compare',
 'gempyp.data_compare.common',
 'gempyp.data_compare.configurator',
 'gempyp.data_compare.core',
 'gempyp.data_compare.data',
 'gempyp.data_compare.report',
 'gempyp.data_compare.tools',
 'gempyp.dv',
 'gempyp.engine',
 'gempyp.engine.executors',
 'gempyp.jira',
 'gempyp.libs',
 'gempyp.libs.enums',
 'gempyp.libs.exceptions',
 'gempyp.pyprest',
 'gempyp.reporter',
 'gempyp.sdk']

package_data = \
{'': ['*'], 'gempyp.data_compare': ['config/*']}

install_requires = \
['XlsxWriter>=3.0.3,<4.0.0',
 'certifi>=2022.6.15,<2023.0.0',
 'cffi>=1.15.0,<2.0.0',
 'charset-normalizer>=2.0.12,<3.0.0',
 'coloredlogs>=15.0.1,<16.0.0',
 'cryptography>=38.0.1,<39.0.0',
 'humanfriendly>=10.0,<11.0',
 'idna>=3.4,<4.0',
 'lxml>=4.9.0,<5.0.0',
 'mysql-connector-python>=8.0.30,<9.0.0',
 'ntlm-auth>=1.5.0,<2.0.0',
 'numpy>=1.19.5,<2.0.0',
 'pandas>=1.1.5,<2.0.0',
 'pg8000>=1.26.0,<2.0.0',
 'pycparser>=2.21,<3.0',
 'pyreadline3>=3.4.1,<4.0.0',
 'pyreadline>=2.1,<3.0',
 'pytest>=6.2.4,<7.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2022.2.1,<2023.0.0',
 'requests-ntlm>=1.1.0,<2.0.0',
 'requests>=2.27.1,<3.0.0',
 'six>=1.16.0,<2.0.0',
 'urllib3>=1.26.12,<2.0.0']

entry_points = \
{'console_scripts': ['gempyp = gempyp.gemPyp:main']}

setup_kwargs = {
    'name': 'gempyp',
    'version': '1.0.4b2',
    'description': 'An ecosystem of libraries useful for software development',
    'long_description': '<h1 align="center">\n\t<img\n\t\twidth="350"\n\t\talt="GemPyp"\n\t\tsrc="https://gempyp.gemecosystem.com/static/media/Gempyp.e73184c67dca4df150fa37048866ecb6.svg">\n</h1>\n\n<h3 align="center">\n\t<div><h2>GemPyP</h2></div>\n    An out of the box Python Automation Framework\n</h3>\n\n<p align="center">\n\t<strong>\n\t\t<a href="https://gempyp.gemecosystem.com/">Website</a>\n\t\t•\n\t\t <a href="##">Docs</a>\n\t\t•\n\t\t <a href="https://github.com/Gemini-Solutions/gempyp/">Repo</a>\n\t</strong>\n</p>\n\n<p align="center">\n<img src="https://img.shields.io/badge/python-3.6-blue"/>\n<img src="https://img.shields.io/pypi/dw/gempyp">\n<img src="https://img.shields.io/pypi/v/gempyp?color=red&label=version&logo=gempyp">\n<img src="https://img.shields.io/pypi/implementation/gempyp">\n\n</p>\n\n## Table of contents[![]()](#table-of-contents)\n\n1. [Overview](#overview)\n2. [Installation](#installation)\n3. [Requirements](#requirements)\n4. [Features](#features)\n5. [Usage](#usage)\n6. [Documentations](#docs)\n7. [Contributors](#contributors)\n8. [More](#more)\n9. [Credits](#credits)\n\n## Overview[![]()](#overview)\n\nGemPyP is a testing and reporting framework that allows automatic execution of testcases along with generation of the report, that enables effortless analysis and monitoring of the set.\n\nThe setting and configurations, including the testcases are passed as a config file to the framework, then GemPyP handles the environments, execution, reporting, storing data and miscellaneous.\n\nIt allows-\n\n- Email integration\n- Parallel execution of testcases\n- Customization of test Suite reports\n- Platform independence (Supports Linux, Windows and MacOS)\n\n## Installation[![]()](#installation)\n\nFor installation make sure require version of python and pip is installed in the system.\n\n```powershell\n$ pip install gempyp\n```\n\n## Requirements[![]()](#requirements)\n\n### Python version 3.6 or above\n\n### Required Libraries\n\n- certifi==2022.6.15\n- cffi==1.15.0\n- charset-normalizer==2.0.12\n- coloredlogs==15.0.1\n- cryptography==37.0.2\n- humanfriendly==10.0\n- idna==3.3\n- lxml==4.9.0\n- ntlm-auth==1.5.0\n- numpy==1.22.4\n- pandas==1.4.2\n- pycparser==2.21\n- pyreadline3==3.4.1\n- python-dateutil==2.8.2\n- pytz==2022.1\n- requests==2.28.0\n- requests-ntlm==1.1.0\n- six==1.16.0\n- urllib3==1.26.9\n\n### These libraries will get downloaded automatically with the package.\n\n## Features[![]()](#features)\n\n1. Easy to use.\n2. Cross Platform.\n3. Multiple modes of execution.\n4. Static Report generated after execution.\n5. Saves Time\n\n## Usage[![]()](#usage)\n\n### Can be used in API Automation and testing python testcases.\n\n## Documentations[![]()](#docs)\n\nThe official documentation is hosted on Read the Docs: https://gempyp.readthedocs.io/en/latest/\n\n## Contributors[![]()](#contributors)\n\nWe welcome and recognize all contributions. You can see a list of current contributors in the [contributors tab](https://github.com/Gemini-Solutions/gempyp/).\n\n## More[![]()](#more)\n\nFor more information visit https://gempyp.gemecosystem.com/ and https://gemecosystem.com/\n\n### Credits[![]()](#credits)\n\n- TODO\n',
    'author': 'Gemini Solutions-QA',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Gemini-Solutions/gempyp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.8,<4.0.0',
}


setup(**setup_kwargs)
