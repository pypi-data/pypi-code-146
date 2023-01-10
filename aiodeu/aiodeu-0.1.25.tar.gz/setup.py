# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiodeu']

package_data = \
{'': ['*']}

extras_require = \
{'aws': ['boto3>=1.26.20,<2.0.0'],
 'faust': ['faust-streaming[cython,fast]>=0.10.1,<0.11.0',
           'python-schema-registry-client>=2.4.1,<3.0.0']}

entry_points = \
{'console_scripts': ['aiodeu = aiodeu.console:main']}

setup_kwargs = {
    'name': 'aiodeu',
    'version': '0.1.25',
    'description': 'aio data engineering utils',
    'long_description': 'None',
    'author': 'Josh Rowe',
    'author_email': 's-block@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/s-block/aiodeu',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
