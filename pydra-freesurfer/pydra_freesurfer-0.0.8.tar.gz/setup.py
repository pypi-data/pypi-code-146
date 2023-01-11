# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydra',
 'pydra.tasks.freesurfer',
 'pydra.tasks.freesurfer.recon_all',
 'pydra.tasks.freesurfer.recon_all.tests']

package_data = \
{'': ['*']}

install_requires = \
['pydra>=0.21,<0.22']

setup_kwargs = {
    'name': 'pydra-freesurfer',
    'version': '0.0.8',
    'description': 'Pydra tasks for FreeSurfer',
    'long_description': "# pydra-freesurfer\n\n[![PyPI - Version](https://img.shields.io/pypi/v/pydra-freesurfer.svg)](https://pypi.org/project/pydra-freesurfer)\n[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pydra-freesurfer.svg)](https://pypi.org/project/pydra-freesurfer)\n\n---\n\nPydra tasks for FreeSurfer.\n\n[Pydra][pydra] is a dataflow engine\nwhich provides a set of lightweight abstractions\nfor DAG construction, manipulation, and distributed execution.\n\n[FreeSurfer][freesurfer] is a neuroimaging toolkit\nfor processing, analyzing, and visualizing human brain MR images.\n\nThis project exposes some of FreeSurfer's utilities as Pydra tasks\nto facilitate their incorporation into more advanced processing workflows.\n\n**Table of contents**\n\n- [Installation](#installation)\n- [Available interfaces](#available-interfaces)\n- [Development](#development)\n- [Licensing](#licensing)\n\n## Installation\n\n```console\npip install pydra-freesurfer\n```\n\n## Available interfaces\n\n- gtmseg\n- mri_convert\n- mri_surf2surf\n- mri_vol2vol\n- mris_anatomical_stats\n- mris_ca_label\n- mris_ca_train\n- mris_expand\n- mris_preproc\n- recon-all\n- tkregister2\n\n## Development\n\nThis project is managed using [Poetry].\n\nTo install, check and test the code:\n\n```console\nmake\n```\n\nTo run the test suite when hacking:\n\n```console\nmake test\n```\n\nTo format the code before review:\n\n```console\nmake format\n```\n\nTo build the project's documentation:\n\n```console\nmake docs\n```\n\n## Licensing\n\nThis project is released under the terms of the [Apache License, Version 2.0][license].\n\n[pydra]: https://nipype.github.io/pydra\n[freesurfer]: https://surfer.nmr.mgh.harvard.edu\n[poetry]: https://python-poetry.org\n[license]: https://opensource.org/licenses/Apache-2.0\n",
    'author': 'The Aramis Lab',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aramis-lab/pydra-freesurfer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
