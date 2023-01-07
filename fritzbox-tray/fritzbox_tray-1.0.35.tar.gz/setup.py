# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['fritzbox_tray']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.4.0,<10.0.0',
 'aiohttp>=3.8.1,<4.0.0',
 'certifi>=2022.12.7,<2023.0.0',
 'charset-normalizer>=2.1.1,<3.0.0',
 'idna>=3.4,<4.0',
 'pystray>=0.19.4,<0.20.0',
 'requests>=2.28.1,<3.0.0',
 'six>=1.16.0,<2.0.0',
 'urllib3>=1.26.13,<2.0.0']

entry_points = \
{'console_scripts': ['fritzbox-tray = fritzbox_tray.__main__:main']}

setup_kwargs = {
    'name': 'fritzbox-tray',
    'version': '1.0.35',
    'description': 'The description of the package',
    'long_description': 'None',
    'author': 'Andreas Violaris',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/aviolaris/fritzbox-tray',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
