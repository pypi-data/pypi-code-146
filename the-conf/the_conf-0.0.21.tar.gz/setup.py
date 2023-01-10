# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['the_conf']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=5.3,<6.0']

setup_kwargs = {
    'name': 'the-conf',
    'version': '0.0.21',
    'description': 'Config build from multiple sources',
    'long_description': "[![Build Status](https://travis-ci.org/jaesivsm/the_conf.svg?branch=master)](https://travis-ci.org/jaesivsm/the_conf) [![Coverage Status](https://coveralls.io/repos/github/jaesivsm/the_conf/badge.svg?branch=master)](https://coveralls.io/github/jaesivsm/the_conf?branch=master)\n\nFrom [this](http://sametmax.com/les-plus-grosses-roues-du-monde/)\n\n    Une bonne lib de conf doit:\n\n    * Offrir une API standardisée pour définir les paramètres qu’attend son programme sous la forme d’un schéma de données.\n    * Permettre de générer depuis ce schéma les outils de parsing de la ligne de commande et des variables d’env.\n    * Permettre de générer depuis ce schéma des validateurs pour ces schémas.\n    * Permettre de générer des API pour modifier la conf.\n    * Permettre de générer des UIs pour modifier la conf.\n    * Séparer la notion de configuration du programme des paramètres utilisateurs.\n    * Pouvoir marquer des settings en lecture seule, ou des permissions sur les settings.\n    * Notifier le reste du code (ou des services) qu’une valeur à été modifiée. Dispatching, quand tu nous tiens…\n    * Charger les settings depuis une source compatible (bdd, fichier, api, service, etc).\n    * Permettre une hiérarchie de confs, avec une conf principale, des enfants, des enfants d’enfants, etc. et la récupération de la valeur qui cascade le long de cette hiérarchie. Un code doit pouvoir plugger sa conf dans une branche de l’arbre à la volée.\n    * Fournir un service de settings pour les architectures distribuées.\n    * Etre quand même utile et facile pour les tous petits scripts.\n    * Auto documentation des settings.\n\n\nBeforehand: for more clarity ```the_conf``` will designate the current program, its configuration will be referred to as the _meta conf_ and the configurations it will absorb (files / cmd line / environ) simply as the _configurations_.\n\n# 1. read the _meta conf_\n\n```the_conf``` should provide a singleton.\nOn instantiation the singleton would read the _meta conf_ (its configuration) from a file. YML and JSON will be considered first. This file will provide names, types, default values and if needed validator for options.\n\n```the_conf``` will the validate the conf file. For each config value :\n * if value has _choices_ and _default value_, _default value_ has to be among _choices_.\n * if the value is nested, a node can't hold anything else than values\n * _required_ values can't have default\n\n# 2. read the _configurations_\n\nOnce the _meta conf_ has been processed, ```the_conf``` will assemble all values at its reach from several sources.\nThree types are to be considered:\n * files (again YML/JSON but maybe also later ini)\n * command line\n * environ\nin this order of importance. This order must be itself overridable. ```the_conf``` must provide a backend for values from the configuration to be reached.\n\n```python\nthe_conf.load('path/to/meta/conf.yml')\nthe_conf.nested.value\n> 1\n```\n\nUpon reading _configurations_, ```the_conf``` will validate gathered values.\n * _configurations_ file type will be guessed from file extention (yaml / yml, json, ini), anything else must raise an error. Parsing errors won't also be silenced. Although, missing won't be an issue as long as all required values are gathered.\n * values must be in the type there declared in or cast to it without error\n * required values must be provided\n * if a value is configured with _choices_, the gathered value must be in _choices_\n\nThe first writable, readable available _configuration_ file found will be set as the main. Values will be edited on it but values from it will still be overridden according to the priorities. A warning should be issued if the main _configuration_ is overriddable.\nIf no suitable file is found, a warning should also be issued ; edition will be impossible and will generate an error.\n\n# 3. generate the _configurations_\n\nProvide an API to list and validate values needed from the _configurations_ (the required ones).\nProvide a command line UI to process that list to let a user generate a _configuration_ file.\n\n# 4. write the _configurations_\n\nDepending on the permissions set in the _meta conf_, ```the_conf``` must allow to edit the values in the configuration file set as _main_ on read phase.\nIf editing a value which will be ignored for being overriden, a warning must be issued.\n",
    'author': 'François Schmidts',
    'author_email': 'francois@schmidts.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jaesivsm/the_conf',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
