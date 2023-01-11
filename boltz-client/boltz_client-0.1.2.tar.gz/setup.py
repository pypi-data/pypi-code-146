# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boltz_client']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['click>=8', 'embit>=0.4', 'httpx>=0.23', 'websockets>=10']

entry_points = \
{'console_scripts': ['boltz = boltz_client.cli:main']}

setup_kwargs = {
    'name': 'boltz-client',
    'version': '0.1.2',
    'description': 'python boltz client',
    'long_description': '# boltz.exchange python client\nA boltz.exchange client for python\n\n## installing\n```console\npoetry install\n```\n\n## running cli\n```console\npoetry run boltz\n```\n\n## starting regtest\n```console\ncd docker\nchmod +x regtest\n./regtest\n```\n\n## running tests\n```console\npoetry run pytest\n```\n',
    'author': 'dni',
    'author_email': 'office@dnilabs.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://boltz.exchange',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
