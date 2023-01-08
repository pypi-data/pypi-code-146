# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_mvc',
 'fastapi_mvc.cli',
 'fastapi_mvc.generators',
 'fastapi_mvc.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<8.2.0', 'copier==6.2.0']

entry_points = \
{'console_scripts': ['fastapi-mvc = fastapi_mvc.cli.cli:cli',
                     'fm = fastapi_mvc.cli.cli:cli']}

setup_kwargs = {
    'name': 'fastapi-mvc',
    'version': '0.24.0',
    'description': 'Developer productivity tool for making high-quality FastAPI production-ready APIs.',
    'long_description': '<div align="center">\n\n![fastapi-mvc](https://github.com/fastapi-mvc/fastapi-mvc/blob/master/docs/_static/logo.png?raw=true)\n\n![fastapi-mvc](https://github.com/fastapi-mvc/fastapi-mvc/blob/master/docs/_static/readme.gif?raw=true)\n[![CI](https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/main.yml)\n[![❄️ Nix CI ❄️](https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/nix.yml/badge.svg)](https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/nix.yml)\n[![codecov](https://codecov.io/gh/fastapi-mvc/fastapi-mvc/branch/master/graph/badge.svg?token=7ESV30TYZS)](https://codecov.io/gh/fastapi-mvc/fastapi-mvc)\n[![K8s integration](https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/integration.yml/badge.svg)](https://github.com/fastapi-mvc/fastapi-mvc/actions/workflows/integration.yml)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![PyPI](https://img.shields.io/pypi/v/fastapi-mvc)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/fastapi-mvc)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/fastapi-mvc)\n![GitHub](https://img.shields.io/github/license/fastapi-mvc/fastapi-mvc?color=blue)\n\n</div>\n\n---\n\n**Documentation**: [https://fastapi-mvc.netlify.app](https://fastapi-mvc.netlify.app)\n\n**Source Code**: [https://github.com/fastapi-mvc/fastapi-mvc](https://github.com/fastapi-mvc/fastapi-mvc)\n\n**Project scaffold**: [https://github.com/fastapi-mvc/copier-project](https://github.com/fastapi-mvc/copier-project)\n\n**Example generated project**: [https://github.com/fastapi-mvc/example](https://github.com/fastapi-mvc/example)\n\n---\n\nFastapi-mvc is a developer productivity tool for FastAPI web framework. \nIt is designed to make programming FastAPI applications easier by making assumptions about what every developer needs to get started. \nIt allows you to write less code while accomplishing more. Core features:\n\n* Generated project based on MVC architectural pattern\n* WSGI + ASGI production server\n* Generated project comes with Sphinx documentation and 100% tests coverage\n* Kubernetes deployment with Redis HA cluster\n* Makefile, GitHub actions and utilities\n* Helm chart for Kubernetes deployment\n* Dockerfile with K8s and cloud in mind\n* Generate pieces of code or even your own generators\n* Uses Poetry dependency management\n* Includes set of Nix expressions\n* Update already generated project with changes from the new template version\n* Virtualized reproducible development environment using Vagrant\n\nFastapi-mvc comes with a number of scripts called generators that are designed to make your development life easier by \ncreating everything that’s necessary to start working on a particular task. One of these is the new application generator, \nwhich will provide you with the foundation of a fresh FastAPI application so that you don’t have to write it yourself.\n\nCreating a new project is as easy as:\n\n```shell\n$ fastapi-mvc new /tmp/galactic-empire\n```\n\nThis will create a fastapi-mvc project called galactic-empire in a `/tmp/galactic-empire` directory and install its dependencies using `make install`.\n\nOnce project is generated and installed lets run development uvicorn server (ASGI):\n\n```shell\n$ cd /tmp/galactic-empire\n$ fastapi-mvc run\n```\n\nTo confirm it’s actually working:\n\n```shell\n$ curl 127.0.0.1:8000/api/ready\n{"status":"ok"}\n```\n\nNow let\'s add new API endpoints. For that we need to generate new controller:\n\n```shell\n$ fastapi-mvc generate controller death_star status load:post fire:delete\n```\n\nAnd then test generated controller endpoints:\n\n```shell\n$ curl 127.0.0.1:8000/api/death_star/status\n{"hello":"world"}\n$ curl -X POST 127.0.0.1:8000/api/death_star/load\n{"hello":"world"}\n$ curl -X DELETE 127.0.0.1:8000/api/death_star/fire\n{"hello":"world"}\n```\n\nYou will see it working in server logs as well:\n\n```shell\nINFO:     127.0.0.1:47284 - "GET /api/ready HTTP/1.1" 200 OK\nINFO:     127.0.0.1:55648 - "GET /api/death_star/status HTTP/1.1" 200 OK\nINFO:     127.0.0.1:55650 - "POST /api/death_star/load HTTP/1.1" 200 OK\nINFO:     127.0.0.1:55652 - "DELETE /api/death_star/fire HTTP/1.1" 200 OK\n```\n\nYou can get the project directly from PyPI:\n\n```shell\npip install fastapi-mvc\n```\n\nOr build with Nix from flake:\n\n```shell\n# Optionally setup fastapi-mvc Nix binary cache to speed up the build process\n# https://app.cachix.org/cache/fastapi-mvc#pull\nnix-env -iA cachix -f https://cachix.org/api/v1/install\ncachix use fastapi-mvc\n# Install with Nix from flake:\nnix build github:fastapi-mvc/fastapi-mvc#default --profile $HOME/.nix-profile\n```\n\n## Projects created with fastapi-mvc\n\nIf you have created a project with fastapi-mvc, feel free to open PR and add yourself to the list. Share your story and project. Your success is my success :)\n\nProjects:\n* [fastapi-mvc/example](https://github.com/fastapi-mvc/example) - Default generated project by `fastapi-mvc new ...`\n\n## Contributing\n\n[CONTRIBUTING](https://github.com/fastapi-mvc/fastapi-mvc/blob/master/CONTRIBUTING.md)\n\n## License\n\n[MIT](https://github.com/fastapi-mvc/fastapi-mvc/blob/master/LICENSE)\n',
    'author': 'Radosław Szamszur',
    'author_email': 'github@rsd.sh',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fastapi-mvc/fastapi-mvc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
