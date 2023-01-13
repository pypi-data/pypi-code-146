# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['philbot-voice']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.2.2,<3.0.0',
 'PyNaCl>=1.5.0,<2.0.0',
 'PyOgg==0.6.14a1',
 'opentelemetry-exporter-otlp-proto-http>=1.15.0,<2.0.0',
 'opentelemetry-instrumentation-flask>=0.36b0,<0.37',
 'opentelemetry-instrumentation>=0.36b0,<0.37',
 'opentelemetry-sdk>=1.15.0,<2.0.0',
 'websocket-client>=1.4.2,<2.0.0',
 'youtube_dl>=2021.12.17,<2022.0.0']

entry_points = \
{'console_scripts': ['philbot-voice = voice:main']}

setup_kwargs = {
    'name': 'philbot-voice',
    'version': '0.33.0',
    'description': '',
    'long_description': 'None',
    'author': 'philipp.lengauer',
    'author_email': 'p.lengauer@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
