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
    'version': '0.0.7.6.5.48',
    'description': 'Netbox Disk Plugin',
    'long_description': '### Directory structure\n\n```\n+- api - The API type\n+- filters - Filters of the models\n+- forms - The ModelForm, ModelFilterForm, ModelImportForm, ModelBulkEditForm\n+- migrations - DB Django Migration\n+- tables - The ModelBaseTable, ModelTable, RelatedModelTable\n+- templates\n  +- netbox_disk - The detail view of each model\n    +- disk - The template content box in the Virtual Machine Model\n+- views - PhysicalvolumeListView, PhysicalvolumeView, PhysicalvolumeEditView, PhysicalvolumeDeleteView, \n           PhysicalvolumeBulkImportView, PhysicalvolumeBulkEditView, PhysicalvolumeBulkDeleteView\n```\n\nBasis:\n- pv:\n  - size\n  - Storage Cluster\n  - virtual_machine\n\nWindows Form:\n- Laufwerk Name (D, E, F)\n- filesystem (ntfs)\n\nLinux Form:\n- vg name\n- lv name\n- path\n- filesystem\n\n\nExtra Filesystem Model & als ChoiceField ausgeben\n\n# Build\npoetry publish --build\n\n\n\ngit add . && git commit -m "0.0.7.6.5.41" && git push',
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
