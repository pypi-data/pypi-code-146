# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cmem_plugin_examples',
 'cmem_plugin_examples.transform',
 'cmem_plugin_examples.workflow']

package_data = \
{'': ['*']}

install_requires = \
['cmem-plugin-base>=2.1.0,<3.0.0']

setup_kwargs = {
    'name': 'cmem-plugin-examples',
    'version': '0.1.0',
    'description': 'Example plugins for eccenca Corporate Memory.',
    'long_description': '# cmem-plugin-examples\n\nExample plugins for eccenca Corporate Memory.\n\nThis is a plugin for [eccenca](https://eccenca.com) [Corporate Memory](https://documentation.eccenca.com).\n\nYou can install it with the [cmemc](https://eccenca.com/go/cmemc) command line\nclients like this:\n\n```\ncmemc admin workspace python install cmem-plugin-examples\n```\n\n',
    'author': 'eccenca',
    'author_email': 'cmempy-developer@eccenca.com',
    'maintainer': 'Sebastian Tramp',
    'maintainer_email': 'sebastian.tramp@eccenca.com',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
