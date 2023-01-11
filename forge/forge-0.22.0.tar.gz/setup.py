# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['forge', 'forge.auth', 'forge.forms', 'forge.views']

package_data = \
{'': ['*'],
 'forge.forms': ['templates/django/forms/*',
                 'templates/django/forms/errors/list/*']}

install_requires = \
['Django>=4.0,<5.0',
 'black>=22.12.0,<23.0.0',
 'click>=8.1.0,<9.0.0',
 'coverage>=7.0.1,<8.0.0',
 'dj-database-url>=1.0.0,<2.0.0',
 'django-widget-tweaks>=1.4.12,<2.0.0',
 'forge-core<1.0.0',
 'forge-db>=0.3.0,<0.4.0',
 'forge-heroku<1.0.0',
 'forge-tailwind<1.0.0',
 'forge-work<1.0.0',
 'hiredis>=2.0.0,<3.0.0',
 'ipython>=8.5.0,<9.0.0',
 'pytest-django>=4.5.2,<5.0.0',
 'pytest>=7.0.0,<8.0.0',
 'python-dotenv',
 'redis>=4.2.2,<5.0.0',
 'ruff>=0.0.194,<0.0.195',
 'whitenoise>=6.0.0,<7.0.0']

entry_points = \
{'console_scripts': ['forge = forge.cli:cli']}

setup_kwargs = {
    'name': 'forge',
    'version': '0.22.0',
    'description': 'Quickly build a professional web app using Django.',
    'long_description': '# Forge\n\n<img height="100" width="100" src="https://user-images.githubusercontent.com/649496/176748343-3829aad8-4bcf-4c25-bb5d-6dc1f796fac0.png" align="right" />\n\n**Quickly build a professional web app using Django.**\n\nForge is a set of packages and opinions for how to build with Django.\nIt guides how you work,\nchooses what tools you use,\nand makes decisions so you don\'t have to.\n\nAt it\'s core,\nForge *is* Django.\nBut we\'ve taken a number of steps to make it even easier to build and deploy a production-ready app on day one.\n\nIf you\'re an experienced Django user,\nyou\'ll understand and (hopefully) agree with some of Forge\'s opinions.\nIf you\'re new to Django or building web applications,\nwe\'ve simply removed questions that you might not even be aware of.\n\nForge will get you from *zero to one* on a revenue-generating SaaS, internal business application, or hobby project.\n\nMore details can be found on [forgepackages.com](https://www.forgepackages.com/).\n\n## Quickstart\n\nStart a new project in 5 minutes:\n\n```sh\ncurl -sSL https://forgepackages.com/quickstart.py | python3 - my-project\n```\n\n[![Forge Django quickstart](https://user-images.githubusercontent.com/649496/173145833-e4f96a4c-efb6-4cc3-b118-184be1a007f1.png)](https://www.youtube.com/watch?v=wYMRxTGDmdU)\n',
    'author': 'Dave Gaeddert',
    'author_email': 'dave.gaeddert@dropseed.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.forgepackages.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
