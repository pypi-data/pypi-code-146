# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['flake8_flask_openapi_docstring']

package_data = \
{'': ['*']}

install_requires = \
['apispec>3', 'pyyaml>=5.4']

entry_points = \
{'flake8.extension': ['FO1 = '
                      'flake8_flask_openapi_docstring:FlaskOpenAPIDocStringLinter']}

setup_kwargs = {
    'name': 'flake8-flask-openapi-docstring',
    'version': '0.1.2',
    'description': 'A Flake8 plugin to enforce OpenAPI docstrings in Flask routes',
    'long_description': '# flake8-flask-openapi-docstring\n\nThis Flake8 plugin will check if your Flask route\'s docstrings are valid OpenAPI spec.\n\nLibraries like [APISpec](https://apispec.readthedocs.io/en/latest/) can generate OpenAPI spec from your Flask routes and docstrings and it\'s important to have present and in the correct format.\n\nfor example, this routes:\n\n```python\n@app.route("/hello", methods=["GET"])\ndef hello():\n    return "Hello World!"\n```\n\nwill raise an error witht his plugin because not only the docstring is missing but also the OpenAPI spec is missing as well.\n\nHowever these route:\n\n```python\n@app.route("/hello", methods=["GET"])\ndef hello():\n    """\n    Returns a greeting\n\n    ---\n    get:\n        responses:\n            200:\n    """\n    return "Hello World!"\n```\n\nwill not raise any error because the docstring is present and the OpenAPI spec is present as well.\n',
    'author': 'Daniele Esposti',
    'author_email': 'daniele.esposti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/expobrain/flake8-flask-openapi-docstring',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.12',
}


setup(**setup_kwargs)
