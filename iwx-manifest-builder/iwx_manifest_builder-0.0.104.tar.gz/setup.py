# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iwx_manifest_builder',
 'iwx_manifest_builder.schema',
 'iwx_manifest_builder.schema.document']

package_data = \
{'': ['*']}

install_requires = \
['beartype>=0.10.4,<0.11.0',
 'loguru>=0.6.0,<0.7.0',
 'marshmallow-jsonschema>=0.13.0,<0.14.0',
 'marshmallow>=3.15.0,<4.0.0']

setup_kwargs = {
    'name': 'iwx-manifest-builder',
    'version': '0.0.104',
    'description': 'Validates data used in building an iwx manifest file.',
    'long_description': '# iwx-manifest-builder\n\nThs Internal Workflow Exchange library provides schemas needed to validate the data passed between FSAI workflows. ',
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
