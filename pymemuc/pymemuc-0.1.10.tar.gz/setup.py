# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymemuc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymemuc',
    'version': '0.1.10',
    'description': 'A Memuc.exe wrapper for Python',
    'long_description': "# pymemuc\n\n[![GitHub](https://img.shields.io/github/license/marmig0404/pymemuc)](LICENSE) [![Documentation Status](https://readthedocs.org/projects/pymemuc/badge/?version=latest)][full_doc] [![PyPI](https://img.shields.io/pypi/v/pymemuc) ![PyPI - Downloads](https://img.shields.io/pypi/dm/pymemuc)][pypi_link] [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pymemuc)][python_link] [![CodeFactor](https://www.codefactor.io/repository/github/marmig0404/pymemuc/badge)][codefactor_link]\n\nA wrapper for [MEmu Command (MEMUC)][memuc_docs] in python.\n\nAllows for easy interaction with MEmu VMs, including VM image management, VM control, running VM commands and ADB interaction.\n\n## Installation\n\n```bash\npip install pymemuc\n```\n\n## Example usage\n\n```python\n# import the PyMemuc class\nfrom pymemuc import PyMemuc\n\n# create a PyMemuc instance, doing so will automatically link to the MEMUC executable\nmemuc = PyMemuc()\n\n# create a new vm\nmemuc.create_vm()\n\n# list out all vms, get the index of the first one\nindex = memuc.list_vm_info()[0]['index']\n\n# start the vm\nmemuc.start_vm(index)\n\n# stop the vm\nmemuc.stop_vm(index)\n```\n\nSee [the demo notebook][demo_notebook] for more examples.\n\n## Documentation\n\nSee the [API documentation][full_doc].\n\n[python_link]: https://www.python.org/\n[pypi_link]: https://pypi.org/project/pymemuc/\n[codefactor_link]: https://www.codefactor.io/repository/github/marmig0404/pymemuc\n[memuc_docs]: https://www.memuplay.com/blog/memucommand-reference-manual.html\n[demo_notebook]: demo/demo.ipynb\n[full_doc]: https://pymemuc.readthedocs.io\n",
    'author': 'Martin Miglio',
    'author_email': 'code@martinmiglio.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/marmig0404/pymemuc',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
