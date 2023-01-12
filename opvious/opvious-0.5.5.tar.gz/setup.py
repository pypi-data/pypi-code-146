# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opvious', 'opvious.executors']

package_data = \
{'': ['*']}

install_requires = \
['backoff>=2.2,<3.0', 'humanize>=4.4.0,<5.0.0', 'pandas>=1.4,<2.0']

extras_require = \
{'aio': ['aiohttp>=3.8,<4.0', 'Brotli>=1.0.9,<2.0.0']}

setup_kwargs = {
    'name': 'opvious',
    'version': '0.5.5',
    'description': 'Opvious Python SDK',
    'long_description': "# Opvious Python SDK  [![CI](https://github.com/opvious/sdk.py/actions/workflows/ci.yml/badge.svg)](https://github.com/opvious/sdk.py/actions/workflows/ci.yml) [![Pypi badge](https://badge.fury.io/py/opvious.svg)](https://pypi.python.org/pypi/opvious/)\n\nThis package provides a lightweight SDK for solving optimization models with the\n[Opvious API][api]. Its main features are:\n\n+ Seamless data import/export via native support for [`pandas`][pandas]\n+ Powerful built-in debugging capabilities: automatic infeasibility relaxation,\n  variable pinning, and more\n+ Non-blocking APIs for performant parallel calls\n\n\n## Quickstart\n\nFirst, install this package and have an API access token handy (these can be\ngenerated [here][token]).\n\n```sh\npip install opvious[aio] # aio is recommended for improved performance\n```\n\nWith these steps out of the way, you are ready to solve any formulation:\n\n```python\nimport opvious\n\n# Instantiate an API client from an API token\nclient = opvious.Client.from_token(TOKEN)\n\n# Assemble and validate inputs for a registered formulation\ninputs = await client.assemble_inputs(\n    formulation_name='my-formulation',\n    parameters={\n        # Formulation parameters...\n    }\n)\n\n# Start an attempt and wait for it to complete\nattempt = await client.start_attempt(inputs)\n\n# Wait for the attempt to complete\noutcome = await client.wait_for_outcome(attempt)\n```\n\n\n## Environments\n\nClients are compatible with Pyodide environments, for example [JupyterLite][]\nkernels. Simply install the package as usual in a notebook, omitting the `aio`\noptional dependencies:\n\n```python\nimport piplite\nawait piplite.install('opvious')\n```\n\nIn other environments, prefer using the `aiohttp`-powered clients as they are\nmore performant (this is the default if the `aio` dependencies were specified).\n\n\n## Next steps\n\nThis SDK is focused on solving optimization models. For convenient access to the\nrest of Opvious API's functionality, consider using the [TypeScript SDK and\nCLI][cli].\n\n\n[api]: https://www.opvious.io\n[cli]: https://www.opvious.io/sdk.ts\n[JupyterLite]: https://jupyterlite.readthedocs.io/\n[token]: https://hub.beta.opvious.io/authorizations\n[pandas]: https://pandas.pydata.org\n",
    'author': 'Opvious Engineering',
    'author_email': 'oss@opvious.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/opvious/sdk.py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
