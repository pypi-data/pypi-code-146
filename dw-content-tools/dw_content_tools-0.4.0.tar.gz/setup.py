# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['content_tools']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'click>=8.1.3,<9.0.0',
 'jsonschema>=4.17.3,<5.0.0',
 'pyyaml>=6.0,<7.0']

entry_points = \
{'console_scripts': ['content_tools = content_tools.__main__:content_tools']}

setup_kwargs = {
    'name': 'dw-content-tools',
    'version': '0.4.0',
    'description': '',
    'long_description': '# Content CLI Tools\n\n## Installation\n\n```\n$ pip3 install dw-content-tools\n```\n\n## Module Repository Validator\n\n```\nValidates that a module repo structure and content is valid, based\non the following rules:\n\n* metadata.yml exists\n* metadata.yml is valid\n    * validate JSON schema\n* docker-compose.yml exists\n* docker-compose.yml is valid\n    * validate JSON schema\n* english.md exists\n* validating english.md:\n    * pages:\n        * unique IDs\n        * all pages contain a valid ID\n        * all pages have a name\n    * all images referenced in md exist as static files\n    * activities:\n        * all activities have an unique `id`\n        * all activities have `type` defined\n        * input:\n            * has required `correct-answer` tag\n        * multiple-choice:\n            * has required `answer` (many) tags\n            * at least one answer is marked as `is-correct`\n            * when more than one answer is correct, `widget` has to be `checkbox`\n        * code:\n            * `template` and `device` attrs are defined\n            * has required `validation-code` tag\n```\n',
    'author': 'Martin Zugnoni',
    'author_email': 'mzugnoni@datawars.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
