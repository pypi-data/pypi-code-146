# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['neptune_aws', 'neptune_aws.impl']

package_data = \
{'': ['*']}

install_requires = \
['neptune-client>=0.10.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata'],
 'dev': ['pre-commit', 'pytest>=5.0', 'pytest-cov==2.10.1']}

setup_kwargs = {
    'name': 'neptune-aws',
    'version': '0.1.0',
    'description': 'Neptune.ai Tools for using Neptune client on AWS integration library',
    'long_description': '# Neptune - Tools for using Neptune client on AWS\n\nTODO: Update docs link\nSee [the official docs](https://docs.neptune.ai/integrations-and-supported-tools/model-training/).\n',
    'author': 'neptune.ai',
    'author_email': 'contact@neptune.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://neptune.ai/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
