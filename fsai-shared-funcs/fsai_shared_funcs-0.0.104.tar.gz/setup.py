# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fsai_shared_funcs', 'fsai_shared_funcs.proto_helpers']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.10.4,<0.11.0',
 'google>=3.0.0,<4.0.0',
 'jsonlines>=3.1.0,<4.0.0',
 'loguru>=0.6.0,<0.7.0',
 'pydash>=5.1.0,<6.0.0']

setup_kwargs = {
    'name': 'fsai-shared-funcs',
    'version': '0.0.104',
    'description': 'Simple functions shared across fsai apps.',
    'long_description': '# fsai-shared-funcs\n\nSimple functions shared across fsai apps.\n\n## Installation\n```shell\npoetry add fsai-shared-funcs\n```',
    'author': 'Michael Mohamed',
    'author_email': 'michael@foundationstack.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fsai-dev/fsai-cli-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
