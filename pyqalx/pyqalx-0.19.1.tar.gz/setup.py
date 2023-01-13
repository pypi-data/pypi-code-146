# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyqalx',
 'pyqalx.bot',
 'pyqalx.config',
 'pyqalx.config.defaults',
 'pyqalx.core',
 'pyqalx.core.adapters',
 'pyqalx.core.entities',
 'pyqalx.factories',
 'pyqalx.factories.sectors',
 'pyqalx.factories.sectors.providers',
 'pyqalx.factories.sectors.providers.aws',
 'pyqalx.factories.sectors.providers.local',
 'pyqalx.transport',
 'pyqalx.vendor',
 'qalxcli',
 'qalxcli.cli']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2<3.1',
 'addict>=2.2,<3.0',
 'appdirs>=1.4,<2.0',
 'boto3>=1.12.31,<2.0.0',
 'bson-extra>=0.0.4,<0.0.5',
 'click>=8.0,<9.0',
 'colorama>=0.4.3,<0.5.0',
 'cryptography>=35.0.0,<36.0.0',
 'deprecation>=2.0,<3.0',
 'dill>=0.3.3',
 'gitpython>=3.1,<4.0',
 'jsonschema>=3.0,<4.0',
 'pyyaml>=5.3,<6.0',
 'requests>=2.21,<3.0',
 'tabulate>=0.8.10,<0.9.0',
 'treelib>=1.6,<2.0',
 'troposphere>=3.1.1,<4.0.0']

extras_require = \
{'flaky': ['flaky>=3.5,<4.0'],
 'pip-licenses': ['pip-licenses>=3.5.3,<4.0.0'],
 'sphinx': ['sphinx>=2.0,<3.0']}

entry_points = \
{'console_scripts': ['qalx = qalxcli.cli.qalx:qalx']}

setup_kwargs = {
    'name': 'pyqalx',
    'version': '0.19.1',
    'description': 'High-level interfaces to the qalx API',
    'long_description': 'pyqalx\n======\n.. image:: https://img.shields.io/bitbucket/pipelines/agiletekengineering/pyqalx   :alt: Bitbucket Pipelines\n\n\n.. image:: https://api.codacy.com/project/badge/Grade/fdfb81fd286a474098b624b426d63c41\n    :target: https://www.codacy.com?utm_source=bitbucket.org&amp;utm_medium=referral&amp;utm_content=agiletekengineering/pyqalx&amp;utm_campaign=Badge_Grade\n\n\n.. image:: https://api.codacy.com/project/badge/Coverage/fdfb81fd286a474098b624b426d63c41\n    :target: https://www.codacy.com?utm_source=bitbucket.org&amp;utm_medium=referral&amp;utm_content=agiletekengineering/pyqalx&amp;utm_campaign=Badge_Coverage\n\n\nInterfaces to qalx. For more details, see `project documentation, <http://docs.qalx.net>`_.\n\n.. admonition:: development status\n\n   ``pyqalx`` is currently under active development. It is pre-version 1.0 beta software and so each minor version\n   can introduce breaking changes.\n\n**qalx** (an abbreviation of "queued calculations" and pronounced "kal-x") is a flexible data management platform for engineering projects. Users store data and files in qalx and it provides tools for passing that data between various systems for processing.\n\nThere will eventually be four ways to interact with the platform:\n\n-  A Python interface (pyqalx)\n-  REST API (api.qalx.net)\n-  Web console (console.qalx.net) - coming soon\n-  A command line interface (qalx-cli) - coming soon\n\nMost users are expected to use the web console and either the python or\ncommand line interfaces. The REST API is intended to be used if you\nprefer to access the platform with a language other than Python or want\nto create a custom interface.\n\n.. _installing:\n\nInstalling\n==========\n\n**qalx** is written in `Python <https://python.org>`_ and can be\ninstalled via the Python Package Index (PyPi) with:\n\n.. code:: bash\n\n   pip install pyqalx\n\nIf installation has completed properly you should be able to import\n``pyqalx`` in a python console:\n\n>>> import pyqalx\n\n.. warning::\n\n      pyqalx requires **Python versions above 3.6**.\n\n\nConfiguration and Authentication\n--------------------------------\n\nEverything you do with **qalx** requires you to be authenticated. That\nis, the platform requires you to identify yourself and will record all\nyour actions as being performed by you.\n\nThe way that **qalx** knows who you are is by reading a ``TOKEN``\nwhich must be sent with every request.\n\n.. warning::\n   During this beta phase, you have to request a ``TOKEN`` by registering your interest at `qalx.net <https://qalx.net>`_\n\nThe easiest way to make sure that your token is sent with every request is to make sure you have a valid ``.qalx`` file\nsaved in your HOME directory.\n\n.. admonition::  where is ``HOME``?\n\n   The ``HOME`` directory can usually be found by putting %USERPROFILE%\n   in the address bar in Windows Explorer or it is simply ``~`` on unix\n   systems.\n\n\nqalx CLI configure\n------------------\nYou can either add the ``TOKEN`` manually to the config file or you can use the **qalx** cli to do this for you automatically\n\n.. code:: bash\n\n   $ qalx configure\n\nThe above command will ask you all the necessary questions to create your user and bot config files.\n\nYou can also create other profiles using the ``qalx configure`` command. You can even create profiles just for bots\nor just for users - or provide extra arguments to write to the config\n\n.. code:: bash\n\n   # Will write a user profile called `dev` to the config file,\n   # will also write a `default` bot config profile\n   $ qalx --user-profile dev configure\n\n   # Will write a bot profile called `dev` to the config file,\n   # will also write a `default` user config profile\n   $ qalx --bot-profile dev configure\n\n   # Will not write the bot profile\n   $ qalx configure --no-bot\n\n   # Will not write the user profile\n   $ qalx configure --no-user\n\n   # Will write a default user and bot profile and will also write two\n   # extra keys to each config - `CUSTOMKEY=customvalue`\n   # and `CUSTOMKEY2=customvalue2`\n   $ qalx configure customkey=customvalue customkey2=customvalue2\n\nManual configuration\n--------------------\n\nIf you don\'t want to use the ``qalx cli`` to configure your profile (or if you want to make changes to it in the future)\nthen you can configure the profile yourself by adding the ``TOKEN`` to your config file under\nthe default profile.\n\n.. code:: ini\n\n   [default]\n   TOKEN = 632gd7yb9squd0q8sdhq0s8diqsd0nqsdq9sdk\n\nAny other configuration settings can be stored in the same file see `<configuration>`_ for more information.\n\nQuickstart\n----------\n\nThe best place to get started: `<https://docs.qalx.net/quickstart>`_\n\n\n\n',
    'author': 'AgileTek Engineering Limited',
    'author_email': 'london@agiletek.co.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://qalx.net',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
