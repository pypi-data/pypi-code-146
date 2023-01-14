# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pubhelper']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pubhelper',
    'version': '0.1.3',
    'description': '',
    'long_description': '# PubHelper\n\n- [x] add retry_wraps\n- [x] add rdm_str\n- [x] add md5\n- [x] add ip_2_int\n- [x] add SimplePriorityQueue\n- [x] add Cache\n- [x] add timethis\n- [x] add with_log\n- [x] add params_check\n',
    'author': 'iulmt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
