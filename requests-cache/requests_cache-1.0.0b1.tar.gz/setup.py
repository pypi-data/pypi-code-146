# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['requests_cache',
 'requests_cache.backends',
 'requests_cache.models',
 'requests_cache.policy',
 'requests_cache.serializers']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=21.2',
 'cattrs>=22.2',
 'platformdirs>=2.5',
 'requests>=2.22',
 'url-normalize>=1.4',
 'urllib3>=1.25.5']

extras_require = \
{'all': ['boto3>=1.15',
         'botocore>=1.18',
         'pymongo>=3',
         'redis>=3',
         'itsdangerous>=2.0',
         'pyyaml>=5.4',
         'ujson>=5.4'],
 'bson': ['bson>=0.5'],
 'docs': ['furo>=2022.12.7,<2023.0.0',
          'linkify-it-py>=2.0',
          'myst-parser>=0.17',
          'sphinx>=5.0.2,<6.0.0',
          'sphinx-autodoc-typehints>=1.19',
          'sphinx-automodapi>=0.14',
          'sphinx-copybutton>=0.5',
          'sphinx-design>=0.2',
          'sphinx-notfound-page>=0.8',
          'sphinxcontrib-apidoc>=0.3',
          'sphinxext-opengraph>=0.6'],
 'dynamodb': ['boto3>=1.15', 'botocore>=1.18'],
 'json': ['ujson>=5.4'],
 'mongodb': ['pymongo>=3'],
 'redis': ['redis>=3'],
 'security': ['itsdangerous>=2.0'],
 'yaml': ['pyyaml>=5.4']}

setup_kwargs = {
    'name': 'requests-cache',
    'version': '1.0.0b1',
    'description': 'A persistent cache for python requests',
    'long_description': "[![](docs/_static/requests-cache-logo-header.png)](https://requests-cache.readthedocs.io)\n\n[![Build](https://github.com/requests-cache/requests-cache/actions/workflows/build.yml/badge.svg)](https://github.com/requests-cache/requests-cache/actions/workflows/build.yml)\n[![Codecov](https://codecov.io/gh/requests-cache/requests-cache/branch/main/graph/badge.svg?token=FnybzVWbt2)](https://codecov.io/gh/requests-cache/requests-cache)\n[![Documentation](https://img.shields.io/readthedocs/requests-cache/stable)](https://requests-cache.readthedocs.io/en/stable/)\n[![Code Shelter](https://www.codeshelter.co/static/badges/badge-flat.svg)](https://www.codeshelter.co/)\n\n[![PyPI](https://img.shields.io/pypi/v/requests-cache?color=blue)](https://pypi.org/project/requests-cache)\n[![Conda](https://img.shields.io/conda/vn/conda-forge/requests-cache?color=blue)](https://anaconda.org/conda-forge/requests-cache)\n[![PyPI - Python Versions](https://img.shields.io/pypi/pyversions/requests-cache)](https://pypi.org/project/requests-cache)\n[![PyPI - Downloads](https://img.shields.io/pypi/dm/requests-cache?color=blue)](https://pypi.org/project/requests-cache)\n\n## Summary\n**requests-cache** is a persistent HTTP cache that provides an easy way to get better\nperformance with the python [requests](https://requests.readthedocs.io/) library.\n\n<!-- RTD-IGNORE -->\nComplete project documentation can be found at [requests-cache.readthedocs.io](https://requests-cache.readthedocs.io).\n<!-- END-RTD-IGNORE -->\n\n## Features\n* 🍰 **Ease of use:** Keep using the `requests` library you're already familiar with. Add caching\n  with a [drop-in replacement](https://requests-cache.readthedocs.io/en/stable/user_guide/general.html#sessions)\n  for `requests.Session`, or\n  [install globally](https://requests-cache.readthedocs.io/en/stable/user_guide/general.html#patching)\n  to add transparent caching to all `requests` functions.\n* 🚀 **Performance:** Get sub-millisecond response times for cached responses. When they expire, you\n  still save time with\n  [conditional requests](https://requests-cache.readthedocs.io/en/stable/user_guide/headers.html#conditional-requests).\n* 💾 **Persistence:** Works with several\n  [storage backends](https://requests-cache.readthedocs.io/en/stable/user_guide/backends.html)\n  including SQLite, Redis, MongoDB, and DynamoDB; or save responses as plain JSON files, YAML,\n  and more\n* 🕗 **Expiration:** Use\n  [Cache-Control](https://requests-cache.readthedocs.io/en/stable/user_guide/headers.html#cache-control)\n  and other standard HTTP headers, define your own expiration schedule, keep your cache clutter-free\n  with backends that natively support TTL, or any combination of strategies\n* ⚙️ **Customization:** Works out of the box with zero config, but with a robust set of features for\n  configuring and extending the library to suit your needs\n* 🧩 **Compatibility:** Can be combined with other\n  [popular libraries based on requests](https://requests-cache.readthedocs.io/en/stable/user_guide/compatibility.html)\n\n## Quickstart\nFirst, install with pip:\n```bash\npip install requests-cache\n```\n\nThen, use [requests_cache.CachedSession](https://requests-cache.readthedocs.io/en/stable/session.html)\nto make your requests. It behaves like a normal\n[requests.Session](https://requests.readthedocs.io/en/latest/user/advanced/#session-objects),\nbut with caching behavior.\n\nTo illustrate, we'll call an endpoint that adds a delay of 1 second, simulating a slow or\nrate-limited website.\n\n**This takes 1 minute:**\n```python\nimport requests\n\nsession = requests.Session()\nfor i in range(60):\n    session.get('https://httpbin.org/delay/1')\n```\n\n**This takes 1 second:**\n```python\nimport requests_cache\n\nsession = requests_cache.CachedSession('demo_cache')\nfor i in range(60):\n    session.get('https://httpbin.org/delay/1')\n```\n\nWith caching, the response will be fetched once, saved to `demo_cache.sqlite`, and subsequent\nrequests will return the cached response near-instantly.\n\n**Patching:**\nIf you don't want to manage a session object, or just want to quickly test it out in your\napplication without modifying any code, requests-cache can also be installed globally, and all\nrequests will be transparently cached:\n```python\nimport requests\nimport requests_cache\n\nrequests_cache.install_cache('demo_cache')\nrequests.get('https://httpbin.org/delay/1')\n```\n\n**Settings:**\nThe default settings work well for most use cases, but there are plenty of ways to customize\ncaching behavior when needed. Here is a quick example of some of the options available:\n```python\nfrom datetime import timedelta\nfrom requests_cache import CachedSession\n\nsession = CachedSession(\n    'demo_cache',\n    use_cache_dir=True,                # Save files in the default user cache dir\n    cache_control=True,                # Use Cache-Control response headers for expiration, if available\n    expire_after=timedelta(days=1),    # Otherwise expire responses after one day\n    allowable_codes=[200, 400],        # Cache 400 responses as a solemn reminder of your failures\n    allowable_methods=['GET', 'POST'], # Cache whatever HTTP methods you want\n    ignored_parameters=['api_key'],    # Don't match this request param, and redact if from the cache\n    match_headers=['Accept-Language'], # Cache a different response per language\n    stale_if_error=True,               # In case of request errors, use stale cache data if possible\n)\n```\n\n<!-- RTD-IGNORE -->\n## Next Steps\nTo find out more about what you can do with requests-cache, see:\n\n* [User Guide](https://requests-cache.readthedocs.io/en/stable/user_guide.html)\n* [Examples](https://requests-cache.readthedocs.io/en/stable/examples.html)\n* [API Reference](https://requests-cache.readthedocs.io/en/stable/reference.html)\n* [Project Info](https://requests-cache.readthedocs.io/en/stable/project_info.html)\n<!-- END-RTD-IGNORE -->\n",
    'author': 'Roman Haritonov',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/requests-cache/requests-cache',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
