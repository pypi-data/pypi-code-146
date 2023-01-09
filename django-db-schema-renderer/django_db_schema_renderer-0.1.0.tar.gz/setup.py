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
    'version': '0.1.0',
    'description': 'Django app to render ER diagram',
    'long_description': '=============================\ndjango-db-schema-renderer app\n=============================\n\nApp to draw db-schema of selected apps, models.\n\nDetailed documentation is in the "docs" directory.\n\nQuick start\n-----------\n\n1. Add "django-db-schema-renderer" to your INSTALLED_APPS setting like this::\n    INSTALLED_APPS = [\n        \'django_db-schema_renderer\',\n        \'django.contrib.admin\',\n\n    ]\n\n\n2. Add app related urls to your root `urls.py`\n    from django_db_schema_renderer.urls import schema_urls\n    \n    urlpatterns = [\n    ...\n    path("db-schema/", include((schema_urls, "db-schema"))),\n    ...\n\n    ]\n\n3. Start the development server and visit http://127.0.0.1:8000/admin/\n   to render db-schema.\n\n',
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
