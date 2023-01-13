# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['highlightjs', 'highlightjs.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['Django==4.1']

setup_kwargs = {
    'name': 'django-highlightjs',
    'version': '0.2.6',
    'description': 'A Django app to easyily integrate highlight.js syntax highlighter.',
    'long_description': '=============================\nWelcome to django-highlightjs\n=============================\n\n.. image:: https://coveralls.io/repos/MounirMesselmeni/django-highlightjs/badge.png?branch=main\n  :target: https://coveralls.io/r/MounirMesselmeni/django-highlightjs?branch=main\n\n\n.. image:: https://img.shields.io/pypi/v/django-highlightjs.svg\n    :target: https://pypi.python.org/pypi/django-highlightjs/\n    :alt: Latest Version\n\n\nUse Highlight.js (https://highlightjs.org) in your Django templates, the Django way.\n\n\nInstallation\n------------\n\n1. Install using pip:\n\n   ``pip install django-highlightjs``\n\n   Alternatively, you can install download or clone this repo and call ``pip install -e .``.\n\n2. Add to INSTALLED_APPS in your ``settings.py``:\n\n   ``\'highlightjs\',``\n\n3. In your templates, load the ``highlightjs`` library and use the ``highlightjs_*`` tags:\n\nSettings\n--------\n\nThe django-highlightjs has some pre-configured settings.\nThey can be modified by adding a dict variable called ``HIGHLIGHTJS`` in your ``settings.py`` and customizing the values you want.\nThe ``HIGHLIGHTJS`` dict variable is contains these settings and defaults:\n\n   .. code:: Python\n\n    HIGHLIGHTJS = {\n      # The URL to the jQuery JavaScript file\n      \'jquery_url\': \'//code.jquery.com/jquery.min.js\',\n      # The highlight.js base URL\n      \'base_url\': \'//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js\',\n      # The complete URL to the highlight.js CSS file\n      \'css_url\': \'//cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/{0}.min.css\',\n      # Include jQuery with highlight.js JavaScript (affects django-highlightjs template tags)\n      \'include_jquery\': False,\n      # The default used style.\n      \'style\': \'monokai_sublime\',\n      }\n\n\nUsage in your `settings.py`:\n   .. code:: Python\n\n    HIGHLIGHTJS = {\n      \'style\': \'github\',\n    }\n\nAll other styles available at https://github.com/isagalaev/highlight.js/tree/main/src/styles\n\n\nExample template\n----------------\n\n   .. code:: Django\n\n    {% load highlightjs %}\n    <html>\n    <head>\n      <link href="{% highlightjs_css_url %}" rel=\'stylesheet\' type=\'text/css\'>\n    </head>\n    <body>\n        {# Highlight Syntax using Highlightjs #}\n\n        {% highlightjs_this code_to_highlight %}\n        {% highlightjs_this code_to_highlight \'python\' %}\n\n        {% highlightjs_javascript jquery=1 %}\n    </body>\n    </html>\n\n\nRequirements\n------------\n\n- Python 3.8, 3.9, 3.10 or 3.11\n- Django >= 3\n\nContributions and pull requests for other Django and Python versions are welcome.\n\n\nBugs and requests\n-----------------\n\nIf you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.\n\nhttps://github.com/MounirMesselmeni/django-highlightjs/issues\n\n\nLicense\n-------\n\nYou can use this under MIT See `LICENSE\n<LICENSE>`_ file for details.\n\n\nAuthor\n------\n\nMy name is Mounir Messelmeni, you can reach me at messelmeni.mounir@gmail.com .\n',
    'author': 'Mounir Messelmeni',
    'author_email': 'messelmeni.mounir@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mounirmesselmeni/django-highlightjs/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
