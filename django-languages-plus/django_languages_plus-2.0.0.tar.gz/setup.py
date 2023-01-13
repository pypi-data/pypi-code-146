# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['languages_plus', 'languages_plus.migrations']

package_data = \
{'': ['*'], 'languages_plus': ['data/*', 'fixtures/*']}

install_requires = \
['django-countries-plus>2', 'django>=3.2,<5']

setup_kwargs = {
    'name': 'django-languages-plus',
    'version': '2.0.0',
    'description': 'A django model & fixture containing common languages and culture codes',
    'long_description': "=============================\nDjango Languages Plus\n=============================\n\n.. image:: https://badge.fury.io/py/django-languages-plus.svg\n    :target: https://badge.fury.io/py/django-languages-plus\n\n.. image:: https://travis-ci.org/cordery/django-languages-plus.svg?branch=master\n    :target: https://travis-ci.org/cordery/django-languages-plus\n\n.. image:: https://codecov.io/gh/cordery/django-languages-plus/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/cordery/django-languages-plus\n\n\n\ndjango-languages-plus provides models and fixtures for working with both common languages and 'culture codes' or locale codes, like pt-BR.\n\nNote that this is only a small (but popular) subset of all living languages, and is not even a comprehensive set of the ISO 639 languages.  It does however include the endonym/autonym/exonym.\n\nThe Language model contains all ISO 639-1 languages and related information from http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes\n\nThe model provides the following fields (original wikipedia.org column name in parentheses).\n\n* name_en (ISO Language Name)\n* name_native (Native Name)\n* iso_639_1 (639-1)\n* iso_639_2T = (639-2/T)\n* iso_639_2B = (639-2/B)\n* iso_639_3 = (639-3)\n* family = (Language Family)\n* countries_spoken\n\n\n------------\nInstallation\n------------\n\n::\n\n    pip install django-languages-plus\n\n\n------------\nUsage\n------------\n\n1. Add ``languages_plus`` to your INSTALLED_APPS\n\n2. Migrate your database and load the language data fixture::\n\n        python manage.py migrate\n        python manage.py loaddata languages_data.json.gz\n\n3. In your code use::\n\n        from languages_plus.models import Language\n        lang = Language.objects.get(iso_639_1='en')\n\n---------------------------------------\nGenerating Culture Codes (ex: pt_BR)\n---------------------------------------\ndjango-countries-plus(https://pypi.python.org/pypi/django-countries-plus) is now an explicit requirement.  After installing both packages you can run the following command once to associate the two datasets and generate a list of culture codes (pt_BR for example)::\n\n        from languages_plus.utils import associate_countries_and_languages\n        associate_countries_and_languages()\n\n---------------------------------------\nRequirements\n---------------------------------------\ndjango-countries-plus >= 1.\n\nDjango:  Tested against the latest versions of 3, and 4.\nPython 3\n\n\nRunning Tests\n-------------\n\nDoes the code actually work?\n\n::\n\n    $ poetry install\n    $ poetry run pytest\n\nOr for the full tox suite:\n\n::\n\n    $ poetry install\n    $ pip install tox\n    $ tox\n",
    'author': 'Andrew Cordery',
    'author_email': 'cordery@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/cordery/django-languages-plus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
