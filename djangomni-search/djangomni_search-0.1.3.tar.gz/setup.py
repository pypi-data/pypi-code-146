# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['djangomni_search']

package_data = \
{'': ['*'],
 'djangomni_search': ['static/djangomni-search/*', 'templates/admin/*']}

setup_kwargs = {
    'name': 'djangomni-search',
    'version': '0.1.3',
    'description': 'Quick search anything in Django Admin from a single place',
    'long_description': '# djangomni-search\n\n> Django Admin Site extension, that allows searching all entities from single\n> field\n\n## Installation\n\nPlease read the instructions carefully, extending Django Admin on this level\ncan go wrong very easily.\n\n### 1. Pip your deps\n\nBasically, install the dependency. You can use `poetry`, or any other package\nmanager.\n\n```shell\npip install djangomni-search\n```\n\n### 2. Put `djangomni_search` into `INSTALLED_APPS`\n\nIt is important to put it on the top.\n\n```python\nINSTALLED_APPS = [\n    \'djangomni_search\',\n    \'django.contrib.admin\',\n    \'django.contrib.auth\',\n    \'...\',\n]\n```\n\n### 3. Configure Admin Site\n\nNow you will need to configure your Admin Site(s) to inherit from\n`djangomni_search.admin.OmniSearchAdminSite`. If you\'re using the default\n[AdminSite](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/), you must\n[create a custom\none](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#overriding-default-admin-site).\n\n```python\nclass SiteAdmin(OmniSearchAdminSite, AdminSite):\n    ...\n```\n\n### 4. Extend your custom `base_site.html`\n\nIf you do not have a custom `base_site.html`, it should already work. In case you have done some customizations to your base site file, you will need to add one script to all pages in admin. This can be only done by\nextending the base template.\n\n```\n{% block extrahead %}\n{% if omni_search %}\n  <link\n    href="{% static \'djangomni-search/main.css\' %}"\n    rel="stylesheet"\n    type="text/css"\n  />\n  <script\n    data-config="{{omni_search}}"\n    id="djangomni-search"\n    src="{% static \'djangomni-search/main.js\' %}"\n  ></script>\n{% endif %}\n{% endblock %}\n```\n\n### 5. Configure autocomplete\n\nThe Omni Search looks for data using the [`autocomplete_fields`](https://docs.djangoproject.com/en/4.1/ref/contrib/admin/#django.contrib.admin.ModelAdmin.autocomplete_fields) attribute of `ModelAdmin`. Configure it for all the models, that you want to search.\n',
    'author': 'Pavel Žák',
    'author_email': 'pavel@zak.global',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
