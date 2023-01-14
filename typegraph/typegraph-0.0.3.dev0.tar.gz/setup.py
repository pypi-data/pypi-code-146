# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['typegraph',
 'typegraph.graphs',
 'typegraph.importers',
 'typegraph.materializers',
 'typegraph.materializers.prisma',
 'typegraph.types',
 'typegraph.utils']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'astunparse>=1.6.3,<2.0.0',
 'attrs>=22.2.0,<23.0.0',
 'dataconf>=2.1.3,<3.0.0',
 'deepmerge>=1.1.0,<2.0.0',
 'frozendict==2.3.4',
 'furl>=2.1.3,<3.0.0',
 'gql[requests]>=3.4.0,<4.0.0',
 'graphql-core>=3.2.3,<4.0.0',
 'httpx[http2]>=0.22,<0.24',
 'jsons>=1.6.3,<2.0.0',
 'ordered-set>=4.1.0,<5.0.0',
 'orjson>=3.8.4,<4.0.0',
 'python-box>=6.1.0,<7.0.0',
 'python-dotenv>=0.21.0,<0.22.0',
 'redbaron>=0.9.2,<0.10.0',
 'semver>=2.13.0,<3.0.0',
 'typing-extensions>=4.4.0,<5.0.0']

entry_points = \
{'console_scripts': ['py-tg = typegraph.utils.loaders:cmd']}

setup_kwargs = {
    'name': 'typegraph',
    'version': '0.0.3.dev0',
    'description': 'Free and open ecosystem for API composition.',
    'long_description': 'None',
    'author': 'Metatype Contributors',
    'author_email': 'support@metatype.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://metatype.dev',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
