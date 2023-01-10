# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datadis']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.19,<0.24']

setup_kwargs = {
    'name': 'datadis',
    'version': '1.0.0',
    'description': 'Datadis API client',
    'long_description': '\n# Datadis\n\nPython client for https://datadis.es\n\n![GitHub](https://img.shields.io/github/license/mrmarble/datadis)\n[![Semantic Release](https://github.com/MrMarble/datadis/actions/workflows/release.yml/badge.svg)](https://github.com/MrMarble/datadis/actions/workflows/release.yml)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/datadis)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=MrMarble_datadis&metric=alert_status)](https://sonarcloud.io/dashboard?id=MrMarble_datadis)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/datadis)\n\n## Installation\n\nFrom [PyPi](https://pypi.org/project/datadis/)\n\n```bash\npip install datadis\n```\n    \n## Usage/Examples\n\n```python\nimport asyncio\nfrom datadis import get_token, get_supplies\n\ntoken = asyncio.run(get_token(\'username\', \'password\'))\n\nsupplies = asyncio.run(get_supplies(token))\n\n#[\n#    {\n#        "address": "home",\n#        "cups": "1234ABC",\n#        "postalCode": "1024",\n#        "province": "madrid",\n#        "municipality": "madrid",\n#        "distributor": "Energy",\n#        "validDateFrom": "2020/09",\n#        "validDateTo": "2021/09",\n#        "pointType": 0,\n#        "distributorCode": "2"\n#    }\n#]\n```\n\n  ',
    'author': 'Alvaro Tinoco',
    'author_email': 'alvarotinocomarmol@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
