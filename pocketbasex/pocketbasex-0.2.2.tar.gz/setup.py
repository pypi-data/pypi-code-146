# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pocketbase',
 'pocketbase.models',
 'pocketbase.models.utils',
 'pocketbase.services',
 'pocketbase.services.utils',
 'pocketbase.stores']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.23.0,<0.24.0']

setup_kwargs = {
    'name': 'pocketbasex',
    'version': '0.2.2',
    'description': 'PocketBase SDK for python.',
    'long_description': '# PocketBase Python SDK\n\n[![Tests](https://github.com/vaphes/pocketbase/actions/workflows/tests.yml/badge.svg)](https://github.com/vaphes/pocketbase/actions/workflows/tests.yml)\n\nPython client SDK for the <a href="https://pocketbase.io/">PocketBase</a> backend.\n\nThis is in early development, and at first is just a translation of <a href="https://github.com/pocketbase/js-sdk">the javascript lib</a> using <a href="https://github.com/encode/httpx/">HTTPX</a>.\n\n---\n\n## Installation\n\nInstall PocketBase using pip:\n\n```shell\n$ pip install pocketbase\n```\n\n## Usage\n\nThe rule of thumb here is just to use it as you would <a href="https://github.com/pocketbase/js-sdk">the javascript lib</a>, but in a pythonic way of course!\n\n```python\nfrom pocketbase import PocketBase # Client also works the same\n\nclient = PocketBase(\'http://127.0.0.1:8090\')\n\n...\n\n# list and filter "example" collection records\nresult = client.records.get_list(\n    "example", 1, 20, {"filter": \'status = true && created > "2022-08-01 10:00:00"\'}\n)\n\n# authenticate as regular user\nuser_data = client.users.auth_via_email("test@example.com", "123456")\n\n# or as admin\nadmin_data = client.admins.auth_via_email("test@example.com", "123456")\n\n# and much more...\n```\n> More detailed API docs and copy-paste examples could be found in the [API documentation for each service](https://pocketbase.io/docs/api-authentication). Just remember to \'pythonize it\' 🙃.\n\n\n<p align="center"><i>The PocketBase Python SDK is <a href="https://github.com/vaphes/pocketbase/blob/master/LICENCE.txt">MIT licensed</a> code.</p>',
    'author': 'Aziz Berkay Yesilyurt',
    'author_email': 'abyesilyurt@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/abyesilyurt/pocketbase',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
