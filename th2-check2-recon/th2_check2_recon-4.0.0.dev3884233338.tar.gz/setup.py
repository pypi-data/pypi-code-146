# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['th2_check2_recon',
 'th2_check2_recon.util',
 'th2_check2_recon.util.cache',
 'th2_check2_recon.util.events']

package_data = \
{'': ['*']}

install_requires = \
['sortedcollections==2.1.0',
 'th2-common==3.10.0.dev3369178157',
 'th2-grpc-crawler-data-processor==0.4.0.dev3361134587',
 'th2-grpc-util==3.1.0.dev3360864447']

setup_kwargs = {
    'name': 'th2-check2-recon',
    'version': '4.0.0.dev3884233338',
    'description': 'Python library for creating th2-check2-recon applications.',
    'long_description': 'This repository is a library for creating th2-check2-recon applications.\n\n## Installation\n```\npip install th2-check2-recon\n```\nThis package can be found on [PyPI](https://pypi.org/project/th2-check2-recon/ "th2-check2-recon").\n',
    'author': 'TH2-devs',
    'author_email': 'th2-devs@exactprosystems.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/th2-net/th2-check2-recon',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
