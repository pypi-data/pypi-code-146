# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['middleware_client']

package_data = \
{'': ['*']}

install_requires = \
['scramjet-client-utils>=1.0.0,<2.0.0', 'scramjet-manager-client>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'scramjet-middleware-client',
    'version': '1.0.0',
    'description': '',
    'long_description': '<h1 align="center"><strong>Scramjet Middleware client</strong></h1>\n\n<p align="center">\n    <a href="https://github.com/scramjetorg/transform-hub/blob/HEAD/LICENSE"><img src="https://img.shields.io/github/license/scramjetorg/transform-hub?color=green&style=plastic" alt="GitHub license" /></a>\n    <a href="https://scr.je/join-community-mg1"><img alt="Discord" src="https://img.shields.io/discord/925384545342201896?label=discord&style=plastic"></a>\n</p>\n\n## About:\n\nThis package provides a **Middleware client** to let you connect with your Scramjet Cloud Platform account.\n\n\n## Usage:\n> ❗NOTE: You need to provide your middleware [access token](https://docs.scramjet.org/platform/quick-start#step-1-set-up-the-environment) if you are not hosting STH locally.\n\n```python\nimport asyncio\nimport json\nfrom middleware_client.middleware_client import MiddlewareClient\nfrom client_utils import ClientUtils\n\n# your middleware token\ntoken = \'\'\n\n# set the token\nClientUtils.setDefaultHeaders({\'Authorization\': f\'Bearer {token}\'})\n\n# middleware url\napi_base =\'https://api.scramjet.cloud/api/v1\' \n\nmiddleware = MiddlewareClient(api_base)\nres = asyncio.run(middleware.get_managers())\n# convert response to json\nmanagers = json.loads(res)\n```\n',
    'author': 'Scramjet',
    'author_email': 'open-source@scramjet.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
