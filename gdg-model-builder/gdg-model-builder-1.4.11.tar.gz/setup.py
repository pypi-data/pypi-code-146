# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gdg_model_builder',
 'gdg_model_builder.context.bounds',
 'gdg_model_builder.context.bounds.execution',
 'gdg_model_builder.context.bounds.session',
 'gdg_model_builder.context.bounds.user',
 'gdg_model_builder.context.context',
 'gdg_model_builder.context.execution',
 'gdg_model_builder.context.session',
 'gdg_model_builder.context.user',
 'gdg_model_builder.event',
 'gdg_model_builder.libutil',
 'gdg_model_builder.libutil.np',
 'gdg_model_builder.libutil.sync',
 'gdg_model_builder.model',
 'gdg_model_builder.model_builder_cli',
 'gdg_model_builder.modifiers',
 'gdg_model_builder.sdk',
 'gdg_model_builder.sdk.ncaab']

package_data = \
{'': ['*'], 'gdg_model_builder.model_builder_cli': ['assets/docker/*']}

install_requires = \
['attrs>=21.4.0,<22.0.0',
 'cattrs>=22.1.0,<23.0.0',
 'checksumdir>=1.2.0,<2.0.0',
 'fastapi[all]>=0.78.0,<0.79.0',
 'numpy>=1.23.0,<2.0.0',
 'pycron>=3.0.0,<4.0.0',
 'redis>=4.3.4,<5.0.0']

setup_kwargs = {
    'name': 'gdg-model-builder',
    'version': '1.4.11',
    'description': '',
    'long_description': None,
    'author': 'Liam Monninger',
    'author_email': 'l.mak.monninger@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>3.9,<4.0',
}


setup(**setup_kwargs)
