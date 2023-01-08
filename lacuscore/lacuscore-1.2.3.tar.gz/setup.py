# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lacuscore']

package_data = \
{'': ['*']}

install_requires = \
['defang>=0.5.3,<0.6.0',
 'playwrightcapture[recaptcha]>=1.17.2,<2.0.0',
 'redis[hiredis]>=4.4.1,<5.0.0',
 'requests>=2.28.1,<3.0.0',
 'ua-parser>=0.16.1,<0.17.0']

extras_require = \
{'docs': ['Sphinx>=6.1.2,<7.0.0']}

setup_kwargs = {
    'name': 'lacuscore',
    'version': '1.2.3',
    'description': 'Core of Lacus, usable as a module',
    'long_description': '[![Documentation Status](https://readthedocs.org/projects/lacuscore/badge/?version=latest)](https://lacuscore.readthedocs.io/en/latest/?badge=latest)\n\n# Modulable Lacus\n\nLacus, but as a simple module.\n\n# Installation\n\n```bash\npip install lacuscore\n```\n\n# Design\n\n`LacusCore` is the part taking care of enqueuing and capturing URLs or web enabled documents.\nIt can be used as a module in your own project, see below for the usage\n\n[Lacus](https://github.com/ail-project/lacus) is the webservice that uses `LacusCore`,\nand you can use [Pylacus](https://github.com/ail-project/pylacus) to query it.\n\nThe `enqueue`, `get_capture_status`, and `get_capture` methods if `LacusCore` and `PyLacus` have\nthe same parameters which means you can easily use them interchangeably in your project.\n\n\nFor more information regarding the usage of the module and a few examples, please refer to\n[the documentation](https://lacuscore.readthedocs.io/en/latest/)\n',
    'author': 'Raphaël Vinot',
    'author_email': 'raphael.vinot@circl.lu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
