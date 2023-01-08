# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['spoor']

package_data = \
{'': ['*']}

install_requires = \
['datadog>=0.44.0,<0.45.0', 'rich>=12.6.0,<13.0.0', 'varname>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'spoor',
    'version': '0.6.0',
    'description': 'Track functions invocations',
    'long_description': '## spoor\n\n![Tests](https://github.com/bmwant/spoor/actions/workflows/tests.yml/badge.svg)\n[![PyPI](https://img.shields.io/pypi/v/spoor)](https://pypi.org/project/spoor/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/spoor)\n\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![EditorConfig](https://img.shields.io/badge/-EditorConfig-grey?logo=editorconfig)](https://editorconfig.org/)\n[![semantic-release: angular](https://img.shields.io/badge/semantic--release-angular-e10079?logo=semantic-release)](https://github.com/semantic-release/semantic-release)\n\n\nTrack invocation of your functions and methods; display collected statistics for the invocations; export data gathered to external services.\n\n```bash\n$ pip install spoor\n```\n\n### Usage\n\n```python\nfrom spoor import Spoor\n\ns = Spoor()\n\n@s.track\ndef func(a: int, b: int) -> int:\n  return a + b\n\nfunc(5, 10)\nfunc(23, 42)\n\nassert s.called(func)\nassert s.call_count(func) == 2\n```\n\n### Configuration\n\n| Option | Type | Default | Description |\n|--------|------|---------|-------------|\n| `attach` | `bool` | `False` | Expose `called`/`call_count` attributes directly on a function/method object. |\n|`distinct_instances` | `bool` | `False` | Separate metrics collection for each instance of a class. Has no effect if tracking only functions. |\n|`skip_dunder` | `bool` | `True` | Do not track double underscore method calls (like `__str__`) for class instances. Has no effect if tracking only functions. |\n| `disabled` | `bool` | `False` | Initialize as inactive and ignore metrics collection until enabled explicitly. Can be controlled via `enable()`/`disable()` methods later. |\n\n\n### Exporters\n\n* [statsd](#)\n* [DataDog](#)\n\n### See also\n\n* 🍒 [podmena](https://github.com/bmwant/podmena) for nice commits emoji\n* 🌈 [rich](https://github.com/Textualize/rich) for beautiful terminal output\n* 🇺🇦 [United 24](https://u24.gov.ua/) to support Ukraine in the war\n',
    'author': 'Misha Behersky',
    'author_email': 'bmwant@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
