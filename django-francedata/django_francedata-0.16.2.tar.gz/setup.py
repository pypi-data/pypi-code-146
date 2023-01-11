# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['francedata',
 'francedata.management',
 'francedata.management.commands',
 'francedata.migrations',
 'francedata.models',
 'francedata.resources',
 'francedata.services',
 'francedata.tests',
 'francedata.tests.services',
 'francedata.tests.testdata']

package_data = \
{'': ['*'], 'francedata': ['templates/desl_imports/admin/*']}

install_requires = \
['Django>=3.2.7,<4.0.0',
 'Unidecode>=1.2.0,<2.0.0',
 'django-json-widget>=1.1.1,<2.0.0',
 'django-ninja>=0.14.0,<0.15.0',
 'django-simple-history>=3.0.0,<4.0.0',
 'openpyxl-dictreader>=0.1.3,<0.2.0',
 'pandas>=1.3.4,<2.0.0',
 'psycopg2>=2.9.2,<3.0.0',
 'python-stdnum>=1.16,<2.0',
 'requests>=2.26.0,<3.0.0',
 'xlrd>=2.0.1,<3.0.0']

setup_kwargs = {
    'name': 'django-francedata',
    'version': '0.16.2',
    'description': 'A Django app to provide a database structure, API and import scripts to manage French communes, intercommunalités, départements and régions, with their structure and data from Insee and the DGCL.',
    'long_description': '.. image:: https://badge.fury.io/py/django-francedata.svg\n    :target: https://pypi.org/project/django-francedata/\n\n.. image:: https://github.com/entrepreneur-interet-general/django-francedata/actions/workflows/django.yml/badge.svg\n    :target: https://github.com/entrepreneur-interet-general/django-francedata/actions/workflows/django.yml\n\n.. image:: https://github.com/entrepreneur-interet-general/django-francedata/actions/workflows/codeql-analysis.yml/badge.svg\n    :target: https://github.com/entrepreneur-interet-general/django-francedata/actions/workflows/codeql-analysis.yml\n\n\n=================\nDjango-Francedata\n=================\n\nProvides a database structure, API and import scripts to manage French communes, intercommunalités, départements and régions, with their structure and data from Insee and the DGCL.\n\nThis app was created as a part of `Open Collectivités <https://github.com/entrepreneur-interet-general/opencollectivites>`_.\n\nUnaccent extension\n##################\n\nIf the PostgreSQL user specified in the Django settings is not a superuser, connect to the postgres user and create the Unaccent extension manually::\n\n    psql\n    \\c <dbname>\n    "CREATE EXTENSION  IF NOT EXISTS unaccent;"\n\nQuickstart\n##########\n\n1. Add "francedata" to your INSTALLED_APPS setting like this::\n\n    INSTALLED_APPS = [\n        ...\n        "django_json_widget",\n        "simple_history",\n        "francedata",\n    ]\n\n2. Run ``python manage.py migrate`` to create the francedata models.\n\n3. Run the two initialization commands to get the communes, EPCIs, départements and régions structure::\n\n    python manage.py cog_import\n    python manage.py banatic_import\n\n4. Visit http://127.0.0.1:8000/admin/ to see the data.\n  \nCommands\n########\n\ncog_import:\n***********\n\n* goal: load the following data from the Code officiel géographique (COG): list of regions, departements and communes, with how they are linked and:\n  * insee and siren ids for the regions/departements\n  * insee for the communes\n* parameters:\n  * --level: partial import of only the specified level (the script expects the higher ones to already be installed) Allowed values: `regions`, `departements`, `communes`\n  * --years: import the specified year (min: 2019), by default it imports the latest available one in https://www.data.gouv.fr/fr/datasets/code-officiel-geographique-cog/\n\nbanatic_import:\n***************\n\n* goal: load the following data from the Banatic:\n  * siren ids and population data for the communes\n  * insee for the communes\n* The script expects that `cog_import` was already run and that the communes level is passed before the epci level.\n* parameters:\n  * --level: partial import of only the specified level. Allowed values: `communes`, `epci`\n  * --years: import the specified year (min: 2019 for the communes level (data is taken from the file `Table de correspondance code SIREN / Code Insee des communes` from https://www.banatic.interieur.gouv.fr/V5/fichiers-en-telechargement/fichiers-telech.php ), by default it imports the latest available one)\n* warning: The epci level only works for the current year (data is taken from https://www.data.gouv.fr/fr/datasets/base-nationale-sur-les-intercommunalites/ )\n',
    'author': 'Sylvain Boissel',
    'author_email': 'sylvain.boissel@beta.gouv.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/entrepreneur-interet-general/django-francedata',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
