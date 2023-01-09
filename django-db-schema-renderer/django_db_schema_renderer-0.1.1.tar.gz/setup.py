# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_db_schema_renderer']

package_data = \
{'': ['*'], 'django_db_schema_renderer': ['templates/*', 'templates/admin/*']}

install_requires = \
['Django>=3.2', 'django-extensions>=3.2.1,<4.0.0', 'pygraphviz>=1.10,<2.0']

setup_kwargs = {
    'name': 'django-db-schema-renderer',
    'version': '0.1.1',
    'description': 'Django app to render ER diagram',
    'long_description': '# Django-db-schema-renderer\n\n## Overview\n\nThis is a django app to render db schema (ER diagram), of selected models or apps inside django admin panel\n\n## Requirements\n\n- Python 3.7+\n- Django 3.1+\n- django-extensions 3+\n- pygraphviz 1.7+\n\nFor successful install of pygraphviz you need to have on your host graphviz installed. you can find official docs [here](https://graphviz.org/download/)\nOn apple silicon this can be achieved by running command:\n\n```bash\nbrew install graphviz\npip3 install \\\n    --global-option=build_ext \\\n    --global-option="-I$(brew --prefix graphviz)/include/" \\\n    --global-option="-L$(brew --prefix graphviz)/lib/" \\\n    pygraphviz\n```\n\n\n# Installation\n\n1. Install using `pip`...\n\n   pip install django-db-schema-renderer\n\n2. Add `django_db_schema_renderer` to your `INSTALLED_APPS` setting, before `django.contrib.admin`(make sure you have `django-extensions` also added)\n\n   ```python\n   INSTALLED_APPS = [\n       \'django_db_schema_renderer\',\n       \'django.contrib.admin\',\n       ...\n       \'django-extensions\'\n\n   ]\n   ```\n\n3. Edit the `{project_dir}/urls.py` module in your project:\n\n   ```python\n   from django_db_schema_renderer.urls import schema_urls\n\n   urlpatterns = [\n   ...\n    path("db-schema/", include((schema_urls, "db-schema"))),\n   ...\n   ]\n\n   ```\n',
    'author': 'Oleksandr Korol',
    'author_email': 'oleksandr.korol@coaxsoft.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
