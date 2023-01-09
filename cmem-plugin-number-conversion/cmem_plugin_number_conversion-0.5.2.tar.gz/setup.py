# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmem_plugin_number_conversion', 'cmem_plugin_number_conversion.transform']

package_data = \
{'': ['*']}

install_requires = \
['cmem-plugin-base>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'cmem-plugin-number-conversion',
    'version': '0.5.2',
    'description': 'Convert numbers between different number bases (binary, octal, decimal, hexadecimal).',
    'long_description': '# cmem-plugin-number-conversion\n\nTransform plugin allows users to easily convert numbers from one base to another.\n\nThis is a plugin for [eccenca](https://eccenca.com) [Corporate Memory](https://documentation.eccenca.com).\n\nYou can install it with the [cmemc](https://eccenca.com/go/cmemc) command line\nclients like this:\n\n```\ncmemc admin workspace python install cmem-plugin-number-conversion\n```\n\n',
    'author': 'eccenca GmbH',
    'author_email': 'cmempy-developer@eccenca.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/eccenca/cmem-plugin-number-conversion',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
