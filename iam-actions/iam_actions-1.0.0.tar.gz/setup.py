# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iam_actions']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0']

setup_kwargs = {
    'name': 'iam-actions',
    'version': '1.0.0',
    'description': 'Generate JSON of AWS policy components',
    'long_description': '# iam_actions\n\nConsume AWS IAM information\n\n## Usage\n\n```python\nimport iam_actions\n\nprint(item_actions.services)\nprint(item_actions.actions)\nprint(item_actions.resource_types)\n```\n',
    'author': 'Constable',
    'author_email': 'info@constableapp.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
