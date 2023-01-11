# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ntfy_lite']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.1.3,<8.0.0',
 'requests>=2.28.1,<3.0.0',
 'types-requests>=2.28.11.2,<3.0.0.0',
 'validators>=0.20.0,<0.21.0']

setup_kwargs = {
    'name': 'ntfy-lite',
    'version': '1.0.1',
    'description': 'minimalistic python API for sending ntfy notifications',
    'long_description': '![unit tests](https://github.com/MPI-IS/ntfy_lite/actions/workflows/tests.yaml/badge.svg)\n![mypy](https://github.com/MPI-IS/ntfy_lite/actions/workflows/python_mypy.yml/badge.svg)\n\n# NTFY LITE\n\n**ntfy_lite** is a minimalistic python API for sending [ntfy](https://ntfy.sh) notifications.\n\nIt comes with a **Handler** for the [logging package](https://docs.python.org/3/library/logging.html).\n\n\n## Installation\n\nfrom source:\n\n```bash\ngit clone https://github.com/MPI-IS/ntfy_lite.git\ncd ntfy_lite\npip install .\n```\n\nfrom pypi:\n```bash\npip install ntfy_lite\n```\n\n## Usage\n\nThe two following examples cover the full API.\nYou may also find the code in the demos folder of the sources.\n\n### pushing notifications\nhttps://github.com/MPI-IS/ntfy_lite/blob/da5750eed1ed58eacf4ff1bb1498586b41242f70/demos/ntfy_push.py#L1-L73\n\n### logging handler\n\nhttps://github.com/MPI-IS/ntfy_lite/blob/52fc7f008fdac3f735d39dd01064a0aa5b751e00/demos/ntfy_logging.py#L1-L146\n\n## Limitation\n\nNo check regarding ntfy [limitations](https://ntfy.sh/docs/publish/#limitations) is performed before notifications are sent.\n\n## Copyright\n\n© 2020, Max Planck Society - Max Planck Institute for Intelligent Systems\n\n',
    'author': 'Vincent Berenz',
    'author_email': 'vberenz@tuebingen.mpg.de',
    'maintainer': 'Vincent Berenz',
    'maintainer_email': 'vberenz@tuebingen.mpg.de',
    'url': 'https://github.com/MPI-IS/ntfy_lite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
