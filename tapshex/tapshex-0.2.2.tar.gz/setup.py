# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tapshex']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'dataclasses>=0.6,<0.7',
 'dctap>=0.4.0,<0.5.0',
 'pip-tools>=6.12.1,<7.0.0']

setup_kwargs = {
    'name': 'tapshex',
    'version': '0.2.2',
    'description': 'Converts Tabular Application Profile into ShEx Schema',
    'long_description': 'tapshex\n=======\n\nGenerate ShEx from tabular application profiles in DCTAP format.\n\nInstallation\n------------\n\n.. code-block:: bash\n\n    $ git clone https://github.com/tombaker/tapshex.git\n    $ cd tapshex\n    $ python -m venv .venv\n    $ source .venv/bin/activate\n    $ python3 -m pip install flit Pygments\n    $ flit install -s\n\n',
    'author': 'Tom Baker',
    'author_email': 'tom@tombaker.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pypi.org/project/tapshex/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
