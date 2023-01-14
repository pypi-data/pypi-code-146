# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bodhi', 'bodhi.client', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['authlib>=0.15.4',
 'click>=7.1.2',
 'koji>=1.27.1',
 'munch>=2.5.0',
 'requests-kerberos>=0.12']

entry_points = \
{'console_scripts': ['bodhi = bodhi.client.cli:cli']}

setup_kwargs = {
    'name': 'bodhi-client',
    'version': '7.0.1',
    'description': 'Bodhi client',
    'long_description': 'None',
    'author': 'Fedora Infrastructure team',
    'author_email': 'None',
    'maintainer': 'Fedora Infrastructure Team',
    'maintainer_email': 'infrastructure@lists.fedoraproject.org',
    'url': 'https://bodhi.fedoraproject.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
