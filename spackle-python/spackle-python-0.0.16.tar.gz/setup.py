# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spackle']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.26.32,<2.0.0', 'botocore>=1.29.35,<2.0.0', 'requests>=2.28.1,<3.0.0']

setup_kwargs = {
    'name': 'spackle-python',
    'version': '0.0.16',
    'description': '',
    'long_description': '# Spackle Python Library\n\n[![CI](https://github.com/spackleso/spackle-python/actions/workflows/test.yml/badge.svg)](https://github.com/spackleso/spackle-python/actions/workflows/test.yml) [![pypi](https://img.shields.io/pypi/v/spackle-python.svg)](https://pypi.python.org/pypi/spackle-python)\n\nThe Spackle Python library provides optimized access to billing aware flags created on the Spackle platform.\n\n## Documentation\n\nSee the [Python API docs](https://docs.spackle.so/python).\n\n## Setup\n\n### Install the Spackle library\n\n```sh\npip install -U spackle-python\n```\n\n### Configure your environment\nIn order to use Spackle, you need to configure your API key on the `spackle` module. You can find your API key in Spackle app [settings page](https://dashboard.stripe.com/settings/apps/so.spackle.stripe).\n\n```python\nimport spackle\nspackle.api_key = "<api key>"\n```\n\n### Bootstrap the client (optional)\n\nThe Spackle client requires a single initialization step that includes a network request. To front load this process, you can call the `bootstrap` method in your codebase.\n\n```python\nspackle.bootstrap()\n```\n\n## Usage\n\n### Fetch a customer\n\nSpackle uses stripe ids as references to customer features.\n\n```python\ncustomer = spackle.Customer.retrieve("cus_00000000")\n```\n\n### Verify feature access\n\n```python\ncustomer.enabled("feature_key")\n```\n\n### Fetch a feature limit\n\n```python\ncustomer.limit("feature_key")\n```\n\n## Logging\nThe Spackle Python library emits logs as it performs various internal tasks. You can control the verbosity of Spackle\'s logging a few different ways:\n\n1. Set the environment variable SPACKLE_LOG to the value debug or info\n\n   ```sh\n   $ export SPACKLE_LOG=debug\n   ```\n\n2. Set spackle.log:\n\n   ```python\n   import spackle\n   spackle.log = \'debug\'\n   ```\n\n3. Enable it through Python\'s logging module:\n\n   ```python\n   import logging\n   logging.basicConfig()\n   logging.getLogger(\'spackle\').setLevel(logging.DEBUG)\n   ```\n',
    'author': 'Hunter Clarke',
    'author_email': 'hunter@spackle.so',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
