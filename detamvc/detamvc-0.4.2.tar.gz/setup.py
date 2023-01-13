# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['detamvc',
 'detamvc.templates.authlib_users',
 'detamvc.templates.core',
 'detamvc.templates.core.static_pages',
 'detamvc.templates.mkdocs_core',
 'detamvc.templates.scaffold']

package_data = \
{'': ['*'],
 'detamvc': ['templates/authlib_users/templates/*',
             'templates/core/static_pages/static/css/*',
             'templates/core/static_pages/static/img/*',
             'templates/core/static_pages/static/js/*',
             'templates/core/static_pages/templates/*',
             'templates/mkdocs_core/docs/*',
             'templates/mkdocs_core/docs/assets/css/*',
             'templates/mkdocs_core/docs/assets/img/*',
             'templates/mkdocs_core/docs/tutorial/*',
             'templates/scaffold/templates/*',
             'templates/scaffold_helpers/*']}

install_requires = \
['Jinja2>=3.1.2,<4.0.0',
 'authlib>=1.2.0,<2.0.0',
 'deta>=1.1.0,<2.0.0',
 'fastapi>=0.78.0,<0.79.0',
 'httpx>=0.23.1,<0.24.0',
 'itsdangerous>=2.1.2,<3.0.0',
 'mkdocs-material>=8.5.7,<9.0.0',
 'odetam>=1.2.0,<2.0.0',
 'python-dotenv>=0.20.0,<0.21.0',
 'python-multipart>=0.0.5,<0.0.6',
 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['detamvc = detamvc.main:app']}

setup_kwargs = {
    'name': 'detamvc',
    'version': '0.4.2',
    'description': '',
    'long_description': '![DetaMVC](https://detamvc.deta.dev/assets/images/detamvc.png)    \n\n\n**Documentation:** [https://detamvc.deta.dev](https://detamvc.deta.dev)  \n**Source Code:** [https://github.com/pyn-sol/detaMVC](https://github.com/pyn-sol/detaMVC)  \n\n\nDetaMVC is a framework for rapidly developing and deploying web applications using:\n- [FastAPI](https://fastapi.tiangolo.com/)\n- [Jinja2](https://fastapi.tiangolo.com/advanced/templates/?h=jinja2)\n- [Deta](https://docs.deta.sh/docs/home)  \n\n\n## Installation\n```\npip install detamvc\n```\n\nOther Requirements:\n- A Deta Account. If you do not have one, go to [Deta](https://www.deta.sh/) and click \'Join Deta\'\n- The [Deta CLI](https://docs.deta.sh/docs/cli/install)\n\n\n## Basics\nIf you are familiar with Ruby on Rails, the commands are very similar for creating an application. \n\n```\ndetamvc new project\n\ncd project\n\ndetamvc scaffold item name:str description:text price:float quantity:int available:bool\n```\n\nBefore running your project, be sure to set your PROJECT_KEY for Deta. You can get this from your Deta dashboard under \'settings\'.\n\n\n```\necho DETA_PROJECT_KEY="#######_#############" > .env\n```\n\nOr, save yourself the hassle and set your development project key using the command. Hint: Do this _before_ creating a new project.\n\n```\ndetamvc set-project-key #######_#################\n```\n\n## Run a Server Manually\n\nThis assumes you have uvicorn installed. You can run with other servers as you wish - just set up like you would for a normal [FastAPI](https://fastapi.tiangolo.com/deployment/manually/ "Run a Server Manually - Uvicorn") application.\n```\ndetamvc s\n```\nor\n```\nuvicorn main:app --reload\n```\n\n## Deploy on Deta\nNow you can deploy this on Deta!\nBefore running the following, you will need to install the [Deta CLI](https://docs.deta.sh/docs/cli/install)\n```\ndeta new --project default\n```',
    'author': 'MBeebe',
    'author_email': 'grow.food.everywhere@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
