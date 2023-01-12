# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipkg',
 'ipkg.cmd',
 'ipkg.pkg',
 'ipkg.pkg.android_studio',
 'ipkg.pkg.brew',
 'ipkg.pkg.cfw',
 'ipkg.pkg.code',
 'ipkg.pkg.conda',
 'ipkg.pkg.docker',
 'ipkg.pkg.edge',
 'ipkg.pkg.fonts',
 'ipkg.pkg.gh',
 'ipkg.pkg.llvm',
 'ipkg.pkg.motrix',
 'ipkg.pkg.obs',
 'ipkg.pkg.reserves_lib_tsinghua_downloader',
 'ipkg.pkg.typora',
 'ipkg.pkg.virtualbox',
 'ipkg.pkg.zotero',
 'ipkg.utils',
 'ipkg.utils.ubuntu']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'httpie>=3.2.1,<4.0.0',
 'questionary>=1.10.0,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'ipkg',
    'version': '0.1.8',
    'description': 'My Package Manager',
    'long_description': '# ipkg\n\nMy Package Manager\n',
    'author': 'Qin Li',
    'author_email': 'liblaf@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://liblaf.github.io/ipkg/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
