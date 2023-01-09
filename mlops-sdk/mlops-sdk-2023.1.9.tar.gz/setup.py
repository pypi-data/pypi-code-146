# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mlops',
 'mlops_sdk',
 'mlops_sdk.config',
 'mlops_sdk.data',
 'mlops_sdk.data.batch',
 'mlops_sdk.data.batch.models',
 'mlops_sdk.data.data',
 'mlops_sdk.data.datasets',
 'mlops_sdk.data.datasets.models',
 'mlops_sdk.data.datasets.models.params',
 'mlops_sdk.data.query',
 'mlops_sdk.experiments',
 'mlops_sdk.ml',
 'mlops_sdk.models',
 'mlops_sdk.rec',
 'mlops_sdk.rec.channels',
 'mlops_sdk.rec.channels.models',
 'mlops_sdk.rec.experiments',
 'mlops_sdk.rec.experiments.models',
 'mlops_sdk.rec.recommendations',
 'mlops_sdk.rec.recommendations.models',
 'mlops_sdk.utils']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.8.1,<4.0.0',
 'black>=21.9b0,<22.0',
 'boto3',
 'cloudpickle>=2.1.0,<3.0.0',
 'flake8>=4.0.1,<5.0.0',
 'hvac>=0.11.2,<0.12.0',
 'pydantic>=1.10.1,<2.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'requests>=2.26.0,<3.0.0',
 'slack-sdk>=3.11.2,<4.0.0',
 'tabulate>=0.8.7',
 'termcolor>=1.1.0,<2.0.0']

extras_require = \
{'all': ['torch>=1.10.0,<2.0.0',
         'torchdiffeq>=0.2.2,<0.3.0',
         'tensorboard>=2.7.0,<3.0.0'],
 'models-torch': ['torch>=1.10.0,<2.0.0',
                  'torchdiffeq>=0.2.2,<0.3.0',
                  'tensorboard>=2.7.0,<3.0.0']}

setup_kwargs = {
    'name': 'mlops-sdk',
    'version': '2023.1.9',
    'description': 'mlops-sdk for data play',
    'long_description': None,
    'author': 'AI Engineering Chapter 정유선',
    'author_email': 'jerryjung@emart.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8.8,<=3.9.5',
}


setup(**setup_kwargs)
