# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lokalise',
 'lokalise.collections',
 'lokalise.endpoints',
 'lokalise.models',
 'lokalise.oauth2']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28,<3.0']

extras_require = \
{':python_full_version <= "3.7.0"': ['importlib-metadata'],
 ':python_version < "3.11"': ['exceptiongroup']}

setup_kwargs = {
    'name': 'python-lokalise-api',
    'version': '2.1.0',
    'description': 'Official Python interface for the Lokalise API v2',
    'long_description': '# Lokalise API v2 official Python interface\n\n![PyPI](https://img.shields.io/pypi/v/python-lokalise-api)\n![CI](https://github.com/lokalise/python-lokalise-api/actions/workflows/ci.yml/badge.svg)\n[![Downloads](https://pepy.tech/badge/python-lokalise-api)](https://pepy.tech/project/python-lokalise-api)\n[![Docs](https://readthedocs.org/projects/python-lokalise-api/badge/?version=latest&style=flat)](https://python-lokalise-api.readthedocs.io)\n\nOfficial Python 3 interface for the [Lokalise APIv2](https://developers.lokalise.com/reference/lokalise-rest-api) that represents returned data as Python objects.\n\n## Quick start\n\nThis plugin requires Python 3.7 and above. Install it:\n\n    pip install python-lokalise-api\n\nObtain a Lokalise API token (in your *Personal profile*) and use it:\n\n```python\nimport lokalise\nclient = lokalise.Client(\'YOUR_API_TOKEN\')\nproject = client.project(\'123.abc\')\nprint(project.name)\n\nclient.upload_file(project.project_id, {\n    "data": \'ZnI6DQogIHRlc3Q6IHRyYW5zbGF0aW9u\',\n    "filename": \'python_upload.yml\',\n    "lang_iso": \'en\'\n})\n\ntranslation_keys = client.keys(project.project_id, {"page": 2,\n    "limit": 3,\n    "disable_references": "1"})\ntranslation_keys.items[0].key_name[\'web\'] # => "sign_up"\n```\n\nYou can also use [OAuth 2 tokens](https://python-lokalise-api.readthedocs.io/en/latest/additional_info/oauth2_flow.html):\n\n```python\nclient = lokalise.OAuthClient(\'YOUR_OAUTH2_API_TOKEN\')\n\nproject = client.project(\'123.abc\')\n```\n\n## Documentation\n\nFind detailed documentation at [python-lokalise-api.readthedocs.io](https://python-lokalise-api.readthedocs.io).\n\n## License\n\nThis plugin is licensed under the [BSD 3 Clause License](https://github.com/lokalise/python-lokalise-api/blob/master/LICENSE).\n\nCopyright (c) [Lokalise group](https://lokalise.com) and [Ilya Krukowski](http://bodrovis.tech)\n',
    'author': 'Ilya Krukowski',
    'author_email': 'golosizpru@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/lokalise/python-lokalise-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
