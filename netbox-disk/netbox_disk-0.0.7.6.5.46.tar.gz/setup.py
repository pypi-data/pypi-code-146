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
    'version': '0.0.7.6.5.46',
    'description': 'Netbox Disk Plugin',
    'long_description': 'Basis:\n- pv:\n  - size\n  - Storage Cluster\n  - virtual_machine\n\nWindows Form:\n- Laufwerk Name (D, E, F)\n- filesystem (ntfs)\n\nLinux Form:\n- vg name\n- lv name\n- path\n- filesystem\n\n\nExtra Filesystem Model & als ChoiceField ausgeben\n\n# Build\npoetry publish --build\n\n\n\ngit add . && git commit -m "0.0.7.6.5.41" && git push',
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
