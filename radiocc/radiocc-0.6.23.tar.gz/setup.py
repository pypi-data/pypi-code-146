# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['radiocc', 'radiocc.old']

package_data = \
{'': ['*'], 'radiocc': ['assets/information/*', 'assets/interface/*']}

install_requires = \
['PyGObject',
 'PyYAML',
 'arrow',
 'bs4',
 'click',
 'colored',
 'dotmap',
 'envtoml',
 'matplotlib',
 'nptyping',
 'numpy',
 'pandas',
 'pudb',
 'pycairo',
 'requests',
 'ruamel.yaml',
 'scipy',
 'spiceypy',
 'tqdm',
 'urlpath']

entry_points = \
{'console_scripts': ['radiocc = radiocc.cli:main']}

setup_kwargs = {
    'name': 'radiocc',
    'version': '0.6.23',
    'description': 'Radio occultations',
    'long_description': '# radiocc\n\n> Provide a tool to compute radio occulations for planetary missions.\n\n---\n\n[Requirements](#requirements) |\n[Installation](#installation) |\n[Usage](#usage) |\n[Configuration](#configuration) |\n[Roadmap](#roadmap) |\n[License](#license)\n\n---\n\n## Requirements\n\n### Ubuntu 21.10\n\n```sh\nsudo apt install -y python3-gi libgirepository1.0-dev libcairo2-dev\ngobject-introspection gir1.2-gtk-3.0\n```\n\n### Fedora 35\n\n```sh\nsudo dnf install gcc cairo-devel pkg-config python3-devel\ngobject-introspection-devel cairo-gobject-devel gtk3\n```\n\n## Installation\n\n```sh\n# Create directory.\nmkdir radiocc && cd radiocc\n\n# Create virtual environnement to install package and activate it.\n# Please read: https://docs.python.org/3/library/venv.html\npython -m venv .env\nsource .env/bin/activate\n\n# Install radiocc\npip install radiocc\n```\n\n## Usage\n\nIf you use **radiocc** as a command-line, you should read the\n[command line guide][command-line-guide file].\n\nIf you decide to use it from Python, you should read the\n[library guide][library-guide file].\n\n## Configuration\n\n**radiocc**\n+ runs a list of input folders gathered in a "to_process" folder\n+ writes the ouputs and saves figures in a "results" folder\n\nTo understand the config file, you should read the\n[config file guide][config-file-guide file].\n\n## Roadmap\n\n+ improve old code for lisibility, portability and testing\n+ optimise code speed\n+ improve CLI interface, library API and config file for parameter tuning\n+ provide GUI interface for parameter tuning and application of corrections\n\n## License\n\nLicensed under the [Apache 2.0 license][license file].\n\n[repo url]: https://gitlab-as.oma.be/radiocc/radiocc\n[pypi url]: https://pypi.org/project/radiocc\n[command-line-guide file]: ./command-line-guide.md\n[library-guide file]: ./doc/usage/library-guide.md\n[config-file-guide file]: ./doc/usage/config-file-guide.md\n[license file]: ./doc/usage/LICENSE\n',
    'author': 'Ananya Krishnan',
    'author_email': 'ananyakrishnaniiserk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab-as.oma.be/radiocc/radiocc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
