# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['iotitc', 'iotitc.bbddinflux', 'iotitc.raspberry']

package_data = \
{'': ['*']}

install_requires = \
['influxdb>=5.3.1,<6.0.0', 'pandas>=1.5.2,<2.0.0', 'psutil>=5.9.4,<6.0.0']

setup_kwargs = {
    'name': 'iotitc',
    'version': '0.1.1',
    'description': '',
    'long_description': '"iotic"',
    'author': 'CristianTacoronteRivero',
    'author_email': 'cristiantr.develop@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
