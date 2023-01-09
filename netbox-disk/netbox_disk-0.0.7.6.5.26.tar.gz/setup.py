# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['netbox_disk',
 'netbox_disk.api',
 'netbox_disk.filters',
 'netbox_disk.forms',
 'netbox_disk.migrations',
 'netbox_disk.tables',
 'netbox_disk.views']

package_data = \
{'': ['*'],
 'netbox_disk': ['templates/netbox_disk/*', 'templates/netbox_disk/disk/*']}

setup_kwargs = {
    'name': 'netbox-disk',
    'version': '0.0.7.6.5.26',
    'description': 'Netbox Disk Plugin',
    'long_description': '',
    'author': 'Tim Rhomberg',
    'author_email': 'timrhomberg@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
