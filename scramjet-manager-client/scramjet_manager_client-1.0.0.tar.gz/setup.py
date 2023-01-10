# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['manager_client']

package_data = \
{'': ['*']}

install_requires = \
['scramjet-api-client>=1.0.0,<2.0.0', 'scramjet-client-utils>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'scramjet-manager-client',
    'version': '1.0.0',
    'description': '',
    'long_description': '<h1 align="center"><strong>Scramjet Manager client</strong></h1>\n\n<p align="center">\n    <a href="https://github.com/scramjetorg/transform-hub/blob/HEAD/LICENSE"><img src="https://img.shields.io/github/license/scramjetorg/transform-hub?color=green&style=plastic" alt="GitHub license" /></a>\n    <a href="https://scr.je/join-community-mg1"><img alt="Discord" src="https://img.shields.io/discord/925384545342201896?label=discord&style=plastic"></a>\n</p>\n\n## About:\n\nThis package provides a **Manager client** which manages [Transform Hub](https://github.com/scramjetorg/transform-hub) clients.\n\n## Usage:\n\n> ❗NOTE: You need to provide your middleware [access token](https://docs.scramjet.org/platform/quick-start#step-1-set-up-the-environment) if you are not hosting STH locally.\n\n```python\nimport asyncio\nimport json\nfrom manager_client.manager_client import ManagerClient\nfrom client_utils import ClientUtils\n\n# your middleware token\ntoken = \'\'\n\n# set the token\nClientUtils.setDefaultHeaders({\'Authorization\': f\'Bearer {token}\'})\n\n# middleware url\napi_base =\'https://api.scramjet.cloud/api/v1\' \n\n# url = {middlewareURL}/space/{manager_id}/api/v1\nmanager = ManagerClient(f\'{api_base}/space/org-aa5bu150-9o5c-489b-83e3-b1yf7e086f3h-manager/api/v1\')\nres = asyncio.run(manager.get_hosts())\n# convert response to json\nhosts = json.loads(res)\n```\n',
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
