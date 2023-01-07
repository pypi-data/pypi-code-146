# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['nerdbridge']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['bridge = nerdbridge.run:run']}

setup_kwargs = {
    'name': 'nerdbridge',
    'version': '0.2.0',
    'description': 'server and client for playing bridge in asci format',
    'long_description': "# nerdbridge\n\nthe nerdbridge package contains a minimal version of a bridge server and client which allows running a (local) bridge server from the command line and connecting 4 clients to it.\nThe clients get an asci style window which shows the hand and allows them to do the bidding and play the game.\n\nThere's also a scorecalc which can calculate the score for each hand after it has been played, but that has not yet been implemented.\n",
    'author': 'Pythor and Keumes',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
