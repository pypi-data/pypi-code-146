# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kubectlgetall']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0']

entry_points = \
{'console_scripts': ['kubectlgetall = kubectlgetall.cli:cli']}

setup_kwargs = {
    'name': 'kubectlgetall',
    'version': '0.1.2',
    'description': 'Get a list of CRs for cluster CRDs in a namespace',
    'long_description': '# kubectlgetall\n\nList all CR\'s for all CRD types on a cluster in a given namespace.\n\n**Requires kubectl to be installed.**\n\n## Usage\n\n```shell\nkubectlgetall <namespace>\n```\n\nThere are some flags that can be passed.\n```shell\nkubectlgetall --help\nUsage: kubectlgetall [OPTIONS] NAMESPACE\n\n  Returns a list of CR for the different CRDs in a given namespace\n\nOptions:\n  --version           Show the version and exit.\n  -s, --sort          Prints the resources in an order. Initial results take\n                      longer to show. Unsorted return results faster but can\n                      hit rate limits.\n  -e, --exclude TEXT  Exclude crd types. Multiple can be excluded eg: "-e <crd\n                      type> -e <other type>"\n  --help              Show this message and exit.\n\n\n```',
    'author': 'Jim Fitzpatrick',
    'author_email': 'jimfity@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Boomatang/kubectlgetall',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
