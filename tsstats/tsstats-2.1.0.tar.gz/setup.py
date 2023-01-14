# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tsstats', 'tsstats.tests']

package_data = \
{'': ['*'], 'tsstats': ['templates/*'], 'tsstats.tests': ['res/*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0', 'pendulum>=2.1.2,<3.0.0']

entry_points = \
{'console_scripts': ['tsstats = tsstats.__main__:cli']}

setup_kwargs = {
    'name': 'tsstats',
    'version': '2.1.0',
    'description': 'A simple Teamspeak stats generator',
    'long_description': "TeamspeakStats |Build Status| |Build status| |Coverage Status| |PyPI| |Documentation Status|\n==========================================================================================================\n\nA simple Teamspeak stat-generator - based solely on server-logs\n\n|screenshot|\n\nInstallation\n============\n\n-  Install the package via PyPi ``pip install tsstats``\n-  Clone this repo\n   ``git clone https://github.com/Thor77/TeamspeakStats`` and install\n   with ``python setup.py install``\n-  Just use the package as is via ``python -m tsstats [-h]``\n\nUsage\n=====\n\n-  Run the script ``tsstats [-h]``\n-  Optionally create a config-file (see\n   `Configuration <https://teamspeakstats.readthedocs.io/en/latest/config.html>`__)\n-  The package works entirely off your Teamspeak server's logs, so that\n   no ServerQuery account is necessary\n\nExample\n=======\n\n::\n\n    tsstats -l /var/log/teamspeak3-server/ -o /var/www/tsstats.html\n\nParse logs in ``/var/log/teamspeak3-server`` and write output to ``/var/www/tsstats.html``.\n\nFor more details checkout the `documentation <http://teamspeakstats.readthedocs.io/en/latest/>`__!\n\n.. |screenshot| image:: https://raw.githubusercontent.com/Thor77/TeamspeakStats/master/screenshot.png\n.. |Build Status| image:: https://travis-ci.org/Thor77/TeamspeakStats.svg?branch=master\n   :target: https://travis-ci.org/Thor77/TeamspeakStats\n.. |Build status| image:: https://ci.appveyor.com/api/projects/status/u9cx7krwmmevbvl2/branch/master?svg=true\n   :target: https://ci.appveyor.com/project/Thor77/teamspeakstats\n.. |Coverage Status| image:: https://coveralls.io/repos/Thor77/TeamspeakStats/badge.svg?branch=master&service=github\n   :target: https://coveralls.io/github/Thor77/TeamspeakStats?branch=master\n.. |PyPI| image:: https://img.shields.io/pypi/v/tsstats.svg\n   :target: https://pypi.python.org/pypi/tsstats\n.. |Documentation Status| image:: https://readthedocs.org/projects/teamspeakstats/badge/?version=latest\n   :target: http://teamspeakstats.readthedocs.io/en/latest/?badge=latest\n",
    'author': 'Thor77',
    'author_email': 'thor77@thor77.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
